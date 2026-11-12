# p063 stapler: why do the legs bend in? mm, y up, x across the staple crown, z along the stapler (front = +z). Section plane z = 0.
# Anvil top y = 0; paper stack y 0..PT. Left leg at x0 = -W/2. Below y = 0 the leg follows the groove: quarter circle radius r, then flat inward.
import json, math
W, L, RW, PT, R = 12.2, 6.0, 0.32, 1.5, 0.6
X0 = -W / 2; SMAX = L - PT - RW; LF = SMAX - math.pi * R / 2; XIN = X0 + R + LF
LOOP = 20.0
T = dict(PRESS=[2.4, 3.3], FADE_OUT=[3.4, 4.2], PIERCE=[7.0, 9.6], CURL=[10.0, 14.4], BLADE_UP=[15.0, 15.6], FADE_IN=[16.6, 17.4], HEAD_UP=[17.6, 18.4],
         STAPLE_FADE=[19.3, 19.8], FOLLOW=[18.4, 19.75])
VO_AT = [0.2, 4.3, 7.0, 10.1, 15.4, 17.9]
HM_UP = 8.0
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(max(0.0, min(1.0, u)))
def ramp(t, a, b): return sm((t - a) / (b - a))
def state(t):
    t %= LOOP
    hm = HM_UP * (1 - ramp(t, *T['PRESS'])) + HM_UP * ramp(t, *T['HEAD_UP'])
    y_start = PT + L + RW * 0  # crown centre when the tips sit on the paper (stage 2 start)
    if t < T['PIERCE'][0]: yc = PT + hm + L
    elif t < T['CURL'][0]: yc = PT + L - PT * ramp(t, *T['PIERCE'])
    else: yc = L - SMAX * ramp(t, *T['CURL'])
    # blade bottom: on the crown while driving, then back up to the magazine top
    blade = yc + RW
    if t >= T['BLADE_UP'][0]: blade = (yc + RW) + (PT + hm + L + RW - (yc + RW)) * ramp(t, *T['BLADE_UP'])
    if t >= T['HEAD_UP'][0]: blade = PT + hm + L + RW
    return dict(t=round(t, 5), hm=round(hm, 5), yc=round(yc, 5), blade=round(blade, 5))
def leg_path(yc, side=-1, n=60):
    # centreline from the crown corner down to the tip for one leg (side -1 = left)
    x0 = side * W / 2; pts = []
    ybot = max(0.0, yc - L); s = max(0.0, L - yc)
    for i in range(n + 1): pts.append((x0, yc - 0.5 - (yc - 0.5 - ybot) * i / n))
    if s > 0:
        m = 80
        for i in range(1, m + 1):
            q = s * i / m
            if q <= math.pi * R / 2: ph = q / R; pts.append((x0 - side * (R - R * math.cos(ph)), -R * math.sin(ph)))
            else: pts.append((x0 - side * (R + q - math.pi * R / 2), -R))
    return pts
def anvil_poly():
    # anvil cross-section at z = 0 (x -11..11, y -1.8..0) with both grooves (wall offset RW + 0.05 from the leg path)
    g = RW + 0.05; Rg = R + g; out = [(-11, -1.8), (11, -1.8), (11, 0)]
    def groove(side):
        x0 = side * W / 2
        arc = [(x0 - side * (R - Rg * math.cos(math.radians(a))), -Rg * math.sin(math.radians(a))) for a in range(0, 91, 5)]
        flat_end = x0 - side * (R + LF + 0.5); ramp_end = x0 - side * (R + LF + 1.3)
        seq = arc + [(flat_end, -Rg), (ramp_end, 0.0)]
        return seq if side == 1 else seq[::-1]
    pts = out + groove(1) + groove(-1) + [(-11, 0)]
    return pts
G = dict(W=W, L=L, RW=RW, PT=PT, R=R, LF=LF, XIN=XIN, SMAX=SMAX, LOOP=LOOP, T=T, VO_AT=VO_AT, HM_UP=HM_UP, ANVIL=anvil_poly())
if __name__ == '__main__':
    json.dump(G, open('geom.json', 'w'), indent=0)
    K = [state(i / 240) for i in range(int(LOOP * 240))]
    json.dump(K, open('kin_240.json', 'w'))
    ev = [dict(type='press', t=2.95), dict(type='seat', t=T['PRESS'][1]), dict(type='pierce', t=7.15), dict(type='pierce_out', t=9.55),
          dict(type='bend', t0=10.0, t1=14.4), dict(type='clinch', t=14.35), dict(type='blade_up', t=15.45), dict(type='head_up', t=18.3)]
    json.dump(ev, open('events.json', 'w'), indent=0)
    print('XIN %.3f  SMAX %.3f  LF %.3f  frames %d' % (XIN, SMAX, LF, len(K)))
