#This was made to be able to heal a % of target's HP instead of a fixed amount, used in FE8R Triage skill originally.


class EvalHealing(ItemComponent):
    nid = 'eval_healing'
    desc = "Item heals for an evaluated amount on hit."
    tag = ItemTags.UTILITY

    expose = ComponentType.String  # E.g., "unit.get_stat('MAG') + 5"

    def _get_heal_amount(self, unit, item, target):
        from app.engine import evaluate
        try:
            base_heal = int(evaluate.evaluate(self.value, unit, local_args={'item': item, 'target': target}))
        except Exception as e:
            logging.error("EvalHealing: Couldn't evaluate %s (%s)", self.value, e)
            base_heal = 0
        empower_heal = skill_system.empower_heal(unit, target)
        empower_heal_received = skill_system.empower_heal_received(target, unit)
        return base_heal + empower_heal + empower_heal_received

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        # Only valid if someone in the target area is not at full HP
        defender = game.board.get_unit(def_pos)
        if defender and defender.get_hp() < defender.get_max_hp():
            return True
        for s_pos in splash:
            s = game.board.get_unit(s_pos)
            if s and s.get_hp() < s.get_max_hp():
                return True
        return False

    def simple_target_restrict(self, unit, item):
        return unit and unit.get_hp() < unit.get_max_hp()

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        heal = self._get_heal_amount(unit, item, target)
        true_heal = min(heal, target.get_max_hp() - target.get_hp())
        actions.append(action.ChangeHP(target, heal))

        if true_heal > 0:
            playback.append(pb.HealHit(unit, item, target, heal, true_heal))
            playback.append(pb.HitSound('MapHeal', map_only=True))
            if heal >= 30:
                name = 'MapBigHealTrans'
            elif heal >= 15:
                name = 'MapMediumHealTrans'
            else:
                name = 'MapSmallHealTrans'
            playback.append(pb.HitAnim(name, target))

    def ai_priority(self, unit, item, target, move):
        if target and skill_system.check_ally(unit, target):
            max_hp = target.get_max_hp()
            missing_health = max_hp - target.get_hp()
            help_term = utils.clamp(missing_health / float(max_hp), 0, 1)
            heal = self._get_heal_amount(unit, item, target)
            heal_term = utils.clamp(min(heal, missing_health) / float(max_hp), 0, 1)
            return help_term * heal_term
        return 0
