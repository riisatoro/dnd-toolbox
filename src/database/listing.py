import json
import os


def get_available_characters():
    uuids = os.listdir("database/sheets")
    
    characters = {}
    for uuid in uuids:
        with open(f"database/sheets/{uuid}/character.json", "r") as f:
            data = json.load(f)
            characters[uuid] = {
                **data,
                "total_level": sum(c["level"] for c in data.get("classes", [])),
            }

    return characters
