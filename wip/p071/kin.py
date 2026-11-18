# p071 umbrella spring catch - kinematics (mm, y up, shaft axis = y, catch on +x side).
# Rib pivot R=(9,-2) on the top notch; stretcher (L_ST) from the runner top collar (9, yt) to the rib at S_AT from the pivot.
# Spring catch: tab rigid in the tube slit, slanted face toward the runner's approach (down): protrusion e(y)=E*f(y), f 0 at Y_LO .. 1 at Y_HI (flat top).
# Tab pushed in by d (mm). Runner bore R_IN = 4.2 over tube R_T = 4.0 -> required d = max over covered tab heights of (E f(y) - (R_IN - R_T) + CLR).
import json, math
R_T, R_IN, E, Y_LO, Y_HI, CLR = 4.0, 4.2, 2.5, -296.0, -281.0, 0.05
RUN_L = 40.0                  # runner length; bottom = yt - RUN_L
PIV = (9.0, -2.0); S_AT, L_ST, L_RIB = 200.0, 260.0, 560.0
FPS = 60
def theta_of(yt):             # rib angle from straight down (rad) for runner top yt (bisection, theta increases as yt rises)
    lo, hi = 0.0, math.radians(89)
    def g(th): x = PIV[0] + S_AT*math.sin(th) - 9.0; y = PIV[1] - S_AT*math.cos(th) - yt; return math.hypot(x, y) - L_ST
    # g(th) < 0 when the runner is too low for that angle -> distance shrinks as theta grows? solve monotone by scan
    best = None; prev = g(lo); a = lo
    for i in range(1, 900):
        b = math.radians(89) * i / 899; v = g(b)
        if (prev <= 0 < v) or (prev >= 0 > v): best = (a, b); break
        prev, a = v, b
    a, b = best
    for _ in range(50):
        m = (a + b) / 2
        if (g(a) <= 0) == (g(m) <= 0): a = m
        else: b = m
    return (a + b) / 2
YB_OPEN = Y_HI                 # runner bottom rests on the flat top
YT_OPEN = YB_OPEN + RUN_L      # -241
YT_OVER = YT_OPEN + 2.5        # overtravel when pushed past the catch
YT_CLOSED = None
# closed: rib angle 6 deg -> find yt by scanning
def yt_of_theta(th):
    x = PIV[0] + S_AT*math.sin(th) - 9.0; yr = PIV[1] - S_AT*math.cos(th)
    return yr - math.sqrt(L_ST**2 - x**2)
YT_CLOSED = yt_of_theta(math.radians(6))
YT_PRE = YB_OPEN - 2.0 + 0 - (E*0) + RUN_L - 30.0     # just before the catch: runner TOP 30 mm below the open top... (set below)
def smooth(u): u = max(0.0, min(1.0, u)); return u*u*(3 - 2*u)
def ease(t, a, b, y0, y1): return y0 + (y1 - y0) * smooth((t - a) / (b - a))
def need_d(yt):
    yb = yt - RUN_L; lo, hi = max(yb, Y_LO), min(yt, Y_HI)
    if hi <= lo: return 0.0
    f = (hi - Y_LO) / (Y_HI - Y_LO)          # protrusion grows with y -> worst at the highest covered point
    return max(0.0, E * f - (R_IN - R_T) + CLR)

