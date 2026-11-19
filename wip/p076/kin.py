# p076 flint lighter "WHERE DOES THE SPARK / COME FROM?" - kinematics, timeline, spark list, clearance checks.
# Side section, mm: x to the back of the lighter (the wheel side), y up, z toward the camera. Wheel axis = z.
# Principle: a spring pushes the ferrocerium "flint" up against a rough (knurled) hardened-steel wheel; turning the wheel
# scrapes tiny bits off the flint; friction makes them hot and, because cerium ignites at only 150-180 C, they burn in air = sparks.
import json, math, random
random.seed(76)
# ---------- geometry ----------
WX, WY = 4.5, 80.0                 # wheel centre
STR_Z, STR_M, STR_W = 48, 0.15, 3.2  # striker wheel: knurl teeth (kit spurGear outline), width (z)
RA = STR_M * (STR_Z + 2) / 2       # tooth-tip radius 3.8
DISC_Z, DISC_M, DISC_W = 44, 0.24, 2.2
DISC_RA = DISC_M * (DISC_Z + 2) / 2  # thumb disc tip radius 5.4
DISC_Z0 = STR_W / 2 + 0.15         # inner face of each thumb disc (|z|)
FL_R, FL_L = 1.25, 5.0             # flint rod radius, length
FL_TOP = WY - RA                   # flint top touches the tooth-tip circle (76.2)
TUBE_RI, TUBE_RO, TUBE_Y0, TUBE_Y1 = 1.4, 1.85, 56.0, FL_TOP - 2.5   # flint tube; the flint sticks out 2.5 mm
SPR_Y0 = TUBE_Y0 + 1.0             # spring seat (tube floor)
NOZ_X, NOZ_R, NOZ_TOP = -5.0, 1.6, 77.0
PIV = (-8.6, 70.6)                 # gas lever pivot; pad at x = -12.4, fork at the nozzle stem (x = -5)
PAD_X = -12.4
LIFT = 0.8                         # nozzle (valve stem) lift when the pad is fully pressed (mm)
# ---------- timeline (video seconds) ----------
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
GAP = [0, 0.1, 0.35, 0.35, 0.35, 0.35, 0.6]
T = {'vo0': 0.15}; T['hookEnd'] = round(T['vo0'] + D[0] + 0.2, 3); T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + D[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + D[6] + 1.3, 1); T['LOOP'] = LOOP
T['roll1'] = round(T['vo1'] + 0.55, 3)          # the thumb roll in step "roll the wheel"
T['lit1'] = round(T['roll1'] + 0.12, 3)          # the gas catches
T['out1'] = round(T['vo2'] - 0.35, 3)            # pad released -> flame out
T['lit2'] = round(T['vo5'] + D[5] - 0.2, 3)      # sparks light the gas at the end of step 4
T['tail'] = round(LOOP - 0.9, 3)                 # back to the hook state (slow-mo spray + flame)
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def win(t, a, b, f=0.3): return min(smooth((t - a) / f), 1 - smooth((t - b + f) / f))
SM_HOOK, SM_SCRAPE, SM_SPARK = 0.3, 0.12, 0.15
def sf(t):                               # time stretch: scene seconds per video second
    if t < T['hookEnd'] - 0.15: return SM_HOOK
    if t < T['hookEnd'] + 0.1: return SM_HOOK + (1 - SM_HOOK) * smooth((t - T['hookEnd'] + 0.15) / 0.25)
    w3 = win(t, T['vo3'] - 0.1, T['vo4'] - 0.1, 0.35); w5 = win(t, T['vo5'] - 0.1, T['lit2'] + 0.05, 0.35)
    base = 1 - (1 - SM_SCRAPE) * w3 - (1 - SM_SPARK) * w5
    if t > T['tail']: base = base + (SM_HOOK - base) * smooth((t - T['tail']) / 0.35)
    return base
W_ROLL = 12.0                            # real wheel speed during a thumb roll (rad/s, scene time); turns clockwise: bottom edge moves to -x (toward the nozzle)
def omega(t):                            # scene-time angular speed (rad per scene second), negative = clockwise
    on = 0.0
    if t < T['hookEnd'] - 0.05: on = 1.0
    if T['roll1'] <= t < T['roll1'] + 0.2: on = smooth((t - T['roll1']) / 0.03) * (1 - smooth((t - T['roll1'] - 0.14) / 0.06))
    on = max(on, win(t, T['vo3'] + 0.2, T['vo4'] - 0.15, 0.3))
    on = max(on, win(t, T['vo5'] + 0.15, T['lit2'] + 0.1, 0.2))
    if t > T['tail']: on = max(on, smooth((t - T['tail']) / 0.3))
    return -W_ROLL * on
def lever(t):                            # pad pressed 0..1
    p = 0.0
    if t < T['hookEnd']: p = 1.0
    p = max(p, win(t, T['roll1'] - 0.05, T['out1'], 0.12))
    p = max(p, win(t, T['lit2'] - 0.35, T['vo6'] + 1.5, 0.15))
    if t > T['tail'] - 0.4: p = max(p, smooth((t - T['tail'] + 0.4) / 0.15))
    return p
