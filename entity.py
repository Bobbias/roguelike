import math
import tcod
from render_functions import RenderOrder

class Entity:
    def __init__(self, x, y, char, color, name, blocks=False,render_order=RenderOrder.CORPSE,
                 fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target, game_map, entities):
        fov = tcod.map_new(game_map.width, game_map.height)

        # set walls unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                        not game_map.tiles[x1][y1].blocked)

        # check to see if there are objects that must be navigated around.
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)
        # allocate A* path
        # 1.41 = normal diagonal cost of moving, set to 0.0 if no diagonal movement
        my_path = tcod.path_new_using_map(fov, 1.41)

        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # check for path and prevent monsters from taking absurd paths
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                self.x = x
                self.y = y
            else:
                # if something is blocking the monster and there is no path
                # we revert to the old system
                self.move_towards(target.x, target.y, game_map, entities)
        tcod.path_delete(my_path)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)



def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None

