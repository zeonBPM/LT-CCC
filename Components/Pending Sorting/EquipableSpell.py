class EquippableSpell(ItemComponent):
    nid = 'equippable spell'
    desc = "This item will be included under the Spells menu. A useful way to separate weapons from utility items like staves or non-damaging tomes. It can counterattack, double, and be equipped."
    tag = ItemTags.BASE
    author = "Windward"

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
        return True

    def can_be_countered(self, unit, item):
        return False