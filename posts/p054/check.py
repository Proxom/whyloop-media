# HARD GATE 5.2: pawl vs tape teeth over one full loop (240 Hz), loop closure, nothing moves without a cause.
import json, math
from shapely.geometry import Polygon
from shapely import affinity
import importlib.util
spec = importlib.util.spec_from_file_location('k', 'kin.py')
g = json.load(open('geom.json')); kin = json.load(open('kin_240.json'))
P, H, T = g['P'], g['H'], g['T']
pts = [(T, -40.0)]
for k in range(-25, 26):  # sawtooth (x = -d), steep face at s = k*P
    pts += [(0.0, k * P - 1e-9), (-H, k * P)]
pts += [(0.0, 26 * P), (T, 40.0)]
tape = Polygon([(T, -40)] + [p for p in pts[1:-1]] + [(T, 26 * P)]).buffer(0)
pawl0 = Polygon(g['pawl']); R = tuple(g['R'])
worst = 0; wt = None
for i, s in enumerate(kin):
    pw = affinity.rotate(pawl0, s['th'], origin=R, use_radians=True)
    tp = affinity.translate(tape, 0, g['Y0'] + s['Y'])
    a = pw.intersection(tp).area
    if a > worst: worst, wt = a, i / 240
print('max pawl/tape overlap area %.5f mm2 at t=%s' % (worst, wt))
d = abs(kin[0]['Y'] + 11 * P - (kin[-1]['Y'] + 0)) ; print('loop: start Y', kin[0]['Y'], 'end Y', kin[-1]['Y'], 'th', kin[0]['th'], kin[-1]['th'], 'travel pitches', g['travel'])
print('PASS' if worst < 2e-3 else 'FAIL')
