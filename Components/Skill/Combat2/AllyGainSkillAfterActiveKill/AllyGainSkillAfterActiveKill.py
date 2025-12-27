class AllyGainSkillAfterActiveKill(SkillComponent):
    nid = 'ally_gain_skill_after_active_kill'
    desc = "Gives a skill to adjacent allies after a kill on personal phase"
    tag = SkillTags.CUSTOM

    expose = ComponentType.Skill

    def end_combat(self, playback, unit, item, target, item2, mode):
        mark_playbacks = [p for p in playback if p.nid in (
            'mark_miss', 'mark_hit', 'mark_crit')]
        if target and target.get_hp() <= 0 and any(p.main_attacker is unit for p in mark_playbacks):  # Unit is overall attacker
            adj_positions = game.target_system.get_adjacent_positions(unit.position)
            for adj_pos in adj_positions:
                other = game.board.get_unit(adj_pos)
                action.do(action.AddSkill(other, self.value))
                action.do(action.TriggerCharge(other, self.skill))
