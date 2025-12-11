#Allows you to enter a python expression.  The unit using this item will take non-lethal damage equal to the number it evaluates to after each use.

#Please contact Squid1003 on the LT discord with any bug reports.

class BackfireDamage(ItemComponent):
    nid = 'backfire_damage'
    desc = "Deals a certain amount of damage to the user.  Cannot be lethal."
    tag = ItemTags.WEAPON

    expose = ComponentType.String
    value = '0'
    triggered = False

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if not self.triggered:
            self.triggered = True
            from app.engine import evaluate
            try:
                damage = evaluate.evaluate(self.value, unit, target)
                damage = min(damage, unit.get_hp() - 1)
                actions.append(action.ChangeHP(unit, -damage))
                playback.append(pb.DamageHit(unit, item, unit, damage, damage))
            except Exception as e:
                print("Could not evaluate %s (%s)" % (self.value, e))
                
    def end_combat(self, playback, unit, item, target, item2, mode):
        self.triggered = False
