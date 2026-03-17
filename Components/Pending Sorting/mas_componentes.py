from __future__ import annotations

from app.data.database.components import ComponentType
from app.data.database.database import DB
from app.data.database.skill_components import SkillComponent, SkillTags
from app.engine import (action, banner, combat_calcs, engine, equations,
                        image_mods, item_funcs, item_system, skill_system)
from app.engine.game_state import game
from app.engine.movement import movement_funcs
from app.engine.objects.unit import UnitObject
from app.utilities import utils, static_random
from app.engine.evaluate import evaluate

class UpkeepChargeIncreaseByStat(SkillComponent):
    nid = 'upkeep_charge_increase_by_stat'
    desc = "Increases charge of skill by the *value* set here each upkeep. Usually used in conjunction with `Build Charge` skill component. Will not go below 0 or above `total_charge`"
    tag = SkillTags.CHARGE

    expose = ComponentType.Stat
    value = 'SKL'

    ignore_conditional = True

    def on_upkeep(self, actions, playback, unit):
        estat = unit.stats[self.value] + unit.stat_bonus(self.value)    #to increase the charge
        new_value = self.skill.data['charge'] + estat
        new_value = utils.clamp(new_value, 0, self.skill.data['total_charge'])
        action.do(action.SetObjData(self.skill, 'charge', new_value))

#like SavageStatus but needs the enemy to be killed
class SavageStatusAfterKill(SkillComponent):
    nid = 'savage_status_after_kill'
    desc = 'Inflicts the given status to enemies within the given number of spaces from target after a kill.'
    tag = SkillTags.CUSTOM

    expose = (ComponentType.NewMultipleOptions)
    options = {
        "status": ComponentType.Skill,
        "range": ComponentType.Int,
    }
    
    def __init__(self, value=None):
        self.value = {
            "status": 'Canto',
            "range": 1,
        }
        if value:
            self.value.update(value)

    def end_combat(self, playback, unit, item, target, item2, mode):
        if target and skill_system.check_enemy(unit, target) and target.get_hp() <= 0:
            r = set(range(self.value.get('range') + 1))
            locations = game.target_system.get_shell({target.position}, r, game.board.bounds)
            for loc in locations:
                target2 = game.board.get_unit(loc)
                if target2 and target2 is not target and skill_system.check_enemy(unit, target2):
                    action.do(action.AddSkill(target2, self.value.get('status'), unit))

class SavageCantripStatus(SkillComponent):
    nid = 'savage_cantrip_status'
    desc = 'Inflicts the given status to enemies within the given number of spaces from ally.'
    tag = SkillTags.CUSTOM

    expose = (ComponentType.NewMultipleOptions)
    options = {
        "status": ComponentType.Skill,
        "range": ComponentType.Int,
    }
    
    def __init__(self, value=None):
        self.value = {
            "status": 'Canto',
            "range": 1,
        }
        if value:
            self.value.update(value)

    def end_combat(self, playback, unit, item, target, item2, mode):
        if target and skill_system.check_ally(unit, target):
            r = set(range(self.value.get('range') + 1))
            locations = game.target_system.get_shell({target.position}, r, game.board.bounds)
            for loc in locations:
                target2 = game.board.get_unit(loc)
                if target2 and target2 is not target and skill_system.check_enemy(unit, target2):
                    action.do(action.AddSkill(target2, self.value.get('status'), unit))

#STATUS WITH DAMAGE
class GiveStatusAfterCombatOnDamage(SkillComponent):
    nid = 'give_status_after_combat_on_damage'
    desc = "Gives a status to target after combat assuming you damage the target, like Engage's Poison"
    tag = SkillTags.COMBAT2

    expose = ComponentType.Skill

    def end_combat(self, playback, unit, item, target, item2, mode):
        playbacks = [p for p in playback if p.nid in ('damage_hit', 'damage_crit')]
        total_damage_dealt = 0
        for p in playbacks:
            total_damage_dealt += p.true_damage

        damage = utils.clamp(total_damage_dealt, 0, target.get_hp())
        if damage > 0:
            if target and any(p.attacker is unit for p in playbacks):  # Unit is overall attacker
                action.do(action.AddSkill(target, self.value, unit))
                action.do(action.TriggerCharge(unit, self.skill))

class GiveStatusAfterDamage(SkillComponent):
    nid = 'give_status_after_damage'
    desc = "Gives a status to target after damaging them"
    tag = SkillTags.COMBAT2

    expose = ComponentType.Skill

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        playbacks = [p for p in playback if p.nid in ('damage_hit', 'damage_crit')]
        total_damage_dealt = 0
        for p in playbacks:
            total_damage_dealt += p.true_damage

        damage = utils.clamp(total_damage_dealt, 0, target.get_hp())
        if damage > 0:
            if target and any(p.attacker == unit for p in playbacks):
                actions.append(action.AddSkill(target, self.value, unit))
                actions.append(action.TriggerCharge(unit, self.skill))

class ImbueEquation(SkillComponent):
    nid = 'imbue_equation'
    desc = 'Unit heals HP at the start of the turn equal to chosen equation'

    tag = SkillTags.STATUS
    expose = ComponentType.Equation
    
    def on_upkeep(self, actions, playback, unit):
        from app.utilities.enums import Strike
        hp_change = equations.parser.get(self.value, unit)
        actions.append(action.ChangeHP(unit, hp_change))
        actions.append(action.TriggerCharge(unit, self.skill))
        self._playback_processing(playback, unit, hp_change)
        skill_system.after_take_strike(actions, playback, unit, None, None, None, 'defense', (0, 0), Strike.HIT)

    def _playback_processing(self, playback, unit, hp_change):
        import random
        from app.engine.combat import playback as pb
        # Playback
        if hp_change < 0:
            playback.append(pb.HitSound('Attack Hit ' + str(random.randint(1, 5))))
            playback.append(pb.UnitTintAdd(unit, (255, 255, 255)))
            playback.append(pb.DamageNumbers(unit, hp_change))
        elif hp_change > 0:
            playback.append(pb.HitSound('MapHeal'))
            if hp_change >= 30:
                name = 'MapBigHealTrans'
            elif hp_change >= 15:
                name = 'MapMediumHealTrans'
            else:
                name = 'MapSmallHealTrans'
            playback.append(pb.CastAnim(name))
            playback.append(pb.DamageNumbers(unit, hp_change))