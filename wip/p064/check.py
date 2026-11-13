# HARD GATE 5.2 for p064: over one full 720 deg cycle (1/4 deg steps) check: valve heads never touch the piston crown,
# rod clears the liner bottom, crank web clears the piston skirt, valves are closed (lift 0) during compression and power,
# loop closes on whole cycles, cams turn at exactly half crank speed.
import json, math
import numpy as np
exec(open('kin.py').read().split('# ---- speed schedule ----')[0])
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
LINER_BOT = 60.0; ROD_HALF = 11.0; WEB_R = R + 16.0
mins = dict(valve=1e9, rod=1e9, web=1e9); bad = []
for th in np.radians(np.arange(0, 720, 0.25)):
    crown = piston_pin(th) + PIN_TO_CROWN; skirt = piston_pin(th) - PIN_TO_SKIRT
    for w in ('in', 'ex'):
        gap = (DECK - lift(th, w)) - crown; mins['valve'] = min(mins['valve'], gap)
    cp = np.array([R * math.sin(th), R * math.cos(th)]); pp = np.array([0, piston_pin(th)])
    u = (LINER_BOT - cp[1]) / (pp[1] - cp[1])
    if 0 <= u <= 1: x = cp[0] + u * (pp[0] - cp[0]); mins['rod'] = min(mins['rod'], BORE / 2 - (abs(x) + ROD_HALF))
    mins['web'] = min(mins['web'], skirt - WEB_R)  # web reaches at most WEB_R from the axis (upward when the pin is up)
    ph = th % (4 * math.pi)
    if math.radians(235) < ph < math.radians(480) and (lift(th, 'in') > 0.01 or lift(th, 'ex') > 0.01): bad.append(round(math.degrees(ph), 2))
rc = H + np.gradient(np.gradient(np.concatenate([H[-2:], H, H[:2]]), GAM[1]-GAM[0]), GAM[1]-GAM[0])[2:-2]; print('cam min radius of curvature', round(float(rc.min()), 2)); assert rc.min() > 0
err = max(abs(lift(math.radians(d), 'in') - s_of((cam_rot(math.radians(d), IN_C) + math.pi) % (2 * math.pi) - math.pi)) for d in range(0, 720, 3)); print('lift vs design max err mm', round(err, 3)); assert err < 0.1
print('min gaps mm', {k: round(v, 2) for k, v in mins.items()}, 'valve open during comp/power at', bad[:5])
th = np.array([r[1] for r in K]); clos = (th[-1] - th[0]) / (4 * math.pi)
ok = mins['valve'] > 1.0 and mins['rod'] > 1.0 and mins['web'] > 1.0 and not bad and abs(clos - round(clos)) < 1e-3
print('loop cycles', round(clos, 5), 'PASS' if ok else 'FAIL'); assert ok
