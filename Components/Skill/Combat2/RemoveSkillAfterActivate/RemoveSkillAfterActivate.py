#Causes the specified skill to be lost next time the skill holder engages in any combat.
class RemoveSkillAfterActivate(SkillComponent):
    nid = 'remove_skill_after_activate'
    desc = "Lose the specified skill after combat ends."
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

    def end_combat(self, playback, unit, item, target, item2, mode):
        to_remove = min(item_funcs.num_stacks(unit, self.value['skill']), self.value['stacks'])
        action.do(action.RemoveSkill(unit, self.value['skill'],to_remove))