import json
import os
from latex2svg import latex2svg

f = open('./nodes/math.json')
data = json.load(f)

color_on = False


def node_color(node: dict):
    if not color_on:
        return "white"
    if "type" not in node:
        return "white"
    type = node["type"]
    if (type == "definition"):
        return "navyblue!20"
    if (type == "theorem"):
        return "yellow!20"
    if (type == "corollary"):
        return "yellow!10"
    return "white"


for node in data:
    if os.path.exists('nodes-svgs/' + node + '.svg'):
        x = 0
       # continue
    with open('nodes-svgs/' + node + '.svg', 'w') as f:
        print('rendering... ' + node)
        output = latex2svg(data[node]["tex"],
                           color=node_color(data[node]))
        f.writelines(output["svg"])
        data[node]["width"] = round(output["width"], 2)
        data[node]["height"] = round(output["height"], 2)

f.close()

g = open('./nodes/math.json', 'w')
json.dump(data, g)
g.close()
