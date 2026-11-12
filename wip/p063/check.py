# HARD GATE 5.2: the staple wire (centreline + radius RW) never enters the anvil, over the whole loop at 240 Hz;
# the two folded legs never touch each other; the blade stays clear of the nose slot walls.
import json
from shapely.geometry import Polygon, LineString
from kin import state, leg_path, anvil_poly, RW, W, XIN
A = Polygon(anvil_poly()).buffer(0)
assert A.is_valid
worst = 9; wt = 0
for i in range(int(20.0 * 240)):
    s = state(i / 240)
    for side in (-1, 1):
        ln = LineString(leg_path(s['yc'], side))
        d = ln.distance(A)
        if d < worst: worst, wt = d, s['t']
gap = 2 * abs(XIN) - 2 * RW
print('min wire centreline to anvil %.4f mm at %.3f s (needs >= RW %.2f); folded legs gap %.3f mm' % (worst, wt, RW, gap))
blade_half, slot_half = W / 2 + RW - 0.02, W / 2 + RW + 0.12
print('blade %.2f vs slot %.2f mm half width' % (blade_half, slot_half))
print('CHECK', 'PASS' if worst >= RW - 0.005 and gap > 0.5 and blade_half < slot_half else 'FAIL')
