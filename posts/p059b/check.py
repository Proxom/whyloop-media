# HARD GATE 5.2 for p059b: no part passes through another over one full loop (shapely, 240 Hz).
# 1) layshaft gear vs main gear mesh; 2) sleeve internal teeth vs brass ring teeth (only while the ring is present) and vs the dog teeth
# whenever their z ranges overlap; 3) in the "no synchro" demo the sleeve front never goes past the dog-teeth end face (z 23);
# 4) the sleeve never passes the ring while the ring is turned (blocking); 5) the loop closes (angles mod 2pi, positions equal).
import json, math
from shapely.geometry import Polygon
from shapely import affinity
G = json.load(open('geom.json')); K = json.load(open('kin_240.json'))
G1 = Polygon(G['G1']).buffer(0); G2 = affinity.translate(Polygon(G['G2']).buffer(0), 0, -G['CD'])
EXT = Polygon(G['EXT']).buffer(0)
INTP = Polygon([[50 * math.cos(a / 90 * 2 * math.pi), 50 * math.sin(a / 90 * 2 * math.pi)] for a in range(90)], [G['INT']]).buffer(0)
Z = G['Z']; worst = dict(mesh=0, blk=0, dog=0); gap = dict(mesh=9, blk=9, dog=9); face = 99
for i, k in enumerate(K):
    a = affinity.rotate(G1, k['g'], origin=(0, 0), use_radians=True)
    b = affinity.rotate(G2, -1.5 * k['g'], origin=(0, -G['CD']), use_radians=True)
    if i % 2 == 0: worst['mesh'] = max(worst['mesh'], a.intersection(b).area); gap['mesh'] = min(gap['mesh'], a.distance(b))
    sf = Z['slv'][0] + k['x']
    if k['rv'] > 0 and sf < Z['blk'][1] + k['bx']:
        r = affinity.rotate(EXT, k['bb'], origin=(0, 0), use_radians=True); worst['blk'] = max(worst['blk'], r.intersection(INTP).area); gap['blk'] = min(gap['blk'], r.distance(INTP))
    if sf < Z['dog'][1]:
        r = affinity.rotate(EXT, k['g'] - k['s'], origin=(0, 0), use_radians=True); worst['dog'] = max(worst['dog'], r.intersection(INTP).area); gap['dog'] = min(gap['dog'], r.distance(INTP))
    if k['rv'] < 1: face = min(face, sf - Z['dog'][1])
bad = [i / 240 for i, k in enumerate(K) if k['rv'] >= 1 and abs(k['bb']) > 1e-4 and Z['slv'][0] + k['x'] < Z['blk'][1] + k['bx'] - 1e-6]
ringgone_inside = [i / 240 for i, k in enumerate(K) if 0 < k['rv'] < 1 and Z['slv'][0] + k['x'] < Z['blk'][1]]  # ring must not fade while the sleeve is inside its space
a, z = K[0], K[-1]; dA = lambda u, v: abs(((u - v + math.pi) % (2 * math.pi)) - math.pi)
step_s, step_g = K[-1]['ws'] / 240, K[-1]['wg'] / 240
loop = max(dA(z['s'] + step_s, a['s']), dA(z['g'] + step_g, a['g']), abs(z['x'] - a['x']), abs(z['bb'] - a['bb']), abs(z['sel'] - a['sel']))
print('mesh overlap %.4f mm2 min gap %.3f | ring overlap %.4f gap %.3f | dog overlap %.4f gap %.3f | min sleeve-to-dog-face gap (no synchro) %.3f mm' % (worst['mesh'], gap['mesh'], worst['blk'], gap['blk'], worst['dog'], gap['dog'], face))
print('blocked-but-passing frames %d | ring fading with sleeve inside %d | loop seam error %.5f' % (len(bad), len(ringgone_inside), loop))
print('CHECK', 'PASS' if max(worst.values()) < 0.01 and not bad and not ringgone_inside and face >= 0 and loop < 1e-3 else 'FAIL')
