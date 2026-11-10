# p060 handcuff double lock: geometry + kinematics (mm, cuff plane = xy, plates stacked in z).
# Arm (single strand) pivots at P=(0,0); its toothed tail (teeth on r 70.4..72, pitch 2 deg) passes the housing at world angle 0.
# Pawl pivots at Q, spring pushes its toothed pad onto the arm teeth; the double-lock bolt slides (y) behind the pad.
# phi = arm rotation (deg, + = clockwise = tighter). A point at arm-frame angle th appears at th - phi.
import json, math, numpy as np
from shapely.geometry import Polygon, Point
from shapely import affinity
from shapely.ops import unary_union
P = np.array([0.0, 0.0]); Q = np.array([86.0, 15.0])
PITCH = 2.0; R_TIP = 72.0; R_ROOT = 70.4; R_IN = 64.2; TH_TIP = -42.0
def r_arm(th):  # sawtooth: gentle rise toward +th, steep (radial) drop at each tip th = k*PITCH
    u = (th / PITCH) % 1.0; return R_ROOT + (R_TIP - R_ROOT) * (u / 0.82 if u < 0.82 else (1 - u) / 0.18)
def pol(r, a): a = math.radians(a); return (r * math.cos(a), r * math.sin(a))
# ---- arm polygon (arm frame) ----
tail_out = []; th = TH_TIP + 0.6
while th <= 0.0001: tail_out.append(pol(r_arm(th), th)); th += 0.05
C = (35.6, 0.0); RB = 35.6; HW = 3.9   # bow: upper semicircle around C (centerline), half width HW
bow_out = [(C[0] + (RB + HW) * math.cos(math.radians(a)), C[1] + (RB + HW) * math.sin(math.radians(a))) for a in np.linspace(8, 180, 90)]
bow_in = [(C[0] + (RB - HW) * math.cos(math.radians(a)), C[1] + (RB - HW) * math.sin(math.radians(a))) for a in np.linspace(180, 0, 90)]
eye = Point(0, 0).buffer(7.5, 64)   # pivot eye around the rivet
tail_in = [pol(R_IN, a) for a in np.linspace(0, TH_TIP, 60)]
tail = Polygon(tail_out[::-1] + tail_in[::-1])  # outer from 0 down to tip, inner from tip back up
tail = Polygon([pol(R_IN, TH_TIP), pol(R_ROOT - 0.2, TH_TIP + 0.0)] + tail_out + [pol(R_TIP - 0.4, 2.0), pol(R_IN, 2.0)] + [pol(R_IN, a) for a in np.linspace(2.0, TH_TIP, 60)][1:])
bow = Polygon(bow_out + bow_in)
ARM = unary_union([tail.buffer(0), bow.buffer(0), eye, Point(C[0] + RB, 0).buffer(HW + 0.2, 32)]).buffer(0.25).buffer(-0.25)
ARM = ARM.difference(Point(0, 0).buffer(2.6, 48))  # rivet hole
# ---- pawl polygon (world, psi = 0, seated with tips at th = k*PITCH when phi = multiple of PITCH) ----
CL = 0.05
pad_in = [pol(r_arm(a) + CL, a) for a in np.arange(-3.9, 3.95, 0.05)]  # tooth face (seated phi=0 -> th = a)
PAWL = Polygon([(79.0, pad_in[0][1])] + pad_in + [(73.6, 5.4), (82.4, 17.6), *[(Q[0] + 3.6 * math.cos(math.radians(a)), Q[1] + 3.6 * math.sin(math.radians(a))) for a in np.linspace(140, -40, 30)], (79.0, 0.6)]).buffer(0)
PAWL = PAWL.difference(Point(*Q).buffer(1.3, 32))
# ---- bolt (world), y offset b: 0 = OUT, 1 = IN ----
BOLT_OUT_Y = -10.8; BOLT_IN_Y = -4.6; BOLT_H = 4.5
def bolt_poly(b): y0 = BOLT_OUT_Y + (BOLT_IN_Y - BOLT_OUT_Y) * b; return Polygon([(79.1, y0), (84.2, y0), (84.2, y0 + BOLT_H), (79.1, y0 + BOLT_H)])
SPRING = (83.6, 94.0, 5.0, 1.7)  # x0 (rest, on the lever edge), x1 (wall), y, coil radius
def arm_at(phi): return affinity.rotate(ARM, -phi, origin=(0, 0))
def pawl_at(psi): return affinity.rotate(PAWL, psi, origin=tuple(Q))
_PC = {}
def psi_min(phi, cap=14.0):  # smallest lift keeping the clearance
    key = round(phi, 6)
    if key in _PC: return _PC[key]
    _PC[key] = v = _psi(phi, cap); return v
def _psi(phi, cap):
    A = arm_at(phi)
    if pawl_at(0).distance(A) >= 0.03: return 0.0
    lo, hi = 0.0, cap
    if pawl_at(hi).distance(A) < 0.03: return None
    for _ in range(22):
        m = (lo + hi) / 2
        if pawl_at(m).distance(A) >= 0.03: hi = m
        else: lo = m
    return hi
