# p100 lotion / soap pump kinematics + HARD GATE 5.2 checks. Units mm, y up, pump axis = y (axisymmetric profiles in (r, y)).
# Real design (US 11,267,009 B1, US 10,875,043 B1, US 8,863,989 B2): a piston in a pump chamber, a return spring, an inlet one-way (ball) valve
# between the dip tube and the chamber, and an outlet one-way (ball) valve between the chamber and the nozzle.
# Press: piston down -> chamber pressure shuts the bottom ball, lifts the top ball -> soap goes up the stem and out.
# Release: spring pushes the piston up -> suction: top ball drops shut, bottom ball lifts -> soap is drawn up the dip tube into the chamber.
# rows: [t, p (press mm), lowLift, topLift, flowOut, flowIn]
import json, math
from shapely.geometry import Polygon, Point
vo = json.load(open('vo/vo.json')); D = [d['dur'] for d in vo]
T = {'vo0': 0.15, 'cutIn': 1.6, 'vo1': 1.7}
T['vo2'] = round(T['vo1'] + D[1] + 0.25, 3); T['vo3'] = round(T['vo2'] + D[2] + 0.25, 3); T['vo4'] = round(T['vo3'] + D[3] + 0.25, 3)
T['vo5'] = round(T['vo4'] + D[4] + 0.25, 3); T['vo6'] = round(T['vo5'] + D[5] + 0.3, 3)
T['pressA'] = T['vo2'] + 0.55; T['pressB'] = T['vo2'] + D[2] - 0.2
T['riseA'] = T['vo3'] + 0.45; T['riseB'] = T['vo6'] - 0.35
T['outA'] = T['vo6']                                     # cut to the outside hero (answer card)
LOOP = round(T['vo6'] + D[6] + 1.7, 2); T['LOOP'] = LOOP
H = {'pressA': 0.12, 'pressB': 0.42, 'riseA': 0.86, 'riseB': 1.30}   # hook: real speed press + squirt + release
STROKE = 14.0; LIFT_LO = 2.0; LIFT_TOP = 1.8
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def phase(t):
    return (H, 0.06) if t < T['cutIn'] else (T, 0.25)
def state(t):
    P, ramp = phase(t)
    p = STROKE * (sm((t - P['pressA']) / (P['pressB'] - P['pressA'])) - sm((t - P['riseA']) / (P['riseB'] - P['riseA'])))
    top = LIFT_TOP * (sm((t - P['pressA']) / ramp) - sm((t - P['pressB']) / ramp))
    low = LIFT_LO * (sm((t - P['riseA']) / ramp) - sm((t - P['riseB']) / ramp))
    fo = 1.0 if P['pressA'] < t < P['pressB'] else 0.0; fi = 1.0 if P['riseA'] < t < P['riseB'] else 0.0
    return p, low, top, fo, fi
# ---- geometry (r, y) ----
G = dict(CH_R=7.5, CH_RO=9.0, CH_TOP=4.0, CONE_Y0=-56.0, SEAT_Y=-62.0, SEAT_R=2.2, BALL_LO=3.2, LEDGE=(-53.5, -52.0), LEDGE_RI=2.5,
         PIST_H=6.0, PIST_Y0=-8.0, POCKET_RI=3.4, POCKET_RO=4.4, POCKET_H=7.0, TOP_SEAT_R=1.6, BALL_TOP=2.6, STEM_RO=3.0, STEM_RI=2.0,
         HEAD_Y0=32.0, HEAD_H=18.0, COLLAR_TOP=16.0, COLLAR_HOLE=3.3, TUBE_RO=2.6, TUBE_RI=1.8, TUBE_Y1=-146.0, NOZ_Y=11.0, NOZ_X1=44.0)
G['LO_Y0'] = G['SEAT_Y'] + math.sqrt(G['BALL_LO'] ** 2 - G['SEAT_R'] ** 2)                       # seated centre of the bottom ball
G['TOP_DY0'] = G['PIST_H'] + math.sqrt(G['BALL_TOP'] ** 2 - G['TOP_SEAT_R'] ** 2)                # seated centre above the piston bottom
# chamber solid wall (right half profile), seat cone, ledge, pocket walls
WALL = Polygon([(G['CH_R'], G['CH_TOP']), (G['CH_RO'], G['CH_TOP']), (G['CH_RO'], G['CONE_Y0']), (4.0, G['SEAT_Y'] - 2.0), (4.0, -70), (G['SEAT_R'], -70),
                (G['SEAT_R'], G['SEAT_Y']), (G['CH_R'], G['CONE_Y0'])])
