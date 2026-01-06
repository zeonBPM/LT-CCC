class RallyOnAction(SkillComponent):
    nid = 'rally_on_action'
    desc = desc = 'Inflicts the given status to allies within the given number of spaces from user.'
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
        if target and skill_system.check_enemy(unit, target):
            r = set(range(self.value.get('range') + 1))
            locations = game.target_system.get_shell({unit.position}, r, game.board.bounds)
            for loc in locations:
                target2 = game.board.get_unit(loc)
                if target2 and target2 is not target and target2 is not unit and skill_system.check_ally(unit, target2):
                    action.do(action.AddSkill(target2, self.value.get('status'), unit))