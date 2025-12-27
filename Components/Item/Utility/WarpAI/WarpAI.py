#Aids in the creation of an AI usable warp staff.  See example for full set-up.
#If aggressive targeting is checked, the AI will try to warp near low HP and/or lord units.

#I use the random module rather than LT's built in random functions, so this component's behavior will not be preserved by turnwheel.  Change the defintion
#of r if you want to adjust this.

#Please contact Squid1003 on the LT discord with any bug reports.

import random
from app.engine.movement import movement_funcs

class WarpStaffAI(ItemComponent):
    nid = 'warpai'
    desc = "Creates an AI usable warp staff."
    tag = ItemTags.UTILITY
    expose = ComponentType.NewMultipleOptions

    options = {
        'warp_range': ComponentType.Int,
        'aggressive_targeting': ComponentType.Bool,
    }

    def __init__(self, value=None):
        self.value = {
            'warp_range': 10,
            'aggressive_targeting': False,
        }
        if value:
            self.value.update(value)

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        enemies = [u for u in game.units if u.position and skill_system.check_enemy(u, target)]
        min_pos=[]
        min_dist=9999
        for i in range(-self.value['warp_range'],self.value['warp_range']+1):
            for j in range(-(self.value['warp_range']-abs(i)),self.value['warp_range']+1-abs(i)):
                pos = (unit.position[0]+i,unit.position[1]+j)
                if game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(target,pos):
                    dist_list = [utils.calculate_distance(enemy.position, pos) for enemy in enemies]
                    if len(dist_list)>0: #Should always be the case, but just to be safe
                        M=min(dist_list)
                        if M<min_dist:
                            min_dist = M
                            min_pos.clear()
                            min_pos.append(pos)
                        elif M==min_dist:
                            min_pos.append(pos)   
        L = len(min_pos)
        if L>0: #Again, should always be true
            if self.value['aggressive_targeting']:
                max_score = 0
                priority_pos = []
                for i in range(0,L):
                    score = 0
                    for enemy in enemies:
                        if utils.calculate_distance(enemy.position,min_pos[i])==min_dist:
                            e_score = (enemy.team=='player')*20+('Lord' in enemy.tags)*10+utils.calculate_distance(min_pos[i],unit.position)*.5+(1-enemy.get_hp()/enemy.get_max_hp())*30
                            score = max(e_score,score)
                    if score>max_score:
                        max_score = score
                        priority_pos.clear()
                        priority_pos.append(min_pos[i])
                    elif score == max_score:
                        priority_pos.append(min_pos[i])
                r=random.randint(0,len(priority_pos)-1)
                t_pos = priority_pos[r]            
            else:
                r=random.randint(0,L-1)
                t_pos=min_pos[r]
            playback.append(pb.RescueHit(unit, item, target))
            actions.append(action.Warp(target, t_pos)) 
            
    def end_combat(self, playback, unit, item, target, item2, mode):
        if target.position:
            game.cursor.set_pos(target.position)

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        from app.engine import evaluate
        for i in range(-self.value['warp_range'],self.value['warp_range']+1):
            for j in range(-(self.value['warp_range']-abs(i)),self.value['warp_range']+1-abs(i)):
                pos = (unit.position[0]+i,unit.position[1]+j)
                target = game.board.get_unit(def_pos)
                if target and game.board.check_bounds(pos) and not game.board.get_unit(pos) and movement_funcs.check_traversable(target,pos) and pos!=unit.position:
                    return True
        return False
