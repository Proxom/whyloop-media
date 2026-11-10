# p059 gearbox synchro (17:00 outlier #1). mm, shaft axis = z. Writes geom.json (2D outlines) + kin_240.json (240 Hz samples) + events.json.
# Principle: the gear spins free on the shaft (driven by the layshaft); the sleeve turns with the shaft. Shifting pushes the sleeve,
# which pushes the brass blocker ring onto the gear's cone; cone friction brings the gear to shaft speed while the ring (dragged half a
# tooth) blocks the sleeve; once speeds match the ring turns back in line, the sleeve slides through it onto the gear's dog teeth: locked.
import json, math, numpy as np
LOOP = 14.0; FPS = 240; N = int(LOOP * FPS)
# ---- gears (involute, m = 3, 20 deg) ----
def gear(z, m=3.0, back=0.12, n_inv=10):
    rp = z * m / 2; ra = rp + m; rf = rp - 1.25 * m; rb = rp * math.cos(math.radians(20))
    inv = lambda a: math.tan(a) - a
    s = math.pi * m / 2 - back  # tooth thickness at pitch circle
    half_p = s / (2 * rp) + inv(math.radians(20))  # half angle of tooth at base circle (involute start)
    pts = []
    for k in range(z):
        c = 2 * math.pi * k / z
        def flank(sign):
            out = []
            r0 = max(rb, rf)
            if rf < rb: out.append((rf, c + sign * half_p))
            for i in range(n_inv + 1):
                r = r0 + (ra - r0) * i / n_inv; a = math.acos(min(1, rb / r)); out.append((r, c + sign * (half_p - inv(a))))
            return out
        R = flank(-1); L = flank(+1)[::-1]
        pts += R + L
        # root arc to next tooth
        a0 = c + half_p; a1 = c + 2 * math.pi / z - half_p
        for i in range(1, 4): pts.append((rf, a0 + (a1 - a0) * i / 4))
    return [[r * math.cos(a), r * math.sin(a)] for r, a in pts], dict(rp=rp, ra=ra, rf=rf)
G1, g1 = gear(30); G2, g2 = gear(20)
# ---- splines / dog teeth: 24 straight teeth, external (hub, blocker, dog ring) and internal (sleeve) ----
NT = 24; P = 2 * math.pi / NT; W_EXT = 0.40 * P; W_INT = 0.40 * P
R_ROOT, R_TIP, S_ROOT, S_TIP, S_OUT = 30.0, 33.5, 33.9, 30.4, 42.0
def ext_teeth(r0=R_ROOT, r1=R_TIP, w=W_EXT, n=4):
    pts = []
    for k in range(NT):
        c = k * P; pts += [[r0 * math.cos(c - w / 2 - 0.02), r0 * math.sin(c - w / 2 - 0.02)], [r1 * math.cos(c - w / 2), r1 * math.sin(c - w / 2)], [r1 * math.cos(c + w / 2), r1 * math.sin(c + w / 2)], [r0 * math.cos(c + w / 2 + 0.02), r0 * math.sin(c + w / 2 + 0.02)]]
        for i in range(1, n): a = c + w / 2 + 0.02 + (P - w - 0.04) * i / n; pts.append([r0 * math.cos(a), r0 * math.sin(a)])
    return pts
def int_teeth():  # inner outline of the sleeve: tooth tips at S_TIP centred between external teeth (offset P/2)
    pts = []
    for k in range(NT):
        c = k * P + P / 2; pts += [[S_ROOT * math.cos(c - W_INT / 2 - 0.02), S_ROOT * math.sin(c - W_INT / 2 - 0.02)], [S_TIP * math.cos(c - W_INT / 2), S_TIP * math.sin(c - W_INT / 2)], [S_TIP * math.cos(c + W_INT / 2), S_TIP * math.sin(c + W_INT / 2)], [S_ROOT * math.cos(c + W_INT / 2 + 0.02), S_ROOT * math.sin(c + W_INT / 2 + 0.02)]]
        for i in range(1, 4): a = c + W_INT / 2 + 0.02 + (P - W_INT - 0.04) * i / 4; pts.append([S_ROOT * math.cos(a), S_ROOT * math.sin(a)])
    return pts
