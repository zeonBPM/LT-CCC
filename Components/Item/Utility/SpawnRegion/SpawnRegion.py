#Allows an item to create a region at the target position.  Multiple regions can be entered as a comma delimited list (see example 2 for format).
#Use with the included target restrict component is recommended.  I did not handle nid assignment very well in this component, so spawning the same 
#type of region twice in the same locaiton can cause errors.  This could probably be fixed by adjusting the nid assignment in line 63.

from app.engine.objects.region import RegionObject

def create_region(region_nid,position,r_type,sub_type=None,size=(1,1),time=None,actions=None,condition='True'):
    if region_nid in game.level.regions:
        self.logger.error("add_region: RegionObject nid %s already present!" % region)
        return
    new_region = RegionObject(region_nid, regions.RegionType(r_type))
    new_region.position = position
    new_region.size = size
    new_region.sub_nid = sub_type
    new_region.time_left = time
    game.register_region(new_region)
    actions.append(action.AddRegion(new_region))
    if condition != 'True':
        action.do(action.ChangeRegionCondition(new_region, condition))
        
class SpawnRegion(ItemComponent):
    nid = 'spawn_region'
    desc = "Creates a region at the specified tile on hit."
    tag = ItemTags.UTILITY
    expose = ComponentType.NewMultipleOptions

    options = {
        'region_type': ComponentType.String,
        'region_sub_type': ComponentType.String,
        'region_duration': ComponentType.Int,
        'condition': ComponentType.String,
        'region_anim': ComponentType.String,
        'overlay': ComponentType.Bool,
        'size': ComponentType.String
    }

    def __init__(self, value=None):
        self.value = {
            'region_type': None,
            'region_sub_type': None,
            'region_duration': 0,
            'condition': 'True',
            'region_anim': None,
            'overlay': False,
            'size': '1'
        }
        if value:
            self.value.update(value)
    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        if self.value['region_type']:
            region_list = self.value['region_type'].split(',')
            sub_region_list = self.value['region_sub_type'].split(',')
            condition_list = self.value['condition'].split(',')
            size_list = self.value['size'].split(',')
            for i in range(0,min(len(region_list),len(sub_region_list))): #Both lists should be same length, but take min to be safe
                rtype = region_list[i]
                srtype = sub_region_list[i]
                cond = condition_list[i]
                offset = 0
                if int(size_list[i])%2==1: #Can only recenter region if odd size
                    offset = (int(size_list[i])-1)//2 #If region has a size greater than 1, offset so the center is at the target position.
                r_position = (target_pos[0]-offset,target_pos[1]-offset)
                create_region(item.nid+'_'+rtype+str(r_position),r_position,rtype,srtype,(int(size_list[i]),int(size_list[i])),self.value['region_duration'],actions,cond)
            if self.value['region_anim']:
                mode = engine.BlendMode.NONE
                actions.append(action.AddMapAnim(self.value['region_anim'], target_pos, 1.0, mode, self.value['overlay']))
                
class StaffRegionTargetRestrict(ItemComponent):
    nid = 'seal_target_restrict'
    desc = "Item will not target tiles already occupied by the corresponding item region."
    tag = ItemTags.TARGET

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        for r in game.level.regions:
            if r.nid.startswith(item.nid) and r.contains(def_pos):
                return False
        return True