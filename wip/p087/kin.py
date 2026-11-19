# p087 overhead door closer "WHY DOESN'T / THE DOOR SLAM?" - kinematics + HARD GATE 5.2 checks.
# Outside: door (900 x 2000 x 44 mm) hinged at world x=0,z=0, opens toward +z by angle a. Closer body on the door's pull face, pinion (vertical axis)
# at door-local (PX, PZ); slide arm of fixed length LARM ends in a roller that runs in a track on the frame header (world line z = TZ).
# Arm direction in door-local coords gives the pinion angle beta; the rack on the piston moves x = R_PITCH * (beta - beta0) (rack and pinion).
# Inside diagram (mm): bore x -80..80; piston 70 long; spring from piston right face to the right wall x = 80; oil must pass a tiny hole to let the piston return.
import json, math
PX, PZ, LARM, TZ = 150.0, 45.0, 300.0, 45.0
R_PITCH = 16.0; PIST_L = 70.0; X0 = -40.0; WALL_L, WALL_R = -80.0, 80.0
SPR_TURNS, SPR_WIRE = 7, 2.5; SPR_BOUND = (SPR_TURNS + 2) * 2 * SPR_WIRE
A_OPEN = 100.0; FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0, 'vo1': 1.8}
GAP = {2: 0.3, 3: 0.3, 4: 0.35, 5: 0.3, 6: 0.4}
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.5, 2); T['LOOP'] = LOOP
T['open_a'] = T['vo1'] + 0.1; T['open_b'] = T['vo1'] + 3.0; T['cutIn'] = T['vo1'] + 0.7
T['slam_a'] = T['vo3'] + 0.9; T['slam_b'] = T['slam_a'] + 0.32         # WITHOUT OIL (what-if, outside shot)
T['back'] = T['vo4'] - 0.05                                               # hard cut back inside: door open again (real state)
T['close_a'] = T['vo4'] + 0.6; T['close_b'] = T['vo6'] - 0.25              # WITH OIL: slow close
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def door_angle(t):
    if t < T['hookEnd']: return 28.0 * (1 - ease(t / 0.9)) ** 1.0           # hook: gentle close (with oil)
    if t < T['open_a']: return 0.0
    if t < T['open_b']: return A_OPEN * ease((t - T['open_a']) / (T['open_b'] - T['open_a']))
    if t < T['slam_a']: return A_OPEN
    if t < T['back']:                                                       # what-if: spring alone, accelerating slam
        u = min(1, max(0, (t - T['slam_a']) / (T['slam_b'] - T['slam_a']))); return A_OPEN * (1 - u * u)
    if t < T['close_a']: return A_OPEN
    if t < T['close_b']:                                                    # oil-limited: nearly constant slow speed, soft finish
        u = (t - T['close_a']) / (T['close_b'] - T['close_a']); return A_OPEN * (1 - (0.85 * u + 0.15 * ease(u)))
    return 0.0
def oil_on(t): return 0.0 if (T['vo3'] - 0.05 <= t < T['back']) else 1.0
def flow(t):  # oil pushed through the tiny hole: only while the piston moves back (closing) with oil
    return 1.0 if (oil_on(t) and (T['close_a'] <= t < T['close_b'] or t < 0.9)) else 0.0
def pinion(a):
    ar = math.radians(a); c, s = math.cos(ar), math.sin(ar)
    Px, Pz = PX * c - PZ * s, PX * s + PZ * c
    Rx = Px + math.sqrt(LARM ** 2 - (TZ - Pz) ** 2); Rz = TZ
    lx, lz = Rx * c + Rz * s, -Rx * s + Rz * c                            # roller in door-local coords
    return math.atan2(lz - PZ, lx - PX), (Rx, Rz)
B0 = pinion(0.0)[0]
rows = []; n = int(round(LOOP * FPS_K)) + 1
for i in range(n):
    t = min(LOOP, i / FPS_K); a = door_angle(t); b, (rx, rz) = pinion(a)
    x = X0 + R_PITCH * (B0 - b)          # opening turns the pinion clockwise in local coords -> rack/piston moves +x
    rows.append([round(t, 4), round(a, 4), round(b, 6), round(x, 4), round(rx, 3), oil_on(t), flow(t)])
# ---- HARD GATE 5.2 checks ----
xs = [r[3] for r in rows]; ang = [r[1] for r in rows]
xmin, xmax = min(xs), max(xs)
assert xmin - PIST_L / 2 >= WALL_L - 1e-6, 'piston passes the left end'
spr = [WALL_R - (x + PIST_L / 2) for x in xs]; assert min(spr) > SPR_BOUND, ('spring coil-bound', min(spr), SPR_BOUND)
# rack-pinion consistency + monotonic: piston position is a strictly increasing function of door angle
pairs = sorted(set((round(r[1], 3), r[3]) for r in rows)); 
for (a1, x1), (a2, x2) in zip(pairs, pairs[1:]):
    if a2 > a1 + 1e-6: assert x2 > x1 - 1e-6, ('piston not monotonic in door angle', a1, a2)
for r in rows: assert abs(r[3] - (X0 + R_PITCH * (B0 - r[2]))) < 1e-3
# arm length constant (roller on the track)
for r in rows[::7]:
    a = math.radians(r[1]); Px, Pz = PX * math.cos(a) - PZ * math.sin(a), PX * math.sin(a) + PZ * math.cos(a)
    assert abs(math.hypot(r[4] - Px, TZ - Pz) - LARM) < 0.01
# nothing moves without a cause: the door only closes while the spring is compressed (piston right of its rest) and only opens in the push window
for r0, r1 in zip(rows, rows[1:]):
    if r1[1] > r0[1] + 1e-9: assert T['open_a'] <= r1[0] <= T['open_b'] + 1e-6 or r1[0] >= T['back'] - 0.01 and r0[0] < T['back'], ('door opens without a push', r1[0])
    if r1[1] < r0[1] - 1e-9: assert r0[3] > X0 + 1e-6 or r0[0] < T['hookEnd'], ('door closes without spring force', r1[0])
# with oil: max closing speed limited; without oil: much faster
def vmax(t0, t1): return max(abs(r1[1] - r0[1]) * FPS_K for r0, r1 in zip(rows, rows[1:]) if t0 <= r0[0] < t1)
v_oil, v_slam = vmax(T['close_a'], T['close_b']), vmax(T['slam_a'], T['slam_b'])
assert v_slam > 8 * v_oil, (v_slam, v_oil)
print('PASS piston x %.1f..%.1f (stroke %.1f mm), pinion turn %.1f deg, spring %.1f..%.1f (bound %.1f), door speed oil %.0f deg/s vs no oil %.0f deg/s' % (
    xmin, xmax, xmax - xmin, math.degrees(B0 - min(r[2] for r in rows)), min(spr), max(spr), SPR_BOUND, v_oil, v_slam))
json.dump(rows, open('kin.json', 'w'), separators=(',', ':'))
json.dump({'T': T, 'LOOP': LOOP, 'FPS_K': FPS_K, 'PX': PX, 'PZ': PZ, 'LARM': LARM, 'TZ': TZ, 'R_PITCH': R_PITCH, 'PIST_L': PIST_L, 'X0': X0, 'SPR_TURNS': SPR_TURNS, 'SPR_WIRE': SPR_WIRE, 'B0': B0}, open('geom.json', 'w'), indent=1)
print(json.dumps(T))
