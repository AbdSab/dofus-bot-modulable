import json
import bot
import utils

trajects = {}


def load(name, path="traject.json"):
    global trajects
    traject_file = open(path, 'r')
    trajects[name] = json.loads(traject_file.read())
    traject_file.close()

def start(name):
    if name in trajects:
        run_tarject(name)

def run_tarject(name):
    global trajects
    traject = trajects[name]
    if bot.map_id is None:
        bot.update_map()
    while True:
        pos = utils.parse_pos(bot.map_pos)
        map = traject[pos]
        print(map)
        if isinstance(map, str):
            direction = map
        else:
            direction = map['direction']
            if 'gather' in map:
                bot.gather()
        bot.go_to(direction)

