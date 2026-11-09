# p055 door latch: why does a door click shut by itself? 2D kinematics (mm) in the horizontal section at latch height.
# x = from the door edge toward the frame (+x = into the jamb), y = through the door thickness, z = up.
# Door closed: slab x<=0, y in [0, T]; it closes moving -y onto the stop and opens toward +y; hinge pin at (-HW, T).
# Latch bolt slides along x in the door; slanted side faces -y (the closing direction), flat side faces +y (opening direction).
# Single source for scene.html (kin_240.json), audio (events.json) and the HARD GATE check (check.py).
import json, math, numpy as np
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
from shapely import affinity

T = 40.0; HW = 800.0; G = 3.0            # door thickness, hinge distance, door-to-jamb gap
HINGE = (-HW, T)
E_MAX, E_MIN = 12.0, 1.0                 # bolt throw (tip x): sprung out / pulled back by the handle
BY0, BY1, BEV, BFLAT, BL = 13.6, 26.4, 10.5, 1.8, 30.0
HOLE = (13.0, 27.4, 20.0)                # strike hole y0, y1, depth x
JY1 = 45.0                               # jamb's opening-side edge
LOOP = 15.0; FS = 1200
V_SNAP = 130.0                           # mm/s outward bolt speed (spring), slowed down for the eye
PHI_MAX = math.radians(40)

def bolt_local(e):
    return Polygon([(e - BL, BY0), (e - BEV, BY0), (e, BY1 - BFLAT), (e, BY1), (e - BL, BY1)])
def to_world(poly, th): return affinity.rotate(poly, th, origin=HINGE, use_radians=True)

jamb = box(G, -25, 80, JY1).difference(box(G - 1, HOLE[0], G + HOLE[2], HOLE[1]))
lip = Polygon([(G, JY1 - 0.01), (G, 47.0), (4.5, 52.0), (8.0, 56.0), (9.3, 55.0), (6.0, 51.2), (4.6, 47.0), (4.6, JY1 - 0.01)])
stop = box(-10, -14, G + 0.5, 0)
FIXED = unary_union([jamb, lip])
def hits(e, th): return to_world(bolt_local(e), th).intersects(FIXED)

# ---- commanded door opening d (mm at the latch edge) and lever angle ----
def pchip_loop(keys):
    ts = np.array([k[0] for k in keys]); ds = np.array([k[1] for k in keys]); vs = np.array([k[2] for k in keys])
    def f(t):
        t = t % LOOP; i = np.searchsorted(ts, t, side='right') - 1; i = min(max(i, 0), len(ts) - 2)
        h = ts[i + 1] - ts[i]; u = (t - ts[i]) / h; h00 = 2*u**3 - 3*u**2 + 1; h10 = u**3 - 2*u**2 + u; h01 = -2*u**3 + 3*u**2; h11 = u**3 - u**2
        return h00 * ds[i] + h10 * h * vs[i] + h01 * ds[i + 1] + h11 * h * vs[i + 1]
    return f
# [t, d, dd/dt]; the closing push ends below 0 so the door really reaches the stop; the pull asks for +5 (the bolt only allows ~1)
DKEYS = [(0.0, 55.0, -3.0), (2.5, 48.0, -3.2), (3.5, 42.0, -12.0), (6.35, 0.6, -12.0), (6.65, -1.5, 0.0),
         (8.25, -1.5, 0.0), (8.55, 5.0, 0.0), (10.45, 5.0, 0.0), (12.2, 60.0, 0.0), (13.0, 58.4, -3.0), (15.0, 55.0, -3.0)]
dcmd = pchip_loop(DKEYS)
def lever(t):  # handle pushed down 10.0-10.35, released 12.35-12.6 (its spring brings it back)
    s = lambda u: 0 if u <= 0 else 1 if u >= 1 else u * u * (3 - 2 * u)
    return PHI_MAX * (s((t - 10.0) / 0.35) - s((t - 12.35) / 0.25))
