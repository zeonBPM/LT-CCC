


class EvalHealAndRestore(ItemComponent):
    nid = 'eval_heal_and_restore'
    desc = "Heals target and removes all negative statuses. Can target units missing HP or with negative status."
    tag = ItemTags.UTILITY

    expose = ComponentType.String  # E.g., "unit.get_stat('MAG') + 10"

    def _get_heal_amount(self, unit, item, target):
        from app.engine import evaluate
        try:
            base_heal = int(evaluate.evaluate(self.value, unit, local_args={'item': item, 'target': target}))
        except Exception as e:
            logging.error("EvalHealAndRestore: Couldn't evaluate %s (%s)", self.value, e)
            base_heal = 0
        empower_heal = skill_system.empower_heal(unit, target)
        empower_heal_received = skill_system.empower_heal_received(target, unit)
        return base_heal + empower_heal + empower_heal_received

    def _can_be_restored(self, status):
        return status.negative

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        defender = game.board.get_unit(def_pos)
        if defender and skill_system.check_ally(unit, defender):
            needs_healing = defender.get_hp() < defender.get_max_hp()
            has_negative_status = any(self._can_be_restored(skill) for skill in defender.skills)
            if needs_healing or has_negative_status:
                return True
        for s_pos in splash:
            s = game.board.get_unit(s_pos)
            if s and skill_system.check_ally(unit, s):
                needs_healing = s.get_hp() < s.get_max_hp()
                has_negative_status = any(self._can_be_restored(skill) for skill in s.skills)
                if needs_healing or has_negative_status:
                    return True
        return False

    def simple_target_restrict(self, unit, item):
        needs_healing = unit.get_hp() < unit.get_max_hp()
        has_negative_status = any(self._can_be_restored(skill) for skill in unit.skills)
        return needs_healing or has_negative_status

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        heal = self._get_heal_amount(unit, item, target)
        true_heal = min(heal, target.get_max_hp() - target.get_hp())
        if true_heal > 0:
            actions.append(action.ChangeHP(target, heal))
            playback.append(pb.HealHit(unit, item, target, heal, true_heal))
            playback.append(pb.HitSound('MapHeal', map_only=True))
            if heal >= 30:
                name = 'MapBigHealTrans'
            elif heal >= 15:
                name = 'MapMediumHealTrans'
            else:
                name = 'MapSmallHealTrans'
            playback.append(pb.HitAnim(name, target))

        for skill in target.all_skills[:]:
            if self._can_be_restored(skill):
                actions.append(action.RemoveSkill(target, skill))
                playback.append(pb.RestoreHit(unit, item, target))

    def ai_priority(self, unit, item, target, move):
        if target and skill_system.check_ally(unit, target):
            max_hp = target.get_max_hp()
            missing_health = max_hp - target.get_hp()
            heal = self._get_heal_amount(unit, item, target)
            heal_term = utils.clamp(min(heal, missing_health) / float(max_hp), 0, 1)
            restore_term = 1.0 if any(self._can_be_restored(skill) for skill in target.skills) else 0.0
            return max(heal_term, restore_term * 0.8)  # Weighted balance
        return 0
