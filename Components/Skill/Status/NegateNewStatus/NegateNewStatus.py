#Prevents units from gaining new status effects.  Does not negate already existing status.
class NegateNewStatus(SkillComponent):
    nid = 'negate_new_status'
    desc = "Unit does not receive status effects"
    tag = SkillTags.STATUS

    def after_gain_skill(self, unit, other_skill):
        if other_skill is not self.skill and skill_system.condition(self.skill, unit):
            action.do(action.RemoveSkill(unit, other_skill))