import json

f = open('../assets/data/map_id_pos.json', 'r')
f2 = open('../assets/data/map_id_pos.json', 'w')

data_json = json.loads(f.read())


new_data = {}
for elm in data_json:
    new_data[elm['id']] = {}
    new_data[elm['id']]['x'] = elm['x']
    new_data[elm['id']]['y'] = elm['y']
    new_data[elm['id']]['world'] = elm['world']

f2.write(json.dumps(new_data))
f2.close()
f.close()
