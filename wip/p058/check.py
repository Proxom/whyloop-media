# HARD GATE 5.2: no part passes through another over one full loop (240 Hz). The pawl and the push rod share the plane of the fixed
# toothed sector plate (the lever's side plates straddle it, so they are in other planes). Pawl at its pawl angle, rod pinned to the pawl.
import json, math, numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
PLATE = Polygon(G['PLATE']).buffer(0); PAWL = Polygon(G['PAWL']).buffer(0); Q = G['Q']; RP = np.array(G['RP']); BTN = np.array(G['BTN']); ER = np.array(G['ER'])
worst = [0, 0, '']; mind = 9; rodmin = 9
for k in K:
    th, be = k['th'], k['beta']
    pw = affinity.rotate(affinity.rotate(PAWL, be, origin=tuple(Q), use_radians=True), th, origin=(0, 0), use_radians=True)
    rp = np.array(affinity.rotate(Point(*RP), be, origin=tuple(Q), use_radians=True).coords[0])
    rod = affinity.rotate(LineString([tuple(rp), tuple(rp + ER * 120)]).buffer(1.2), th, origin=(0, 0), use_radians=True)
    for nm, g in (('pawl', pw), ('rod', rod)):
        ov = g.intersection(PLATE).area
        if ov > worst[0]: worst = [ov, k['t'], nm]
    mind = min(mind, pw.distance(PLATE)); rodmin = min(rodmin, rod.distance(PLATE))
print('max overlap %.5f mm2 at %.3f s (%s); min pawl gap %.4f mm; min rod gap %.3f mm' % (worst[0], worst[1], worst[2], mind, rodmin))
print('CHECK', 'PASS' if worst[0] < 0.01 and mind > 0.01 else 'FAIL')
