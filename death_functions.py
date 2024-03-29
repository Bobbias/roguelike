import tcod

from game_states import GameStates
from render_functions import RenderOrder
from game_messages import Message

def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    return Message('you died!', tcod.red), GameStates.PLAYER_DEAD

def kill_monster(monster):
    death_message = Message('{} is dead!'.format(monster.name.capitalize()), tcod.orange)

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of {}'.format(monster.name)
    monster.render_order = RenderOrder.CORPSE

    return death_message