# ---------------- timeline from the voiceover ----------------
import sys
VO = json.load(open('vo/vo.json'))
D = [v['dur'] for v in VO]
GAP = 0.22
T = {}
T['vo0'] = 0.15
T['hookEnd'] = max(1.55, T['vo0'] + D[0] + 0.15)
T['vo1'] = T['hookEnd'] + 0.1
T['vo2'] = T['vo1'] + D[1] + 0.08
T['vo3'] = T['vo2'] + D[2] + GAP + 0.2
T['vo4'] = T['vo3'] + D[3] + GAP
T['vo5'] = T['vo4'] + D[4] + GAP + 0.3
T['vo6'] = T['vo5'] + D[5] + GAP + 0.2
LOOP = round(T['vo6'] + D[6] + 0.9, 1)
T['LOOP'] = LOOP
YT_TOUCH = Y_LO - 0.4            # runner top just under the slope (no contact yet)
YT_LOOP = YT_OPEN - 22.0         # loop seam: runner 22 mm below rest, rising (umbrella almost open)
V_LOOP = None
# piecewise runner-top path yt(t) and finger press df(t)
def yt_at(t):
    # 0 .. snap: finish the opening from YT_LOOP (continues the end of the loop)
    a0, a1 = 0.0, 0.55
    if t < a1: return YT_LOOP + (YT_OVER - YT_LOOP) * (t / a1) ** 1.0
    if t < a1 + 0.35: return ease(t, a1, a1 + 0.35, YT_OVER, YT_OPEN)
    if t < T['vo1']: return YT_OPEN
    # cut to the closed umbrella; slide up to just under the catch during vo1
    if t < T['vo1'] + 0.35: return YT_CLOSED
    if t < T['vo2'] + 0.2: return ease(t, T['vo1'] + 0.35, T['vo2'] + 0.2, YT_CLOSED, YT_TOUCH)
    if t < T['vo3'] + 0.3: return YT_TOUCH
    # step 1: slow push, the runner shoves the catch in
    if t < T['vo4'] + 0.15: return ease(t, T['vo3'] + 0.3, T['vo4'] + 0.15, YT_TOUCH, YT_OPEN - 9.0)
    # step 2: passes, snap, settles on the flat top
    s0 = T['vo4'] + 0.15; s1 = s0 + 1.1
    if t < s1: return YT_OPEN - 9.0 + (YT_OVER - (YT_OPEN - 9.0)) * smooth((t - s0) / (s1 - s0)) 
    if t < s1 + 0.45: return ease(t, s1 + 0.05, s1 + 0.45, YT_OVER, YT_OPEN)
    if t < T['vo5'] + 0.85: return YT_OPEN
    # step 3: catch pressed (vo5 .. +0.7), runner slides down to closed
    if t < T['vo6'] - 0.1: return ease(t, T['vo5'] + 0.85, T['vo6'] - 0.1, YT_OPEN, YT_CLOSED)
    # payoff: open again, reaches the loop seam at LOOP
    if t < T['vo6'] + 0.4: return YT_CLOSED
    u = (t - (T['vo6'] + 0.4)) / (LOOP - (T['vo6'] + 0.4))
    return YT_CLOSED + (YT_LOOP - YT_CLOSED) * (1 - (1 - u) ** 1.6) if u < 1 else YT_LOOP
def df_at(t):     # finger press on the tab (step 3)
    a = T['vo5'] + 0.25; b = a + 0.5; c = T['vo5'] + 0.85 + 0.9
    return 2.6 * min(smooth((t - a) / (b - a)), 1 - smooth((t - c) / 0.4))
rows = []; worst = 1e9; snaps = []
N = int(LOOP * FPS) + 1
prev_d = 0
for i in range(N):
    t = i / FPS; yt = yt_at(t); need = need_d(yt); dfi = df_at(t); d = max(need, dfi)
    th = theta_of(yt)
    # HARD GATE 5.2: runner bore never cuts into the tab
    yb = yt - RUN_L
    for k in range(31):
        y = Y_LO + (Y_HI - Y_LO) * k / 30
        if yb + 1e-6 < y <= yt:
            gap = R_IN - (R_T + E * (y - Y_LO) / (Y_HI - Y_LO) - d)
            worst = min(worst, gap)
    # runner bottom never below the flat top while the tab is out
    if yb < Y_HI - 0.01 and yb > Y_LO and d < E * 1.0 - 0.2 - 1e-6 and need_d(yt) > d + 1e-6: raise SystemExit('runner inside tab')
    if prev_d > 1.5 and d < 0.3 and dfi < 0.1: snaps.append(round(t, 3))
    prev_d = d
    rows.append([round(t, 4), round(yt, 3), round(d, 3), round(math.degrees(th), 3), round(dfi / 2.6, 3)])
assert worst >= CLR - 1e-6, worst
# loop seam
assert abs(rows[0][1] - yt_at(LOOP - 1e-6)) < 0.6, (rows[0][1], yt_at(LOOP - 1e-6))
G = dict(LOOP=LOOP, T=T, FPS_K=FPS, R_T=R_T, R_IN=R_IN, E=E, Y_LO=Y_LO, Y_HI=Y_HI, RUN_L=RUN_L, PIV=PIV, S_AT=S_AT, L_ST=L_ST, L_RIB=L_RIB,
         YT_OPEN=YT_OPEN, YT_CLOSED=round(YT_CLOSED, 2), YT_TOUCH=YT_TOUCH, snaps=snaps,
         TH_OPEN=round(math.degrees(theta_of(YT_OPEN)), 2), TH_CLOSED=round(math.degrees(theta_of(YT_CLOSED)), 2), TH_TOUCH=round(math.degrees(theta_of(YT_TOUCH)), 2))
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
print(json.dumps(G)); print('min bore-to-tab gap', round(worst, 3), 'mm; rows', len(rows))
