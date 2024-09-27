class CharacterCompat:
    def add_health(self, value: int):
        current_hp = self.combat_info["health_current"]
        total_hp = self.combat_info["health_total"]

        if total_hp - current_hp < value:
            current_hp = total_hp
        else:
            current_hp += value

        self.combat_info["health_current"] = current_hp


    def add_damage(self, value: int):
        temp_hp = self.combat_info["health_temp"]
        current_hp = self.combat_info["health_current"]
        total_hp = self.combat_info["health_total"]

        if temp_hp >= value:
            temp_hp -= value
        else:
            value -= temp_hp
            temp_hp = 0
            current_hp -= value

        if current_hp < 0:
            current_hp = 0

        self.combat_info["health_temp"] = temp_hp
        self.combat_info["health_current"] = current_hp

    def add_temporary_hp(self, value: int):
        self.combat_info["health_temp"] += value

    def restore_spell_slots(self):
        for slot in self.spell_slots.values():
            slot["current"] = slot["total"]

    def add_spell_slot(self, level: str):
        if self.spell_slots[level]["current"] < self.spell_slots[level]["total"]:
            self.spell_slots[level]["current"] += 1

    def remove_spell_slot(self, level: str):
        if self.spell_slots[level]["current"] > 0:
            self.spell_slots[level]["current"] -= 1
