# p106 pressure cooker weight (jiggler) kinematics + HARD GATE 5.2 checks. Units mm, pot axis = +y, pot bottom at y 0.
# Rows: [t, h (weight lift above its seat), tilt (deg, exterior only), p (steam push / weight, 1.0 = lift threshold)]
import json, math
FPS_K = 120
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.15, cutIn=2.3, vo1=2.5, s2=6.9, vo2=7.0, s3=11.0, vo3=11.2, liftA=12.6, liftB=13.0, s4=15.0, vo4=15.2, dropA=15.6, dropB=15.95,
         outA=19.8, ans=20.0, vo5=20.1)
LOOP = 24.0
for i, k in enumerate(['vo0', 'vo1', 'vo2', 'vo3', 'vo4', 'vo5']):
    assert T[k] + VO[i] < ([T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5'], LOOP - 0.8] + [99])[i], ('VO overlap', k)
G = dict(LOOP=LOOP, FPS_K=FPS_K, T=T, POT_RI=105.0, POT_RO=107.5, POT_H=150.0, LID_TOP=168.0, PIPE_RO=4.0, PIPE_RI=1.6, PIPE_Y0=165.0, PT=186.0,
         W_BORE=4.6, W_DEPTH=12.0, W_R=19.0, W_H=26.0, LIFT=3.0, TILT=2.2, WATER=62.0)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
# lift/drop cycles [upA, upB, downA, downB] for the bobbing parts (hook, step 4, outro)
CYC_HOOK = [(0.2, 0.36, 0.62, 0.8), (1.1, 1.26, 1.52, 1.7)]
CYC_S4 = [(17.0, 17.18, 17.62, 17.85), (18.5, 18.68, 19.12, 19.35)]
CYC_OUT = [(20.3, 20.46, 20.9, 21.1), (21.7, 21.86, 22.3, 22.5), (23.0, 23.16, 23.55, 23.75)]
def cyc(t, C, L):
    for a, b, c, d in C:
        if a <= t < d: return L * (ease((t - a) / (b - a)) if t < b else 1 - ease((t - c) / (d - c)))
    return 0.0
def state(t):
    L = G['LIFT']
    if t < T['cutIn']: h = cyc(t, CYC_HOOK, L * 1.4)
    elif t < T['s2']: h = 0.0
    elif t < T['s4']: h = L * ease((t - T['liftA']) / (T['liftB'] - T['liftA']))
    elif t < T['outA']: h = (L * (1 - ease((t - T['dropA']) / (T['dropB'] - T['dropA']))) if t < T['dropB'] else cyc(t, CYC_S4, L))
    else: h = cyc(t, CYC_OUT, L * 1.4)
    ext = t < T['cutIn'] or t >= T['outA']
    tilt = G['TILT'] * math.sin(t * 11) * min(1, h / L) if ext else 0.0
    # steam push p: rises while the weight is shut, sits at the threshold while it hovers, dips after each puff
    if T['cutIn'] <= t < T['s2']: p = 0.2 + 0.3 * ease((t - T['cutIn']) / (T['s2'] - T['cutIn']))
    elif T['s2'] <= t < T['liftA']: p = 0.5 + 0.5 * ease((t - T['s2']) / (T['liftA'] - 0.1 - T['s2']))
    else: p = 1.0 if h > 1e-3 else 0.9
    falling = any(c <= t < d for a, b, c, d in CYC_HOOK + CYC_S4 + CYC_OUT) or T['dropA'] <= t < T['dropB']
    if falling: p = 0.9
    elif t >= T['s3'] and t < T['liftA']: p = 1.0 if t >= T['liftA'] - 0.1 else p
    if h > 1e-3 and not falling: p = 1.0
    return [h, tilt, p]
rows = [[round(i / FPS_K, 4)] + [round(v, 4) for v in state(i / FPS_K)] for i in range(int(LOOP * FPS_K) + 1)]
fail = []
for (t, h, tl, p), (t2, h2, tl2, p2) in zip(rows, rows[1:]):
    if h < -1e-6: fail.append(('weight below its seat (through the pipe)', t))
    if h2 > h + 1e-6 and p2 < 1.0: fail.append(('weight rose without enough push', t2))
    # bore vs pipe: the bore still overlaps the pipe by (W_DEPTH - h); tilt moves the bore wall sideways
    over = G['W_DEPTH'] - h
    if over * math.sin(math.radians(abs(tl))) + 1e-6 >= G['W_BORE'] - G['PIPE_RO']: fail.append(('bore hits pipe', t, tl))
    if h > G['W_DEPTH'] - 2: fail.append(('weight comes off the pipe', t))
if G['PT'] - G['W_DEPTH'] <= G['LID_TOP']: fail.append(('weight skirt in the lid',))
for a, b, c in zip(rows, rows[1:], rows[2:]):
    if b[1] > 1e-3 and b[3] < 1.0 and c[1] >= b[1] >= a[1]: fail.append(('weight held up without enough push', b[0]))
if rows[0][1] != 0 or rows[-1][1] > 1e-3: fail.append(('loop not seamless', rows[0][1], rows[-1][1]))
print('checks:', 'PASS' if not fail else fail[:6], '| rows', len(rows))
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
