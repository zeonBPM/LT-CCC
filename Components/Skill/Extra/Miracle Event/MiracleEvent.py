class MiracleEvent(SkillComponent):
    nid = 'miracle_event'
    desc = "Unit will not die after combat, but will instead be resurrected with 1 hp.  Also calls an event on proc."
    tag = SkillTags.COMBAT2
    expose = ComponentType.Event
    miracle_procced = False
    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        for act in reversed(actions):
            if isinstance(act, action.ChangeHP) and -act.num >= act.old_hp and act.unit == unit:
                self.miracle_procced = True

    def cleanup_combat(self, playback, unit, item, target, item2, mode):
        if unit.get_hp() <= 0:
            action.do(action.SetHP(unit, 1))
            game.death.miracle(unit)
            action.do(action.TriggerCharge(unit, self.skill))
    def end_combat(self, playback, unit, item, target, item2, mode):
        if self.miracle_procced:
          self.miracle_procced = False
          event_prefab = DB.events.get_from_nid(self.value)
          if event_prefab:
              local_args = {'item': item, 'item2': item2, 'mode': mode}
              game.events.trigger_specific_event(event_prefab.nid, unit, target, unit.position, local_args)