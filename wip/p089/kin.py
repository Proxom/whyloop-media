# p089 hook-and-loop (Velcro) "WHY DOES / VELCRO STICK?" - kinematics + HARD GATE 5.2 checks. Units: macro units (1 = ~0.05 mm; hook ~10 tall).
# Macro side view (x right, y up, z toward camera). Bottom tape top face at y=0 with soft loops (arches in the y-z plane, feet at z_row +-2.2).
# Top tape (hooks hang down from its underside). Hook = stem (L=8) + arc of fixed length (radius 1.6 x 220 deg); bend b in (0,1] straightens it (curvature b/1.6).
# Each hook column i (x_i = -60 + 6 i) has its own loop in the same z-row, feet at x_e = x_i + 1.6; caught fibre = loop apex sits in the hook cup.
# Peel: the top tape bends up left of the peel front xf (radius RP), each hook root follows the tape; when its caught fibre has been lifted
# YREL above the loop's rest height the hook straightens, the fibre slides off the tip and the loop springs back (release), then the hook springs back.
import json, math
import numpy as np
L_STEM, R_ARC, A_ARC = 8.0, 1.6, math.radians(220); ARC_LEN = R_ARC * A_ARC; RT, RF = 0.4, 0.35; FOFF = RT + RF + 0.05
G = 15.0; H0 = 6.2; NCOL = 21; XS = [-60 + 6 * i for i in range(NCOL)]; RP = 14.0; AMAX = math.radians(115); YREL = 4.5
FPS = 30; FPS_K = 120
import os; DXR = float(os.environ.get('DXR', '0.8')); HR = float(os.environ.get('HR', '4.6'))   # released loops spring back combed: lower + leaning
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.3, 'hookEnd': 1.0, 'vo1': 1.75}
GAP = {2: 0.3, 3: 0.3, 4: 0.45, 5: 0.35, 6: 0.2, 7: 0.45}
for i in range(2, 8): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo7'] + dur[7] + 1.45, 2); LOOP = round(math.ceil(LOOP * FPS) / FPS, 4); T['LOOP'] = LOOP
T['cutIn'] = T['hookEnd']
T['p3'] = T['vo3'] + 1.85; T['p0'] = T['p3'] - 3.2; T['p1'] = T['p0'] + 1.4; T['p2'] = T['p1'] + 1.0          # press (slow): down, slide over, settle = CAUGHT on 'catch'
T['s0'] = T['vo4'] + 0.2; T['s1'] = T['s0'] + 0.8; T['s2'] = T['vo5'] - 0.5; T['s3'] = T['vo5'] - 0.1      # flat pull (shear): right, hold, relax
T['f0'] = T['vo5'] + 0.1; T['f1'] = T['vo6'] + dur[6] + 0.2                                               # peel front travels
T['ans'] = T['vo7'] - 0.05
XF0, XF1 = -41.0, 4.0; SHEAR = 2.0; LEAN = math.radians(8)   # flat pull: tape slides 2.0, hooks lean back 8 deg (cups move only ~0.7)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def lerp(a, b, u): return a + (b - a) * u
def lean_at(t):
    if T['s0'] <= t < T['s1']: return -LEAN * ease((t - T['s0']) / (T['s1'] - T['s0']))
    if T['s1'] <= t < T['s2']: return -LEAN
    if T['s2'] <= t < T['s3']: return -LEAN * (1 - ease((t - T['s2']) / (T['s3'] - T['s2'])))
    return 0.0
def tape_pose(t):
    """(ox, oy, xf): tape offset (x, root-y shift) and peel front."""
    if t < T['p0']: return (-2.9, 42.0 - G, -1e9) if t >= T['cutIn'] else (0.0, 0.0, -1e9)
    if t < T['p1']: return (-2.9, lerp(42.0, 11.7, ease((t - T['p0']) / (T['p1'] - T['p0']))) - G, -1e9)
    if t < T['p2']: return (lerp(-2.9, 0.0, ease((t - T['p1']) / (T['p2'] - T['p1']))), 11.7 - G, -1e9)
    if t < T['p3']: return (0.0, lerp(11.7, G, ease((t - T['p2']) / (T['p3'] - T['p2']))) - G, -1e9)
    if t < T['s0']: return (0.0, 0.0, -1e9)
    if t < T['s1']: return (SHEAR * ease((t - T['s0']) / (T['s1'] - T['s0'])), 0.0, -1e9)
    if t < T['s2']: return (SHEAR, 0.0, -1e9)
    if t < T['s3']: return (SHEAR * (1 - ease((t - T['s2']) / (T['s3'] - T['s2']))), 0.0, -1e9)
    if t < T['f0']: return (0.0, 0.0, -1e9)
    u = (t - T['f0']) / (T['f1'] - T['f0']); u = min(1, max(0, u))
    return (0.0, 0.0, lerp(XF0, XF1, 0.5 * u + 0.5 * ease(u)))
