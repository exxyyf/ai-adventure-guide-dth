import json

def parse_pixtral_json_simple(text: str) -> dict:
    """Simple parsing of pixtral response"""
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        data = json.loads(text[start:end])

        return {
            "name": data.get("name", "Unknown"),
            "location": data.get("location", "Unknown"),
            "setting": data.get("setting", "Unknown"),
        }

    except Exception:
        return {
            "name": "Unknown",
            "location": "Unknown",
            "setting": "Unknown",
        }