EXT = ext_teeth(); INT = int_teeth()
# ---- axial layout (z) ----
Z = dict(gear=(0, 18), dog=(18, 23), cone=(23, 31), blk=(25, 33), hub=(36, 54), slv=(35, 57))
CONE_R = (27.0, 24.0)  # cone radius at z 23 and z 31
# ---- timeline ----
T = dict(FADE_OUT=(1.3, 2.3), PUSH=(4.0, 4.5), SYNC=(4.5, 7.3), ALIGN=(7.35, 7.7), ENGAGE=(7.8, 8.6), DISENGAGE=(11.0, 11.7), SPINUP=(11.9, 12.9), FADE_IN=(11.6, 12.7), FOLLOW=(12.55, 13.95))
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def seg(t, a, b): return sm((t - a) / (b - a))
ts = np.arange(N) / FPS
# sleeve shift (negative = toward the gear): neutral 0 -> contact -2.95 -> engaged -15.5 -> back to 0
X_CONTACT, X_ENG = -2.95, -15.5
def slv_x(t):
    if t < T['PUSH'][0]: return 0.0
    if t < T['PUSH'][1]: return X_CONTACT * seg(t, *T['PUSH'])
    if t < T['ENGAGE'][0]: return X_CONTACT
    if t < T['ENGAGE'][1]: return X_CONTACT + (X_ENG - X_CONTACT) * seg(t, *T['ENGAGE'])
    if t < T['DISENGAGE'][0]: return X_ENG
    return X_ENG * (1 - seg(t, *T['DISENGAGE']))
def blk_x(t):  # blocker ring: the sleeve front (z 35+s) pushes its back face (z 33+b) up to 1 mm onto the cone; it follows back
    s = slv_x(t); return max(-1.0, min(0.0, s + 1.95))
# speeds: shaft constant (5 rev per loop); gear = shaft + A * p(t)
WS = 2 * math.pi * 5 / LOOP
def p(t):
    if t < T['SYNC'][0]: return 1.0
    if t < T['SYNC'][1]: u = (t - T['SYNC'][0]) / (T['SYNC'][1] - T['SYNC'][0]); return (1 - u) ** 1.6 * (1 - sm(u)) ** 0.0 if u < 1 else 0.0
    if t < T['SPINUP'][0]: return 0.0
    if t < T['SPINUP'][1]: return seg(t, *T['SPINUP'])
    return 1.0
pv = np.array([p(t) for t in ts]); I_tot = pv.sum() / FPS
n_rel = 2  # extra gear revs per loop relative to the shaft
A = 2 * math.pi * n_rel / I_tot
cum = np.concatenate([[0], np.cumsum(pv[:-1])]) / FPS
i_sync = int(T['SYNC'][1] * FPS)
phi0 = -(A * cum[i_sync]) % (2 * math.pi)
rel = phi0 + A * cum  # gear angle minus shaft angle
th_s = WS * ts
K = []
for i, t in enumerate(ts):
    s = slv_x(t); b = blk_x(t)
    # blocker ring angular offset vs hub: dragged half a tooth by the faster gear (blocks), turned back in line by the sleeve chamfers
    if T['ALIGN'][0] <= t < T['DISENGAGE'][1] + 0.1: beta = 0.5 * P * (1 - seg(t, *T['ALIGN']))
    else: beta = 0.5 * P * seg(t, T['DISENGAGE'][1] + 0.1, T['DISENGAGE'][1] + 0.4) if t >= T['DISENGAGE'][1] + 0.1 else 0.5 * P
    K.append(dict(s=round(th_s[i], 6), g=round(th_s[i] + rel[i], 6), x=round(s, 4), bx=round(b, 4), bb=round(beta, 6)))
ev = [dict(type='push', t=T['PUSH'][1]), dict(type='rub', t0=T['SYNC'][0], t1=T['SYNC'][1]), dict(type='align', t=T['ALIGN'][1]), dict(type='lock', t=T['ENGAGE'][1] - 0.05), dict(type='release', t=T['DISENGAGE'][0] + 0.25)]
json.dump(dict(LOOP=LOOP, G1=G1, G2=G2, g1=g1, g2=g2, EXT=EXT, INT=INT, NT=NT, Z=Z, CONE_R=CONE_R, S_OUT=S_OUT, R_ROOT=R_ROOT, R_TIP=R_TIP, S_ROOT=S_ROOT, S_TIP=S_TIP, CD=75.0, RATIO=1.5, T=T, A=A, WS=WS), open('geom.json', 'w'))
json.dump(K, open('kin_240.json', 'w')); json.dump(ev, open('events.json', 'w'))
print('A (gear extra speed) %.3f rad/s = %.3f rev/s; shaft %.3f rev/s; rel at sync end %.4f; rel loop %.4f' % (A, A / 2 / math.pi, WS / 2 / math.pi, rel[i_sync] % (2 * math.pi), (rel[-1] + A * pv[-1] / FPS - rel[0]) % (2 * math.pi)))
