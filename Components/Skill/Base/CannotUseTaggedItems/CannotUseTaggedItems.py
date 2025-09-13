#This component allows you to enter a list of item tags.  Any items with these tags will be unusable by the skill owner.
class CannotUseTaggedItems(SkillComponent):
    nid = 'cannot_use_tagged_item'
    desc = "Unit cannot use items with the given tags"
    tag = SkillTags.BASE
    
    expose = (ComponentType.List, ComponentType.Tag)

    def available(self, unit, item) -> bool:
        return not any(tag in item.tags for tag in self.value)