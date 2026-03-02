class GiveSkillAfterKill(SkillComponent):
    nid = 'give_skill_after_kill'
    desc = "Gives a skill to a dying unit (for some reason??)"
    tag = SkillTags.COMBAT2

    expose = ComponentType.Skill

    def end_combat(self, playback, unit, item, target, item2, mode):
        if target and target.get_hp() <= 0:
            action.do(action.AddSkill(target, self.value))
            action.do(action.TriggerCharge(unit, self.skill))