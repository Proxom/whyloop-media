import os, json, math
import kin
from shapely.geometry import Point
fr, ev, _ = kin.simulate(240)
lk = [e for e in ev if e['type'] == 'lock'][0]; f = fr[int(lk['t'] * 240) + 2]
arm = kin.pend_at(f['phi']); d = arm.distance(Point(0, 0))
print('PH', os.environ.get('PH'), 'lock t', round(lk['t'], 3), 'payout deg', round(-lk['ag'] / kin.D, 2), 'phi at lock', round(f['phi'] / kin.D, 2), 'catch min radius', round(d, 3), 'depth below tips', round(kin.RO - d, 3))
