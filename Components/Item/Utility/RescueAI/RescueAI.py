#Aids in the creation of an AI usable rescue staff.  See example for full set-up.
#The AI will favor rescuing hurt allies, high level units, and distant units.  The ai_priority can be modified for different behavior.
#You can also enter a python condition on the component.  If it evaluates to true for a unit, that unit will be targeted by rescue.

#I use the random module rather than LT's built in random functions, so this component's behavior will not be preserved by turnwheel.  Change the defintion
#of r if you want to adjust this.

#Please contact Squid1003 on the LT discord with any bug reports.

import random
from app.engine.movement import movement_funcs

class RescueStaffAI(ItemComponent):
    nid = 'rescueai'
    desc = "Creates an AI usable rescue staff."
    tag = ItemTags.UTILITY
    expose = ComponentType.String
    value = 'False'

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        un = game.board.get_unit(target_pos)
        valid_pos = []
        for i in [-1,1]:
            pos = (unit.position[0]+i,unit.position[1])
            if game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(un,pos):
                valid_pos.append(pos)
            pos = (unit.position[0],unit.position[1]+i)
            if game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(un,pos):
                valid_pos.append(pos)
        L = len(valid_pos)
        if L>0: #Should always be the case, but just to be safe
            r=random.randint(0,L-1)
            t_pos=valid_pos[r]
            playback.append(pb.RescueHit(unit, item, target))
            actions.append(action.Warp(target, t_pos))
    def end_combat(self, playback, unit, item, target, item2, mode):
        if target.position:
            game.cursor.set_pos(target.position)

    def ai_priority(self, unit, item, target, move):
        if target and skill_system.check_ally(unit, target):
            priority_term = 0
            from app.engine import evaluate
            try:
                if evaluate.evaluate(self.value, unit, target, local_args={'item': item}):
                    priority_term = 10
            except Exception as e:
                print("Could not evaluate %s (%s)" % (self.value, e))
            max_hp = target.get_max_hp()
            missing_health = max_hp - target.get_hp()
            if missing_health == 0 and priority_term == 0:
                return 0
            help_term = utils.clamp(missing_health / float(max_hp), 0, 1)*.3
            level_term = utils.clamp(target.get_internal_level() / 50.0, 0, 1)*.15
            distance_term = utils.calculate_distance(unit.position,target.position)*.005
            return help_term + level_term +priority_term +distance_term
        return 0
