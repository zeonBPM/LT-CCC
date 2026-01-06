class DynamicCanter(SkillComponent):
    nid = 'dynamic_canter'
    desc = 'Unit moves a number of spaces after taking any action calculated dynamically.'
    tag = SkillTags.MOVEMENT

    author = 'saragl728'
    
    expose = ComponentType.String
    value: str = ""

    def canto_movement(self, unit, unit2) -> int:
        from app.engine.evaluate import evaluate    
        try:
            local_args = {'skill': self.skill}
            return int(evaluate(self.value, unit, local_args=local_args))
        except Exception as e:
            logging.error("Couldn't evaluate %s conditional (%s)", self.value, e)
            return 0

    def has_canto(self, unit, unit2) -> bool:
        """
        Can move again after any action, has exactly the number of movement that was determined in the component
        """
        return True