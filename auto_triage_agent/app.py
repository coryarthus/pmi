# app.py
import streamlit as st
import openai
import json
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

openai.api_key = st.secrets.get("openai_api_key")

user_input = st.text_area("Enter customer question:", height=150)

if st.button("Submit") and user_input:
    with st.spinner("Generating summary..."):
        summary_prompt = f"Summarize the following customer question clearly and concisely:\n{user_input}"
        summary_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        summary = summary_response.choices[0].message.content.strip()

    st.markdown("### ✍️ Summary")
    st.markdown(summary)

    if st.button("Confirm Summary"):
        with st.spinner("Classifying intent..."):
            categorization_prompt = generate_categorization_prompt(summary, medical_types, non_medical_types)
            categorization_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": categorization_prompt}]
            )
            result_text = categorization_response.choices[0].message.content.strip()
            try:
                result_json = json.loads(result_text)
            except json.JSONDecodeError:
                st.error("🔴 Failed to parse categorization result.")
                st.code(result_text)
                st.stop()

        if validate_output(result_json, medical_types + non_medical_types):
            st.markdown("### ✅ Categorization Result")
            st.json(result_json)

            if result_json["confidence"] < 1.0:
                st.warning("Confidence is below 100%. Defaulting to medical referral.")
                st.markdown("[Visit Medical Information Site](https://yourcompany.com/medical-information)")
            elif result_json["category"] == "Medical":
                st.markdown("🔹 Question is Medical. [Refer to Medical Info Site](https://yourcompany.com/medical-information)")
            else:
                st.markdown("🔹 Question is Non-Medical.")
                match = next((t for t in non_medical_types if t["type"] == result_json["type"]), None)
                if match:
                    st.markdown(f"**Automated Response:**\n{match['description']}")
        else:
            st.error("🔴 Categorization output failed schema validation.")
            st.code(result_text)
