# p073 bike V-brake (linear pull) - kinematics. Front view: x across the bike, y up; wheel plane = y-z (axis x).
# Arms pivot on bosses at (+-PX, PY); arm angle phi (rad, + = tilted outward). Point at distance s along the right arm: (PX + s sin phi, PY + s cos phi) (left = mirror).
# Pad face (toward the rim) x = PX + S_PAD sin phi - OFF; contact when it reaches the rim side x = RIM_X. Cable top at S_TOP.
# Linear pull: the cable moves (relative to its housing) by the change of the distance between the two arm tops.
import json, math
PX, PY, S_PAD, S_TOP, OFF, RIM_X, GAP = 40.0, -70.0, 60.0, 115.0, 22.0, 10.0, 10.0
PAD_H = 10.0
def face(phi):      # innermost x of the pad face (both corners, local (-OFF, S_PAD +- PAD_H/2) rotated by -phi)
    return min(PX - OFF * math.cos(phi) + (S_PAD + d) * math.sin(phi) for d in (-PAD_H / 2, PAD_H / 2))
def solve(xt):
    lo, hi = math.radians(-20), math.radians(10)
    for _ in range(80):
        m = (lo + hi) / 2
        if face(m) < xt: lo = m
        else: hi = m
    return (lo + hi) / 2
PHI_C = solve(RIM_X); PHI_O = solve(RIM_X + GAP)
FPS = 60
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
T = {'vo0': 0.15}
T['hookEnd'] = T['vo0'] + D[0] + 0.15
for i in range(1, 7): T[f'vo{i}'] = T[f'vo{i-1}'] + (D[i - 1] if i > 1 else 0) + (0.1 if i == 1 else 0.2)
T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = T[f'vo{i-1}'] + D[i - 1] + (0.9 if i == 6 else 0.3 if i in (3, 4) else 0.2)
LOOP = round(T['vo6'] + D[6] + 1.1, 1); T['LOOP'] = LOOP
def ramp(t, a, b): return smooth((t - a) / (b - a))
def u_at(t):         # engagement 0 (open) .. 1 (pads on the rim)
    if t < T['hookEnd']: return ramp(t, 0.3, 0.75)
    if t < T['vo2'] - 0.45: return ramp(t, T['vo1'] + 0.8, T['vo1'] + 1.25)
    if t < T['vo3']: return 1 - ramp(t, T['vo2'] - 0.45, T['vo2'] + 0.1)
    if t < T['vo5']: return 0.97 * ramp(t, T['vo3'] + 0.9, T['vo5'] - 0.1)
    if t < LOOP - 1.4: return 0.97 + 0.03 * ramp(t, T['vo5'] + 0.1, T['vo5'] + 0.45)
    return 1 - ramp(t, LOOP - 1.4, LOOP - 0.7)
def phi_of(u): return PHI_O + (PHI_C - PHI_O) * u
def top_x(phi): return PX + S_TOP * math.sin(phi)
CABLE_OPEN = 2 * top_x(PHI_O)
rows = []; ang = 0.0; om = 0.0; W0 = 2 * math.pi * 0.4
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; u = u_at(t); phi = phi_of(u)
    fx = face(phi)
    assert fx >= RIM_X - 1e-6, (t, fx)            # HARD GATE 5.2: the pad never enters the rim
    assert top_x(phi) > 16 + 3                        # arm tops stay clear of the tyre (half width 16)
    pull = CABLE_OPEN - 2 * top_x(phi)                # cable travel vs its housing (mm)
    target = 0.0 if u > 0.999 else W0
    om += (target - om) * min(1, (3.2 if target == 0 else 1.5) / FPS)
    if u > 0.999: om = max(0.0, om - W0 / 0.9 / FPS)
    ang += om / FPS
    rows.append([round(t, 4), round(u, 4), round(math.degrees(phi), 4), round(pull, 3), round(ang, 4), round(om / W0, 3)])
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, PX=PX, PY=PY, S_PAD=S_PAD, S_TOP=S_TOP, OFF=OFF, RIM_X=RIM_X, GAP=GAP, PHI_C=math.degrees(PHI_C), PHI_O=math.degrees(PHI_O),
         PAD_H=PAD_H, PULL_MAX=round(CABLE_OPEN - 2 * top_x(PHI_C), 2), RATIO=round(S_TOP / S_PAD, 2))
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print(json.dumps(G))
