# p101 clipless (SPD-style) pedal kinematics + HARD GATE 5.2 checks. Units mm, deg.
# Side view: x = toe direction, y up, pedal body top y = 0, pedal axle along z. Bike/crank at -z, "outward" = +z.
# Cleat (local): plate x -17.8..17.8 (front end rounded in plan, R 15 about x 2.8), y 0..3, z -15..15; boss + sole above.
# Pose: Q = world position of the plate's front-top corner (local (17.8, 3)); phi = tilt about z through Q (negative = heel up);
# theta = heel-out twist about the vertical axis through local (2.8, 0) (plan view); psi = rear jaw angle about its pin (+ = open, top moves -x).
# Real design: the front of the cleat hooks under the front jaw first, pushing the heel down cams the spring-loaded rear jaw open
# until it snaps over the cleat; pulling up cannot free it; twisting the heel outward cams the rear jaw open and the cleat lifts out.
# rows: [t, Qx, Qy, phi, theta, psi, slowmo]
import json, math, numpy as np
from shapely.geometry import Polygon
from shapely import affinity
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
T = {'vo0': 0.15, 'cutIn': 2.2}
T['vo1'] = 2.3; T['vo2'] = round(T['vo1'] + D[1] + 0.2, 3); T['vo3'] = round(T['vo2'] + D[2] + 0.2, 3)
T['vo4'] = round(T['vo3'] + D[3] + 0.2, 3); T['vo5'] = round(T['vo4'] + D[4] + 0.2, 3); T['vo6'] = round(T['vo5'] + D[5] + 0.25, 3)
LOOP = round(T['vo6'] + D[6] + 1.7, 2); T['LOOP'] = LOOP
PHI0 = -14.0; LIFT = (8.0, 16.0); HOOKQ = (13.0, 3.05); SEAT = (17.8, 3.0)
PIN = (-24.0, -6.0)
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
lerp = lambda a, b, u: a + (b - a) * u
def approach(u):   # lifted -> above the body -> slide under the front lip (3 parts)
    if u < 0.4: v = sm(u / 0.4); return lerp(LIFT[0], HOOKQ[0], v), lerp(LIFT[1], HOOKQ[1], v)
    v = sm((u - 0.4) / 0.6); return lerp(HOOKQ[0], SEAT[0], v), lerp(HOOKQ[1], SEAT[1], v)
# twist pivot plan geometry
T['twA'] = T['vo5'] + 1.6; T['twB'] = T['twA'] + 2.4          # twist 0 -> TH1 (slow)
T['liftA'] = T['twB'] + 0.15; T['liftB'] = T['liftA'] + 0.9   # cleat lifts out
TH1 = 16.0
def base(t):
    """pose without the jaw: Qx, Qy, phi, theta, slow"""
    if t < T['cutIn']:                                   # hook: real-speed click-in at 0.10-0.75 s, then hold
        if t < 0.45: x, y = approach(sm((t - 0.05) / 0.4)); return x, y, PHI0, 0, 0
        return SEAT[0], SEAT[1], PHI0 * (1 - sm((t - 0.45) / 0.3)), 0, 0
    if t < T['vo2']:                                     # step 1: slow approach + hook under the front jaw
        u = (t - T['cutIn']) / (T['vo2'] - 0.3 - T['cutIn']); x, y = approach(min(1, u)); return x, y, PHI0, 0, 0
    if t < T['vo4']:                                     # steps 2-3: heel down (slow), the snap happens on its own
        a, b = T['vo2'] + 0.5, T['vo3'] + 0.9; u = (t - a) / (b - a)
        return SEAT[0], SEAT[1], PHI0 * (1 - sm(u)), 0, 1 if T['vo2'] < t < T['vo3'] + 1.4 else 0
    if t < T['vo5']:                                     # step 4: pull up -> held (lifts only the 0.15 mm clearance)
        u = sm((t - T['vo4'] - 0.6) / 0.25) * (1 - sm((t - T['vo5'] + 0.5) / 0.25)); return SEAT[0], SEAT[1] + 0.15 * u, 0, 0, 0
    if t < T['liftA']:                                   # step 5: twist the heel out
        return SEAT[0], SEAT[1], 0, TH1 * sm((t - T['twA']) / (T['twB'] - T['twA'])), 1 if t > T['twA'] - 0.2 else 0
    if t < T['vo6'] + D[6] + 0.3:                        # lift out
        u = sm((t - T['liftA']) / (T['liftB'] - T['liftA'])); return SEAT[0] + (LIFT[0] - SEAT[0]) * 0.3 * u, SEAT[1] + (LIFT[1] - SEAT[1]) * u, 0, TH1, 0
    u = sm((t - (T['vo6'] + D[6] + 0.3)) / 1.2)          # back to the loop start in the air
    return lerp(SEAT[0] + (LIFT[0] - SEAT[0]) * 0.3, LIFT[0], u), LIFT[1], PHI0 * u, TH1 * (1 - u), 0
# ---- side-view polygons ----
def plate(Qx, Qy, phi):
    P = Polygon([(-17.8, 0.9), (-16.9, 0), (16.9, 0), (17.8, 0.9), (17.8, 3), (-17.8, 3)])
    P = affinity.translate(P, -17.8, -3); P = affinity.rotate(P, phi, origin=(0, 0)); return affinity.translate(P, Qx, Qy)
