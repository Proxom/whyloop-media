# p054 zip tie: why does a zip tie only go one way? 2D kinematics (mm), x-y = the plane the tie lies in, z = tape width (out of the bench).
# Tail tape runs along +y through the head's slot; its sawtooth teeth face -x (toward the pawl). Pull = +y.
# Pawl = flexible tongue hinged at its root on the slot's -x wall, leaning up toward the tape; the tip's upper corner rides the teeth.
# Single source for scene.html (kin_240.json), audio (events.json) and the HARD GATE check (check.py).
import json, math, numpy as np
from shapely.geometry import Polygon
from shapely import affinity

P = 1.6        # tooth pitch
H = 0.62       # tooth height (protrudes to x = -H at the tall side)
T = 1.30       # tape base thickness (x from 0 to T)
TW = 4.8       # tape width (z)
LOOP = 13.0
FS = 2400      # simulation rate
GAP = 0.03     # tip clearance under the steep face when locked
EXTRA = 0.087680
G0 = 0.45      # rest gap below the face after a tick (> the tip's rise when it swings out, so every 1-pitch pull ticks once)
# pawl in its reference pose (theta = 0): root R, direction phi from +y toward +x, tip corner exactly on x = 0
PHI = math.radians(30.0); W = 0.95
TIPY = 1.05
L = 3.55
R = (0.0 - L * math.sin(PHI), TIPY - L * math.cos(PHI))

def d_of(s):  # tooth protrusion (toward -x) at strap coordinate s; steep face at s = k*P (tall above, valley below)
    u = (s / P) % 1.0
    return H * (1.0 - u)

def pawl_poly(theta=0.0):
    # right edge from tip corner C down along -dir; end face horizontal through C; width W perpendicular to the axis
    dx, dy = math.sin(PHI), math.cos(PHI)
    nx, ny = -dy, dx                       # left normal (toward -x side)
    C = np.array([0.0, TIPY]); Rt = np.array(R)
    base_r = Rt - 0.9 * np.array([dx, dy])  # extend below the root into the head wall (hidden there)
    base_l = base_r + W * np.array([nx, ny])
    # end face slopes down to the left (undercut 24 deg) so only the tip corner meets the teeth
    e = np.array([-math.cos(math.radians(24)), -math.sin(math.radians(24))]); dvec = np.array([dx, dy])
    A = np.array([e, -dvec]).T; a, b = np.linalg.solve(A, base_l - C); lft = C + a * e
    poly = Polygon([tuple(C), tuple(base_r), tuple(base_l), tuple(lft)])
    return affinity.rotate(poly, theta, origin=R, use_radians=True)

def tip(theta):
    c, s = math.cos(theta), math.sin(theta); vx, vy = 0.0 - R[0], TIPY - R[1]
    return (R[0] + c * vx - s * vy, R[1] + s * vx + c * vy)

def gfun(theta, Y):  # >0: tip corner clear of the tape surface, <0: inside
    x, y = tip(theta); return (-d_of(y - Y)) - x

def contact(Y):
    # smallest outward rotation (CCW, theta>0) that keeps the tip corner on/outside the tooth surface
    lo = -0.08
    if gfun(lo, Y) >= 0: return lo
    hi = lo
    while gfun(hi, Y) < 0: lo = hi; hi += 0.004   # scan outward: first clearance, never 'through' a face
    for _ in range(30):
        m = 0.5 * (lo + hi)
        if gfun(m, Y) >= 0: hi = m
        else: lo = m
    return hi

# sample points on the pawl's strap-facing edges (right edge + end face) for the clearance test
_pp = pawl_poly(0.0); _c = list(_pp.exterior.coords)
EDGE = []
for (a, b) in [(_c[0], _c[1]), (_c[3], _c[0])]:
    for i in range(41): EDGE.append((a[0] + (b[0] - a[0]) * i / 40, a[1] + (b[1] - a[1]) * i / 40))
EDGE = np.array(EDGE)
def clear(theta, Y):
    c, s = math.cos(theta), math.sin(theta); v = EDGE - np.array(R)
    x = R[0] + c * v[:, 0] - s * v[:, 1]; y = R[1] + s * v[:, 0] + c * v[:, 1]
    u = ((y - Y) / P) % 1.0; surf = -H * (1.0 - u)
    return bool(np.all((x <= surf + 1e-6) | (x > T)))

