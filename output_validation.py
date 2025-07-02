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