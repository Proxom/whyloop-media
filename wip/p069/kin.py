# p069 car clutch (diaphragm-spring, push-type, single dry plate). mm, axis = +x (engine at -x, gearbox/wheels at +x).
# Flywheel friction face at x = 0. Rows of kin.json: [t, pedal 0..1, plate_x (front face), disc_x (front face), slope s, bearing_x (front face),
#   fork angle deg, engine angle deg, disc/wheel angle deg, disc speed rev/s]
import json, math
FPS_K = 60; LOOP = 25.2
G = dict(FW_R=140, FW_T=30, DISC_T=9.0, DISC_R=112, DISC_RI=60, PLATE_T=16, PLATE_RI=75, PLATE_RO=114, RIDGE_R=105, RIDGE_TUBE=2.0,
         FING_T=2.5, F_RI=32, F_RO=106, F_PIV=85, XF=38.25, BEAR_R0=22, BEAR_R1=40, BEAR_L=22, BEAR_RC=32, TORUS_D=2.55, TORUS_TUBE=1.0, HUB_R=26, HUB_X=[-8, 22], TUBE_R=[18, 21], TUBE_X0=45, LIP=[92, 127, 44, 47], S_ENG=-0.5, S_REL=0.0,
         FORK_PIV=[118, -120], FORK_L=120, SHAFT_R=12, LOOP=LOOP, FPS_K=FPS_K, ENG_RPS=83 / 151.2)
# pedal timeline: 1 = pressed (clutch disengaged). Hook 0-1 s: pressed -> released (payoff: clamp + wheel spins up).
PED = [(0.0, 1), (0.08, 1), (0.42, 0), (1.0, 0), (1.0001, 1), (8.6, 1), (9.8, 0), (15.2, 0), (16.3, 1), (LOOP, 1)]
EV = dict(cut=1.0, rel1=8.6, rel1_end=9.8, press2=15.2, press2_end=16.3, vo=[0.10, 1.40, 4.85, 8.50, 12.10, 15.10, 18.75, 22.40])
sm = lambda u: (lambda v: v * v * (3 - 2 * v))(max(0.0, min(1.0, u)))
def pedal(t):
    for (a, pa), (b, pb) in zip(PED, PED[1:]):
        if a <= t <= b: return pa + (pb - pa) * sm((t - a) / (b - a))
    return PED[-1][1]
def stack(p):
    """pedal p -> diaphragm slope, plate, disc, bearing positions (all from the lever geometry)."""
    s = G['S_ENG'] + (G['S_REL'] - G['S_ENG']) * p          # pushing the fingers in flattens the cone
    mid = lambda r: G['XF'] + (r - G['F_PIV']) * s            # finger mid-surface pivots on the fulcrum ring at r = 85
    c = math.sqrt(1 + s * s) * G['FING_T'] / 2               # half thickness measured along x on a tilted finger
    # finger rests on the plate's round ridge (torus tube at r = 105 on the plate back): centre-to-finger distance = tube + half thickness
    plate_back = mid(G['RIDGE_R']) - (G['FING_T'] / 2 + G['RIDGE_TUBE']) * math.sqrt(1 + s * s)
    plate_x = plate_back - G['PLATE_T']
    # disc: clamped when plate_x == DISC_T; otherwise floats centred in the gap
    gap = plate_x - G['DISC_T']
    disc_x = max(0.0, gap / 2)
    bear_x = mid(G['F_RI']) + c + 0.02                              # flat bearing face touches the finger tips (r = 32)
    tip = bear_x + G['BEAR_L'] + 3                            # fork prongs on the bearing's back flange
    fork = math.degrees(math.asin((tip - G['FORK_PIV'][0]) / G['FORK_L']))
    return s, plate_x, disc_x, bear_x, fork, gap
# speeds: engine constant; disc = engine when clamped (after a 1.1 s slip), decays to 0 over 1.8 s when free (car stops)
def solve_s_eng():
    lo, hi = -0.9, 0.0
    for _ in range(80):
        m = (lo + hi) / 2; G['S_ENG'] = m
        if stack(0)[1] < G['DISC_T']: lo = m
        else: hi = m
    G['S_ENG'] = hi
solve_s_eng()
def run():
    rows = []; dt = 1 / FPS_K; n = int(LOOP * FPS_K) + 1
    eng = 0.0; dsk = 0.0; w = 0.0
    for i in range(n):
        t = i * dt; p = pedal(t); s, px, dx, bx, fk, gap = stack(p)
        E = G['ENG_RPS']
        clamp = gap < 0.02
        if t < 1.0:   # hook: wheel stopped while pressed, then catches up
            w = 0.0 if not clamp else min(E, w + E * dt / 0.3)
        elif abs(t - 1.0) < dt: w = 0.0; dsk = 0.0
        elif clamp: w = min(E, w + E * dt / 1.1)
        else: w = max(0.0, w - E * dt / 2.4)
        eng += 360 * E * dt; dsk += 360 * w * dt
        rows.append([round(t, 4), round(p, 5), round(px, 4), round(dx, 4), round(s, 5), round(bx, 4), round(fk, 4), round(eng, 3), round(dsk, 3), round(w, 4)])
    # hook (t < 1): disc continues from the loop's final angle so frame 0 matches the last frame
    end = rows[-1][8]
    for r in rows:
        if r[0] < 1.0: r[8] = round(r[8] + end, 3)
    return rows
if __name__ == '__main__':
    R = run(); G['EV'] = EV
    json.dump(R, open('kin.json', 'w')); json.dump(G, open('geom.json', 'w'), indent=1)
    for t in [0, 0.5, 1.0, 5, 9.5, 10.2, 11, 15, 16.5, 18.7, 25.1]:
        r = R[int(t * FPS_K)]; print(t, 'pedal', r[1], 'plate', r[2], 'disc', r[3], 'bear', r[5], 'fork', r[6], 'w', r[9])
    # loop: engine angle per loop must be a multiple of 360/6 (6 bolts) so the last frame matches the first
    print('engine deg per loop', R[-1][7], 'mod 60 =', R[-1][7] % 60)