# ---- commanded strap motion: list of (t0, t1, dY) eased pulls ----
ease = lambda u: 0.0 if u <= 0 else 1.0 if u >= 1 else u * u * (3 - 2 * u)
PULLS = [(0.05, 0.40, P), (0.55, 0.90, P), (1.05, 1.40, P), (1.55, 1.90, P), (2.05, 2.40, P),
         (4.55, 5.25, P), (5.55, 6.25, P), (6.45, 6.85, 0.5 * P),
         (7.15, 7.40, -1.2 * P), (7.95, 8.15, -0.6 * P),
         (11.0, 11.35, P + G0 - GAP + EXTRA), (11.5, 11.85, P), (12.0, 12.35, P), (12.5, 12.85, P)]
def cmd(t):
    return sum(dy * ease((t - a) / (b - a)) for a, b, dy in PULLS)

# initial strap offset: tip seated just under a steep face (s_rel = k*P - GAP) at theta = contact
def seat_Y():
    # tip corner resting on the valley floor GAP below a steep face: x = -d(P-GAP) = -H*GAP/P
    xt = -H * G0 / P; lo, hi = -0.08, 0.4
    for _ in range(60):
        m = 0.5 * (lo + hi)
        if tip(m)[0] > xt: lo = m
        else: hi = m
    return tip(lo)[1] - (P - G0)
Y0 = seat_Y()

N = int(LOOP * FS); dt = 1.0 / FS
Y = Y0; th = contact(Y0); OMEGA_IN = 14.0
while not clear(th, Y0): th += 0.0005; OMEGA_IN = 14.0  # rad/s max inward snap speed (spring)
out = []; ev = []; locked = False; lock_ev = []
prevc = cmd(0.0); hard = None
for i in range(N + 1):
    t = i * dt; c = cmd(t); dc = c - prevc; prevc = c
    Yn = Y + dc
    # one-way constraint: moving down, the steep face above the tip cannot pass the tip's end face
    if dc < 0:
        x, y = tip(th); s = y - Yn
        # the face just above the tip (in strap coordinates) is at k*P with k = ceil((y - Y)/P)
        k = math.ceil((y - Y) / P - 1e-9); face = k * P
        if s > face - GAP:  # would pass the face -> stop with GAP clearance
            Yn = y - (face - GAP)
            if not locked: lock_ev.append(t); locked = True
    else:
        if dc > 1e-9: locked = False
    Y = Yn
    thc = th
    tt = th - OMEGA_IN * dt
    if clear(tt, Y): th = tt
    elif clear(th, Y):
        lo_, hi_ = tt, th
        for _ in range(22):
            m = 0.5 * (lo_ + hi_)
            if clear(m, Y): hi_ = m
            else: lo_ = m
        th = hi_
    else:
        hi_ = th
        while not clear(hi_, Y): hi_ += 0.002
        lo_ = hi_ - 0.002
        for _ in range(16):
            m = 0.5 * (lo_ + hi_)
            if clear(m, Y): hi_ = m
            else: lo_ = m
        th = hi_
    thc = th
    out.append((t, Y, th, thc))

# snap events (tick sounds): big inward drops of the contact angle
thcs = np.array([o[3] for o in out]); ths = np.array([o[2] for o in out])
for i in range(1, len(out)):
    if thcs[max(0,i - 24)] - thcs[i] > 0.06 and not (ev and out[i][0] - ev[-1]['t'] < 0.1): ev.append({'t': out[i][0], 'type': 'tick', 'v': float(thcs[i - 1] - thcs[i])})
for t in lock_ev: ev.append({'t': t, 'type': 'lock', 'v': 1.0})
ev.sort(key=lambda e: e['t'])

Yend = out[-1][1]
step = (Yend - Y0) / P
print('Y0 %.4f  end travel %.4f pitches  ticks %d  locks %s' % (Y0, step, sum(e['type'] == 'tick' for e in ev), [round(t, 3) for t in lock_ev]))
print('theta range %.4f..%.4f rad' % (ths.min(), ths.max()))
kin = []
for i in range(0, N, FS // 240):
    t, Yv, thv, _ = out[i]; kin.append({'Y': round(Yv - Y0, 5), 'th': round(thv, 5)})
json.dump(kin, open('kin_240.json', 'w'))
json.dump(ev, open('events.json', 'w'), indent=0)
pp = pawl_poly(0.0)
geo = {'P': P, 'H': H, 'T': T, 'TW': TW, 'LOOP': LOOP, 'R': R, 'Y0': Y0, 'tipY': TIPY,
       'pawl': [list(map(float, c)) for c in list(pp.exterior.coords)[:-1]],
       'thMin': float(ths.min()), 'thMax': float(ths.max()), 'travel': round(step, 4)}
json.dump(geo, open('geom.json', 'w'), indent=1)
import subprocess; subprocess.run(['python3.13', 'geom.py'])
