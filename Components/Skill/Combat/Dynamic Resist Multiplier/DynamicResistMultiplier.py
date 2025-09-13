#Allows you to enter a python expression which should evaluate to a float.  Damage taken will be multiplied by this value, evaluated dynamically during combat.
class DynamicResistMultiplier(SkillComponent):
    nid = 'dynamic_resist_multiplier'
    desc = "Multiplies damage taken by a fraction"
    tag = SkillTags.COMBAT

    expose = ComponentType.String

    def resist_multiplier(self, unit, item, target, item2, mode, attack_info, base_value):
        from app.engine import evaluate
        try:
            local_args = {'item': item, 'item2': item2, 'mode': mode, 'skill': self.skill, 'attack_info': attack_info, 'base_value': base_value}
            return float(evaluate.evaluate(self.value, unit, target, unit.position, local_args))
        except Exception:
            print("Couldn't evaluate %s conditional" % self.value)
            return 1