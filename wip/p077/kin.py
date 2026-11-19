# p077 fuel nozzle auto shut-off "HOW DOES THE PUMP / KNOW IT'S FULL?" - timeline + mechanism states + checks.
# Simplified side section (mm, nozzle frame): handle along +x, the spout bends down to a vertical tip at x = TIPX; y up; z toward the camera.
# Principle (Wikipedia Gasoline pump; HowStuffWorks; VST hose note): fuel flowing through a Venturi throat in the handle sucks air in through a small
# sensing hole near the spout tip (via a thin tube and a diaphragm chamber). When fuel covers the hole, air can no longer get in, the vacuum in the
# chamber rises, the diaphragm moves and releases a latch; the lever's pivot (plunger) drops and the main valve spring closes the valve.
import json, math
# ---------- geometry (nozzle frame) ----------
TIPX, TIPY = -85.0, -80.0           # spout tip, WORLD coords (opening points straight down); the handle group is tilted 31 deg
HOLE_Y = TIPY + 7.0                  # sensing hole centre (on the spout's left side, 7 mm above the tip)
HOLE_R = 1.6
PIPE_R, SPOUT_R = 17.0, 10.0         # car filler pipe inner radius, spout outer radius (concentric)
VALVE_X = 80.0; STEM_LIFT = 7.0      # main poppet valve; lift when fully open
PIVOT_X = 2.0; LEVER_Y = -7.0        # lever pivot on the plunger; lever lies along +x
HAND_X = 110.0                       # where the hand squeezes
PLUNGER_DROP = 9.0                   # pivot drop when the latch lets go; the bar then pivots on the closed stem and the lever goes slack under the hand
HAND_LIFT = STEM_LIFT * (HAND_X - PIVOT_X) / (VALVE_X - PIVOT_X)
DIA_LIFT = 3.0                       # diaphragm centre lift when tripped
FPS = 60
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
GAP = [0, 0.1, 0.35, 0.35, 0.35, 0.35, 0.6]
T = {'vo0': 0.15}; T['hookEnd'] = round(T['vo0'] + D[0] + 0.25, 3); T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + D[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + D[6] + 1.3, 1); T['LOOP'] = LOOP
T['click0'] = 1.0                                   # hook: squeezed with a full tank -> trips at once
T['sq1'] = T['vo1'] + 0.15; T['cover1'] = T['vo1'] + 1.55; T['click1'] = T['vo1'] + 1.9    # "Then, click!"
T['sq2'] = T['vo1'] + D[1] + 0.05                   # re-squeeze for the explanation (level back low: a new fill, after a flash)
T['cover2'] = T['vo4'] + 1.4                        # fuel reaches the hole ("fuel covers the hole")
T['trip2'] = T['vo5'] + 1.6                         # diaphragm pulled far enough -> latch lets go ("it trips a latch")
T['click2'] = T['trip2'] + 0.12
T['sq3'] = LOOP - 0.3                              # end: squeeze again with the tank full -> hook repeats
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
LV_LOW, LV_HOLE = TIPY - 40.0, HOLE_Y + HOLE_R + 1.5   # fuel level: well below the tip / just covering the hole
def level(t):
    if t < T['hookEnd']: return LV_HOLE
    if t < T['sq2'] - 0.05: return TIPY - 14 + (LV_HOLE - (TIPY - 14)) * smooth((t - T['vo1'] - 0.2) / (T['cover1'] - T['vo1'] - 0.2))
    if t < T['vo4']: return LV_LOW + 8 * smooth((t - T['sq2']) / (T['vo4'] - T['sq2']))
    return LV_LOW + 8 + (LV_HOLE - LV_LOW - 8) * smooth((t - T['vo4'] - 0.1) / (T['cover2'] - T['vo4'] - 0.1))
def squeezed(t):  # hand holds the lever squeezed (0..1)
    s = 0.0
    if t < T['hookEnd']: s = 1.0
    if t >= T['sq1'] - 0.2: s = smooth((t - T['sq1'] + 0.2) / 0.2)
    if T['sq2'] - 0.45 <= t < T['sq2'] - 0.05: s = 1 - smooth((t - T['sq2'] + 0.45) / 0.15)   # quick release + re-squeeze resets the latch
    if T['sq2'] - 0.05 <= t: s = smooth((t - T['sq2'] + 0.05) / 0.2)
    if t >= T['vo6'] + 1.0: s = 1 - smooth((t - T['vo6'] - 1.0) / 0.2) * (1 - smooth((t - T['sq3'] + 0.25) / 0.25))
    return s
