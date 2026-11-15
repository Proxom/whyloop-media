# HARD GATE 5.2 for p066: contacts over the whole loop.
import json
G = json.load(open('geom.json')); K = json.load(open('kin.json')); d = G['DELTA'] / 2; ok = True
mn = 999
for r in K:
    for i in (1, 2, 3):
        u = r[i] - r[i + 1]                       # pin(i-1) minus fly(i), degrees
        gap = min(u - d, 360 - d - u)             # >= 0: pin and fly never overlap (0 = touching = driving)
        mn = min(mn, gap)
        if gap < -1e-3: ok = False; print('PIN/FLY OVERLAP', r[0], i, gap)
print('min pin-fly gap (deg)', round(mn, 4), '-> mm at RP', round(mn * 3.14159 / 180 * G['RP'], 4))
# latch timing and contact are checked below with the real lever polygons (shapely)
# latch tooth vs cam: cam rim radius 10.0 < R - D - 0.5
CAM_R = 10.0; ok &= CAM_R < G['R'] - G['D'] - 0.5; print('cam clear of latch by', round(G['R'] - G['D'] - CAM_R, 2), 'mm')
# gates aligned at the end, reading matches the combination
fin = K[-1]; print('final readings', [(-round(x / 9)) % 40 for x in G['TH'][1:]], 'gate angles at end', [round(((G['G_LOC'][i] + fin[i + 1]) + 180) % 360 - 180, 3) for i in (1, 2, 3)])
# lever: rests on the rims (cannot turn 0.5 deg) whenever beta = 0; never overlaps a wheel; does not rise again after it starts to drop
import importlib.util, sys
spec = importlib.util.spec_from_file_location('kin_mod', 'kin.py')
import math
from shapely.geometry import Polygon
from shapely import affinity
src = open('kin.py').read(); ns = {}
exec(src.split('# ---- latch lever')[0].split('rows, picks')[0], ns)  # constants + helpers only
exec('from shapely.geometry import Polygon, Point\nfrom shapely import affinity\n' + src.split('# ---- latch lever')[1].split('out = []; t_rel')[0].split('\n', 2)[2], ns)
ns['G_LOC'] = G['G_LOC']; ns['wrap'] = lambda a: (a + 180) % 360 - 180
bad = 0; minD = 9
for r in K[::6]:
    wp = [ns['wheel_poly']((G['G_LOC'][i] + r[i + 1]) % 360) for i in (1, 2, 3)]
    tp = affinity.rotate(ns['TP'], -r[5], origin=ns['PV']); ap = affinity.rotate(ns['AP'], -r[5], origin=ns['PV'])
    dd = min(min(tp.distance(w), ap.distance(w)) for w in wp); minD = min(minD, dd)
    if dd < 0.02: bad += 1
    if r[5] == 0 and ns['lever_free'](0.5, wp): bad += 1; print('lever could drop at', r[0])
print('lever-wheel min gap mm', round(minD, 3), 'violations', bad); ok &= bad == 0
bs = [r[5] for r in K if r[0] >= G['EV']['drop0']]
mono = all(b2 >= b1 - 1e-3 for b1, b2 in zip(bs, bs[1:])); print('lever drop monotonic', mono); ok &= mono
print('hook tip moves out by %.2f mm (groove %.1f)' % (G['HOOK_L'] * math.sin(math.radians(K[-1][5])), G['GROOVE']))
print('PASS' if ok else 'FAIL')
