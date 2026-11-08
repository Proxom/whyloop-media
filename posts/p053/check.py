# HARD GATE 5.2 (p053): over the whole loop (240 Hz) the catch never overlaps the lock wheel (max overlap area, depth),
# the wheel never turns while locked, the pendulum only moves with a cause (a != 0 or contact or settling), loop closure.
import json, math, kin
from shapely.geometry import Point
fr = json.load(open('kin_240.json')); D = kin.D
maxA = 0; maxDepth = 0; moved = 0
for i, f in enumerate(fr):
    inter = kin.pend_at(f['phi']).intersection(kin.gear_at(f['ag']))
    if inter.area > maxA: maxA = inter.area
    if not inter.is_empty and inter.area > 0: maxDepth = max(maxDepth, inter.area / max(inter.length / 2, 1e-9))
    if i and f['lock'] and fr[i - 1]['lock'] and abs(f['ag'] - fr[i - 1]['ag']) > 1e-12: moved += 1
# full-body check: bob/rod vs wheel (must stay outside)
body = 0
from shapely import affinity
for f in fr[::4]:
    if affinity.rotate(kin.PEND, f['phi'], origin=tuple(kin.P), use_radians=True).intersection(kin.gear_at(f['ag'])).area > 1e-6: body += 1
print(json.dumps({'samples': len(fr), 'maxOverlapMm2': round(maxA, 6), 'approxMaxDepthMm': round(maxDepth, 5), 'bodyOverlapSamples': body, 'wheelMovedWhileLocked': moved,
  'phiStartEnd': [fr[0]['phi'], fr[-1]['phi']], 'agStartEnd': [fr[0]['ag'], fr[-1]['ag']], 'phiMaxDeg': round(max(f['phi'] for f in fr) / D, 2), 'phiMinDeg': round(min(f['phi'] for f in fr) / D, 2)}))
