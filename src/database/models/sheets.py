from database.base import Base
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import JSON


CHARACTER_SHEET_TEMPLATE = {
    "level": 0,
    "save_throws": [],
    "stats": {
        "strength": 0,
        "dexterity": 0,
        "constitution": 0,
        "intelligence": 0,
        "wisdom": 0,
        "charisma": 0,
    },
    "combat_stats": {
        "current": 0,
        "max": 0,
        "temp": 0,
        "ac": 0,
        "speed": 0,
        "initiative": 0,
        "hit_dice": 0,
    },
    "skills": {
        "acrobatics": 0,
        "animal_handling": 0,
        "arcana": 0,
        "athletics": 0,
        "deception": 0,
        "history": 0,
        "insight": 0,
        "intimidation": 0,
        "investigation": 0,
        "medicine": 0,
        "nature": 0,
        "perception": 0,
        "performance": 0,
        "persuasion": 0,
        "religion": 0,
        "sleight_of_hand": 0,
        "stealth": 0,
        "survival": 0,
    },
    "proficiency": [],
    "double_proficiency": [],
}

CHARACTER_INVENTORY_TEMPLATE = {
    "gold": {
        "copper": 0,
        "silver": 0,
        "electrum": 0,
        "gold": 0,
        "platinum": 0,
    },
    "items": [],
    "weapons": [],
    "armor": [],
    "consumables": [],
    "potions": [],
}

CHARACTER_PERSONALITY_TEMPLATE = {
    "sheet_type": "",
    "alignment:": "",
    "race": "",
    "class_": "",
    "background": "",
}

CHARACTERS_SPELLS_TEMPLATE = {}


class Sheet(Base):
    __tablename__ = 'sheets'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    stats = Column(JSON, default=CHARACTER_SHEET_TEMPLATE)
    inventory = Column(JSON, default=CHARACTER_INVENTORY_TEMPLATE)
    personality = Column(JSON, default=CHARACTER_PERSONALITY_TEMPLATE)
    spells = Column(JSON, default=CHARACTERS_SPELLS_TEMPLATE)
