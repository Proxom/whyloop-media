# p105 bottle dynamo kinematics + HARD GATE 5.2 checks. Units mm, rad, s.
# Wheel in the world xy plane (axis z), hub at the origin. Dynamo axis along the radial unit u at angle TH (deg), roller pressed on the +z sidewall.
# Rows: [t, wheelAngle, rollerAngle, omegaWheel, brightness 0..1, cut 0..1]
import json, math
FPS_K = 120
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.2, cutIn=2.2, vo1=2.4, s2=7.2, vo2=7.4, cutA=7.6, cutB=8.6, s3=12.0, vo3=12.2, s4=17.0, vo4=17.2,
         fastA=18.0, fastB=19.2, stopA=20.4, stopB=21.6, ans=22.9, vo5=23.0, goA=23.2, goB=24.6)
LOOP = 26.8
starts = [T['vo0'], T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5']]; nxt = [T['cutIn'], T['s2'], T['s3'], T['s4'], T['ans'], LOOP - 0.5]
for i in range(6): assert starts[i] + VO[i] < nxt[i], ('VO overlap', i, starts[i] + VO[i], nxt[i])
G = dict(TH=88.0, RT=320.0, RTUBE=18.0, RR=12.0, RL=7.0, ZOFF=30.0, BODY_R=17.0, BODY_Y0=14.0, BODY_Y1=100.0, MAG_R=9.0, MAG_Y0=30.0, MAG_Y1=62.0,
         COIL_RI=11.0, COIL_RO=15.0, COIL_Y0=27.0, COIL_Y1=65.0, FORK_TH=100.0, FORK_Z=45.0, FORK_R=10.0)
W_SLOW, W_HOOK, W_FAST = 0.6, 0.9, 1.5
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def omega(t):
    if t < T['cutIn']: return W_HOOK
    if t < T['fastA']: return W_SLOW
    if t < T['stopA']: return W_SLOW + (W_FAST - W_SLOW) * ease((t - T['fastA']) / (T['fastB'] - T['fastA']))
    if t < T['goA']: return W_FAST * (1 - ease((t - T['stopA']) / (T['stopB'] - T['stopA'])))
    return W_HOOK * ease((t - T['goA']) / (T['goB'] - T['goA']))
RATIO = G['RT'] / G['RR']            # roller rim speed = tire speed at the contact radius (no slip)
rows = []; wa = 0.0; dt = 1 / FPS_K; n = int(LOOP * FPS_K) + 2
for i in range(n):
    t = i * dt; w = omega(t)
    cut = 0.0 if t < T['cutA'] or t >= T['ans'] else ease((t - T['cutA']) / (T['cutB'] - T['cutA']))
    rows.append([round(t, 5), wa, wa * RATIO, w, min(1.0, w / W_FAST), cut]); wa += w * dt
# ---- HARD GATE 5.2 checks ----
# 1) roller never penetrates the tire: roller lowest line at z = ZOFF - RR; tire side z(r) = sqrt(RTUBE^2 - (r-RT)^2) over the roller length
for k in range(201):
    r = G['RT'] - G['RL'] + 2 * G['RL'] * k / 200; zt = math.sqrt(max(0, G['RTUBE'] ** 2 - (r - G['RT']) ** 2)); assert zt <= G['ZOFF'] - G['RR'] + 1e-6, ('roller in tire', r)
# contact exists (touch at r = RT)
assert abs(math.sqrt(G['RTUBE'] ** 2) - (G['ZOFF'] - G['RR'])) < 1e-6
# 2) dynamo body (radius BODY_R around the axis at z=ZOFF, from r = RT+BODY_Y0) never touches the tire
for k in range(401):
    r = G['RT'] + G['BODY_Y0'] + k * 0.25; zt = math.sqrt(max(0, G['RTUBE'] ** 2 - (r - G['RT']) ** 2)) if abs(r - G['RT']) < G['RTUBE'] else 0
    if zt > 0: assert zt < G['ZOFF'] - G['BODY_R'], ('body hits tire', r, zt)
# 3) magnet inside the coil, coil inside the body wall (2 mm wall), magnet spins about the axis (radius constant) -> never touches the coil
assert G['MAG_R'] < G['COIL_RI'] - 1 and G['COIL_RO'] < G['BODY_R'] - 1.5 and G['COIL_Y0'] < G['MAG_Y0'] and G['COIL_Y1'] > G['MAG_Y1']
# 4) dynamo vs fork blade: fork axis at angle FORK_TH, z = FORK_Z; body axis at angle TH, z = ZOFF. Closest distance over the body length
def P(th, r, z): a = math.radians(th); return (r * math.cos(a), r * math.sin(a), z)
dmin = 1e9
for r1 in range(330, 425, 2):
    p = P(G['TH'], r1, G['ZOFF'])
    for r2 in range(0, 520, 2):
        q = P(G['FORK_TH'], r2, G['FORK_Z']); dmin = min(dmin, math.dist(p, q))
assert dmin > G['BODY_R'] + G['FORK_R'] + 5, ('dynamo hits fork', dmin)
# 5) fork blade clear of the tire (fork at z = 45 > tire half width 18 + fork radius 10)
assert G['FORK_Z'] - G['FORK_R'] > G['RTUBE'] + 5
# 6) nothing moves without a cause: roller and magnet angles = wheel angle * RATIO exactly; lamp brightness follows wheel speed (0 when stopped)
assert all(abs(r[2] - r[1] * RATIO) < 1e-6 for r in rows) and all((r[4] == 0) == (r[3] == 0) for r in rows)
G.update(LOOP=LOOP, T=T, FPS_K=FPS_K, RATIO=RATIO, W_FAST=W_FAST)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('kin PASS: roller touches the tire, no penetration; body/tire, body/fork (min %.1f mm), magnet/coil clear; roller ratio %.2f; rows %d' % (dmin, RATIO, len(rows)))
