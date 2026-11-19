# p079 winged corkscrew "WHY DO THE / WINGS GO UP?" - kinematics + HARD GATE 5.2 checks (shapely, venv python)
# mm, y up, bottle lip top y = 0. Section plane z = 0 holds the shaft axis, both pinion axes (along z) and both wings.
# Rack = rings around the shaft (tooth profile revolved, so the shaft can spin while it meshes). Pinion = gear sector at the wing root.
# State: s = shaft travel down relative to the body (0..D). Wing angle = TH0 + s / RP (rack-and-pinion rolling).
#   twist: worm depth in the cork = s - GAP, handle angle = -2 pi s / WP (right-hand worm, turned clockwise from above)
#   push wings down: s decreases, the cork rides up with the worm: cork lift c = D - s (worm depth stays D - GAP)
import json, math
import numpy as np
from shapely.geometry import Polygon
from shapely import affinity

FPS_K = 120
M, Z = 2.0, 15; RP = M * Z / 2                   # pinion pitch radius 15
RACK_R = 6.0                                     # rack pitch radius on the shaft
PX = RACK_R + RP                                 # pinion centre x = +-21
PY = 75.0                                        # pinion centre y
TH0 = math.radians(-74); SWING = math.radians(148)
D = SWING * RP                                   # 38.75 mm shaft travel
WP = 9.0                                         # worm pitch (mm per turn)
GAP = 3.0                                        # worm tip above the cork top at s = 0
CORK_L, CORK_R = 38.0, 9.5
WORM_TIP, WORM_TOP = 3.0, 40.0                   # shaft-local y (shaft-local = world y + s)
RACK_Y0, RACK_Y1 = 60.0, 129.0
COLLAR_Y0, COLLAR_Y1, COLLAR_R = 129.0, 133.0, 7.4
HANDLE_Y0 = 134.0
HEAD_TOP = 91.0
PITCH = math.pi * M

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)

# ---------------- timeline (video seconds) ----------------
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {}
T['vo0'] = 0.35
T['hookEnd'] = 0.95                                # flash cut from the payoff clip to the start state
T['vo1'] = 2.75; T['tw1a'] = 2.9; T['tw1b'] = 5.5   # twist: s 0 -> 0.45 D
T['vo2'] = T['vo1'] + dur[1] + 0.35                 # ghost the head, name the parts (hold)
T['vo3'] = T['vo2'] + dur[2] + 0.35; T['tw2a'] = T['vo3'] + 0.5; T['tw2b'] = T['vo3'] + dur[3] + 0.6   # slow: s -> D
T['vo4'] = T['tw2b'] + 0.45; T['pa'] = T['vo4'] + 0.25; T['pb'] = T['vo4'] + dur[4] + 0.2            # push wings down: s D -> 0, cork out
T['vo5'] = T['pb'] + 0.35
T['ans'] = T['vo5']
LOOP = round(T['vo5'] + dur[5] + 2.3, 2)
T['LOOP'] = LOOP
S1 = 0.45 * D

def state(t):
    """returns s (shaft travel), c (cork lift), worm depth into the cork, handle angle"""
    if t < T['hookEnd']:                           # hook: the payoff moment (wings pushed down, cork comes up)
        u = ease(t / T['hookEnd'] * 0.92 + 0.04); s = D * (0.78 - 0.78 * u); return s, D - s, D - GAP, -2 * math.pi * D / WP
    if t < T['tw1a']: s = 0
    elif t < T['tw1b']: s = S1 * ease((t - T['tw1a']) / (T['tw1b'] - T['tw1a']))
    elif t < T['tw2a']: s = S1
    elif t < T['tw2b']: s = S1 + (D - S1) * ease((t - T['tw2a']) / (T['tw2b'] - T['tw2a']))
    else: s = None
    if s is not None:
        return s, 0.0, max(0.0, s - GAP), -2 * math.pi * s / WP
    if t < T['pa']: s = D
    elif t < T['pb']: s = D * (1 - ease((t - T['pa']) / (T['pb'] - T['pa'])))
    else: s = 0.0
    return s, D - s, D - GAP, -2 * math.pi * D / WP

