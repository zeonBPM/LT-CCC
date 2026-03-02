class RestoreOnUpkeep(SkillComponent):
    nid = 'restore_on_upkeep'
    desc = "Unit will restore adjacent units on upkeep"
    tag = SkillTags.ADVANCED

    def on_upkeep(self, actions, playback, unit):
        x = unit.position[0]
        y = unit.position[1]
        adjacent_tiles = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        adjacent_tiles = [pos for pos in adjacent_tiles if game.board.check_bounds(pos)]
        adjacent = [game.board.get_unit(pos) for pos in adjacent_tiles]
        to_restore = [un for un in adjacent if un and skill_system.check_ally(unit, un)]
        for un in to_restore:
          for skill in un.all_skills[:]:
            if skill.negative:
                actions.append(action.RemoveSkill(un, skill))