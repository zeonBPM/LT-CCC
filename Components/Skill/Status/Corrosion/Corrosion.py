#Allows the user to specify a percentage of max HP which will be lost on upkeep.
class Corrosion(SkillComponent):
    nid = 'corrosion'
    desc = "Unit loses % of HP at beginning of turn"
    tag = SkillTags.STATUS

    expose = ComponentType.Float
    value = 0.2

    def on_upkeep(self, actions, playback, unit):
        max_hp = equations.parser.hitpoints(unit)
        hp_change = int(-max_hp * self.value)
        if abs(hp_change)>=unit.get_hp():
            hp_change=-unit.get_hp()
        actions.append(action.ChangeHP(unit, hp_change))
        # Playback
        playback.append(pb.HitSound('Attack Hit ' + str(random.randint(1, 5))))
        playback.append(pb.UnitTintAdd(unit, (255, 255, 255)))
        playback.append(pb.DamageNumbers(unit, -hp_change))