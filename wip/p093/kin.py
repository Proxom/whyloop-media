# p093 thermostatic radiator valve "HOW DOES IT KNOW / THE ROOM IS WARM?" - kinematics + HARD GATE 5.2 checks.
# Section diagram, y up, mm. Valve seat = hole x -9..9 in the partition at y -6..0. The disc (thickness 4) sits above the seat;
# disc bottom y = GAP0 - s (s = stem push-down, 0 open .. GAP0 closed). Stem runs up through the bonnet; a collar on the stem is pushed UP by the
# return spring (bonnet floor y 20 -> collar bottom). The wax capsule in the head sits between the fixed head top (CAP_TOP) and the pusher on the
# stem top: capsule length = CAP_TOP - (STEM_TOP0 - s + PUSH_T). Wax grows when warm -> s grows; cools -> spring pushes s back (stroke enlarged x3 for visibility).
import json, math
GAP0 = 8.0; DISC_T = 4.0; SEAT_Y = 0.0; CH_TOP = 14.0
SPR_FLOOR = 20.0; COLLAR0 = 48.0; COLLAR_T = 3.0; BONNET_CAP = 52.0
STEM_TOP0 = 66.0; PUSH_T = 33.0; CAP_TOP = 146.0
SPR_TURNS, SPR_WIRE = 5, 1.0; SPR_BOUND = (SPR_TURNS + 2) * 2 * SPR_WIRE
FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.25, 'hookEnd': 1.0}
T['vo1'] = round(T['vo0'] + dur[0] + 0.3, 3)
GAP = {2: 0.3, 3: 0.3, 4: 0.3, 5: 0.3, 6: 0.4}
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.5, 2); T['LOOP'] = LOOP
T['cutIn'] = round(T['vo1'] + 1.5, 3)
T['warmA'] = T['vo3'] + 0.05; T['warmB'] = T['vo3'] + 0.8          # room warms (thermometer)
T['pushA'] = T['vo3'] + 0.7; T['pushB'] = T['vo4'] + 2.0          # wax grows -> pin down -> valve shuts
T['coolA'] = T['vo5'] + 0.2; T['coolB'] = T['vo5'] + 1.7          # room cools
T['openA'] = T['vo5'] + 0.8; T['openB'] = T['vo5'] + 3.3          # wax shrinks, spring pushes the valve open
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def temp(t):  # 0 cool .. 1 warm
    if t < 0.9: return ease(t / 0.8)
    if t < T['cutIn']: return 1.0 if t < T['hookEnd'] else 0.0
    if t < T['warmA']: return 0.0
    if t < T['coolA']: return ease((t - T['warmA']) / (T['warmB'] - T['warmA']))
    return 1 - ease((t - T['coolA']) / (T['coolB'] - T['coolA']))
def push(t):  # stem push-down s (mm)
    if t < T['hookEnd']: return GAP0 * ease((t - 0.1) / 0.75)
    if t < T['pushA']: return 0.0
    if t < T['openA']: return GAP0 * ease((t - T['pushA']) / (T['pushB'] - T['pushA']))
    return GAP0 * (1 - ease((t - T['openA']) / (T['openB'] - T['openA'])))
rows = []; n = int(round(LOOP * FPS_K)) + 1
for i in range(n):
    t = min(LOOP, i / FPS_K); s = push(t); gap = GAP0 - s
    rows.append([round(t, 4), round(s, 4), round(gap / GAP0, 4), round(temp(t), 4)])
# ---- HARD GATE 5.2 checks (whole loop, 1/120 s) ----
for t, s, f, tp in rows:
    disc_bot = SEAT_Y + GAP0 - s; assert disc_bot >= SEAT_Y - 1e-9, ('disc passes the seat', t)
    assert disc_bot + DISC_T <= CH_TOP - 1, ('disc hits the chamber roof', t)
    collar = COLLAR0 - s; spr = collar - SPR_FLOOR; assert spr > SPR_BOUND, ('spring coil-bound', t, spr)
    assert collar + COLLAR_T <= BONNET_CAP, ('collar hits the cap', t)
    assert STEM_TOP0 - s >= 56.0, ('pusher hits the bonnet cap', t)
    cap_len = CAP_TOP - (STEM_TOP0 - s + PUSH_T); assert cap_len > 20, t
# cause checks: the stem only moves down while the room is warm (or warming), only moves up while the room is cooling/cool; the hook is the same story fast.
for a, b in zip(rows, rows[1:]):
    ds = b[1] - a[1]
    if abs(ds) < 1e-9 or a[0] < T['hookEnd'] or T['hookEnd'] <= a[0] < T['cutIn']: continue
    if ds > 0: assert a[3] > 0.2, ('stem pushed down while cold', a)
    if ds < 0: assert a[3] < 0.8, ('stem rises while warm', a)
# loop seam: the last row equals the first (open, cool)
assert rows[-1][1] == 0 and abs(rows[0][1]) < 1e-6 and rows[-1][3] == 0 and rows[0][3] == 0
geom = dict(T=T, LOOP=LOOP, FPS_K=FPS_K, GAP0=GAP0, DISC_T=DISC_T, SPR_FLOOR=SPR_FLOOR, COLLAR0=COLLAR0, COLLAR_T=COLLAR_T, BONNET_CAP=BONNET_CAP,
            STEM_TOP0=STEM_TOP0, PUSH_T=PUSH_T, CAP_TOP=CAP_TOP, SPR_TURNS=SPR_TURNS, SPR_WIRE=SPR_WIRE)
json.dump(geom, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
cl = [COLLAR0 - r[1] - SPR_FLOOR for r in rows]
print('kin PASS: LOOP', LOOP, 'spring', round(min(cl), 1), '..', round(max(cl), 1), '> bound', SPR_BOUND, '; disc gap 0..', GAP0, '; capsule', CAP_TOP - STEM_TOP0 - PUSH_T, '..', CAP_TOP - STEM_TOP0 - PUSH_T + GAP0)
print(json.dumps(T))
