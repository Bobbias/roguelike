import libtcodpy as tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20  #only for realtime roguelikes

TURN_BASED = True
FULLSCREEN = False

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

color_dark_wall = tcod.Color(0, 0, 100)
color_dark_ground = tcod.Color(50, 50, 150)

class Tile:
    """A tile in the map. Can block movement or sight."""
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        block_sight = blocked if block_sight is None else None
        self.block_sight = block_sight

class Rect:
    """Defines a rectangle. Takes x, y, width, and height."""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

class Object:
    """Generic object class for defining new objects to display. Takes x, y, char, color."""
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        if not game_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(0, self.color)
        tcod.console_put_char(0, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(0, self.x, self.y, ' ', tcod.BKGND_NONE)

def create_room(room):
    global game_map #TODO: clean this up.
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False

def create_v_tunnel(y1, y2, x):
    global game_map #TODO: clean this up.
    for y in range(min(y1, y2), max(y1, y2) + 1):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False

def create_h_tunnel(x1, x2, y):
    global game_map #TODO: clean this up.
    for x in range(min(x1, x2), max(x1, x2) + 1):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False

def make_map():
    global game_map #TODO: Refactor this shit.
    game_map = [
        [Tile(True) for y in range(MAP_HEIGHT)]
        for x in range(MAP_WIDTH)
        ]

    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(20, 15, 10, 15)
    create_room(room1)
    create_room(room2)

    create_h_tunnel(22, 55, 23)

    player_x = 25
    player_y = 23

def get_key_event(turn_based=None):
    """Return key function for turn based or realtime gameplay."""
    if turn_based:
        key = tcod.console_wait_for_keypress(True)
    else:
        key = tcod.console_check_for_keypress()
    return key

def handle_keys():
    """Handle Keypresses"""
    global player_x, player_y #TODO: Refactor this.
    key = get_key_event(TURN_BASED)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif key == tcod.KEY_ESCAPE:
        return True

    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player_y = player_y - 1
    if tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player_y = player_y + 1
    if tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player_x = player_x - 1
    if tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player_x = player_x + 1

def main():
    """Main function for the game."""

    #setup Font
    font_path = 'arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    tcod.console_set_custom_font(font_path, font_flags)

    #init screen
    window_title = 'Python 3 libtcod tutorial'
    tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, FULLSCREEN)

    tcod.sys_set_fps(LIMIT_FPS)  #only for realtime roguelikes

    exit_game = False
    while not tcod.console_is_window_closed() or not exit_game:
        tcod.console_set_default_foreground(0, tcod.white)

        tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)

        tcod.console_flush()
        tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)

        exit_game = handle_keys()

if __name__ == '__main__':
    main()
