import event
import bot
import messages
import math
import threading
import combat_utils
import time
import pyautogui

#Parameters
mode = 'near'
script = lambda x: print('fight turn')
#----------

fight_mode = False
entities = []
stats = {}
initial_places = []


def get_enemies():
    global entities
    return list(filter(lambda e: e['is_ally'] is False, entities))


def get_player():
    global entities
    return list(filter(lambda e: e['is_ally'] is True, entities))[0]


def set_ready():
    event.wait_for(messages.GameFightHumanReadyStateMessage)


def update_entities(msg):
    global entities
    entities = []
    for disposition in msg['dispositions']:
        if messages.IdentifiedEntityDispositionInformations == disposition['__type__']:
            entities.append({
                'id': int(disposition['id']),
                'cell_id': disposition['cellId'],
                'is_ally': int(disposition['id']) > 0
            })

def update_stats(msg):
    global stats
    stats = {}
    for current_stats in msg['stats']:
        stats['pv'] = current_stats['lifePoints']
        stats['pa'] = current_stats['actionPointsCurrent']
        stats['pm'] = current_stats['movementPointsCurrent']


def update_movement(msg):
    global entities
    if fight_mode is False:
        return
    index = 0
    for entity in entities:
        if entity['id'] == msg['actorId']:
            break
        index += 1
    entities[index]['cell_id'] = msg['keyMovements'][-1]

def fight_start(msg):
    global fight_mode
    fight_mode = True
    x = threading.Thread(target=start)
    x.start()

def fight_end(msg):
    global fight_mode
    fight_mode = False
    print("ended fight")

def update_initial_places(msg):
    global initial_places
    initial_places = msg['positionsForChallengers']


def start():
    global initial_places
    event.wait_for(messages.GameFightPlacementPossiblePositionsMessage)
    distances = []
    cells = []
    time.sleep(1)
    enemies = get_enemies()
    enemies_coords = [bot.cell_to_coords(x['cell_id']) for x in enemies]
    init_coords = [bot.cell_to_coords(x) for x in initial_places]
    for enemy in enemies_coords:
        for cell in init_coords:
            dist = math.sqrt((cell[0] - enemy[0]) ** 2 + (cell[1] - enemy[1]) ** 2)
            distances.append(dist)
            cells.append(cell)
    nearest = distances.index(min(distances))
    x, y = cells[nearest]
    bot.click_on_pos(x, y)
    bot.click_on_pos(10, 100)
    bot.press('f1')


def fight_script(s):
    global script
    script = s


def start_turn(msg):
    global script
    player = get_player()['id']
    if int(msg['id']) == player:
        script()
        bot.press('f1')

def go_to_nearest_entity():
    pyautogui.moveTo(x=10, y=10)
    enemies = list(map(lambda x: x['cell_id'], get_enemies()))
    cell = combat_utils.get_nearest_cell_entities(get_player()['cell_id'], enemies, 6)
    bot.click_on_cell(cell)
    time.sleep(1)


def enemy_is_cac():
    cells = combat_utils.get_cac_cells(get_player()['cell_id'])
    enemies = list(map(lambda x: x['cell_id'], get_enemies()))
    found = []
    for enemy in enemies:
        if enemy in cells:
            found.append(enemy)
    if len(found) == 0:
        return False
    else:
        return found[0]


event.on(messages.GameFightStartingMessage, fight_start)
event.on(messages.GameFightEndMessage, fight_end)
event.on(messages.GameEntitiesDispositionMessage, update_entities)
#event.on(messages.FighterStatsListMessage, update_stats)
event.on(messages.GameMapMovementMessage, update_movement)
event.on(messages.GameFightPlacementPossiblePositionsMessage, update_initial_places)
event.on(messages.GameFightTurnStartMessage, start_turn)