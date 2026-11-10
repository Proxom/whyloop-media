# HARD GATE 5.2: no part passes through another over one full loop (shapely, 240 Hz), in the BODY frame.
# Nub+finger+arm contour (same construction as scene.html armContour) vs the 12-tooth gear; also gear vs the other arm.
import json, math
from shapely.geometry import Polygon
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
GEAR = Polygon(G['GEAR']).buffer(0); RA, AW, RHO, RC0, AT, SP = G['RA'], G['AW'], G['RHO'], G['RC0'], G['A_TIP'], G['ARM_SPAN']
A0 = AT - SP; SPW = 3.2 / RA; ROFF = 27.3; BOFF = AT - G['PSI_C']
pol = lambda r, a: (r * math.cos(a), r * math.sin(a))
def contour(d):
    rc = RC0 + d; aE = AT + RHO / RA; aI = AT - RHO / RA
    off = lambda a: d * (3 * min(1, max(0, (a - A0) / SP)) ** 2 - min(1, max(0, (a - A0) / SP)) ** 3) / 2
    p = [pol(ROFF, A0 - SPW), pol(ROFF, A0)] + [pol(RA + AW + off(A0 + (aE - A0) * i / 40), A0 + (aE - A0) * i / 40) for i in range(41)]
    c, s = math.cos(AT), math.sin(AT); loc = lambda x, y: (c * x - s * y, s * x + c * y)
    p += [loc(rc, RHO)] + [loc(rc + RHO * math.cos(math.pi / 2 + math.pi * i / 24), RHO * math.sin(math.pi / 2 + math.pi * i / 24)) for i in range(1, 24)] + [loc(rc, -RHO)]
    p += [pol(RA - AW + off(aI + (A0 - aI) * i / 40), aI + (A0 - aI) * i / 40) for i in range(41)] + [pol(RA - AW, A0 - SPW)]
    return Polygon(p).buffer(0)
worst = [0, 0]; mind = 9
for i, k in enumerate(K):
    rel = k['h'] - (k['b'] + BOFF)  # handle angle in body frame
    arm = contour(k['d'])
    for j in (0, 1):
        a = affinity.rotate(arm, rel + j * math.pi, origin=(0, 0), use_radians=True)
        ov = a.intersection(GEAR).area; dd = a.distance(GEAR); mind = min(mind, dd)
        if ov > worst[0]: worst = [ov, i / 240]
    if max(abs(x) for x in []) if False else False: pass
print('max overlap %.5f mm2 at %.3f s; min gap %.4f mm' % (worst[0], worst[1], mind))
print('max arm outer radius %.2f mm (skirt inner 27.0)' % (RA + AW + max(k['d'] for k in K)))
print('CHECK', 'PASS' if worst[0] < 0.01 else 'FAIL')
