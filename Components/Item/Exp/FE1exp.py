from app.engine.item_components.exp_components import (determine_all_defenders, 
                                                       determine_all_damaged_defenders,
                                                       determine_all_healed_defenders, 
                                                       modify_exp)


class FEOneExp(ItemComponent):
    nid = 'fe_one_exp'
    desc = "Item gives exp to user based on amount of damage dealt"
    tag = ItemTags.EXP
    author = "Squid1003"
    
    def _calc_exp_normal(self, playback, unit, defender):
        #Non-fatal damage dealt
        damage_defender = 0
        for brush in playback:
            if brush.nid == 'damage_hit' and brush.attacker == unit and brush.defender == defender:
                damage_defender += brush.true_damage
        return min(damage_defender, 20)
       
    def _calc_exp_fatal(self, defender):
        base_exp = defender.get_stat('EXP')
        level = defender.level
        boss = 10 if 'Boss' in defender.tags else 0
        return base_exp + level - 1 + boss
    
    def exp(self, playback, unit, item) -> int:
        total_exp = 0
        defenders = determine_all_damaged_defenders(playback, unit)
        for defender in defenders:
            if not defender.is_dying:
                exp_gained = self._calc_exp_normal(playback, unit, defender)
            else:
                exp_gained = self._calc_exp_fatal(defender)           
            total_exp += exp_gained
        total_exp = utils.clamp(int(total_exp), 0, 100)
        return total_exp