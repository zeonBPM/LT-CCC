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
