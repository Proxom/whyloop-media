import json, math, numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
from shapely.ops import unary_union
import kin
G = json.load(open('geom.json'))
SP = unary_union([Polygon(r['ext'], r['holes']) for r in G['SPACER']])
for ph in [-24, -22, -18, -14, -12, -10, -8, -6]:
    A = kin.arm_at(ph); print(ph, 'arm-spacer', round(A.distance(SP), 2), 'ovl', round(A.intersection(SP).area, 2), 'arm-pawl0', round(A.distance(kin.pawl_at(0)), 3))
print('bolt in vs pawl0', round(kin.bolt_poly(1).distance(kin.pawl_at(0)), 3), 'bolt out vs pawl(6.1)', round(kin.bolt_poly(0).distance(kin.pawl_at(6.1)), 3))
print('bolt vs spacer', [round(kin.bolt_poly(b).intersection(SP).area, 3) for b in (0, .5, 1)], 'pawl sweep vs spacer', round(kin.pawl_at(6.1).intersection(SP).area, 3))
