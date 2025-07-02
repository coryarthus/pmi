# app.py
import streamlit as st
import json
import sys
from openai import OpenAI
from schema import medical_types, non_medical_types

MAX_CLARIFY_ATTEMPTS = 3
CONFIDENCE_THRESHOLD = 0.85

client = OpenAI(api_key=st.secrets["openai_api_key"])

def generate_summary_prompt(question, additional_details=""):
    base = f"Summarize the following customer question clearly and concisely:\n{question}"
    if additional_details.strip():
        base += f"\nAdditional details: {additional_details}"
    return base

def generate_categorization_prompt(summary, medical_types, non_medical_types, clarifications):
    all_types = medical_types + non_medical_types
    types_json = json.dumps(all_types, indent=2)
    clar_text = "\n".join(f"- {c}" for c in clarifications)
    prompt = f"""
You are an AI assistant tasked with triaging customer questions for a pharmaceutical company.

Classify the following question summary:
\"\"\"{summary}\"\"\"

Use the following clarifying info from user to assist classification:
{clar_text if clar_text else '(none)'}

Choose one category and one type from the structured list below.

Only respond with a JSON object in this format:
{{
  "category": "Medical" or "Non-Medical",
  "type": "exact type name",
  "confidence": number between 0.0 and 1.0
}}

Use this schema to guide your classification:
{types_json}

If you are less than 100% confident, set confidence < 1.0.
"""
    return prompt

def validate_output(response_json, schema):
    categories = {"Medical", "Non-Medical"}
    valid_types = {entry["type"] for entry in schema}
    try:
        category = response_json["category"]
        type_ = response_json["type"]
        confidence = float(response_json["confidence"])
        return category in categories and type_ in valid_types and 0 <= confidence <= 1
    except (KeyError, ValueError, TypeError):
        return False

def get_static_response(non_medical_type):
    for entry in non_medical_types:
        if entry["type"] == non_medical_type:
            return entry.get("static_response") or entry.get("description") or ""
    return ""

def safe_rerun():
    """Force Streamlit to rerun the script."""
    sys.exit()

# --- Initialize session state ---
if "question" not in st.session_state:
    st.session_state.question = ""
if "additional_details" not in st.session_state:
    st.session_state.additional_details = ""
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "summary_accepted" not in st.session_state:
    st.session_state.summary_accepted = None  # None means no answer yet
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
if "result_text" not in st.session_state:
    st.session_state.result_text = ""
if "clarify_attempts" not in st.session_state:
    st.session_state.clarify_attempts = 0
if "clarifying_answers" not in st.session_state:
    st.session_state.clarifying_answers = []
if "awaiting_clarification" not in st.session_state:
    st.session_state.awaiting_clarification = False

st.set_page_config(page_title="Auto-Triage Agent", layout="centered")
st.title("🧠 Conversational Auto-Triage Agent")

# === Debug info ===
st.caption(f"Debug: awaiting_clarification={st.session_state.awaiting_clarification}, clarify_attempts={st.session_state.clarify_attempts}")

# --- Step 1: Input initial question ---
if st.session_state.summary_accepted is None:
    user_question = st.text_area("Enter your question:", value=st.session_state.question, height=150)
    if st.button("Submit") and user_question.strip():
        st.session_state.question = user_question.strip()
        st.session_state.additional_details = ""
        st.session_state.summary_accepted = None
        st.session_state.confirmed = False
        st.session_state.result_text = ""
        st.session_state.clarify_attempts = 0
        st.session_state.clarifying_answers = []
        st.session_state.awaiting_clarification = False

        with st.spinner("Generating summary..."):
            prompt = generate_summary_prompt(st.session_state.question)
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            st.session_state.summary = response.choices[0].message.content.strip()
        st.session_state.summary_accepted = False  # Show summary for accept/reject

# --- Step 2: Show summary and ask to accept or reject ---
if st.session_state.summary and st.session_state.summary_accepted is False:
    st.markdown("### ✍️ Summary of your question:")
    st.markdown(st.session_state.summary)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Accept Summary"):
            st.session_state.summary_accepted = True
            st.session_state.confirmed = True
    with col2:
        if st.button("Reject Summary"):
            st.session_state.summary_accepted = None  # Back to question input
            st.session_state.additional_details = ""
            st.session_state.summary = ""
            st.session_state.confirmed = False
            safe_rerun()

# --- Step 3: If summary accepted, proceed to classification ---
if st.session_state.summary_accepted:
    # Show clarifying input box if awaiting clarification
    if st.session_state.awaiting_clarification:
        st.markdown(f"### 🤔 Clarifying question (attempt {st.session_state.clarify_attempts + 1} of {MAX_CLARIFY_ATTEMPTS}):")
        clar_answer = st.text_area("Please provide more details to help clarify your question:", height=100)
        if st.button("Submit Clarification"):
            if clar_answer.strip():
                st.session_state.clarifying_answers.append(clar_answer.strip())
                st.session_state.clarify_attempts += 1
                st.session_state.awaiting_clarification = False
                st.session_state.result_text = ""  # Clear old result to re-classify
                safe_rerun()
            else:
                st.warning("Please enter details before submitting.")
    else:
        if not st.session_state.result_text:
            with st.spinner("Classifying intent..."):
                prompt = generate_categorization_prompt(
                    st.session_state.summary,
                    medical_types,
                    non_medical_types,
                    st.session_state.clarifying_answers,
                )
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                )
                st.session_state.result_text = response.choices[0].message.content.strip()

        if st.session_state.result_text:
            st.markdown("### 🧪 Raw LLM Response")
            st.code(st.session_state.result_text)

            try:
                result_json = json.loads(st.session_state.result_text)
            except json.JSONDecodeError as e:
                st.error("🔴 Failed to parse categorization result.")
                st.code(str(e))
                st.stop()

            if not validate_output(result_json, medical_types + non_medical_types):
                st.error("🔴 Categorization output failed schema validation.")
                st.stop()

            confidence = float(result_json["confidence"])

            if confidence < CONFIDENCE_THRESHOLD:
                if st.session_state.clarify_attempts < MAX_CLARIFY_ATTEMPTS:
                    if not st.session_state.awaiting_clarification:
                        st.session_state.awaiting_clarification = True
                    st.info(
                        f"Confidence ({confidence:.2f}) is below threshold ({CONFIDENCE_THRESHOLD}). "
                        "Please provide more information to clarify your question."
                    )
                else:
                    st.warning(
                        "Maximum clarifying attempts reached without high confidence. "
                        "Defaulting to Medical Information referral."
                    )
                    st.markdown("[Visit Medical Information Site](https://yourcompany.com/medical-information)")
                    if st.button("Start Over"):
                        st.session_state.clear()
                        safe_rerun()
            else:
                st.markdown("### ✅ Categorization Result")
                st.json(result_json)

                if (
                    result_json["category"] == "Medical"
                    or confidence < 1.0
                ):
                    st.warning("Refer the user to Medical Information.")
                    st.markdown("[Visit Medical Information Site](https://yourcompany.com/medical-information)")
                else:
                    st.markdown(f"🔹 Question is Non-Medical, Type: **{result_json['type']}**")
                    static_response = get_static_response(result_json["type"])
                    if static_response:
                        st.markdown(f"**Automated Response:** {static_response}")

                if st.button("Start Over"):
                    st.session_state.clear()
                    safe_rerun()
                    