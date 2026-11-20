# p104 vacuum flask: timeline, geometry and HARD GATE 5.2 checks. Units mm, flask local axis +y, base centre at y 0.
# kin rows: [t, px, py, theta (flask tilt, rad), sy (stopper drop above seated), srot (stopper turn, rad)]
import json, math
FPS_K = 120
VO = [d['dur'] for d in json.load(open('vo/vo.json'))]
T = dict(vo0=0.15, cutIn=2.4, vo1=2.5, s2=8.0, vo2=8.1, s3=13.0, vo3=13.1, airOutB=13.9, s4=18.2, vo4=18.4, neck=20.0, stA=20.3, stB=21.7, outA=22.4, vo5=22.6, ans=22.4)
LOOP = 26.5
H = dict(pourEnd=1.4, setDown=2.25)
starts = [T['vo0'], T['vo1'], T['vo2'], T['vo3'], T['vo4'], T['vo5'], LOOP - 0.8]
for i in range(6): assert starts[i] + VO[i] < starts[i + 1], ('VO overlap', i, starts[i] + VO[i], starts[i + 1])
# ---- geometry (r, y) profiles, closed polygons ----
OUTER = [[0.01, 0], [35, 0], [38, 3], [38, 212], [25.5, 229], [25.5, 243], [24, 243], [24, 229.6], [36.5, 212.6], [36.5, 3.6], [34.5, 1.5], [0.01, 1.5]]
INNER = [[0.01, 7], [29, 7], [31.5, 9.5], [31.5, 208], [21.5, 224], [21.5, 243], [20, 243], [20, 224.6], [30, 208.6], [30, 10.5], [28.5, 8.5], [0.01, 8.5]]
LIP = [[20, 243], [25.5, 243], [25.5, 245.5], [20, 245.5]]
COFFEE_TOP = 190.0
COFFEE = [[0.01, 8.6], [28.4, 8.6], [29.9, 10.5], [29.9, COFFEE_TOP], [0.01, COFFEE_TOP]]
STOPPER = [[0.01, 222], [19.6, 222], [19.6, 245.6], [23.5, 245.6], [24.5, 247], [24.5, 262], [23, 264], [0.01, 264]]   # plug + grip, seated
CUP = dict(x=150.0, R=30.0, H=62.0, t=2.0, level=50.0)
PIV = dict(pour_th=-110 * math.pi / 180, mouth=[CUP['x'] - 12, CUP['H'] + 62])
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def rot(th, x, y): return [x * math.cos(th) - y * math.sin(th), x * math.sin(th) + y * math.cos(th)]
mo = rot(PIV['pour_th'], 0, 245.5); P0 = [PIV['mouth'][0] - mo[0], PIV['mouth'][1] - mo[1]]
def state(t):
    if t < T['cutIn']:
        u = ease((t - H['pourEnd']) / (H['setDown'] - H['pourEnd']))
        return [P0[0] * (1 - u), P0[1] * (1 - u), PIV['pour_th'] * (1 - u), 999.0, 0.0]
    if t < T['outA']:
        u = ease((t - T['stA']) / (T['stB'] - T['stA'])); sy = 90 * (1 - u) if t >= T['neck'] else 999.0
        return [0.0, 0.0, 0.0, sy, -4 * math.pi * u]
    return [0.0, 0.0, 0.0, 0.0, 0.0]
rows = [[round(i / FPS_K, 4)] + [round(v, 5) for v in state(i / FPS_K)] for i in range(int(LOOP * FPS_K) + 1)]
# ---- heat dot model (shared with scene.html): phase 'air' crosses the gap, phase 'vac' bounces at the inner wall ----
X_COF, X_IW_IN, X_IW_OUT, X_OW_IN, X_OW_OUT = 29.9, 30.0, 31.5, 36.5, 38.0
def heat_x(phase, u):   # u in [0,1) along the dot's own cycle
    if phase == 'air': return 18 + u * 44              # 18 -> 62 mm: coffee -> wall -> gap (carried by air) -> outside
    return 18 + 11.3 * (1 - abs(1 - 2 * u))            # 18 -> 29.3 -> 18: stops just short of the inner wall and comes back
G = dict(LOOP=LOOP, FPS_K=FPS_K, T=T, H=H, OUTER=OUTER, INNER=INNER, LIP=LIP, COFFEE=COFFEE, COFFEE_TOP=COFFEE_TOP, STOPPER=STOPPER, CUP=CUP,
         X=dict(cof=X_COF, iwIn=X_IW_IN, iwOut=X_IW_OUT, owIn=X_OW_IN, owOut=X_OW_OUT))
# ---- checks ----
fail = []
def seg_d(p, a, b):
    ax, ay = a; bx, by = b; px, py = p; dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy; u = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L)) if L else 0
    return math.hypot(px - ax - u * dx, py - ay - u * dy)
def poly_min(A, B):
    m = 1e9
    for P in A:
        for a, b in zip(B, B[1:] + B[:1]): m = min(m, seg_d(P, a, b))
    return m
def inside(p, poly):
    x, y = p; c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
def densify(poly, step=0.5):
    out = []
    for a, b in zip(poly, poly[1:] + poly[:1]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        out += [[a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n] for k in range(n)]
    return out
# the two walls touch only at the lip (neck): vacuum gap everywhere below y 243
iw = [p for p in densify(INNER) if p[1] < 242.9]; ow = [p for p in densify(OUTER) if p[1] < 242.9]
gap = min(poly_min(iw, OUTER), poly_min(ow, INNER)); print('min wall gap below the lip (mm):', round(gap, 2))
if gap < 2.0: fail.append(('walls too close', gap))
if any(inside(p, OUTER) for p in densify(INNER)): fail.append('inner wall passes through outer wall')
if any(inside(p, INNER) for p in densify(COFFEE) if p[0] > 0.5): fail.append('coffee inside the inner wall')
if any(inside(p, INNER) or inside(p, LIP) for p in densify(STOPPER) if p[0] > 0.5 and not (abs(p[1] - 245.6) < 0.01)): fail.append('stopper through the neck')
# stopper descends straight down onto the lip: never overlaps the neck while dropping
for t, px, py, th, sy, sr in rows:
    if sy < 500 and sy > 0:
        if any(inside([p[0], p[1] + sy], INNER) or inside([p[0], p[1] + sy], LIP) for p in densify(STOPPER)[::4] if p[0] > 0.5): fail.append(('stopper overlap while dropping', t)); break
# hook: flask never hits the cup or the table (sample the outer profile, both sides)
pts = [[s * p[0], p[1]] for p in densify(OUTER, 2) for s in (1, -1)]
for t, px, py, th, sy, sr in rows:
    if t >= T['cutIn']: break
    for x, y in pts:
        X, Y = rot(th, x, y); X += px; Y += py
        if Y < -0.01: fail.append(('flask below table', t)); break
        if abs(X - CUP['x']) < CUP['R'] and Y < CUP['H']: fail.append(('flask hits cup', t)); break
# heat dots: 'vac' never reaches the inner wall (nothing crosses the vacuum), 'air' only moves while air is shown
for k in range(200):
    u = k / 200
    if heat_x('vac', u) >= X_IW_IN: fail.append(('vac dot crosses', u))
print('checks:', 'PASS' if not fail else fail[:6], '| rows', len(rows), '| pour pose base', [round(v, 1) for v in P0])
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
