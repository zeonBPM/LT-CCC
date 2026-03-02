class ForceEquipOnUse(ItemComponent):
    nid = 'force_equip_on_use'
    desc = "Forces the item to get equipped when used if it otherwise wouldn't be. Meant to be paired with the 'Equippable Spells' component, which by default are only equippable manually."
    tag = ItemTags.CUSTOM
    author = "AmbiguouslyAnonymous"
    
    def start_combat(self, playback, unit, item, target, item2, mode):
        if item and item is not unit.get_weapon():
            action.do(action.EquipItem(unit, item))