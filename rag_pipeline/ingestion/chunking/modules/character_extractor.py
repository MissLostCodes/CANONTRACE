import re

def extract_characters(text: str, canonical_map: dict) -> list[str]:
    """
    canonical_map:
    {
      "edmond_dantes": {
          "canonical_name": "Edmond Dantès",
          "aliases": ["Edmond", "Dantès", "Edmond Dantès"]
      }
    }
    """
    found = set()

    for char_id, data in canonical_map.items():
        for alias in data["aliases"]:
            if re.search(rf"\b{re.escape(alias)}\b", text, re.IGNORECASE):
                found.add(char_id)
                break

    return sorted(found)
