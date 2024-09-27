import json


from fastapi import HTTPException


class CharacterSheetIO:
    def find_character(self):
        if not self.uuid:
            return

        with open(f"database/sheets.json") as f:
            data = json.load(f)
        if not data.get(self.uuid):
            raise HTTPException(status_code=404, detail="Character not found")

        self.from_json(data[self.uuid])

    def to_json(self):
        return {
            "name": self.name,
            "race": self.race,
            "classes": self.classes,
            "background": self.background,
            "alignment": self.alignment,
            "stats": self.stats,
            "skills": self.skills,
            "combat_info": self.combat_info,
            "death_saves": self.death_saves,
            "inspiration": self.inspiration,
            "spell_stat": self.spell_stat,
            "spell_slots": self.spell_slots,
            "melee_attacks": self.melee_attacks,
            "avatar": self.avatar,
        }

    def to_render(self):
        data = self.to_json()
        data["id"] = self.uuid
        data['total_level'] = self.total_level
        data['proficiency_bonus'] = self.proficiency_bonus
        data['initiative'] = self.calc_stat_modifier("DEX")

        data['race_class_text'] = ", ".join([
            self.race,
            *[f"{c['name']} ({c['level']})" for c in self.classes]
        ])

        data['render_stats'] = [
            {
                "name": key,
                "value": value["value"],
                "modifier": self.calc_stat_modifier(key),
                "saving": self.calc_stat_saving(key),
            }
            for key, value in data["stats"].items()
        ]

        data['render_skills'] = [
            {
                "name": key,
                "proficient": value["proficient"],
                "expertise": value["expertise"],
                "modifier": self.calc_skill_modifier(key, value["proficient"], value["expertise"]),
            }
            for key, value in data["skills"].items()
        ]
        data["render_spells"] = {
            "stat": self.spell_stat,
            "to_hit": self.calc_spell_to_hit(self.spell_stat),
            "saving": self.calc_spell_save(self.spell_stat),
            "slots": [{
                "level": k,
                "current": v["current"],
                "total": v["total"],
            } for k, v in self.spell_slots.items() if v["total"]],
        }
        data["render_melee_attacks"] = [
            {
                "name": value["name"],
                "to_hit": self.calc_melee_to_hit(value['stat'], value['proficient']) + value.get("additional_to_hit", 0),
                "damage_bonus": self.calc_melee_damage_bonus(value['stat']) + value.get("additional_damage_bonus", 0),
                "distance": value["distance"],
                "type": value["type"],
            }
            for value in self.melee_attacks
        ]
        data['render_passives'] = {
            "perception": 10 + self.calc_skill_modifier("Perception", self.skills["Perception"]["proficient"], self.skills["Perception"]["expertise"]),
            "insight": 10 + self.calc_skill_modifier("Insight", self.skills["Insight"]["proficient"], self.skills["Insight"]["expertise"]),
            "investigation": 10 + self.calc_skill_modifier("Investigation", self.skills["Investigation"]["proficient"], self.skills["Investigation"]["expertise"]),
        }
        return data

    def from_json(self, file_data):
        self.name = file_data["name"]
        self.race = file_data["race"]
        self.classes = file_data["classes"]
        self.background = file_data["background"]
        self.alignment = file_data["alignment"]
        self.stats = file_data["stats"]
        self.skills = file_data["skills"]
        self.combat_info = file_data["combat_info"]
        self.death_saves = file_data["death_saves"]
        self.inspiration = file_data["inspiration"]
        self.spell_stat = file_data["spell_stat"]
        self.spell_slots = file_data["spell_slots"]
        self.melee_attacks = file_data["melee_attacks"]
        self.avatar = file_data["avatar"]

    def write_to_file(self):
        with open("database/sheets.json") as f:
            data = json.load(f)
        data[self.uuid] = self.to_json()
        with open("database/sheets.json", "w") as f:
            json.dump(data, f, indent=4, sort_keys=True)
