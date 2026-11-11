# p062 open differential kinematics (mm, s). Car frame: x right, y up, -z forward; rear axle on x at y=R_TIRE.
# Rotations about +x; forward rolling = negative angle. c = carrier (ring gear) angle, d = half speed difference:
#   right wheel thR = c + d, left wheel thL = c - d (open differential: thL + thR = 2c).
# Side gears turn by +-d relative to the carrier; each spider turns -(Z_SIDE/Z_SPIDER)*d about its own pin axis.
# Pinion turns (Z_RING/Z_PINION) times the ring gear. Gear phase offsets are solved here and verified in check.py.
import json, math
import numpy as np
FPS = 240; LOOP = 42.0
Z_RING, Z_PIN, Z_SIDE, Z_SPI = 41, 11, 16, 10
R_TIRE, TRACK = 330.0, 1500.0
# geometry (pitch radius at the outer end, pitch angle)
RING_R = 100.0; G_RING = math.atan2(Z_RING, Z_PIN); G_PIN = math.pi / 2 - G_RING; A_RP = RING_R / math.sin(G_RING); PIN_R = A_RP * math.sin(G_PIN)
SIDE_R = 40.0; G_SIDE = math.atan2(Z_SIDE, Z_SPI); G_SPI = math.pi / 2 - G_SIDE; A_SS = SIDE_R / math.sin(G_SIDE); SPI_R = A_SS * math.sin(G_SPI)
XA = 46.0 - A_RP * math.cos(G_RING)  # ring/pinion common apex on the axle axis; ring gear plane at x=46
def sm(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def ramp(t, a, b, v0, v1): return v0 + (v1 - v0) * sm((t - a) / (b - a))
def kfun(t):  # speed split: +k -> right wheel faster (left turn)
    if t < 10.0: return 0.2
    if t < 12.0: return ramp(t, 10.0, 12.0, 0.2, 0.0)
    if t < 24.8: return 0.0
    if t < 26.3: return ramp(t, 24.8, 26.3, 0.0, 0.25)
    if t < 32.6: return 0.25
    if t < 33.4: return ramp(t, 32.6, 33.4, 0.25, 1.0)
    if t < 36.6: return 1.0
    if t < 37.4: return ramp(t, 36.6, 37.4, 1.0, 0.25)
    if t < 40.6: return 0.25
    return ramp(t, 40.6, 42.0, 0.25, 0.2)
def wfun(t):  # carrier speed rad/s (0.5 rev/s); slow motion at the key moment of step 2
    w = 2 * math.pi * 0.5
    if 25.6 <= t < 30.0: w *= ramp(t, 25.6, 26.4, 1, 0.45) if t < 27.0 else ramp(t, 29.2, 30.0, 0.45, 1)
    return w
N = int(LOOP * FPS) + 2
c = d = 0.0; x = z = psi = 0.0; rows = []
for i in range(N):
    t = i / FPS; k = kfun(t); w = wfun(t)
    rows.append(dict(t=round(t, 5), c=c, d=d, k=k, x=x, z=z, psi=psi))
    dt = 1 / FPS; c -= w * dt; d -= k * w * dt
    v = w * R_TIRE; yaw = 2 * k * w * R_TIRE / TRACK
    psi += yaw * dt; x += -math.sin(psi) * v * dt; z += -math.cos(psi) * v * dt
# --- frames ---
def rot_x(a): ca, sa = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, ca, -sa], [0, sa, ca]])
def basis(axis, u):
    axis = np.array(axis, float); u = np.array(u, float); v = np.cross(axis, u); return axis, u, v
GEARS = {  # name: (frame 'carrier'|'housing', apex, axis, u, Z, gamma, A0)
 'sideR': ('carrier', (0, 0, 0), (1, 0, 0), (0, 1, 0), Z_SIDE, G_SIDE, A_SS),
 'sideL': ('carrier', (0, 0, 0), (-1, 0, 0), (0, 1, 0), Z_SIDE, G_SIDE, A_SS),
 'spi0': ('carrier', (0, 0, 0), (0, 1, 0), (1, 0, 0), Z_SPI, G_SPI, A_SS),
 'spi1': ('carrier', (0, 0, 0), (0, -1, 0), (1, 0, 0), Z_SPI, G_SPI, A_SS),
 'ring': ('carrier', (XA, 0, 0), (1, 0, 0), (0, 1, 0), Z_RING, G_RING, A_RP),
 'pin': ('housing', (XA, 0, 0), (0, 0, -1), (0, 1, 0), Z_PIN, G_PIN, A_RP),
}
def local_angle(name, r):  # rotation of the gear about its own axis (without offset)
    if name == 'sideR' or name == 'sideL': return r['d']
    if name in ('spi0', 'spi1'): return -Z_SIDE / Z_SPI * r['d']
    if name == 'ring': return 0.0
    if name == 'pin': return SGN_PIN * Z_RING / Z_PIN * r['c']
