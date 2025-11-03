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
