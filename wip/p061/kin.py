# p061 bike quick release: why does it stay shut? Over-center eccentric cam. mm, x = axle axis (outward), y up, z = toward the bike's front (viewer).
# Lever angle gamma = degrees from the wheel plane (95 open, 0 closed alongside the fork). Cam offset direction beta = 188 - gamma (deg, from +x).
# Cam disc radius R about centre C = pin + E(cos b, sin b); it pushes the follower face of the cam body (contact = leftmost cam point).
# Loose: the conical spring keeps the cam body on the cam, the pin stays. After the body touches the dropout (x = 0) the pin moves out
# (rod stretches, clamp force F ~ pin travel). Peak at beta 180 (gamma 8); closed at gamma 0 the squeeze is 98 % of peak (over the top).
import json, math
E, R, FOL, CLR = 1.8, 6.2, 7.0, 0.02   # eccentricity, cam radius, follower thickness, cam-face clearance
LOOP, HZ = 17.0, 240
def ss(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
def ease_out(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def ease_in(u): u = max(0, min(1, u)); return u ** 2
# gamma schedule (t0, t1, g0, g1, ease)
SEG = [(0, 3.0, 95, 95, ss), (3.0, 4.8, 95, 70, ss), (4.8, 8.4, 70, 12, ss), (8.4, 9.4, 12, 8.0, ss), (9.4, 9.62, 8.0, 0, ease_in),
       (9.62, 10.8, 0, 0, ss), (10.8, 11.3, 0, 4.0, ss), (11.3, 11.5, 4.0, 0, ease_in), (11.5, 13.3, 0, 0, ss),
       (13.3, 14.0, 0, 8.0, ss), (14.0, 14.8, 8.0, 95, ease_out), (14.8, LOOP, 95, 95, ss)]
def gamma(t):
    for a, b, g0, g1, f in SEG:
        if a <= t <= b: return g0 + (g1 - g0) * f((t - a) / (b - a))
    return 95
PIN_C = FOL + R + CLR - E * math.cos(math.radians(118))   # pin x when the body first touches the dropout (gamma 70)
def pose(t):
    g = gamma(t); b = math.radians(188 - g)
    face_free = PIN_C + E * math.cos(b) - R - CLR          # follower face if the pin stays put
    if face_free >= FOL: pin, x0 = PIN_C, face_free - FOL     # loose: body rides on the cam, gap x0 to the dropout
    else: pin, x0 = FOL + R + CLR - E * math.cos(b), 0.0     # clamped: body on the dropout, pin pulled out
    F = (pin - PIN_C) / (E * (1 + math.cos(math.radians(118))))  # 1.0 at the peak
    return dict(t=round(t, 5), g=round(g, 4), b=round(188 - g, 4), pin=round(pin, 5), x0=round(x0, 5), F=round(F, 5))
K = [pose(i / HZ) for i in range(int(LOOP * HZ) + 1)]
EV = [dict(type='touch', t=None), dict(type='peak', t=None)]
for a, b in zip(K, K[1:]):
    if a['x0'] > 0 and b['x0'] == 0 and EV[0]['t'] is None: EV[0]['t'] = b['t']
    if a['g'] > 8 >= b['g'] and EV[1]['t'] is None: EV[1]['t'] = b['t']
EV += [dict(type='thunk', t=9.62, gain=1.0), dict(type='thunk', t=11.5, gain=0.6),
       dict(type='squeeze', t0=EV[0]['t'], t1=9.4), dict(type='release', t=next(k['t'] for k in K if k['t'] > 13.3 and k['x0'] > 0)),
       dict(type='swing', t0=3.0, t1=4.8), dict(type='swing', t0=14.0, t1=14.8)]
json.dump(dict(E=E, R=R, FOL=FOL, LOOP=LOOP, HZ=HZ, PIN_C=PIN_C, K=K), open('kin_240.json', 'w'))
json.dump(EV, open('events.json', 'w'), indent=1)
pk = max(k['F'] for k in K); cl = [k for k in K if abs(k['t'] - 10.0) < 1e-6][0]
print('PIN_C', round(PIN_C, 3), 'open gap', K[0]['x0'], 'peak F', pk, 'closed F', cl['F'], 'events', EV[:2])
