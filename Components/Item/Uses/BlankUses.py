from app.engine.item_components.usable_components import ManaCostAsUses

class BlankUses(ManaCostAsUses):
    nid = 'blank_uses'
    desc = "Display empty string in place of Uses on the item. Do not combine with other uses components."

    def _calc_uses(self, unit, item):
        return ''