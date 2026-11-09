# p056 light switch: over-center snap. mm, 2D section (x = out of the wall, y = up), angles CCW positive.
# Lever pivots at A; its inner leg carries a spring-loaded plunger (axis d = -(cos phi, sin phi)) whose round tip
# presses on the copper contact bar, which rocks on a rod at B. Tip below B -> bar bottom goes in -> ON contact.
# The bar flips the moment the tip's contact point crosses B (t_c = 0): the spring, not the finger, drives the snap.
import json, math, numpy as np
G = dict(A=[-7.0, 0.0], B=[-24.0, 0.0], R_TIP=1.5, BAR_H=1.0, BAR_L=13.0, PHI_MAX=20.0, BETA_MAX=8.0,
         FLOOR=3.5, LP=7.0, HOUSE_END=12.0, HOUSE_W=2.8, BORE_R=1.9, PL_R=1.5, LEVER_W=2.5, SLOT=5.21, PLATE=[-2.5, 0.0],
         L0=7.0, LOOP=15.0)
A = np.array(G['A']); B = np.array(G['B']); r = G['R_TIP']; h = G['BAR_H']
def rot(v, a): c, s = math.cos(a), math.sin(a); return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])
def plunger_s(phi, beta):
    n = rot([1, 0], beta); d = -rot([1, 0], phi)
    return (r + h - n @ (A - B)) / (n @ d)
def tc(phi, beta):
    s = plunger_s(phi, beta); d = -rot([1, 0], phi); C = A + s * d; tau = rot([0, 1], beta); return (C - B) @ tau
# snap angle (going ON -> OFF the bar is at -BETA_MAX): solve tc(phi, -b) = 0
b = math.radians(G['BETA_MAX']); lo, hi = math.radians(-10), math.radians(10)
for _ in range(80):
    m = (lo + hi) / 2
    if tc(m, -b) > 0: lo = m
    else: hi = m
PHI_SNAP = (lo + hi) / 2  # tc>0 for smaller phi (tip above B)
G['PHI_SNAP_DEG'] = math.degrees(PHI_SNAP)
# timeline (s); VO-driven values patched from vo.json if present
T = dict(PUSH1=(1.0, 6.6), SNAP1=6.6, PUSH2=(10.6, 12.4), SNAP2=12.4)
try:
    T.update({k: tuple(v) if isinstance(v, list) else v for k, v in json.load(open('timeline.json')).items() if k in ('PUSH1','PUSH2','LOOP')})
except FileNotFoundError: pass
G['LOOP'] = T.get('LOOP', G['LOOP'])
PM = math.radians(G['PHI_MAX']); BM = b; TB, TL = 0.028, 0.065  # bar flip time, lever run-out time (spring-driven)
def ease_in(u, p=1.35): u = min(max(u, 0), 1); return u ** p
def state(t):
    t = t % G['LOOP']
    a0, a1 = T['PUSH1']; c0, c1 = T['PUSH2']
    if t < a0: return PM, -BM
    if t < a1: return PM - (PM - PHI_SNAP) * ease_in((t - a0) / (a1 - a0)), -BM
    if t < a1 + TL:
        u = (t - a1); be = -BM + 2 * BM * min(1, (u / TB) ** 2); ph = PHI_SNAP - (PHI_SNAP + PM) * (u / TL) ** 2; return ph, be
    if t < c0: return -PM, BM
    if t < c1: return -PM + (PM - PHI_SNAP) * ease_in((t - c0) / (c1 - c0)), BM
    if t < c1 + TL:
        u = (t - c1); be = BM - 2 * BM * min(1, (u / TB) ** 2); ph = -PHI_SNAP + (PHI_SNAP + PM) * (u / TL) ** 2; return ph, be
    return PM, -BM
rows = []
for i in range(int(G['LOOP'] * 240)):
    t = i / 240; ph, be = state(t); s = plunger_s(ph, be)
    rows.append(dict(phi=round(ph, 6), beta=round(be, 6), s=round(s, 5), spring=round(s - G['LP'] - G['FLOOR'], 5), tc=round(tc(ph, be), 4)))
json.dump(rows, open('kin_240.json', 'w'))
ev = [dict(type='snap_off', t=T['PUSH1'][1]), dict(type='bar_off', t=T['PUSH1'][1] + TB), dict(type='lever_off', t=T['PUSH1'][1] + TL),
      dict(type='snap_on', t=T['PUSH2'][1]), dict(type='bar_on', t=T['PUSH2'][1] + TB), dict(type='lever_on', t=T['PUSH2'][1] + TL),
      dict(type='push1', t=T['PUSH1'][0]), dict(type='push2', t=T['PUSH2'][0])]
json.dump(ev, open('events.json', 'w'), indent=1)
G['T'] = {k: v for k, v in T.items()}; json.dump(G, open('geom.json', 'w'), indent=1)
sp = [r_['spring'] for r_ in rows]
print('phi_snap %.2f deg, s range %.2f..%.2f, spring %.2f..%.2f mm' % (G['PHI_SNAP_DEG'], min(r_['s'] for r_ in rows), max(r_['s'] for r_ in rows), min(sp), max(sp)))
# loop check
print('loop closes:', rows[0]['phi'] == round(state(G['LOOP'] - 1e-9)[0], 6))
