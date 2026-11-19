# p083 push-and-turn child-resistant cap "WHY DOES IT / JUST CLICK?" - kinematics + HARD GATE 5.2 checks (v2: spring + flat drive lugs)
# mm, cap axis = y. Inner cap top surface at y = 0 (seated). Two features between the cap tops (patents US 11104494 B2, US 11279530 B2, US 8857638 B2):
#  1. SLOPED TEETH ring (r 5-10.5): h(th) = H * frac(N th / 2pi) on the inner cap; the outer cap carries the same saw ring hanging down.
#  2. FLAT DRIVE LUGS ring (r 11.5-14.5): inner lugs stand LH high, outer lugs hang LO down; their flat faces only overlap when the outer cap is pushed down.
#  A spring holds the outer cap up by G0 (rest). At rest the steep tooth faces still overlap by H - G0 (closing: they catch, both caps turn, no push);
#  turning to open, the outer teeth ride up the slopes (lift up to H) and drop back to G0 = the click, the inner cap does not turn.
#  Pushed: lift 0 -> the flat lugs overlap by G0 - LUG_CLR and lock -> the outer cap drives the inner cap off the thread.
# phi = outer - inner angle. Positive angle = counterclockwise seen from above = the opening direction.
import json, math
import numpy as np
FPS_K = 120
N, H = 10, 2.4                     # teeth on the ring, tooth height (exaggerated for the camera)
G0 = 1.6                           # spring holds the outer cap this high above the pushed position
LUG_CLR = 0.5                      # lug clearance at rest
PITCH = 3.2                        # thread lead mm per turn
R_T0, R_T1 = 5.0, 10.5             # sloped teeth ring
R_L0, R_L1 = 11.5, 14.5            # lug ring
GAP = 0.6                          # outer top-wall underside sits H + GAP above the inner top when pushed (lift 0)
UND = H + GAP
LH = 1.4                           # inner lug height
LO = UND - LH + G0 - LUG_CLR       # outer lug length -> lug overlap when pushed = G0 - LUG_CLR
WL = math.radians(9.0)             # lug width (angle); inner lug [k TP, k TP + WL], outer lug [k TP - WL, k TP] in their own frames
INNER = dict(r_out=15.5, r_in=14.0, y_bot=-14.0, top=0.0, wall=2.0)
OUTER = dict(r_out=18.6, r_in=16.8, y_top=UND + 2.5, y_bot=-17.0, lip_r=15.0, lip_top=-14.0 - H - 0.35)
NECK_R = 13.5
TP = 2 * math.pi / N
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def lin(t, a, b): return min(1, max(0, (t - a) / (b - a)))
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0}
T['vo1'] = 2.6; T['vo2'] = T['vo1'] + dur[1] + 0.3; T['vo3'] = T['vo2'] + dur[2] + 0.18; T['vo4'] = T['vo3'] + dur[3] + 0.3
T['vo5'] = T['vo4'] + dur[4] + 0.35; T['vo6'] = T['vo5'] + dur[5] + 0.3
LOOP = round(T['vo6'] + dur[6] + 1.95, 2); T['LOOP'] = LOOP
K1, K2 = 5, 15                     # teeth slipped in the hook and in step 2/3 (K1 + K2 = 2N -> outer angle returns to 0 mod 2pi)
T['s1a'], T['s1b'] = 0.0, 2.45
T['exa'], T['exb'], T['exc'], T['exd'] = T['vo1'] + 0.25, T['vo1'] + 1.15, T['vo2'] - 0.95, T['vo2'] - 0.15
T['s2a'], T['s2b'] = T['vo2'] + 0.9, T['vo4'] - 0.05
T['pda'], T['pdb'] = T['vo4'] + 0.25, T['vo4'] + 0.7          # pushed down (spring compressed, lugs drop in)
T['opa'], T['opb'] = T['vo4'] + 1.1, T['vo5'] + 0.1
T['pua'], T['pub'] = T['opb'] + 0.05, T['opb'] + 0.35          # push released
T['offa'], T['offb'] = T['vo5'] + 0.4, T['vo5'] + 1.3
T['dna'], T['dnb'] = T['vo6'] - 0.35, T['vo6'] + 0.35; T['cla'], T['clb'] = T['vo6'] + 0.45, T['vo6'] + dur[6] + 0.3
OPEN_TURNS = 1.25; EX = 30.0; OFF = 16.0
def state(t):
    """inner angle A_i, phi, axial lift of the outer cap over the pushed position, rise of both caps (thread / lift-off), push 0..1, explode height"""
    k = K1 * lin(t, T['s1a'], T['s1b']) + K2 * lin(t, T['s2a'], T['s2b'])          # constant turning speed while slipping
    phi = k * TP
    A_i = 2 * math.pi * OPEN_TURNS * (ease(lin(t, T['opa'], T['opb'])) - ease(lin(t, T['cla'], T['clb'])))
    rise = PITCH * A_i / (2 * math.pi) + OFF * (ease(lin(t, T['offa'], T['offb'])) - ease(lin(t, T['dna'], T['dnb'])))
    ex = EX * (ease(lin(t, T['exa'], T['exb'])) - ease(lin(t, T['exc'], T['exd'])))
    push = ease(lin(t, T['pda'], T['pdb'])) - ease(lin(t, T['pua'], T['pub']))
    rest = G0 * (1 - push)
    ride = H * (k - math.floor(k + 1e-9))
    return A_i, phi, max(ride, rest, ex), rise, push, ex
