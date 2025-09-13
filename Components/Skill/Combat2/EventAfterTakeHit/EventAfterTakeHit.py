#Runs a specified event at the end of combat if the user was hit during combat.  Will trigger even if no damage was taken.
class EventAfterTakeHit(SkillComponent):
    nid = 'event_after_take_hit'
    desc = "Run an event after combat if hit."
    tag = SkillTags.COMBAT2

    expose = ComponentType.Event
    _hit = False

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if strike == Strike.HIT:
            self._hit = True
            
    def end_combat(self, playback, unit, item, target, item2, mode):
        if self._hit:
            event_prefab = DB.events.get_from_nid(self.value)
            if event_prefab:
                local_args = {'item': item, 'item2': item2, 'mode': mode}
                game.events.trigger_specific_event(event_prefab.nid, unit, target, unit.position, local_args)
        self._hit = False