def flame(t):                            # flame level 0..1 (needs gas + a spark)
    if t < T['hookEnd']: return 1.0
    f = 0.0
    if T['lit1'] <= t < T['out1'] + 0.12: f = smooth((t - T['lit1']) / 0.12) * (1 - smooth((t - T['out1']) / 0.12))
    if T['lit2'] <= t < T['vo6'] + 1.62: f = smooth((t - T['lit2']) / 0.12) * (1 - smooth((t - T['vo6'] - 1.5) / 0.12))
    if t > T['tail'] - 0.2: f = max(f, smooth((t - T['tail'] + 0.2) / 0.15))
    return f
FPS = 60; N = int(LOOP * FPS) + 1
rows = []; tau = 0.0; phi = 0.0; sparks = []; acc = 0.0
PER_RAD = 18.0
for i in range(N):
    t = i / FPS; s = sf(t); w = omega(t); lv = lever(t); fl = flame(t)
    rows.append([round(t, 4), round(tau, 5), round(phi, 5), round(lv, 4), round(fl, 4), round(s, 4)])
    dtau = s / FPS; dphi = w * dtau
    # sparks: scraped bits leave the contact patch, thrown forward (-x) by the bottom edge of the wheel
    acc += abs(dphi) * PER_RAD
    cold = T['vo3'] - 0.2 < t < T['vo4'] + 0.2                       # step 2: show the scraped bits before they glow
    heat = T['vo5'] - 0.2 < t < T['lit2'] + 0.3                      # step 4: the bits heat up and catch fire (slowed down)
    while acc >= 1.0:
        acc -= 1.0; te = tau + random.random() * dtau
        if cold: sp, life, dly = random.uniform(70, 140), random.uniform(0.5, 0.8), 0.0
        elif heat: sp, life, dly = random.uniform(60, 120), random.uniform(0.45, 0.7), random.uniform(0.04, 0.07)
        else: sp, life, dly = random.uniform(220, 420), random.uniform(0.16, 0.32), 0.006
        a = math.radians(random.uniform(4, 34)); b = math.radians(random.uniform(-12, 12))
        v = [-sp * math.cos(a) * math.cos(b), sp * math.sin(a), sp * math.cos(a) * math.sin(b)]
        p0 = [WX - 0.5 + random.uniform(-0.3, 0.3), FL_TOP + 0.15, random.uniform(-1.2, 1.2)]
        sparks.append([round(te, 5), [round(x, 3) for x in p0], [round(x, 2) for x in v], round(life, 3), 0 if cold else 1, round(dly, 3), round(random.uniform(0.6, 1.3), 2)])
    tau += dtau; phi += dphi
# loop seam: the wheel pattern repeats every 90 deg (48 knurl teeth, 44 disc ribs -> 360/gcd = 90 deg): scale phi so the end angle is a multiple of 90 deg
Q = math.pi / 2; tgt = round(phi / Q) * Q; kf = tgt / phi
for r in rows: r[2] = round(r[2] * kf, 5)
assert abs(kf - 1) < 0.01, kf
# ---------- checks (HARD GATE 5.2) ----------
# 1. no tooth enters the flint: every point of the striker outline is within RA of the centre, the flint top plane is RA below it
assert abs((WY - FL_TOP) - RA) < 1e-9
# 2. flint (r 1.25) clear of the thumb discs (inner faces at |z| = 1.75); tube top clear of the discs (disc bottom y = WY - DISC_RA)
assert FL_R < DISC_Z0 - 0.3, 'flint touches discs'
assert TUBE_Y1 < WY - DISC_RA - 0.3, ('tube hits discs', TUBE_Y1, WY - DISC_RA)
# 3. nozzle clear of the thumb discs in x
assert NOZ_X + NOZ_R < WX - DISC_RA - 0.5, 'nozzle hits discs'
# 4. sparks leave in front of the wheel (never back through the flint/wheel): vx < 0 and they start outside the tube
assert all(s[2][0] < 0 for s in sparks)
# 5. spark direction matches the wheel: bottom edge velocity = omega x r at (0,-RA) -> vx = omega*RA... with omega < 0 -> vx < 0
assert all(r for r in [omega(0.5) < 0])
G = dict(TAU_END=round(tau, 5), LOOP=LOOP, T=T, FPS_K=FPS, WX=WX, WY=WY, RA=RA, STR_Z=STR_Z, STR_M=STR_M, STR_W=STR_W, DISC_Z=DISC_Z, DISC_M=DISC_M, DISC_W=DISC_W, DISC_RA=DISC_RA, DISC_Z0=DISC_Z0,
         FL_R=FL_R, FL_L=FL_L, FL_TOP=FL_TOP, TUBE_RI=TUBE_RI, TUBE_RO=TUBE_RO, TUBE_Y0=TUBE_Y0, TUBE_Y1=TUBE_Y1, SPR_Y0=SPR_Y0, NOZ_X=NOZ_X, NOZ_R=NOZ_R, NOZ_TOP=NOZ_TOP,
         PIV=PIV, PAD_X=PAD_X, LIFT=LIFT)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w')); json.dump(sparks, open('sparks.json', 'w'))
print('PASS', {k: T[k] for k in T}, 'sparks', len(sparks), 'cold', sum(1 for s in sparks if s[4] == 0), 'tau end', round(tau, 3), 'kf', round(kf, 5), 'phi end', round(phi, 2))
