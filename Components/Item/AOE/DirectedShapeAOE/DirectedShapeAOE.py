#Component which allows for an item affect a user defined AOE, rotated to face in a particular direction.  Example of how to set this up is included.
#I recommend you do not use the 'all' option for target whatsoever.  It will most likely not work the way you want.
#Please contact Squid1003 on the LT discord with any bug reports.

from app.engine.item_components.aoe_components import ShapeBlastAOE
import math

def rotate(coords:list[list], theta:int):
    #Rotate by theta = k*pi/2 radians counterclockwise for k an integer.
    cos = int(math.cos(theta)) 
    sin = int(math.sin(theta))
    new_coords = [[coord[0] * cos + coord[1] * sin, coord[1] * cos-coord[0] * sin] for coord in coords]
    return new_coords

class DirectedShapeAOE(ShapeBlastAOE):
    nid = 'directed_shape_aoe'
    desc = """Affects an area around the target according to the specified shape.  Will rotate based on target location.  Default direction is north.
    Target: Which units are affected by the AOE.
    Range: How far the AOE is extended.  Use range 1 to only include the drawn shape.
    This component will define the item's range.  Do not use in conjunction with other range components."""
    tag = ItemTags.AOE
    
    expose = ComponentType.NewMultipleOptions
    options = {
        'shape': ComponentType.Shape,
        'target': (ComponentType.MultipleChoice, ("ally", "enemy", "unit", "all")),
        'range': ComponentType.Int
    }
    
    _angles = {(0, -1): 0, (1,0): 3*math.pi/2, (0, 1): math.pi, (-1, 0): math.pi/2}
    
    def _get_rotation(self, shape, position, start_position):
        direction = (position[0] - start_position[0],position[1] - start_position[1])
        angle = self._angles[direction]
        if angle != 0:
            return rotate(shape, angle)
        else:
            return shape
            
    def _get_shape(self, position, start_position, rng) -> set:
        value_list = set()
        coords = self.value['shape']
        coords = self._get_rotation(coords, position, start_position)
        for i in range(1, rng):
            for coord in coords:
                value_list.add((start_position[0] + i * coord[0], start_position[1] + i * coord[1]))
        return value_list
    
    def splash(self, unit, item, position) -> tuple:
        rng = self._get_power(unit)
        splash = self._get_shape(position, unit.position, rng)
        splash = {pos for pos in splash if game.tilemap.check_bounds(pos)}
        if self.value['target'] == 'all':
            return None, splash
        from app.engine import item_system
        if item_system.is_spell(unit, item):
            # spell blast
            splash = [game.board.get_unit(s) for s in splash]
            if self.value['target'] == 'ally':
                splash = [s.position for s in splash if s and skill_system.check_ally(unit, s)]
            elif self.value['target'] == 'enemy':
                splash = [s.position for s in splash if s and skill_system.check_enemy(unit, s)]
            elif self.value['target'] == 'unit':
                splash = [s.position for s in splash if s]
            return None, splash
        else:
            # regular blast
            splash = [game.board.get_unit(s) for s in splash if s != position]
            if self.value['target'] == 'ally':
                splash = [s.position for s in splash if s and skill_system.check_ally(unit, s)]
            elif self.value['target'] == 'enemy':
                splash = [s.position for s in splash if s and skill_system.check_enemy(unit, s)]
            elif self.value['target'] == 'unit':
                splash = [s.position for s in splash if s]
            return position if game.board.get_unit(position) else None, splash

    def splash_positions(self, unit, item, position) -> set:
        rng = self._get_power(unit)
        splash = self._get_shape(position, unit.position, rng)
        splash = {pos for pos in splash if game.tilemap.check_bounds(pos)}
        return splash
    
    def range_restrict(self, unit, item) -> set: #Should be unnecessary but just in case its range somehow gets increased.
        return {(1, 0), (-1, 0), (0, 1), (0, -1)}
 
    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        if self.value['target'] == 'all':
            return True
        targets = [game.board.get_unit(s) for s in splash]
        if self.value['target'] == 'ally':
            targets = [s.position for s in targets if s and skill_system.check_ally(unit, s)]
        elif self.value['target'] == 'enemy':
            targets = [s.position for s in targets if s and skill_system.check_enemy(unit, s)]
        elif self.value['target'] == 'unit':
            targets = [s.position for s in targets if s]
        if len(targets) > 0:
            return True
        else:
            return False
            
    def minimum_range(self, unit, item) -> int:
        return 1
        
    def maximum_range(self, unit, item) -> int:
        return 1
