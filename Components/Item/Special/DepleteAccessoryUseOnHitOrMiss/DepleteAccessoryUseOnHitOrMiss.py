#I didn't check if this one needs new imports yet


class DepleteAccessoryUseOnHitOrMiss(ItemComponent):
    nid = 'deplete_accessory_use'
    desc = "The unit's accessory will lose one durability after hitting or missing."
    tag = ItemTags.SPECIAL
    author = 'FdRstar'
    
    def __init__(self, value=None):
        self.combat_uses = 0
    
    def _deplete_accessory(self, actions, unit):
        item = unit.get_accessory()
        if not item:
            return
        self.combat_uses += 1
        actions.append(action.SetObjData(item, 'c_uses', item.data['c_uses'] - 1))
        actions.append(action.UpdateRecords('item_use', (unit.nid, item.nid)))
        if item.data['c_uses'] - self.combat_uses <= 0:
            item_system.on_unusable(unit, item)
            
    def start_combat_unconditional(self, playback, unit, item, target, item2, mode):
        self.combat_uses = 0
    
    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self._deplete_accessory(actions, unit)
            
    def on_miss(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self._deplete_accessory(actions, unit)