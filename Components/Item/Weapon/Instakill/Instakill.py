#Allows you to enter a python expression.  The value it evaluates to gives the probability the item will instantly kill the target.
#I use the random module rather than LT's built in random functions, so this component's behavior will not be preserved by turnwheel.  Change the defintion
#of r if you want to adjust this.

#Known 'bug': it takes a long time for the target's HP to drain if the target has a large HP pool (eg in the hundreds)

#Please contact Squid1003 on the LT discord with any bug reports.

import random

class Instakill(ItemComponent):
    nid = 'Instakill'
    desc = "Item instantly kills the target with a specified probability."
    tag = ItemTags.WEAPON

    expose = ComponentType.String
    value = 'False'

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        r=random.randint(1,100)
        damage = 0
        from app.engine import evaluate
        try:
            threshold = evaluate.evaluate(self.value, unit, target, local_args={'item': item})
            if r<=threshold:
                damage = target.get_hp()
                for act in reversed(actions):
                    if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == target:
                        actions.remove(act)
                for disp in playback:
                    if isinstance(disp,pb.DamageHit) or isinstance(disp,pb.DamageCrit) or (isinstance(disp,pb.HitSound) and disp.sound.startswith('Attack Hit')):
                        playback.remove(disp)
                actions.append(action.SetHP(target, 0))
                playback.append(pb.DamageHit(unit, item, target, 999, damage))
        except Exception as e:
            print("Could not evaluate %s (%s)" % (self.value, e))
