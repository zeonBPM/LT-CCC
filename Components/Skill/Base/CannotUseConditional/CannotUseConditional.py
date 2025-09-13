#This component allows you to enter a python expression.  If it evaluates to false for a unit/item pair, the item will be unusable.
#Example file shows usage to restrict the unit to only be able to use a specific weapon, for instance.
class CannotUseConditional(SkillComponent):
    nid = 'cannot_use_condition'
    desc = "Unit cannot use or equip items unless the condition is true."
    tag = SkillTags.BASE
    
    expose = ComponentType.String

    def available(self, unit, item) -> bool:
        from app.engine import evaluate
        try:
            condition = evaluate.evaluate(self.value, unit, local_args={'item': item})
            return condition
                
        except Exception as e:
            logging.error("CannotUseCondition failed to evaluate condition %s with error %s", self.value, e)
            return