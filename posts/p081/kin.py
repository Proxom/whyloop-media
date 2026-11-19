# p081 prism pencil sharpener "HOW DOES IT MAKE / A PERFECT POINT?" - kinematics + HARD GATE 5.2 checks
# mm, pencil axis = y (tip down). Body y -12.5..12.5. Guide bore r 3.75 above y 3.7, shaping cone below (half angle 11 deg) to a 0.6 mm clearance hole.
# The blade face is the plane tangent to the cone along the +x generator; its edge lies on that generator (enters the cone tangentially).
# State: pencil end height ye. While ye is above y_touch the pencil only slides in. Below, each turn shaves one layer: advance ADV mm per turn.
# Pencil profile at any time: r(y) = min(R, rc(y)) for y >= ye (flat end of radius rc(ye)) -> the pencil never pokes outside the cone.
import json, math
import numpy as np
FPS_K = 120
TH = math.radians(11.0); TN = math.tan(TH)
BODY_Y0, BODY_Y1, BODY_X0, BODY_Z = -12.5, 12.5, -8.5, 5.5
R_EXIT = 0.6; Y_APEX = BODY_Y0 - R_EXIT / TN
R_BORE = 3.75; Y_CONE_TOP = Y_APEX + R_BORE / TN
R_PEN, R_LEAD = 3.6, 1.0
Y_TOUCH = Y_APEX + R_PEN / TN
Y_LEAD = Y_APEX + R_LEAD / TN
YE_FINAL = BODY_Y0                                  # the blade ends at the body bottom: round tip of radius R_EXIT (prism sharpeners give a round tip)
ADV = 0.75                                           # mm of axial advance per pencil turn (shaving thickness ~ ADV * sin(TH) = 0.14 mm)
rc = lambda y: max(0.0, (y - Y_APEX) * TN)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0, 'vo1': 3.1}
T['ins_a'] = T['vo1'] + 0.4; T['ins_b'] = T['vo1'] + 2.0
T['vo2'] = T['vo1'] + dur[1] + 0.3; T['cut_a'] = T['vo2'] + 0.35
T['vo3'] = T['vo2'] + dur[2] + 0.3
T['vo4'] = T['vo3'] + dur[3] + 0.3
T['cut_b'] = T['vo4'] + dur[4] - 0.2
T['vo5'] = T['vo4'] + dur[4] + 0.4
LOOP = round(T['vo5'] + dur[5] + 2.0, 2); T['LOOP'] = LOOP
YE_START = BODY_Y1 + 9.0
def state(t):
    """pencil end ye, pencil turn angle, lift (hook pull-out), cut fraction 0..1"""
    if t < T['hookEnd']:                             # hook: the finished pencil comes out of the sharpener, turning slowly
        ye = YE_FINAL; turns = (Y_TOUCH - YE_FINAL) / ADV
        return ye, 2 * math.pi * turns + 1.2 * t, 24.0 + 4.0 * t, 1.0
    if t < T['cut_a']:
        ye = YE_START + (Y_TOUCH - YE_START) * ease((t - T['ins_a']) / (T['ins_b'] - T['ins_a'])); return ye, 0.0, 0.0, 0.0
    u = min(1, max(0, (t - T['cut_a']) / (T['cut_b'] - T['cut_a']))); f = 0.5 * ease(u) + 0.5 * u if u < 1 else 1.0
    ye = Y_TOUCH + (YE_FINAL - Y_TOUCH) * f
    return ye, 2 * math.pi * (Y_TOUCH - ye) / ADV, 0.0, f
rows = []
for i in range(int(LOOP * FPS_K) + 2):
    t = i / FPS_K; ye, ang, lift, f = state(min(t, LOOP)); rows.append([round(t, 4), round(ye, 4), round(ang, 4), round(lift, 4), round(f, 5)])
json.dump(rows, open('kin.json', 'w'))
# ---------------- checks ----------------
# 1. pencil inside the hole at every height over the whole loop (bore above the cone, cone below), never below the body bottom while cutting
worst = 1e9
for t in np.arange(0, LOOP, 1 / 60):
    ye, ang, lift, f = state(t)
    for y in np.linspace(ye, BODY_Y1 + 20, 400):
        yy = y + lift
        if BODY_Y0 <= yy <= BODY_Y1:
            wall = R_BORE if yy >= Y_CONE_TOP else rc(yy)
            r = min(R_PEN, rc(y)) if f > 0 or t < T['hookEnd'] else R_PEN    # cut profile once cutting started
            if t >= T['hookEnd'] and f == 0: r = R_PEN
            worst = min(worst, wall - r)
    assert ye >= BODY_Y0 - 1e-6, ('pencil below the blade end', t)
    if f == 0 and t >= T['hookEnd']: assert ye >= Y_TOUCH - 1e-6, ('uncut pencil inside the cone', t)
print('pencil-hole min clearance %.3f mm (0 = touching the cone/blade edge)' % worst)
assert worst > -1e-6, 'pencil passes through the body'
# 2. the blade (tangent plane x*cos(TH) - (y - Y_APEX)*sin(TH) = 0 rotated: n = (cos, -sin)) never cuts into the pencil beyond the cone
#    pencil points satisfy r <= rc(y) -> distance to the tangent plane >= 0 (convexity)
mind = 1e9
for y in np.linspace(YE_FINAL, Y_TOUCH, 200):
    r = rc(y)
    for a in np.linspace(0, 2 * math.pi, 180):
        x, z = r * math.cos(a), r * math.sin(a); d = x * math.cos(TH) - (y - Y_APEX) * math.sin(TH)
        mind = min(mind, -d)
print('blade face to pencil min distance %.4f mm (0 only along the edge)' % mind)
assert mind > -1e-6
turns = (Y_TOUCH - YE_FINAL) / ADV
print('turns to sharpen: %.1f; lead exposed below y = %.2f' % (turns, Y_LEAD))
G = dict(LOOP=LOOP, T=T, FPS_K=FPS_K, TH=TH, BODY_Y0=BODY_Y0, BODY_Y1=BODY_Y1, BODY_X0=BODY_X0, BODY_Z=BODY_Z, R_EXIT=R_EXIT, Y_APEX=Y_APEX, R_BORE=R_BORE,
         Y_CONE_TOP=Y_CONE_TOP, R_PEN=R_PEN, R_LEAD=R_LEAD, Y_TOUCH=Y_TOUCH, Y_LEAD=Y_LEAD, YE_FINAL=YE_FINAL, ADV=ADV, YE_START=YE_START)
json.dump(G, open('geom.json', 'w'), indent=1)
print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
