import json
import pyautogui
import requests
from PIL import Image
from PIL import ImageChops
import cv2
import tinydb

poi_db = tinydb.TinyDB("assets/db/poi_dofus_hunt.json")
map_db = tinydb.TinyDB("assets/db/map_id_pos.json")

POI_ID_URL = lambda id: "https://i18napi.herokuapp.com/poi/{}".format(id)
MAP_POS_URL = lambda id: "https://i18napi.herokuapp.com/mapposition/{}".format(id)

ZAAP_SEARCH_IMG = 'assets/img/zaap_search.png'
ZAAP_IMG = 'assets/img/zaap.png'

MAP_ID_POS_FILE = 'assets/data/map_id_pos.json'
RESSOURCES_ID_FILE = 'assets/data/ressources_id.json'
CELL_ID_FILE = 'assets/data/cell_id.json'
POI_DATA = 'assets/data/poi.json'
ZAAP_LIST_FILE = 'assets/data/zaap.json'


poi_data = None
map_data = None
ressouces_data = None
cell_id = None
zaap_data = None


with open(MAP_ID_POS_FILE, 'r') as f:
    map_data = json.loads(f.read())
with open(RESSOURCES_ID_FILE, 'r') as f:
    ressouces_data = json.loads(f.read())
with open(CELL_ID_FILE, 'r') as f:
    cell_id = json.loads(f.read())
with open(POI_DATA, 'r') as f:
    poi_data = json.loads(f.read())
    poi_data = {v: k for k, v in poi_data.items()}
with open(ZAAP_LIST_FILE, 'r') as f:
    zaap_data = json.loads(f.read())


def get_map_pos(id):
    # found = map_db.search(tinydb.Query().id == id)
    # if len(found) > 0:
    #     return found[0]['x'], found[0]['y']
    # pos = map_data[str(id)]
    # map_db.insert({
    #     'id': id,
    #     'x': pos['x'],
    #     'y': pos['y']
    # })
    # return pos['x'], pos['y']
    # x = (id >> 9) & 511
    # y = id & 511
    # if (x & 0x0100) == 0x0100:
    #     x = - (x & 0xFF)
    # if (y & 0x0100) == 0x0100:
    #     y = -(y & 0xFF)
    # return x, y
    res = requests.get(MAP_POS_URL(id))
    res = res.json()
    return res['posX'], res['posY']


def get_map_world(id):
    return (id & 0x3FFC0000) >> 18


def get_ressouce_name(id):
    name = ressouces_data[str(id)]
    return name


def get_poi_name(id):
    poId = tinydb.Query()
    found = poi_db.search(poId.id == id)
    if len(found) > 0:
        return found[0]['label']
    res = requests.get(POI_ID_URL(id))
    res = res.json()
    poi_db.insert({
        'id': id,
        'label': res['label']
    })
    return res['label']


def get_poi_id(id):
    label = get_poi_name(id)
    return int(poi_data[label])


def get_cell_id_weight(id):
    cell = cell_id[str(id)]
    return float(cell['x']), float(cell['y'])

def get_zaap_search_zone():
    pos = pyautogui.locateCenterOnScreen(ZAAP_SEARCH_IMG, confidence=0.8)
    return pos

def get_zaap():
    pos = pyautogui.locateCenterOnScreen(ZAAP_IMG, region=(300, 20, 1260, 1000), confidence=0.8)
    return pos

def get_zaap_list():
    data = []
    print(zaap_data)
    for pos, zone in zaap_data.items():
        p = [int(x) for x in pos.split(",")]
        data.append((p[0], p[1], zone))
    return data