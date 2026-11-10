# p058 handbrake: what holds it up? mm, side section in x-y (x = toward the front of the car, y up), angles CCW positive.
# The lever pivots at O = (0,0). A fixed sector plate (straddled by the lever's two side plates) carries teeth on an arc
# around O: each tooth is a ramp rising with the angle (lever going UP) and a steep radial face. The pawl pivots on the lever
# at Q; its round tip rides on the teeth. The button spring pulls the push rod forward, which turns the pawl clockwise = tip
# into the teeth. Going up: the ramp pushes the tip out, it drops off the edge = CLICK. Going down: the tip hits the steep face
# and the load turns the pawl further in (self-locking) = HELD. Pressing the button pushes the rod back: the pawl turns out of
# the teeth and the lever can go down. The pawl angle beta (CCW = out) is the smallest value keeping 0.05 mm clearance (shapely).
import json, math, numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
D2R = math.pi / 180
R0, H, P, NT = 40.0, 2.6, 4.5 * D2R, 9          # tooth root radius, height, pitch (angle), number of teeth
RHO, GAP = 0.9, 0.05                              # pawl tip radius, clearance
TH_REST = 6.0 * D2R                               # lever rest angle (on its stop)
ALPHA = -38.0 * D2R                              # tip polar angle (lever frame)
pol = lambda r, a: np.array([r * math.cos(a), r * math.sin(a)])
T0 = pol(R0 + RHO + GAP, ALPHA)                   # tip centre (nose points in toward the teeth)
Q = pol(46.2, ALPHA + 18 * D2R)                   # pawl pivot: ahead of the tip and ABOVE the contact line -> the load turns the pawl IN (self-locking)
NB = pol(44.7, ALPHA + 2.2 * D2R)                 # root of the nose on the pawl arm
RP = Q + np.array([6.0, 10.0])                    # rod pin on the pawl's upper arm (lever frame)
BTN = np.array([262.0, 0.0])                      # rod end at the button (lever frame, rest)
ER = (BTN - RP) / np.linalg.norm(BTN - RP)        # rod axis
PSI0 = ALPHA + TH_REST - 0.62 * P                 # first steep face (world angle): the tip rests in valley 0
def plate_poly():
    pts = []
    a_lo = PSI0 - 14 * D2R
    for i in range(30): a = a_lo + (PSI0 - a_lo) * i / 29; pts.append((R0 * math.cos(a), R0 * math.sin(a)))     # land below the first tooth
    for k in range(NT):
        a0 = PSI0 + k * P
        for i in range(41):
            u = i / 40; a = a0 + u * P; r = R0 + H * u; pts.append((r * math.cos(a), r * math.sin(a)))
    a1 = PSI0 + NT * P
    for i in range(1, 41):   # rounded shoulder past the last tooth, sweeping down to the pivot hub
        u = i / 40; a = a1 + 75 * D2R * u; r = (R0 - 2.0) - (R0 - 2.0 - 13.0) * u ** 1.6; pts.append((r * math.cos(a), r * math.sin(a)))
    pts += [(-20, -4), (-27, -24), (-30, -62), (40, -62), (34, -44)]
    return Polygon(pts).buffer(0)
PLATE = plate_poly()
def pawl_local(beta):   # pawl outline in the LEVER frame at pawl angle beta (rotation about Q)
    return affinity.rotate(PAWL0, beta, origin=tuple(Q), use_radians=True)
def pawl_parts():
    tip = Point(*T0).buffer(RHO, 40); nb = Point(*NB).buffer(1.6, 32); qb = Point(*Q).buffer(2.4, 40); rb = Point(*RP).buffer(1.7, 32)
    return unary_union([unary_union([tip, nb]).convex_hull, unary_union([nb, qb]).convex_hull, unary_union([qb, rb]).convex_hull])
PAWL0 = pawl_parts()
def world(poly, th): return affinity.rotate(poly, th, origin=(0, 0), use_radians=True)
BETA_MAX = 40 * D2R
def defl(th, lo=0.0):   # smallest beta >= lo with clearance >= GAP
    if world(pawl_local(lo), th).distance(PLATE) >= GAP - 1e-7: return lo
    a, b = lo, BETA_MAX
    for _ in range(36):
        m = (a + b) / 2
        if world(pawl_local(m), th).distance(PLATE) >= GAP - 1e-7: b = m
        else: a = m
    return b
def tip_r(th, beta): p = affinity.rotate(Point(*T0), beta, origin=tuple(Q), use_radians=True); return math.hypot(p.x, p.y)
# beta needed to clear all tooth tops by 0.6 mm (button pressed)
BETA_OUT = next(b * D2R for b in np.arange(0, 40, 0.25) if tip_r(0, b * D2R) >= R0 + H + RHO + 1.6)
# click angles: lever angle where the tip passes tooth top k (going up); hold angles: lever settles onto the steep face
def scan(th0, th1, n):
    ths = np.linspace(th0, th1, n); return ths, np.array([defl(t) for t in ths])

# ---------- lever programme ----------
def jump_after(th_lo, th_hi):   # lever angle where the tip drops off a tooth top (largest drop of defl) inside [th_lo, th_hi]
    ths = np.arange(th_lo, th_hi, 0.01 * D2R); ds = np.array([defl(x) for x in ths]); i = int(np.argmin(np.diff(ds)))
    a, b = ths[i], ths[i + 1]; hi_v = ds[i]
    for _ in range(30):
        m = (a + b) / 2
        if defl(m) > hi_v - 1.0 * D2R: a = m
        else: b = m
    return b
