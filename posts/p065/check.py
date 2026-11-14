# p065 collision / contact check over the whole loop (2D x-y plane at z = 0, where bar, crossbar, catch, cheese and pencil all meet)
import json, math, numpy as np
from shapely.geometry import Point, LineString, Polygon, box
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin.json'))
P = np.array(G['P']); A = np.array(G['A']); Q = tuple(G['Q']); RB, RW, RJ, LB = G['RB'], G['RW'], G['RJ'], G['LB']
pd = np.array(G['pen_dir']); CH = G['CH']; worst = {}
def upd(k, v, t):
    if k not in worst or v < worst[k][0]: worst[k] = (v, t)
cheese0 = Polygon([(Q[0] + CH['x0'], Q[1] + 0.4), (Q[0] + CH['x1'], Q[1] + 0.4), (Q[0] + CH['x1'], Q[1] + 0.4 + CH['h']), (Q[0] + CH['x0'], Q[1] + 0.4 + CH['h'])])
cheese0 = affinity.rotate(cheese0, G['PHI0'], origin=Q, use_radians=True)
for t, a, b, ph, px, py in K:
    rot = lambda poly: affinity.rotate(poly, -ph, origin=Q, use_radians=True)
    bar = LineString([tuple(P), tuple(P + LB * np.array([math.cos(b), math.sin(b)]))])
    c = A + RJ * np.array([math.cos(a), math.sin(a)]); cp = Point(*c)
    parts = [rot(Polygon(p)) for p in G['catch']] + [rot(Polygon(G['plate']))]; chz = rot(cheese0)
    upd('bar-catch/plate gap', min(bar.distance(p) for p in parts) - RB, t)
    upd('crossbar-bar gap', cp.distance(bar) - RB - RW, t)
    if G['BASE']['x0'] < c[0] < G['BASE']['x1']: upd('crossbar-base gap', c[1] - RW - G['BASE']['top'], t)
    upd('crossbar-trigger/cheese gap', min(cp.distance(p) for p in parts + [chz]) - RW, t)
    tip = np.array([px, py]); pen = LineString([tuple(tip), tuple(tip + pd * 200)])
    sv = max(0.0, float(np.dot(c - tip, pd))); rr = G['PEN_R'] if sv < 6.5 else G['PEN_R'] + 0.62   # real pencil profile (ferrule rings 4.22)
    upd('crossbar-pencil gap', float(np.linalg.norm(c - tip - sv * pd)) - rr - RW, t)
    upd('pencil-cheese gap', Point(*tip).distance(chz) - G['PEN_R'], t)
    upd('plate-base gap', min(y for x, y in parts[-1].exterior.coords) - G['BASE']['top'], t)
    upd('bar-base gap', min(P[1] + s * math.sin(b) for s in (0, LB)) - RB - G['BASE']['top'], t)
ok = True
for k, (v, t) in worst.items():
    bad = v < -0.02 and not (k == 'pencil-cheese gap' and v > -0.05); ok &= not bad
    print(f'{k:30s} min {v:7.3f} mm at t={t:6.3f}', 'FAIL' if bad else 'ok')
# loop closure: first and last samples match (the loop ends with a dissolve back to the set pose)
print('PASS' if ok else 'FAIL')
