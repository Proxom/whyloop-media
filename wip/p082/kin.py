# p082 self-cancelling turn signal "WHO TURNS / THE BLINKER OFF?" - kinematics + HARD GATE 5.2 checks (2D, view down the steering column)
# mm, column axis = z (toward the driver/camera). Angles in the x-y plane, CCW positive as seen by the driver. Right turn = wheel CW (theta < 0).
# Cancel cam: ring on the steering shaft, base radius RB with two bumps (lobes) of height H. It turns with the wheel (theta).
# Switch actuator: rigid with the stalk, pivots at P (below-left of the cam). Lever angle phi (deg, CW positive = stalk UP = right signal).
#   A notched detent holds phi at 0 or PHI_ON. Past the hump (PHI_HUMP) a centering spring snaps it to 0.
# Finger: hinged on the actuator at HNG, hangs toward the cam, length LF. It may fold CCW (tip moves +x) against a light spring; a stop pin blocks CW.
#   phi = 0: the finger tip is outside the lobes -> nothing touches. phi = PHI_ON: the tip sits between the base circle and the lobe tops.
#   Turning right (cam CW) the lobe meets the finger's left face -> the finger folds (beta > 0), lever stays put.
#   Turning back (cam CCW) the lobe meets the right face -> finger on its stop -> the lobe pushes the actuator CCW (phi drops) -> past the hump the spring snaps it to 0.
import json, math
import numpy as np
D2R = math.pi / 180
RB, H, LW = 26.0, 7.0, 28.0            # cam base radius, lobe height, lobe half width (deg)
LOBES = [210.0, 330.0]                  # lobe centres in the cam frame (deg), mirror-symmetric
P = np.array([-30.0, -25.0])            # actuator pivot
HNG0 = np.array([0.0, 45.0])            # finger hinge at phi = 0
LF = 10.0                               # finger length (hangs along -y in the actuator frame)
PHI_ON, PHI_HUMP = 12.0, 6.0
THMAX = -190.0
def rcam(psi_world, theta):
    d = (psi_world - theta) % 360.0; r = RB
    for c in LOBES:
        x = (d - c + 180) % 360 - 180
        if abs(x) < LW: r = max(r, RB + H * math.cos(math.pi / 2 * x / LW) ** 2)
    return r
def rot(v, a): c, s = math.cos(a), math.sin(a); return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])
def hinge(phi): return P + rot(HNG0 - P, -phi * D2R)
def finger_pts(phi, beta, n=11):
    h = hinge(phi); d = rot(np.array([0.0, -1.0]), (-phi + beta) * D2R)
    return [h + d * LF * i / (n - 1) for i in range(n)]
def pen(phi, beta, theta):
    """max penetration of the finger into the cam (>0 = overlap)"""
    m = -1e9
    for p in finger_pts(phi, beta):
        rho = math.hypot(*p); psi = math.degrees(math.atan2(p[1], p[0])); m = max(m, rcam(psi, theta) - rho)
    return m
FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0}
gap = 0.3
T['vo1'] = T['vo0'] + dur[0] + gap; T['flick_a'] = T['vo1'] + 0.55; T['flick_b'] = T['flick_a'] + 0.25
for i in range(2, 7): T[f'vo{i}'] = T[f'vo{i-1}'] + dur[i - 1] + gap
T['turn_a'] = T['vo3'] + 0.25; T['turn_b'] = T['vo3'] + dur[3] + 0.1
T['back_a'] = T['vo4'] + 0.15
LOOP = round(T['vo6'] + dur[6] + 2.0, 2); T['LOOP'] = LOOP
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
# --- find, on the way back, the wheel angle where the lobe first touches the rigid finger (phi = PHI_ON, beta = 0) and where phi reaches the hump
ths = np.arange(THMAX, 0.0001, 0.05)
th_touch = next(th for th in ths if pen(PHI_ON, 0, th) > 0) - 0.05
def push_phi(theta, phi_prev):
    """largest phi <= phi_prev with no overlap (the lobe pushes the actuator CCW)"""
    if pen(phi_prev, 0, theta) <= 0: return phi_prev
    lo, hi = 0.0, phi_prev
    for _ in range(40):
        mid = (lo + hi) / 2
        if pen(mid, 0, theta) > 0: hi = mid
        else: lo = mid
    return lo
ph = PHI_ON; th_hump = None
for th in np.arange(th_touch, 0.0001, 0.02):
    ph = push_phi(th, ph)
    if ph <= PHI_HUMP: th_hump = th; break
assert th_hump is not None, 'the lobe never pushes the lever past the hump'
print('return: touch at theta %.1f, hump at %.1f' % (th_touch, th_hump))
T['touch'] = T['vo4'] + 1.7; T['hump'] = T['vo5'] + 0.55; T['snap_b'] = T['hump'] + 0.14; T['home'] = T['vo5'] + 2.7
def theta_of(t):
    if t < T['turn_a']: return 0.0
    if t < T['turn_b']: return THMAX * ease((t - T['turn_a']) / (T['turn_b'] - T['turn_a']))
    if t < T['back_a']: return THMAX
    if t < T['touch']: return THMAX + (th_touch - THMAX) * ease((t - T['back_a']) / (T['touch'] - T['back_a']))
    if t < T['hump']: u = (t - T['touch']) / (T['hump'] - T['touch']); return th_touch + (th_hump - th_touch) * u
    if t < T['home']: u = (t - T['hump']) / (T['home'] - T['hump']); return th_hump * (1 - (u * u * (3 - 2 * u) * 0.6 + 0.4 * u))
    return 0.0
