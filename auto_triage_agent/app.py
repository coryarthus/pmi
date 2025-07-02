# app.py
import streamlit as st
import json
from openai import OpenAI
from schema import medical_types, non_medical_types

def generate_categorization_prompt(summary, medical_types, non_medical_types):
    all_types = medical_types + non_medical_types
    types_json = json.dumps(all_types, indent=2)

    return f"""
You are an AI assistant tasked with triaging customer questions for a pharmaceutical company.

Classify the following question summary:
\"{summary}\"

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

# --- Streamlit UI ---
st.set_page_config(page_title="Auto-Triage Agent", layout="centered")
st.title("🧠 Conversational Auto-Triage Agent")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Initialize session state
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "confirmed" not in st.session_state:
    st.session_state.confirmed = False
if "result_text" not in st.session_state:
    st.session_state.result_text = ""

user_input = st.text_area("Enter customer question:", height=150)

if st.button("Submit") and user_input:
    with st.spinner("Generating summary..."):
        summary_prompt = f"Summarize the following customer question clearly and concisely:\n{user_input}"
        summary_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        st.session_state.summary = summary_response.choices[0].message.content.strip()
        st.session_state.confirmed = False
        st.session_state.result_text = ""

if st.session_state.summary:
    st.markdown("### ✍️ Summary")
    st.markdown(st.session_state.summary)

    if not st.session_state.confirmed:
        if st.button("Confirm Summary"):
            st.session_state.confirmed = True

if st.session_state.confirmed and not st.session_state.result_text:
    with st.spinner("Classifying intent..."):
        categorization_prompt = generate_categorization_prompt(
            st.session_state.summary, medical_types, non_medical_types
        )
        categorization_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": categorization_prompt}]
        )
        st.session_state.result_text = categorization_response.choices[0].message.content.strip()

if st.session_state.result_text:
    st.markdown("### 🧪 Raw LLM Response")
    st.code(st.session_state.result_text)

