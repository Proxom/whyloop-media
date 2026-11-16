# p068 mechanism check over the whole loop: rack never overlaps the pinion (rolling contact, pinion turned by -d/RP), teeth stay in mesh
# (contact point y=0 inside the rack's toothed length), rack top clears the spring bracket (y=38), the needle stays on the dial (0..300 deg), loop closes.
import json, math, sys
sys.argv = ['kin']; exec(open('kin.py').read().split('# ---------- load script')[0])
G = json.load(open('geom.json')); KJ = json.load(open('kin.json'))
mx = 0; mn_gap = 9
for t, d, ang, L in KJ[::2]:
    P = affinity.rotate(pin, ang, origin=(0, 0)); R = rack_scene(d)
    mx = max(mx, P.intersection(R).area); mn_gap = min(mn_gap, P.distance(R))
    assert -6 - d < -3 and 30 - d > 3, ('teeth out of mesh', t)
    assert 32 - d < 38 - 1, ('rack hits bracket', t, d)
    assert -2 <= -ang <= 300, ('needle off the dial', t, ang)
assert mx < 1e-4, ('overlap', mx)
assert abs(KJ[0][1] - KJ[-1][1]) < 1e-6, 'loop'
print('check PASS: max overlap %.6f mm2, min rack-pinion gap %.3f mm, d max %.2f mm (needle %.1f deg)' % (mx, mn_gap, max(r[1] for r in KJ), -min(r[2] for r in KJ)))
