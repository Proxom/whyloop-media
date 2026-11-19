# p085 Schrader tire valve "WHY DOESN'T / THE AIR ESCAPE?" - kinematics + HARD GATE 5.2 checks.
# Valve frame (model units, 1 u = 0.1 mm), stem axis = +y (toward the hub; the bike wheel's valve sits at 6 o'clock). Seat = barrel bottom face at y = 0.
# Core: brass barrel (bore r 12) screwed into the stem; pin r 3 through it; brass cup + rubber washer under the seat; spring between the cup and the cage ring.
# Closed: washer top = seat (y 0). The pump head's pusher presses the pin top down by d (open). Spring + tire air push the cup up; the pin follows the pusher back up.
import json, math
SEAT = 0.0; WASH_T = 4.0; CUP_T = 8.0; PIN_TOP0 = 104.0; STEM_TOP = 110.0; CAGE_TOP = -60.0
SPR_TURNS, SPR_WIRE = 5, 1.8; SPR_BOUND = (SPR_TURNS + 2) * 2 * SPR_WIRE
D_MAX = 14.0; PUSH_LEN = 22.0; CEIL_SEATED = STEM_TOP + 2.0          # pusher bottom = ceiling - PUSH_LEN; seated -> pusher at 90 -> d = 14
HEAD_RI, THREAD_R, CAP_RI = 42.0, 40.0, 42.0; CUP_R, LEG_RI, BORE_R, BORE_STEP = 20.0, 22.0, 26.0, -70.0
CEIL_AWAY = 330.0
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]; gap = 0.28
T = {'vo0': 0.3, 'hookEnd': 1.0}
T['vo1'] = 2.45
EXTRA = {3: 0.45, 5: 0.25}   # longer gaps so every step caption is on screen >= 2.5 s at full opacity
for i in range(2, 8): T[f'vo{i}'] = T[f'vo{i-1}'] + dur[i - 1] + gap + EXTRA.get(i, 0)
LOOP = round(T['vo7'] + dur[7] + 1.9, 2); T['LOOP'] = LOOP
T['cap_a'] = T['vo1'] + 0.1; T['cap_b'] = T['vo1'] + 1.0; T['cut_a'] = T['vo1'] + 1.15; T['cut_b'] = T['vo1'] + 2.1
T['head_a'] = T['vo4'] - 0.1; T['head_b'] = T['vo4'] + 1.35                       # pump head comes down and seats
T['flow_a'] = T['vo5'] - 0.1; T['flow_b'] = T['vo6'] + 0.35                       # pumping
T['lift_a'] = T['vo6'] + 0.35; T['lift_b'] = T['vo6'] + 0.75                      # pump pulled off (fast)
def ease(u): u = min(1, max(0, u)); return u * u * (3 - 2 * u)
def ceil_of(t):
    if t < T['hookEnd']:                                                            # hook replay: seated, then pulled off 0.28-0.55 s
        return CEIL_SEATED + (CEIL_AWAY - CEIL_SEATED) * ease((t - 0.28) / 0.27)
    if t < T['head_a']: return CEIL_AWAY
    if t < T['head_b']: return CEIL_AWAY + (CEIL_SEATED - CEIL_AWAY) * ease((t - T['head_a']) / (T['head_b'] - T['head_a']))
    if t < T['lift_a']: return CEIL_SEATED
    if t < T['lift_b']: return CEIL_SEATED + (CEIL_AWAY - CEIL_SEATED) * ease((t - T['lift_a']) / (T['lift_b'] - T['lift_a']))
    return CEIL_AWAY
def d_of(ceil): return max(0.0, min(D_MAX, PIN_TOP0 - (ceil - PUSH_LEN)))         # pin pushed only while the pusher touches it
def flow_of(t, d, ceil):
    seated = abs(ceil - CEIL_SEATED) < 1e-6
    if t < T['hookEnd']: return 1.0 if (seated and d > 0) else 0.0
    return 1.0 if (seated and d > 0 and T['flow_a'] <= t < T['flow_b']) else 0.0
def cut_of(t):
    if t < T['hookEnd']: return 180.0
    if t < T['cut_a']: return 0.0
    return 180.0 * ease((t - T['cut_a']) / (T['cut_b'] - T['cut_a']))
def cap_of(t):  # 0 = on, 1 = off and gone (cap only in the outside shot)
    if t < T['hookEnd']: return 1.0
    return ease((t - T['cap_a']) / (T['cap_b'] - T['cap_a']))
FPS_K = 120; rows = []; N = int(LOOP * FPS_K) + 1
for i in range(N):
    t = i / FPS_K; c = ceil_of(t); d = d_of(c); f = flow_of(t, d, c)
    rows.append([round(t, 4), round(c, 4), round(d, 4), round(cut_of(t), 3), round(cap_of(t), 4), f])
# ---------------- HARD GATE 5.2 checks over the whole loop ----------------
bad = []
for r in rows:
    t, c, d = r[0], r[1], r[2]
    wtop = SEAT - d; pinTop = PIN_TOP0 - d; pb = c - PUSH_LEN
    if wtop > SEAT + 1e-9: bad.append((t, 'washer above the seat'))
    if pb < pinTop - 1e-9: bad.append((t, 'pusher inside the pin'))
    if d > 0 and abs(pb - pinTop) > 1e-6: bad.append((t, 'pin moved without the pusher touching it'))
    L = (SEAT - WASH_T - CUP_T - d) - CAGE_TOP
    if L < SPR_BOUND: bad.append((t, 'spring coil-bound'))
    if c < CEIL_SEATED - 1e-9: bad.append((t, 'head below the stem top'))
    if SEAT - WASH_T - CUP_T - d < BORE_STEP: bad.append((t, 'cup hits the bore step'))
    if r[5] and d <= 0: bad.append((t, 'air flows through a closed valve'))
assert HEAD_RI > THREAD_R and CAP_RI > THREAD_R and LEG_RI > CUP_R and BORE_R > LEG_RI + 3 - 0.01
print('checks:', 'PASS' if not bad else bad[:5])
dmax = max(r[2] for r in rows); Lmin = min((SEAT - WASH_T - CUP_T - r[2]) - CAGE_TOP for r in rows)
print('d max %.2f, spring min %.1f (coil-bound %.1f), LOOP %.2f' % (dmax, Lmin, SPR_BOUND, LOOP))
# loop: last state = closed, head away; first frame = hook replay (seated) -> cut with the flash
G = dict(LOOP=LOOP, T={k: round(v, 3) for k, v in T.items()}, FPS_K=FPS_K, SEAT=SEAT, WASH_T=WASH_T, CUP_T=CUP_T, PIN_TOP0=PIN_TOP0, STEM_TOP=STEM_TOP,
         CAGE_TOP=CAGE_TOP, SPR_TURNS=SPR_TURNS, SPR_WIRE=SPR_WIRE, PUSH_LEN=PUSH_LEN, HEAD_RI=HEAD_RI, THREAD_R=THREAD_R, CUP_R=CUP_R, LEG_RI=LEG_RI, BORE_R=BORE_R, BORE_STEP=BORE_STEP)
json.dump(G, open('geom.json', 'w'), indent=1); json.dump(rows, open('kin.json', 'w'))
