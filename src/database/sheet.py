from database.common import SKILLS, STATS, SKILL_TO_STAT_MAPPER
from database.rw_operations import CharacterSheetIO
from database.combat_operations import CharacterCompat


class CharacterSheet(
    CharacterSheetIO,
    CharacterCompat,
):
    def __init__(self, uuid: str | None = None):
        self.uuid = uuid
        self.name: str = ""
        self.race: str = ""
        self.classes: list = []
        self.background: str = ""
        self.alignment: str = ""
        self.stats: dict = {}
        self.skills: dict = {}
        self.combat_info: dict = {}
        self.death_saves: dict = {}
        self.inspiration: int = 0

        self.find_character()

    @property
    def proficiency_bonus(self):
        return 2 + (self.total_level - 1) // 4

    @property
    def total_level(self):
        return sum([c["level"] for c in self.classes])

    def calc_stat_modifier(self, value):
        return (self.stats[value]['value'] - 10) // 2

    def calc_stat_saving(self, stat):
        if not self.stats[stat]["saving"]:
            return None
        return self.calc_stat_modifier(stat) + self.proficiency_bonus

    def calc_skill_modifier(self, skill, proficient, expertise):
        stat = SKILL_TO_STAT_MAPPER[skill]
        modifier = self.calc_stat_modifier(stat)
        if proficient:
            modifier += self.proficiency_bonus
        if expertise:
            modifier += self.proficiency_bonus
        return modifier

    def calc_spell_to_hit(self, stat):
        return self.proficiency_bonus + self.calc_stat_modifier(stat)

    def calc_spell_save(self, stat):
        return 8 + self.proficiency_bonus + self.calc_stat_modifier(stat)

    def calc_melee_to_hit(self, stat, proficient):
        modifier = self.calc_stat_modifier(stat)
        if proficient:
            modifier += self.proficiency_bonus
        return modifier

    def calc_melee_damage_bonus(self, stat):
        return self.calc_stat_modifier(stat)
