import bot
import map_utils
import pyautogui


def abs(x):
    return -x if x < 0 else x


def distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])


def get_walk_iterations(pm):
    cells = []
    for i in range(0, pm + 1):
        for j in range(-pm + i, pm + 1 - i):
            cells.append((i, j))
    for i in range(-pm, 0):
        for j in range(-pm - i, pm + 1 + i):
            cells.append((i, j))
    return cells


def get_walkable_coords(origin, pm):
    iterations = get_walk_iterations(pm)
    zones = list(map(lambda x: (x[0] + origin[0], x[1] + origin[1]), iterations))
    return zones


def get_walkable_cells(origin, pm):
    origin_coords = map_utils.cell_id_to_coord(origin)
    zones = get_walkable_coords(origin_coords, pm)
    zones = list(map(lambda x: map_utils.cell_coord_to_id(x), zones))
    zones = list(filter(lambda x: x != origin, zones))
    cells = []
    for cell in zones:
        x, y = bot.cell_to_coords(cell)
        color = pyautogui.pixel(x, y)
        if color == (87, 112, 24) or color == (93, 117, 30) or color == (85, 121, 56) or color == (90, 125, 62):
            cells.append(cell)
    return cells


def get_nearest_cell_entities(origin, entities, pm):
    zones = get_walkable_cells(origin, pm)
    zones_coord = list(map(lambda x: map_utils.cell_id_to_coord(x), zones))
    entities_coord = list(map(lambda x: map_utils.cell_id_to_coord(x), entities))
    distances = []
    print(zones)
    for zone in zones_coord:
        for entity in entities_coord:
            distances.append({
                'distance': distance(zone, entity),
                'entity': map_utils.cell_coord_to_id(entity),
                'zone': map_utils.cell_coord_to_id(zone)
            })
    nearest = min(distances, key=lambda x: x['distance'])
    return nearest['zone']


def get_cac_cells(origin):
    x,y = map_utils.cell_id_to_coord(origin)
    cac = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    cac_cells = list(map(lambda x: map_utils.cell_coord_to_id(x), cac))
    return cac_cells