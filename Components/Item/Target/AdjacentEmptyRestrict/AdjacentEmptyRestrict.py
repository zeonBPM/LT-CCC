#Prevents an item from being used if there are no open tiles adjacent to the user.  Useful for things like the rescue staff.

from app.engine.movement import movement_funcs

class AdjacentEmptyRestrict(ItemComponent):
    nid = 'adjacentemptyrestrict'
    desc = "Prevents units from using this item if no adjacent squares are open."
    tag = ItemTags.TARGET
    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        for i in [-1,1]:
            pos = (unit.position[0]+i,unit.position[1])
            target = game.board.get_unit(def_pos)
            if target and game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(target,pos):
                return True
        for j in [-1,1]:
            pos = (unit.position[0],unit.position[1]+j)
            target = game.board.get_unit(def_pos)
            if target and game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(target,pos):
                return True
        return False 