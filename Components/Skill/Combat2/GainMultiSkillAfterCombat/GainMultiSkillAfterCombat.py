#Allows you to enter a list of skills.  All these skills will be added to the user after any combat.
class GainMultiSkillAfterCombat(SkillComponent):
    nid = 'gain_multi_skill_after_combat'
    desc = "Gives all listed skills to user after any combat"
    tag = SkillTags.COMBAT2

    expose = (ComponentType.List, ComponentType.Skill)

    def end_combat(self, playback, unit, item, target, item2, mode):
        for skill in self.value:
            action.do(action.AddSkill(unit, skill))
        action.do(action.TriggerCharge(unit, self.skill))