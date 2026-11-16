# p067 gravity gate latch kinematics. mm. Gate closed: boards z in [-36,0], hinge axis at x=-900, z=-36. Latch bar on the gate front (bar plane z=10),
# pivot pin at x=-150; keeper (catch) on the post front face at x=60, profile in the (z, y) plane, y relative to the bar's bottom at rest (Y0).
# The gate angle TH(t) is scripted; the bar lift at the keeper (LIFT) is SOLVED: the ramp pushes it up (min lift with no overlap, shapely), gravity drops it
# (ballistic, a = 1.5 g for a bar pivoted at its end, divided by slow^2), the keep staple stops it at 0, the hand lifts it at the end.
import json, math, numpy as np
from shapely.geometry import Polygon, box
FPS_K = 120; LOOP = 26.4; HX, HZ = -900.0, -36.0; XK = 60.0; BZ = 10.0; BW = 6.0; BH = 20.0; LP = XK + 150.0  # pivot -> keeper distance
KEEP = [(0, -45), (6, -45), (6, -12), (60, -12), (62, -10), (22.5, 13.2), (21, 14), (19.6, 14), (18.6, 13.2), (18, 11), (18, -4), (6, -4), (6, 30), (0, 30)]
KP = Polygon(KEEP); assert KP.is_valid
def zc(th):  # bar centre z at the keeper for gate angle th (deg)
    a = math.radians(th); dx, dz = XK - HX, BZ - HZ; return HZ + dx * math.sin(a) + dz * math.cos(a)
def th_for(z):  # inverse of zc
    lo, hi = -1.0, 30.0
    for _ in range(60):
        m = (lo + hi) / 2; lo, hi = (m, hi) if zc(m) < z else (lo, m)
    return (lo + hi) / 2
def bar(z, L): return box(z - BW / 2, L, z + BW / 2, L + BH)
def req(z, L0=0.0):  # min lift >= L0 with no overlap with the keeper (bar pushed up from below only)
    if bar(z, L0).intersection(KP).area < 1e-6: return L0
    lo, hi = L0, 40.0
    for _ in range(40):
        m = (lo + hi) / 2; lo, hi = (lo, m) if bar(z, m).intersection(KP).area < 1e-6 else (m, hi)
    return hi
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(min(1, max(0, u)))
def seg(t, a, b, v0, v1, f=sm): return v0 + (v1 - v0) * f((t - a) / (b - a))
easein = lambda u: (lambda v: v ** 1.7)(min(1, max(0, u)))
TH_LOCK = th_for(15.0 - 0.3)   # bar front 0.3 mm from the wall: pull stops here
TH_HOOKB = th_for(14.0)        # hook bounce: bar hits the wall
EV = {}
def TH(t):
    # hook: push shut 0.35-1.70 (accelerating), bounce out to the wall 1.70-1.86, back to rest 1.86-2.3
    if t < 0.35: return 6.0
    if t < 1.70: return seg(t, 0.35, 1.70, 6.0, 0.0, easein)
    if t < 1.86: return seg(t, 1.70, 1.86, 0.0, TH_HOOKB, lambda u: math.sin(min(1, max(0, u)) * math.pi / 2))
    if t < 2.8: return seg(t, 1.86, 2.3, TH_HOOKB, 0.12)
    # problem (latch hidden): 14 deg -> push shut 3.3-4.3, bounce open to 9 deg 4.3-5.6
    if t < 3.3: return 14.0
    if t < 4.3: return seg(t, 3.3, 4.3, 14.0, 0.0, easein)
    if t < 10.6: return seg(t, 4.3, 5.6, 0.0, 9.0, lambda u: math.sin(min(1, max(0, u)) * math.pi / 2))
    # step 1: close slowly; ramp ride 11.4-14.4; step 2 slow motion over the lip 14.4-15.5 and onto the stop 15.5-16.2
    if t < 11.4: return seg(t, 10.6, 11.4, 9.0, th_for(50.0), lambda u: 1 - (1 - min(1, max(0, u))) ** 2)
    if t < 14.4: return seg(t, 11.4, 14.4, th_for(50.0), th_for(19.5), lambda u: min(1, max(0, u)))
    if t < 15.5: return seg(t, 14.4, 15.5, th_for(19.5), th_for(13.5), lambda u: min(1, max(0, u)))
    if t < 17.6: return seg(t, 15.5, 16.2, th_for(13.5), 0.0)
    # step 3: pull 17.6-18.3 -> the bar hits the wall and stays (pull held until 20.4), then back to rest
    if t < 18.3: return seg(t, 17.6, 18.3, 0.0, TH_LOCK, lambda u: min(1, max(0, u)) ** 1.5)
    if t < 20.4: return TH_LOCK - 0.004 * abs(math.sin((t - 18.3) * 9)) * math.exp(-(t - 18.3) * 3)
    if t < 23.6: return seg(t, 20.4, 21.0, TH_LOCK, 0.12)
    # open: hand lifts 23.6-24.1, gate opens 24.1-25.9 to 14 deg
    return seg(t, 24.1, 25.6, 0.12, 6.0)