LEDGE = Polygon([(G['LEDGE_RI'], G['LEDGE'][0]), (G['CH_R'], G['LEDGE'][0]), (G['CH_R'], G['LEDGE'][1]), (G['LEDGE_RI'], G['LEDGE'][1])])
def pocket(pb):   # pocket wall + seat lip + top stop (right half) for piston bottom at pb
    y0 = pb + G['PIST_H']
    return Polygon([(G['TOP_SEAT_R'], y0), (G['POCKET_RI'], y0), (G['POCKET_RI'], y0 + G['POCKET_H']), (G['STEM_RI'], y0 + G['POCKET_H']), (G['STEM_RI'], y0 + G['POCKET_H'] + 1.5),
                    (G['POCKET_RO'], y0 + G['POCKET_H'] + 1.5), (G['POCKET_RO'], y0 - G['PIST_H']), (G['TOP_SEAT_R'], y0 - G['PIST_H'])])
SPR_SOLID = 8 * 2 * 0.7 + 2.8
FPS_K = 120; rows = []; bad = []; mins = dict(lo=1e9, lo_ledge=1e9, top=1e9, head=1e9, spring=1e9)
for i in range(int(LOOP * FPS_K) + 1):
    t = i / FPS_K; p, low, top, fo, fi = state(t)
    pb = G['PIST_Y0'] - p
    bl = Point(0, G['LO_Y0'] + low).buffer(G['BALL_LO'], 64); d1 = bl.distance(WALL) if low > 1e-6 else 0.0; d2 = bl.distance(LEDGE)
    if low > 0.05 and bl.intersection(WALL).area > 1e-4: bad.append(('low-ball-in-wall', round(t, 3)))
    if bl.intersection(WALL).area > 0.02: bad.append(('low-ball-overlap', round(t, 3), bl.intersection(WALL).area))
    if d2 <= 0.05: bad.append(('low-ball-ledge', round(t, 3), d2))
    bt = Point(0, pb + G['TOP_DY0'] + top).buffer(G['BALL_TOP'], 64); a3 = bt.intersection(pocket(pb)).area
    if a3 > 0.02: bad.append(('top-ball-overlap', round(t, 3), a3))
    head = G['HEAD_Y0'] - p - G['COLLAR_TOP']; spr = pb - G['LEDGE'][1]
    if head < 0.5: bad.append(('head-collar', t, head))
    if spr < SPR_SOLID + 2: bad.append(('spring-solid', t, spr))
    if pb < G['LEDGE'][1] + SPR_SOLID: bad.append(('piston-low', t))
    mins['lo_ledge'] = min(mins['lo_ledge'], d2); mins['head'] = min(mins['head'], head); mins['spring'] = min(mins['spring'], spr)
    rows.append([round(t, 4), round(p, 4), round(low, 4), round(top, 4), fo, fi])
# cause checks: top ball open only while pressing (or closing right after); bottom ball open only while rising; never both open
for r0, r1 in zip(rows, rows[1:]):
    dp = r1[1] - r0[1]; t = r1[0]
    if r1[2] > 0.05 and r1[3] > 0.05: bad.append(('both-open', t))
    if r1[3] > 0.05 and dp < -1e-6: bad.append(('top-open-while-rising', t))
    if r1[2] > 0.05 and dp > 1e-6: bad.append(('low-open-while-pressing', t))
    if r1[5] and not dp < 1e-6: bad.append(('flow-in-without-rise', t))
    if r1[4] and not dp > -1e-6: bad.append(('flow-out-without-press', t))
assert rows[0][1] == 0 and abs(rows[-1][1]) < 1e-6 and rows[-1][2] < 1e-6 and rows[-1][3] < 1e-6, 'loop ends must match'
G.update(T=T, LOOP=LOOP, FPS_K=FPS_K, H=H, STROKE=STROKE)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()}); print('mins', {k: round(v, 2) for k, v in mins.items()})
print('PASS' if not bad else 'FAIL', bad[:8])
