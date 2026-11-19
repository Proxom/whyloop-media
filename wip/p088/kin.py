# p088 trunk gas strut "WHAT HOLDS / THE TRUNK OPEN?" - kinematics + HARD GATE 5.2 checks (side view, mm, y up, x = rearward)
# Hatch lid hinged at H; lid direction d(a) = (sin a, -cos a) (a = 0 closed, hanging down; a = A_OPEN open).
# Strut: tube end fixed on the body at B, rod end on the lid at P = H + LM * d(a). Strut length L = |P - B| = tube length + exposed rod.
# Piston (on the rod's inner end) sits inside the tube at depth = ROD - exposed from the seal; must stay inside the tube.
import json, math
import numpy as np
H = (0.0, 1000.0); LM = 300.0; B = (-60.0, 200.0); A_OPEN = math.radians(80)
TUBE = 420.0; ROD = 480.0; PIST = 14.0           # tube length, rod length, piston thickness
FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'pop0': 0.1, 'pop1': 0.9, 'hookEnd': 1.0, 'vo0': 1.0}
T['vo1'] = T['vo0'] + dur[0] + 0.55; T['cut'] = T['vo1'] - 0.3
T['vo2'] = T['vo1'] + dur[1] + 0.35
T['vo3'] = T['vo2'] + dur[2] + 0.35
T['vo4'] = T['vo3'] + dur[3] + 0.35
T['vo5'] = T['vo4'] + dur[4] + 0.45; T['ext'] = T['vo5'] - 0.2
LOOP = round(T['vo5'] + dur[5] + 2.2, 2); T['LOOP'] = LOOP
T['close_a'] = LOOP - 1.35; T['close_b'] = LOOP - 0.25     # a hand pushes the lid shut at the end (loop back to closed)
sm = lambda x: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, x)))
def ang(t):
    if t < T['pop0']: return 0.0
    if t < T['pop1']: return A_OPEN * sm((t - T['pop0']) / (T['pop1'] - T['pop0']))
    if t < T['close_a']: return A_OPEN
    if t < T['close_b']: return A_OPEN * (1 - sm((t - T['close_a']) / (T['close_b'] - T['close_a'])))
    return 0.0
def P(a): return (H[0] + LM * math.sin(a), H[1] - LM * math.cos(a))
rows = []
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; a = ang(t); p = P(a); L = math.hypot(p[0] - B[0], p[1] - B[1]); ex = L - TUBE; depth = ROD - ex
    rows.append([round(t, 5), round(a, 6), round(L, 4), round(ex, 4), round(depth, 4)])
json.dump(rows, open('kin.json', 'w'))
# ---------------- HARD GATE 5.2 checks ----------------
L = np.array([r[2] for r in rows]); dep = np.array([r[4] for r in rows]); ex = np.array([r[3] for r in rows]); tt = np.array([r[0] for r in rows]); aa = np.array([r[1] for r in rows])
print('strut length %.1f .. %.1f, exposed rod %.1f .. %.1f, piston depth %.1f .. %.1f (tube %.0f)' % (L.min(), L.max(), ex.min(), ex.max(), dep.min(), dep.max(), TUBE))
assert dep.max() <= TUBE - PIST - 5, 'piston passes the closed tube end'
assert dep.min() >= 20, 'piston passes the seal / guide at the rod end'
assert ex.min() > 30, 'rod end fitting hits the tube'
# rod length = tube + exposed rod - consistent with the lid geometry (checked by construction above): both ends stay on their mounts
# nothing moves without a cause: the lid only rises when it is released (hook pop) and only closes while the hand pushes it
da = np.diff(aa)
for i in np.where(da > 1e-9)[0]: assert T['pop0'] - 1/FPS_K <= tt[i] <= T['pop1'], ('lid rose outside the release', tt[i])
for i in np.where(da < -1e-9)[0]: assert T['close_a'] - 1/FPS_K <= tt[i] <= T['close_b'], ('lid closed without a push', tt[i])
assert abs(aa[0] - aa[-1]) < 1e-9
print('checks PASS; LOOP %.2f' % LOOP)
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, H=H, LM=LM, B=B, A_OPEN=A_OPEN, TUBE=TUBE, ROD=ROD, PIST=PIST)
json.dump(G, open('geom.json', 'w'), indent=1)
print({k: round(v, 2) for k, v in T.items()})
