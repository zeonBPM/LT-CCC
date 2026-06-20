class Sacrifice(ItemComponent):
    nid = 'sacrifice'
    desc = "Causes the item's user to take damage equal to the amount the target healed."
    tag = ItemTags.SPECIAL
    author = 'WindwardBound'

    def _get_heal_amount(self, unit, item, target):
        return unit.get_hp() - 1
    
    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        heal = self._get_heal_amount(unit, item, target)
        true_heal = min(heal, target.get_max_hp() - target.get_hp())
        end_health = unit.get_hp() - true_heal
        action.do(action.SetHP(unit, max(1, end_health)))