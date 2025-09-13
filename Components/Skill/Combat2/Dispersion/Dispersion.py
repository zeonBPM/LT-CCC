#Allows you to enter a python expression.  When the skill holder takes damage during combat, the damage will be equally divided among all units satisfying the
#evaluated condition.  Multiple potential uses, but probably protect is the most prominent one (see examples for set-up).
#Only the targeted unit can take lethal damage.  Once a supporting unit would reach 1 HP, they can no longer absorb more damage.
#If the original target would be killed even after the damage is distributed, the dispersion will not occur.
#If the damage cannot be divided evenly, any excess damage will be randomly distributed to viable units.
def bin_fill(D,bins):
    L=len(bins)
    temp_bins = bins.copy()
    filled = [0] * L
    fill_level = 0
    residual = 0
    while D > 0 and L>0:
        split = min(min(temp_bins),D//(L))
        if split>0:
            D-=L*split
            for i in range(0,L):
                temp_bins[i]-=split
                
            temp_bins = [val for val in temp_bins if val>0]
            L=len(temp_bins)
            fill_level+=split
        else:
            residual = D
            D = 0
    filled = [min(val,fill_level) for val in bins]
    unfilled = [index for index in range(0,L) if bins[index]>fill_level]
    residual_fill = random.sample(unfilled,residual)
    for index in residual_fill:
        filled[index]+=1
    return filled

class Dispersion(SkillComponent):
    nid = 'dispersion'
    desc = "Shares damage taken with units satisfying the specified condition"
    tag = SkillTags.COMBAT2
    expose = ComponentType.String
    value = ''

    def after_take_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        damage_taken = 0
        playbacks = [p for p in playback if p.nid in ('damage_hit', 'damage_crit') and p.attacker == target]
        for p in playbacks:
            damage_taken += p.damage
        from app.engine import evaluate
        try:
            allies = [u for u in game.units if (u!= unit and u.position and u.get_hp()>1 and evaluate.evaluate(self.value, unit, u, local_args={'mode': mode,'skill': self.skill}))]
        except Exception as e:
            print("Could not evaluate %s (%s)" % (self.value, e))
            return
        if (L:=len(allies))>0 and mode != 'splash' and damage_taken > 1: #Damage dispersion can happen
            allies.append(unit)
            HP = [ally.get_hp()-1 for ally in allies]
            HP[-1]+=1 #Only the target unit can take lethal damage
            dispersed_damage = bin_fill(damage_taken,HP)
            if dispersed_damage[-1] < HP[-1]: #Don't trigger if the target unit is going to die anyway
                for act in reversed(actions): #Remove the damage we would have taken normally
                    if isinstance(act, action.ChangeHP) and act.num < 0 and act.unit == unit:
                        actions.remove(act)
                for disp in playback:
                    if isinstance(disp,pb.DamageHit) or isinstance(disp,pb.DamageCrit):
                        playback.remove(disp)
                for i in range(0,L+1):
                    actions.append(action.ChangeHP(allies[i], -dispersed_damage[i]))
                    playback.append(pb.DamageHit(target, item2, allies[i], dispersed_damage[i], dispersed_damage[i]))
                    
            actions.append(action.TriggerCharge(unit, self.skill))