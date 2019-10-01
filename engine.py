import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap

LIMIT_FPS = 20  # only for realtime roguelikes

TURN_BASED = True
FULLSCREEN = False

class Rect:
    """Defines a rectangle. Takes x, y, width, and height."""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


def main():
    """Main function for the game."""

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    MAP_WIDTH = 80
    MAP_HEIGHT = 45

    colors = {
        'dark_wall': tcod.Color(0, 0, 100)
        'dark_ground': tcod.Color(50, 50, 150)
    }
    
    player = Entity(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, '@', tcod.white)
    npc = Entity(SCREEN_WIDTH // 2 - 5, SCREEN_HEIGHT // 2, '@', tcod.yellow)
    entities = [npc, player]

    # setup Font
    font_path = 'arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    tcod.console_set_custom_font(font_path, font_flags)

    # init screen
    window_title = 'Python 3 libtcod tutorial'
    con = tcod.console.Console(SCREEN_WIDTH, SCREEN_HEIGHT,
                               window_title, FULLSCREEN)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)

        render_all(con, entities, SCREEN_WIDTH, SCREEN_HEIGHT)

        tcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            if not game_map.is_blocked(player.x + dx, player.y + dy):
                player.move(dx, dy)

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())


if __name__ == '__main__':
    main()
