#SHOW 10 STATS ON LEVEL UP RATHER THAN 8
by PKLucky
go to this file and line and replace accordingly
you'd also need to add a new graphic to your custom sprites folder that can fit another row of stats(for the level up screen) and adjust the portrait and level op quote position accordingly. the provided ones are for a 10/12/14 stat UI, courtesy of Prismatic Empress
this was done in 24/07/26, engine updates may change things in the future

lt-maker/app/engine/level_up.py (line 436)


def __init__(self, parent, unit, stat_changes, old_level, new_level):
        self.parent = parent
        self.unit = unit
        self.stat_list = [stat_changes.get(nid, 0) for nid in DB.stats.keys()]
        self.stat_list = self.stat_list[:10]  # Can only show first 8 stats on level up by default
        self.old_level = old_level
        self.new_level = new_level

def get_position(self, i, absolute=False):
        tl_offset = (0, 0)
        if absolute:
            tl_offset = self.topleft()
        if i >= 5:
            position = (self.width//2 + 8 + tl_offset[0], (i - 5) * 16 + 35 + tl_offset[1])
        else:
            position = (10 + tl_offset[0], i * 16 + 35 + tl_offset[1])
        return position