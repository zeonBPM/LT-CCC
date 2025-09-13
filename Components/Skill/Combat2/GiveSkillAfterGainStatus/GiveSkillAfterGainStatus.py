#Allows you to enter a list of skills.  If the user is inflicted with any of these skills, apply a specified status to the inflictor.
class GiveSkillAfterGainStatus(SkillComponent):
    nid = 'skill_after_inflict_status'
    desc = "Give a skill to the attacker after gaining a status."
    tag = SkillTags.COMBAT2

    expose = ComponentType.NewMultipleOptions
    options = {
        'gained': (ComponentType.List, ComponentType.Skill),
        'given': ComponentType.Skill
    }

    def __init__(self, value=None):
        self.value = {
            'gained': None,
            'given': None
        }
        if value:
            self.value.update(value)
            
    def after_gain_skill(self, unit, other_skill):
        if other_skill.nid in self.value['gained'] and other_skill.initiator_nid and skill_system.condition(self.skill, unit):
            other_unit = game.get_unit(other_skill.initiator_nid)
            if other_unit:
                action.do(action.AddSkill(other_unit, self.value['given']))