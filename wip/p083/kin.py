# p083 push-and-turn child-resistant cap "WHY DOES IT / JUST CLICK?" - kinematics + HARD GATE 5.2 checks
# mm, cap axis = y. Inner cap top surface at y = 0 (seated). Sawtooth ring on the inner cap top: h(th) = H * frac(N th / 2pi)
# (slope rises with +th, vertical stop face at each tooth boundary). The outer cap's underside ring is the same sawtooth, hanging down.
# phi = outer angle - inner angle. Outer underside at world angle th: lift + h(th - A_i - phi).
# Without a push the outer cap rides on the inner teeth: lift = max_th[h(th) - h(th - phi)] = H * frac(N phi / 2pi)  (rides up the slope, drops at the stop face = the click).
# With a push lift is held at 0 -> phi cannot change -> the outer cap drives the inner cap (both turn; the thread lifts both by PITCH per turn).
# Positive angle = counterclockwise seen from above = the opening direction.
import json, math
import numpy as np
FPS_K = 120
N, H = 10, 1.6                     # teeth on the ring, tooth height (exaggerated ~1.6x for the camera)
PITCH = 3.2                        # thread lead mm per turn
R_T0, R_T1 = 5.0, 13.0             # teeth ring radii
GAP = 0.6                          # outer top-wall underside sits H + GAP above the inner top when seated
INNER = dict(r_out=15.5, r_in=14.0, y_bot=-14.0, top=0.0, wall=2.0)
OUTER = dict(r_out=18.6, r_in=16.8, y_top=H + GAP + 2.5, y_bot=-17.0, lip_r=15.0, lip_top=-14.0 - H - 0.35)
NECK_R = 13.5
TP = 2 * math.pi / N
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def lin(t, a, b): return min(1, max(0, (t - a) / (b - a)))
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0}
T['vo1'] = 2.6; T['vo2'] = T['vo1'] + dur[1] + 0.3; T['vo3'] = T['vo2'] + dur[2] + 0.18; T['vo4'] = T['vo3'] + dur[3] + 0.3; T['vo5'] = T['vo4'] + dur[4] + 0.35
LOOP = round(T['vo5'] + dur[5] + 2.0, 2); T['LOOP'] = LOOP
K1, K2 = 5, 15                     # teeth slipped in the hook and in step 2/3 (K1 + K2 = 2N -> outer angle returns to 0 mod 2pi)
T['s1a'], T['s1b'] = 0.0, 2.45
T['exa'], T['exb'], T['exc'], T['exd'] = T['vo1'] + 0.25, T['vo1'] + 1.15, T['vo2'] - 0.95, T['vo2'] - 0.15
T['s2a'], T['s2b'] = T['vo2'] + 0.9, T['vo4'] - 0.05
T['push'] = T['vo4'] + 0.15; T['opa'], T['opb'] = T['vo4'] + 0.75, T['vo5'] + 0.6
T['offa'], T['offb'] = T['vo5'] + 0.6, T['vo5'] + 1.5
T['dna'], T['dnb'] = LOOP - 1.75, LOOP - 1.05; T['cla'], T['clb'] = LOOP - 1.05, LOOP - 0.05
OPEN_TURNS = 1.25; EX = 30.0; OFF = 16.0
def state(t):
    """inner angle A_i, phi, axial lift of the outer cap over the inner (play), rise of both caps (thread), push 0/1, explode height"""
    k = K1 * lin(t, T['s1a'], T['s1b']) + K2 * lin(t, T['s2a'], T['s2b'])          # constant turning speed while slipping
    phi = k * TP
    A_i = 2 * math.pi * OPEN_TURNS * (ease(lin(t, T['opa'], T['opb'])) - ease(lin(t, T['cla'], T['clb'])))
    rise = PITCH * A_i / (2 * math.pi) + OFF * (ease(lin(t, T['offa'], T['offb'])) - ease(lin(t, T['dna'], T['dnb'])))
    ex = EX * (ease(lin(t, T['exa'], T['exb'])) - ease(lin(t, T['exc'], T['exd'])))
    push = 1.0 if T['push'] <= t < T['opb'] + 0.2 else 0.0
    ride = H * (k - math.floor(k + 1e-9)) if push == 0 else 0.0
    return A_i, phi, max(ride, ex), rise, push, ex
rows = []
for i in range(int(LOOP * FPS_K) + 2):
    t = min(i / FPS_K, LOOP); A_i, phi, lift, rise, push, ex = state(t); rows.append([round(t, 4), round(A_i, 5), round(phi, 5), round(lift, 4), round(rise, 4), push, round(ex, 3)])
json.dump(rows, open('kin.json', 'w'))
# ---------------- checks (HARD GATE 5.2) over the whole loop ----------------
h = lambda th: H * np.mod(N * th / (2 * math.pi), 1.0)
th = np.linspace(0, 2 * math.pi, 7201)[:-1]
worst = 1e9; worst_lip = 1e9; turned_while_slip = 0
prev = None
for t in np.arange(0, LOOP, 1 / 120):
    A_i, phi, lift, rise, push, ex = state(t)
    inner_top = h(th - A_i); outer_bot = lift + h(th - A_i - phi)          # both in the inner cap frame (rise moves both together)
    worst = min(worst, (outer_bot - inner_top).min())
    worst_lip = min(worst_lip, INNER['y_bot'] - (OUTER['lip_top'] + lift)) if ex == 0 else worst_lip
    if prev is not None:
        dA = A_i - prev[0]; dphi = phi - prev[1]
        if push == 0 and abs(dA) > 1e-9 and t < T['cla']: turned_while_slip += 1     # inner cap may only turn while pushed (or when closing)
        if push == 1: assert abs(dphi) < 1e-9, ('outer slipped while pushed', t)
    prev = (A_i, phi)
print('teeth min clearance %.4f mm (0 = touching)' % worst); assert worst > -1e-6, 'outer teeth pass through the inner teeth'
print('retaining lip below the inner skirt by >= %.3f mm' % worst_lip); assert worst_lip > 0
assert turned_while_slip == 0, 'inner cap turned without a push'
# closing (end of loop): the outer turns clockwise, phi stays 0 mod pitch -> the stop faces drive the inner cap (no push needed)
A0 = state(0); A1 = state(LOOP - 1e-6)
print('loop: start', [round(v, 4) for v in A0], 'end', [round(v, 4) for v in A1])
assert abs((A1[1] - A0[1]) % (2 * math.pi)) < 1e-6 or abs((A1[1] - A0[1]) % (2 * math.pi) - 2 * math.pi) < 1e-6
assert abs(A1[0]) < 1e-6 and abs(A1[3]) < 1e-6
# radial clearances (static): outer skirt vs inner skirt, inner skirt vs neck, lip vs neck
assert OUTER['r_in'] > INNER['r_out'] and INNER['r_in'] > NECK_R and OUTER['lip_r'] > NECK_R and OUTER['lip_r'] < INNER['r_out']
print('clicks: hook %d, step 2-3 %d (one per tooth)' % (K1, K2))
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, N=N, H=H, PITCH=PITCH, R_T0=R_T0, R_T1=R_T1, GAP=GAP, INNER=INNER, OUTER=OUTER, NECK_R=NECK_R, K1=K1, K2=K2, EX=EX, OFF=OFF, OPEN_TURNS=OPEN_TURNS)
json.dump(G, open('geom.json', 'w'), indent=1)
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
