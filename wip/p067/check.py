# p067 mechanism check over the whole loop: bar never overlaps the keeper, gate never passes the stop, lift within the keep staple, loop closes,
# locked pull: the bar front touches the wall (gap < 0.5 mm) and the bar bottom is below the lip top (cannot ride out).
import json
from shapely.geometry import Polygon, box
G = json.load(open('geom.json')); K = json.load(open('kin.json')); KP = Polygon(G['KEEP']); W, H = G['BW'], G['BH']
ov = 0; mx = 0
for t, th, L, z, on in K:
    assert th >= -1e-9, ('gate through the stop', t)
    assert 0 <= L <= 22, ('lift outside the staple', t, L)
    if on: a = box(z - W / 2, L, z + W / 2, L + H).intersection(KP).area; mx = max(mx, a)
assert mx < 1e-3, ('overlap', mx)
i = int(round(19.0 * G['FPS_K'])); t, th, L, z, on = K[i]; gap = 18.0 - (z + W / 2); assert 0 <= gap < 0.5 and L < 11, ('lock', gap, L)
assert abs(K[0][1] - K[-1][1]) < 1e-6 and abs(K[0][2] - K[-1][2]) < 1e-6, 'loop'
print('check PASS: max overlap %.5f mm2, locked gap %.2f mm, bar bottom %.1f mm below the lip top' % (mx, gap, 14 - L))
