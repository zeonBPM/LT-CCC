class RallyOnKill(SkillComponent):
    nid = 'rally_on_kill'
    desc = 'Inflicts the given status to allies within the given number of spaces from user when defeating an enemy.'
    tag = SkillTags.CUSTOM
    author = 'saragl728'

    expose = (ComponentType.NewMultipleOptions)
    options = {
        "status": ComponentType.Skill,
        "range": ComponentType.Int,
    }
    
    def __init__(self, value=None):
        self.value = {
            "status": 'Canto',
            "range": 1,
        }
        if value:
            self.value.update(value)

    def end_combat(self, playback, unit, item, target, item2, mode):
        if target and target.get_hp() <= 0:
            r = set(range(self.value.get('range') + 1))
            locations = game.target_system.get_shell({unit.position}, r, game.board.bounds)
            for loc in locations:
                target2 = game.board.get_unit(loc)
                if target2 and target2 is not target and target2 is not unit and skill_system.check_ally(unit, target2):
                    action.do(action.AddSkill(target2, self.value.get('status'), unit))

class RallyOnActiveKill(SkillComponent):
    nid = 'rally_on_active_kill'
    desc = 'Inflicts the given status to allies within the given number of spaces from user when defeating an enemy after initiating combat.'
    tag = SkillTags.CUSTOM
    author = 'saragl728'

    expose = (ComponentType.NewMultipleOptions)
    options = {
        "status": ComponentType.Skill,
        "range": ComponentType.Int,
    }
    
    def __init__(self, value=None):
        self.value = {
            "status": 'Canto',
            "range": 1,
        }
        if value:
            self.value.update(value)

    def end_combat(self, playback, unit, item, target, item2, mode):
        mark_playbacks = [p for p in playback if p.nid in ('mark_miss', 'mark_hit', 'mark_crit')]
        if target and target.get_hp() <= 0 and any(p.main_attacker is unit for p in mark_playbacks):  # Unit is overall attacker
            r = set(range(self.value.get('range') + 1))
            locations = game.target_system.get_shell({unit.position}, r, game.board.bounds)
            for loc in locations:
                target2 = game.board.get_unit(loc)
                if target2 and target2 is not target and target2 is not unit and skill_system.check_ally(unit, target2):
                    action.do(action.AddSkill(target2, self.value.get('status'), unit))