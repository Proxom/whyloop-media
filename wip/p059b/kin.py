# p059b gearbox synchro REMAKE (clarity rules, Erkan 10 Nov 18:30). mm, shaft axis = z. Writes geom.json, kin_240.json, events.json, timeline.json.
# Principle (same as p059): the gear spins freely on the output shaft (driven by the layshaft); the sleeve turns with the shaft on a hub.
# Shifting slides the sleeve, which presses the brass blocker ring onto the gear's cone; cone friction brings the gear to shaft speed while
# the ring (dragged half a tooth) blocks the sleeve; once speeds match the ring turns back in line and the sleeve slides onto the dog teeth.
# NEW in p059b: a "without a synchro" demo (ring removed, the sleeve's teeth butt against the faster dog teeth and bounce = grind),
# slow motion during the rub (w(t) scales both speeds), and an H-pattern lever (sideways select = no sleeve motion; forward = sleeve).
import json, math, numpy as np
exec(open('../../posts/p059/kin.py').read().split('# ---- axial layout')[0])  # reuse p059 gear + spline geometry (G1, G2, EXT, INT, NT, P, radii)
Z = dict(gear=(0, 18), dog=(18, 23), cone=(23, 31), blk=(25, 33), hub=(36, 54), slv=(35, 57))
CONE_R = (27.0, 24.0)
LOOP = 42.0; FPS = 240; N = int(LOOP * FPS)
VO_AT = [0.3, 5.6, 9.0, 12.4, 16.0, 19.4, 23.4, 28.2, 31.3, 34.5]
T = dict(SELECT=(1.0, 2.4), FADE_OUT=(3.4, 5.2), NAME=(5.4, 12.2), RING_OUT=(12.2, 12.8), CRASH_PUSH=(14.6, 15.9), CHATTER=(15.9, 17.6),
         CRASH_BACK=(17.8, 18.8), RING_IN=(18.6, 19.3), PUSH=(20.6, 21.4), SYNC=(21.4, 27.6), SLOWMO=(22.4, 28.0), ALIGN=(27.65, 28.0),
         ENGAGE=(28.6, 30.0), LOCKED=(30.0, 34.4), PAYOFF=(34.4, 38.0), DISENGAGE=(38.0, 38.7), SPINUP=(38.9, 39.9), FADE_IN=(38.6, 40.2),
         DESELECT=(40.0, 41.2), FOLLOW=(40.4, 41.95))
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def seg(t, a, b): return sm((t - a) / (b - a))
ts = np.arange(N) / FPS
X_CONTACT, X_ENG, X_DOGFACE = -2.95, -15.5, -11.85   # sleeve front z = 35 + x; dog teeth end face at z 23 -> x = -12 (0.15 mm clear)
def chatter(t):  # sleeve bouncing off the dog-teeth end faces: |sin| bounces, decaying, always >= 0 (never inside the teeth)
    u = t - T['CHATTER'][0]; return 1.1 * abs(math.sin(2 * math.pi * 7.0 * u)) * math.exp(-u * 0.6) * (1 - seg(t, T['CHATTER'][1] - 0.25, T['CHATTER'][1]))
def slv_x(t):
    if t < T['CRASH_PUSH'][0]: return 0.0
    if t < T['CRASH_PUSH'][1]: return X_DOGFACE * seg(t, *T['CRASH_PUSH'])
    if t < T['CHATTER'][1]: return X_DOGFACE + chatter(t)
    if t < T['CRASH_BACK'][0]: return X_DOGFACE
    if t < T['CRASH_BACK'][1]: return X_DOGFACE * (1 - seg(t, *T['CRASH_BACK']))
    if t < T['PUSH'][0]: return 0.0
    if t < T['PUSH'][1]: return X_CONTACT * seg(t, *T['PUSH'])
    if t < T['ENGAGE'][0]: return X_CONTACT
    if t < T['ENGAGE'][1]: return X_CONTACT + (X_ENG - X_CONTACT) * seg(t, *T['ENGAGE'])
    if t < T['DISENGAGE'][0]: return X_ENG
    return X_ENG * (1 - seg(t, *T['DISENGAGE']))
def ring_vis(t):  # 1 = brass ring present; 0 = removed for the "without a synchro" demo
    if t < T['RING_OUT'][0]: return 1.0
    if t < T['RING_OUT'][1]: return 1 - seg(t, *T['RING_OUT'])
    if t < T['RING_IN'][0]: return 0.0
    return seg(t, *T['RING_IN'])
