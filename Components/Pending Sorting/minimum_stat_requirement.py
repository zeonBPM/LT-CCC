class MinimumStatRequirement(ItemComponent):
    nid = 'minimum_stat_requirement'
    desc = 'Item can only be used by units that meet one or more minimum stat requirements. Useful for recreating FE1,3 weapon level.'
    tag = ItemTags.USES

    expose = (ComponentType.Dict, ComponentType.Stat)
    value = []

    def available(self, unit, item) -> bool:
        av = True   #this variable will be set to false if a requirement fails
        requirements = {k: v for (k, v) in self.value}
        #checks if unit meets the requirements for all stats
        for x, y in requirements.items():
            if unit.get_stat(x) < y:
                av = False
        return av