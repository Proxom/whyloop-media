# p091 window blind cord lock "WHY DOESN'T / THE BLIND FALL?" - kinematics + HARD GATE 5.2 checks.
# Cord lock (side view, mm, y up, +x = outer end of the headrail, -x = toward the middle of the window):
#   fixed smooth GUIDE pin G at (0,0) r 4.5; floating toothed ROLLER r 5.0 whose axle runs in a slanted SLOT from B (bottom, wide gap)
#   to A (top, narrow gap). The cord comes along the headrail from the blind (-x), passes over G, through the gap, out of the exit hole.
# Physics: the roller sits between the slot wall and the cord -> when the cord moves and touches it, it ROLLS: centre speed = cord speed / 2.
#   Cord up (blind's weight) -> roller rolls up the slot -> gap shrinks -> cord pinched between roller and guide -> stops (LOCK).
#   Cord pulled down -> roller rolls down to the wide end (free). Cord pulled toward the middle -> cord path misses the roller -> runs free.
# c = cord pulled out (mm) = blind rise (lift cords); the blind's bottom rail y = YB0 + c.
import json, math
RG, RR, RC = 4.5, 5.0, 1.2           # guide radius, roller radius, cord radius
SQ = 1.7                            # pinched cord thickness (2.4 -> 1.7 mm)
B = (13.0, -12.0); A = (10.2, -3.6)  # slot ends (roller centre)
EV = (15.0, -26.0); EC = (-2.0, -26.0)   # exit point: cord hanging normally (lock is tilted, cord rests on the roller) / pulled toward the middle
ENTRY_X = -46.0; FPS = 30; FK = 240
LS = math.dist(A, B)
def P_of(u): return (B[0] + (A[0] - B[0]) * u, B[1] + (A[1] - B[1]) * u)
def gap(u): return math.hypot(*P_of(u)) - RG - RR
lo, hi = 0.0, 1.0
for _ in range(60):
    m = (lo + hi) / 2
    (lo, hi) = (m, hi) if gap(m) > SQ else (lo, m)
U_LOCK = lo; L_LOCK = 2 * LS * U_LOCK      # cord travel from bottom to lock
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'vo1': 2.75}
GAP = {2: 0.35, 3: 0.35, 4: 0.3, 5: 1.85, 6: 1.25}
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.45, 2); T['LOOP'] = LOOP
T['cutIn'] = T['vo1'] - 0.15; T['outEnd'] = T['vo6'] - 0.05
C_HOOK = 40.0; PULL = 100.0
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
# --- schedule: (t0, t1, kind, c0, c1) ---
T['hp0'], T['hp1'] = 0.05, 0.40                  # hook: quick pull down (roller already at the bottom, spins)
T['hl0'], T['hl1'] = 0.48, 0.80                  # hook: let go -> rolls up -> LOCK
c1 = C_HOOK - L_LOCK
T['pd0'], T['pd1'] = T['vo2'] + 0.25, T['vo3'] - 0.35   # PULL DOWN (blind rises)
c2 = c1 + PULL
T['lg0'] = T['vo3'] + 0.9; T['lg1'] = T['vo4'] + dur[4] - 0.35   # LET GO, slow motion lock-up; LOCK lands on 'pinched', then ~1.8 s hold
c3 = c2 - L_LOCK
T['rp0'], T['rp1'] = T['vo5'] + 0.05, T['vo5'] + 0.45          # release: small pull down unpinches
T['rm0'], T['rm1'] = T['vo5'] + 0.5, T['vo5'] + 1.5            # cord moved toward the middle: it leaves the roller
T['rf0'], T['rf1'] = T['vo5'] + 1.7, T['vo5'] + 2.3            # then the roller falls (gravity) to the wide end
c4 = c3 + 3.0
T['ld0'], T['ld1'] = T['vo5'] + 2.45, T['vo6'] + 0.6           # cord runs up freely: blind lowers to the start height
T['rb0'], T['rb1'] = T['vo6'] + 0.9, T['vo6'] + 1.5            # cord swings back to hanging (outside shot)
def cord(t):
    if t < T['hp0']: return 0.0
    if t < T['hp1']: return C_HOOK * ease((t - T['hp0']) / (T['hp1'] - T['hp0']))
    if t < T['hl0']: return C_HOOK
    if t < T['hl1']: return C_HOOK - L_LOCK * ease((t - T['hl0']) / (T['hl1'] - T['hl0']))
    if t < T['pd0']: return c1
    if t < T['pd1']: return c1 + PULL * ease((t - T['pd0']) / (T['pd1'] - T['pd0']))
    if t < T['lg0']: return c2
    if t < T['lg1']:
        u = (t - T['lg0']) / (T['lg1'] - T['lg0']); return c2 - L_LOCK * (0.5 * u + 0.5 * ease(u))   # slow-motion, steady
    if t < T['rp0']: return c3
    if t < T['rp1']: return c3 + 3.0 * ease((t - T['rp0']) / (T['rp1'] - T['rp0']))
    if t < T['ld0']: return c4
    if t < T['ld1']: return c4 * (1 - ease((t - T['ld0']) / (T['ld1'] - T['ld0'])))
    return 0.0
