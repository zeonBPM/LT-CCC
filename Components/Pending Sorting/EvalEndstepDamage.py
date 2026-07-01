class EvalEndstepDamage(SkillComponent):
    nid = 'eval_endstep_damage'
    desc = "Unit takes damage at endstep according to the given evaluation"
    tag = SkillTags.STATUS
    from app.engine import evaluate
    import random

    expose = ComponentType.String
    value = ''

    def _playback_processing(self, playback, unit, hp_change):
        # Playback
        try:
            DMG = int(evaluate.evaluate(self.value, unit))
        except:
            logging.error("Couldn't evaluate %s conditional" % self.value)
            DMG = 0
        if hp_change < 0:
            playback.append(pb.HitSound('Attack Hit ' + str(random.randint(1, 5))))
            playback.append(pb.UnitTintAdd(unit, (255, 255, 255)))
            playback.append(pb.DamageNumbers(unit, DMG))
        elif hp_change > 0:
            playback.append(pb.HitSound('MapHeal'))
            if hp_change >= 30:
                name = 'MapBigHealTrans'
            elif hp_change >= 15:
                name = 'MapMediumHealTrans'
            else:
                name = 'MapSmallHealTrans'
            playback.append(pb.CastAnim(name))
            playback.append(pb.DamageNumbers(unit, DMG))
            
    def on_endstep(self, actions, playback, unit):
        try:
            DMG = int(evaluate.evaluate(self.value, unit))
        except:
            logging.error("Couldn't evaluate %s conditional" % self.value)
            DMG = 0
        hp_change = -DMG
        actions.append(action.ChangeHP(unit, hp_change))
        actions.append(action.TriggerCharge(unit, self.skill))
        self._playback_processing(playback, unit, hp_change)
        skill_system.after_take_strike(actions, playback, unit, None, None, None, 'defense', (0, 0), Strike.HIT)