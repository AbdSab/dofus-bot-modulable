import json

cells = {}
file_data = None

with open("cellids.txt", 'r') as out:
    file_data = out.read().split('\n')

for line in file_data:
    cell = json.loads("{"+line+"}")
    for key in cell:
        if key not in cells:
            cells[key] = {}
        cells[key].update(cell[key])

with open('../assets/data/cell_id.json', 'w') as out:
    out.write(json.dumps(cells))