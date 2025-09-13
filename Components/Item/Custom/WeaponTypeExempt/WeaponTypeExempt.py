       
class WeaponTypeExempt(ItemComponent):
    nid = 'weapon_type_exempt'
    desc = "Categorizes a weapon type but does not require the wielder to be able to use that weapon type"
    tag = ItemTags.CUSTOM

    expose = ComponentType.WeaponType

    def weapon_type(self, unit, item):
        return self.value

    def available(self, unit, item) -> bool:
        return True