def blk_x(t):
    if ring_vis(t) < 1: return 0.0
    return max(-1.0, min(0.0, slv_x(t) + 1.95))
def w(t):  # slow-motion factor (both speeds)
    a, b = T['SLOWMO']; return 1 - 0.55 * (seg(t, a, a + 0.5) - seg(t, b - 0.5, b))
def p(t):  # relative gear speed profile (1 = gear faster than shaft, 0 = matched)
    if t < T['SYNC'][0]: return 1.0
    if t < T['SYNC'][1]: u = (t - T['SYNC'][0]) / (T['SYNC'][1] - T['SYNC'][0]); return (1 - u) ** 1.5
    if t < T['SPINUP'][0]: return 0.0
    if t < T['SPINUP'][1]: return seg(t, *T['SPINUP'])
    return 1.0
wv = np.array([w(t) for t in ts]); pv = np.array([p(t) for t in ts])
n_s = 13; WS = 2 * math.pi * n_s / (wv.sum() / FPS)          # shaft: exactly 13 turns per loop
pw = pv * wv; n_rel = 6; A = 2 * math.pi * n_rel / (pw.sum() / FPS)  # gear: exactly 6 extra turns per loop
cum_s = np.concatenate([[0], np.cumsum(wv[:-1])]) / FPS * WS
cum_r = np.concatenate([[0], np.cumsum(pw[:-1])]) / FPS * A
i_sync = int(T['SYNC'][1] * FPS); phi0 = -cum_r[i_sync] % (2 * math.pi)
rel = phi0 + cum_r
K = []
for i, t in enumerate(ts):
    s = slv_x(t); b = blk_x(t)
    if T['ALIGN'][0] <= t < T['DISENGAGE'][1] + 0.1: beta = 0.5 * P * (1 - seg(t, *T['ALIGN']))
    elif t >= T['DISENGAGE'][1] + 0.1: beta = 0.5 * P * seg(t, T['DISENGAGE'][1] + 0.1, T['DISENGAGE'][1] + 0.4)
    else: beta = 0.5 * P
    sel = seg(t, *T['SELECT']) * (1 - seg(t, *T['DESELECT']))
    K.append(dict(s=round(cum_s[i], 6), g=round(cum_s[i] + rel[i], 6), x=round(s, 4), bx=round(b, 4), bb=round(beta, 6), rv=round(ring_vis(t), 4),
                  ws=round(WS * wv[i], 4), wg=round(WS * wv[i] + A * pw[i], 4), sel=round(sel, 4), sm=round(1 - wv[i], 4)))
ev = [dict(type='select', t=T['SELECT'][0] + 0.7), dict(type='crash', t0=T['CHATTER'][0], t1=T['CHATTER'][1]),
      dict(type='push', t=T['PUSH'][1] - 0.35), dict(type='rub', t0=T['SYNC'][0], t1=T['SYNC'][1]), dict(type='align', t=T['ALIGN'][1]),
      dict(type='lock', t=T['ENGAGE'][1] - 0.05), dict(type='release', t=T['DISENGAGE'][0] + 0.25), dict(type='select', t=T['DESELECT'][0] + 0.7)]
# chatter impact times (local minima of the bounce) for the grind sound
imp = [T['CHATTER'][0] + k / 14.0 for k in range(int((T['CHATTER'][1] - T['CHATTER'][0]) * 14))]
json.dump(dict(LOOP=LOOP, G1=G1, G2=G2, g1=g1, g2=g2, EXT=EXT, INT=INT, NT=NT, Z=Z, CONE_R=CONE_R, S_OUT=S_OUT, R_ROOT=R_ROOT, R_TIP=R_TIP,
               S_ROOT=S_ROOT, S_TIP=S_TIP, CD=75.0, RATIO=1.5, T=T, A=A, WS=WS, VO_AT=VO_AT, IMPACTS=imp), open('geom.json', 'w'))
json.dump(K, open('kin_240.json', 'w')); json.dump(ev, open('events.json', 'w'))
print('shaft %.3f rev/s, gear +%.3f rev/s rel; rel at sync end %.5f; loop closure s %.5f g %.5f' % (WS / 2 / math.pi, A / 2 / math.pi, rel[i_sync] % (2 * math.pi),
      (cum_s[-1] + WS * wv[-1] / FPS) % (2 * math.pi), (cum_s[-1] + WS * wv[-1] / FPS + phi0 + cum_r[-1] + A * pw[-1] / FPS - (phi0)) % (2 * math.pi)))
