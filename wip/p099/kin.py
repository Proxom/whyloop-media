# p099 airplane oxygen mask: why you must PULL it. Kinematics + HARD GATE 5.2 checks. Units mm, s. Side plane (x right, y up), z toward the camera.
# Real system (SKYbrary 'Chemical Oxygen Generators'; FAA AM21-11): the mask hangs on a lanyard tied to a release pin; the pin restrains a spring-loaded
# striker (firing pin). Pulling the mask pulls the pin out, the spring drives the striker into a percussion cap, the cap's heat starts the sodium chlorate
# core, which then makes oxygen for ~12-20 min; the oxygen flows through the tube to the mask's reservoir bag (it may not fully inflate).
# rows: [t, maskDrop, pinDrop, rodShift, front(x of reaction front or -999), flow(0..1), bag(0..1), slow(0/1)]
import json, math
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
T = {'vo0': 0.12, 'cutIn': 2.0, 'vo1': 2.1}
T['vo2'] = round(T['vo1'] + D[1] + 0.3, 3); T['vo3'] = round(T['vo2'] + D[2] + 0.3, 3); T['vo4'] = round(T['vo3'] + D[3] + 0.35, 3)
T['vo5'] = round(T['vo4'] + D[4] + 0.3, 3); T['outA'] = round(T['vo5'] + D[5] + 0.2, 3); T['vo6'] = round(T['outA'] + 0.3, 3)
LOOP = round(T['vo6'] + D[6] + 1.25, 2); T['LOOP'] = LOOP
T['pullA'] = T['vo3'] + 0.45; T['pullB'] = T['pullA'] + 1.6                 # step 3: slow pull (real: one quick tug)
T['fireA'] = T['vo4'] + 0.9; T['fireB'] = T['fireA'] + 0.9                  # step 4: striker in slow motion (real: a few ms)
T['coreA'] = T['fireB'] + 0.25                                              # reaction front starts at the cap end
T['flowA'] = T['vo5'] + 0.2                                                 # oxygen leaves the core (real: a few seconds later; shortened)
H = {'pullA': 0.08, 'pullB': 0.5, 'fireA': 0.42, 'fireB': 0.47, 'flowA': 0.62}
# ---- geometry ----
CY = 60.0                                   # canister axis height
CAN = dict(x0=-130.0, x1=95.0, R=28.0, t=2.0)  # steel canister
INS_R0, INS_R1 = 23.0, 26.0                 # insulation sleeve (inner, outer)
CORE = dict(x0=-118.0, x1=80.0, R=18.0)     # sodium chlorate core
CAP = dict(x0=-128.0, x1=-124.0, R=5.0)     # percussion cap (brass) in the end wall
HOUS = dict(x0=-200.0, x1=-130.0, R=14.0, t=2.0)   # firing head housing
ROD = dict(L=36.0, r=3.5, collarL=7.0, collarR=9.0)  # striker rod (tip at the right) + collar at the back
TIP0 = -150.0                                # cocked tip x
TRAVEL = CAP['x0'] - TIP0                    # tip ends exactly on the cap face (22 mm)
HOLE_X = -160.0; HOLE_R = 2.8                # cross hole in the rod (cocked position)
PIN = dict(r=2.5, L=44.0, top0=CY + 22.0)    # release pin, vertical; top0 = top end y when in
BACKWALL = HOUS['x0'] + HOUS['t']            # spring seat (inner face of the back wall)
MASK_X = -100.0; MASK_TOP0 = -110.0          # cord tie point = top of the mask assembly (flow indicator top)
PIN_BOT0 = PIN['top0'] - PIN['L']            # 38
CORD_L = math.hypot(HOLE_X - MASK_X, PIN_BOT0 - MASK_TOP0) + 14.0  # 14 mm slack
DROP = 66.0                                  # mask pulled down by 66 mm (pin fully out: needs pin top below the housing bottom)
OUT_X = CAN['x1'] + 9.0                      # outlet nipple end
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def pin_drop(md):                            # cord: pin moves only once the cord is taut
    dx = HOLE_X - MASK_X; need = (PIN_BOT0 - (MASK_TOP0 - md))
    taut = math.sqrt(max(0, CORD_L ** 2 - dx ** 2))
    return max(0.0, need - taut)
