        
class GainSkillAfterMiss(SkillComponent):
    nid = 'gain_skill_after_miss'
    desc = "Gives a status to the holder when they miss a single strike(can happen multiple times)."
    tag = SkillTags.COMBAT2
    author = "Minccino"

    expose = ComponentType.Skill

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if strike == Strike.MISS:
            actions.append(action.AddSkill(unit, self.value, unit))
            actions.append(action.TriggerCharge(unit, self.skill))