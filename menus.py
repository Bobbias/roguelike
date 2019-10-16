import tcod

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    header_height = tcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    tcod.console_set_default_background(con, tcod.black)
    tcod.console_clear(con)
    tcod.console_blit(con, 0, 0, width, screen_height, 0, screen_width - width, 0)

    tcod.console_set_default_foreground(con, tcod.white)
    tcod.console_set_default_background(con, tcod.Color(10, 10, 10))
    tcod.console_print_rect_ex(con, 0, 0, width, height, tcod.BKGND_SET, tcod.LEFT, header)

    y = header_height
    letter_index = ord('a')
    for option_text in options:
        if 'empty' in option_text:
            text = option_text
        else:
            text = '({}) {}'.format(chr(letter_index), option_text)
        tcod.console_print_ex(con, 0, y, tcod.BKGND_SET, tcod.LEFT, text)
        y += 1
        letter_index += 1
    x = screen_width - width
    y = 10
    tcod.console_blit(con, 0, 0, width, height, 0, x, y, 1.0, 0.7)

def inventory_menu(con, header, inventory, inventory_width, screen_width, screen_height):
    if len(inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = [item.name for item in inventory.items]
    menu(con, header, options, inventory_width, screen_width, screen_height)
