# p086 pop-up toaster "WHAT MAKES / THE TOAST POP?" - kinematics + HARD GATE 5.2 checks (front cut view, mm, y up)
# Carriage (tray + slider plate + steel armature plate + toast) slides on a vertical rod at the left. Ycar = tray height.
# A tension spring runs from a fixed anchor (y = YA) down to the slider top (Ycar + 30): it is stretched when the carriage is down.
# Pushing the lever moves the carriage down until the armature (bottom at Ycar - 4) sits on the electromagnet (top at YM).
# Power on -> the magnet holds the armature; a timer runs; when it ends the timer cuts the magnet current -> nothing holds -> the spring pulls the carriage up.
import json, math
import numpy as np
YM = 22.0                      # electromagnet top face
YD = YM + 4.0                  # carriage down (armature resting on the magnet)
YU = 126.0                     # carriage up (stop)
YA = 186.0                     # spring top anchor
SP_OFF = 20.0                  # spring attaches at slider top = Ycar + SP_OFF
TURNS, WIRE = 14, 1.6          # spring coil count, wire diameter -> coil-bound length
FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'pop0': 0.2, 'hookEnd': 1.0, 'vo1': 2.2, 'cut': 2.6}
T['push_a'] = 3.0; T['push_b'] = 3.7; T['touch'] = T['push_b']
T['vo2'] = T['vo1'] + dur[1] + 0.5
T['vo3'] = T['vo2'] + dur[2] + 0.4
T['vo4'] = T['vo3'] + dur[3] + 0.35
T['off'] = T['vo4'] + dur[4] - 0.05           # timer reaches zero -> magnet current cut
T['vo5'] = T['off'] + 0.15
T['rise_b'] = T['off'] + 0.05 + 0.9          # rise shown in slow motion (0.9 s)
T['vo6'] = T['vo5'] + dur[5] + 0.45
T['ext'] = T['vo6']                          # back to the outside view
LOOP = round(T['vo6'] + dur[6] + 2.3, 2); T['LOOP'] = LOOP
T['repush_a'] = LOOP - 1.25; T['repush_b'] = LOOP - 0.55
sm = lambda x: (lambda u: u * u * (3 - 2 * u))(min(1, max(0, x)))
def ycar(t):
    if t < T['pop0'] + 0.05: return YD
    if t < 0.62: return YD + (YU - YD) * (1 - (1 - (t - T['pop0'] - 0.05) / (0.62 - T['pop0'] - 0.05)) ** 3)
    if t < T['push_a']: return YU
    if t < T['push_b']: return YU - (YU - YD) * sm((t - T['push_a']) / (T['push_b'] - T['push_a']))
    if t < T['off'] + 0.05: return YD
    if t < T['rise_b']: u = (t - T['off'] - 0.05) / 0.9; return YD + (YU - YD) * (1 - (1 - u) ** 2.2)
    if t < T['repush_a']: return YU
    if t < T['repush_b']: return YU - (YU - YD) * sm((t - T['repush_a']) / (T['repush_b'] - T['repush_a']))
    return YD
def mag(t):   # magnet current on: from the moment the plate touches (switch closed) until the timer ends
    return 1 if (t < T['pop0']) or (T['touch'] <= t < T['off']) or (t >= T['repush_b']) else 0
def heat(t):  # element glow follows the power with a short warm-up / cool-down
    if T['touch'] <= t < T['off']: return sm((t - T['touch']) / 1.2)
    if t >= T['off']: return max(0.0, 1 - (t - T['off']) / 1.5) if t < T['off'] + 1.5 else 0.0
    return 0.0
def timer(t): # fraction of the toast time left
    if T['touch'] <= t < T['off']: return 1 - (t - T['touch']) / (T['off'] - T['touch'])
    return 0.0
rows = []
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; rows.append([round(t, 5), round(ycar(t), 4), mag(t), round(heat(t), 4), round(timer(t), 4)])
json.dump(rows, open('kin.json', 'w'))
# ---------------- HARD GATE 5.2 checks ----------------
y = np.array([r[1] for r in rows]); tt = np.array([r[0] for r in rows]); mg = np.array([r[2] for r in rows])
assert y.min() >= YD - 1e-9, 'armature passes into the magnet'
assert y.max() <= YU + 1e-9, 'carriage passes the top stop'
L = YA - (y + SP_OFF); Lcb = TURNS * WIRE
print('spring length %.1f .. %.1f mm (coil-bound %.1f)' % (L.min(), L.max(), Lcb)); assert L.min() > Lcb + 5
# the carriage only moves down while the lever is pushed (push windows), only moves up while the magnet is off
dy = np.diff(y)
for i in np.where(dy < -1e-6)[0]:
    t = tt[i]; assert (T['push_a'] - 1e-3 <= t <= T['push_b']) or (T['repush_a'] - 1e-3 <= t <= T['repush_b']), ('moved down without a push', t)
for i in np.where(dy > 1e-6)[0]:
    assert mg[i] == 0 and mg[i + 1] == 0, ('rose while the magnet holds', tt[i])
# while the magnet is on, the carriage is down (held)
assert all(abs(y[i] - YD) < 1e-6 for i in range(len(y)) if mg[i] == 1 and tt[i] >= T['touch'] + 1e-3 and tt[i] < T['repush_a']) 
# the magnet is only on when the plate touches it (switch closed at the bottom)
assert all(abs(y[i] - YD) < 1e-6 for i in range(len(y)) if mg[i] == 1)
# toast (125 tall) fully inside the 190 body when down, sticks out when up
assert YD + 125 < 190 - 5 and YU + 125 > 190 + 40
# loop: last frame state = first frame state
assert abs(y[0] - y[-1]) < 1e-6 and mg[0] == mg[-1]
print('checks PASS; LOOP %.2f' % LOOP)
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, YM=YM, YD=YD, YU=YU, YA=YA, SP_OFF=SP_OFF, TURNS=TURNS, WIRE=WIRE)
json.dump(G, open('geom.json', 'w'), indent=1)
print({k: round(v, 2) for k, v in T.items()})
