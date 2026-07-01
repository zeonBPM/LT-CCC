class ImmuneSpecific(SkillComponent):
    nid = 'immune_specific'
    desc = "Unit cannot receive the following statuses"
    tag = SkillTags.STATUS

    expose = (ComponentType.List, ComponentType.Skill)

    #only remove if skill's nid is on the list
    def after_gain_skill(self, unit, other_skill):
        if other_skill.nid in self.value:
            action.do(action.RemoveSkill(unit, other_skill))