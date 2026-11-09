# head geometry (2D x-y): outer block minus (slot + pawl pocket swept over the pawl's motion range). Writes into geom.json.
import json, math
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity
g = json.load(open('geom.json')); P, H, T = g['P'], g['H'], g['T']; R = tuple(g['R'])
pawl0 = Polygon(g['pawl'])
sw = unary_union([affinity.rotate(pawl0, g['thMin'] - 0.03 + i * (g['thMax'] - g['thMin'] + 0.08) / 40, origin=R, use_radians=True) for i in range(41)])
X0, X1, YB, YT = -4.0, 2.8, -3.2, 2.6
pocket = sw.buffer(0.14).intersection(box(-10, R[1] + 0.35, 10, 10))
slot = box(-H - 0.13, YB - 1, T + 0.1, YT + 1)
head = box(X0, YB, X1, YT).difference(unary_union([pocket, slot])).buffer(0)
parts = list(head.geoms) if head.geom_type == 'MultiPolygon' else [head]
g['head'] = [[list(map(float, c)) for c in list(p.simplify(0.004).exterior.coords)[:-1]] for p in parts]
g['headBox'] = [X0, YB, X1, YT]
# the pawl as attached in the wall: clip its base to the wall so nothing sticks out of the head
g['pawlVis'] = [list(map(float, c)) for c in list(pawl0.intersection(box(X0 + 0.1, YB + 0.1, X1, YT)).exterior.coords)[:-1]]
json.dump(g, open('geom.json', 'w'), indent=1)
print(len(parts), 'head parts', [len(p) for p in g['head']], 'pocket area %.2f' % pocket.area)
