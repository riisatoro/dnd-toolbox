from database.sheet import CharacterSheet


cache: dict = {
    "uuuu": CharacterSheet(uuid="uuuu")
}


def get_sheet(uuid: str) -> CharacterSheet:
    sheet = cache.get(uuid)
    if not sheet:
        sheet = CharacterSheet(uuid=uuid)
        cache[uuid] = sheet
    return sheet


def save_sheet(uuid: str) -> None:
    sheet = cache.get(uuid)
    if sheet:
        sheet.write_to_file()
    else:
        raise ValueError(f"Sheet with uuid {uuid} not found in cache")