rows = []; latched = True; dia = 0.0; vac = 0.0; T['clicks'] = []
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; lv = level(t); sq = squeezed(t)
    if sq < 0.05: latched = True                                  # releasing the lever resets the latch (plunger springs back up)
    covered = lv >= HOLE_Y + HOLE_R
    valve_open = latched and sq > 0.9
    flow = 1.0 if valve_open else 0.0
    # diaphragm pull (0..1) by episode, only while fuel flows with the hole covered (otherwise it relaxes): the latch lets go at 1
    if not (valve_open and covered): dia = max(0.0, dia - 3.0 / FPS)
    elif t < T['hookEnd']: dia = smooth((t + 0.3) / 0.95)
    elif t < T['sq2'] - 0.5: dia = smooth((t - T['cover1']) / 0.35)
    elif t < T['sq3'] - 0.1: dia = smooth((t - T['vo5'] - 0.2) / (T['trip2'] - T['vo5'] - 0.2))
    else: dia = smooth((t - T['sq3']) / 0.95)
    vac = dia
    if latched and dia >= 0.98 and t > 0.3: latched = False; T['clicks'].append(round(t, 3))
    # lever/stem/plunger: latched -> pivot fixed, stem lift follows the squeeze; unlatched -> stem closed by its spring, pivot drops
    if latched: stem = STEM_LIFT * sq; drop = 0.0
    else: stem = 0.0; drop = PLUNGER_DROP * sq
    air = flow * (0.0 if covered else 1.0)
    rows.append([round(t, 4), round(lv, 3), round(sq, 4), round(stem, 4), round(drop, 4), round(dia, 4), round(flow, 3), round(air, 3), int(latched)])
# smooth the 0/1 flow + air for the particles (0.15 s ramps) -> extra columns 9, 10
for j, c in [(6, 9), (7, 10)]:
    v = 0.0
    for r in rows: v += (r[j] - v) * min(1, 1 / (0.12 * FPS)); r.append(round(v, 4))
# ---------- checks ----------
# 1. lever is one rigid straight bar through (PIVOT, -drop) and (VALVE, stem): latched -> pivot fixed; unlatched -> stem closed, pivot dropped
for r in rows:
    stem, drop = r[3], r[4]
    if r[8]: assert drop == 0 and abs(stem - STEM_LIFT * r[2]) < 1e-3
    else: assert stem == 0 and drop <= PLUNGER_DROP + 1e-9
    hand = -drop + (stem + drop) * (HAND_X - PIVOT_X) / (VALVE_X - PIVOT_X)
    assert hand <= HAND_LIFT + 1e-6
# 2. valve never open while unlatched; air never flows while the hole is covered
assert all(not (r[8] == 0 and r[3] > 0) for r in rows)
assert all(not (r[1] >= HOLE_Y + HOLE_R and r[7] > 0) for r in rows)
# 3. spout inside the filler pipe with clearance (concentric): radial gap
assert PIPE_R - SPOUT_R >= 5.0
# 4. clicks happen at the expected moments (hook, step 0, step 4)
assert len(T['clicks']) == 3 and abs(T['clicks'][2] - T['trip2']) < 0.15, T['clicks']
# snap: ease stem + pivot over ~3 frames at 60 fps (the valve snaps shut / the plunger drops quickly, not in one frame)
for j in (3, 4):
    v = rows[0][j]
    for r in rows: v += (r[j] - v) * 0.45; r[j] = round(v, 4)
G = dict(HAND_LIFT=HAND_LIFT, LOOP=LOOP, T=T, FPS_K=FPS, TIPX=TIPX, TIPY=TIPY, HOLE_Y=HOLE_Y, HOLE_R=HOLE_R, PIPE_R=PIPE_R, SPOUT_R=SPOUT_R, VALVE_X=VALVE_X, STEM_LIFT=STEM_LIFT,
         PIVOT_X=PIVOT_X, LEVER_Y=LEVER_Y, HAND_X=HAND_X, PLUNGER_DROP=PLUNGER_DROP, DIA_LIFT=DIA_LIFT, LV_HOLE=LV_HOLE)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('PASS', T, 'loop', LOOP)
