# p095 flip key kinematics + HARD GATE 5.2 checks. Units mm, deg. Top view (x, z), pivot axis = y.
# Real design (US 7,370,501 / US 8,978,429): a torsion spring around the pivot urges the blade from folded (theta 180) to open (theta 0);
# the push button (coaxial, pushed up by a coil spring) has two legs that sit in the swivel AND in two notches of the case collar -> blade locked;
# pressing the button drops the legs out of the case notches -> swivel free -> the torsion spring snaps the blade out until it rests on the case nose;
# then the button spring pushes the legs back into the notches (2 notches 180 deg apart serve both positions) -> locked open.
# rows: [t, theta, b(press mm), wind(deg), slowmo(0/1)]
import json, math, numpy as np
from shapely.geometry import Polygon, Point, box
from shapely.ops import unary_union
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
T = {'vo0': 0.15}
T['cutIn'] = 1.6; T['vo1'] = 1.7; T['vo2'] = round(T['vo1'] + D[1] + 0.25, 3); T['vo3'] = round(T['vo2'] + D[2] + 0.25, 3)
T['vo4'] = round(T['vo3'] + D[3] + 0.3, 3); T['vo5'] = round(T['vo4'] + D[4] + 0.25, 3); T['vo6'] = round(T['vo5'] + D[5] + 0.35, 3)
T['press'] = T['vo3'] + 0.55                       # button goes down (step 3)
T['snapA'] = T['vo4'] + 0.75; T['snapB'] = T['snapA'] + 1.3   # slow motion snap (real ~0.15 s)
T['pop'] = T['vo5'] + 0.6                          # button pops back up (step 5)
T['outA'] = T['vo6'] - 0.05                        # cut to outside for the fold-back
T['foldP'] = T['vo6'] + 0.25; T['foldA'] = T['vo6'] + 0.45; T['foldB'] = T['vo6'] + 2.1; T['foldPop'] = T['foldB'] + 0.06
LOOP = round(T['vo6'] + 2.1 + 0.06 + 0.15 + 2.75, 2); T['LOOP'] = LOOP
H = {'pressA': 0.15, 'snapA': 0.30, 'snapB': 0.52, 'pop': 0.56}   # hook (real speed payoff)
B_DN = 3.4; WIND0 = 60.0
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def snap(u): u = min(1, max(0, u)); return 180 * (1 - math.sin(math.pi / 2 * u))          # accelerates until the stop
def bounce(dt, dur): return 0 if dt < 0 or dt > dur else 3.0 * math.sin(math.pi * dt / dur)
def state(t):
    if t < T['cutIn']:                                   # hook: press, fast snap, pop
        b = B_DN * sm((t - H['pressA']) / 0.08) * (1 - sm((t - H['pop']) / 0.06))
        th = 180 if t < H['snapA'] else (snap((t - H['snapA']) / (H['snapB'] - H['snapA'])) + bounce(t - H['snapB'], 0.04))
        return th, b, 0
    if t < T['outA']:
        b = B_DN * sm((t - T['press']) / 0.35) * (1 - sm((t - T['pop']) / 0.25))
        if t < T['snapA']: th = 180
        else: th = snap((t - T['snapA']) / (T['snapB'] - T['snapA'])) + bounce(t - T['snapB'], 0.3)
        return th, b, 1 if T['snapA'] - 0.3 < t < T['snapB'] + 0.5 else 0
    b = B_DN * sm((t - T['foldP']) / 0.15) * (1 - sm((t - T['foldPop']) / 0.06))
    th = 0 if t < T['foldA'] else 180 * sm((t - T['foldA']) / (T['foldB'] - T['foldA']))
    return th, b, 0
# ---- geometry (top view) ----
PIV = (0.0, 12.0); R_HEAD = 13.0; BL_R0 = 13.5; BL_R1 = 66.0; BL_W = 9.0
BODY = unary_union([box(-78, -17, 18, 7), Point(PIV).buffer(R_HEAD, 64)])
def blade(th):
    a = math.radians(th); d = np.array([math.cos(a), math.sin(a)]); n = np.array([-d[1], d[0]]); p = np.array(PIV); h = BL_W / 2
    pts = [p + d * BL_R0 + n * h, p + d * (BL_R1 - 6) + n * h, p + d * BL_R1 + n * 1.5, p + d * BL_R1 - n * 1.5, p + d * (BL_R1 - 6) - n * h, p + d * BL_R0 - n * h]
    return Polygon(pts)
# button legs vs case collar (y up): legs y in [1-b, 7-b], collar y in [4, 7]; engaged if top > 4
LEG_W, NOTCH_W, LEG_R = 3.0, 3.4, 10.0
TOL = math.degrees(math.atan(((NOTCH_W - LEG_W) / 2) / LEG_R))
FPS_K = 120; rows = []; minGap = 1e9; bad = []
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; th, b, slow = state(t); g = BODY.distance(blade(th)); minGap = min(minGap, g)
    if g < 0.3: bad.append(('blade-body', round(t, 3), round(g, 3)))
    mis = abs(((th + 90) % 180) - 90)
    if 7 - b > 4.0 and mis > TOL: bad.append(('leg-collar', round(t, 3), round(mis, 2), round(b, 2)))
    if th < -1e-6 or th > 180 + 1e-6: bad.append(('range', t, th))
    rows.append([round(t, 4), round(th, 3), round(b, 3), round(WIND0 + th, 2), slow])
# cause checks: blade only turns while the legs are out of the notches (b >= 3.0) or exactly aligned
for r0, r1 in zip(rows, rows[1:]):
    if abs(r1[1] - r0[1]) > 1e-6 and r1[2] < 3.0 and abs(r1[0] - T['cutIn']) > 0.01: bad.append(('turn-while-locked', r1[0], r1[2]))
    if r1[1] < r0[1] - 1e-6 and r1[2] < 3.0: bad.append(('open-without-press', r1[0]))
assert rows[0][1] == 180 and abs(rows[-1][1] - 180) < 1e-6 and rows[0][2] < 0.01 and rows[-1][2] < 0.01, 'loop ends must match (folded, button up)'
G = dict(T=T, LOOP=LOOP, FPS_K=FPS_K, PIV=PIV, R_HEAD=R_HEAD, BL_R0=BL_R0, BL_R1=BL_R1, BL_W=BL_W, B_DN=B_DN, LEG_W=LEG_W, NOTCH_W=NOTCH_W, LEG_R=LEG_R, H=H)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('LOOP', LOOP, 'T', {k: round(v, 2) for k, v in T.items()}); print('min blade-body gap %.2f mm, leg tol %.2f deg' % (minGap, TOL))
print('PASS' if not bad else 'FAIL', bad[:8])
