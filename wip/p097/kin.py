# p097 pepper grinder: timeline + geometry + HARD GATE 5.2 checks. Units mm, y up, lathe phi: x = r sin(phi), z = r cos(phi) (camera at +z).
# Ring (fixed) bore: rR(y) = 10 + 0.25 (y - 4), y 4..30, grooves cut OUTWARD (bore never smaller than rR).
# Cone (turns with the shaft, lifted by dz): rC(y) = 7.5 - 0.15 (y - dz - 4), grooves cut INWARD (never bigger than rC).
# Gap(y) = rR - rC: wide at the top, narrow at the bottom; lifting the cone (dz > 0) makes every gap smaller (finer).
import json, math, numpy as np
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
VO_AT = [0.3, 2.5, 6.1, 9.75, 14.45, 17.3, 22.0]
for i in range(6): assert VO_AT[i] + D[i] < VO_AT[i + 1] - 0.15, ('VO overlap', i)
LOOP = 24.6; assert VO_AT[6] + D[6] < LOOP - 0.8
T = {f'vo{i}': VO_AT[i] for i in range(7)}
T.update(hookEnd=1.0, cutA=2.3, cutB=3.0, wideA=17.3, knobA=17.6, knobB=18.8, pushA=19.0, pushB=19.6, cmpA=19.9, outA=22.0, LOOP=LOOP)
DZMAX = 8.0; REVS = 10; NC = 10; P = LOOP / 8
def dz(t):
    if t < T['knobA'] or t >= T['outA']: return 0.0
    u = min(1, (t - T['knobA']) / (T['knobB'] - T['knobA'])); return DZMAX * u * u * (3 - 2 * u)
theta = lambda t: 2 * math.pi * REVS * t / LOOP
rR = lambda y: 10 + 0.25 * (y - 4)
rC = lambda y, d: 7.5 - 0.15 * (y - d - 4)
gap = lambda y, d: rR(y) - rC(y, d)
# flight of one corn: s in [0,1) inside the gap (y 31 -> 3.5), then falls out
def yflight(s): return 31.0 - 27.5 * s ** 1.25
def piece(y, d):   # child piece radius + spread of the 4 pieces (cluster extent = spread + r)
    g = gap(min(max(y, 4), 30), d); p = (31 - y) / 27.5; r = min(1.6, 0.2 * g); sp = min(0.27 * g, 0.9 + 2.0 * p); return r, sp
# ---- checks over one loop at 1/120 s ----
ok = True; mins = []
for t in np.arange(0, LOOP, 1 / 120):
    d = dz(t)
    for y in np.linspace(4, 30, 53):
        g = gap(y, d); mins.append(g)
        if g < 1.0: ok = False; print('gap too small', t, y, g)
    for i in range(NC):
        s = ((t / P) + i / NC) % 1.0
        y = yflight(s)
        if 4 <= y <= 30:
            r, sp = piece(y, d)
            if sp + r > 0.49 * gap(y, d): ok = False; print('piece overlaps', t, i, y, sp + r, gap(y, d))
# static corns in the chamber above the ring (back half only), no overlap with each other / wall (r 14) / cone top / shaft
rng = np.random.default_rng(97); corns = []; RC = 2.4
while len(corns) < 46:
    r = rng.uniform(4.0, 14 - RC - 0.4); y = rng.uniform(33.0, 47.0); ph = rng.uniform(math.pi * 0.52, math.pi * 1.48)
    x, z = r * math.sin(ph), r * math.cos(ph)
    coneTop = 34 + DZMAX
    if y - RC < coneTop + 0.5 and r - RC < rC(min(y, coneTop), DZMAX) + 0.5: continue
    if r - RC < 2.2 + 0.4: continue
    if any((x - a) ** 2 + (y - b) ** 2 + (z - c) ** 2 < (2 * RC + 0.2) ** 2 for a, b, c in corns): continue
    corns.append((round(x, 3), round(y, 3), round(z, 3)))
print('min gap over loop %.2f mm; dz max %.1f; corns %d; checks %s' % (min(mins), DZMAX, len(corns), 'PASS' if ok else 'FAIL'))
print('bottom gap coarse %.2f fine %.2f; top gap %.2f' % (gap(4, 0), gap(4, DZMAX), gap(30, 0)))
json.dump(dict(T=T, LOOP=LOOP, DZMAX=DZMAX, REVS=REVS, NC=NC, P=P, corns=corns, RC=RC), open('geom.json', 'w'), indent=1)
assert ok
