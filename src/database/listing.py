import json

def get_available_characters():
    with open("database/sheets.json", "r") as f:
        data = json.load(f)

    characters = [
        {
            "id": key,
            "name": value["name"],
            "race": value["race"],
            "classes": value["classes"],
            "avatar": value["avatar"],
            "level": sum(c["level"] for c in value["classes"]),
        }
        for key, value in data.items()
    ]
    return characters
