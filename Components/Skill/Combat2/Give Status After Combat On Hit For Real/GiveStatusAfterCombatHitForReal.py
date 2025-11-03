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

