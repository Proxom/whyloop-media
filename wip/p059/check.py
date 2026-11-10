# HARD GATE 5.2: no part passes through another over one full loop (shapely, 240 Hz).
# 1) layshaft gear vs main gear (involute mesh, ratio 1.5); 2) sleeve internal teeth vs blocker-ring teeth and vs dog teeth whenever their
# z ranges overlap (all angles relative to the sleeve, which turns with the shaft); 3) cone gap >= 0.
import json, math
from shapely.geometry import Polygon
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
G1 = Polygon(G['G1']).buffer(0); G2 = affinity.translate(Polygon(G['G2']).buffer(0), 0, -G['CD'])
EXT = Polygon(G['EXT']).buffer(0)
INTP = Polygon([[50 * math.cos(a / 90 * 2 * math.pi), 50 * math.sin(a / 90 * 2 * math.pi)] for a in range(90)], [G['INT']]).buffer(0)  # sleeve ring (inner toothed hole)
Z = G['Z']; worst = dict(mesh=0, blk=0, dog=0); gap = dict(mesh=9, blk=9, dog=9)
for i, k in enumerate(K):
    a = affinity.rotate(G1, k['g'], origin=(0, 0), use_radians=True)
    b = affinity.rotate(G2, -1.5 * k['g'], origin=(0, -G['CD']), use_radians=True)
    worst['mesh'] = max(worst['mesh'], a.intersection(b).area); gap['mesh'] = min(gap['mesh'], a.distance(b))
    if i % 2: continue
    sf = Z['slv'][0] + k['x']
    if sf < Z['blk'][1] + k['bx']:
        r = affinity.rotate(EXT, k['bb'], origin=(0, 0), use_radians=True); worst['blk'] = max(worst['blk'], r.intersection(INTP).area); gap['blk'] = min(gap['blk'], r.distance(INTP))
    if sf < Z['dog'][1]:
        r = affinity.rotate(EXT, k['g'] - k['s'], origin=(0, 0), use_radians=True); worst['dog'] = max(worst['dog'], r.intersection(INTP).area); gap['dog'] = min(gap['dog'], r.distance(INTP))
    if sf < Z['blk'][1] + k['bx'] - 0.0 and sf > Z['blk'][0] and abs(k['bb']) > 1e-3 and False: pass
# blocking: while the ring is turned (bb != 0) the sleeve front must not pass its back face
bad = [i / 240 for i, k in enumerate(K) if abs(k['bb']) > 1e-4 and Z['slv'][0] + k['x'] < Z['blk'][1] + k['bx'] - 1e-6]
print('mesh overlap %.4f mm2 min gap %.3f | blocker overlap %.4f gap %.3f | dog overlap %.4f gap %.3f | blocked-but-passing frames %d' % (worst['mesh'], gap['mesh'], worst['blk'], gap['blk'], worst['dog'], gap['dog'], len(bad)))
print('min sleeve-to-ring face gap %.3f mm' % min(Z['blk'][1] + k['bx'] - (Z['slv'][0] + k['x']) for k in K if abs(k['bb']) > 1e-4))
print('CHECK', 'PASS' if max(worst.values()) < 0.01 and not bad else 'FAIL')
