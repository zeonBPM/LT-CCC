#An alternate implementation of astra.  If astra procs, the unit can attack up to max_attack additional times.  After each additional attack, there is a 
#follow_up_proc percent chance of another attack activating.  
class AstraAlt(SkillComponent):
    nid = 'astra_alt'
    desc = "Modified astra"
    tag = SkillTags.CUSTOM

    expose = ComponentType.NewMultipleOptions

    options = {
        'max_attacks': ComponentType.Int,
        'damage_percent': ComponentType.Float,
        'show_proc_effects': ComponentType.Bool,
        'follow_up_proc': ComponentType.Int,
    }

    _num_procs = 0  # Number of times this astra has procced
    _should_modify_damage = False  # Are we actually in an astra section of combat
    _hitcount = 0  # Hit counts
    _extra_attacks = 0

    def __init__(self, value=None):
        self.value = {
            'max_attacks': 5,
            'damage_percent': 0.5,
            'show_proc_effects': True,
            'follow_up_proc': 20,
        }
        if value:
            self.value.update(value)

    def start_sub_combat(self, actions, playback, unit, item, target, item2, mode, attack_info):
        # If we haven't done any subattacks
        if attack_info[1] == 0:
            self._num_procs = 0
            self._should_modify_damage = False

        if not self._should_modify_damage:
            self._hitcount = 0

        if not self._should_modify_damage and mode == 'attack' and target and skill_system.check_enemy(unit, target):
            if not get_weapon_filter(self.skill, unit, item):
                return
            proc_rate = get_proc_rate(unit, self.skill)
            i=0
            first=0
            while i < self.value['max_attacks']-1:
                r=static_random.get_combat()
                if r<proc_rate+self.value['follow_up_proc']*first:
                    self._extra_attacks+=1
                    i+=1
                    first=1
                else:
                    proc_rate=0
                    i=self.value['max_attacks']
            if self._extra_attacks>0:
                self._num_procs += 1
                self._should_modify_damage = True
                action.do(action.TriggerCharge(unit, self.skill))
                if bool(self.value['show_proc_effects']):
                    playback.append(pb.AttackProc(unit, self.skill))

    def dynamic_multiattacks(self, unit, item, target, item2, mode, attack_info, base_value) -> int:
        return int(self._extra_attacks) * self._num_procs

    def damage_multiplier(self, unit, item, target, item2, mode, attack_info, base_value):
        if self._should_modify_damage:
            return max(0, float(self.value['damage_percent']))
        return 1

    def after_strike(self, actions, playback, unit, item, target, item2, mode, attack_info, strike):
        if self._should_modify_damage:
            self._hitcount += 1
            if self._hitcount >= int(self._extra_attacks) + 1:    
                self._should_modify_damage = False

    def cleanup_combat(self, playback, unit, item, target, item2, mode):
        # Shouln't be necessary but just in case
        self._num_procs = 0
        self._should_modify_damage = False
        self._hitcount = 0
        self._extra_attacks = 0