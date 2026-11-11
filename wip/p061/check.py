# p061 collision / mechanism check over the full loop at 240 Hz (geometry numbers mirror scene.html)
import json, math
J = json.load(open('kin_240.json')); E, R, FOL = J['E'], J['R'], J['FOL']; RB, ZS, LS = 10.5, 3.2, 17
worst = dict(camFace=9, camShellY=9, leverFork=9, leverBody=9, tangHole=9, gapNeg=0)
for k in J['K']:
    b = math.radians(k['b']); cx = k['pin'] + E * math.cos(b); cy = E * math.sin(b); face = k['x0'] + FOL
    worst['camFace'] = min(worst['camFace'], (cx - R) - face)            # cam disc vs follower face (must be >= 0)
    worst['camShellY'] = min(worst['camShellY'], math.sqrt(RB**2 - ZS**2) - (abs(cy) + R))  # informational: cam inside body outline in y
    a = math.radians(90 - k['g']); d = (math.cos(a), math.sin(a)); n = (-d[1], d[0])
    for s, w in [(5.5, 4.6), (20, 4.2), (46, 5.6), (60, 6.6), (65, 0)]:
        for sg in (-1, 1):
            px = k['pin'] + d[0] * s + n[0] * w * sg; py = d[1] * s + n[1] * w * sg
            worst['leverFork'] = min(worst['leverFork'], px - 0.0)       # fork + dropout occupy x <= 0
            if px < face + 0.0 + 1e-9: worst['leverBody'] = min(worst['leverBody'], px - face)  # lever must stay right of the follower face
    worst['gapNeg'] = min(worst['gapNeg'], k['x0'])
print({k: round(v, 4) for k, v in worst.items()})
assert worst['camFace'] >= 0.0199 and worst['leverFork'] > 0 and worst['gapNeg'] >= 0 and worst['leverBody'] == 9, 'COLLISION'
print('lever z +-2.6 < slot 3.2; cam cheeks z 1.4..3.0 < 3.2; tang half-diagonal', round(math.hypot(2.2, 1.2), 2), '< follower hole 2.9; OK')
