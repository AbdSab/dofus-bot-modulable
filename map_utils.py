
MAP_WIDTH = 14
MAP_HEIGHT = 20
MAP_CELLS_COUNT = 560
CELL_WIDTH = 86
CELL_HALF_WIDTH = 43
CELL_HEIGHT = 43
CELL_HALF_HEIGHT = 21.5

CELLPOS = [0] * MAP_CELLS_COUNT

b = 0
a = 0
start_x = 0
start_y = 0
cell = 0

def init():
    global a, b, start_x, start_y, cell, CELLPOS, MAP_HEIGHT, MAP_WIDTH
    while a < MAP_HEIGHT:
        b = 0
        while b < MAP_WIDTH:
            CELLPOS[cell] = ((start_x + b), (start_y + b))
            cell += 1
            b += 1
        start_x += 1
        b = 0
        while b < MAP_WIDTH:
            CELLPOS[cell] = ((start_x + b), (start_y + b))
            cell += 1
            b += 1
        start_y -= 1
        a +=1
init()

def cell_id_to_coord(cell_id):
    return CELLPOS[cell_id]

def cell_coord_to_id(pos):
    x, y = pos
    return int((x - y) * MAP_WIDTH + y + (x - y) / 2)