rows = []
n = int(LOOP * FPS_K) + 2
for i in range(n):
    t = i / FPS_K; s, c, wd, ha = state(min(t, LOOP))
    rows.append([round(t, 4), round(s, 4), round(c, 4), round(wd, 4), round(ha, 5)])
json.dump(rows, open('kin.json', 'w'))

# ---------------- gear outline (port of kit.js gearOutline, backlash 0.05) ----------------
def gear_outline(z, m, pa=20, backlash=0.05, ppf=8):
    D2R = math.pi / 180; rp = z * m / 2; rb = rp * math.cos(pa * D2R); ra = rp + m; rf = max(rp - 1.25 * m, 0.5 * m)
    inv = lambda a: math.tan(a) - a; half = (math.pi / (2 * z)) - backlash / (2 * rp) + inv(pa * D2R); pts = []
    for i in range(z):
        c = i * 2 * math.pi / z; fl = []
        for k in range(ppf + 1):
            r = max(rb, rf) + (ra - max(rb, rf)) * k / ppf; a = math.acos(min(1, rb / r)); fl.append((r, inv(a)))
        a0, a1 = c - half, c + half; gap = math.pi / z; ra0, ra1 = a0 - 0.012, a1 + 0.012
        fr = c - 2 * gap + half + 0.012
        for k in range(1, 4): a = fr + (ra0 - fr) * k / 3; pts.append((rf * math.cos(a), rf * math.sin(a)))
        if rb > rf: pts.append((rb * 0.995 * math.cos(a0), rb * 0.995 * math.sin(a0)))
        for r, e in fl: pts.append((r * math.cos(a0 + e), r * math.sin(a0 + e)))
        for r, e in reversed(fl): pts.append((r * math.cos(a1 - e), r * math.sin(a1 - e)))
        if rb > rf: pts.append((rb * 0.995 * math.cos(a1), rb * 0.995 * math.sin(a1)))
        pts.append((rf * math.cos(ra1), rf * math.sin(ra1)))
    return pts

# Gear phase: rack tooth centred on y = PY (world) at s = 0 -> the pinion must show a GAP at world angle pi at s = 0.
# Pinion group rotation = theta (wing direction = local +x). Teeth sit at local angles DELTA + i*24deg, gaps at DELTA + 12deg + i*24deg.
DELTA = (math.pi - TH0 - math.pi / Z) % (2 * math.pi / Z)
# sector of teeth kept (local angles): contact local angle = pi - theta, theta in [TH0, TH0+SWING] -> [pi-TH0-SWING, pi-TH0] +- 22 deg
SEC0 = math.pi - TH0 - SWING - math.radians(24); SEC1 = math.pi - TH0 + math.radians(24)
full = gear_outline(Z, M)
def rot(p, a): return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))
def sector_poly():
    pts = []
    for p in full:
        q = rot(p, DELTA); ang = math.atan2(q[1], q[0]) % (2 * math.pi)
        if SEC0 <= ang <= SEC1: pts.append((ang, q))
    pts.sort(key=lambda x: x[0]); ring = [q for _, q in pts]
    hub = 9.5   # back of the sector: hub arc through the wing side (local 0)
    a_end, a_start = pts[-1][0], pts[0][0] + 2 * math.pi
    for k in range(1, 24): a = a_end + (a_start - a_end) * k / 24; ring.append((hub * math.cos(a), hub * math.sin(a)))
    return ring
SECTOR = sector_poly()

# rack ring profile in the section (x > 0 side): pitch line x = RACK_R, tooth tips toward +x, centred teeth at shaft-local y = PY + k*PITCH
def rack_poly(s, side=1):
    ad, de, ta = M, 1.25 * M, math.tan(math.radians(20)); hw = PITCH / 4 - 0.05
    pts = [(0, RACK_Y0 - s)]
    k0 = math.ceil((RACK_Y0 + 2 - PY) / PITCH); k1 = math.floor((RACK_Y1 - 2 - PY) / PITCH)
    pts.append((RACK_R - de, RACK_Y0 - s))
    for k in range(k0, k1 + 1):
        c = PY + k * PITCH - s
        pts += [(RACK_R - de, c - hw - de * ta), (RACK_R + ad, c - hw + ad * ta), (RACK_R + ad, c + hw - ad * ta), (RACK_R - de, c + hw + de * ta)]
    pts += [(RACK_R - de, RACK_Y1 - s), (0, RACK_Y1 - s)]
    return Polygon([(side * x, y) for x, y in pts])

