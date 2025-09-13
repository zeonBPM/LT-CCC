#Same as default ignore damage, but suppresses damage number display.
class IgnoreDamage_mod(SkillComponent):
    nid = 'ignore_damage2'
    desc = "Unit will ignore all damage and not display damage number"
    tag = SkillTags.COMBAT2

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        # Remove any acts that reduce my HP!
        did_something = False
        for act in reversed(actions):
            if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                actions.remove(act)
                did_something = True
        for disp in playback:
            if isinstance(disp,pb.DamageHit) or isinstance(disp,pb.DamageCrit):
                playback.remove(disp)
        playback.append(pb.DamageHit(unit, item2, target, 0, 0))
        if did_something:
            actions.append(action.TriggerCharge(unit, self.skill))