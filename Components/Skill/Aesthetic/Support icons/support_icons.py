from app.data.database.skill_components import SkillComponent, SkillTags

from app.engine import skill_system
from app.engine.game_state import game

class SupportIcons(SkillComponent):
    nid = 'support_icons'
    desc = "Support rank appears above allies's heads."
    tag = SkillTags.AESTHETIC

    author = 'Beccarte'

    def target_icon(self, unit, icon_unit) -> str:
        if skill_system.check_ally(unit, icon_unit) and game.query_engine.get_support_rank(unit.nid, icon_unit.nid):
            rank = game.query_engine.get_support_rank(unit.nid, icon_unit.nid)
            icon_file = 'support_' + rank
            return icon_file
