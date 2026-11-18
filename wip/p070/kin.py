# p070 click pen: kinematics of the rotating-cam (push-push) mechanism in the UNROLLED cam plane.
# u = angle around the pen axis (deg), y = height along the axis (mm, up = toward the button). Y0 = lowest point of the barrel ridges.
# Barrel ridges (fixed): 8 cells of T = 45 deg. Each ridge end is a slope rising +h over T, ending at a vertical wall.
#   even cells = SHORT LEDGE (the cam lug stops in the top corner -> refill held forward = tip OUT)
#   odd cells  = LONG SLOT next to the wall (the lug slides up into it -> refill goes back = tip IN)
# Plunger (button, does not turn): sawtooth edge, same slope, offset by T/2. Cam (rotor + refill): 4 lugs, 90 deg apart, top sloped like the teeth.
# Spring (around the refill near the nose) pushes the refill + cam UP; a small button spring pushes the plunger up to its stop.
# Each click: press -> the lug is pushed below the ridge ends (P < Y0 - h/2) and slides along the plunger slope (+T/2);
# release -> it rides up, hits the next ridge slope, and slides along it (+T/2 more) into a ledge or a slot. 4 clicks = 180 deg = one loop (4-fold cam).
import json, math
T, H, C, W_LUG, LH = 45.0, 1.2, 1.5, 18.0, 2.2
S = H / T; Y0 = 0.0; PREST = 3.6; PBOT = -0.8; PSNAP = -0.68; GT = 7.0; TOP = 8.0
Y_OUT = Y0 + H; Y_IN = PREST + H / 2 - S * C
FPS = 60; LOOP = 25.6
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(max(0.0, min(1.0, u)))
# clicks: (press start, press dur, snap dur, release start, release dur, slide dur, rise dur)
CL = [(0.05, 0.24, 0.07, 0.34, 0.22, 0.07, 0.10),     # A: hook, IN -> OUT
      (2.45, 0.24, 0.07, 2.75, 0.22, 0.07, 0.14),     # B: wide, OUT -> IN
      (8.55, 2.20, 0.75, 12.35, 0.95, 0.90, 0.40),    # C: step 1 (slow), IN -> OUT
      (15.95, 1.35, 0.55, 17.75, 0.80, 0.75, 1.60)]   # D: step 2 (slow), OUT -> IN
def plunger(t):
    for (tp, pd, sd, tr, rd, sl, ri) in CL:
        if tp <= t < tr: return PREST + (PBOT - PREST) * sm((t - tp) / pd)
        if tr <= t < tr + rd: return PBOT + (PREST - PBOT) * sm((t - tr) / rd)
    return PREST
def tcross(f, t0, t1, level, down=True):
    # first time in [t0,t1] where f crosses level
    n = 4000
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        if (f(t) <= level) if down else (f(t) >= level): return t
    raise ValueError('no crossing')
# lug states: (u_r, y, state) piecewise through every click
state = {'u': -C, 'y': Y_IN, 'st': 'IN'}
segs = []
for (tp, pd, sd, tr, rd, sl, ri) in CL:
    u0, y0, st0 = state['u'], state['y'], state['st']
    Wl = u0 if st0 == 'OUT' else u0 + C        # right wall of the current cell
    groove_next = (round(Wl / T) % 2 == 1)      # cell [Wl, Wl+T): odd index = slot
    Cp = Wl - T / 2                             # start of the plunger cell above the lug
    ts = tcross(plunger, tp, tp + pd, PSNAP)
    ta = tcross(plunger, tr, tr + rd, Y0 - H / 2, down=False)      # lug meets the next ridge slope
    tq = tcross(plunger, tr, tr + rd, Y0 + H / 2 + 0.05, down=False) # plunger tooth clears the lug corner -> slide
    seg = dict(tp=tp, ts=ts, sd=sd, tr=tr, ta=ta, tq=tq, sl=sl, ri=ri, u0=u0, y0=y0, Wl=Wl, Cp=Cp, groove=groove_next)
    uend = Wl + T - C if groove_next else Wl + T
    seg['uend'] = uend; segs.append(seg)
    state = {'u': uend, 'y': Y_IN if groove_next else Y_OUT, 'st': 'IN' if groove_next else 'OUT'}
def lug(t):
    u, y, st = -C, Y_IN, 'IN'
    for g in segs:
        if t < g['tp']: return u, y, st
        P = plunger(t)
        if t < g['tr']:
            if t < g['ts']: return g['u0'], min(g['y0'], P + S * (g['u0'] - g['Cp'])), st
            ur = g['u0'] + (g['Wl'] + T / 2 - g['u0']) * sm((t - g['ts']) / g['sd'])
            return ur, P + S * (ur - g['Cp']), 'PRESS'
        ur = g['Wl'] + T / 2
        if t < g['tq']: return ur, min(P + H, Y0 + H / 2), 'PRESS'
        sl_end = g['tq'] + g['sl']
        if t < sl_end:
            ur = ur + (g['uend'] - ur) * sm((t - g['tq']) / g['sl']); return ur, Y0 + S * (ur - g['Wl']), 'SLIDE'
        if g['groove']:
            yb = Y0 + S * (g['uend'] - g['Wl']); yr = yb + (Y_IN - yb) * sm((t - sl_end) / g['ri'])
            e2 = S * (g['uend'] - (g['Wl'] + T / 2))
            y = min(yr, P + e2)
            if t < sl_end + g['ri']: return g['uend'], y, 'RISE'
            u, y, st = g['uend'], Y_IN, 'IN'
        else: u, y, st = g['uend'], Y_OUT, 'OUT'
    return u, y, st
rows = []
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; P = plunger(t); u, y, st = lug(t); y -= 0.0005   # 0.5 um clearance: contacts touch, never overlap
    rows.append([round(t, 4), round(P, 6), round(u, 6), round(y, 6), {'IN': 0, 'OUT': 1, 'PRESS': 2, 'SLIDE': 3, 'RISE': 4}[st]])
json.dump(rows, open('kin.json', 'w'))
EV = dict(vo=[0.15, 1.45, 4.8, 8.4, 12.35, 15.9, 18.95, 21.1], clicks=[[g['tp'], g['ts'], g['tr'], g['tq']] for g in segs],
          snaps=[g['ts'] for g in segs], ledge=[g['tq'] + g['sl'] for g in segs], cut=1.0)
G = dict(T=T, H=H, C=C, W_LUG=W_LUG, LH=LH, S=S, Y0=Y0, PREST=PREST, PBOT=PBOT, GT=GT, TOP=TOP, Y_OUT=Y_OUT, Y_IN=Y_IN, LOOP=LOOP, FPS_K=FPS, EV=EV)
json.dump(G, open('geom.json', 'w'), indent=1)
print('Y_IN', round(Y_IN, 3), 'Y_OUT', Y_OUT, 'travel', round(Y_IN - Y_OUT, 3))
for g in segs: print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in g.items()})
print('end u', rows[-1][2], 'start u', rows[0][2], 'y', rows[-1][3], rows[0][3])
