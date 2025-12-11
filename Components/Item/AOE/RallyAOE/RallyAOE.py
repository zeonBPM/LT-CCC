#Minor edit to ally blast aoe which prevents the user from being included.  Primarily for rally skills.
#Please contact Squid1003 on the LT discord with any bug reports.

class RallyAOE(ItemComponent):
    nid = 'rally_blast_aoe'
    desc = "Gives Blast AOE that affects allies but not the user"
    tag = ItemTags.AOE
    expose = ComponentType.Int  # Radius
    value = 1

    def _get_power(self, unit) -> int:
        empowered_splash = skill_system.empower_splash(unit)
        return self.value + 1 + empowered_splash

    def splash_positions(self, unit, item, position) -> set:
        ranges = set(range(self._get_power(unit)))
        splash = game.target_system.find_manhattan_spheres(ranges, position[0], position[1])
        splash = {pos for pos in splash if game.tilemap.check_bounds(pos)}
        return splash

    def splash(self, unit, item, position) -> tuple:
        ranges = set(range(self._get_power(unit)))
        splash = game.target_system.find_manhattan_spheres(ranges, position[0], position[1])
        splash = {pos for pos in splash if game.tilemap.check_bounds(pos)}
        from app.engine import skill_system
        splash = [game.board.get_unit(s) for s in splash]
        splash = [s.position for s in splash if s and skill_system.check_ally(unit, s) and s!=unit]
        return None, splash 
