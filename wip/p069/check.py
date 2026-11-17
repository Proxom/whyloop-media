# HARD GATE 5.2: no part passes through another. Axisymmetric parts -> check in the (x, r) half plane with shapely for every kin row.
import json, math
from shapely.geometry import Polygon, Point, box
from shapely.affinity import rotate
G = json.load(open('geom.json')); K = json.load(open('kin.json'))
def finger(s):
    # finger as a tilted strip around its mid line x = XF + (r - PIV) s, r in [F_RI, F_RO]
    c = math.sqrt(1 + s * s) * G['FING_T'] / 2; f = lambda r: G['XF'] + (r - G['F_PIV']) * s
    return Polygon([(f(G['F_RI']) - c, G['F_RI']), (f(G['F_RO']) - c, G['F_RO']), (f(G['F_RO']) + c, G['F_RO']), (f(G['F_RI']) + c, G['F_RI'])])
fly = box(-G['FW_T'], 30, 0, G['FW_R']).union(box(-G['FW_T'], 0, -12, 30))          # recess r < 30 down to x = -12
lipP = box(G['LIP'][2], G['LIP'][0], G['LIP'][3], G['LIP'][1])
tori = [Point(G['XF'] + d * G['TORUS_D'], G['F_PIV']).buffer(G['TORUS_TUBE'], 32) for d in (-1, 1)]
shaft = box(-10, 0, 450, G['SHAFT_R']); tube = box(G['TUBE_X0'], G['TUBE_R'][0], 140, G['TUBE_R'][1])
worst = {}; fails = 0
def chk(name, a, b, tol=1e-6):
    global fails
    d = a.distance(b); inter = a.intersection(b).area
    if name not in worst or d < worst[name]: worst[name] = d
    if inter > tol: fails += 1; print('overlap', name, round(inter, 5)); return False
    return True
for r in K:
    t, p, px, dx, s, bx, fk = r[:7]
    disc = box(dx, G['DISC_RI'] - 34, dx + G['DISC_T'], G['DISC_R'])          # facings + core (r 26..112)
    hub = box(dx + G['HUB_X'][0], G['SHAFT_R'], dx + G['HUB_X'][1], G['HUB_R'])
    plate = box(px, G['PLATE_RI'], px + G['PLATE_T'], G['PLATE_RO']).union(Point(px + G['PLATE_T'], G['RIDGE_R']).buffer(G['RIDGE_TUBE'], 48))
    fin = finger(s); bear = box(bx, G['BEAR_R0'], bx + G['BEAR_L'], G['BEAR_R1'])
    chk('disc-flywheel', disc, fly); chk('hub-flywheel', hub, fly); chk('disc-plate', disc, plate); chk('finger-plate', fin, plate)
    chk('finger-bearing', fin, bear); chk('finger-lip', fin, lipP); chk('finger-hub', fin, hub)
    for tt in tori: chk('finger-fulcrum', fin, tt)
    chk('bearing-tube(slides)', bear, box(0, 0, 1, 1)); chk('hub-tube', hub, tube); chk('plate-lip', plate, lipP); chk('fin-tube', fin, tube)
    # contact must exist: finger touches the ridge and the bearing (else the plate/bearing would float)
    if fin.distance(plate) > 0.05 or fin.distance(bear) > 0.05: fails += 1; print('lost contact at', t)
    if p == 0 and abs(px - (dx + G['DISC_T'])) > 0.02: fails += 1; print('not clamped at', t)
print({k: round(v, 3) for k, v in worst.items()})
print('FAIL' if fails else 'PASS', fails)
