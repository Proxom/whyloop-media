# HARD GATE 5.2 (p055): over the whole loop (240 Hz) the bolt never overlaps the jamb/strike, the door slab never overlaps the stop or jamb,
# the bolt only moves with a cause (strike contact pushes it in, spring/handle move it), the door never passes the stop, loop closure.
import json, math, kin
from shapely.geometry import box
fr = json.load(open('kin_240.json'))
slab = box(-320, 0, 0, kin.T)
maxB = maxD = 0; bad_cause = 0; minspring = 1e9
for i, f in enumerate(fr):
    th = f['th']; b = kin.to_world(kin.bolt_local(f['e']), th)
    maxB = max(maxB, b.intersection(kin.FIXED).area)
    maxD = max(maxD, kin.to_world(slab, th).intersection(kin.unary_union([kin.FIXED, kin.stop])).area)
    minspring = min(minspring, f['e'] - kin.BL + 50)
    if i:
        p = fr[i - 1]; de = f['e'] - p['e']
        # bolt going in without the handle must be because it touches the strike (would overlap if it stayed out)
        if de < -1e-6 and f['phi'] <= p['phi'] + 1e-9 and not kin.to_world(kin.bolt_local(p['e']), th).intersects(kin.FIXED): bad_cause += 1
print(json.dumps({'samples': len(fr), 'boltOverlapMm2': round(maxB, 6), 'doorOverlapMm2': round(maxD, 6), 'boltInWithoutCause': bad_cause,
  'minSpringLenMm': round(minspring, 2), 'dMin': min(f['d'] for f in fr), 'dMax': max(f['d'] for f in fr),
  'loop': [fr[0], fr[-1]]}))
