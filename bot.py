import event
import data
import pyautogui
import messages
import time
import log
import math
import chat
import threading

DIRECTIONS_COORDS = {
    "right": (1572, 500),
    "bottom": (900, 907),
    "top": (904, 35),
    "left": (343, 600)
}

map_id = None
map_pos = None
world = None
elements = []


def update_map_state(msg):
    global map_id, map_pos, elements
    map_id = int(msg['mapId'])
    map_pos = data.get_map_pos(map_id)
    elements = []
    if messages.interactiveElements in msg:
        elm = [{'elementId': x['elementId'], 'elementTypeId': x['elementTypeId'], 'onCurrentMap': x['onCurrentMap']} for x in msg[messages.interactiveElements]]
        if messages.statedElements in msg:
            for e in elm:
                e_type_id = e['elementTypeId']
                e_id = e['elementId']
                found = next((item for item in msg[messages.statedElements] if item["elementId"] == e_id), None)
                if found is not None:
                    elements.append({
                        'id': e_type_id,
                        'elementCellId': found['elementCellId'],
                        'elementState': found['elementState'],
                        'onCurrentMap': found['onCurrentMap']
                    })
    elements = list(filter(lambda x: x['onCurrentMap'] is True, elements))
    log.log("{} Ressoucres : {}".format(map_pos, list(map(lambda x: x['id'], elements))))


def go_to(direction):
    log.log("Going to {}".format(direction))
    x, y = DIRECTIONS_COORDS[direction]
    pyautogui.click(x=x, y=y)
    event.wait_for(messages.MapComplementaryInformationsDataMessage, 10)


def enter_door(x, y):
    click_on_pos(x, y)
    event.wait_for(messages.MapComplementaryInformationsDataMessage)


def click_on_pos(x, y):
    pyautogui.click(x=x, y=y)


def cell_to_coords(cell_id):
    u_x = cell_id % 28
    i_x = cell_id % 14
    u_y = int(cell_id / 28)
    i_y = int(cell_id / 14)
    y = 30 + 20 + i_y * 21
    x = 330 + 45 + i_x * 87
    if u_x / 14 >= 1:
        x += 43
    if u_y >= 1:
        y += 21
    return x, y


def click_on_cell(cell_id):
    x, y = cell_to_coords(cell_id)
    pyautogui.click(x=x, y=y)


def click_on_image(img):
    pos = pyautogui.locateCenterOnScreen(img, confidence=.8)
    pyautogui.click(pos)


def gather():
    global elements
    for e in elements:
        if e['elementState'] != 0:
            continue
        click_on_cell(e['elementCellId'])
        log.log('gathering')
        event.wait_for_first([
            messages.ObjectQuantityMessage,
            messages.ObjectAddedMessage
        ])
        log.log('finished gather')


def zaap(zone):
    pyautogui.press('h')
    event.wait_for(messages.MapComplementaryInformationsDataInHavenBagMessage)
    pyautogui.click(x=787, y=285)
    event.wait_for(messages.ZaapDestinationsMessage)
    time.sleep(1)
    pyautogui.click(x=1100, y=238)
    pyautogui.write(zone)
    pyautogui.press('enter')
    event.wait_for(messages.MapComplementaryInformationsDataMessage)


def nearest_zaap(pos):
    x, y = pos
    zaaps = data.get_zaap_list()
    distances = list(map(lambda _p: math.sqrt((x-_p[0])**2 + (y-_p[1])**2), zaaps))
    nearest_distance_index = distances.index(min(distances))
    return zaaps[nearest_distance_index]


def travel(pos):
    global map_pos
    _x, _y, zone = nearest_zaap(pos)
    x, y = pos
    zaap(zone)
    chat.general("/travel {},{}".format(x, y))
    time.sleep(.5)
    pyautogui.press('enter')
    while pos != map_pos:
        event.wait_for(messages.MapComplementaryInformationsDataMessage)

def update_map():
    go_to("right")
    go_to("left")


def press(key):
    pyautogui.press(key)


event.on(messages.MapComplementaryInformationsDataMessage, update_map_state)
