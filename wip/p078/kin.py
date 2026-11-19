# p078 bike floor pump "HOW DOES AIR GO / ONLY ONE WAY?" - timeline, piston stroke, cup-lip state, tire valve, checks.
# Section through the barrel axis, mm: y up (barrel bottom y = 0, top y = BAR_H), x to the right, z toward the camera.
# Principle (Wikipedia Bicycle pump): the piston carries a cup-shaped seal opening downward. On the down (forward) stroke the air
# below pushes the cup's sides against the cylinder wall -> it seals and the air is pushed out to the tire through the tire valve,
# which the pressure forces open. On the up-stroke the lip is not pressed, outside air slips past it into the barrel, and the
# tire valve shuts so the tire air cannot come back.
import json, math
BAR_RI, BAR_H = 16.0, 320.0
Y_TOP, Y_BOT = 270.0, 40.0          # piston (cup lip) travel
LIP_SEAL, LIP_BENT = BAR_RI, BAR_RI - 2.2   # lip outer radius: pressed on the wall / bent inward (drawn a little exaggerated)
VLIFT = 1.6                          # tire valve core lift when air flows in
FPS = 60
VO = json.load(open('vo/vo.json')); D = [v['dur'] for v in VO]
GAP = [0, 0.1, 0.35, 0.35, 0.35, 0.35, 0.6]
T = {'vo0': 0.15}; T['hookEnd'] = round(T['vo0'] + D[0] + 0.2, 3); T['vo1'] = T['hookEnd'] + 0.1
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + D[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + D[6] + 1.3, 1); T['LOOP'] = LOOP
def smooth(u): u = max(0.0, min(1.0, u)); return u * u * (3 - 2 * u)
MID = (Y_TOP + Y_BOT) / 2
# piston height keyframes (t, y); between keys: smoothstep
KEYS = [(0.0, MID + 30), (T['hookEnd'] - 0.2, Y_BOT + 10),            # hook: a push in progress (cup sealing, air into the tire)
        (T['hookEnd'], Y_TOP), (T['vo1'] + 0.25, Y_TOP), (T['vo1'] + 1.25, Y_BOT), (T['vo1'] + 1.55, Y_BOT), (T['vo1'] + 2.6, Y_TOP),   # push, pull
        (T['vo2'] + 0.2, Y_TOP - 20), (T['vo3'] - 0.1, Y_TOP - 110),   # step 1: settle low-mid, shows the cup
        (T['vo3'] + 0.3, Y_TOP - 110), (T['vo4'] - 0.15, Y_TOP),        # step 2: slow pull up (air slips in)
        (T['vo4'] + 0.3, Y_TOP), (T['vo5'] - 0.2, Y_BOT + 30),          # step 3: slow push down (seals, air out)
        (T['vo5'] + 0.2, Y_BOT + 30), (T['vo5'] + 1.6, Y_TOP - 60),     # step 4: pull again: tire valve shuts
        (T['vo6'] + 0.2, Y_TOP - 60), (T['vo6'] + 1.1, Y_BOT + 10), (T['vo6'] + 1.4, Y_BOT + 10), (T['vo6'] + 2.4, Y_TOP),
        (LOOP - 0.45, Y_TOP), (LOOP, MID + 30)]
KEYS[-1] = (LOOP, MID + 30)
def piston(t):
    for (t0, y0), (t1, y1) in zip(KEYS, KEYS[1:]):
        if t0 <= t <= t1: return y0 + (y1 - y0) * smooth((t - t0) / max(1e-6, t1 - t0))
    return KEYS[-1][1]
# hook to loop seam: the hook starts mid-push; the end must arrive mid-push with the same downward motion -> last segment goes Y_TOP -> MID+30 (down)
rows = []; prev = piston(0) + 1e-3; lip = 0.0; valve = 0.0
for i in range(int(LOOP * FPS) + 1):
    t = i / FPS; y = piston(t); v = (y - prev) * FPS; prev = y
    down = max(0.0, -v); up = max(0.0, v)
    # lip bend 0 (sealed) .. 1 (bent in) follows the up-stroke speed; sealed (0) whenever the piston moves down or stands
    target = min(1.0, up / 60.0)
    lip += (target - lip) * min(1.0, 14.0 / FPS)
    valve_t = min(1.0, down / 60.0)
    valve += (valve_t - valve) * min(1.0, 20.0 / FPS)
    rows.append([round(t, 4), round(y, 3), round(v, 2), round(lip, 4), round(valve, 4), round(min(1, down / 80), 3), round(min(1, up / 80), 3)])
# ---------- checks ----------
assert all(Y_BOT - 1e-6 <= r[1] <= Y_TOP + 1e-6 for r in rows), 'piston leaves the barrel travel'
R_LIP = [LIP_SEAL - (LIP_SEAL - LIP_BENT) * r[3] for r in rows]
assert all(rl <= BAR_RI + 1e-9 for rl in R_LIP), 'lip enters the wall'
assert all(not (r[2] < -5 and r[3] > 0.2) for r in rows), 'cup open while pushing'
assert all(not (r[2] > 5 and r[4] > 0.3) for r in rows), 'tire valve open while pulling'
assert abs(rows[0][1] - rows[-1][1]) < 0.5, ('loop seam', rows[0][1], rows[-1][1])
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, BAR_RI=BAR_RI, BAR_H=BAR_H, Y_TOP=Y_TOP, Y_BOT=Y_BOT, LIP_SEAL=LIP_SEAL, LIP_BENT=LIP_BENT, VLIFT=VLIFT)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print('PASS', T)
