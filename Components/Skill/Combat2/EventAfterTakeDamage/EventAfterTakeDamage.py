#Runs a specified event at the end of combat if the user was hit and damaged during combat.
class EventAfterTakeDamage(SkillComponent):
    nid = 'event_after_take_hit'
    desc = "Run an event after combat if damaged."
    tag = SkillTags.COMBAT2

    expose = ComponentType.Event
    _damaged = False

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        for act in actions:
            if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                self._damaged = True
                break
            
    def end_combat(self, playback, unit, item, target, item2, mode):
        if self._damaged:
            event_prefab = DB.events.get_from_nid(self.value)
            if event_prefab:
                local_args = {'item': item, 'item2': item2, 'mode': mode}
                game.events.trigger_specific_event(event_prefab.nid, unit, target, unit.position, local_args)
        self._damaged = False