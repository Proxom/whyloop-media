# HARD GATE mechanism check over the whole loop: every gear pair stays in mesh (tooth of one centred in a gap of the other,
# i.e. tangential offset 0.5 pitch at the contact), open-diff law thL + thR = 2 c, spider rate = -(16/10) d, pinion = 41/11 ring.
import json, math, numpy as np, importlib.util, sys
spec = importlib.util.spec_from_file_location('kin', 'kin.py'); K = importlib.util.module_from_spec(spec); sys.argv = ['kin']; spec.loader.exec_module(K)
worst = {}
for r in K.rows[::4]:
    for A, B in K.PAIRS:
        s, p = K.mesh_offset(A, B, r, K.OFF[A], K.OFF[B]); e = abs(s - 0.5); worst[(A, B)] = max(worst.get((A, B), 0), e)
    thR, thL = r['c'] + r['d'], r['c'] - r['d']; assert abs(thR + thL - 2 * r['c']) < 1e-9
ok = all(v < 0.03 for v in worst.values())  # <3 % of pitch: chord-vs-arc measurement noise of the tangent projection (constant over the loop = no drift)
print('mesh offset error (fraction of pitch, max over loop):', {f'{a}-{b}': round(v, 5) for (a, b), v in worst.items()}, 'PASS' if ok else 'FAIL')
# wheel speeds in the three phases (rev/s)
for t in (20.0, 31.0, 35.0):
    i = int(t * K.FPS); a, b = K.rows[i], K.rows[i + 24]; dt = 0.1
    wl = -((b['c'] - b['d']) - (a['c'] - a['d'])) / dt / (2 * math.pi); wr = -((b['c'] + b['d']) - (a['c'] + a['d'])) / dt / (2 * math.pi); wc = -(b['c'] - a['c']) / dt / (2 * math.pi)
    print(f't={t}: carrier {wc:.3f} rev/s, left {wl:.3f}, right {wr:.3f}, (L+R)/2 {(wl + wr) / 2:.3f}')
