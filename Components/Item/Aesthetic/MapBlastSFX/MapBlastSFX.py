#Prevents splash items from playing the item's sound effect multiple times.

class MapBlastSFX(ItemComponent):
    nid = 'blast_hit_sfx'
    desc = "Plays sound a single time per combat."
    tag = ItemTags.AESTHETIC

    expose = ComponentType.Sound
    value = 'Attack Hit 1'
    num = 0

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        if self.num == 0:
            playback.append(pb.HitSound(self.value))
            self.num = 1
    def end_combat(self, playback, unit, item, target, item2, mode):
        self.num = 0