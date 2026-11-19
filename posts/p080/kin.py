# p080 can opener "HOW DOES IT / CUT THE LID?" - kinematics + HARD GATE 5.2 checks (venv python)
# mm, y up, can axis = y, seam top y = SEAM_TOP. Opener on the +x side of the can.
# Fixed body (upper handle, key, axle, toothed traction wheel under the rim). Moving jaw (cutting wheel + lower handle) turns about the pivot (axis z).
# Squeeze: jaw angle ALPHA_OPEN -> 0, the cutting wheel punches through the lid just inside the rim.
# Turn the key: traction wheel angle beta, can angle phi = -beta * RT / R_CONTACT (rolling without slip on the underside of the seam).
import json, math
import numpy as np

FPS_K = 120
CAN_R, NECK_R = 37.5, 36.2
SEAM_RI, SEAM_RO, SEAM_Y0, SEAM_TOP = 35.6, 38.6, -3.4, 0.4
LID_Y = -3.0
# traction wheel (toothed): plane x = XT (normal along x), teeth z=18, module 0.62 -> tip radius 6.2
TW_Z, TW_M = 18, 0.62; RT_TIP = TW_Z * TW_M / 2 + TW_M; RT = TW_Z * TW_M / 2   # rp 5.58, tip 6.2
XT, TW_W = 38.0, 2.4
YT = SEAM_Y0 - RT_TIP + 0.2                       # teeth bite 0.2 mm into the underside of the seam
R_CONTACT = XT                                    # contact radius on the seam (wheel plane x = XT at z = 0)
# cutting wheel: plane x = XC, radius RC, V edge; engaged edge 0.9 mm below the lid
XC, RC, CW_W = 33.8, 6.5, 1.0
YC = LID_Y - 0.9 + RC
PIV = (45.0, -2.0)                                # jaw pivot (axis z)
ALPHA_OPEN = -0.26                                # jaw angle with the handles open (cutter lifted)

def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {}
T['vo0'] = 0.3; T['hookEnd'] = 1.0
T['vo1'] = 2.5; T['sqa'] = 4.3; T['sqb'] = 5.5
T['vo2'] = T['vo1'] + dur[1] + 0.35
T['vo3'] = T['vo2'] + dur[2] + 0.35; T['ta'] = T['vo3'] + 0.9
T['vo4'] = T['vo3'] + dur[3] + 0.35; T['tm'] = T['vo4'] + 0.6
T['tb'] = T['vo4'] + dur[4] + 0.5; T['drop'] = T['tb'] + 0.15
T['vo5'] = T['tb'] + 0.75
LOOP = round(T['vo5'] + dur[5] + 2.2, 2); T['LOOP'] = LOOP
PHI_END = 2 * math.pi + 0.12                      # a little past one full turn: the cut closes
PHI_MID = 2.3

def state(t):
    """jaw angle, can angle phi, key/wheel angle beta, slit angle (0..PHI_END), lid drop 0..1"""
    if t < T['hookEnd']:                           # hook: the end of the cut, the lid drops free
        u = t / T['hookEnd']; phi = PHI_END - 1.2 + 1.2 * min(1, u / 0.7); drop = ease((u - 0.72) / 0.25)
        return 0.0, phi, -phi * R_CONTACT / RT, min(phi, PHI_END), drop
    jaw = ALPHA_OPEN * (1 - ease((t - T['sqa']) / (T['sqb'] - T['sqa'])))
    u = min(1, max(0, (t - T['ta']) / (T['tb'] - T['ta']))); phi = PHI_END * (u * u * (3 - 2 * u) * 0.5 + u * 0.5) if u < 1 else PHI_END   # soft start, steady middle
    drop = ease((t - T['drop']) / 0.35)
    return jaw, phi, -phi * R_CONTACT / RT, phi, drop

rows = []
for i in range(int(LOOP * FPS_K) + 2):
    t = i / FPS_K; a, phi, beta, slit, drop = state(min(t, LOOP)); rows.append([round(t, 4), round(a, 5), round(phi, 5), round(beta, 5), round(slit, 5), round(drop, 4)])
json.dump(rows, open('kin.json', 'w'))

# ---------------- checks ----------------
def jaw_xf(p, a):  # rotate a point (x, y) of the jaw about the pivot by angle a
    dx, dy = p[0] - PIV[0], p[1] - PIV[1]; return (PIV[0] + dx * math.cos(a) - dy * math.sin(a), PIV[1] + dx * math.sin(a) + dy * math.cos(a))
