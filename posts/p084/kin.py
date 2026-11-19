# p084 v2 single-lever mixer tap cartridge "ONE LEVER: / HOT OR COLD?" - geometry, timeline, kinematics + HARD GATE 5.2 checks.
# 2D disc plane (u right, v away from the viewer), mm. Lower (inlet) disc fixed: HOT inlet slot (near left), COLD inlet slot (near right), OUTLET crescent (far side).
# Upper (control) disc: the lever holder turns it with the lever (lever LEFT = clockwise seen from above = theta > 0 here), the lever tilt slides it toward the
# viewer by s. p_world = R(-theta) * (p_frame + (0, -s)). Its underside pocket bridges the inlets it uncovers to the outlet (US 9,115,819 B2 figs 9-11).
import json, math
import numpy as np
D2R = math.pi / 180
RL = 24.0                                         # lower disc radius
HOTR = (-8.0, -9.5, -2.0, -2.0, 2.0)              # inlet slots (u0, v0, u1, v1, r)
COLDR = (2.0, -9.5, 8.0, -2.0, 2.0)
OUTS = (12.0, 17.0, 62.0, 118.0)                  # outlet crescent: r0, r1, angle0, angle1 (deg, v up)
PK = (-4.0, 0.0, 4.0, 21.0, 2.8)                  # pocket in the control-disc frame (u0, v0, u1, v1, r)
EL = (0.0, 4.0, 16.5, 21.5)                       # control disc outline: ellipse centre + semi-axes (frame)
S_OPEN, TH = 7.0, 32.0
G = 0.05; uu, vv = np.meshgrid(np.arange(-28, 28, G), np.arange(-28, 28, G))
def rr_in(u, v, b):
    u0, v0, u1, v1, r = b; cu = np.clip(u, u0 + r, u1 - r); cv = np.clip(v, v0 + r, v1 - r)
    return ((u - cu) ** 2 + (v - cv) ** 2 <= r * r) & (u >= u0) & (u <= u1) & (v >= v0) & (v <= v1)
def sector(u, v, b):
    r0, r1, a0, a1 = b; r = np.hypot(u, v); a = np.degrees(np.arctan2(v, u)); return (r >= r0) & (r <= r1) & (a >= a0) & (a <= a1)
HOTM, COLDM, OUTM = rr_in(uu, vv, HOTR), rr_in(uu, vv, COLDR), sector(uu, vv, OUTS)
def to_frame(s, th):
    c, sn = math.cos(th * D2R), math.sin(th * D2R)             # inverse of R(-theta) is R(+theta)
    return c * uu - sn * vv, sn * uu + c * vv + s
def areas(s, th):
    fu, fv = to_frame(s, th); pk = rr_in(fu, fv, PK); ell = ((fu - EL[0]) / EL[2]) ** 2 + ((fv - EL[1]) / EL[3]) ** 2 <= 1
    return dict(ah=(pk & HOTM).sum() * G * G, ac=(pk & COLDM).sum() * G * G, ao=(pk & OUTM).sum() * G * G,
                leak=((HOTM | COLDM) & ~ell).sum() * G * G, pk_out=(pk & ~ell).sum() * G * G)
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
starts = [0.95, 3.05]
for d in VO[1:-1]: starts.append(round(starts[-1] + VO[len(starts) - 1] + 0.16, 2))
T = {f'vo{i}': starts[i] for i in range(7)}; T['hookEnd'] = 0.9
T['inside'] = T['vo1'] - 0.15; T['outside'] = T['vo6'] - 0.12
T['lift_a'] = T['vo4'] + 0.4; T['lift_b'] = T['lift_a'] + 2.2
T['hot_a'] = T['vo5'] + 0.25; T['hot_b'] = T['hot_a'] + 1.1; T['cold_a'] = T['vo5'] + 2.0; T['cold_b'] = T['cold_a'] + 1.3
LOOP = round(T['vo6'] + VO[6] + 1.25, 2); T['LOOP'] = LOOP
sm = lambda x: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, x)))
def state(t):
    if t < T['hookEnd']: return S_OPEN, -TH + 2 * TH * sm((t - 0.1) / 0.7)
    if t < T['inside']: return S_OPEN * (1 - sm((t - 1.9) / 0.7)), TH * (1 - sm((t - 1.1) / 0.7))
    if t < T['lift_a']: return 0.0, 0.0
    if t < T['hot_a']: return S_OPEN * sm((t - T['lift_a']) / (T['lift_b'] - T['lift_a'])), 0.0
    if t < T['cold_a']: return S_OPEN, TH * sm((t - T['hot_a']) / (T['hot_b'] - T['hot_a']))
    return S_OPEN, TH - 2 * TH * sm((t - T['cold_a']) / (T['cold_b'] - T['cold_a']))
FPS = 30; rows = []
for i in range(int(LOOP * FPS) + 2):
    t = i / FPS; s, th = state(t); a = areas(s, th); rows.append([round(t, 4), round(s, 4), round(th, 4), round(a['ah'], 3), round(a['ac'], 3), round(a['ao'], 3), a['leak'], a['pk_out']])
leak = max(r[6] for r in rows); pko = max(r[7] for r in rows); print('max inlet area outside the control disc (must be 0):', leak, '| pocket outside disc:', pko)
assert leak == 0 and pko == 0
for th in (-TH, 0, TH):
    tot = [areas(s, th)['ah'] + areas(s, th)['ac'] for s in np.linspace(0, S_OPEN, 15)]
    assert all(b >= a - 1e-9 for a, b in zip(tot, tot[1:])), ('flow not monotonic', th); assert tot[0] == 0, ('not closed at s=0', th)
    print(f'theta {th:+.0f}: total inlet overlap s=0..{S_OPEN}:', [round(float(x), 1) for x in tot[::2]])
fr = []
for th in np.linspace(-TH, TH, 17):
    a = areas(S_OPEN, th); fr.append(a['ah'] / (a['ah'] + a['ac']))
assert all(b >= a - 1e-9 for a, b in zip(fr, fr[1:])), 'hot share not monotonic'
print('hot share vs theta -TH..TH:', [round(float(x), 2) for x in fr[::2]])
print('outlet joined when open (min mm2):', min(r[5] for r in rows if r[3] + r[4] > 0))
assert min(r[5] for r in rows if r[3] + r[4] > 0) > 5
s0 = [r for r in rows if T['inside'] < r[0] < T['lift_a']]; assert all(r[3] + r[4] == 0 for r in s0)
json.dump([r[:6] for r in rows], open('kin.json', 'w'))
json.dump(dict(T=T, LOOP=LOOP, FPS_K=FPS, RL=RL, HOTR=HOTR, COLDR=COLDR, OUTS=OUTS, PK=PK, EL=EL, S_OPEN=S_OPEN, TH=TH,
               AMAX=max(r[3] + r[4] for r in rows)), open('geom.json', 'w'), indent=1)
print('T', T)
