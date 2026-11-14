# p065 snap mousetrap "WHAT HOLDS / IT BACK?" - kinematics (mm, seconds). x = along the base (rear -x, front +x), y up, z across.
# Mechanism (Hooker US 528,671): the coiled spring pushes the jaw forward/down; when set, the jaw is held back by a locking bar that
# passes over it, hinged at the rear of the base; the bar's front tip sits under the rearward shoulder (lip) of a catch on the hinged
# trigger. Pressing the trigger (bait) tilts the catch, the lip slides off the tip, and the spring swings the jaw over.
# Writes geom.json (constants + events) and kin.json (samples at 120 Hz: t, alpha, beta, phi, pencil dy).
import json, math
import numpy as np
from shapely.geometry import Point, LineString, Polygon
from shapely import affinity

D = math.radians
G = dict(LOOP=23.0, BASE=dict(x0=-49, x1=49, w=45, top=10.0),
         A=[0.0, 14.5], RJ=38.2, RW=0.7, JW=17.0,          # jaw: coil axis A, crossbar radius RJ, wire radius RW, half width JW
         P=[-47.5, 11.2], LB=60.0, RB=0.8,                 # locking bar: rear pivot P, length LB, wire radius RB
         Q=[13.0, 12.0],                                   # trigger pintle (hinge) axis
         PHI0=D(9.0),                                      # trigger set tilt (front up), radians; phi below = extra rotation (front down)
         PEN_ANG=D(52.0), PEN_R=3.6)
P = np.array(G['P']); A = np.array(G['A']); Q = np.array(G['Q'])
LB, RB, RJ, RW = G['LB'], G['RB'], G['RJ'], G['RW']
# set bar angle: tip center at y = 17.6
B0 = math.asin((17.6 - P[1]) / LB); G['B0'] = B0
tip0 = P + LB * np.array([math.cos(B0), math.sin(B0)])
def bar_dir(b): return np.array([math.cos(b), math.sin(b)])
def crossbar(a): return A + RJ * np.array([math.cos(a), math.sin(a)])
def dist_line(c, b):  # signed distance of point c above(+)/below(-) the bar line
    d = bar_dir(b); n = np.array([-d[1], d[0]]); return float(np.dot(c - P, n))
# jaw set angle: crossbar exactly RB+RW below the bar line (resting against it), alpha slightly past 180
lo, hi = D(180.0), D(200.0)
for _ in range(60):
    m = (lo + hi) / 2; s = dist_line(crossbar(m), B0) + (RB + RW)
    (lo, hi) = (m, hi) if s > 0 else (lo, m)
A0 = (lo + hi) / 2; G['A0'] = A0
# catch (part of the trigger, in trigger coords relative to Q, at phi=0): upright plate + rearward lip (2D polygons in x-y)
LIP_Y = tip0[1] + RB + 0.05                     # lip underside just above the tip
ENG = 1.0                                      # lip overlaps the tip end by 1.0 mm
tip_end_x = tip0[0] + RB
lip_rear = tip_end_x - ENG
UP_X0 = tip_end_x + 0.35                        # upright rear face, 0.35 mm in front of the tip end
catch_parts = [
    [(UP_X0, Q[1] - 1.2), (UP_X0 + 0.8, Q[1] - 1.2), (UP_X0 + 0.8, LIP_Y + 0.8), (UP_X0, LIP_Y + 0.8)],             # upright
    [(lip_rear, LIP_Y), (UP_X0, LIP_Y), (UP_X0, LIP_Y + 0.8), (lip_rear, LIP_Y + 0.8)],                            # lip
]
PL = 31.0                                       # trigger plate length from the hinge, thickness 0.8
plate = [(Q[0] - 1.0, Q[1] - 0.4), (Q[0] + PL, Q[1] - 0.4), (Q[0] + PL, Q[1] + 0.4), (Q[0] - 1.0, Q[1] + 0.4)]
G.update(catch=catch_parts, plate=plate, LIP_Y=LIP_Y, lip_rear=lip_rear, UP_X0=UP_X0, PL=PL, tip0=tip0.tolist())
def trig_world(pts, phi): return affinity.rotate(Polygon(pts), -phi, origin=tuple(Q), use_radians=True)  # set pose -> pressed by phi (front down)
plate = list(affinity.rotate(Polygon(plate), G['PHI0'], origin=tuple(Q), use_radians=True).exterior.coords)[:-1]   # plate tilted front-up when set
G['catch'] = [[list(c) for c in p] for p in catch_parts]; G['plate'] = [list(c) for c in plate]
def lip_rear_x(phi): return min(x for x, y in trig_world(catch_parts[1], phi).exterior.coords)
phis = np.linspace(0, D(15), 3000); PHR = next(p for p in phis if lip_rear_x(p) > tip_end_x + 0.02); G['PHR'] = float(PHR)
# cheese on the plate (in plate coords: from the hinge 20..29 mm, height 6), pencil eraser presses its top at 25 mm
CH = dict(x0=13.5, x1=22.5, h=6.2, w=10.0); G['CH'] = CH
def plate_pt(u, v, phi):  # point (u along plate from hinge, v above plate centerline) -> world, at trigger angle PHI0 - phi
    th = G['PHI0'] - phi; return Q + np.array([u * math.cos(th) - v * math.sin(th), u * math.sin(th) + v * math.cos(th)])
