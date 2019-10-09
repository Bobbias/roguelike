import tcod
import tcod.event
from input_handlers import handle_keys
from entity import Entity, get_blocking_entities_at_location
from render_functions import render_all, clear_all
from map_objects.game_map import GameMap
from fov_functions import init_fov, recompute_fov
from game_states import GameStates
from components.fighter import Fighter
from death_functions import kill_monster, kill_player

LIMIT_FPS = 20  # only for realtime roguelikes

TURN_BASED = True
FULLSCREEN = False

def main():
    """Main function for the game."""

    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50

    MAP_WIDTH = 80
    MAP_HEIGHT = 45

    ROOM_MAX_SIZE = 10
    ROOM_MIN_SIZE = 6
    MAX_ROOMS = 30

    FOV_ALGORITHM = 0
    FOV_LIGHT_WALLS = True
    FOV_RADIUS = 10

    max_monsters_per_room = 3

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.Color(50, 50, 150),
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', tcod.white, 'Player', blocks=True, fighter=fighter_component)
    entities = [player]

    # setup Font
    font_path = '/home/bobbias/roguelike/arial10x10.png'
    font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    tcod.console_set_custom_font(font_path, font_flags)

    # init screen
    # window_title = 'Python 3 libtcod tutorial'
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, order='F')

    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
    game_map.create_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player, entities, max_monsters_per_room)

    fov_recompute = True
    fov_map = init_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()

    game_state = GameStates.PLAYERS_TURN

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, key, mouse)
        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)

        render_all(con, entities, player, game_map, fov_map, fov_recompute, SCREEN_WIDTH, SCREEN_HEIGHT, colors)
        fov_recompute = False

        tcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key)

        move = action.get('move')
        exit_game = action.get('exit')
        fullscreen = action.get('fullscreen')

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

        if exit_game:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)
            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state = GameStates.PLAYER_DEAD:
                                break
                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
