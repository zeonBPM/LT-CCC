from app.engine.game_menus.icon_options import UsesDisplayConfig
from app.engine.fonts import FONT
from app.engine.item_components.usable_components import ManaCostAsUses


class HPCostAsUses(ItemComponent):
    nid = 'hp_cost_as_uses'
    requires = ['hp_cost', 'eval_hp_cost']
    desc = "Display the HP Cost in place of Uses on the item. Do not combine with other uses components."

    tag = ItemTags.USES
    delim = None

    def _calc_uses(self, unit, item):
        if (item.eval_hp_cost):
            return item.eval_hp_cost._check_value(unit, item);
        return item.hp_cost.value

    def _calc_max_uses(self, unit, item):
        return None

    def _font_color(self, unit, item):
        color = 'red'
        if not item_funcs.available(unit, item):
            color = 'grey'
        if 'text-' + color in FONT:
            return color
        return None

    def item_uses_display(self, unit, item) -> UsesDisplayConfig:
        return UsesDisplayConfig(self._calc_uses, self.delim, self._calc_max_uses, self._font_color, unit, item)

