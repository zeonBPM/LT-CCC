
class EvalHPCost(ItemComponent):
    nid = 'eval_hp_cost'
    desc = "Item subtracts the specified amount of HP upon use. If the subtraction would kill the unit the item becomes unusable."
    tag = ItemTags.CUSTOM

    expose = ComponentType.String
    value = ""

    _did_something = False

    def _check_value(self, unit, item) -> int:
        from app.engine import evaluate
        try:
            return int(evaluate.evaluate(self.value, unit, local_args={'item': item}))
        except:
            print("Couldn't evaluate %s conditional" % self.value)
        return 0
    
    def available(self, unit, item) -> bool:
        return unit.get_hp() > self._check_value(unit, item)

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self._did_something = True

    def on_miss(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        self._did_something = True

    def end_combat(self, playback, unit, item, target, item2, mode):
        value = self._check_value(unit, item)
        if self._did_something:
            action.do(action.ChangeHP(unit, -value))
        self._did_something = False

    def reverse_use(self, unit, item):
        value = self._check_value(unit, item)
        action.do(action.ChangeHP(unit, value))
