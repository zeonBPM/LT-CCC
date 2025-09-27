class GBAPoisonNonLethal(SkillComponent):
    nid = 'gba_poison_non_lethal'
    desc = "Unit takes random amount of damage up to num.  Cannot drop below 1 HP."
    tag = SkillTags.STATUS

    expose = ComponentType.Int
    value = 5

    def on_upkeep(self, actions, playback, unit):
        old_random_state = static_random.get_combat_random_state()
        hp_loss = -static_random.get_randint(1, self.value)
        new_random_state = static_random.get_combat_random_state()
        actions.append(action.RecordRandomState(old_random_state, new_random_state))
        hp_loss = min(hp_loss, unit.get_hp()-1) #Make damage non-lethal
        actions.append(action.ChangeHP(unit, hp_loss))