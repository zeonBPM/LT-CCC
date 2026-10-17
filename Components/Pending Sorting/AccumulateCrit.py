class AccummulateCrit(SkillComponent):
    nid = 'accumulate_crit'
    desc = 'Gain +x crit after combat if the unit did not crit.  Resets after landing a crit.'
    tag = SkillTags.CUSTOM
    
    expose = ComponentType.Int
    value = 1
    
    def __init__(self, value = None):
        if value is not None:
            self.value = value
        self.crit = 0
    
    def modify_crit_accuracy(self, unit, item):
        return self.crit
        
    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if any([mark.nid == 'mark_crit' for mark in playback]):
            self.crit = 0
             
    def end_combat(self, playback, unit, item, target, item2, mode):
        if not any([mark.nid == 'mark_crit' for mark in playback]):
            self.crit += self.value
        
    def on_end_chapter_unconditional(self, unit, skill):
        self.crit = 0