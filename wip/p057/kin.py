# p057 gas cap: why does it click? Torque-limiting ratchet. mm, planar section in x-y (z = cap axis toward the viewer).
# Body (closer) carries 12 inclined teeth (ramp + steep face). The handle (cover) carries two flexible arms whose round nubs
# sit in the tooth corners. Tightening (clockwise seen from outside, angle decreasing): the nub pushes on the ramp and drives the
# body until the seal stops it; then the nub rides up the ramp (arm bends outward) and drops off the edge = CLICK.
# Loosening (counter-clockwise): the nub pushes the steep face = positive drive, no slip.
# The arm deflection d(psi) is the smallest outward offset that keeps the nub 0.05 mm clear of the teeth (bisection, shapely).
import json, math, numpy as np
from shapely.geometry import Polygon, Point, box
from shapely import affinity
N = 12; P = 2 * math.pi / N; R0 = 12.0; H = 3.5; RHO = 1.3; GAP = 0.05
RA = 19.2; AW = 1.0; ARM_SPAN = math.radians(70); A_TIP = math.radians(90)  # arm centre radius, half width, span, tip angle (handle frame)
RC0 = R0 + RHO + GAP  # nominal (undeflected) nub centre radius
LOOP = 15.0
def gear_pts(n_ramp=40):
    pts = []
    for k in range(N):
        a0 = k * P
        for i in range(n_ramp + 1):
            u = i / n_ramp; th = a0 + u * P; r = R0 + H * (1 - u)
            if i == 0: r = R0 + H - 0.0  # tooth top (sharp edge)
            pts.append((r * math.cos(th), r * math.sin(th)))
        # steep face at a0+P: from root up to the next top (next tooth's i=0 point)
    return pts
GEAR = Polygon(gear_pts()).buffer(0)
def nub_poly(psi, d):  # nub (circle + finger up to the arm) in BODY frame, centre angle psi, outward offset d
    rc = RC0 + d; c = Point(rc, 0).buffer(RHO, 48); f = box(rc, -RHO, RA - AW + d + 0.4, RHO)
    return affinity.rotate(c.union(f), psi, origin=(0, 0), use_radians=True)
def defl(psi):
    lo, hi = 0.0, H + 1.0
    if nub_poly(psi, 0).distance(GEAR) >= GAP - 1e-6: return 0.0
    for _ in range(40):
        m = (lo + hi) / 2
        if nub_poly(psi, m).distance(GEAR) >= GAP - 1e-6: hi = m
        else: lo = m
    return hi
# corner (valley) of tooth k=1: lowest deflection just clockwise of the steep face at angle P
ps = np.linspace(P - math.radians(14), P - 0.0005, 300); ds = [defl(p) for p in ps]; PSI_C = float(ps[int(np.argmin(ds))]); D_C = float(min(ds))
# peak just before the nub falls off the previous edge (angle 0): scan psi from PSI_C down to about -6 deg
ps2 = np.linspace(PSI_C, -math.radians(6), 900); ds2 = [defl(p) for p in ps2]; ip = int(np.argmax(ds2)); PSI_PK = float(ps2[ip]); D_PK = float(ds2[ip])
print('corner %.3f deg d=%.3f, peak %.3f deg d=%.3f' % (math.degrees(PSI_C), D_C, math.degrees(PSI_PK), D_PK))
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(max(u, 0), 1))
smq = lambda u: (lambda v: v * v * v * (v * (6 * v - 15) + 10))(min(max(u, 0), 1))
A = (0.25, 4.4); TH_A = math.radians(-60)
SLIP0 = 4.9; TOOTH = 1.15; CLIMB = 0.95; SNAP = 0.07; NS = 3
D = (9.6, 12.4); TH_D = math.radians(150)
def state(t):  # handle angle Hh, body angle Bd (rad), relative nub angle psi (body frame, tooth-local), click flag
    t = t % LOOP; Bd = 0.0; rel = 0.0  # rel = extra handle advance relative to body (multiples of the tooth motion)
    if t < A[0]: Bd = 0
    elif t < A[1]: Bd = TH_A * smq((t - A[0]) / (A[1] - A[0]))
    else: Bd = TH_A
    psi = PSI_C; slip = 0.0
    for j in range(NS):
        t0 = SLIP0 + j * TOOTH
        if t >= t0 + CLIMB + SNAP: slip += P
        elif t >= t0 + CLIMB: u = (t - t0 - CLIMB) / SNAP; psi = PSI_PK - (PSI_PK - (PSI_C - P)) * u; slip += 0; break
        elif t >= t0: psi = PSI_C - (PSI_C - PSI_PK) * sm((t - t0) / CLIMB); break
    if t >= D[0]:
        Bd += TH_D * smq((t - D[0]) / (D[1] - D[0]))
    Hh = Bd + (psi - PSI_C) - slip  # handle = body + relative motion (clockwise is negative)
    return Hh, Bd, psi
rows = []
for i in range(int(LOOP * 240)):
    t = i / 240; Hh, Bd, psi = state(t); d = defl(psi)
    rows.append(dict(h=round(Hh, 6), b=round(Bd, 6), psi=round(psi, 6), d=round(d, 4)))
json.dump(rows, open('kin_240.json', 'w'))
ev = [dict(type='turn', t0=A[0], t1=A[1]), dict(type='seal', t=A[1])]
for j in range(NS):
    t0 = SLIP0 + j * TOOTH
    # landing = first sample after the edge where deflection is back near the valley
    tl = next(i / 240 for i in range(int((t0 + CLIMB) * 240), int((t0 + CLIMB + 0.2) * 240)) if rows[i]['d'] < D_C + 0.15)
    ev.append(dict(type='climb', t0=t0, t1=t0 + CLIMB)); ev.append(dict(type='click', t=tl))
ev += [dict(type='grab', t=D[0] + 0.05), dict(type='turn', t0=D[0], t1=D[1])]
json.dump(ev, open('events.json', 'w'), indent=1)
G = dict(N=N, P=P, R0=R0, H=H, RHO=RHO, GAP=GAP, RA=RA, AW=AW, ARM_SPAN=ARM_SPAN, A_TIP=A_TIP, RC0=RC0, LOOP=LOOP, PSI_C=PSI_C, D_C=D_C, PSI_PK=PSI_PK,
         GEAR=[list(p) for p in GEAR.exterior.coords][:-1], A=A, D=D, SLIP0=SLIP0, TOOTH=TOOTH, CLIMB=CLIMB, SNAP=SNAP, NS=NS)
json.dump(G, open('geom.json', 'w'))
e = state(LOOP - 1e-9); s = state(0)
print('loop: handle %.4f -> %.4f deg; body %.3f deg (must be a multiple of %.1f)' % (math.degrees(s[0]), math.degrees(e[0]), math.degrees(e[1]), math.degrees(P)))
print('events', [(x['type'], round(x.get('t', x.get('t0')), 3)) for x in ev])
