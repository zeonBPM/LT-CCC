#Two related components which allow adding mulitple stacks of a status when using an item.
#Note SelfStatusStacksOnHit is a subclass of StatusStacksOnHit, so it cannot be used unless you also have StatusStacksOnHit in your custom components file.
#Please contact Squid1003 on the LT discord with any bug reports.

from app.engine.item_components.hit_components import ai_status_priority

class StatusStacksOnHit(ItemComponent):
    nid = 'status_stacks_on_hit'
    desc = "Target gains X stacks of the specified status on hit. Applies instantly, potentially causing values to change mid-combat."
    tag = ItemTags.SPECIAL

    expose = ComponentType.NewMultipleOptions
    options = {
        'skill': ComponentType.Skill,
        'stacks': ComponentType.Int
    }

    def __init__(self, value=None):
        self.value = {
            'skill': None,
            'stacks': 0
        }
        if value:
            self.value.update(value)
            
    def _get_target(self, unit, target):
        return target

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        for i in range(0, self.value['stacks']):
            act = action.AddSkill(self._get_target(unit,target), self.value['skill'], unit)
            action.do(act)
        playback.append(pb.StatusHit(unit, item, target, self.value['skill']))

    def ai_priority(self, unit, item, target, move):
        # Do I add a new status to the target
        return ai_status_priority(unit, target, item, move, self.value['skill'])
        
class SelfStatusStacksOnHit(StatusStacksOnHit):
    nid = 'self_status_stacks_on_hit'
    desc = "Unit gains X stacks of the specified status on hit. Applies instantly, potentially causing values to change mid-combat."
    
    def _get_target(self, unit, target):
        return unit
