#Allows you to remove a skill from the user after they dodge an attack.
class LoseSkillAfterTakeMiss(SkillComponent):
    nid = 'lose_skill_after_take_miss'
    desc = "Lose X stacks of a skill immediately after an enemy misses you"
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
        if strike == Strike.MISS:
            to_remove = min(self.value['stacks'],item_funcs.num_stacks(unit,self.value['skill']))
            action.do(action.RemoveSkill(unit, self.value['skill'], to_remove))
            action.do(action.TriggerCharge(unit, self.skill))
            return