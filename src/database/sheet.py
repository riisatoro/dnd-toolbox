import json
import os

from fastapi import HTTPException


class IO:
    def read(self, uuid: str) -> None:
        data = {}
        
        for file in os.scandir(f"database/sheets/{uuid}"):
            try:
                with open(file.path, "r") as f:
                    data[file.name] = json.load(f)
            except json.JSONDecodeError:
                raise HTTPException(status_code=500, detail=f"{file} is corrupted")
            except FileNotFoundError:
                raise HTTPException(status_code=404, detail=f"{file} not found")

        return data

    def write(self, uuid: str) -> None:
        for file, values in self.data.items():
            with open(f"database/sheets/{uuid}/{file}", "w") as f:
                json.dump(values, f, indent=4)


class Character:
    @property
    def total_level(self) -> int:
        return sum(c["level"] for c in self.data["character.json"]["classes"])

    @property
    def proficiency_bonus(self) -> int:
        return 2 + (self.total_level - 1) // 4

    def render_character(self) -> dict:
        return {
            **self.data["character.json"],
            "total_level": self.total_level,
            "proficiency_bonus": self.proficiency_bonus,
        }


class Combat:
    def render_combat(self) -> dict:
        return self.data["combat.json"]
    
    def add_health(self, value: int) -> None:
        current, total = self.data["combat.json"]["health"]["value"], self.data["combat.json"]["health"]["total"]
        if current + value > total:
            self.data["combat.json"]["health"]["value"] = total
        else:
            self.data["combat.json"]["health"]["value"] += value
    
    def add_damage(self, value: int) -> None:
        temporary = self.data["combat.json"]["health"]["temporary"]
        if temporary - value >= 0:
            self.data["combat.json"]["health"]["temporary"] -= value
        else:
            self.data["combat.json"]["health"]["temporary"] = 0
            self.data["combat.json"]["health"]["value"] -= value
        
        if self.data["combat.json"]["health"]["value"] < 0:
            self.data["combat.json"]["health"]["value"] = 0

    def add_temporary(self, value: int) -> None:
        self.data["combat.json"]["health"]["temporary"] += value


class Spells:
    def render_spells(self) -> dict:
        return {
            **self.data["spells.json"],
            "to_hit": self.get_spell_to_hit(self.data["spells.json"]["cast_from"]),
            "saving": self.get_spell_saving(self.data["spells.json"]["cast_from"]),
        }
    
    def get_spell_to_hit(self, stat: str) -> int:
        return self.get_stat_modifier(stat) + self.proficiency_bonus
    
    def get_spell_saving(self, stat: str) -> int:
        return 8 + self.get_stat_modifier(stat) + self.proficiency_bonus
    
    def restore_spell_slots(self) -> None:
        for key, value in self.data["spells.json"]["spell_slots"].items():
            self.data["spells.json"]["spell_slots"][key]["value"] = value["total"]

    def add_spell_slot(self, key: str) -> None:
        if self.data["spells.json"]["spell_slots"][key]["value"] < self.data["spells.json"]["spell_slots"][key]["total"]:
            self.data["spells.json"]["spell_slots"][key]["value"] += 1
    
    def remove_spell_slot(self, key: str) -> None:
        if self.data["spells.json"]["spell_slots"][key]["value"] > 0:
            self.data["spells.json"]["spell_slots"][key]["value"] -= 1


class Stats:
    def get_stat_modifier(self, key: str) -> int:
        return (self.data["stats.json"][key]["value"] - 10) // 2
    
    def get_stat_saving(self, key: str) -> int:
        if self.data["stats.json"][key]["saving"]:
            return self.get_stat_modifier(key) + self.proficiency_bonus
        return self.get_stat_modifier(key)

    def render_stats(self) -> dict:
        return {
            k: {
                **v, 
                "modifier": self.get_stat_modifier(k),
                "saving_modifier": self.get_stat_saving(k)
            }
            for k, v in self.data["stats.json"].items()
        }
    

class MeleeAttack:
    def render_melee(self) -> dict:
        return self.data["melee_attacks.json"]


class Consumables:
    def render_consumables(self) -> dict:
        return self.data["consumables.json"]
    
    def add_consumable(self, key: str) -> None:
        self.data["consumables.json"][key]["value"] += 1
    
    def remove_consumable(self, key: str) -> None:
        if self.data["consumables.json"][key]["value"] > 0:
            self.data["consumables.json"][key]["value"] -= 1


class Skills:
    @property
    def passive_perception(self) -> int:
        return (10 + self.get_skill_modifier("Perception"))

    @property
    def passive_insight(self) -> int:
        return (10 + self.get_skill_modifier("Insight"))
    
    @property
    def passive_investigation(self) -> int:
        return (10 + self.get_skill_modifier("Investigation"))
    
    def get_skill_modifier(self, key: str) -> int:
        stat = self.data["skills.json"][key]["from_stat"]
        modifier = self.get_stat_modifier(stat)
 
        if self.data["skills.json"][key]["proficient"]:
            modifier += self.proficiency_bonus
        if self.data["skills.json"][key]["expertise"]:
            modifier += self.proficiency_bonus
        return modifier

    def render_skills(self) -> dict:
        return {
            "passives": {
                "perception": self.passive_perception,
                "insight": self.passive_insight,
                "investigation": self.passive_investigation,
            },
            "skills": {
                k: {
                    **v,
                    "modifier": self.get_skill_modifier(k),
                }
                for k, v in self.data["skills.json"].items()
            }
        }


class Abilities:
    def render_abilities(self) -> dict:
        return self.data["abilities.json"]


class CharacterSheet(
    IO,
    Abilities,
    Character,
    Combat,
    Consumables,
    MeleeAttack,
    Skills,
    Spells,
    Stats,
):
    def __init__(self, uuid: str):
        self.uuid = uuid
        self.data = {}
        self.data = self.read(uuid)

    def render(self) -> dict:
        return {
            "uuid": self.uuid,
            "abilities": self.render_abilities(),
            "character": self.render_character(),
            "combat": self.render_combat(),
            "consumables": self.render_consumables(),
            "melee": self.render_melee(),
            "skills": self.render_skills(),
            "spells": self.render_spells(),
            "stats": self.render_stats(),
        }
