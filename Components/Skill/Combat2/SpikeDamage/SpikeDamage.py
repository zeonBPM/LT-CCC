#Allows you to enter a python expression which should evaluate to an integer.  When the skill holder is attacked, the attacker takes the evaluated damage amount.
#Damage is available as a local arg if you want spike damage to be related to the amount of damage taken.
class SpikeDamage(SkillComponent):
    nid = 'spike'
    desc = "Attackers take a specified amount of damage per hit.  Cannot be fatal."
    tag = SkillTags.COMBAT2

    expose = ComponentType.String
    value = ''

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        from app.engine import evaluate
        spike_damage = 0
        damage_taken = 0
        for act in reversed(actions):
            if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                damage_taken -= act.num
        try:
            if skill_system.check_enemy(unit, target):
                spike_damage = int(evaluate.evaluate(self.value, unit, target, local_args={'item': item, 'skill': self.skill, 'damage': damage_taken}))
        except:
            logging.error("Couldn't evaluate spike_damage expression" % self.value)
        damage = -utils.clamp(spike_damage, 0, target.get_hp())
        if damage < 0:
            playback.append(pb.DamageHit(unit, item, target, spike_damage, damage))

        actions.append(action.ChangeHP(target, damage))
        actions.append(action.TriggerCharge(unit, self.skill))