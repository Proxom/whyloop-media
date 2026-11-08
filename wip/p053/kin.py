# p053 seatbelt Part 2: the VEHICLE sensor. Simplified retractor side view (x = car forward, y up, z = spool axis toward camera).
# A lock wheel with 24 sawtooth teeth sits on the spool end (center O). Below it hangs a small pendulum on a pin P:
# a brass bob below the pin, a short arm with a catch finger above it. Braking (car decelerates) -> inertia swings the bob
# forward (+x, counterclockwise), the arm tips the catch up into the teeth. The occupant then pulls the belt out (spool turns
# clockwise = unwind) and the next steep tooth face hits the catch -> the spool stops (locked). After the stop the belt goes
# slack, the spool turns back (rewind), the tooth slope lifts the catch out and gravity swings the pendulum back.
# Everything is simulated at 2400 Hz from the car deceleration a(t) and the spool command; contacts are polygon tests (shapely).
import json, math, numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
from shapely.ops import unary_union
D = math.pi / 180; TAU = 2 * math.pi
N, RO, RI = 24, 18.0, 15.0; PITCH = TAU / N
LOOP = 15.0; G = 9.81
# --- lock wheel (gear frame): steep face at psi = k*pitch + PH, slope from RO down to RI ---
import os
PH = float(os.environ.get('PH', '8')) * D  # wall offset (deg) from the nominal lock wall
def rprof(psi):  # (unused helper)
    s = ((psi - PH) / PITCH) % 1.0
    return RO - (RO - RI) * s
def gear_poly():
    pts = []
    for k in range(N):
        for i in range(0, 41):
            s = i / 40; a = PH + TW0_G + (k + s) * PITCH
            r = RO - (RO - RI) * (s if i < 40 else 0.99999)
            pts.append((r * math.cos(a), r * math.sin(a)))
    return Polygon(pts).buffer(0)
TW0_G = (-58 * D + 0.3 * PITCH)
GEAR = gear_poly()
# --- pendulum: designed in its ENGAGED pose (phi = PHI_E) so the catch is a hook that fits the tooth gap next to the wall,
#     then rotated back by -PHI_E about the pin P to get the rest pose (rod hanging straight down) ---
ARM, PHI_E, THC = 11.0, 34 * D, -58 * D
LBOB, RBOB = 15.0, 5.2
TW0 = THC + 0.3 * PITCH                         # nominal wall angle (gear frame at lock)
C = np.array([(RO + 0.6) * math.cos(THC), (RO + 0.6) * math.sin(THC)])
inward = -C / np.linalg.norm(C); uarm = np.array([inward[1], -inward[0]])   # z x uarm = inward: CCW about P moves the catch inward
P = C - ARM * uarm
def rot(v, a, o=(0, 0)): c, s_ = math.cos(a), math.sin(a); x, y = v[0] - o[0], v[1] - o[1]; return np.array([o[0] + c * x - s_ * y, o[1] + s_ * x + c * y])
def pend_poly():
    pts = []  # hook: radial face at TW0-0.04p (faces the wall), inner edge 0.45 mm above the gap floor, outer edge RO+1.9
    face = TW0 - 0.04 * PITCH; back = TW0 - 0.62 * PITCH
    for i in range(13):
        th = face - (face - back) * i / 12; pts.append(((RI + 0.45 + (RO - RI) * (TW0 - th) / PITCH) * math.cos(th), (RI + 0.45 + (RO - RI) * (TW0 - th) / PITCH) * math.sin(th)))
    for i in range(13):
        th = back + (face - back) * i / 12; pts.append(((RO + 2.0) * math.cos(th), (RO + 2.0) * math.sin(th)))
    hook = Polygon(pts)
    n = np.array([-uarm[1], uarm[0]]); w = 1.35; E = C + 0.4 * uarm
    bar = Polygon([tuple(P - w * n), tuple(E - w * n), tuple(E + w * n), tuple(P + w * n)])
    boss = Point(*P).buffer(2.3, 32)
    arm = unary_union([hook, bar, boss]).buffer(0.25).buffer(-0.25)
    arm = affinity.rotate(arm, -PHI_E, origin=tuple(P), use_radians=True)
    rod = Polygon([(P[0] - 1.1, P[1]), (P[0] + 1.1, P[1]), (P[0] + 1.1, P[1] - LBOB), (P[0] - 1.1, P[1] - LBOB)])
    bob = Point(P[0], P[1] - LBOB).buffer(RBOB, 48)
    return unary_union([arm, rod, bob]), arm