# tooth tops: tip world angle passes PSI0 + (k+1) P  ->  approximate lever angle, then refine
TJ = []
for k in range(1, 7):
    guess = PSI0 + k * P - ALPHA
    TJ.append(jump_after(guess - 0.3 * D2R, guess + 2.8 * D2R))
print('jump angles', [round(x / D2R, 3) for x in TJ])
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(max(u, 0), 1))
smq = lambda u: (lambda v: v * v * v * (v * (6 * v - 15) + 10))(min(max(u, 0), 1))
LOOP = 18.5
T = dict(PULL1=(0.0, 1.55), LET1=(1.6, 1.74), FADE_OUT=(2.5, 3.4), PULL2=(6.55, 8.85), PUSHDN=(10.55, 11.45), LIFT=(11.95, 12.25),
         PRESS=(12.6, 13.6), LOWER=(14.45, 15.6), RELEASE=(15.72, 15.92), FADE_IN=(15.95, 16.85), FOLLOW=(16.75, 18.4))
TH1 = TJ[2] + 0.42 * P; TH2 = TJ[4] + 0.42 * P; HOLD3 = TJ[2] + 0.04 * D2R; HOLD5 = TJ[4] + 0.04 * D2R
def lever(t):
    t = t % LOOP
    a, b = T['PULL1']
    if t < a: return TH_REST
    if t < b: return TH_REST + (TH1 - TH_REST) * sm((t - a) / (b - a))
    a, b = T['LET1']
    if t < a: return TH1
    if t < b: u = (t - a) / (b - a); return TH1 - (TH1 - HOLD3) * u * u      # cable pulls it back: accelerates onto the face
    a, b = T['PULL2']
    if t < a: return HOLD3
    if t < b: return HOLD3 + (TH2 - HOLD3) * sm((t - a) / (b - a))
    a, b = T['PUSHDN']
    if t < a: return TH2
    if t < b: u = (t - a) / (b - a); return TH2 - (TH2 - HOLD5) * (0.5 * u + 0.5 * u * u)
    a, b = T['LIFT']; up = 0.25 * P
    if t < a: return HOLD5
    if t < b: return HOLD5 + up * sm((t - a) / (b - a))
    a, b = T['LOWER']
    if t < a: return HOLD5 + up
    if t < b: return HOLD5 + up - (HOLD5 + up - TH_REST) * smq((t - a) / (b - a))
    return TH_REST
def button(t):   # pawl angle forced by the button (0 = released)
    t = t % LOOP; a, b = T['PRESS']; c, d = T['RELEASE']
    if t < a or t >= d: return 0.0
    if t < b: return BETA_OUT * sm((t - a) / (b - a))
    if t < c: return BETA_OUT
    return BETA_OUT * (1 - sm((t - c) / (d - c)))
FS = 240; NF = int(LOOP * FS); W_MAX = 320 * D2R   # pawl snap-in speed limit (spring driven): ~6 deg in 20 ms
rows = []; beta = defl(TH_REST); prev_target = beta
for i in range(NF):
    t = i / FS; th = lever(t); bb = button(t); tgt = max(defl(th, 0.0), bb)
    beta = max(tgt, beta - W_MAX / FS) if i else tgt
    rows.append(dict(t=round(t, 5), th=round(th, 7), beta=round(beta, 7), btn=round(bb, 6)))
# events from the motion: click = pawl lands after dropping off a tooth; lock = lever stops on the steep face
ev = []
for i in range(1, NF):
    if rows[i]['btn'] == 0 and rows[i - 1]['beta'] - rows[i]['beta'] > 0.5 * D2R and rows[i]['beta'] - rows[i + 1]['beta'] < 0.3 * D2R:
        ev.append(dict(type='click', t=rows[i]['t']))
ev += [dict(type='lock', t=T['LET1'][1]), dict(type='lock', t=T['PUSHDN'][1]), dict(type='press', t=T['PRESS'][0] + 0.06), dict(type='rest', t=T['LOWER'][1]),
       dict(type='release', t=T['RELEASE'][1]), dict(type='pull', t0=T['PULL1'][0], t1=T['PULL1'][1]), dict(type='pull', t0=T['PULL2'][0], t1=T['PULL2'][1]),
       dict(type='pull', t0=T['LOWER'][0], t1=T['LOWER'][1])]
json.dump(rows, open('kin_240.json', 'w')); json.dump(ev, open('events.json', 'w'), indent=1)
G = dict(R0=R0, H=H, P=P, NT=NT, RHO=RHO, GAP=GAP, TH_REST=TH_REST, ALPHA=ALPHA, T0=T0.tolist(), Q=Q.tolist(), NB=NB.tolist(), RP=RP.tolist(), BTN=BTN.tolist(), ER=ER.tolist(),
         PSI0=PSI0, BETA_OUT=BETA_OUT, LOOP=LOOP, T=T, TJ=TJ, PLATE=[list(p) for p in PLATE.exterior.coords][:-1], PAWL=[list(p) for p in PAWL0.exterior.coords][:-1])
json.dump(G, open('geom.json', 'w'))
clicks = [e['t'] for e in ev if e['type'] == 'click']
print('clicks', clicks); print('loop closes:', abs(rows[0]['th'] - lever(LOOP - 1e-9)) < 1e-6, round(rows[0]['beta'] / D2R, 3), round(rows[-1]['beta'] / D2R, 3))
print('lever range %.2f..%.2f deg, beta max %.2f deg' % (min(r['th'] for r in rows) / D2R, max(r['th'] for r in rows) / D2R, max(r['beta'] for r in rows) / D2R))
