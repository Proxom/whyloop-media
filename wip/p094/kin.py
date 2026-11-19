# p094 prismatic day/night rear-view mirror "ONE FLICK, / NO GLARE?" - timing, kinematics, 2D ray optics + HARD GATE 5.2 checks.
# Side plane (mm): s = world z (toward the driver / rear of the car), y = up. Mirror body local coords at tilt 0:
#   back face (silvered) s = 0, y -32..32; front face s = 3 + (y + 32) tan(ALPHA)  -> wedge, thicker at the top.
# The whole body (housing + glass + tab pivot) tilts about the ball centre PV; the tab drives the tilt (tilt = linear in tab angle).
# Diagram is EXAGGERATED (wedge 14 deg, cabin compressed) so the rays can be seen; real wedges are a few degrees (said in the first comment).
import json, math
ALPHA = math.radians(14.0); NG = 1.52; H = 32.0; T0 = 3.0
PV = (-14.0, 47.0); EYE = (210.0, -45.0); ROOF_Y = 108.0; Y0 = 0.0; S_IN = 330.0
R_FRONT, R_BACK = 0.04, 0.90          # patent US4679906: front ~4 %, rear (silvered) ~90 %
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
GAP = {1: 0.28, 2: 0.32, 3: 0.29, 4: 0.34, 5: 0.35, 6: 0.33}
T = {'vo0': 0.3}
for i in range(1, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.3, 2); T['LOOP'] = LOOP
T['hookEnd'] = 1.0; T['hf_a'] = 0.35; T['hf_b'] = 0.75                          # hook: payoff flash (day -> night, glare dims)
T['orb_a'] = T['vo1'] + 0.1; T['orb_b'] = T['vo1'] + 1.9                         # orbit front -> side
T['cut_a'] = T['vo1'] + 0.45; T['cut_b'] = T['vo1'] + 1.65                       # near half fades away (section)
T['ray_a'] = T['vo2'] + 0.05; T['ray_b'] = T['vo2'] + 0.75; T['ray_c'] = T['vo2'] + 1.5   # incoming ray grows, then the bright ray to the eye
T['flip_a'] = T['vo4'] + 0.55; T['flip_b'] = T['vo4'] + 2.35                     # slow-mo tilt (1.8 s)
T['back_a'] = T['vo6'] + 0.05; T['back_b'] = T['vo6'] + 1.35                     # orbit back to the front view
T['end_a'] = LOOP - 0.62; T['end_b'] = LOOP - 0.18                              # tab back to DAY so the last frame = first frame
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def rot(p, th):
    c, s = math.cos(th), math.sin(th); x, y = p[0] - PV[0], p[1] - PV[1]; return (PV[0] + c * x - s * y, PV[1] + s * x + c * y)
def body_faces(th):
    b0, b1 = rot((0.0, -H), th), rot((0.0, H), th)
    f0, f1 = rot((T0, -H), th), rot((T0 + 2 * H * math.tan(ALPHA), H), th)
    return (b0, b1), (f0, f1)
def outward(seg, inside_pt):                     # unit normal of the segment pointing away from inside_pt
    (x0, y0), (x1, y1) = seg; dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); n = (dy / L, -dx / L)
    if (inside_pt[0] - x0) * n[0] + (inside_pt[1] - y0) * n[1] > 0: n = (-n[0], -n[1])
    return n
def hit(o, d, seg):                              # ray o + t d vs segment; returns (t, point, u) or None
    (x0, y0), (x1, y1) = seg; ex, ey = x1 - x0, y1 - y0; den = d[0] * (-ey) - d[1] * (-ex)
    if abs(den) < 1e-12: return None
    rx, ry = x0 - o[0], y0 - o[1]; t = (rx * (-ey) - ry * (-ex)) / den; u = (d[0] * ry - d[1] * rx) / den
    if t <= 1e-6 or u < 0 or u > 1: return None
    return t, (o[0] + t * d[0], o[1] + t * d[1]), u
def refl(d, n): k = d[0] * n[0] + d[1] * n[1]; return (d[0] - 2 * k * n[0], d[1] - 2 * k * n[1])
def refr(d, n, n1, n2):                          # n points against d (toward the incoming side)
    c1 = -(d[0] * n[0] + d[1] * n[1]); r = n1 / n2; k = 1 - r * r * (1 - c1 * c1); assert k > 0, 'TIR'
    c2 = math.sqrt(k); return (r * d[0] + (r * c1 - c2) * n[0], r * d[1] + (r * c1 - c2) * n[1])
def extend(p, d):                                # end point: the roof if going up, else 360 mm
    if d[1] > 1e-6:
        t = (ROOF_Y - p[1]) / d[1]; return (p[0] + t * d[0], p[1] + t * d[1]), True
    return (p[0] + 360 * d[0], p[1] + 360 * d[1]), False
def trace(th):
    back, front = body_faces(th); ctr = rot((T0 / 2 + H * math.tan(ALPHA) / 2, 0.0), th)
    o = (S_IN, Y0); d = (-1.0, 0.0)
    h = hit(o, d, front); assert h, 'incoming ray misses the glass'; P = h[1]; nf = outward(front, ctr)
    rf = refl(d, nf); Ef, roofF = extend(P, rf)                                   # FRONT surface reflection (~4 %)
    di = refr(d, nf, 1.0, NG); hb = hit(P, di, back); assert hb, 'misses the back face'; Q = hb[1]
    nb = outward(back, ctr); db = refl(di, (-nb[0], -nb[1]) if False else nb)
    nfi = (-nf[0], -nf[1]); hx = hit(Q, db, front); assert hx, 'no exit'; X = hx[1]
    do = refr(db, nfi, NG, 1.0); Eb, roofB = extend(X, do)                        # BACK (silver) reflection (~90 %)
    return dict(P=P, Q=Q, X=X, rf=rf, do=do, Ef=Ef, Eb=Eb, roofF=roofF, roofB=roofB)
