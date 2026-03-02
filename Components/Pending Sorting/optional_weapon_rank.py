from app.engine.evaluate import evaluate
import logging

class OptionalWeaponRank(ItemComponent):
    nid = 'optional_weapon_rank'
    desc = 'Weapon has a weapon rank that can be disregarded in certain cases.'
    requires = ['weapon_type']
    tag = ItemTags.WEAPON

    expose = ComponentType.WeaponRank

    def weapon_rank(self, unit, item):
        return self.value

#All these IgnoreWeaponRank will first do a normal weapon rank check(like in WeaponRank) and then do their specific ckeck
#Be careful when using more than one IgnoreWeaponRank component together, failing a condition to ignore weapon rank will cancel a different met condition to IgnoreWeapon rank
class EvalIgnoreWeaponRank(ItemComponent):
    nid = 'eval_ignore_weapon_rank'
    desc = "Weapon ignores weapon rank restrictions while condition is true."
    requires = ['weapon_type']
    paired_with = ('optional_weapon_rank',)
    tag = ItemTags.USES

    expose = ComponentType.String

    def available(self, unit, item) -> bool:
        rank = item_system.weapon_rank(unit, item)  #call the weapon rank
        required_wexp = DB.weapon_ranks.get(rank).requirement
        weapon_type = item_system.weapon_type(unit, item)
        if weapon_type:
            has_enough_wexp = unit.wexp.get(weapon_type) >= required_wexp
            if has_enough_wexp:
                return True
            else:
                try:
                    return bool(evaluate(self.value, unit, local_args={'item': item}))
                except:
                    logging.error("EvalIgnoreWeaponRank: Couldn't evaluate %s conditional" % self.value)
                return False
        else:  # If no weapon type, then always available
            return True
        
class UnitIgnoreWeaponRank(ItemComponent):
    nid = 'unit_ignore_weapon_rank'
    desc = 'Certain units can ignore weapon rank requirements.'
    requires = ['weapon_type']
    paired_with = ('optional_weapon_rank',)
    tag = ItemTags.USES

    expose = (ComponentType.List, ComponentType.Unit)

    def available(self, unit, item) -> bool:
        rank = item_system.weapon_rank(unit, item)  #call the weapon rank
        required_wexp = DB.weapon_ranks.get(rank).requirement
        weapon_type = item_system.weapon_type(unit, item)
        if weapon_type:
            has_enough_wexp = unit.wexp.get(weapon_type) >= required_wexp
            if has_enough_wexp:
                return True
            else:
                return unit.nid in self.value
        else:  # If no weapon type, then always available
            return True
        
class ClassIgnoreWeaponRank(ItemComponent):
    nid = 'class_ignore_weapon_rank'
    desc = 'Certain classes can ignore weapon rank requirements.'
    requires = ['weapon_type']
    paired_with = ('optional_weapon_rank',)
    tag = ItemTags.USES

    expose = (ComponentType.List, ComponentType.Class)

    def available(self, unit, item) -> bool:
        rank = item_system.weapon_rank(unit, item)  #call the weapon rank
        required_wexp = DB.weapon_ranks.get(rank).requirement
        weapon_type = item_system.weapon_type(unit, item)
        if weapon_type:
            has_enough_wexp = unit.wexp.get(weapon_type) >= required_wexp
            if has_enough_wexp:
                return True
            else:
                return unit.klass in self.value
        else:  # If no weapon type, then always available
            return True

class TagIgnoreWeaponRank(ItemComponent):
    nid = 'tag_ignore_weapon_rank'
    desc = 'Units with certain tags can ignore weapon rank requirements.'
    requires = ['weapon_type']
    paired_with = ('optional_weapon_rank',)
    tag = ItemTags.USES

    expose = (ComponentType.List, ComponentType.Tag)

    def available(self, unit, item) -> bool:
        rank = item_system.weapon_rank(unit, item)  #call the weapon rank
        required_wexp = DB.weapon_ranks.get(rank).requirement
        weapon_type = item_system.weapon_type(unit, item)
        if weapon_type:
            has_enough_wexp = unit.wexp.get(weapon_type) >= required_wexp
            if has_enough_wexp:
                return True
            else:
                return any(tag in self.value for tag in unit.tags)
        else:  # If no weapon type, then always available
            return True
        
class AffinityIgnoreWeaponRank(ItemComponent):
    nid = 'affinity_ignore_weapon_rank'
    desc = 'Units with certain affinities can ignore weapon rank requirements.'
    requires = ['weapon_type']
    paired_with = ('optional_weapon_rank',)
    tag = ItemTags.USES

    expose = (ComponentType.List, ComponentType.Affinity)

    def available(self, unit, item) -> bool:
        rank = item_system.weapon_rank(unit, item)  #call the weapon rank
        required_wexp = DB.weapon_ranks.get(rank).requirement
        weapon_type = item_system.weapon_type(unit, item)
        if weapon_type:
            has_enough_wexp = unit.wexp.get(weapon_type) >= required_wexp
            if has_enough_wexp:
                return True
            else:
                return unit.affinity in self.value
        else:  # If no weapon type, then always available
            return True