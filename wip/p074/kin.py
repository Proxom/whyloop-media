# p074 nail clipper (compound lever) - kinematics. Side view: x along the clipper (jaws at +x), y up, z across.
# Lever 2 = upper leaf: pivots at the rear joint P2, its blade edge at x = XJ. Lever 1 = top lever: pivots on the pin top F, its heel presses the upper leaf.
# Numbers follow Wikipedia "Compound lever" (nail clipper example): lever 1 effort 8 units / load 1 unit (x8), lever 2 effort 6 / load 8 (x0.75) -> W/F = 6. 1 unit = 7 mm.
import json, math
U = 7.0
P2 = (0.0, 1.4)                      # upper leaf pivot (rear joint)
XH, XF, XJ = 6 * U, 7 * U, 8 * U     # heel 42, pin/fulcrum 49, blades 56 (horizontal distances, as in the Wikipedia figure)
XT = XF - 8 * U                      # thumb at -7
F = (XF, 10.8)                       # pin top = lever 1 fulcrum
NUB_R = 1.2
NUB_C = (XH - XF, -3.4 + NUB_R)      # heel nub centre relative to F (rest)
UP_TOP = [(-2, 2.8), (10, 5.0), (30, 7.0), (42, 7.4), (48, 7.2), (53, 6.4), (57.4, 5.1)]
UP_BOT = [(-2, 1.4), (10, 3.6), (30, 5.6), (42, 6.0), (48, 5.6), (53, 5.2), (56.6, 4.8)]
LO_TOP = [(-2, 1.4), (10, -0.5), (30, -1.7), (46, -1.5), (53, 0.6), (56.6, 2.0)]
JAW_UP0 = 4.8; JAW_LO = 2.0
NAIL_B, NAIL_T = 2.05, 2.55
TH_MAX = math.asin((JAW_UP0 - JAW_LO) / (XJ - P2[0]))
LEV_C = [(1.5, 0.2), (-3, -1.6), (-7, -2.6), (-11, -0.6), (-20, 3.5), (-40, 9.5), (-56, 13.0)]   # lever centreline rel. F (rest), half thickness 0.8
LEV_HT = 0.8
def rot(p, c, a): x, y = p[0] - c[0], p[1] - c[1]; return (c[0] + x * math.cos(a) - y * math.sin(a), c[1] + x * math.sin(a) + y * math.cos(a))
def interp(poly, x):
    for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
        if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return None
def leaf_top(x, th):                # upper leaf rotated by -th about P2 (jaw goes down)
    P = [rot(p, P2, -th) for p in UP_TOP]; return interp(P, x)
def nub(phi):                       # nub centre (abs) for lever rotation phi (+ = thumb end down = CCW)
    return rot((F[0] + NUB_C[0], F[1] + NUB_C[1]), F, phi)
def solve_phi(th):
    lo, hi = -0.2, 0.6
    for _ in range(80):
        m = (lo + hi) / 2; c = nub(m)
        if c[1] - NUB_R > leaf_top(c[0], th): lo = m
        else: hi = m
    return (lo + hi) / 2
PHI0 = solve_phi(0.0)
def jaw_edge(th): return rot((56.6, JAW_UP0), P2, -th)
FPS = 60
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
def ramp(t, a, b): return smooth((t - a) / (b - a))
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
GAP = [0, 0.1, 0.25, 0.3, 0.35, 0.35, 0.6]
T = {'vo0': 0.15}; T['hookEnd'] = T['vo0'] + D[0] + 0.15; T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = T[f'vo{i-1}'] + D[i - 1] + GAP[i]
LOOP = round(T['vo6'] + D[6] + 1.3, 1); T['LOOP'] = LOOP
def _th_for(y):
    lo, hi = 0.0, 0.2
    for _ in range(80):
        m = (lo + hi) / 2
        if rot((56.6, JAW_UP0), P2, -m)[1] > y: lo = m
        else: hi = m
    return (lo + hi) / 2