rows = []
for i in range(int(LOOP * FPS_K) + 2):
    t = min(i / FPS_K, LOOP); A_i, phi, lift, rise, push, ex = state(t); rows.append([round(t, 4), round(A_i, 5), round(phi, 5), round(lift, 4), round(rise, 4), round(push, 4), round(ex, 3)])
json.dump(rows, open('kin.json', 'w'))
# ---------------- checks (HARD GATE 5.2) over the whole loop ----------------
h = lambda th: H * np.mod(N * th / (2 * math.pi), 1.0)
th = np.linspace(0, 2 * math.pi, 7201)[:-1]
lugI = lambda a: np.mod(a, TP) < WL - 1e-4                          # inner lug occupancy (interior)
lugO = lambda a: np.mod(a, TP) > TP - WL + 1e-4                     # outer lug occupancy (interior)
worst = 1e9; worst_lug = 1e9; worst_lip = 1e9; prev = None; slipped_while_pushed = 0
for t in np.arange(0, LOOP, 1 / 120):
    A_i, phi, lift, rise, push, ex = state(t)
    worst = min(worst, (lift + h(th - A_i - phi) - h(th - A_i)).min())
    both = lugI(th - A_i) & lugO(th - A_i - phi)
    if both.any(): worst_lug = min(worst_lug, (lift + UND - LO) - LH)          # where lugs share an angle, the outer lug must be above the inner lug
    if ex == 0: worst_lip = min(worst_lip, INNER['y_bot'] - (OUTER['lip_top'] + lift))
    if prev is not None:
        dA = A_i - prev[0]; dphi = phi - prev[1]
        if dA > 1e-9: assert push > 0.999, ('inner cap turned open without a push', t)
        if dA < -1e-9: assert lift + 1e-9 < H and abs(math.remainder(phi, TP)) < 1e-6 and push == 0, ('closing must be driven by the steep faces at rest', t)
        if push > 0.001: assert abs(dphi) < 1e-9, ('outer slipped while pushed', t)
    prev = (A_i, phi)
print('teeth min clearance %.4f mm (0 = touching)' % worst); assert worst > -1e-6
print('lug clearance where lugs share an angle: %.3f mm' % worst_lug); assert worst_lug > -1e-6
print('retaining lip below the inner skirt by >= %.3f mm' % worst_lip); assert worst_lip > 0
# engagement facts at the key states
print('rest: steep faces overlap %.2f mm (closing catches); lugs clear by %.2f mm' % (H - G0, G0 + UND - LO - LH))
print('pushed: lugs overlap %.2f mm (lock), outer lug length %.2f' % (LH - (UND - LO), LO))
A0 = state(0); A1 = state(LOOP - 1e-6)
print('loop: start', [round(v, 4) for v in A0], 'end', [round(v, 4) for v in A1])
assert abs(math.remainder(A1[1] - A0[1], 2 * math.pi)) < 1e-6 and abs(A1[0]) < 1e-6 and abs(A1[3]) < 1e-6 and abs(A1[2] - A0[2]) < 1e-6
assert OUTER['r_in'] > INNER['r_out'] and INNER['r_in'] > NECK_R and OUTER['lip_r'] > NECK_R and OUTER['lip_r'] < INNER['r_out'] and R_L1 < INNER['r_out'] - 0.6
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, N=N, H=H, G0=G0, LH=LH, LO=LO, WL=WL, UND=UND, PITCH=PITCH, R_T0=R_T0, R_T1=R_T1, R_L0=R_L0, R_L1=R_L1, GAP=GAP, INNER=INNER, OUTER=OUTER, NECK_R=NECK_R, K1=K1, K2=K2, EX=EX, OFF=OFF, OPEN_TURNS=OPEN_TURNS)
json.dump(G, open('geom.json', 'w'), indent=1)
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
