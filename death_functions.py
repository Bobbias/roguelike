import tcod

from game_states import GameStates


def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return 'you died!', GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = '{} is dead!'.format(monster.name.captialize())

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of {}'.format(monster.name)

    return death_message
