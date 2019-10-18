import tcod
import tcod.event
from input_handlers import handle_keys, handle_mouse
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all, RenderOrder
from map_objects.game_map import GameMap
from fov_functions import init_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from game_messages import MessageLog, Message
from components.inventory import Inventory

LIMIT_FPS = 20  # only for realtime roguelikes

TURN_BASED = True
FULLSCREEN = False

def main():
    """Main function for the game."""

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    BAR_WIDTH = 20
    PANEL_HEIGHT = 7
    PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

    MAP_WIDTH = 80
    MAP_HEIGHT = 43

    MESSAGE_X = BAR_WIDTH + 2
    MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
    MESSAGE_HEIGHT = PANEL_HEIGHT - 1

    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30

    FOV_ALGORITHM = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    MAX_MONSTERS_PER_ROOM = 3
    MAX_ITEMS_PER_ROOM = 2

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    inventory_component = Inventory(26)
    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    # setup Font
    font_path = '/home/bobbias/roguelike/arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    tcod.console_set_custom_font(font_path, font_flags)

    # init screen
    # window_title = 'Python 3 libtcod tutorial'
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, order='F', renderer=tcod.RENDERER_OPENGL2)
    panel = tcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

    message_log = MessageLog(MESSAGE_X, MESSAGE_WIDTH, MESSAGE_HEIGHT)

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.create_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player, entities, MAX_MONSTERS_PER_ROOM, MAX_ITEMS_PER_ROOM)

    fov_recompute = True
    fov_map = init_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None

    while not tcod.console_is_window_closed():

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        # SECTION: fov and rendering
        
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

        render_all(con, panel, message_log, entities, player, game_map, fov_map, fov_recompute,
                   SCREEN_WIDTH, SCREEN_HEIGHT, BAR_WIDTH, PANEL_HEIGHT, PANEL_Y, mouse, colors,
                   game_state)
        fov_recompute = False

        tcod.console_flush()

        clear_all(con, entities)

        # SECTION: event handler setup

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        move = action.get('move')
        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

        left_click = action.get('left_click')
        right_click = action.get('right_click')

        # SECTION: action handlers

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:
                    player.move(dx, dy)
                    fov_recompute = True
                game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)
                    break
            else:
                message_log.add_message(Message('there is nothing here to pick up.', tcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if (inventory_index is not None
            and previous_game_state != GameStates.PLAYER_DEAD
            and inventory_index < len(player.inventory.items)
        ):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit_game:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        # SECTION: Process player turn results

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')

            if message:
                message_log.add_message(message)
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)
            if item_added:
                entities.remove(item_added)
                game_state = GameStates.ENEMY_TURN
            if item_consumed:
                game_state = GameStates.ENEMY_TURN
            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN
            if drop_inventory:
                previous_game_state = game_state
                game_state = GameStates.DROP_INVENTORY
            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING
                targeting_item = targeting
                message_log.add_message(targeting_item.item.targeting_message)
            if targeting_cancelled:
                game_state = previous_game_state
                message_log.add_message(Message('Targeting cancelled'))

        # SECTION: Process enemy turn

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