BOSS = [(-11, 3), (11, 3), (11, 9), (-11, 9)]
def boss(Qx, Qy, phi):
    P = affinity.translate(Polygon(BOSS), -17.8, -3); P = affinity.rotate(P, phi, origin=(0, 0)); return affinity.translate(P, Qx, Qy)
FRONT = Polygon([(18.3, 0), (27, 0), (27, 7), (19.5, 7), (15.8, 4.2), (18.3, 3.2)])
REAR0 = Polygon([(-18.3, 0), (-21, 0), (-21, -3), (-27, -3), (-27, 8), (-19.5, 8), (-15.8, 5.0), (-15.8, 3.7), (-16.3, 3.2), (-18.3, 3.2)])
def rear(psi): return affinity.rotate(REAR0, psi, origin=PIN)
def needed_psi(pl):
    if not rear(0).intersects(pl) or rear(0).intersection(pl).area < 1e-6: return 0.0
    lo, hi = 0.0, 40.0
    for _ in range(40):
        m = (lo + hi) / 2
        if rear(m).intersection(pl).area > 1e-7: lo = m
        else: hi = m
    return hi + 0.05
OVER = 2.5; RPIV = 20.6; HALFW = 15.0; R_LIP = 10.0      # lip overhang, plan geometry, lip height above the pin
def twist_d(th):                                         # plan view: how far the rear-most corner pushes the jaw face back
    a = math.radians(th); return max(0.0, RPIV * math.cos(a) + HALFW * math.sin(a) - 21.1 + 0.05)
FPS_K = 120; rows = []; bad = []; psi = 0.0; RATE = 260.0   # spring closes the jaw at <= 260 deg/s (snap)
seenOpen = False; minFront = 1e9; minRear = 1e9; snapT = None; relT = None
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; Qx, Qy, phi, th, slow = base(t)
    if th > 0.01:                                        # plan-view cam (twist) and the lift-out
        need = math.degrees(twist_d(th) / R_LIP)
        if Qy > SEAT[1] + 0.05:                          # lifting: lip must be clear (released) until the plate is above the lip top
            if Qy - SEAT[1] < 5.5: need = max(need, math.degrees(OVER / R_LIP) + 0.5)
            if relT is None: relT = t
            if Qy - SEAT[1] < 5.5 and twist_d(th) < OVER: bad.append(('lift-before-release', round(t, 3), round(twist_d(th), 2)))
    else:
        pl = plate(Qx, Qy, phi); need = needed_psi(pl)
        f = FRONT.intersection(pl).area; minFront = min(minFront, FRONT.distance(pl))
        if f > 1e-6: bad.append(('front-overlap', round(t, 3), round(f, 4)))
        if boss(Qx, Qy, phi).intersects(FRONT) or boss(Qx, Qy, phi).intersects(rear(need)): bad.append(('boss', round(t, 3)))
        if pl.bounds[1] < -1e-6: bad.append(('below-body', round(t, 3)))
    prev = psi; psi = max(need, psi - RATE / FPS_K) if t >= T['cutIn'] or t > 0.3 else need
    if t < T['cutIn']: psi = max(need, prev - 900 / FPS_K)          # hook: real speed
    if th < 0.01:
        ov = rear(psi).intersection(plate(Qx, Qy, phi)).area
        if ov > 1e-6: bad.append(('rear-overlap', round(t, 3), round(ov, 4)))
        minRear = min(minRear, rear(psi).distance(plate(Qx, Qy, phi)))
    if psi > prev + 1e-9 and need <= prev + 1e-9: bad.append(('opens-without-cause', round(t, 3)))
    if t > T['vo2'] and psi > 3: seenOpen = True
    if snapT is None and t > T['vo2'] and seenOpen and psi < 0.5: snapT = t
    rows.append([round(t, 4), round(Qx, 3), round(Qy, 3), round(phi, 3), round(th, 3), round(psi, 3), slow])
# locked: while flat and seated, the lip covers the plate end (pull-up cannot free it)
for r in rows:
    if T['vo4'] < r[0] < T['vo5'] and (r[5] > 0.5 or r[2] > SEAT[1] + 0.2): bad.append(('not-locked', r[0]))
assert abs(rows[0][1] - rows[-1][1]) < 0.05 and abs(rows[0][2] - rows[-1][2]) < 0.05 and abs(rows[0][3] - rows[-1][3]) < 0.1 and rows[-1][4] < 0.1 and rows[-1][5] < 0.1, 'loop ends'
T['snap'] = snapT; T['release'] = relT
G = dict(T=T, LOOP=LOOP, FPS_K=FPS_K, PIN=PIN, SEAT=SEAT, PHI0=PHI0, TH1=TH1, OVER=OVER, R_LIP=R_LIP)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('LOOP', LOOP, {k: (round(v, 2) if v else v) for k, v in T.items()})
print('min gap front %.2f rear %.2f; max psi %.1f; release twist at d>=%.1f: theta %.1f deg' % (minFront, minRear, max(r[5] for r in rows), OVER, next(th for th in np.arange(0, 30, 0.1) if twist_d(th) >= OVER)))
print('PASS' if not bad else 'FAIL', bad[:10], len(bad))
