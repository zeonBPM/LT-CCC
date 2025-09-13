#Allows for creation of status effects which are only active until the unit takes damage.
class LoseStatusAfterTakeDamage(SkillComponent):
    nid = 'lose_status_after_take_damage'
    desc = "If unit is damaged, they lose the given number of charges of the specified status."
    tag = SkillTags.COMBAT2

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
  
    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        for act in actions:
            if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                to_remove = min(self.value['stacks'],item_funcs.num_stacks(unit,self.value['skill']))
                action.do(action.RemoveSkill(unit, self.value['skill'], to_remove))
                action.do(action.TriggerCharge(unit, self.skill))
                return