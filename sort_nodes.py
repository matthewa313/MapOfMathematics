import json
from collections import OrderedDict

f = open('./nodes/math/linear-algebra.json')
data = json.load(f)

data = OrderedDict(sorted(data.items()))

g = open('./nodes/math/linear-algebra.json', 'w')
json.dump(data, g)

f.close()
g.close()
