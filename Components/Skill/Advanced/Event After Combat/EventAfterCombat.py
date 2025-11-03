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
