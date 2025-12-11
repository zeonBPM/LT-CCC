#Pretty much does what it says.  Can be used to make enemies rescue units, among other things.
#Please contact Squid1003 on the LT discord with any bug reports.

class RescueUnit(ItemComponent):
    nid = 'rescue_unit'
    desc = "Rescues the target on hit."
    tag = ItemTags.SPECIAL
   
    def end_combat(self, playback, unit, item, target, item2, mode):
        action.do(action.Rescue(unit, target))
