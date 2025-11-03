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



class CantoPlusPlus(SkillComponent):
    nid = 'canto_plus_plus'
    desc = "Unit can use its full movement again, even after attacking"
    tag = SkillTags.MOVEMENT
    author = ",̶'̶,̶|̶'̶,̶'̶_̶"

    def canto_movement(self, unit, unit2) -> int:
        return unit.stats['MOV']

    def has_canto(self, unit, unit2) -> bool:
        return True
