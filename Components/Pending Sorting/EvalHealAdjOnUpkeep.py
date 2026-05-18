class EvalHealAdjOnUpkeep(SkillComponent):
    nid = 'Eval_heal_adj_on_upkeep'
    desc = "Unit will heal adjacent units on upkeep according to the given evaluation"
    tag = SkillTags.STATUS
    author = 'Windward'

    expose = ComponentType.String

    def on_upkeep(self, actions, playback, unit):
        x = unit.position[0]
        y = unit.position[1]
        adjacent_tiles = ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
        adjacent_tiles = [pos for pos in adjacent_tiles if game.board.check_bounds(pos)]
        adjacent = [game.board.get_unit(pos) for pos in adjacent_tiles]
        to_heal = [un for un in adjacent if un and skill_system.check_ally(unit, un)]
        for un in to_heal:
            max_hp = equations.parser.hitpoints(unit)
            if un.get_hp() < max_hp:
                from app.engine import evaluate
                try:
                    heal = int(evaluate.evaluate(self.value, unit))
                except:
                    logging.error("Couldn't evaluate %s conditional" % self.value)
                    heal = 0
                if heal > 0:
                    actions.append(action.ChangeHP(un, heal))
                    # Playback
                    playback.append(pb.HitSound('MapHeal'))
                    playback.append(pb.DamageNumbers(un, -heal))
                    if heal >= 30:
                        name = 'MapBigHealTrans'
                    elif heal >= 15:
                        name = 'MapMediumHealTrans'
                    else:
                        name = 'MapSmallHealTrans'
                    playback.append(pb.CastAnim(name))