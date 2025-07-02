import json

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