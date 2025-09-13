#Allows you to enter a list of growth rate multipliers.
class GrowthMultiplier(SkillComponent):
    nid = 'growth_multiplier'
    desc = "Multiplies stat growths on level up by the specified amount."
    tag = SkillTags.COMBAT

    expose = (ComponentType.FloatDict, ComponentType.Stat)
    value = []

    def growth_change(self, unit):
        return {stat[0]: int((stat[1]-1)*unit.growths[stat[0]]) for stat in self.value}