def mode(t):
    if t < T['rm0']: return 0.0
    if t < T['rm1']: return ease((t - T['rm0']) / (T['rm1'] - T['rm0']))
    if t < T['rb0']: return 1.0
    if t < T['rb1']: return 1 - ease((t - T['rb0']) / (T['rb1'] - T['rb0']))
    return 0.0
# ---------- taut cord geometry ----------
def wrap_pts(cx, cy, R, a0, a1, n):
    return [(cx + R * math.cos(a0 + (a1 - a0) * k / n), cy + R * math.sin(a0 + (a1 - a0) * k / n)) for k in range(n + 1)]
def seg_dist(p, a, b):
    ax, ay = a; bx, by = b; px, py = p; dx, dy = bx - ax, by - ay; L2 = dx * dx + dy * dy
    s = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L2)); return math.hypot(px - ax - s * dx, py - ay - s * dy)
def cord_path(u, m):
    P = P_of(u); g = gap(u); rce = min(RC, g / 2); Rg, Rp = RG + rce, RR + rce
    E = (EV[0] + (EC[0] - EV[0]) * m, EV[1] + (EC[1] - EV[1]) * m)
    bE = math.atan2(E[1], E[0]); dE = math.hypot(*E); aT = bE + math.acos(Rg / dE)    # cw wrap on G, tangent to E
    TG = (Rg * math.cos(aT), Rg * math.sin(aT))
    contact = seg_dist(P, TG, E) < Rp
    pts = [(ENTRY_X, Rg), (-12, Rg)]
    if not contact:
        pts += wrap_pts(0, 0, Rg, math.pi / 2, aT, 14)[0:]; pts.append(E)
    else:
        d = (P[0], P[1]); D = math.hypot(*d); ph = math.atan2(d[1], d[0]) + math.acos(min(1.0, (Rg + Rp) / D))
        TP = (P[0] - Rp * math.cos(ph), P[1] - Rp * math.sin(ph))
        pts += wrap_pts(0, 0, Rg, math.pi / 2, ph, 14)
        bP = math.atan2(E[1] - P[1], E[0] - P[0]); dP = math.hypot(E[0] - P[0], E[1] - P[1]); gam = bP - math.acos(Rp / dP)
        s0 = ph + math.pi
        while gam < s0: gam += 2 * math.pi
        while gam - s0 > 2 * math.pi: gam -= 2 * math.pi
        pts += wrap_pts(P[0], P[1], Rp, s0, gam, 10); pts.append(E)
    # below the exit hole the cord hangs straight down (as in the outside shot), or toward the middle when pulled there
    dx, dy = -0.45 * m, -1.0; L = math.hypot(dx, dy); x1, y1 = pts[-1]
    pts.append((x1 + dx / L * 2.0 - 0.0, y1 + dy / L * 2.0)); pts.append((x1 + dx / L * 40, y1 + dy / L * 40))
    return pts, contact, rce
def resample(pts, n=110):
    acc = [0.0]
    for a, b in zip(pts, pts[1:]): acc.append(acc[-1] + math.dist(a, b))
    out = []; j = 0
    for k in range(n):
        s = acc[-1] * k / (n - 1)
        while j < len(acc) - 2 and acc[j + 1] < s: j += 1
        l = acc[j + 1] - acc[j]; v = 0 if l < 1e-9 else (s - acc[j]) / l
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * v, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * v))
    return out