def tape_point(u, ox, oy, xf):
    """point on the tape underside for rest coordinate u, and its rotation (rad, + = CCW)."""
    if u >= xf: return u + ox, G + oy, 0.0
    s = xf - u; sa = RP * AMAX
    if s <= sa: ph = s / RP; return xf - RP * math.sin(ph) + ox, G + RP * (1 - math.cos(ph)) + oy, -ph
    x0, y0 = xf - RP * math.sin(AMAX), G + RP * (1 - math.cos(AMAX)); d = s - sa
    return x0 - d * math.cos(AMAX) + ox, y0 + d * math.sin(AMAX) + oy, -AMAX
def hook_curve(b, n=40):
    """hook centreline in tape-local coords (hook hangs to -y, curls toward +x). returns pts, tangents (arc part only for s)."""
    pts = [(0.0, -L_STEM * k / 8) for k in range(9)]
    k = b / R_ARC; th = -math.pi / 2; x, y = 0.0, -L_STEM; ds = ARC_LEN / n
    for i in range(n): th2 = th + k * ds; x += math.cos((th + th2) / 2) * ds; y += math.sin((th + th2) / 2) * ds; th = th2; pts.append((x, y))
    return pts
def arc_point(b, s):
    """point + inward normal at arc length s (may exceed ARC_LEN: straight extrapolation past the tip)."""
    k = b / R_ARC; th = -math.pi / 2; x, y = 0.0, -L_STEM; n = 80; S = min(s, ARC_LEN); ds = S / n
    for i in range(n): th2 = th + k * ds; x += math.cos((th + th2) / 2) * ds; y += math.sin((th + th2) / 2) * ds; th = th2
    if s > ARC_LEN: x += math.cos(th) * (s - ARC_LEN); y += math.sin(th) * (s - ARC_LEN)
    return x, y, (-math.sin(th), math.cos(th))
S_CUP = R_ARC * math.pi / 2
def fibre_local(b, s): x, y, nrm = arc_point(b, s); return x + nrm[0] * FOFF, y + nrm[1] * FOFF
def to_world(px, py, rx, ry, rot): c, s = math.cos(rot), math.sin(rot); return rx + c * px - s * py, ry + s * px + c * py
# ---- per-hook release state machine over a fine clock ----
DTK = 1 / FPS_K; NK = int(round(LOOP * FPS_K)) + 1
REL_T, SLIDE_T, SNAP_T, BACK_T = 0.10, 0.06, 0.12, 0.16
state = [dict(caught=False, rel=None) for _ in XS]; REL_LOG = [None] * len(XS)
rows = []
for kk in range(NK):
    t = min(LOOP, kk * DTK); ox, oy, xf = tape_pose(t); caughtNow = t >= T['p3'] and t < T['ans']
    R = []
    for i, xi in enumerate(XS):
        rx, ry, rot = tape_point(xi, ox, oy, xf); rot += lean_at(t); st = state[i]; xe = xi + 1.6
        b, s, apex, glow = 1.0, S_CUP, (xe, H0), 0.0
        if t < T['p3'] or t >= T['ans']:                  # before the catch completes (and in the outside end shot): loops at rest, hooks free
            st['caught'] = False; st['rel'] = None; st.pop('off', None)
            if T['p1'] <= t < T['p3']:                     # sliding into / settling in the cup: fibre at the rest apex, hook moves around it
                pass
        else:
            if st['rel'] is None:
                fx, fy = to_world(*fibre_local(1.0, S_CUP), rx, ry, rot)
                if fy - H0 > YREL: st['rel'] = t; REL_LOG[i] = t
            if st['rel'] is None: b = 1.0; s = S_CUP; apex = to_world(*fibre_local(1.0, S_CUP), rx, ry, rot); glow = 0.6 if (T['s0'] <= t < T['s3']) else 0.0
            else:
                tr = t - st['rel']; glow = 0.0
                if tr < REL_T: u = ease(tr / REL_T); b = lerp(1.0, 0.32, u); s = lerp(S_CUP, ARC_LEN * 0.92, u); apex = to_world(*fibre_local(b, s), rx, ry, rot)
                elif tr < REL_T + SLIDE_T: u = ease((tr - REL_T) / SLIDE_T); b = 0.32; s = lerp(ARC_LEN * 0.92, ARC_LEN + 1.6, u); apex = to_world(*fibre_local(b, s), rx, ry, rot)
                else:
                    tr2 = tr - REL_T - SLIDE_T; b0 = 0.32; s = ARC_LEN + 1.6
                    p_off = st.setdefault('off', to_world(*fibre_local(b0, s), rx, ry, rot))
                    u = ease(tr2 / SNAP_T); apex = (lerp(p_off[0], xe + DXR, u), lerp(p_off[1], HR, u))
                    b = lerp(b0, 1.0, ease((tr2 - SNAP_T * 0.6) / BACK_T)); s = -1
        R.append([round(rx, 4), round(ry, 4), round(rot, 5), round(b, 4), round(apex[0], 4), round(apex[1], 4), round(glow, 3), 0.0])
    if T['f0'] <= t < T['ans']:      # peel: ONLY the row at the bend glows; released and not-yet-loaded rows dimmed
        act = None
        for i in range(NCOL):
            r_ = state[i]['rel']
            if r_ is not None and t - r_ < REL_T + SLIDE_T + 0.12: act = i; break
        if act is None:
            lifts = [(R[i][5] - H0, i) for i in range(NCOL) if state[i]['rel'] is None]
            lifts = [x for x in lifts if x[0] > 0.4]
            if lifts: act = max(lifts)[1]
        for i in range(NCOL): R[i][6] = 1.0 if i == act else 0.0; R[i][7] = 0.0 if i == act else 1.0
    rows.append((t, R, (round(ox, 4), round(oy, 4), round(max(xf, -999), 4))))
