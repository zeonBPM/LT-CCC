#This makes weapon type into a list with multipple items, so that the item can be used by classes with different weapons allowed.
#My main idea was to use it with magic, but the best example would be having a halberd count both as an Axe and Lance(whichever is first if the unit can use both)




#should have the same dependencies as the normal WeaponType, so it will work by default.

class WeaponTypes(ItemComponent):
    nid = 'weapon_types'
    desc = "Defines a list of weapon types, item is usable if the unit can use at least one of them. Will default to the first one in the list if more than one is usable"
    tag = ItemTags.WEAPON
    author = "zeonBPM"
    
    expose = (ComponentType.List, ComponentType.WeaponType)

    def weapon_type(self, unit, item) -> Optional[str]:
        klass = DB.classes.get(unit.klass)
        if not klass:
            return self.value[0]

        usable_types = unit_funcs.usable_wtypes(unit)
        for wtype in self.value:
            if wtype in usable_types:
                wexp_gain = klass.wexp_gain.get(wtype)
                unit_wexp = unit.wexp.get(wtype, 0)
                if wexp_gain and unit_wexp > 0:
                    return wtype

        return self.value[0]
        if not self.value:
            return 'Default'

    def available(self, unit, item) -> bool:
        if not self.value or not unit:
            return False

        klass = DB.classes.get(unit.klass)
        if not klass:
            return False

        usable_types = unit_funcs.usable_wtypes(unit)
        for wtype in self.value:
            if wtype in usable_types:
                wexp_gain = klass.wexp_gain.get(wtype)
                unit_wexp = unit.wexp.get(wtype, 0)
                if wexp_gain and unit_wexp > 0:
                    return True

        return False
