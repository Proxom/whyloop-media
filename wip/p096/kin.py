# p096 plane window breather hole - timing + HARD GATE 5.2 checks (static assembly; the only motion is air/moisture particles + camera + clip plane).
# Units mm. Window axis = z (cabin +z, outside -z). Section plane x = 0 (side view camera at +x).
import json, math
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0}
GAP = {1: 0.3, 2: 0.3, 3: 0.32, 4: 0.34, 5: 0.3, 6: 0.3}
for i in range(1, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.4, 2); T['LOOP'] = LOOP
T['orbA'] = T['vo1'] - 0.05; T['orbB'] = T['vo1'] + 1.9          # front -> side orbit + cut
T['fill'] = T['vo3'] + 0.3                                         # air starts through the hole
T['bal'] = T['vo4']; T['load'] = T['vo4'] + 3.0; T['backup'] = T['vo4'] + 5.0
T['wet'] = T['vo5']; T['back'] = T['vo6'] + 0.05; T['backB'] = T['vo6'] + 1.3
# geometry (z ranges of the parts must not overlap; the hole must be inside the middle pane)
G = dict(W=240, H=340, R=100, OUT=[-110, -98], MID=[-55, -47], INN=[0, 4], SKIN=[-126, -112], PANEL=[4, 30], HOLE_Y=-140, HOLE_R=7)
parts = sorted([('skin', G['SKIN']), ('outer', G['OUT']), ('middle', G['MID']), ('inner', G['INN']), ('panel', G['PANEL'])], key=lambda p: p[1][0])
for (a, ra), (b, rb) in zip(parts, parts[1:]): assert ra[1] <= rb[0], f'{a} overlaps {b}'
# hole inside the middle pane outline (rounded rect W x H, corner R): bottom edge at -H/2, hole centre 30 mm above it
assert G['HOLE_Y'] - G['HOLE_R'] > -G['H'] / 2 + 5
# particle paths: from the cabin-side gap (between middle and inner) through the hole into the outer gap; they may cross z in MID only within the hole
import random; random.seed(96)
P = []
for i in range(40):
    ty = random.uniform(-150, 150); tz = random.uniform(G['OUT'][1] + 6, G['MID'][0] - 6)
    P.append(dict(t0=T['fill'] + i * 0.07, start=[G['HOLE_Y'] + random.uniform(-40, 60), -20.0], hole=[G['HOLE_Y'], -51.0], end=[ty, tz]))
HF, HB = G['MID'][1] + 3, G['MID'][0] - 3   # straight through the hole: z from -44 to -58 at y = HOLE_Y
def at(p, u):  # 3 segments: start -> front of hole (u<0.3) -> back of hole (u<0.45) -> end
    if u < 0.3: v = u / 0.3; a, b = p['start'], [G['HOLE_Y'], HF]
    elif u < 0.45: v = (u - 0.3) / 0.15; a, b = [G['HOLE_Y'], HF], [G['HOLE_Y'], HB]
    else: v = (u - 0.45) / 0.55; a, b = [G['HOLE_Y'], HB], p['end']
    return [a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v]
for p in P:
    for k in range(401):
        y, z = at(p, k / 400)
        if G['MID'][0] - 1 <= z <= G['MID'][1] + 1: assert abs(y - G['HOLE_Y']) <= G['HOLE_R'] - 2, 'particle passes through the middle pane outside the hole'
        assert not (G['OUT'][0] <= z <= G['OUT'][1]) and not (G['INN'][0] <= z <= G['INN'][1]), 'particle passes through a pane'
# moisture droplets: start on the inner face of the outer pane, go down the gap to the hole, out to the cabin gap
M = []
for i in range(18):
    y0 = random.uniform(-120, 140)
    M.append(dict(t0=T['wet'] + 0.4 + i * 0.11, start=[y0, G['OUT'][1] + 5], hole=[G['HOLE_Y'], -51.0], end=[G['HOLE_Y'] + random.uniform(-25, 25), -15.0]))
for p in M:
    for k in range(401):
        u = k / 400
        if u < 0.6: v = u / 0.6; a, b = p['start'], [G['HOLE_Y'], G['MID'][0] - 3]
        elif u < 0.75: v = (u - 0.6) / 0.15; a, b = [G['HOLE_Y'], G['MID'][0] - 3], [G['HOLE_Y'], G['MID'][1] + 3]
        else: v = (u - 0.75) / 0.25; a, b = [G['HOLE_Y'], G['MID'][1] + 3], p['end']
        y, z = a[0] + (b[0] - a[0]) * v, a[1] + (b[1] - a[1]) * v
        if G['MID'][0] - 1 <= z <= G['MID'][1] + 1: assert abs(y - G['HOLE_Y']) <= G['HOLE_R'] - 2
        assert not (G['OUT'][0] <= z <= G['OUT'][1]) and not (G['INN'][0] <= z <= G['INN'][1])
json.dump(dict(T=T, LOOP=LOOP, G=G, P=P, M=M), open('geom.json', 'w'), indent=1)
print('kin PASS', T)