TH_MAX = _th_for(JAW_LO); E_NAIL = _th_for(NAIL_T) / TH_MAX          # engagement where the blade touches the nail
T['cutH'] = 0.8; T['cut'] = T['vo5'] + 0.6
def e_at(t):         # engagement 0 (open) .. 1 (blades meet)
    if t < T['hookEnd']: return E_NAIL * ramp(t, 0.3, 0.75) + (1 - E_NAIL) * ramp(t, T['cutH'], T['cutH'] + 0.15)
    if t < T['vo2']: return ramp(t, T['vo1'] + 0.5, T['vo1'] + 0.9) - ramp(t, T['vo1'] + 1.6, T['vo1'] + 2.1)
    if t < T['vo4']: return 0.5 * ramp(t, T['vo3'] + 1.2, T['vo3'] + 5.8)
    if t < T['vo5']: return 0.5 + (E_NAIL - 0.5) * ramp(t, T['vo4'] + 0.6, T['vo4'] + 4.6)
    if t < LOOP - 1.1: return E_NAIL + (1 - E_NAIL) * ramp(t, T['cut'], T['cut'] + 0.15)
    return 1 - ramp(t, LOOP - 1.1, LOOP - 0.5)
def finger_at(t):    # finger + nail slide-in offset along +x (mm), 0 = in place
    if t < T['hookEnd']: return 0.0
    if t < T['vo4'] - 0.4: return 60.0
    if t < LOOP - 0.4: return 60.0 * (1 - ramp(t, T['vo4'] - 0.4, T['vo4'] + 0.5))
    return 0.0
def cut_state(t):    # -1 whole nail, else seconds since the cut
    if t < T['hookEnd']: return t - T['cutH'] if t >= T['cutH'] else -1
    if t < T['vo4'] - 0.4 or t >= LOOP - 0.4: return -1
    return t - T['cut'] if t >= T['cut'] else -1
rows = []; checks = 0
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; e = e_at(t); th = TH_MAX * e; phi = solve_phi(th); fx = finger_at(t); cs = cut_state(t)
    je = jaw_edge(th)
    assert je[1] >= JAW_LO - 1e-6, (t, je)                          # blades never pass each other
    if cs < 0 and fx < 1.0: assert je[1] >= NAIL_T - 1e-6, (t, je)  # the blade only goes through the nail after the cut
    c = nub(phi); assert abs(c[1] - NUB_R - leaf_top(c[0], th)) < 1e-4  # heel touches the leaf (no gap, no overlap)
    for k in range(3, 60):                                         # lever underside stays above the upper leaf
        s = -k; cy = interp(LEV_C[::-1], s)
        if cy is None: continue
        q = rot((F[0] + s, F[1] + cy - LEV_HT), F, phi - PHI0)
        lt = leaf_top(q[0], th)
        if lt is not None and q[0] < c[0] - 2.5: assert q[1] > lt + 0.3, (t, s, q, lt); checks += 1
    lb = rot((56.6, JAW_UP0 - 1.4), P2, -th)
    rows.append([round(t, 4), round(e, 4), round(math.degrees(th), 4), round(math.degrees(phi - PHI0), 4), round(fx, 3), round(cs, 4)])
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, U=U, P2=P2, F=F, XH=XH, XF=XF, XJ=XJ, XT=XT, NUB_C=NUB_C, NUB_R=NUB_R, UP_TOP=UP_TOP, UP_BOT=UP_BOT, LO_TOP=LO_TOP,
         LEV_C=LEV_C, LEV_HT=LEV_HT, NAIL_B=NAIL_B, NAIL_T=NAIL_T, E_NAIL=E_NAIL, TH_MAX=math.degrees(TH_MAX), PHI0=math.degrees(PHI0),
         PHI_MAX=round(max(r[3] for r in rows), 3), MA1=(XF - XT) / (XF - XH), MA2=(XH - P2[0]) / (XJ - P2[0]))
G['MA'] = G['MA1'] * G['MA2']
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('checks', checks, 'PASS'); print({k: G[k] for k in ('LOOP', 'TH_MAX', 'PHI0', 'PHI_MAX', 'MA1', 'MA2', 'MA', 'E_NAIL')}); print(T)
