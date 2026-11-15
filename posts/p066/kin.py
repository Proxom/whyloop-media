# p066 combination lock kinematics (Wikipedia "Rotary combination lock" design: dial spindle -> drive cam with a drive pin;
# each wheel has a fly on its front face and a drive pin on its back face; gates (notches) under a fence/latch).
# Angles in degrees, measured CLOCKWISE seen from the front ("turn right" = +). Element 0 = cam (on the dial), 1 = front wheel
# (closest to the cam), 2 = middle, 3 = back wheel (furthest). Pin of element i-1 and fly of element i sit at the same base angle,
# so their relative angle u = phi[i-1] - phi[i] can only move inside [DELTA/2, 360 - DELTA/2] (pin + fly widths = DELTA).
import json, math
FPS_K = 120
R, D = 13.0, 2.2          # wheel radius, gate depth (mm)
RP = 9.5                  # pin / fly radius
PIN_W, FLY_W = 1.6, 2.0   # pin diameter, fly width (mm) -> DELTA
DELTA = math.degrees((PIN_W + FLY_W) / RP)
GATE_W, TOOTH_W, CHAMF = 17.0, 9.0, 7.0   # gate opening, latch tooth and chamfer widths (degrees at the rim)
NUM = 40; DEG_PER = 360 / NUM
COMBO = [15, 35, 5]
TH = [0, 1305, 405, 1035]  # right 3 turns + to 15; left 2 turns past 35 to 35; right 1 turn past 5 to 5 (numbers run clockwise on the face, so turning right counts DOWN: reading = -theta/9 mod 40)
for a, n in zip(TH[1:], COMBO): assert (-round(a / DEG_PER)) % NUM == n
# dial motion: (t0, t1, theta0, theta1, accel, decel)
SEGS = [(10.9, 21.0, TH[0], TH[1], 0.8, 1.2), (25.2, 32.0, TH[1], TH[2], 0.7, 1.1), (35.0, 39.6, TH[2], TH[3], 0.6, 2.4)]
def trap(t, t0, t1, a0, a1, ta, td):
    if t <= t0: return a0
    if t >= t1: return a1
    T = t1 - t0; vmax = 1.0 / (T - ta / 2 - td / 2); s = t - t0  # normalised distance 1
    if s < ta: x = 0.5 * vmax / ta * s * s
    elif s < T - td: x = 0.5 * vmax * ta + vmax * (s - ta)
    else: r = T - s; x = 1 - 0.5 * vmax / td * r * r
    return a0 + (a1 - a0) * x
def theta(t):
    for (t0, t1, a0, a1, ta, td) in SEGS:
        if t < t0: return a0
        if t <= t1: return trap(t, t0, t1, a0, a1, ta, td)
    return SEGS[-1][3]
LOOP, DIS0 = 48.8, 47.3
POP0, POP1, POP_H = 39.62, 40.05, 9.0
U0 = [None, 360 - DELTA / 2 - 205, DELTA / 2 + 1.5, DELTA / 2 + 1.5]   # starting play (as if last turned left)
phi = [0.0, -U0[1], -U0[1] - U0[2], -U0[1] - U0[2] - U0[3]]
rows, picks, last_drive = [], [], [None] * 4
N = int(round(DIS0 * FPS_K))
for k in range(N + 1):
    t = k / FPS_K; phi[0] = theta(t)
    for i in (1, 2, 3):
        lo, hi = phi[i - 1] - (360 - DELTA / 2), phi[i - 1] - DELTA / 2
        new = min(max(phi[i], lo), hi); moving = abs(new - phi[i]) > 1e-9
        if moving and not last_drive[i]: picks.append({'t': round(t, 3), 'wheel': i, 'dir': 'R' if new > phi[i] else 'L'})
        last_drive[i] = moving; phi[i] = new
    rows.append([t] + phi[:])
# gates: set so that every gate sits at the top (0 deg) at the end -> local gate angle g_i = -phi_i(end)
fin = rows[-1]; G_LOC = [None] + [(-fin[i + 1]) % 360 for i in (1, 2, 3)]  # row = [t, cam, w1, w2, w3]
def wrap(a): return (a + 180) % 360 - 180
def support(i, ph):  # radius under the latch tooth that wheel i offers
    a = abs(wrap(G_LOC[i] + ph)); free = (GATE_W - TOOTH_W) / 2
    if a <= free: return R - D
    if a >= free + CHAMF: return R
    return R - D + D * (a - free) / CHAMF
