class BestowSkillOnUpkeep(SkillComponent):
    nid = 'bestow_skill_on_upkeep'
    desc = "Unit will give a skill to adjacent units on upkeep"
    tag = SkillTags.ADVANCED
    author = 'Windward'

    expose = ComponentType.Skill

    def on_upkeep(self, actions, playback, unit):
        x = unit.position[0]
        y = unit.position[1]
        adjacent_tiles = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        adjacent_tiles = [pos for pos in adjacent_tiles if game.board.check_bounds(pos)]
        adjacent = [game.board.get_unit(pos) for pos in adjacent_tiles]
        to_bestow = [un for un in adjacent if un and skill_system.check_ally(unit, un)]
        for un in to_bestow:
            actions.append(action.AddSkill(un, self.value))