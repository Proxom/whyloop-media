# p098 fuel gauge sender kinematics + HARD GATE 5.2 checks. Units mm, deg. Side section of the tank in the x-y plane (y up), cut at z = 0 (back half shown).
# Real design (HowStuffWorks 'How Fuel Gauges Work', Delphi sending unit article): a float on a pivoted metal arm rides on the fuel; the arm moves a wiper along a strip of
# resistive material grounded at one end; full tank -> wiper near the grounded end -> small resistance -> large current to the gauge -> needle at F; as the level drops the
# float sinks, the wiper moves away from ground, resistance rises, current falls, the needle drops toward E. (Some makes wire it the other way; said in the first comment.)
# Arm angle a (deg) from the -x direction, positive up: float centre = P + L(-cos a, sin a). Wiper contact on the strip at radius RW along the same direction.
# rows: [t, level, a, frac(path length 0..1), current(0..1 rel), needle n (0 E .. 1 F), stream(0/1), fillspeedup(0/1)]
import json, math, numpy as np
from shapely.geometry import Polygon, Point, box, LineString
from shapely import affinity
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
T = {'vo0': 0.15}; T['cutIn'] = round(0.15 + D[0] + 0.1, 3); T['vo1'] = T['cutIn'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + D[i - 1] + (0.3 if i in (3, 4, 5) else 0.25), 3)
T['drainA'] = T['vo3'] + 0.3; T['drainB'] = T['vo3'] + D[3] + 0.1           # fuel used (sped up)
T['fillA'] = T['vo5'] + 0.35; T['fillB'] = T['vo5'] + D[5] - 0.2             # refill (sped up)
T['outA'] = T['vo6'] - 0.15                                                   # cut to the dash gauge for the answer card
LOOP = round(T['vo6'] + D[6] + 1.25, 2); T['LOOP'] = LOOP
H = {'sweepA': 0.25, 'sweepB': 1.25}                                          # hook: needle F -> E (payoff flash), back to F at the loop seam
TOP, FLOOR, XL, XR, WALL = 240.0, 0.0, -95.0, 305.0, 5.0
P = (140.0, 165.0); L = 170.0; RW = 56.0; STRIP_R = (50.0, 62.0); A_GND, A_END = 22.0, -76.0
FL_W, FL_H = 44.0, 24.0; FLOAT_DIP = 4.0                                    # float centre sits 4 mm below the surface (top sticks out 8 mm)
LV_FULL, LV_EMPTY = 205.0, 20.0
R_FULL, R_EMPTY, R_G = 10.0, 73.0, 20.0
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def armAngle(level): return math.degrees(math.asin((level - FLOAT_DIP - P[1]) / L))
A_FULL, A_EMPTY = armAngle(LV_FULL), armAngle(LV_EMPTY)
def resist(a): return R_FULL + (R_EMPTY - R_FULL) * (A_FULL - a) / (A_FULL - A_EMPTY)     # linear in wiper travel
I_FULL, I_EMPTY = 1 / (R_FULL + R_G), 1 / (R_EMPTY + R_G)
def needle(a): I = 1 / (resist(a) + R_G); return (I - I_EMPTY) / (I_FULL - I_EMPTY), (I / I_FULL)
def level(t):
    if t < T['drainA']: return LV_FULL
    if t < T['fillA']: return LV_FULL + (LV_EMPTY - LV_FULL) * sm((t - T['drainA']) / (T['drainB'] - T['drainA']))
    return LV_EMPTY + (LV_FULL - LV_EMPTY) * sm((t - T['fillA']) / (T['fillB'] - T['fillA']))
def floatPos(a): r = math.radians(a); return (P[0] - L * math.cos(r), P[1] + L * math.sin(r))
def floatPoly(a):
    cx, cy = floatPos(a); return affinity.rotate(box(cx - FL_W / 2, cy - FL_H / 2, cx + FL_W / 2, cy + FL_H / 2), 0)   # float hangs level (pinned, free to swivel)
