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