SGN_PIN = 1.0
def teeth(name, r, off):  # tooth-centre points on the outer pitch circle, housing frame
    fr, apex, axis, u, Z, g, A0 = GEARS[name]; a, uu, vv = basis(axis, u); ang = local_angle(name, r) + off
    phi = 2 * np.pi * np.arange(Z) / Z + ang
    P = np.array(apex) + A0 * (math.sin(g) * (np.outer(np.cos(phi), uu) + np.outer(np.sin(phi), vv)) + math.cos(g) * a)
    if fr == 'carrier': P = P @ rot_x(r['c']).T
    return P
PAIRS = [('sideR', 'spi0'), ('sideR', 'spi1'), ('sideL', 'spi0'), ('sideL', 'spi1'), ('ring', 'pin')]
def contact(A, B, r):  # outer pitch contact point = common generator end
    fa, apA, axA = GEARS[A][0], np.array(GEARS[A][1], float), np.array(GEARS[A][2], float); fb, axB = GEARS[B][0], np.array(GEARS[B][2], float)
    gA, gB, A0 = GEARS[A][5], GEARS[B][5], GEARS[A][6]
    if fa == 'carrier': R = rot_x(r['c']); axA = R @ axA; apA = R @ apA
    if fb == 'carrier': axB = rot_x(r['c']) @ axB
    gen = math.cos(gA) * axA + math.cos(gB) * axB; gen /= np.linalg.norm(gen)
    C = apA + A0 * gen; T = np.cross(axA, C - apA); T /= np.linalg.norm(T); return C, T
def mesh_offset(A, B, r, oA, oB):
    C, T = contact(A, B, r); PA = teeth(A, r, oA); PB = teeth(B, r, oB)
    ia = np.argmin(np.linalg.norm(PA - C, axis=1)); ib = np.argmin(np.linalg.norm(PB - C, axis=1))
    pitch = 2 * math.pi * GEARS[A][6] * math.sin(GEARS[A][5]) / GEARS[A][4]
    s = ((PA[ia] - C) @ T - (PB[ib] - C) @ T) / pitch; return (s % 1.0), pitch
def solve_offsets():
    global SGN_PIN
    off = {'sideR': 0.0, 'ring': 0.0}
    r0 = rows[0]
    def fix(A, B):  # choose off[B] so that the mesh offset is 0.5 pitch at t=0
        best = None
        for j in range(720):
            ob = j / 720 * 2 * math.pi / GEARS[B][4]
            s, _ = mesh_offset(A, B, r0, off[A], ob); e = abs(s - 0.5)
            if best is None or e < best[0]: best = (e, ob)
        off[B] = best[1]
    fix('sideR', 'spi0'); fix('sideR', 'spi1')
    # sideL from spi0
    best = None
    for j in range(720):
        oL = j / 720 * 2 * math.pi / Z_SIDE; s, _ = mesh_offset('sideL', 'spi0', r0, oL, off['spi0']); e = abs(s - 0.5)
        if best is None or e < best[0]: best = (e, oL)
    off['sideL'] = best[1]
    # pinion sign: pick the one that keeps the mesh
    for sg in (1.0, -1.0):
        SGN_PIN = sg; fix('ring', 'pin')
        r1 = rows[FPS // 7]; s, _ = mesh_offset('ring', 'pin', r1, off['ring'], off['pin'])
        if abs(s - 0.5) < 0.02: break
    return off
OFF = solve_offsets()
out = []
for r in rows[::1]:
    out.append([round(r['t'], 4), round(r['c'], 5), round(r['d'], 5), round(r['k'], 4), round(r['x'], 1), round(r['z'], 1), round(r['psi'], 5),
                round(local_angle('sideR', r) + OFF['sideR'], 5), round(local_angle('sideL', r) + OFF['sideL'], 5), round(local_angle('spi0', r) + OFF['spi0'], 5),
                round(local_angle('spi1', r) + OFF['spi1'], 5), round(local_angle('ring', r) + OFF['ring'], 5), round(local_angle('pin', r) + OFF['pin'], 5)])
json.dump(out, open('kin_240.json', 'w'), separators=(',', ':'))
geom = dict(LOOP=LOOP, FPS=FPS, Z=dict(ring=Z_RING, pin=Z_PIN, side=Z_SIDE, spi=Z_SPI), R_TIRE=R_TIRE, TRACK=TRACK, XA=XA,
            RING=[RING_R, G_RING, A_RP], PIN=[PIN_R, G_PIN, A_RP], SIDE=[SIDE_R, G_SIDE, A_SS], SPI=[SPI_R, G_SPI, A_SS], SGN_PIN=SGN_PIN, OFF=OFF,
            cols='t c d k x z psi sideR sideL spi0 spi1 ring pin'.split())
json.dump(geom, open('geom.json', 'w'), indent=1)
print('ok', len(out), 'rows; offsets', {k: round(v, 4) for k, v in OFF.items()}, 'SGN_PIN', SGN_PIN, 'XA', round(XA, 2), 'PIN_R', round(PIN_R, 2), 'SPI_R', round(SPI_R, 2), 'A_SS', round(A_SS, 2))
print('car end pose', round(x), round(z), round(math.degrees(psi), 1))
