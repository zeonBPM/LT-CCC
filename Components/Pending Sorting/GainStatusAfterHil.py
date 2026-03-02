class GainStatusAfterHit(SkillComponent):
    nid = 'gain_status_after_hit'
    desc = "Unit gains a status after attacking.  Activates mid-combat."
    tag = SkillTags.COMBAT2

    expose = ComponentType.Skill

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if target and not skill_system.check_ally(unit, target) and strike in (Strike.HIT, Strike.CRIT):
            actions.append(action.AddSkill(unit, self.value, unit))