def fold_beta(phi, theta):
    if pen(phi, 0, theta) <= 0: return 0.0
    lo, hi = 0.0, 120.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if pen(phi, mid, theta) > 0: lo = mid
        else: hi = mid
    return hi
def sim(tmax, dt=1 / FPS_K):
    rows = []; phi = 0.0; snapped = False; t = 0.0
    while t <= tmax + 1e-9:
        th = theta_of(t)
        if t < T['flick_a']: phi = 0.0
        elif t < T['flick_b']: phi = PHI_ON * ease((t - T['flick_a']) / (T['flick_b'] - T['flick_a']))
        elif not snapped:
            phi = PHI_ON if t < T['touch'] - 0.3 else push_phi(th, phi)
            if phi <= PHI_HUMP + 1e-6 and t > T['touch'] - 0.3: snapped = True; t_s = t; phi_s = phi
        if snapped: phi = phi_s * (1 - ease((t - t_s) / 0.14))
        beta = fold_beta(phi, th) if (phi > PHI_HUMP and not snapped) else 0.0
        sig = 1.0 if (t >= T['flick_b'] - 0.05 and not snapped) else 0.0
        rows.append([round(t, 4), round(th, 3), round(phi, 4), round(beta, 3), sig]); t += dt
    return rows
rows = sim(LOOP + 0.02)
t_snap = next(r[0] for r in rows if r[0] > T['flick_b'] and r[4] == 0)
T['snap'] = t_snap
# hook (0 .. hookEnd): the payoff moment, replayed from just before the snap
HOOK0 = t_snap - 0.62
byT = {round(r[0], 4): r for r in rows}
for r in rows:
    if r[0] < T['hookEnd']:
        src = rows[min(len(rows) - 1, int(round((HOOK0 + r[0]) * FPS_K)))]; r[1:] = src[1:]
json.dump(rows, open('kin.json', 'w'))
# ---------------- checks (whole loop, every kin row) ----------------
worst = -1e9; bmax = 0
for r in rows:
    t, th, phi, beta, sig = r
    p = pen(phi, beta, th); worst = max(worst, p); bmax = max(bmax, beta)
    assert beta >= -1e-9, 'finger folded past its stop'
print('finger-cam max overlap %.4f mm (<= 0.02 ok: contact only)' % worst); assert worst < 0.02, 'finger passes through the cam'
# neutral: no contact for any wheel angle
cl = min(-pen(0, 0, th) for th in np.arange(-360, 360, 0.5)); print('neutral clearance %.2f mm' % cl); assert cl > 0.5
# signal on, turning INTO the turn: the lever stays at PHI_ON (only the finger folds); cause: lobe moving +x at the finger
seg = [r for r in rows if T['turn_a'] <= r[0] <= T['turn_b']]
assert all(abs(r[2] - PHI_ON) < 1e-6 for r in seg), 'lever moved while turning in'
print('turn-in: max fold %.1f deg, lever stays at %.1f deg' % (max(r[3] for r in seg), PHI_ON)); assert max(r[3] for r in seg) > 15
# the lever only leaves PHI_ON while the lobe touches the rigid finger (nothing moves without a cause)
for r in rows:
    if r[0] > T['flick_b'] + 0.01 and r[2] < PHI_ON - 1e-3 and r[4] == 1: assert pen(r[2], 0, r[1]) > -0.05, ('lever moved without contact', r)
# actuator arc (radius RA around the cam) never touches the cam
RA = 40.0; assert RA > RB + H + 1
print('snap at t=%.2f; LOOP %.2f' % (t_snap, LOOP))
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, RB=RB, H=H, LW=LW, LOBES=LOBES, P=P.tolist(), HNG0=HNG0.tolist(), LF=LF, PHI_ON=PHI_ON, PHI_HUMP=PHI_HUMP, THMAX=THMAX, RA=RA,
         th_touch=th_touch, th_hump=th_hump)
json.dump(G, open('geom.json', 'w'), indent=1)
print({k: round(v, 2) for k, v in T.items()})
# actuator arc band (inner radius 43 about the cam centre at phi = 0, angles 84..222 deg) rotated with the lever never reaches the lobes
mb = 1e9
for phi in np.linspace(0, PHI_ON, 25):
    for a in np.linspace(84, 222, 140):
        q = P + rot(np.array([43 * math.cos(a * D2R), 43 * math.sin(a * D2R)]) - P, -phi * D2R); mb = min(mb, math.hypot(*q))
    for q0 in [np.array([8.0, 42.0])]:
        q = P + rot(q0 - P, -phi * D2R); mb = min(mb, math.hypot(*q))
print('actuator band to cam centre min %.2f mm (lobe tips at %.1f)' % (mb, RB + H)); assert mb > RB + H + 0.5
