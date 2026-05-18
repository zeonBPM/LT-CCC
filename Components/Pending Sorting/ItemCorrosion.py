class ItemCorrosion(SkillComponent):
    nid = 'item_corrosion'
    desc = 'removes X enemy weapon uses at end of combat.'
    tag = SkillTags.COMBAT2
    author = 'Windward'

    expose = ComponentType.Int
    Value = 1

    def end_combat(self, playback, unit, item, target, item2, mode):
        
        # Handles Uses
        if item2.data.get('uses', None) and item2.data.get('starting_uses', None):
            if target and skill_system.check_enemy(unit, target):
                curr_uses = item2.data.get('uses')
                max_uses = item2.data.get('starting_uses')
                action.do(action.SetObjData(item2, 'uses', min(curr_uses - self.value, max_uses)))

            # Handles Chapter Uses
        if item2.data.get('c_uses', None) and item2.data.get('starting_c_uses', None):
            if target and skill_system.check_enemy(unit, target):
                curr_uses = item2.data.get('c_uses')
                max_uses = item2.data.get('starting_c_uses')
                action.do(action.SetObjData(item2, 'c_uses', min(curr_uses - self.value, max_uses)))