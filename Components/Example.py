
#If you want, add a short description or use case for your component. And which game uses it.
#Restore is used to remove all statuses marked as negative(mainly debuffs), similar to an active use Nihil. will do nothing if no status in the target has the negative component.


#Add all required imports

from app.engine import action
from app.engine import item_system, item_funcs, skill_system, equations
from app.engine.combat import playback as pb


#Add the main component, this is the default restore from LT
class Restore(ItemComponent):
    nid = 'restore'
    desc = "Item removes all negative statuses from target on hit"
    tag = ItemTags.UTILITY

    def _can_be_restored(self, status):
        return status.negative

    def target_restrict(self, unit, item, def_pos, splash) -> bool:
        defender = game.board.get_unit(def_pos)
        # only targets units that need to be restored
        if defender and skill_system.check_ally(unit, defender) and any(self._can_be_restored(skill) for skill in defender.skills):
            return True
        for s_pos in splash:
            s = game.board.get_unit(s_pos)
            if skill_system.check_ally(unit, s) and any(self._can_be_restored(skill) for skill in s.skills):
                return True
        return False

    def on_hit(self, actions, playback, unit, item, target, item2, target_pos, mode, attack_info):
        for skill in target.all_skills[:]:
            if self._can_be_restored(skill):
                actions.append(action.RemoveSkill(target, skill))
                playback.append(pb.RestoreHit(unit, item, target))



#If you have a component that extends another one, add it after the dependency. This is RestoreSpecific, that uses Restore as a base
class RestoreSpecific(Restore):
    nid = 'restore_specific'
    desc = "Item removes specific status from target on hit"
    tag = ItemTags.UTILITY

    expose = ComponentType.Skill # Nid

    def _can_be_restored(self, status):
        return status.nid == self.value

