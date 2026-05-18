class Disarm(SkillComponent):
    nid = 'disarm'
    desc = "unequips target enemy's weapon on end combat"
    tag = SkillTags.COMBAT2
    author = 'Windward'

    def end_combat(self, playback, unit, item, target, item2, mode):
        mark_playbacks = [p for p in playback if p.nid in ('mark_hit', 'mark_crit')]
        if target and any(p.attacker is unit and (p.main_attacker is unit or p.attacker is p.main_attacker.strike_partner)
                          for p in mark_playbacks):  # Unit is overall attacker
            action.do(action.UnequipItem(target, item2))
            action.do(action.TriggerCharge(unit, self.skill))