from map_objects.tile import Tile
from map_objects.rect import Rect
from random import randint
from entity import Entity
import tcod
from components.ai import BasicMonster
from components.fighter import Fighter
from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def create_map(self, max_rooms, room_min, room_max, map_width, map_height, player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            w = randint(room_min, room_max)
            h = randint(room_min, room_max)

            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    player.x, player.y = new_x, new_y
                else:
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)
                self.place_entities(new_room, entities, max_monsters_per_room)
                rooms.append(new_room)
                num_rooms += 1

    def create_room(self, room):
        for x in range(room.x1 +1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range (min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                if randint(0, 100) < 80:
                    fighter_component = Fighter(hp=10, defense=0, power=3)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                else:
                    fighter_component = Fighter(hp=16, defense=1, power=4)
                    ai_component = BasicMonster()
                    monster = Entity(x, y, 'T', tcod.darker_green, 'Troll', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

            if (monster):
                entities.append(monster)


    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