# ---- HARD GATE 5.2 checks (120 Hz): hook tube vs every loop fibre crossing the hook plane, hooks vs bottom tape ----
def loop_top_segment(ax, ay): return [(ax, ay), (ax, ay - 0.05)]   # superellipse arch (n=4, half-width 2.2): within |z|<0.8 of the hook plane the fibre dips < 0.02
minclr = 9; worst = None; caught_ok = True
for t, R, _p in rows:
    for i, r in enumerate(R):
        rx, ry, rot, b = r[0], r[1], r[2], r[3]; pts = np.array([to_world(px, py, rx, ry, rot) for px, py in hook_curve(b)])
        assert pts[:, 1].min() - RT > 0.0, ('hook into bottom tape', t, i)
        for j in range(max(0, i - 2), min(len(R), i + 3)):
            ax, ay = R[j][4], R[j][5]
            for (qx, qy) in loop_top_segment(ax, ay):
                d = np.sqrt(((pts - [qx, qy]) ** 2).sum(1)).min() - RT - RF
                if d < minclr: minclr, worst = d, (round(t, 3), i, j)
assert minclr > 0, ('hook passes through a loop', minclr, worst)
# every hook released exactly once during the peel and in order (one row at a time)
rels = REL_LOG
print('release times (s):', [None if r is None else round(r, 2) for r in rels])
order = [r for r in rels if r is not None]; assert order == sorted(order), 'release order'
gaps = np.diff(order); print('min gap between rows %.2f s' % gaps.min()); assert gaps.min() > 0.2
# shear: all hooks caught, none released
for t, R, _p in rows:
    if T['s0'] <= t < T['s3']: assert all(REL_LOG[i] is None or REL_LOG[i] > t for i in range(NCOL))
print('PASS: min clearance hook-loop %.3f at %s' % (minclr, worst))
# ---- export at the video frame rate ----
out = [[round(t, 4), *P] + sum(R, []) for (t, R, P) in rows if abs(t * FPS - round(t * FPS)) < 1e-6]
json.dump(out, open('kin.json', 'w'))
G_OUT = dict(T=T, LOOP=LOOP, FPS=FPS, NCOL=NCOL, XS=XS, G=G, H0=H0, RP=RP, AMAX=AMAX, L_STEM=L_STEM, R_ARC=R_ARC, ARC_LEN=ARC_LEN, RT=RT, RF=RF,
             XF0=XF0, XF1=XF1, SHEAR=SHEAR, REL=[None if r is None else round(r, 4) for r in REL_LOG], WLOOP=2.2)
json.dump(G_OUT, open('geom.json', 'w'), indent=1); print('LOOP', LOOP, {k: round(v, 2) for k, v in T.items()})
