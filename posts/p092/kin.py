# p092 eddy-current speedometer "HOW DOES THE NEEDLE / KNOW YOUR SPEED?" - kinematics + HARD GATE 5.2 checks. Units mm, axis z = gauge axis (+z toward the driver).
# Magnet (bar, tip radius R_MAG) spins with the cable at omega (rev/s, shown SLOWED). The aluminum cup (inner radius R_CUP_IN) surrounds it with an air gap and
# carries the needle on its spindle. Eddy-current drag torque ~ KD * omega * overlap; the hairspring torque ~ phi. First-order lag: phi' = (KD*omega*overlap - phi)/TAU.
# overlap = how far the cup surrounds the magnet (exploded view: cup lifted LIFT0 mm in step 1, slides down in step 2).
import json, math
R_MAG, MAG_T = 17.0, 20.0; R_CUP_IN, R_CUP_OUT = 21.0, 23.0; CUP_RIM, CUP_BASE = -80.0, -40.0; MAG_Z = (-72.0, -52.0); LIFT0 = 0.0
KD = math.radians(50) / 0.7; TAU = 0.55; FPS_K = 120; SWEEP = math.radians(240); MPH_MAX = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.25, 'vo1': 2.1}
GAP = {2: 0.25, 3: 0.25, 4: 0.25, 5: 0.25, 6: 0.3}
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.5, 2); T['LOOP'] = LOOP
T['hookEnd'] = 1.0; T['cutIn'] = T['vo1'] + 0.55; T['out'] = T['vo6'] - 0.05
T['spinA'] = T['cutIn'] + 0.25; T['slideA'] = T['vo2'] + 0.15; T['slideB'] = T['vo2'] + 1.55
T['fastA'] = T['vo5'] + 1.0; T['fastB'] = T['vo5'] + 1.9; T['balA'] = T['vo4'] + 0.5; T['balB'] = T['vo4'] + 1.1; T['slowA'] = LOOP - 2.1; T['slowB'] = LOOP - 1.1
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def omega(t):
    if t < T['cutIn']: return 1.5 + 0.6 * ease(t / 0.4)                    # hook (outside): from 54 mph the car accelerates, needle sweeps up to 75
    if t < T['spinA']: return 0.0                                           # cut inside: fresh exploded view, magnet at rest
    if t < T['balA']: return 0.4 * ease((t - T['spinA']) / 0.8)          # steps 1-3: gentle spin (14 mph)
    if t < T['fastA']: return 0.4 + 0.3 * ease((t - T['balA']) / (T['balB'] - T['balA']))   # step 4: a bit faster -> drag jumps, cup turns until spring = drag (25 mph)
    if t < T['out']: return 0.7 + 0.8 * ease((t - T['fastA']) / (T['fastB'] - T['fastA']))
    return 1.5                                                              # outside again: steady 54 mph = the first frame (seamless loop)
def lift(t):
    if t < T['cutIn']: return 0.0
    if t < T['slideA']: return LIFT0
    return LIFT0 * (1 - ease((t - T['slideA']) / (T['slideB'] - T['slideA'])))
def overlap(t):  # fraction of the magnet height inside the cup
    lo = CUP_RIM + lift(t); return max(0.0, min(1.0, (MAG_Z[1] - lo) / (MAG_Z[1] - MAG_Z[0])))
N = int(LOOP * FPS_K) + 2; rows = []; mag = 0.0; phi = KD * 1.5
for i in range(N):
    t = i / FPS_K
    if abs(t - T['cutIn']) < 0.5 / FPS_K: phi = 0.0                       # hard cut to the exploded view (cup lifted off, spring at rest)
    pass                                                                   # cut outside: same state continues (no reset)
    w = omega(t); ov = overlap(t); tau = 0.12 if t < T['cutIn'] else TAU
    phi += (KD * w * ov - phi) / tau / FPS_K if (t >= T['cutIn'] or t < T['cutIn']) else 0
    if t < T['cutIn']: phi_out = phi
    mag = (mag + 2 * math.pi * w / FPS_K) % (2 * math.pi)
    rows.append([round(t, 4), round(mag, 5), round(phi, 5), round(lift(t), 3), round(w, 4), round(ov, 4), round(w * ov, 4), round(phi / SWEEP * MPH_MAX, 3)])
# ---- HARD GATE 5.2 checks ----
ok = True
gap = R_CUP_IN - R_MAG; assert gap >= 3.0, 'air gap'                       # magnet tip never touches the cup wall (radial) for any angle
for r in rows:
    t, m, ph, lf, w, ov, fl, mp = r
    if MAG_Z[1] > CUP_BASE - 2 + lf: ok = False; print('axial hit', t)     # magnet top below the cup's inner base
    if not (-1e-6 <= ph <= SWEEP): ok = False; print('phi range', t, ph)
    if w < -1e-9: ok = False
for a, b in zip(rows, rows[1:]):                                            # nothing moves without a cause: cup turns forward only with drag > spring, back only with drag < spring
    if abs(b[0] - T['cutIn']) < 1 / FPS_K or abs(b[0] - T['out']) < 1 / FPS_K: continue
    dphi = b[2] - a[2]; drag = KD * b[6]
    if dphi > 1e-9 and not drag > a[2] - 1e-9: ok = False; print('cause+', a[0])
    if dphi < -1e-9 and not drag < a[2] + 1e-9: ok = False; print('cause-', a[0])
mph = lambda ph: ph / SWEEP * MPH_MAX
print('T', {k: round(v, 3) for k, v in T.items()})
print('air gap', gap, 'mm; phi max deg', round(math.degrees(max(r[2] for r in rows)), 1), 'hook mph', round(mph(KD * 2.1)), 'inside mph', round(mph(KD * 0.7)), '->', round(mph(KD * 1.5)))
print('first/last phi', rows[0][2], rows[-1][2], 'PASS' if ok else 'FAIL')
json.dump(rows, open('kin.json', 'w'), separators=(',', ':'))
json.dump({'T': T, 'LOOP': LOOP, 'FPS_K': FPS_K, 'R_MAG': R_MAG, 'MAG_T': MAG_T, 'MAG_Z': MAG_Z, 'R_CUP_IN': R_CUP_IN, 'R_CUP_OUT': R_CUP_OUT, 'CUP_RIM': CUP_RIM, 'CUP_BASE': CUP_BASE,
           'LIFT0': LIFT0, 'SWEEP': SWEEP, 'MPH_MAX': MPH_MAX, 'KD': KD}, open('geom.json', 'w'), indent=1)