def fire(u): u = min(1, max(0, u)); return TRAVEL * u * u   # spring accelerates the striker until it hits the cap
def state(t):
    if t < T['cutIn']:
        md = DROP * sm((t - H['pullA']) / (H['pullB'] - H['pullA']))
        rod = fire((t - H['fireA']) / (H['fireB'] - H['fireA']))
        flow = sm((t - H['flowA']) / 0.5); front = -999 if t < H['fireB'] else CORE['x0'] + 6
        return md, rod, front, flow, flow * 0.75, 0
    if t < T['outA']:
        md = DROP * sm((t - T['pullA']) / (T['pullB'] - T['pullA']))
        rod = fire((t - T['fireA']) / (T['fireB'] - T['fireA']))
        front = -999 if t < T['coreA'] else CORE['x0'] + (CORE['x1'] - CORE['x0']) * 0.42 * min(1, (t - T['coreA']) / (T['outA'] - T['coreA'])) ** 0.6
        flow = sm((t - T['flowA']) / 0.8); bag = sm((t - T['flowA'] - 1.6) / 2.0) * 0.75
        slow = 1 if (T['pullA'] - 0.2 < t < T['pullB'] + 0.2) or (T['fireA'] - 0.2 < t < T['fireB'] + 0.4) else 0
        return md, rod, front, flow, bag, slow
    return DROP, TRAVEL, CORE['x0'] + (CORE['x1'] - CORE['x0']) * 0.42, 1.0, 0.75, 0
FPS_K = 120; rows = []; bad = []
prev = None
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; md, rod, front, flow, bag, slow = state(t); pd = pin_drop(md)
    pin_top = PIN['top0'] - pd; rod_bot = CY - ROD['r']
    # 1. striker moves only once the pin has left the rod's cross hole (pin top below the rod bottom, 0.3 mm clearance)
    if rod > 1e-6 and pin_top > rod_bot - 0.3: bad.append(('rod-moves-with-pin-in', round(t, 3), round(pin_top, 2)))
    # 2. pin inside the hole while cocked: pin radius < hole radius (no overlap), pin and hole share x
    assert PIN['r'] < HOLE_R
    # 3. tip never passes the cap face; collar stays inside the housing; spring length positive
    tip = TIP0 + rod
    if tip > CAP['x0'] + 1e-6: bad.append(('tip-through-cap', t, tip))
    collar_back = TIP0 - ROD['L'] + rod
    if collar_back - BACKWALL < 4.0: bad.append(('spring-solid', t))
    if tip > HOUS['x1'] + 6 + 1e-6: bad.append(('tip-out', t))
    # 4. causes: core starts only after the strike; oxygen only after the core runs; bag only after flow
    if front > -999 and rod < TRAVEL - 1e-6: bad.append(('core-before-strike', round(t, 3)))
    if flow > 0 and front == -999: bad.append(('flow-before-core', round(t, 3)))
    if bag > flow + 1e-6: bad.append(('bag-before-flow', round(t, 3)))
    # 5. cord: never longer than CORD_L; pin only moves down; mask never above its start
    dist = math.hypot(HOLE_X - MASK_X, (PIN_BOT0 - pd) - (MASK_TOP0 - md))
    if dist > CORD_L + 1e-6: bad.append(('cord-stretched', t, dist))
    if prev and (pd < prev[1] - 1e-9 and t > T['cutIn'] + 0.01 and abs(t - T['cutIn']) > 0.01): bad.append(('pin-back-up', t))
    prev = (md, pd)
    rows.append([round(t, 4), round(md, 3), round(pd, 3), round(rod, 3), round(front, 2), round(flow, 3), round(bag, 3), slow])
# pin fully clear of the housing bottom at the end of the pull (so it can fall away with the cord)
pd_end = pin_drop(DROP)
if PIN['top0'] - pd_end > CY - HOUS['R'] - 0.5: bad.append(('pin-not-out', round(PIN['top0'] - pd_end, 2)))
# 6. oxygen particle path: inside the gap between core (R 18) and insulation (r 23): path radius 20.5, particle r 1.4
PR, PATH_R = 2.0, 20.5
if not (CORE['R'] + PR < PATH_R < INS_R0 - PR): bad.append(('particle-gap',))
G = dict(T=T, H=H, LOOP=LOOP, FPS_K=FPS_K, CY=CY, CAN=CAN, INS=[INS_R0, INS_R1], CORE=CORE, CAP=CAP, HOUS=HOUS, ROD=ROD, TIP0=TIP0, TRAVEL=TRAVEL,
         HOLE_X=HOLE_X, HOLE_R=HOLE_R, PIN=PIN, MASK_X=MASK_X, MASK_TOP0=MASK_TOP0, PIN_BOT0=PIN_BOT0, CORD_L=CORD_L, DROP=DROP, OUT_X=OUT_X, PR=PR, PATH_R=PATH_R)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()}); print('pin top at end', round(PIN['top0'] - pd_end, 2), 'housing bottom', CY - HOUS['R'], 'pin starts moving at mask drop', round(next(r[1] for r in rows if r[2] > 0), 1))
print('PASS' if not bad else 'FAIL', bad[:8])