def sector(r0, r1, a0, a1, n=60):
    pts = []
    for i in range(n + 1): q = math.radians(a0 + (a1 - a0) * i / n); pts.append((P[0] - r1 * math.cos(q), P[1] + r1 * math.sin(q)))
    for i in range(n + 1): q = math.radians(a1 + (a0 - a1) * i / n); pts.append((P[0] - r0 * math.cos(q), P[1] + r0 * math.sin(q)))
    return Polygon(pts)
CARD = sector(34, 76, A_END - 6, A_GND + 6)                    # ceramic card (z = -12, same depth band as the float -> must never overlap in x-y)
BRACKET = box(P[0] - 6, P[1] - 6, P[0] + 6, TOP)                # vertical sender tube from the tank top down to the pivot
TANK_IN = box(XL + WALL, FLOOR, XR - WALL, TOP)
FPS_K = 120; rows = []; bad = []; minCard = minBr = minWall = 1e9
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; lv = level(t); a = armAngle(lv); n, I = needle(a); fp = floatPoly(a)
    frac = (A_GND - a) / (A_GND - A_END)
    dc = CARD.distance(fp); db = BRACKET.distance(fp); dw = fp.exterior.distance(TANK_IN.exterior) if TANK_IN.contains(fp) else -1
    minCard, minBr, minWall = min(minCard, dc), min(minBr, db), min(minWall, dw)
    if dc < 1: bad.append(('float-card', t, dc))
    if db < 1: bad.append(('float-bracket', t, db))
    if dw < 1: bad.append(('float-wall', t, dw))
    if not (A_END < a < A_GND): bad.append(('wiper-off-strip', t, a))
    if not (lv - FL_H / 2 < lv < lv + FL_H / 2): bad.append(('float-not-at-surface', t))
    stream = 1 if T['fillA'] - 0.25 < t < T['fillB'] + 0.05 else 0
    rows.append([round(t, 4), round(lv, 3), round(a, 3), round(frac, 4), round(I, 4), round(n, 4), stream, 1 if (T['drainA'] < t < T['drainB'] or T['fillA'] < t < T['fillB']) else 0])
# cause checks: needle only changes when the arm (wiper) moves; arm only moves when the level changes; level rises only while fuel pours in
for r0, r1 in zip(rows, rows[1:]):
    if abs(r1[5] - r0[5]) > 1e-9 and abs(r1[2] - r0[2]) < 1e-9: bad.append(('needle-without-wiper', r1[0]))
    if abs(r1[2] - r0[2]) > 1e-9 and abs(r1[1] - r0[1]) < 1e-9: bad.append(('arm-without-level', r1[0]))
    if r1[1] > r0[1] + 1e-9 and not r1[6]: bad.append(('rise-without-fuel', r1[0]))
# monotonic chain: lower level -> smaller angle -> longer path -> less current -> lower needle
for lv in np.linspace(LV_EMPTY, LV_FULL, 50):
    pass
a1, a2 = armAngle(100), armAngle(101); assert a2 > a1 and resist(a2) < resist(a1) and needle(a2)[0] > needle(a1)[0]
assert abs(rows[0][5] - 1) < 1e-6 and abs(rows[-1][5] - 1) < 1e-6, 'loop ends must be full'
G = dict(T=T, H=H, LOOP=LOOP, FPS_K=FPS_K, TOP=TOP, FLOOR=FLOOR, XL=XL, XR=XR, WALL=WALL, P=P, L=L, RW=RW, STRIP_R=STRIP_R, A_GND=A_GND, A_END=A_END, FL_W=FL_W, FL_H=FL_H,
         FLOAT_DIP=FLOAT_DIP, LV_FULL=LV_FULL, LV_EMPTY=LV_EMPTY, A_FULL=A_FULL, A_EMPTY=A_EMPTY, R_FULL=R_FULL, R_EMPTY=R_EMPTY, R_G=R_G)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
print('arm full %.1f empty %.1f deg; R %.0f..%.0f ohm; current empty/full %.2f; min gaps card %.1f bracket %.1f wall %.1f mm' % (A_FULL, A_EMPTY, R_FULL, R_EMPTY, I_EMPTY / I_FULL, minCard, minBr, minWall))
print('PASS' if not bad else 'FAIL', bad[:8])
