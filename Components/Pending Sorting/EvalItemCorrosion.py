class EvalItemCorrosion(SkillComponent):
    nid = 'eval_item_corrosion'
    desc = 'removes enemy weapon uses at end of combat, according to the given evaluation.'
    tag = SkillTags.COMBAT2
    author = 'Windward'

    expose = ComponentType.String
    

    def end_combat(self, playback, unit, item, target, item2, mode):

        #Handles Uses
        if item2.data.get('uses', None) and item2.data.get('starting_uses', None):
            curr_uses = item2.data.get('uses')
            max_uses = item2.data.get('starting_uses')
            from app.engine import evaluate
            try:
                corrode = int(evaluate.evaluate(self.value, unit))
            except:
                logging.error("Couldn't evaluate %s conditional" % self.value)
                corrode = 0
            action.do(action.SetObjData(item2, 'uses', min(curr_uses - corrode, max_uses)))

        # Handles Chapter Uses
        if item.data.get('c_uses', None) and item.data.get('starting_c_uses', None):
            curr_uses = item.data.get('c_uses')
            max_uses = item.data.get('starting_c_uses')
            from app.engine import evaluate
            try:
                corrode = int(evaluate.evaluate(self.value, unit))
            except:
                logging.error("Couldn't evaluate %s conditional" % self.value)
                corrode = 0
            action.do(action.SetObjData(item2, 'c_uses', min(curr_uses - corrode, max_uses)))