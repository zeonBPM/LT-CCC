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
