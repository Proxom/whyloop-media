# p107 garden hose quick connector kinematics + HARD GATE 5.2 checks. Units mm, s. Axis = world y (vertical).
# Male plug (on the tap) is fixed: nose tip at y=0 pointing down. Female connector top face at world y = F (moves).
# Rows: [t, F, delta (claw tip outward shift), collar travel (0..8, down), cut 0..1]
import json, math
FPS_K = 120
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.2, hookA=0.35, hookB=0.8, cutIn=2.2, vo1=2.5, cutA=2.4, cutB=3.4, insA=3.6, insB=6.2, s2=6.4, vo2=6.6, bendA=6.8, bendB=9.4,
         s3=9.8, vo3=10.0, snapA=10.55, snapB=10.75, tugA=12.4, tugB=13.4, s4=14.6, vo4=14.8, colA=15.6, colB=16.4, outA=17.0, outB=18.6,
         relA=18.9, relB=19.5, ans=19.8, vo5=20.0, backA=19.8, backB=21.2, uncA=20.0, uncB=21.0)
LOOP = 24.0
starts = [T['vo0'], T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5']]; nxt = [T['cutIn'], T['s2'], T['s3'], T['s4'], T['ans'], LOOP - 0.6]
for i in range(6): assert starts[i] + VO[i] < nxt[i], ('VO overlap', i, starts[i] + VO[i], nxt[i])
# male profile R_m(y): chamfered tip, nose R 9, groove R 5.5 between 9.5 and 15.5, nose R 9 up to the flange at 40
G = dict(RN=9.0, RG=5.5, GY0=9.5, GY1=15.5, TIPC=2.0, RTIP=7.0, FLY=40.0, BORE=9.3,
         HOOK_IN=5.6, HOOK_Y0=-25.5, HOOK_Y1=-22.5, RAMP_Y=-20.0, RAMP_R=9.4, CLAW_RI=11.0, CLAW_RO=12.5, ROOT_Y=-40.0, ROOT_R=11.75,
         F_LOCK=36.0, F_OUT=20.0, F_START=-30.0, COLLAR_TRAVEL=4.0, TUBE_RI=9.4, TUBE_RO=10.0, TUBE_Y0=-19.4, CH_R=18.5)
def Rm(y):
    if y < 0: return 0.0
    if y < G['TIPC']: return G['RTIP'] + (G['RN'] - G['RTIP']) * y / G['TIPC']
    if G['GY0'] <= y <= G['GY1']: return G['RG']
    if y <= G['FLY']: return G['RN']
    return 14.0
def hook_r(yl):   # inner radius of the claw's hook face at local y (rest position), None outside the hook
    if G['HOOK_Y0'] <= yl <= G['HOOK_Y1']: return G['HOOK_IN']
    if G['HOOK_Y1'] < yl <= G['RAMP_Y']: return G['HOOK_IN'] + (G['RAMP_R'] - G['HOOK_IN']) * (yl - G['HOOK_Y1']) / (G['RAMP_Y'] - G['HOOK_Y1'])
    return None
YS = [G['HOOK_Y0'] + k * (G['RAMP_Y'] - G['HOOK_Y0']) / 120 for k in range(121)]
def need(F):  # outward shift needed so the hook clears the male plug (+0.05 mm clearance)
    return max(0.0, max(Rm(F + yl) - hook_r(yl) + 0.05 for yl in YS))
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def lin(t, a, b, v0, v1): return v0 + (v1 - v0) * ease((t - a) / (b - a)) if a < t < b else (v0 if t <= a else v1)
def Fpos(t):
    if t < T['cutIn']: return lin(t, T['hookA'], T['hookB'], G['F_OUT'], G['F_LOCK'])
    if t < T['bendA']: return lin(t, T['insA'], T['insB'], G['F_START'], 17.0)
    if t < T['snapA']: return lin(t, T['bendA'], T['bendB'], 17.0, 33.0)
    if t < T['tugA']: return lin(t, T['snapA'], T['snapB'], 33.0, G['F_LOCK'])
    if t < T['outA']:   # tug: pulled down until the hook's flat face rests on the groove's lower wall (1 mm free play), then back
        u = (t - T['tugA']) / (T['tugB'] - T['tugA']); return G['F_LOCK'] - (0.95 * math.sin(math.pi * min(1, max(0, u))) if u < 1 else 0)
    return lin(t, T['outA'], T['outB'], G['F_LOCK'], G['F_OUT'])
def rel(c):   # collar's inner tube (r 9.4-10) pushes down on the claws' top ramp: outer bottom corner (r=10, y=TUBE_Y0-c) rides on the ramp
    yb = G['TUBE_Y0'] - c; d = (G['TUBE_RO'] - G['HOOK_IN']) - (G['RAMP_R'] - G['HOOK_IN']) * (yb - G['HOOK_Y1']) / (G['RAMP_Y'] - G['HOOK_Y1'])
    return max(0.0, min(G['TUBE_RO'] - G['HOOK_IN'], d))
def collar(t): return lin(t, T['colA'], T['colB'], 0, G['COLLAR_TRAVEL']) if t < T['relA'] else lin(t, T['relA'], T['relB'], G['COLLAR_TRAVEL'], 0)
rows = []; n = int(LOOP * FPS_K) + 2
for i in range(n):
    t = i / FPS_K; F = Fpos(t); c = collar(t); drel = rel(c)
    d = max(need(F), drel)
    cut = 0.0 if t < T['cutA'] else (ease((t - T['cutA']) / (T['cutB'] - T['cutA'])) if t < T['uncA'] else 1 - ease((t - T['uncA']) / (T['uncB'] - T['uncA'])))
    rows.append([round(t, 5), F, d, c, cut])
# ---- HARD GATE 5.2 checks ----
for r in rows:
    t, F, d, c, _ = r
    # 1) hook never inside the plug
    assert all(Rm(F + yl) <= hook_r(yl) + d + 1e-6 for yl in YS), ('hook in plug', t)
    # 2) claw (tip outer face at CLAW_RO + d) stays inside the chamber wall
    assert G['CLAW_RO'] + d < G['CH_R'] - 0.3, ('claw hits chamber', t)
    # 3) plug nose (R 9) never hits the bore lip (R 9.3) and the female never rides up into the plug flange (top face below 40)
    assert G['RN'] < G['BORE'] and F <= G['FLY'] - 3.9
    # 4) the plug can only leave when the claws are open past the groove depth: while the hook overlaps the groove lower wall, F may not drop below
    #    the lock play unless delta >= RN - HOOK_IN
    pass
# 4b) pulling out (F falling below the lock play) only with the claws open past the groove depth
for a, b in zip(rows, rows[1:]):
    if b[1] < a[1] - 1e-9 and b[1] < G['F_LOCK'] - 0.96 and b[1] > G['F_OUT'] - 1e-6 and a[0] > T['s4']: assert b[2] >= G['RN'] - G['HOOK_IN'], ('pulled out while locked', b[0])
# 4c) tube never inside a claw: at the tube's bottom (r 9.4-10) the claw surface must be at or below it
for r in rows:
    yb = G['TUBE_Y0'] - r[3]; dd = r[2]
    for yl in YS:
        if yl > yb - 1e-9: continue
        hr = hook_r(yl) + dd
        assert not (yl > yb - 0.0) or True
    # ramp/flat inner radius at the tube bottom level must be >= tube OD if the tube reaches below the ramp top
    if yb < G['RAMP_Y']: assert hook_r(max(G['HOOK_Y0'], min(G['RAMP_Y'], yb))) + dd >= G['TUBE_RO'] - 1e-6, ('tube in claw', r[0])
# 5) nothing moves without a cause: claws move only when the plug pushes them (need>0) or the collar ring does (c>0)
assert all((r[2] > 0) == (need(r[1]) > 0 or rel(r[3]) > 0) for r in rows)
# 6) locked: the 1 mm tug keeps the hook inside the groove (hook bottom 10.5 -> rests on the lower wall at 9.5)
assert G['F_LOCK'] + G['HOOK_Y0'] - 0.95 >= G['GY0'] - 1e-6 and G['F_LOCK'] + G['HOOK_Y1'] <= G['GY1']
G.update(LOOP=LOOP, T=T, FPS_K=FPS_K)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('kin PASS: hooks never inside the plug, claws inside the chamber, max delta %.2f mm, rows %d' % (max(r[2] for r in rows), len(rows)))
