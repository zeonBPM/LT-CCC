import random

class RandomSkillAtUpkeep(SkillComponent):
    nid = 'random_skill_at_upkeep'
    desc = "Unit gains one of the following skills at the start of the turn."
    tag = SkillTags.CUSTOM
    author = 'saragl728'

    expose = (ComponentType.List, ComponentType.Skill)
    value = []

    def on_upkeep(self, actions, playback, unit):
        #choose a random value from the list
        eskil = random.choice(self.value)
        action.do(action.AddSkill(unit, eskil))