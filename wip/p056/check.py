# HARD GATE 5.2: no part passes through another over one full loop (shapely, 240 Hz samples). Also writes pad polygons to geom.json.
import json, math, numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
A = np.array(G['A']); B = np.array(G['B']); h = G['BAR_H']; L = G['BAR_L']; BM = math.radians(G['BETA_MAX'])
def place(poly, ang, org):  # rotate local poly by ang (rad) about origin, then translate to org
    return affinity.translate(affinity.rotate(poly, ang, origin=(0, 0), use_radians=True), org[0], org[1])
bar_loc = Polygon([(-h, -L), (h, -L), (h, L), (-h, L)]).buffer(0)
on_pad_loc = Polygon([(-h - 0.03 - 2.2, -12.4), (-h - 0.03, -12.4), (-h - 0.03, -9.0), (-h - 0.03 - 2.2, -9.0)])
off_loc = Polygon([(-h - 0.03 - 2.2, 9.0), (-h - 0.03, 9.0), (-h - 0.03, 12.4), (-h - 0.03 - 2.2, 12.4)])
ON = place(on_pad_loc, -BM, B); OFF = place(off_loc, BM, B)
G['ON_PAD'] = [list(p) for p in ON.exterior.coords][:-1]; G['OFF_STOP'] = [list(p) for p in OFF.exterior.coords][:-1]
json.dump(G, open('geom.json', 'w'), indent=1)
P0, P1 = G['PLATE']; S = G['SLOT']
plate = [Polygon([(P0, S), (P1, S), (P1, 60), (P0, 60)]), Polygon([(P0, -60), (P1, -60), (P1, -S), (P0, -S)])]
W = G['LEVER_W']; HW = G['HOUSE_W']; BR = G['BORE_R']; PR = G['PL_R']; HE = G['HOUSE_END']; FL = G['FLOOR']; LP = G['LP']; r = G['R_TIP']
paddle_loc = Polygon([(0, -W), (24, -W), (24, W), (0, W)]).union(Point(24, 0).buffer(W, 32))
rails_loc = Polygon([(-HE, BR + 0.05), (-3, BR + 0.05), (-3, HW), (-HE, HW)]).union(Polygon([(-HE, -HW), (-3, -HW), (-3, -BR - 0.05), (-HE, -BR - 0.05)]))
floor_loc = Polygon([(-FL, -HW), (-2.0, -HW), (-2.0, HW), (-FL, HW)])
worst = {}
def rec(k, v, t):
    if v > worst.get(k, (0, 0))[0]: worst[k] = (v, t)
for i, k in enumerate(K):
    t = i / 240; ph = k['phi']; be = k['beta']; s = k['s']
    bar = place(bar_loc, be, B)
    pad = place(paddle_loc, ph, A); rails = place(rails_loc, ph, A); flo = place(floor_loc, ph, A)
    pl_body = place(Polygon([(-s + 0.02, -PR), (-(s - LP), -PR), (-(s - LP), PR), (-s + 0.02, PR)]), ph, A)
    tipc = A + s * -np.array([math.cos(ph), math.sin(ph)]); tip = Point(tipc).buffer(r, 64)
    rec('tip-bar', tip.intersection(bar).area, t); rec('plunger-bar', pl_body.intersection(bar).area, t)
    rec('bar-ON', bar.intersection(ON).area, t); rec('bar-OFF', bar.intersection(OFF).area, t)
    rec('rails-bar', rails.union(flo).intersection(bar).area, t)
    rec('paddle-plate', sum(pad.intersection(p).area for p in plate), t)
    rec('plunger-rails', pl_body.intersection(rails).area, t)
    rec('tip-gap', max(0, tip.distance(bar) - 0.0), t)
    if i % 240 == 0: pass
on_gap = min(place(bar_loc, k['beta'], B).distance(ON) for k in K if k['beta'] < -BM + 1e-6)
print(json.dumps({k: [round(v[0], 5), round(v[1], 3)] for k, v in worst.items()}))
print('bar-ON gap when ON: %.3f mm' % on_gap)
bad = [k for k, v in worst.items() if k != 'tip-gap' and v[0] > 0.01] + (['tip-gap'] if worst.get('tip-gap', (0,))[0] > 0.02 else [])
print('CHECK', 'FAIL ' + str(bad) if bad else 'PASS')