press_pt = lambda phi: plate_pt(18.0, 0.4 + CH['h'], phi)
# ---------------- timeline ----------------
T_IN0, T_TOUCH, T_REL = 13.2, 13.9, 16.0     # pencil enters, touches the cheese, lip slips off the tip
T_SNAP = 1.20                                  # slow-motion swing duration (video seconds)
PHI_END = PHR + D(1.0)
EV = dict(touch=T_TOUCH, release=T_REL)
pen_dir = np.array([math.cos(G['PEN_ANG']), math.sin(G['PEN_ANG'])])
def phi_t(t):
    if t < T_TOUCH: return 0.0
    if t < T_REL: u = (t - T_TOUCH) / (T_REL - T_TOUCH); return PHR * (u * u * (3 - 2 * u) * 0.25 + 0.75 * u ** 1.6) / 1.0
    if t < T_REL + 0.15: return PHR + (PHI_END - PHR) * (t - T_REL) / 0.15
    return PHI_END
# pencil tip: eraser end center = press point + PEN_R along -normal... keep it simple: tip center sits PEN_R above the cheese top point
def pen_tip(t):
    if t < T_TOUCH:
        u = max(0.0, (t - T_IN0) / (T_TOUCH - T_IN0)); u = u * u * (3 - 2 * u)
        return press_pt(0.0) + np.array([0, G['PEN_R']]) + pen_dir * 160.0 * (1 - u)
    return press_pt(phi_t(t)) + np.array([0, G['PEN_R']])
# jaw hit on the pencil: first alpha below A0 at which the crossbar touches the pencil body capsule (at the pressed pose)
pt_end = pen_tip(20.0); pen_seg = LineString([tuple(pt_end), tuple(pt_end + pen_dir * 200)])
alphas = np.linspace(A0, 0, 20000)
AH = next(a for a in alphas if Point(*crossbar(a)).distance(pen_seg) <= G['PEN_R'] + RW + 0.05); G['AH'] = float(AH)
def alpha_t(t):
    if t < T_REL: return A0
    u = (t - T_REL) / T_SNAP
    if u < 1: return A0 - (A0 - AH) * u ** 1.7
    v = (t - T_REL - T_SNAP)
    return AH + D(2.5) * math.exp(-v * 9) * abs(math.sin(v * 22))   # small rebound off the pencil, then pinned
# bar: held at B0; after release it rides on the crossbar (contact angle), keeps going a little, then falls back to rest on the catch
def bar_contact(a):
    c = crossbar(a); d = c - P; r = np.linalg.norm(d)
    if r > LB + 1: return -9
    return math.atan2(d[1], d[0]) + math.asin(min(1, (RB + RW) / r))
def bar_hits(b, phi):
    seg = LineString([tuple(P), tuple(P + LB * bar_dir(b))]).buffer(RB, 16)
    return any(seg.intersection(trig_world(p, phi)).area > 1e-4 for p in catch_parts + [plate])
# rest angle after the snap: the bar falls until it touches the tilted catch
bs = np.linspace(D(40), B0 - D(5), 4000); B_REST = next(b for b in bs if bar_hits(b, PHI_END)) + D(0.15); G['B_REST'] = float(B_REST)
ts = np.arange(0, G['LOOP'] + 1e-9, 1 / 120)
al = np.array([alpha_t(t) for t in ts])
be = np.full_like(ts, B0); peak_i = None
for i, t in enumerate(ts):
    if t < T_REL: continue
    c = bar_contact(al[i]); be[i] = max(be[i - 1] if peak_i is None else be[i], c)
    if peak_i is None and al[i] < D(98): peak_i = i; break
tp, bp = ts[peak_i], be[peak_i]; w_end = (be[peak_i] - be[peak_i - 3]) / (3 / 120)
B_PEAK = bp + D(4); T_PK = tp + 0.22; T_DOWN = T_PK + 0.55
for i in range(peak_i, len(ts)):
    t = ts[i]
    if t < T_PK: u = (t - tp) / (T_PK - tp); be[i] = bp + (B_PEAK - bp) * (1 - (1 - u) ** 2)
    elif t < T_DOWN: u = (t - T_PK) / (T_DOWN - T_PK); be[i] = B_PEAK + (B_REST - B_PEAK) * u * u
    else: v = t - T_DOWN; be[i] = B_REST + D(3.0) * math.exp(-v * 8) * abs(math.sin(v * 18))
ph = np.array([phi_t(t) for t in ts]); pen = np.array([pen_tip(t) for t in ts])
EV.update(hit=T_REL + T_SNAP, bar_peak=T_PK, bar_land=T_DOWN)
G['EV'] = EV; G['pen_dir'] = pen_dir.tolist()
json.dump(G, open('geom.json', 'w'), indent=1)
json.dump([[round(float(t), 4), round(float(a), 5), round(float(b), 5), round(float(p), 5), round(float(x), 3), round(float(y), 3)] for t, a, b, p, (x, y) in zip(ts, al, be, ph, pen)], open('kin.json', 'w'))
print('A0 %.2f B0 %.2f PHR %.2f AH %.2f B_REST %.2f' % tuple(math.degrees(v) for v in (A0, B0, PHR, AH, B_REST)), 'tip0', tip0.round(2), 'events', EV)