def pinion_poly(s, side=1):
    th = TH0 + s / RP
    P = Polygon(SECTOR); P = affinity.rotate(P, th, origin=(0, 0), use_radians=True); P = affinity.translate(P, PX, PY)
    if side < 0: P = affinity.scale(P, -1, 1, origin=(0, 0))
    return P

# ---------------- checks over the whole loop ----------------
worst_ov, min_gap = 0.0, 1e9
for t in np.arange(0, LOOP, 1 / 60):
    s, c, wd, ha = state(t)
    for side in (1, -1):
        R_ = rack_poly(s, side); Pn = pinion_poly(s, side)
        ov = R_.intersection(Pn).area; worst_ov = max(worst_ov, ov); min_gap = min(min_gap, R_.distance(Pn) if ov == 0 else 0)
    # handle never sinks into the head top
    assert HANDLE_Y0 - s >= HEAD_TOP + 0.3, ('handle hits head', t, s)
    # rack stays engaged: the pinion contact (world y = PY) lies inside the rack zone with 2 teeth margin
    assert RACK_Y0 - s + 2 * PITCH < PY < RACK_Y1 - s - 2 * PITCH, ('rack out of mesh', t)
    # worm tip never below the cork bottom
    assert wd < CORK_L - 2.0, ('worm through the cork', t, wd)
    # cork stays coaxial and inside the body cage while it rises (cage inner radius 11 > cork 9.5)
print('mesh check: worst overlap area %.4f mm2, min clearance %.3f mm' % (worst_ov, min_gap))
assert worst_ov < 0.02, 'teeth pass through each other'

# wing clearance: wing arm (centre line from r=10 to r=80, half width 4) vs body cage (x in [-14,14] for y in [-12,57], base bell R 19 at y<6)
def wing_poly(s, side=1):
    th = TH0 + s / RP
    W = Polygon([(10, -4.5), (62, -3.2), (66, -7), (80, -6.5), (84, 0), (80, 6.5), (66, 7), (62, 3.2), (10, 4.5)])
    W = affinity.rotate(W, th, origin=(0, 0), use_radians=True); W = affinity.translate(W, PX, PY)
    if side < 0: W = affinity.scale(W, -1, 1, origin=(0, 0))
    return W
body = Polygon([(-19, -12), (19, -12), (19, 6), (14, 22), (14, 57), (-14, 57), (-14, 22), (-19, 6)])
neck = Polygon([(-15.5, -200), (15.5, -200), (15.5, 0), (-15.5, 0)])
mind = 1e9
for s in np.linspace(0, D, 60):
    for side in (1, -1):
        Wp = wing_poly(s, side); assert not Wp.intersects(body), ('wing hits body', s); assert not Wp.intersects(neck), ('wing hits bottle', s)
        mind = min(mind, Wp.distance(body))
print('wing-body min clearance %.2f mm' % mind)

G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, M=M, Z=Z, RP=RP, RACK_R=RACK_R, PX=PX, PY=PY, TH0=TH0, SWING=SWING, D=D, WP=WP, GAP=GAP, CORK_L=CORK_L, CORK_R=CORK_R,
         WORM_TIP=WORM_TIP, WORM_TOP=WORM_TOP, RACK_Y0=RACK_Y0, RACK_Y1=RACK_Y1, COLLAR_Y0=COLLAR_Y0, COLLAR_Y1=COLLAR_Y1, COLLAR_R=COLLAR_R, HANDLE_Y0=HANDLE_Y0,
         HEAD_TOP=HEAD_TOP, PITCH=PITCH, DELTA=DELTA, SECTOR=[[round(x, 4), round(y, 4)] for x, y in SECTOR], vo=[d['dur'] for d in vo])
json.dump(G, open('geom.json', 'w'), indent=1)
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
