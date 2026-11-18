# HARD GATE 5.2: no part passes through another. The cam lugs, the barrel ridges and the plunger teeth all work on the same cylinder,
# so the check runs in the unrolled plane (arc length at r = 3.6 mm, height mm) for every 1/60 s row, all 4 lugs.
import json, math
from shapely.geometry import Polygon
from shapely.ops import unary_union
G = json.load(open('geom.json')); K = json.load(open('kin.json'))
T, H, C, W, LH, S, Y0, GT, TOP = (G[k] for k in ['T', 'H', 'C', 'W_LUG', 'LH', 'S', 'Y0', 'GT', 'TOP'])
KM = math.pi * 3.6 / 180
def P_(pts): return Polygon([(u * KM, y) for u, y in pts])
cells = []
for i in range(-6, 14):
    a = i * T
    if i % 2 == 0: cells.append(P_([(a, Y0), (a + T, Y0 + H), (a + T, TOP), (a, TOP)]))
    else:
        ug = a + T - W - C
        cells.append(P_([(a, Y0), (ug, Y0 + S * (ug - a)), (ug, GT), (a + T, GT), (a + T, TOP), (a, TOP)]))
ridges = unary_union(cells)
def plunger(P):
    return unary_union([P_([(b, P), (b + T, P + H), (b + T, P + 14), (b, P + 14)]) for b in [T / 2 + j * T for j in range(-7, 14)]])
def lugs(ur, y): return [P_([(ur + k * 90, y), (ur + k * 90 - W, y - S * W), (ur + k * 90 - W, y - LH), (ur + k * 90, y - LH)]) for k in range(4)]
fails = 0; worst = {'lug-ridge': 9, 'lug-plunger': 9}; touch = 0
for t, P, ur, y, st in K:
    pl = plunger(P)
    for L in lugs(ur, y):
        for nm, other in (('lug-ridge', ridges), ('lug-plunger', pl)):
            a = L.intersection(other).area; d = L.distance(other); worst[nm] = min(worst[nm], d)
            if a > 1e-6: fails += 1; print('overlap', nm, t, round(a, 6))
    # the lug must be held (touching a ridge or the plunger) unless it is moving
    L0 = lugs(ur, y)[0]
    if st in (0, 1) and min(L0.distance(ridges), L0.distance(pl)) > 1e-3: touch += 1
print({k: round(v, 4) for k, v in worst.items()}, 'rest rows not touching:', touch)
print('FAIL' if fails or touch else 'PASS', fails)
