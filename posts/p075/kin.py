# p075 kettle auto switch-off - kinematics. Side section: x to the right (handle side), y up, mm.
# Bimetal strip: fixed at x = SX0, length SL, steel layer on top, copper below (copper expands more -> the free end bends UP).
# The rod (x = XR) stands on the strip and lifts the rocker arm (pivot PR); past the toggle point the spring snaps the rocker to OFF.
import json, math
SX0, SL, XR = 105.0, 40.0, 142.0
S_ROD = XR - SX0                    # rod sits 37 mm along the strip
STRIP_TOP0 = 36.0
ROD_LEN = 11.25
PR = (130.0, 51.25); ARM_HT = 1.25
PSI_ON, PSI_TRIP, PSI_OFF = -6.0, -2.0, 12.0
D_MAX = 5.0                          # strip lift at the rod for full heat (mm)
def arm_under(psi): return PR[1] + (XR - PR[0]) * math.tan(math.radians(psi)) - ARM_HT / math.cos(math.radians(psi))
def rod_top(d): return STRIP_TOP0 + d + ROD_LEN
FPS = 60
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ramp(t, a, b): return smooth((t - a) / (b - a))
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
GAP = [0, 0.1, 0.3, 0.3, 0.3, 0.3, 0.7]
T = {'vo0': 0.15}; T['hookEnd'] = T['vo0'] + D[0] + 0.15; T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = T[f'vo{i-1}'] + D[i - 1] + GAP[i]
LOOP = round(T['vo6'] + D[6] + 1.3, 1); T['LOOP'] = LOOP
T['on1'] = T['vo1'] + 0.35
H0 = 0.25                            # hook starts warm (flash-forward of the click)
def heat(t):
    if t < T['hookEnd']: return H0 + (1 - H0) * ramp(t, 0.25, 1.1)
    if t < T['vo2'] - 0.05: return ramp(t, T['vo1'] + 1.0, T['vo1'] + 2.3)
    if t < T['vo3']: return 0.0
    if t < T['vo4']: return 0.3 * ramp(t, T['vo3'] + 0.6, T['vo4'])
    if t < T['vo5']: return 0.3 + 0.12 * ramp(t, T['vo4'] + 0.2, T['vo5'])
    if t < LOOP - 1.0: return 0.42 + 0.58 * ramp(t, T['vo5'] + 0.3, T['vo5'] + 1.6)
    return 1 - (1 - H0) * ramp(t, LOOP - 1.0, LOOP - 0.55)
def user_on(t):      # times when a finger has just pushed the paddle down to ON (rocker forced to PSI_ON)
    return (t < T['hookEnd'] and t < 0.05) or (T['hookEnd'] <= t and abs(t - T['on1']) < 0.2) or (T['vo2'] - 0.05 <= t < T['vo2'] + 0.05) or (t >= LOOP - 0.5)
rows = []; psi = PSI_ON; power = 1; snapping = 0.0; T['snaps'] = []
prev_off = False
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; h = heat(t); d = D_MAX * h; rt = rod_top(d)
    if t >= T['hookEnd'] and t < T['on1'] - 0.2 and i > 0 and rows[-1][0] < T['hookEnd']: psi = PSI_OFF; power = 0   # after the hook: start OFF and cool
    if (abs(t - T['vo2']) < 0.01 or abs(t - (LOOP - 0.5)) < 0.01) and h < 0.29: psi = PSI_ON; power = 1
    if user_on(t) and h < 0.29:
        psi = max(PSI_ON, psi - 18.0 / (0.15 * FPS)) if psi > PSI_ON else PSI_ON; power = 1 if psi <= PSI_ON + 1e-6 else power
    if power == 1:
        lo, hi = -30.0, 30.0
        for _ in range(60):
            m = (lo + hi) / 2
            if arm_under(m) < rt: lo = m
            else: hi = m
        need = hi                                                   # arm angle that just rests on the rod top
        psi = max(PSI_ON, need)
        if psi >= PSI_TRIP: power = 0; T['snaps'].append(round(t, 3))
    else:
        if psi < PSI_OFF and not user_on(t): psi = min(PSI_OFF, psi + 18.0 / (0.08 * FPS))
    au = arm_under(psi)
    assert rt <= au + 1e-6, (t, rt, au, psi)                          # the rod never enters the rocker arm
    if power == 1 and psi > PSI_ON + 1e-6: assert abs(rt - au) < 1e-3   # while it lifts the arm, they touch
    boil = 0.0
    rows.append([round(t, 4), round(h, 4), round(d, 4), round(psi, 4), power])
# boiling intensity follows power with a lag (bubbles fade over 1.5 s after the cut, start 1 s after switch-on)
b = 0.0; out = []
for r in rows:
    t = r[0]; target = 1.0 if r[4] == 1 and not (T['hookEnd'] <= t < T['on1'] + 0.4) else 0.0
    if t < 0.02 or abs(t - T['vo2']) < 0.02: b = 1.0
    b += (target - b) * min(1, (1.6 if target else 1.4) / FPS)
    out.append(r + [round(b, 4)])
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, SX0=SX0, SL=SL, XR=XR, S_ROD=S_ROD, STRIP_TOP0=STRIP_TOP0, ROD_LEN=ROD_LEN, PR=PR, ARM_HT=ARM_HT, PSI_ON=PSI_ON, PSI_OFF=PSI_OFF, D_MAX=D_MAX)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(out, open('kin.json', 'w'))
print('PASS', {k: T[k] for k in T if k != 'snaps'}, 'snaps', T['snaps'])
