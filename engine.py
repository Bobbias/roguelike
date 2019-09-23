import libtcodpy as tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20  #only for realtime roguelikes
TURN_BASED = True
FULLSCREEN = False

player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

def get_key_event(turn_based=None):
    """Return key function for turn based or realtime gameplay"""
    if turn_based:
        key = tcod.console_wait_for_keypress(True)
    else:
        key = tcod.console_check_for_keypress()
    return key




def handle_keys():
    """Handle Keypresses"""
    global player_x, player_y #eww
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
