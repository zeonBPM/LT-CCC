from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.skill_components import SkillComponent, SkillTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system,
                        target_system)
from app.engine.game_state import game
from app.engine.objects.unit import UnitObject
from app.utilities import (utils, static_random)

from app.engine.skill_components import charge_components
from app.engine.combat import playback as pb
from app.data.database.item_components import ItemComponent, ItemTags


class DoNothing(SkillComponent):
    nid = 'do_nothing'
    desc = 'does nothing'
    tag = SkillTags.CUSTOM

    expose = ComponentType.Int
    value = 1

class CantoPlusPlus(SkillComponent):
    nid = 'canto_plus_plus'
    desc = "Unit can use its full movement again, even after attacking"
    tag = SkillTags.MOVEMENT
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    def canto_movement(self, unit, unit2) -> int:
        return unit.stats['MOV']

    def has_canto(self, unit, unit2) -> bool:
        return True

class BuildChargeActive(SkillComponent):
    nid = 'build_charge_active'
    desc = "Skill starts each chapter with 0 charges, and builds up to the specified maximum."
    tag = SkillTags.CHARGE
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.Int
    value = 10

    ignore_conditional = True

    def init(self, skill):
        self.skill.data['charge'] = 0
        self.skill.data['total_charge'] = self.value

    def on_end_chapter(self, unit, skill):
        self.skill.data['charge'] = 0

    def text(self) -> str:
        return str(self.skill.data['charge'])

class ChargeAfterKill(SkillComponent):
    nid = 'charge_after_kill'
    desc = "Charges this skill after a kill"
    tag = SkillTags.CHARGE
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.Int
    value = 1

    def end_combat(self, playback, unit, item, target, item2, mode):
        marks = charge_components.get_marks(playback, unit, item)
        if marks and target and target.get_hp() <= 0:
            new_value = self.skill.data['charge'] + self.value
            new_value = min(new_value, self.skill.data['total_charge'])
            action.do(action.SetObjData(self.skill, 'charge', new_value))

class EvalHealOnHit(SkillComponent):
    nid = 'eval_heal_on_hit'
    desc = "Heals user eval'd value on hit; exposes unit, item, skill, hits"
    tag = SkillTags.COMBAT2
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.String
    value = '7 * hits'

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        hits = 0
        playbacks = [p for p in playback if p.nid in (
            'damage_hit', 'damage_crit') and p.attacker == unit]
        for p in playbacks:
            hits += 1

        from app.engine import evaluate
        total_heal = 0
        try:
            total_heal = int(evaluate.evaluate(self.value, unit, local_args={'item': item, 'skill': self.skill, 'hits': hits}))
        except:
            logging.error("eval_heal_on_hit couldn't evaluate healing value %s" % self.value)

        actions.append(action.ChangeHP(unit, total_heal))
        playback.append(pb.HealHit(unit, item, unit, total_heal, total_heal))
        actions.append(action.TriggerCharge(unit, self.skill))

class EvalTargetOnlyRestrict(ItemComponent):
    nid = 'eval_target_only_restrict'
    desc = \
"""
Restricts which units or spaces can be targeted, but only calls once per target tile. These properties are accessible in the eval body:

- `unit`: the unit using the item
- `target`: the target of the item
- `item`: the item itself
- `position`: the position of the unit
- `target_pos`: the position of the target
- `splash`: the set of splash tiles, if applicable
"""
    tag = ItemTags.TARGET
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.String
    value = 'True'

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        from app.engine import evaluate
        try:
            target = game.board.get_unit(def_pos)
            unit_pos = unit.position
            target_pos = def_pos
            if evaluate.evaluate(self.value, unit, target, unit_pos, local_args={'target_pos': target_pos, 'item': item, 'splash': splash}):
                return True
        except Exception as e:
            print("Could not evaluate %s (%s)" % (self.value, e))
            return True
        return False

    def simple_target_restrict(self, unit, item):
        from app.engine import evaluate
        try:
            if evaluate.evaluate(self.value, unit, local_args={'item': item}):
                return True
        except Exception as e:
            print("Could not evaluate %s (%s)" % (self.value, e))
            return True
        return False

class EventAfterCombat(SkillComponent):
    nid = 'event_after_combat'
    desc = 'calls event after combat (why is this custom?)'
    tag = SkillTags.ADVANCED
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.Event
    value = ''

    def end_combat(self, playback, unit: UnitObject, item, target: UnitObject, item2, mode):
        if skill_system.check_enemy(unit, target):
            game.events.trigger_specific_event(self.value, unit, target, unit.position, {'item': item, 'item2': item2, 'mode': mode})

class SetChargeAfterTakeDamage(SkillComponent):
    nid = 'set_charge_after_take_damage'
    desc = """
Set charge value on this skill immediately after an enemy damages you
Params exposed: unit, item, target, item2, charge (old charge level), damage (damage done)
"""
    tag = SkillTags.COMBAT2
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.String
    value = '42'

    def init(self, skill):
        self.skill.data['charge'] = 0

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        from app.engine import evaluate
        for act in actions:
            if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                try:
                    charge = evaluate.evaluate(self.value, unit, target, local_args={'item': item, 'item2': item2, 'charge': self.skill.data['charge'], 'damage': -1 * act.num})
                    self.skill.data['charge'] = charge
                except Exception as e:
                    print("set_charge_after_take_damage could not evaluate %s (%s)" % (self.value, e))
                return

class GiveStatusAfterCombatOnHitForReal(SkillComponent):
    nid = 'give_status_after_combat_on_hit_real'
    desc = "Gives a status to target after combat, assuming you hit the target, even if you didn't initiate. (why is this custom?)"
    tag = SkillTags.COMBAT2
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    expose = ComponentType.Skill

    def end_combat(self, playback, unit, item, target, item2, mode):
        mark_playbacks = [p for p in playback if p.nid in (
            'mark_hit', 'mark_crit')]
        if target and any(p.attacker is unit for p in mark_playbacks):
            action.do(action.AddSkill(target, self.value, unit))
            action.do(action.TriggerCharge(unit, self.skill))

