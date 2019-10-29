import tcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    window = tcod.console_new(width, height)
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '({}) {}'.format(chr(letter_index), option_text)
        tcod.console_print_ex(window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]
    menu(con, header, options, inventory_width, screen_width, screen_height)

def main_menu(con, background_image, screen_width, screen_height):
    tcod.image_blit_2x(background_image, 0, 0, 0)

    tcod.console_set_default_foreground(0, tcod.light_yellow)
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4,
                     tcod.BKGND_NONE, tcod.CENTER, 'TOMBS OF THE ANCIENT KINGS')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2), tcod.BKGND_NONE, tcod.CENTER, 'By: Bobbias')

    menu(con, '', ['New Game', 'Continue', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 hp from {})'.format(player.fighter.max_hp),
               'Strength (+1 attack from {})'.format(player.fighter.power),
               'Agility (+1 defense from {})'.format(player.fighter.defense)]
    menu(con, header, options, menu_width, screen_width, screen_height)

def player_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = tcod.console_new(character_screen_width, character_screen_height)
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Character Information')
    tcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Level: {}'.format(player.level.current_level))
    tcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Experience: {}'.format(player.level.current_xp))
    tcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Experience to level: {}'.format(player.level.experience_to_next_level))
    tcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Maximum HP: {}'.format(player.fighter.max_hp))
    tcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Attack: {}'.format(player.fighter.attack))
    tcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, tcod.BKGND_NONE,
                               tcod.LEFT, 'Defense: {}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    tcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
