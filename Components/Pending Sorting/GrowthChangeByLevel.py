


class GrowthChangeByLevel(SkillComponent):
    nid = 'equation_growth_by_level'
    desc = "Gives growth rate % bonuses equal to unit internal level.Choose which stats to include."
    tag = SkillTags.CUSTOM
    author = 'Dung'

    expose = (ComponentType.List, ComponentType.Stat)

    def growth_change(self, unit):
        growth_bonus = unit.get_internal_level()
        return {stat_nid: growth_bonus for stat_nid in DB.stats.keys() if stat_nid in self.value}