def in_can(x, y, z):  # solid can material near the top: seam ring + neck wall (2D section at radius r)
    r = math.hypot(x, z)
    if SEAM_RI <= r <= SEAM_RO and SEAM_Y0 <= y <= SEAM_TOP: return 'seam'
    if NECK_R - 0.3 <= r <= NECK_R and -17 <= y <= SEAM_Y0: return 'wall'
    if r < SEAM_RI and LID_Y - 0.25 <= y <= LID_Y: return 'lid'
    return None
# 1. traction wheel (tip radius, plane x = XT +- TW_W/2) never enters the neck wall; bites the seam only by the planned 0.2 mm
worst_wall = 1e9
for th in np.linspace(0, 2 * math.pi, 720):
    for xx in (XT - TW_W / 2, XT + TW_W / 2):
        y = YT + RT_TIP * math.sin(th); z = RT_TIP * math.cos(th); r = math.hypot(xx, z)
        if -17 <= y <= SEAM_Y0: worst_wall = min(worst_wall, r - NECK_R)
assert worst_wall > 0.3, ('traction wheel hits the can wall', worst_wall)
bite = (YT + RT_TIP) - SEAM_Y0; assert 0 < bite <= 0.25, bite
# 2. cutting wheel over the whole loop: below the lid top only when the jaw is closed (punch + cut); never in the seam
worst_seam = 1e9; pierced_open = 0
for t in np.arange(0, LOOP, 1 / 60):
    a = state(t)[0]
    for th in np.linspace(0, 2 * math.pi, 180):
        for xo in (-CW_W / 2, CW_W / 2):
            for rr in (RC, RC * 0.6):
                # wheel point in the jaw frame (x = XC + xo, y = YC + rr sin, z = rr cos), then jaw rotation about z through the pivot
                px, py = jaw_xf((XC + xo, YC + rr * math.sin(th)), a); pz = rr * math.cos(th)
                hit = in_can(px, py, pz)
                if hit == 'seam': raise AssertionError(('cutter in the seam', t, px, py, pz))
                if hit == 'lid' and T['hookEnd'] <= t < T['sqa']: pierced_open += 1
                r = math.hypot(px, pz)
                if SEAM_Y0 <= py <= SEAM_TOP: worst_seam = min(worst_seam, SEAM_RI - r)
assert pierced_open == 0, 'cutter goes into the lid before the squeeze'
print('cutter-seam min clearance %.2f mm, wall clearance %.2f mm, tooth bite %.2f mm' % (worst_seam, worst_wall, bite))
# 3. jaw plate (front, z 3..6) and its cutter boss stay above the seam over the whole squeeze
JAW = [(27.5, -0.6), (31.8, -0.6), (31.8, 5.0), (31.8, 9.0), (44.0, 9.0), (49.5, 3.0), (50.0, -2.0), (49.0, -6.5), (41.0, -6.5), (40.2, -2.0), (40.5, 2.5), (38.0, 4.6), (27.5, 4.6)]
for a in np.linspace(ALPHA_OPEN, 0, 40):
    for i in range(len(JAW)):
        p, q = JAW[i], JAW[(i + 1) % len(JAW)]
        for u in np.linspace(0, 1, 30):
            x, y = jaw_xf((p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u), a)
            for z in (3.0, 6.0):
                assert in_can(x, y, z) is None, ('jaw plate hits the can', a, x, y, z)
# 4. rolling: the wheel surface speed equals the seam speed (by construction) -> report turns of the key per can turn
print('key turns per can turn: %.2f' % (R_CONTACT / RT))
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, CAN_R=CAN_R, NECK_R=NECK_R, SEAM_RI=SEAM_RI, SEAM_RO=SEAM_RO, SEAM_Y0=SEAM_Y0, SEAM_TOP=SEAM_TOP, LID_Y=LID_Y,
         TW_Z=TW_Z, TW_M=TW_M, RT=RT, XT=XT, TW_W=TW_W, YT=YT, XC=XC, RC=RC, CW_W=CW_W, YC=YC, PIV=PIV, ALPHA_OPEN=ALPHA_OPEN, PHI_END=PHI_END, JAW=JAW, R_CONTACT=R_CONTACT)
json.dump(G, open('geom.json', 'w'), indent=1)
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
