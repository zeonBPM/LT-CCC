class HealOnUpkeep(SkillComponent):
    nid = 'heal_on_upkeep'
    desc = "Unit will heal +X HP on upkeep"
    tag = SkillTags.STATUS
    author = 'zeonBPM'


    expose = ComponentType.Int

    def on_upkeep(self, actions, playback, unit):
            heal = self.value
            if heal > 0:
                actions.append(action.ChangeHP(unit, heal))
                playback.append(pb.HitSound('MapHeal'))
                playback.append(pb.DamageNumbers(unit, -heal))
                if heal >= 30:
                    name = 'MapBigHealTrans'
                elif heal >= 15:
                    name = 'MapMediumHealTrans'
                else:
                    name = 'MapSmallHealTrans'
                playback.append(pb.CastAnim(name))