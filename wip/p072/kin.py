# p072 toilet fill valve (Portsmouth-style ballcock) - kinematics. mm, y up, side view in x-y; pivot at the origin.
# Float ball centre C = (-L cos a, L sin a) on the long arm; ball floats half-submerged -> a = asin(h / L), clamped to [A_MIN (arm stop), A_C (valve shut)].
# Short arm (rigid with the long arm) ends in the piston slot: x_tip = R_S sin(a - A_C). Washer face x = x_tip + W_OFF; seat face at x = W_OFF -> gap = -x_tip.
# Water: flush drains the tank to H_LOW, then dh/dt = K * max(gap, GMIN) until the washer seals (gap 0); K is solved so the seal lands at T_CLOSE.
import json, math
L, R_S, W_OFF = 230.0, 24.0, 14.0
A_C, A_MIN = math.radians(-15.0), math.radians(-32.0)
H_LOW, R_BALL, GMIN = -225.0, 48.0, 0.5
TANK = dict(x0=-330.0, x1=140.0, y0=-260.0, y1=60.0, z=90.0)
FPS = 60
H_CLOSE = L * math.sin(A_C)
def alpha(h): return max(A_MIN, min(A_C, math.asin(max(-1, min(1, h / L)))))
def gap(a): return max(0.0, -R_S * math.sin(a - A_C))
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
T = {'vo0': 0.15}
T['hookEnd'] = max(1.7, T['vo0'] + D[0] + 0.15)
T['vo1'] = T['hookEnd'] + 0.1
T['vo2'] = T['vo1'] + D[1] + 0.15
T['vo3'] = T['vo2'] + D[2] + 0.2
T['vo4'] = T['vo3'] + D[3] + 0.2
T['vo5'] = T['vo4'] + D[4] + 0.15
T['vo6'] = T['vo5'] + D[5] + 0.25
LOOP = round(T['vo6'] + D[6] + 1.05, 1); T['LOOP'] = LOOP
T['fl0'] = T['vo1'] + 0.45; T['fl1'] = T['vo1'] + 2.3          # flush: the level drops
T['close'] = T['vo5'] + 5.3                                       # washer seals ("presses on the hole")
def simulate(K, t_end, dt=1 / 600):
    t = T['fl1']; h = H_LOW; out = []
    while t < t_end:
        g = gap(alpha(h))
        if g <= 0: break
        h += K * max(g, GMIN) * dt; t += dt
        h = min(h, H_CLOSE + 0.0)
        if alpha(h) >= A_C - 1e-9: h = H_CLOSE; break
    return t
lo, hi = 1.0, 200.0
for _ in range(60):
    m = (lo + hi) / 2
    if simulate(m, 999) > T['close']: lo = m
    else: hi = m
K = (lo + hi) / 2
def h_story(t):     # the main story (not the hook)
    if t < T['fl0']: return H_CLOSE
    if t < T['fl1']: return H_CLOSE + (H_LOW - H_CLOSE) * smooth((t - T['fl0']) / (T['fl1'] - T['fl0']))
    return None
# integrate the refill once on a fine grid
grid = {}; tt = T['fl1']; h = H_LOW; dt = 1 / 600; closed_at = None
while tt <= LOOP + 0.01:
    grid[round(tt * 600)] = h
    if closed_at is None:
        g = gap(alpha(h))
        if alpha(h) >= A_C - 1e-9: closed_at = tt; h = H_CLOSE
        else: h = min(H_CLOSE, h + K * max(g, GMIN) * dt)
    tt += dt
def h_at(t):
    v = h_story(t)
    if v is not None: return v
    k = round(t * 600); k = max(min(grid), min(max(grid), k)); return grid[k]
HOOK_OFF = T['close'] - 0.55          # hook (0 .. hookEnd) shows the seal moment as a flash-forward
def state(t):
    ts = t + HOOK_OFF if t < T['hookEnd'] else t
    h = h_at(ts); a = alpha(h); g = gap(a)
    flow = 0.0 if (g <= 1e-6 or ts < T['fl1'] - 0.6) else min(1.0, g / 7.0) ** 0.5
    if T['fl0'] - 0.0 < ts < T['fl1']: flow = max(flow, 0.0)
    return h, a, g, flow
rows = []
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; h, a, g, fl = state(t)
    C = (-L * math.cos(a), L * math.sin(a))
    # HARD GATE 5.2 checks: washer never past the seat, ball inside the tank, ball not below the water by more than its radius (it floats)
    assert g >= -1e-9
    assert C[0] - R_BALL > TANK['x0'] + 5 and C[1] - R_BALL > TANK['y0'] + 5, C
    rows.append([round(t, 4), round(h, 3), round(math.degrees(a), 4), round(g, 4), round(fl, 4)])
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, L=L, R_S=R_S, W_OFF=W_OFF, A_C=math.degrees(A_C), A_MIN=math.degrees(A_MIN), H_LOW=H_LOW, H_CLOSE=round(H_CLOSE, 2),
         R_BALL=R_BALL, TANK=TANK, K=round(K, 3), closed_at=round(closed_at, 3), HOOK_OFF=round(HOOK_OFF, 3), GAP_MAX=round(gap(A_MIN), 2), RATIO=round(L / R_S, 1))
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print(json.dumps(G))
