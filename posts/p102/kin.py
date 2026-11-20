# p102 pencil tire gauge kinematics + HARD GATE 5.2 checks. Units mm, gauge local axis = +y, chuck mouth at y 0.
# Rows: [t, gy (gauge lift above engaged), d (piston travel), s (stick travel), open (valve open 0/1)]
import json, math
FPS_K = 120
P = 32.0                                   # tire pressure shown (psi); 1 mm per psi (60 psi = 60 mm full travel)
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.2, cutIn=2.3, vo1=2.5, pressA=3.0, pressB=3.6, vo2=6.8, pistA=7.0, pistB=10.0, vo3=11.1, vo4=15.5, liftA=16.0, liftB=16.5,
         retA=16.5, retB=17.1, outA=20.3, vo5=20.5, ans=23.2)
LOOP = 25.0
H = dict(shootA=0.15, shootB=0.6)
for i, k in enumerate(['vo0', 'vo1', 'vo2', 'vo3', 'vo4', 'vo5']):
    assert T[k] + VO[i] < ([T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5'], LOOP - 0.8] + [99])[i], ('VO overlap', k)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def eout(u): u = min(1, max(0, u)); return 1 - (1 - u) ** 3
def state(t):
    if t < T['cutIn']:                      # hook: engaged, piston + stick shoot out
        d = P * eout((t - H['shootA']) / (H['shootB'] - H['shootA'])); return [0.0, d, d, 1]
    if t < T['outA']:
        gy = 10 * (1 - ease((t - T['pressA']) / (T['pressB'] - T['pressA'])))
        gy += 14 * ease((t - T['liftA']) / (T['liftB'] - T['liftA']))
        op = 1 if gy < 0.5 else 0
        d = P * ease((t - T['pistA']) / (T['pistB'] - T['pistA']))
        d *= 1 - ease((t - T['retA']) / (T['retB'] - T['retA']))
        return [gy, d, None, op]
    return [14.0, 0.0, P, 0]
rows = []; smax = 0; prev_open = 0
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; gy, d, s, op = state(t)
    if t >= T['cutIn'] and t < T['outA']:
        if t - 1 / FPS_K < T['cutIn']: smax = 0
        smax = max(smax, d); s = smax
    rows.append([round(t, 4), round(gy, 4), round(d, 4), round(s, 4), op])
# ---- geometry (gauge local) ----
G = dict(LOOP=LOOP, FPS_K=FPS_K, T=T, H=H, P=P, TUBE_RI=7.6, TUBE_RO=9.0, PIST_Y=20.0, PIST_H=5.0, STOP_Y=126.0, STOP_TOP=132.0, HOLE_R=3.3,
         ROD_R=3.0, CAP_R=5.5, CAP_H=2.5, ROD_L=118.0, SPR_R=6.4, SPR_W=0.6, SPR_TURNS=14, VALVE_TOP=2.8, VPIN_REST=1.5, GPIN_BOT=-0.5, SEAL_Y=2.9)
# ---- checks over the whole loop ----
fail = []
for t, gy, d, s, op in rows:
    pt = G['PIST_Y'] + G['PIST_H'] + d                      # piston top
    sb = G['PIST_Y'] + G['PIST_H'] + s                      # stick cap bottom
    if pt > G['STOP_Y'] - G['SPR_TURNS'] * 2 * G['SPR_W']: fail.append(('spring solid', t))
    if sb < pt - 1e-6: fail.append(('stick inside piston', t, sb, pt))
    if s + 1e-6 < d: fail.append(('piston passed the stick', t))
    if sb + G['CAP_H'] > G['STOP_Y']: fail.append(('cap hits stop', t))
    if G['CAP_R'] >= G['SPR_R'] - G['SPR_W']: fail.append(('cap vs spring', t))
    if G['SPR_R'] + G['SPR_W'] >= G['TUBE_RI']: fail.append(('spring vs tube', t))
    if G['ROD_R'] >= G['HOLE_R']: fail.append(('rod vs hole', t))
    # valve: stem lip (world) never above the seal (gauge local seal y + gy)
    if G['VALVE_TOP'] > G['SEAL_Y'] + gy + 1e-6: fail.append(('stem through seal', t))
    vpin = min(G['VPIN_REST'], G['GPIN_BOT'] + gy)
    if (vpin < G['VPIN_REST'] - 1.5) != bool(op): fail.append(('valve state', t, vpin, op))
    if d > 0.01 and not op and t >= T['cutIn'] and t < T['liftA']: fail.append(('piston moves with valve shut', t))
    # piston only rises while air flows (cause), stick only moves when the piston pushes it
for a, b in zip(rows, rows[1:]):
    if b[3] > a[3] + 1e-6 and abs(b[3] - b[2]) > 1e-3 and b[0] >= T['cutIn']: fail.append(('stick moved without the piston', b[0]))
    if b[2] > a[2] + 1e-6 and not b[4] and b[0] >= T['cutIn']: fail.append(('piston rose with valve shut', b[0]))
print('checks:', 'PASS' if not fail else fail[:6], '| rows', len(rows))
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
