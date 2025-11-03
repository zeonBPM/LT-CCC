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
