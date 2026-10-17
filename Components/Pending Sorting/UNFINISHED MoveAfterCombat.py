class MoveAfterCombat(ItemComponent):
    nid = 'move_after_combat'
    desc = """Moves the unit to a new tile after combat.
    Disp: (x,y) displacement from unit's current position.
    Resolve: Method for ensuring the new position is valid.
    Rotate: Whether to rotate coordinates based on target's position.
    """
    tag = ItemTags.SPECIAL
    author = 'Squid'
    expose = ComponentType.NewMultipleOptions
    options = {
        'disp': ComponentType.String,
        'resolve': (ComponentType.MultipleChoice, ("Empty", "Displace")),
        'rotate': ComponentType.Bool
    }
    
    target_pos = None
    _angles = {(0, -1): 0, (1,0): 3*math.pi/2, (0, 1): math.pi, (-1, 0): math.pi/2}
    
    def __init__(self, value=None):
        self.value = {
            'disp': '(0,0)',
            'resolve': "Empty",
            'rotate': True
        }
        if value:
            self.value.update(value)
            
            
    def check_displace(unit, target, magnitude):
        #Check if target can be displaced perpendicularly to the side, and return displaced pos
        p1 = unit.position
        p2 = target.position
        delta = tools.get_vec(p1, p2)      
        delta = (tools.sign(delta[0]), tools.sign(delta[1]))
        delta = tools.rotate([delta], math.pi / 2)[0]
        new_pos = None
        sign = game.get_random(0,1) * 2 - 1
        delta = tools.s_mult(delta, sign)
        new_pos = get_displace_pos(unit, target, delta, magnitude)
        if not new_pos:
            delta = tools.s_mult(delta, -1) #Try reverse direction
            new_pos = get_displace_pos(unit, target, delta, magnitude)
        return new_pos
       
def get_displace_pos(unit, target, delta, magnitude):
    result = None
    for dist in range(1, magnitude+1):
        disp = tools.s_mult(delta, dist)
        new_position = tools.vec_add(target.position, disp)
        mcost = movement_funcs.get_mcost(target, new_position)
        if game.board.check_bounds(new_position) and \
                not game.board.get_unit(new_position) and \
                mcost <= target.get_movement():
            result = new_position
        else: # target can't move through this tile
            break
    return result
    
    
    def _get_new_position(self, unit, def_pos):
        angle = None
        if def_pos and self.value['rotate']:
            p1 = unit.position
            p2 = def_pos
            delta = tools.get_vec(p1, p2)      
            delta = (tools.sign(delta[0]), tools.sign(delta[1]))
            angle = self._angles[delta]
        new_position = None
        try:
            from app.engine import evaluate
            disp = evaluate.evaluate(self.value['disp'], unit, local_args={'def_pos': def_pos})
            disp = (int(disp[0]), int(disp[1])) #Apparently evaluate returns floats
            if angle:
                disp = tools.rotate([disp], angle)[0]
            new_position = tools.vec_add(unit.position, disp)           
        except Exception as e:
            logging.error("Move after combat failed to evaluate disp %s with error %s", self.value['disp'], e)
        return new_position    
    
    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self.target_pos = target_pos

    def on_miss(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self.target_pos = target_pos
   
    def end_combat(self, playback, unit, item, target, item2, mode):
        new_position = None
        if self.target_pos:
            new_position = self._get_new_position(unit, self.target_pos)
        if new_position:
            action.do(action.ForcedMovement(unit, new_position))
            playback.append(pb.ShoveHit(unit, item, unit))
        self.target_pos = None
    
    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        new_position = self._get_new_position(unit, def_pos)
        if new_position and game.board.check_bounds(new_position):
            mcost = movement_funcs.get_mcost(unit, new_position)
            if mcost <= unit.get_movement():
                if self.value['resolve'] == 'Empty':
                    if not game.board.get_unit(new_position):
                        return True
                elif self.value['resolve'] == 'Displace':
                    target = game.board.get_unit(new_position)
                    if (not target) or check_displace(unit, target, 1):
                        return True
        return False