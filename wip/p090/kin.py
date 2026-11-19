# p090 wiper park switch "WHY DO WIPERS / STOP AT THE BOTTOM?" - kinematics + HARD GATE 5.2 checks.
# Motor -> worm -> gear (angle phi, deg). One gear turn = one up-and-down wipe (crank-rocker, harmonic approximation):
#   wiper angle theta = THMAX * (1 - cos phi) / 2   -> phi = 0 (mod 360) is the PARK position (blade at the bottom).
# Park contact: a copper plate on the gear face; outer track has ONE insulating gap (GAP_W deg) centred so that it sits under the
# fixed contact finger exactly at phi = 0. With the dash switch OFF, the motor gets power ONLY through finger -> copper -> motor.
# Contact opens when phi mod 360 enters [360 - GAP_W/2, 360 + GAP_W/2]; the motor then brakes (shorted armature) to a stop at phi = 0.
# Timeline (slow motion after switch-off, shown on screen as SLOW MOTION): rows [t, phi, theta, switchOn, contactClosed, current, omega]
import json, math
THMAX = 95.0; GAP_W = 24.0; FPS_K = 120
vo = json.load(open('vo/vo.json')); dur = [d['dur'] for d in vo]
T = {'vo0': 0.25}
GAP = {1: 0.0, 2: 0.3, 3: 0.3, 4: 0.28, 5: 0.3, 6: 0.33}
T['vo1'] = 2.7
for i in range(2, 7): T[f'vo{i}'] = round(T[f'vo{i-1}'] + dur[i - 1] + GAP[i], 3)
LOOP = round(T['vo6'] + dur[6] + 1.55, 2); T['LOOP'] = LOOP
T['hookEnd'] = T['vo1'] - 0.25            # hook text until vo1
T['park0'] = 0.85                          # hook: blade lands at the bottom
T['on'] = 1.3                              # switch ON: wipers run
T['off'] = 3.4                             # switch OFF mid-swipe (blade halfway up, going up)
T['slow'] = 4.0                            # slow motion fully engaged
T['cutIn'] = T['vo2'] - 0.1
T['open'] = round(T['vo4'] + 2.9, 3)       # the gap reaches the contact: power cut
OMEGA_RUN = None
PHI_OFF = 810.0; PHI_OPEN = 1080.0 - GAP_W / 2; PHI_PARK = 1080.0
RAMP = 0.25
OMEGA_RUN = (PHI_OFF - 360.0) / ((T['off'] - T['on']) - RAMP / 2)
# after OFF: omega linear from OMEGA_RUN to OMEGA_S over [off, slow], then OMEGA_S until open
D1 = T['slow'] - T['off']; D2 = T['open'] - T['slow']
OMEGA_S = (PHI_OPEN - PHI_OFF - D1 * OMEGA_RUN / 2) / (D1 / 2 + D2)
BRAKE = 2 * (PHI_PARK - PHI_OPEN) / OMEGA_S; T['stop'] = round(T['open'] + BRAKE, 3)
T['cutOut'] = round(T['vo5'] + 1.75, 3)
def phi(t):
    if t < T['park0']: u = t / T['park0']; return 270.0 + 90.0 * (1 - (1 - u) ** 2)
    if t < T['on']: return 360.0
    if t < T['off']:
        s = t - T['on']
        if s < RAMP: return 360.0 + OMEGA_RUN * s * s / (2 * RAMP)
        return 360.0 + OMEGA_RUN * RAMP / 2 + OMEGA_RUN * (s - RAMP)
    if t < T['slow']: s = t - T['off']; return PHI_OFF + OMEGA_RUN * s + (OMEGA_S - OMEGA_RUN) * s * s / (2 * D1)
    if t < T['open']: return PHI_OFF + D1 * (OMEGA_RUN + OMEGA_S) / 2 + OMEGA_S * (t - T['slow'])
    if t < T['stop']: s = t - T['open']; return PHI_OPEN + OMEGA_S * s - OMEGA_S * s * s / (2 * BRAKE)
    return PHI_PARK
def switch_on(t): return 1 if T['on'] <= t < T['off'] else 0
def contact(p): m = p % 360.0; return 0 if (m >= 360 - GAP_W / 2 - 1e-9 or m <= GAP_W / 2 + 1e-9) else 1
def theta(p): return THMAX * (1 - math.cos(math.radians(p))) / 2
rows = []; n = int(round(LOOP * FPS_K)) + 1
for i in range(n):
    t = min(LOOP, i / FPS_K); p = phi(t); sw = switch_on(t); c = contact(p)
    cur = 1 if (sw or c) and T['on'] <= t < T['open'] else 0      # current reaches the motor (from the switch or through the park contact)
    rows.append([round(t, 4), round(p, 4), round(theta(p), 4), sw, c, cur, 0.0])
for r0, r1 in zip(rows, rows[1:]): r0[6] = round((r1[1] - r0[1]) * FPS_K, 3)
# ---- HARD GATE 5.2 checks ----
assert abs(phi(T['off'] - 1e-6) - PHI_OFF) < 0.05 and abs(phi(T['open'] - 1e-6) - PHI_OPEN) < 0.05 and abs(phi(T['stop'] - 1e-6) - PHI_PARK) < 0.05
assert abs(PHI_OFF % 360 - 90) < 1e-6, 'switch-off is mid-swipe (blade halfway, going up)'
ph = [r[1] for r in rows]; assert all(b >= a - 1e-9 for a, b in zip(ph, ph[1:])), 'motor never runs backwards'
for r in rows:
    assert 0 - 1e-9 <= r[2] <= THMAX + 1e-9
    t, om = r[0], r[6]
    # nothing moves without a cause: the gear turns only with current, while braking right after the cut, or in the hook (which shows the same park ending)
    if om > 1e-6 and t >= T['on']: assert r[5] == 1 or T['open'] <= t < T['stop'] + 1e-6, ('moves without power', t)
    if T['off'] <= t < T['open']: assert r[3] == 0 and r[4] == 1, ('after switch-off the only power path is the park contact', t)
# the contact opens exactly when the gap edge reaches the finger, and the blade parks at the bottom
assert contact(phi(T['open'] - 0.01)) == 1 and contact(phi(T['open'] + 0.001)) == 0
assert theta(PHI_PARK) < 1e-9 and theta(PHI_OPEN) < 1.1
print('PASS run %.0f deg/s (%.2f s per wipe), slow-mo %.1f deg/s (x%.3f), cut at phi %.0f (blade %.2f deg), park after %.2f s brake; theta 0..%.0f' % (
    OMEGA_RUN, 360 / OMEGA_RUN, OMEGA_S, OMEGA_S / OMEGA_RUN, PHI_OPEN, theta(PHI_OPEN), BRAKE, THMAX))
json.dump(rows, open('kin.json', 'w'), separators=(',', ':'))
json.dump({'T': T, 'LOOP': LOOP, 'FPS_K': FPS_K, 'THMAX': THMAX, 'GAP_W': GAP_W}, open('geom.json', 'w'), indent=1)
print(json.dumps(T))