def HAND(t):  # hand lift at the keeper (mm)
    if t < 23.6 or t > 25.1: return 0.0
    return seg(t, 23.6, 24.1, 0.0, 18.0) if t < 24.7 else seg(t, 24.7, 25.0, 18.0, 0.0)
def SLOW(t): return 6.0 if 14.0 < t < 16.5 else (1.6 if t < 3 else 2.5)
latch_on = lambda t: not (2.8 <= t < 6.0)   # the problem shot hides the latch (bar + keeper)
dt = 1 / FPS_K; N = int(round(LOOP * FPS_K)) + 1; rows = []; L = 0.0; v = 0.0; drops = []; hits = []
for i in range(N):
    t = i * dt; th = TH(t); z = zc(th)
    if not latch_on(t): L = 0.0; v = 0.0; rows.append([round(t, 4), round(th, 5), 0.0, round(z, 4), 0]); continue
    r = req(z); h = HAND(t)
    a = 1.5 * 9810.0 / SLOW(t) ** 2
    if r > L + 1e-6 or h > L: L = max(r, h); v = 0.0
    elif L > max(r, h):
        v -= a * dt; L2 = L + v * dt
        if L2 <= max(r, h):
            if max(r, h) == 0 and v < -40: drops.append(round(t, 3))
            L2 = max(r, h); v = -0.2 * v if max(r, h) == 0 and abs(v) > 60 else 0.0
        L = L2
    rows.append([round(t, 4), round(th, 5), round(L, 4), round(z, 4), 1])
# event times: gate on the stop, bar hits the wall
pr = None
for r in rows:
    if pr and pr[1] > 1e-4 and r[1] <= 1e-4: hits.append(('stop', r[0]))
    if pr and pr[3] < r[3] and r[3] + BW / 2 >= 18.0 - 0.35 and pr[3] + BW / 2 < 18.0 - 0.35 and r[2] < 12: hits.append(('wall', r[0]))
    pr = r
# first-landing per drop (debounce)
land = []; 
for d in drops:
    if not land or d - land[-1] > 0.3: land.append(d)
EV = {'land': land, 'hits': hits, 'TH_LOCK': TH_LOCK}
json.dump(rows, open('kin.json', 'w'), separators=(',', ':'))
json.dump({'LOOP': LOOP, 'FPS_K': FPS_K, 'KEEP': KEEP, 'XK': XK, 'BZ': BZ, 'BW': BW, 'BH': BH, 'LP': LP, 'HX': HX, 'HZ': HZ, 'EV': EV}, open('geom.json', 'w'), indent=1)
print('EV', EV); print('lift max', max(r[2] for r in rows))
for tt in [0, 1.0, 1.5, 1.7, 1.8, 2.5, 11.4, 13, 14.4, 15.0, 15.4, 16.2, 18.3, 22, 24.0, 24.5, 25.0, 26.4]:
    r = rows[int(round(tt * FPS_K))]; print(tt, r)
