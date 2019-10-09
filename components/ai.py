import tcod

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if monster.distance_to(target) >= 2:
                monster.move_astar(target, game_map, entities)
            elif target.fighter.hp > 0:
                monster.fighter.attack(target)
