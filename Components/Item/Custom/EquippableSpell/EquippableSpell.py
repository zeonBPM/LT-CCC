class EquippableSpell(ItemComponent):
    nid = 'equippable_spell'
    desc = "This item will show up in the Spell menu, but is able to be manually equipped. If paired with the 'Force Equip On Use' component, it can manually and automatically be equipped."
    tag = ItemTags.BASE
    author = "AmbiguouslyAnonymous"

    def is_spell(self, unit, item):
        return True

    def is_weapon(self, unit, item):
        return False

    def equippable(self, unit, item):
        return True

    def wexp(self, playback, unit, item, target):
        return 1

    def can_double(self, unit, item):
        return False

    def can_counter(self, unit, item):
        return False

    def can_be_countered(self, unit, item):
        return True