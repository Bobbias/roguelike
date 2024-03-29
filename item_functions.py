import tcod
from game_messages import Message
from components.ai import ConfusedMonster


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False,
                        'message': Message('You are already at full health.', tcod.yellow)
        })
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True,
                        'message': Message('Your wounds start to feel better!', tcod.green)
        })
    return results

def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True,
                        'target': target,
                        'message': Message(('A lightning bolt strikes {} with a loud thunder! '
                        'Dealing {} damage.').format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False,
                        'target': None,
                        'message': Message('No enemy is close enough to strike.', tcod.red)})

    return results

def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage  = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results

    results.append({'consumed': True,
                    'message': Message('The fireball explodes, burning everything within {} tiles!'.format(radius),
                                       tcod.orange)})
    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append({'message': Message('The {} gets burned for {} hit points'.format(entity.name, damage),
                                               tcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False,
                        'message': Message('You cannot target a tile outside your field of view.', tcod.yellow)})
        return results
    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True,
                            'message': Message('The eyes of the {} look vacant, '
                                               'as it begins to stumble around.'.format(entity.name),
                                               tcod.light_green)})
            break
        else:
            results.append({'consumed': False,
                            'message': Message('There is no targetable enemy at that location.', tcod.yellow)})
    return results
