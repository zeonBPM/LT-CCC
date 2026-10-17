class DamageFollowUp(SkillComponent):
    nid = 'damage_follow_up'
    desc = "Multiplies damage dealt by a fraction after the first strike"
    tag = SkillTags.COMBAT
    author = 'saragl728'

    expose = ComponentType.Float
    value = 0.5

    def damage_multiplier(self, unit, item, target, item2, mode, attack_info, base_value):
        return self.value if attack_info[0] > 0 else 1