PEND, ARMP = pend_poly()
T = C; U = uarm
def pend_at(phi): return affinity.rotate(ARMP, phi, origin=tuple(P), use_radians=True)
def gear_at(ag): return affinity.rotate(GEAR, ag, origin=(0, 0), use_radians=True)
def hit(phi, ag): return pend_at(phi).intersection(gear_at(ag)).area > 1e-7
# --- inputs ---
def sm(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
T_BRAKE, T_FULL, A_MAX, T_STOP = 2.7, 6.0, 0.8, 8.6     # braking builds from 0 to 0.8 g, car stops at T_STOP
T_ACC0, T_ACC1, A_ACC = 11.8, 13.4, -0.22               # drives off again (accelerating -> bob swings backward)
def a_car(t):  # deceleration in g (positive = braking)
    if T_BRAKE <= t < T_STOP: return A_MAX * sm((t - T_BRAKE) / (T_FULL - T_BRAKE)) * (1 - sm((t - (T_STOP - 0.12)) / 0.12))
    if T_ACC0 <= t < T_ACC1: return A_ACC * math.sin(math.pi * (t - T_ACC0) / (T_ACC1 - T_ACC0))
    return 0.0
V0 = 1.0  # cruise speed (scenery units / s, normalised)
T_PAY, W_PAY = float(os.environ.get('TPAY', '6.85')), 50 * D  # occupant leans into the belt: spool unwinds (clockwise)
T_REW = (10.3, 11.4)
WN, ZETA = 2.6, 0.75        # pendulum (slowed down): natural frequency rad/s, damping
def simulate(fps=240):
    H = 2400; dt = 1 / H; phi = 0.0; om = 0.0; ag = 0.0; locked = False; t_lock = None; ag_lock = 0.0
    frames, events = [], []; nF = round(LOOP * fps); nxt = 0; w = 0.0; s_car = 0.0; v = V0; contact = False
    # car speed: integrate -a; scale so the car stops exactly at T_STOP and is back to V0 at T_ACC1
    ts = np.arange(0, LOOP, dt); acc = np.array([a_car(t) for t in ts])
    brake_area = acc[(ts >= T_BRAKE) & (ts < T_STOP)].sum() * dt; acc_area = -acc[(ts >= T_ACC0) & (ts < T_ACC1)].sum() * dt
    for step in range(round(LOOP * H) + 1):
        t = step * dt
        a = a_car(t)
        if T_BRAKE <= t < T_STOP: v = V0 * (1 - acc[(ts >= T_BRAKE) & (ts < min(t, T_STOP))].sum() * dt / brake_area) if step % 24 == 0 else v
        elif T_STOP <= t < T_ACC0: v = 0.0
        elif T_ACC0 <= t < T_ACC1: v = V0 * (-acc[(ts >= T_ACC0) & (ts < t)].sum() * dt / acc_area) if step % 24 == 0 else v
        elif t >= T_ACC1 or t < T_BRAKE: v = V0
        if nxt < nF and t + 1e-9 >= nxt / fps:
            frames.append({'t': round(nxt / fps, 5), 'phi': phi, 'ag': ag, 'lock': int(locked), 'a': a, 'v': v, 's': s_car, 'w': w, 'c': int(contact)}); nxt += 1
        s_car += v * dt
        # spool command
        if locked: w = 0.0
        elif t_lock is None: w = W_PAY * sm((t - T_PAY) / 0.15) if t >= T_PAY else 0.0
        else:
            r0, r1 = T_REW
            w = ag_lock * (math.pi / 2) / (r1 - r0) * math.sin(math.pi * (t - r0) / (r1 - r0)) if r0 <= t <= r1 else 0.0
        if locked and t >= T_REW[0] and t_lock is not None: locked = False; events.append({'t': t, 'type': 'release'})
        # pendulum dynamics (inertia from car deceleration: equilibrium tan(phi) = a/g), held while locked
        if not locked:
            eq = math.atan(a)
            om += (WN * WN * (eq - phi) - 2 * ZETA * WN * om) * dt
            phiN = phi + om * dt
            if hit(phiN, ag):
                lo, hi = phi, phiN
                if hit(lo, ag):
                    lo = phi
                    while hit(lo, ag) and lo > -0.6: lo -= 0.0005
                for _ in range(30):
                    m = (lo + hi) / 2
                    if hit(m, ag): hi = m
                    else: lo = m
                phiN = lo; om = min(om, 0.0) if phiN >= phi else 0.0; contact = True
            else: contact = False
            phi = phiN
        # spool
        if w != 0.0:
            agN = ag + (-w) * dt  # unwind = clockwise = negative ag
            if hit(phi, agN):
                if w > 0:  # steep face meets the catch -> lock
                    lo, hi = ag, agN
                    for _ in range(40):
                        m = (lo + hi) / 2
                        if hit(phi, m): hi = m
                        else: lo = m
                    agN = lo; locked = True; t_lock = t; ag_lock = agN; w = 0.0; events.append({'t': t, 'type': 'lock', 'ag': agN})
                else:      # rewind: the slope lifts the catch out (pendulum pushed back)
                    p = phi
                    while hit(p, agN) and p > -0.6: p -= 0.0004
                    phi = p; om = min(om, 0.0); events.append({'t': t, 'type': 'lift'}) if not events or events[-1]['type'] != 'lift' else None
            ag = agN
    return frames, events, {'brakeArea': brake_area, 'accArea': acc_area}
if __name__ == '__main__':
    import sys
    fr, ev, info = simulate(240)
    # loop seam: remove the tiny pendulum residual (<0.3 deg) over the last 1.2 s of cruise so frame N == frame 0
    res = fr[-1]['phi']
    for f in fr: f['phi'] -= res * sm((f['t'] - (LOOP - 1.2)) / 1.2)
    lift = [e for e in ev if e['type'] == 'lift']
    evs = [e for e in ev if e['type'] != 'lift'] + ([{'t': lift[0]['t'], 'type': 'liftStart'}, {'t': lift[-1]['t'], 'type': 'liftEnd'}] if lift else [])
    json.dump(fr, open('kin_240.json', 'w')); json.dump(sorted(evs, key=lambda e: e['t']), open('events.json', 'w'), indent=1)
    gp = list(GEAR.exterior.coords)
    json.dump({'N': N, 'RO': RO, 'RI': RI, 'PH': PH, 'P': P.tolist(), 'T': T.tolist(), 'U': U.tolist(), 'ARM': ARM, 'LBOB': LBOB, 'RBOB': RBOB,
               'arm': list(ARMP.exterior.coords), 'gear': gp, 'LOOP': LOOP}, open('geom.json', 'w'))
    phis = [f['phi'] / D for f in fr]
    print('events', json.dumps(evs)[:600]); print('phi range deg', round(min(phis), 2), round(max(phis), 2), 'start/end', round(phis[0], 3), round(phis[-1], 3))
    print('ag end deg', round(fr[-1]['ag'] / D, 4), 'P', P.round(3).tolist(), 'T', T.round(3).tolist())
    for tt in [2.7, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0, 9.0, 10.3, 10.8, 11.2, 11.6, 12.5, 13.4, 14.0, 14.9]:
        f = fr[int(tt * 240)]; print(tt, 'phi', round(f['phi'] / D, 2), 'ag', round(f['ag'] / D, 2), 'lock', f['lock'], 'a', round(f['a'], 3), 'v', round(f['v'], 3), 'c', f['c'])