# ---------- integrate roller state at FK Hz ----------
n = int(round(LOOP * FK)) + 1
u = 0.0; ang = 0.0; rows = []; prev_c = cord(0.0); log = []
for i in range(n):
    t = min(LOOP, i / FK); c = cord(t); m = mode(t); dc = c - prev_c; prev_c = c   # dc > 0: cord pulled down
    _, contact, _ = cord_path(u, m)
    du = 0.0; dang = 0.0; cause = ''
    if T['rf0'] <= t < T['rf1'] and u > 0:      # gravity drop after the small unpinching pull
        du = -min(u, U_LOCK / ((T['rf1'] - T['rf0']) * FK)); cause = 'gravity'
    elif contact and abs(dc) > 0:
        if dc < 0:                               # cord moving up: rolls the roller up the slot
            du = min(U_LOCK - u, -dc / 2 / LS); dang = -(-dc) / (2 * RR)   # rolling between wall and cord
            cause = 'cord up'
        else:                                    # cord pulled down: rolls it down; at the bottom it just spins
            du = -min(u, dc / 2 / LS); dang = dc / (2 * RR) if u > 0 else dc / RR; cause = 'cord down'
    u = max(0.0, min(U_LOCK, u + du)); ang += dang
    locked = u >= U_LOCK - 1e-6
    log.append((t, c, dc, u, du, contact, locked, m, cause))
    if i % (FK // FPS) == 0:
        pts, ct, rce = cord_path(u, m); P = P_of(u)
        rows.append([round(t, 4), round(c, 3), round(u, 5), round(ang, 4), round(m, 4), int(ct), int(locked), round(P[0], 3), round(P[1], 3), round(gap(u), 3),
                     [round(v, 2) for p in resample(pts) for v in p]])
# ---------- HARD GATE 5.2 checks ----------
for (t, c, dc, u_, du, ct, lk, m, cause) in log:
    P = P_of(u_); g = gap(u_)
    assert g >= SQ - 1e-6, ('roller passes into the guide', t, g)
    assert 0 <= u_ <= U_LOCK + 1e-9                     # roller stays in its slot
    if du > 1e-12: assert ct and dc < 0, ('roller moves up without the cord dragging it', t)
    if du < -1e-12: assert (ct and dc > 0) or cause == 'gravity', ('roller moves down without a cause', t)
    if m <= 1e-6: assert ct, ('cord should rest on the roller when hanging', t)
    if m >= 0.999: assert not ct, ('cord pulled to the middle must miss the roller', t)
# lock really stops the cord: once locked in hanging mode, the cord never moves up
for a, b in zip(log, log[1:]):
    if a[6] and a[7] < 0.5 and b[1] < a[1] - 1e-9: raise AssertionError(('cord moves up while pinched', b[0]))
# cord moves up only while the blind's weight can pull it (not locked) and down only while pulled
assert abs(cord(LOOP) - cord(0)) < 1e-9 and mode(LOOP) == mode(0)
u_end = log[-1][3]; assert u_end < 1e-6, ('roller must end at the wide end for the loop', u_end)
# cord vs roller/guide overlap: cord centreline keeps >= squashed half-thickness from both surfaces
for r in rows:
    P = (r[7], r[8]); pts = list(zip(r[10][0::2], r[10][1::2]))
    for a, b in zip(pts, pts[1:]):
        assert seg_dist((0, 0), a, b) >= RG + SQ / 2 - 0.12, ('cord into guide', r[0])
        assert seg_dist(P, a, b) >= RR + SQ / 2 - 0.12, ('cord into roller', r[0])
print('PASS: slot %.2f mm, lock at u=%.3f (gap %.2f mm, cord 2.4 -> %.1f), free gap %.2f mm, lock-up cord travel %.1f mm; c %.1f..%.1f mm' % (
    LS, U_LOCK, gap(U_LOCK), SQ, gap(0), L_LOCK, min(l[1] for l in log), max(l[1] for l in log)))
json.dump(rows, open('kin.json', 'w'), separators=(',', ':'))
json.dump({'T': T, 'LOOP': LOOP, 'FPS': FPS, 'RG': RG, 'RR': RR, 'RC': RC, 'A': A, 'B': B, 'U_LOCK': U_LOCK, 'L_LOCK': L_LOCK, 'EV': EV, 'EC': EC, 'ENTRY_X': ENTRY_X,
           'C_HOOK': C_HOOK, 'PULL': PULL}, open('geom.json', 'w'), indent=1)
print(json.dumps({k: round(v, 2) for k, v in T.items()}))
