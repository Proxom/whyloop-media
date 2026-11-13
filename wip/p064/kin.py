# p064 four-stroke engine (17:00 1M+ #4). mm, s. Front view: x right, y up, z toward the camera; crank axis = z at the origin.
# theta = crank angle from TDC (cycle angle phi = theta mod 4pi: 0-pi intake, pi-2pi compression, 2pi-3pi power, 3pi-4pi exhaust).
# Crank pin = (r sin th, r cos th) (crank rotation.z = -th). Slider-crank: pin y = r cos th + sqrt(l^2 - r^2 sin^2 th).
# DOHC: two camshafts (axes along z) above the valves turn at HALF crank speed (rotation.z = -(th - thc)/2), lobe points down at thc.
# Valve lift is NOT scripted: it is the flat-tappet displacement computed from the cam profile (support function), so the cam drives it.
import json, math
import numpy as np
FPS = 240; LOOP = 44.0
R, L, BORE = 43.0, 145.0, 86.0
PIN_TO_CROWN, PIN_TO_SKIRT = 30.0, 32.0
DECK = 232.0                         # head face (valves seat flush here); TDC crown = 218 -> 14 mm clearance
VX = 22.0; VHEAD_R = 15.0            # valve x (intake -VX, exhaust +VX), valve head radius
STEM = 92.0                          # valve head bottom -> tappet top
RB = 25.0; LMAX = 7.0                # cam base radius, max lift
CAM_Y = DECK + STEM + RB             # cam axis height (tappet top touches the base circle when closed)
IN_C, EX_C = math.radians(100), math.radians(615)     # lobe centres (crank deg); duration 260 crank deg each
H0 = math.radians(65)                                  # half duration in CAM angle (= 130 crank deg)
SPARK = 2 * math.pi - math.radians(8)
def sm(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
# ---- cam profile from the desired flat-tappet lift s(gamma) (support function h = RB + s): p = h n + h' t ----
def s_of(g): u = min(1.0, abs(g) / H0); return LMAX * (0.5 + 0.5 * math.cos(math.pi * u))
NB = 720; GAM = np.linspace(-math.pi, math.pi, NB, endpoint=False)
H = np.array([RB + s_of(g) for g in GAM]); dH = np.gradient(np.concatenate([H[-2:], H, H[:2]]), GAM[1] - GAM[0])[2:-2]
# local frame: gamma = 0 means the lobe nose points along local -y; n = (sin g, -cos g), t = dn/dg = (cos g, sin g)
PX = H * np.sin(GAM) + dH * np.cos(GAM); PY = -H * np.cos(GAM) + dH * np.sin(GAM)
def cam_rot(th, thc): return -(th - thc) / 2.0
def lift(th, which):  # tappet displacement = support of the DRAWN profile toward -y after rotating the cam by g, minus RB
    thc = IN_C if which == 'in' else EX_C; g = cam_rot(th, thc); c, s = math.cos(g), math.sin(g)
    yw = PX * s + PY * c
    return float(max(0.0, -yw.min() - RB))
def piston_pin(th): return R * math.cos(th) + math.sqrt(L * L - (R * math.sin(th)) ** 2)
# ---- speed schedule ----
TS = 12.0                      # step 1 (intake) starts here: theta = 0 (TDC)
WS = 2 * math.pi * 0.085       # slow inside speed: 4 strokes in ~23.5 s
def wshape(t, wf):
    if t < 6.0: return wf
    if t < 8.0: return wf + (WS - wf) * sm((t - 6.0) / 2.0)
    if t < 38.3: return WS
    if t < 39.8: return WS + (2.2 * wf - WS) * sm((t - 38.3) / 1.5)
    if t < 41.8: return 2.2 * wf
    if t < 43.6: return 2.2 * wf + (wf - 2.2 * wf) * sm((t - 41.8) / 1.8)
    return wf
def slowmo(th):  # power-stroke slow motion around the spark: 0.4x from 2pi-0.35 to 2pi+0.9
    a, b = 2 * math.pi - 0.3, 2 * math.pi + 0.7
    if th < a - 0.25 or th > b + 0.3: return 1.0
    if th < a: return 1 - 0.55 * sm((th - (a - 0.25)) / 0.25)
    if th < b: return 0.45
    return 0.45 + 0.55 * sm((th - b) / 0.3)
def integrate(wf):
    N = int(LOOP * FPS) + 1; th = np.zeros(N); w = np.zeros(N); x = 0.0
    # pass 1: theta relative to TS
    ts = np.arange(N) / FPS; raw = np.zeros(N)
    for i in range(1, N):
        t = ts[i - 1]; raw[i] = raw[i - 1] + wshape(t, wf) * slowmo(raw[i - 1] - raw[int(TS * FPS)] if i > TS * FPS else -9) / FPS
    return ts, raw - raw[int(TS * FPS)]
def total(wf): ts, th = integrate(wf); return th[-1] - th[0]
# choose the fast speed so the loop closes on a whole number of cycles (4pi) near 1.1 rev/s
target_wf = 2 * math.pi * 1.1
lo, hi = 2 * math.pi * 0.6, 2 * math.pi * 1.6
tot = total(target_wf); ncyc = round(tot / (4 * math.pi)); goal = ncyc * 4 * math.pi
for _ in range(40):
    mid = (lo + hi) / 2
    if total(mid) < goal: lo = mid
    else: hi = mid
WF = (lo + hi) / 2; ts, TH = integrate(WF)
print('WF rev/s', round(WF / 2 / math.pi, 3), 'cycles/loop', ncyc, 'closure err deg', round(math.degrees(TH[-1] - TH[0] - goal), 3))
# events (times when theta crosses stroke boundaries in the slow cycle)
def t_at(v): i = int(np.searchsorted(TH, v)); return round(float(ts[i]), 3)
EV = {'intake': t_at(0.0), 'comp': t_at(math.pi), 'spark': t_at(SPARK), 'power': t_at(2 * math.pi), 'exhaust': t_at(3 * math.pi), 'end': t_at(4 * math.pi)}
print('events', EV)
rows = []
for i in range(0, len(ts)):
    th = float(TH[i]); rows.append([round(float(ts[i]), 5), th, lift(th, 'in'), lift(th, 'ex')])
json.dump(rows, open('kin_240.json', 'w'))
json.dump(dict(LOOP=LOOP, FPS=FPS, R=R, L=L, BORE=BORE, PIN_TO_CROWN=PIN_TO_CROWN, PIN_TO_SKIRT=PIN_TO_SKIRT, DECK=DECK, VX=VX, VHEAD_R=VHEAD_R, STEM=STEM, RB=RB, LMAX=LMAX, CAM_Y=CAM_Y,
               IN_C=IN_C, EX_C=EX_C, H0=H0, SPARK=SPARK, EV=EV, CAMPX=[round(float(v), 3) for v in PX[::2]], CAMPY=[round(float(v), 3) for v in PY[::2]], cols=['t', 'th', 'lin', 'lex']), open('geom.json', 'w'), indent=0)