# ---- timeline ----
LOOP = 41.0; FPS_K = 240
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
CLICKS = [(1.15, 1.95, -22, -20), (9.5, 10.6, -20, -18), (11.7, 12.8, -18, -16), (19.2, 19.75, -16, -14), (20.35, 20.9, -14, -12)]
def phi_of(t):
    v = -22.0
    for a, b, p0, p1 in CLICKS:
        if t >= a: v = p0 + (p1 - p0) * ease((t - a) / (b - a))
    return v
PUSHES = {'pull1': (14.6, 16.6), 'push_blk': (29.6, 31.0), 'pull_blk': (31.8, 33.2)}  # force shown, arm blocked (no motion)
PIN = (23.5, 24.5, 26.0, 27.0, 28.0)  # pin rises to the hole, pushes the bolt (24.5-26.0), stays, withdraws
def bolt_of(t): return ease((t - PIN[1]) / (PIN[2] - PIN[1])) if t < 40.4 else 1.0
PIN_TIP_OUT = -22.0; HOLE_Y = -14.0; PIN_LEN = 11.0
def pin_tip(t):  # y of the key pin tip (x = 81.65); it touches the bolt bottom while pushing
    if t < PIN[0] or t > PIN[4] + 0.01: return None
    yb = BOLT_OUT_Y + (BOLT_IN_Y - BOLT_OUT_Y) * bolt_of(t)
    if t < PIN[1]: return PIN_TIP_OUT + (yb - 0.05 - PIN_TIP_OUT) * ease((t - PIN[0]) / (PIN[1] - PIN[0]))
    if t < PIN[3]: return yb - 0.05
    return yb - 0.05 + (PIN_TIP_OUT - yb + 0.05) * ease((t - PIN[3]) / (PIN[4] - PIN[3]))
if __name__ == '__main__':
    N = int(LOOP * FPS_K); rows = []; psi_prev = 0.0; clicks = []
    for i in range(N):
        t = i / FPS_K; ph = phi_of(t); need = psi_min(ph)
        assert need is not None, ('arm jams', t)
        dmax = 260.0 / FPS_K  # spring snap-back rate limit (deg/s)
        psi = need if need >= psi_prev else max(need, psi_prev - dmax)
        if psi_prev - need > 3.0: clicks.append(round(t, 3))
        psi_prev = psi
        rows.append({'t': round(t, 4), 'phi': round(ph, 5), 'psi': round(psi, 5), 'b': round(bolt_of(t), 5), 'pin': pin_tip(t)})
    # geometry export (outer ring + holes as lists)
    def rings(g):
        g = g if g.geom_type == 'Polygon' else max(g.geoms, key=lambda x: x.area)
        return {'ext': [list(map(lambda v: round(v, 3), p)) for p in g.exterior.coords], 'holes': [[list(map(lambda v: round(v, 3), p)) for p in h.coords] for h in g.interiors]}
    # housing spacer (mid layer): housing outline minus the arm channel, the pawl sweep, the bolt channel, the spring pocket and the pin hole
    HOUS = Polygon([(62.0, -14.0), (97.0, -14.0), (97.0, 23.0), (62.0, 23.0)]).buffer(-3, join_style=1).buffer(3, join_style=1)
    chan = Polygon([pol(R_IN - 0.5, a) for a in np.linspace(-60, 40, 80)] + [pol(R_TIP + 0.5, a) for a in np.linspace(40, -60, 80)])
    sweep = unary_union([pawl_at(s) for s in np.linspace(0, 12, 13)]).buffer(0.4)
    bch = unary_union([bolt_poly(b) for b in np.linspace(0, 1, 9)]).buffer(0.2)
    spk = Polygon([(82.5, 2.6), (95.0, 2.6), (95.0, 7.4), (82.5, 7.4)])
    hole = Polygon([(80.6, -16), (82.7, -16), (82.7, -10.0), (80.6, -10.0)])
    qpin = Point(*Q).buffer(1.25, 32)
    asw = unary_union([arm_at(p) for p in np.arange(-34, -3.9, 0.5)]).buffer(0.5)
    SPACER = HOUS.difference(unary_union([chan, sweep, bch, spk, hole, asw])).buffer(0).buffer(-0.3).buffer(0.3)
    geo = {'LOOP': LOOP, 'Q': list(Q), 'PITCH': PITCH, 'R_TIP': R_TIP, 'R_ROOT': R_ROOT, 'C': C, 'RB': RB, 'HW': HW, 'BOLT': [BOLT_OUT_Y, BOLT_IN_Y, BOLT_H, 79.1, 84.2],
           'SPRING': SPRING, 'HOLE_Y': HOLE_Y, 'PIN_X': 81.65, 'PIN_LEN': PIN_LEN, 'CLICKS': clicks, 'PUSHES': PUSHES, 'PIN': PIN,
           'ARM': rings(ARM), 'PAWL': rings(PAWL), 'HOUS': rings(HOUS), 'WRIST': [35.0, 11.0, 24.0, 28.0], 'SPACER': [rings(g) for g in (SPACER.geoms if SPACER.geom_type != 'Polygon' else [SPACER])]}
    json.dump(geo, open('geom.json', 'w')); json.dump(rows, open('kin_240.json', 'w'), separators=(',', ':'))
    print('clicks at', clicks); print('max psi', max(r['psi'] for r in rows)); print('spacer parts', len(geo['SPACER']))
