# p103 prismatic day/night rear-view mirror: geometry, kinematics + HARD GATE 5.2 checks. 2D side view in the x-y plane (mm).
# World: +x = forward (toward the windshield), +y = up. The mirror faces the driver (-x). Diagram not to scale (eye + car behind moved close).
# Mirror local frame (group MIR, rotates by theta about the ball pivot P): silver back plane x = 0 (silver layer 0..1.5),
# glass front from (-GB, -H) bottom to (-GT, 0) top (thicker at the top), housing x 1.5..HX, y -H-2..2.
import json, math
FPS_K = 120
H, GB, GT, HX = 70.0, 8.0, 18.0, 24.0
ALPHA = math.degrees(math.atan((GT - GB) / H))           # wedge angle (exaggerated, real ones are a few degrees)
P = (34.0, -12.0)                                         # ball pivot (world), housing rotates about it
PL = (30.0, -16.0)                                        # pivot in mirror-local coords
MC_L = (0.0, -35.0)                                       # back-surface mid point (local)
EYE = (-300.0, -150.0); CAR = (-380.0, -38.0)             # driver's eye, headlights of the car behind (world)
ROOF_Y = 52.0; WS = [(46.0, ROOF_Y), (420.0, -170.0)]     # roof liner bottom, windshield line
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.2, flipA=0.55, flipB=0.9, cutIn=2.3, vo1=2.5, vo2=6.7, rayA=6.9, rayB=8.2, vo3=10.7, tabA=11.3, tabB=12.2,
         vo4=15.9, front=18.6, vo5=21.6, ans=21.4)
LOOP = 25.6
nxt = [T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5'], LOOP - 0.8]
for i, k in enumerate(['vo0', 'vo1', 'vo2', 'vo3', 'vo4', 'vo5']): assert T[k] + VO[i] < nxt[i], ('VO overlap', k, T[k] + VO[i], nxt[i])
def rot(v, a): c, s = math.cos(a), math.sin(a); return (c * v[0] - s * v[1], s * v[0] + c * v[1])
def to_world(pl, th):  # local -> world for mirror rotation th (rad): rotate about PL, place PL at P
    d = rot((pl[0] - PL[0], pl[1] - PL[1]), th); return (P[0] + d[0], P[1] + d[1])
def ang(v): return math.degrees(math.atan2(v[1], v[0])) % 360
def unit(v): L = math.hypot(*v); return (v[0] / L, v[1] / L)
# day: back normal bisects (to eye) and (to car) from the back mid point -> solve theta iteratively (mid point moves with theta)
th = 0.0
for _ in range(60):
    M = to_world(MC_L, th); ue = unit((EYE[0] - M[0], EYE[1] - M[1])); uc = unit((CAR[0] - M[0], CAR[1] - M[1]))
    n0 = unit((ue[0] + uc[0], ue[1] + uc[1])); th = math.radians(ang(n0) - 180.0)
TH_DAY = math.degrees(th); TH_NIGHT = TH_DAY - ALPHA
def refl(d, n): k = 2 * (d[0] * n[0] + d[1] * n[1]); return (d[0] - k * n[0], d[1] - k * n[1])
def views(thd):  # what the eye sees via the back (silver) and via the front (glass) surface: direction of the reversed eye ray
    t = math.radians(thd); M = to_world(MC_L, t); d = unit((M[0] - EYE[0], M[1] - EYE[1]))
    nb = rot((-1.0, 0.0), t); nf = rot(unit((-H, -(GT - GB))), t)
    return ang(refl(d, nb)), ang(refl(d, nf)), ang((CAR[0] - M[0], CAR[1] - M[1]))
vb_d, vf_d, car_d = views(TH_DAY); vb_n, vf_n, car_n = views(TH_NIGHT)
print(f'alpha {ALPHA:.2f} deg, theta day {TH_DAY:.2f}, night {TH_NIGHT:.2f}')
print(f'DAY  : eye sees via silver {vb_d:.1f} deg, via glass {vf_d:.1f} deg, car at {car_d:.1f}')
print(f'NIGHT: eye sees via silver {vb_n:.1f} deg, via glass {vf_n:.1f} deg, car at {car_n:.1f}')
assert abs(vb_d - car_d) < 0.3, 'day: silver must show the car'; assert abs(vf_n - car_n) < 2.0, 'night: glass must show the car'
assert 90 < vb_n < 180, 'night: silver must look up (roof)'; assert vf_d > 180, 'day: glass looks down (lap)'
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
TAB_DAY, TAB_NIGHT = -55.0, -125.0                       # tab angle (deg, local, about its hinge under the housing)
def state(t):
    if t < T['cutIn']: u = ease((t - T['flipA']) / (T['flipB'] - T['flipA']))
    elif t < T['front']: u = ease((t - T['tabA']) / (T['tabB'] - T['tabA']))
    else: u = 1.0
    return [TH_DAY + (TH_NIGHT - TH_DAY) * u, TAB_DAY + (TAB_NIGHT - TAB_DAY) * u, u]
# HARD GATE 5.2: housing corners stay under the roof and behind the windshield; tab stays below the housing; glass never crosses the stem
HOUS = [(-GT - 1, 2), (HX, 2), (HX, -H - 2), (-GB - 1, -H - 2)]; HINGE = (10.0, -H - 4); TABL = 20.0
def ws_side(p): (x0, y0), (x1, y1) = WS; return (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0)
rows = []; worst = 1e9
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; thd, tab, u = state(t); r = math.radians(thd)
    for c in HOUS:
        w = to_world(c, r); assert w[1] < ROOF_Y - 1, ('housing hits roof', t, w); assert ws_side(w) < 0, ('housing through windshield', t, w)
        worst = min(worst, ROOF_Y - w[1])
    for a in (math.radians(tab),):
        tip = (HINGE[0] + TABL * math.cos(a), HINGE[1] + TABL * math.sin(a)); assert tip[1] < -H - 2, ('tab inside housing', t)
    rows.append([round(t, 4), round(thd, 4), round(tab, 3), round(u, 4)])
# nothing moves without a cause: the mirror tilts only while the tab moves (same u)
json.dump(rows, open('kin.json', 'w'))
G = dict(FPS_K=FPS_K, LOOP=LOOP, T=T, H=H, GB=GB, GT=GT, HX=HX, ALPHA=ALPHA, P=P, PL=PL, MC_L=MC_L, EYE=EYE, CAR=CAR, ROOF_Y=ROOF_Y, WS=WS,
         TH_DAY=TH_DAY, TH_NIGHT=TH_NIGHT, HINGE=HINGE, TABL=TABL, views=dict(day=[vb_d, vf_d], night=[vb_n, vf_n]))
json.dump(G, open('geom.json', 'w'), indent=1)
print('kin PASS: roof clearance min %.1f mm; tab below housing; tilt only with the tab; rows %d' % (worst, len(rows)))
