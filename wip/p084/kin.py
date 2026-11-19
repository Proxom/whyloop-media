# p084 single-lever mixer tap cartridge "ONE LEVER: / HOT OR COLD?" - geometry, timeline, kinematics + HARD GATE 5.2 checks.
# 2D disc plane (u right, v away from the viewer), mm. Lower (inlet) disc fixed: HOT inlet (left), COLD inlet (right), OUTLET slot (front).
# Upper (control) disc: lever holder turns it by theta about the cartridge axis; the lever tilt slides it by s along the holder.
#   p_world = R(theta) * (p_frame + (0, s)). Its underside pocket joins the inlets it covers to the outlet (US 9,115,819 B2 figs 9-11).
import json, math
import numpy as np
D2R = math.pi / 180
RL = 20.0                                   # lower disc radius
HOT, COLD, RI = (-5.0, 5.2), (5.0, 5.2), 3.0 # inlet centres + radius
OUT = (-8.0, -10.0, 8.0, -4.0)              # outlet slot (u0, v0, u1, v1), rounded ends
PK = (-4.2, -16.5, 4.2, 0.0, 2.5)           # pocket in the control-disc frame (u0, v0, u1, v1, corner r)
EL = (0.0, -3.0, 15.0, 20.0)                # control disc outline: ellipse centre (u,v) + semi-axes, frame coords
S_OPEN, TH = 7.0, 32.0
G = 0.05; uu, vv = np.meshgrid(np.arange(-26, 26, G), np.arange(-26, 26, G))
def rr_in(u, v, b):
    u0, v0, u1, v1, r = b; cu = np.clip(u, u0 + r, u1 - r); cv = np.clip(v, v0 + r, v1 - r)
    return ((u - cu) ** 2 + (v - cv) ** 2 <= r * r) & (u >= u0) & (u <= u1) & (v >= v0) & (v <= v1)
def to_frame(s, th):
    c, sn = math.cos(-th * D2R), math.sin(-th * D2R); return c * uu - sn * vv, sn * uu + c * vv - s
def areas(s, th):
    fu, fv = to_frame(s, th); pk = rr_in(fu, fv, PK)
    hot = (uu - HOT[0]) ** 2 + (vv - HOT[1]) ** 2 <= RI * RI; cold = (uu - COLD[0]) ** 2 + (vv - COLD[1]) ** 2 <= RI * RI
    out = rr_in(uu, vv, (*OUT, 3.0)); ell = ((fu - EL[0]) / EL[2]) ** 2 + ((fv - EL[1]) / EL[3]) ** 2 <= 1
    return dict(ah=(pk & hot).sum() * G * G, ac=(pk & cold).sum() * G * G, ao=(pk & out).sum() * G * G,
                leak=((hot | cold) & ~ell).sum() * G * G, pk_out=(pk & ~ell).sum() * G * G)
# ---------------- timeline (VO-driven) ----------------
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
starts = [0.95, 3.15]; 
for d in VO[1:-1]: starts.append(round(starts[-1] + VO[len(starts) - 1] + 0.22, 2))
T = {f'vo{i}': starts[i] for i in range(7)}; T['hookEnd'] = 0.9
T['inside'] = T['vo1'] - 0.15; T['outside'] = T['vo6'] - 0.12
T['lift_a'] = T['vo4'] + 0.5; T['lift_b'] = T['lift_a'] + 2.4
T['hot_a'] = T['vo5'] + 0.3; T['hot_b'] = T['hot_a'] + 1.2; T['cold_a'] = T['hot_b'] + 0.4; T['cold_b'] = T['cold_a'] + 1.5
LOOP = round(T['vo6'] + VO[6] + 1.6, 2); T['LOOP'] = LOOP
sm = lambda x: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, x)))
def state(t):
    if t < T['hookEnd']: return S_OPEN, -TH + 2 * TH * sm((t - 0.1) / 0.7)
    if t < T['inside']:
        th = TH * (1 - sm((t - 1.1) / 0.8)); s = S_OPEN * (1 - sm((t - 2.0) / 0.8)); return s, th
    if t < T['lift_a']: return 0.0, 0.0
    if t < T['hot_a']: return S_OPEN * sm((t - T['lift_a']) / (T['lift_b'] - T['lift_a'])), 0.0
    if t < T['cold_a']: return S_OPEN, TH * sm((t - T['hot_a']) / (T['hot_b'] - T['hot_a']))
    return S_OPEN, TH - 2 * TH * sm((t - T['cold_a']) / (T['cold_b'] - T['cold_a']))
FPS = 30; rows = []
for i in range(int(LOOP * FPS) + 2):
    t = i / FPS; s, th = state(t); a = areas(s, th); rows.append([round(t, 4), round(s, 4), round(th, 4), round(a['ah'], 3), round(a['ac'], 3), round(a['ao'], 3), a['leak'], a['pk_out']])
# ---------------- HARD GATE 5.2 checks ----------------
leak = max(r[6] for r in rows); pko = max(r[7] for r in rows); print('max inlet area outside the control disc (must be 0):', leak, '| pocket outside disc:', pko)
assert leak == 0 and pko == 0
for th in (-TH, 0, TH):
    tot = [areas(s, th)['ah'] + areas(s, th)['ac'] for s in np.linspace(0, S_OPEN, 15)]
    assert all(b >= a - 1e-9 for a, b in zip(tot, tot[1:])), ('flow not monotonic', th); assert tot[0] == 0, ('not closed at s=0', th)
    print(f'theta {th:+.0f}: total inlet overlap s=0..{S_OPEN}:', [round(x, 1) for x in tot[::2]])
fr = []
for th in np.linspace(-TH, TH, 17):
    a = areas(S_OPEN, th); fr.append(a['ah'] / (a['ah'] + a['ac']))
assert all(b >= a - 1e-9 for a, b in zip(fr, fr[1:])), 'hot share not monotonic'
print('hot share vs theta -TH..TH:', [round(x, 2) for x in fr[::2]])
print('outlet always joined when open:', min(r[5] for r in rows if r[3] + r[4] > 0))
s0 = [r for r in rows if T['inside'] < r[0] < T['lift_a']]; assert all(r[3] + r[4] == 0 for r in s0)
json.dump([r[:6] for r in rows], open('kin.json', 'w'))
json.dump(dict(T=T, LOOP=LOOP, FPS_K=FPS, RL=RL, HOT=HOT, COLD=COLD, RI=RI, OUT=OUT, PK=PK, EL=EL, S_OPEN=S_OPEN, TH=TH,
               AMAX=max(r[3] + r[4] for r in rows)), open('geom.json', 'w'), indent=1)
print('T', T)
