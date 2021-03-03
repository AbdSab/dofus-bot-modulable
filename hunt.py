import bot
import pyautogui
import event
import messages
import data
import time
import requests
import log
from operator import itemgetter

DIRECTION = {
    6: 'top',
    4: 'left',
    2: 'bottom',
    0: 'right'
}

HUNT_URL_API = lambda x, y, direction, world: "https://dofus-map.com/huntTool/getData.php?x={}&y={}&direction={}&world={}&language=fr".format(x, y, direction, world)

SELECT_LEVEL_BUTTON = lambda x: "assets/img/hunt/level_{}.png".format(x)
JALON_IMG = "assets/img/hunt/jalon.png"
ALL_STEPS = "assets/img/hunt/search_step.png"


hunt_data = None
map_phorror = None
total_steps = None
total_flags = None

def set_jalon():
    coord = pyautogui.locateCenterOnScreen(JALON_IMG, region=(277,249, 314, 384), confidence=0.9)
    pyautogui.click(coord)
    event.wait_for(messages.TreasureHuntMessage)


def get_hunt_data():
    global hunt_data
    if hunt_data is not None:
        return hunt_data
    manual_update_hunt()
    return hunt_data


def get_next_step():
    global hunt_data
    if hunt_data is not None:
        return hunt_data['steps'][-1]
    manual_update_hunt()
    return hunt_data['steps'][-1]

def manual_update_hunt():
    bot.go_to('right')
    set_jalon()
    time.sleep(1)
    pyautogui.click()
    event.wait_for(messages.TreasureHuntMessage)
    bot.go_to('left')


def start():
    bot.zaap("champs de cania")
    bot.go_to('right')
    bot.go_to('right')
    bot.click_on_cell(356-14)
    event.wait_for(messages.MapComplementaryInformationsDataMessage)
    bot.click_on_cell(292)
    event.wait_for(messages.MapComplementaryInformationsDataMessage)
    bot.click_on_cell(288)
    pyautogui.moveTo(x=10, y=100)
    time.sleep(1)
    bot.click_on_image(SELECT_LEVEL_BUTTON(200))
    event.wait_for(messages.TreasureHuntMessage)
    bot.click_on_cell(503)
    event.wait_for(messages.MapComplementaryInformationsDataMessage)
    bot.click_on_cell(556)
    event.wait_for(messages.MapComplementaryInformationsDataMessage)
    bot.travel(hunt_data['map_pos'])
    pass


def update_hunt(msg):
    global hunt_data, total_steps, total_flags
    total_flags = len(msg['flags'])
    total_steps = int(msg['totalStepCount'])
    steps = msg['knownStepsList']
    hunt_data = {
        'map_id': int(msg['startMapId']),
        'map_pos': data.get_map_pos(int(msg['startMapId'])),
        'steps': []
    }
    for step in steps:
        type = step['__type__']
        direction = DIRECTION[step['direction']]
        is_phorror = False
        _id = None
        if type == messages.TreasureHuntStepFollowDirectionToPOI:
            _id = step['poiLabelId']
        elif type == messages.TreasureHuntStepFollowDirectionToHint:
            is_phorror = True
            _id = step['npcId']
        hunt_data['steps'].append({
            'direction': direction,
            'is_phorror': is_phorror,
            'id': _id
        })
    log.log("Next step :{}".format(hunt_data['steps'][-1]))

def get_next_step_pos():
    next_step = get_next_step()
    direction = next_step['direction']
    print(next_step)
    if bot.map_pos is None:
        bot.update_map()
    x, y = bot.map_pos
    world = 0
    url = HUNT_URL_API(x, y, direction, world)
    log.log(url)
    res = requests.get(url)
    res = res.json()
    log.log(res)
    target_id_original = next_step['id']
    target_id = data.get_poi_id(target_id_original)
    steps = next((item['d'] for item in res['hints'] if item['n'] == target_id), None)
    if steps is None:
        steps = next((item['d'] for item in res['hints'] if item['n'] == target_id_original), None)
    log.log("Steps {}".format(steps))
    return steps


def all_steps():
    global total_steps, total_flags
    if total_steps == total_flags:
        pyautogui.click(ALL_STEPS)
        event.wait_for(messages.TreasureHuntMessage)


def go_to_next_step():
    global map_phorror
    next_step = get_next_step()
    print(next_step)
    print(map_phorror)
    if next_step['is_phorror'] == False:
        next_step_steps = get_next_step_pos()
        for i in range(0, next_step_steps):
            bot.go_to(next_step['direction'])
        set_jalon()
        all_steps()
    else:
        if map_phorror == next_step['id']:
            set_jalon()
            all_steps()
            return
        bot.go_to(next_step['direction'])
        go_to_next_step()


def update_map(msg):
    global map_phorror
    map_phorror = None
    for actor in msg['actors']:
        if actor['__type__'] == messages.GameRolePlayTreasureHintInformations:
            map_phorror = actor['npcId']
    print('map changed ', map_phorror)


event.on(messages.TreasureHuntMessage, update_hunt)
event.on(messages.MapComplementaryInformationsDataMessage, update_map)