def miss_eye(p, d):                              # signed angle (deg) between the ray and the direction to the eye
    a = math.atan2(d[1], d[0]); b = math.atan2(EYE[1] - p[1], EYE[0] - p[0]); return math.degrees(a - b)
def solve(f):
    lo, hi = math.radians(-40), math.radians(40)
    flo = f(lo)
    for _ in range(80):
        mid = (lo + hi) / 2; fm = f(mid)
        if (fm > 0) == (flo > 0): lo, flo = mid, fm
        else: hi = mid
    return (lo + hi) / 2
TH_DAY = solve(lambda th: miss_eye(trace(th)['X'], trace(th)['do']))
TH_NIGHT = solve(lambda th: miss_eye(trace(th)['P'], trace(th)['rf']))
PHI_DAY, PHI_NIGHT = math.radians(-58), math.radians(-128)                      # tab angle (about the x axis, in body coords)
def mode(t):   # 0 = day, 1 = night (u drives tab + tilt together)
    if t < T['hookEnd']: return ease((t - T['hf_a']) / (T['hf_b'] - T['hf_a']))
    if t < T['flip_a']: return 0.0
    if t < T['end_a']: return ease((t - T['flip_a']) / (T['flip_b'] - T['flip_a']))
    return 1 - ease((t - T['end_a']) / (T['end_b'] - T['end_a']))
FPS_K = 30; rows = []
for i in range(int(round(LOOP * FPS_K)) + 1):
    t = min(LOOP, i / FPS_K); u = mode(t); th = TH_DAY + (TH_NIGHT - TH_DAY) * u; phi = PHI_DAY + (PHI_NIGHT - PHI_DAY) * u
    r = trace(th)
    eb = abs(miss_eye(r['X'], r['do'])); ef = abs(miss_eye(r['P'], r['rf']))
    seen = R_BACK * math.exp(-(eb / 4.0) ** 2) + R_FRONT * math.exp(-(ef / 4.0) ** 2)   # light reaching the eye (for the inset)
    rows.append([round(t, 4), round(th, 6), round(phi, 6), round(u, 4), [round(v, 2) for v in (*r['P'], *r['Q'], *r['X'], *r['Ef'], *r['Eb'])], int(r['roofB']), round(seen, 4)])
# ---- HARD GATE 5.2 checks ----
d0, n0 = trace(TH_DAY), trace(TH_NIGHT)
assert abs(miss_eye(d0['X'], d0['do'])) < 0.05 and abs(miss_eye(n0['P'], n0['rf'])) < 0.05
assert abs(miss_eye(d0['P'], d0['rf'])) > 15, 'day: the faint front reflection must miss the eye'
assert n0['roofB'] and abs(miss_eye(n0['X'], n0['do'])) > 15, 'night: the bright reflection must go up to the roof'
assert TH_NIGHT > TH_DAY, 'night = tilted up'
for th in (TH_DAY, TH_NIGHT):          # hit points stay on the glass, well inside the edges
    r = trace(th); b, f = body_faces(th)
    for p, seg in ((r['P'], f), (r['Q'], b), (r['X'], f)):
        (x0, y0), (x1, y1) = seg; u = ((p[0] - x0) * (x1 - x0) + (p[1] - y0) * (y1 - y0)) / ((x1 - x0) ** 2 + (y1 - y0) ** 2); assert 0.15 < u < 0.85, ('edge', u)
# tab (rod r 3, length 18 from pivot (-8,-41)) never enters the housing (bottom outer y = -37) in body coords
for k in range(101):
    ph = PHI_DAY + (PHI_NIGHT - PHI_DAY) * k / 100
    for L in (0, 6, 12, 18): y = -41 + L * math.sin(ph); assert y + 3 < -37 + 1e-9, 'tab hits housing'
# nothing moves without a cause: tilt changes only while the tab moves (both from u)
for a, b in zip(rows, rows[1:]):
    if abs(b[1] - a[1]) > 1e-9: assert abs(b[2] - a[2]) > 1e-9
G = dict(T=T, LOOP=LOOP, FPS_K=FPS_K, ALPHA=ALPHA, NG=NG, H=H, T0=T0, PV=PV, EYE=EYE, ROOF_Y=ROOF_Y, Y0=Y0, S_IN=S_IN, TH_DAY=TH_DAY, TH_NIGHT=TH_NIGHT, PHI_DAY=PHI_DAY, PHI_NIGHT=PHI_NIGHT)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('PASS', 'LOOP', LOOP, 'tilt day %.2f night %.2f deg' % (math.degrees(TH_DAY), math.degrees(TH_NIGHT)),
      'day front miss %.1f' % miss_eye(d0['P'], d0['rf']), 'night back miss %.1f roof %s at %s' % (miss_eye(n0['X'], n0['do']), n0['roofB'], [round(v) for v in n0['Eb']]),
      'seen day %.3f night %.3f' % (rows[int(T['vo3'] * 30)][6], rows[int(T['vo6'] * 30)][6]))