def ecmd(t): return E_MAX - (E_MAX - E_MIN) * lever(t) / PHI_MAX
def theta(d): return math.asin(d / HW)

N = int(LOOP * FS); dt = 1.0 / FS
d = max(0.0, dcmd(0.0)); e = E_MAX; out = []; ev = []
state_contact = False; held = False; prev_e = e
for i in range(N + 1):
    t = i * dt; dc = max(0.0, dcmd(t)); th0 = theta(d)
    # handle pulls the bolt in directly
    if e > ecmd(t): e = ecmd(t)
    if dc < d:                      # closing: the slanted side meets the strike, the bolt is pushed in as far as needed
        d = dc; th = theta(d)
        if hits(e, th):
            lo, hi = E_MIN - 1, e
            for _ in range(30):
                m = 0.5 * (lo + hi)
                if hits(m, th): hi = m
                else: lo = m
            e = lo
            if not state_contact: ev.append({'t': t, 'type': 'contact'}); state_contact = True
    elif dc > d:                    # opening: the flat side meets the hole wall -> the door stops (no x force on a flat face)
        if hits(e, theta(dc)):
            lo, hi = d, dc
            for _ in range(30):
                m = 0.5 * (lo + hi)
                if hits(e, theta(m)): hi = m
                else: lo = m
            if not held and dc - lo > 0.05: ev.append({'t': t, 'type': 'hold'}); held = True
            d = lo
        else:
            d = dc; held = False
    th = theta(d)
    # spring pushes the bolt out toward the handle's limit, as far as the strike lets it
    tgt = min(ecmd(t), e + V_SNAP * dt)
    if tgt > e:
        if not hits(tgt, th): e = tgt
        else:
            lo, hi = e, tgt
            for _ in range(20):
                m = 0.5 * (lo + hi)
                if hits(m, th): hi = m
                else: lo = m
            e = lo
    if prev_e < E_MAX - 6 and e >= E_MAX - 6 and lever(t) < 1e-6 and i > 0:
        ev.append({'t': t, 'type': 'snap' if d < 5 else 'spring_out'})
    if state_contact and e >= E_MAX - 1e-6: state_contact = False
    prev_e = e
    out.append((t, d, e, lever(t)))

# stop thud: first time the door reaches d=0 (on the stop)
ds = np.array([o[1] for o in out]); ts = np.array([o[0] for o in out])
i0 = int(np.argmax(ds <= 1e-9)); ev.append({'t': float(ts[i0]), 'type': 'stop'})
ev.append({'t': 10.0, 'type': 'handle'}); ev.append({'t': 12.35, 'type': 'handle_back'})
ev.sort(key=lambda x: x['t'])
for x in ev: x['t'] = round(x['t'], 4)
print('events', ev)
print('d start/end %.3f %.3f  e start/end %.3f %.3f' % (out[0][1], out[-1][1], out[0][2], out[-1][2]))
print('min e %.2f  max d %.2f  d during pull %.3f' % (min(o[2] for o in out), ds.max(), ds[int(9.0 * FS)]))
kin = [{'d': round(o[1], 4), 'th': round(theta(o[1]), 7), 'e': round(o[2], 4), 'phi': round(o[3], 5)} for o in out[0:N:FS // 240]]
json.dump(kin, open('kin_240.json', 'w')); json.dump(ev, open('events.json', 'w'), indent=0)
geo = {'T': T, 'HW': HW, 'G': G, 'HINGE': HINGE, 'E_MAX': E_MAX, 'E_MIN': E_MIN, 'BY0': BY0, 'BY1': BY1, 'BEV': BEV, 'BFLAT': BFLAT, 'BL': BL,
       'HOLE': HOLE, 'JY1': JY1, 'LOOP': LOOP, 'lip': list(lip.exterior.coords)[:-1], 'PHI_MAX': PHI_MAX}
json.dump(geo, open('geom.json', 'w'), indent=0)