# ---- latch lever (bell crank): pivot PV; tooth hangs from the horizontal arm onto the wheel rims; the vertical arm's tip sits in a
# groove on the inner side of the shackle's left leg. A spring turns the lever clockwise (beta > 0 = clockwise, tooth down).
from shapely.geometry import Polygon, Point
from shapely import affinity
PV = (-7.0, 15.0); TOOTH = [(-1.02, 13.03), (1.02, 13.03), (1.02, 15.6), (-1.02, 15.6)]
ARM = [(-7.6, 15.0), (1.02, 15.0), (1.02, 16.6), (-7.6, 16.6)]
def wheel_poly(g_cw):  # rim with a chamfered gate centred at clockwise angle g_cw from the top
    pts = []; n = 720
    free = (GATE_W - TOOTH_W) / 2 + TOOTH_W / 2  # half opening at the bottom, degrees
    for k in range(n):
        a = k * 360 / n; d = abs(wrap(a - g_cw)); half_b = GATE_W / 2; half_t = half_b + CHAMF
        rr = R - D if d <= half_b else (R if d >= half_t else R - D + D * (d - half_b) / CHAMF)
        th = math.radians(90 - a); pts.append((rr * math.cos(th), rr * math.sin(th)))
    return Polygon(pts)
TP, AP = Polygon(TOOTH), Polygon(ARM)
def lever_free(beta, wp):
    tp = affinity.rotate(TP, -beta, origin=PV, use_radians=False); ap = affinity.rotate(AP, -beta, origin=PV, use_radians=False)
    return all(tp.distance(w) >= 0.03 and ap.distance(w) >= 0.03 for w in wp)
BMAX = 22.0; HOOK_L = 7.8; GROOVE = 1.1   # deg; hook tip 7.8 mm above the pivot, groove depth 1.1 mm
REL = math.degrees(math.asin((GROOVE + 0.15) / HOOK_L))  # rotation at which the hook tip is out of the groove
out = []; t_rel = None; prev_b = 0.0
for r in rows:
    t = r[0]
    if t < 38.6: beta = 0.0   # far from the final gate line-up the lever rests on the rims (verified in check.py)
    else:
        wp = [wheel_poly((G_LOC[i] + r[i + 1]) % 360) for i in (1, 2, 3)]
        lo, hi = 0.0, BMAX
        if lever_free(hi, wp): beta = hi
        else:
            for _ in range(22):
                m = (lo + hi) / 2
                if lever_free(m, wp): lo = m
                else: hi = m
            beta = lo
    if t_rel is None and beta >= REL: t_rel = t
    if t_rel is None: pop = 0.0
    else:
        u = t - t_rel; pop = POP_H * min(1, u / 0.35) ** 0.6
        if u > 0.35: pop = POP_H * (1 + 0.06 * math.exp(-(u - 0.35) * 9) * math.sin((u - 0.35) * 40))
    out.append([round(v, 4) for v in r] + [round(beta, 4), round(pop, 3)])
drop = [o for o in out if o[5] > 0.05]
bfin = out[-1][5]
EV = {'picks': picks, 'stops': [s[1] for s in SEGS], 'drop0': drop[0][0], 'drop1': next(o[0] for o in out if o[5] >= bfin - 0.05), 'pop': t_rel, 'beta_fin': bfin, 'REL': REL}
geom = dict(PV=PV, TOOTH=TOOTH, ARM=ARM, HOOK_L=HOOK_L, GROOVE=GROOVE, R=R, D=D, RP=RP, PIN_W=PIN_W, FLY_W=FLY_W, DELTA=DELTA, GATE_W=GATE_W, TOOTH_W=TOOTH_W, CHAMF=CHAMF, G_LOC=G_LOC, COMBO=COMBO,
            TH=TH, SEGS=SEGS, LOOP=LOOP, DIS0=DIS0, FPS_K=FPS_K, EV=EV, POP_H=POP_H)
json.dump(geom, open('geom.json', 'w'), indent=1); json.dump(out, open('kin.json', 'w'))
print('DELTA %.2f deg' % DELTA); print('picks', picks); print('drop', EV['drop0'], EV['drop1'], 'pop', EV['pop'], 'beta', bfin, 'REL', round(REL, 2), 'gates', [round(g, 1) for g in G_LOC[1:]])
