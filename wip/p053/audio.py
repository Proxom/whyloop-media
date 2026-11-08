# p053 audio stems. usage: python3 audio.py <vo dir with vo0..4.wav> -> vo_stem.wav, bed_stem.wav (48 kHz stereo, LOOP s)
# SFX come from the same simulation as the picture (kin_240.json, events.json): road rumble follows the car speed v(t),
# a soft tap when the catch first meets the teeth, the lock clunk, a soft tick when it lets go, webbing rustle while the spool turns.
import json, sys, wave, numpy as np
SR = 48000; DUR = 15.0; N = int(SR * DUR); rng = np.random.default_rng(53)
VO_AT = [0.15, 2.75, 5.4, 8.95, 12.8]
def readwav(p):
    w = wave.open(p); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth(); x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).astype(float)
    x = x.reshape(-1, ch).mean(1) / (32768 if sw == 2 else 2 ** 31); n = int(len(x) * SR / sr); return np.interp(np.arange(n) * sr / SR, np.arange(len(x)), x)
vo = np.zeros(N)
for i, t in enumerate(VO_AT):
    x = readwav(f'{sys.argv[1]}/vo{i}.wav'); i0 = int(t * SR); vo[i0:i0 + len(x)] += x[:N - i0]
L = np.zeros(N); R = np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0):
    i0 = int(round(t * SR)); idx = (np.arange(len(sig)) + i0) % N; gl = np.cos((pan + 1) * np.pi / 4); gr = np.sin((pan + 1) * np.pi / 4)
    np.add.at(L, idx, sig * gain * gl); np.add.at(R, idx, sig * gain * gr)
def env(n, att, dec): t = np.arange(n) / SR; a = np.clip(t / att, 0, 1); return np.exp(-t / dec) * a * a * (3 - 2 * a)
def modal(fr, am, de, dur=0.25, att=0.0015):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f, a, d in zip(fr, am, de): f *= 1 + rng.uniform(-0.03, 0.03); s += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
    return s * env(n, att, 10)
def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
kin = json.load(open('kin_240.json')); ev = json.load(open('events.json'))
tk = np.array([k['t'] for k in kin]); tt = np.arange(N) / SR
v = np.interp(tt, tk, [k['v'] for k in kin], period=DUR); w = np.interp(tt, tk, [abs(k['w']) for k in kin], period=DUR)
# road rumble: low band noise, level follows speed (seamless: speed is the same at both ends of the loop)
rum = bandnoise(N, 40, 220); rum2 = bandnoise(N, 220, 600)
L += 0.10 * rum * v + 0.025 * rum2 * v; R += 0.10 * np.roll(rum, 977) * v + 0.025 * np.roll(rum2, 977) * v
# braking: a low tire-hum swell while decelerating (no squeal), from the deceleration a(t)
a = np.interp(tt, tk, [max(0, k['a']) for k in kin], period=DUR); hum = bandnoise(N, 70, 300)
L += 0.05 * hum * a * v; R += 0.05 * hum * a * v
# webbing rustle while the spool turns
rus = bandnoise(N, 150, 900); L += 0.08 * rus * np.clip(w / 0.8, 0, 1); R += 0.08 * rus * np.clip(w / 0.8, 0, 1)
tlock = [e['t'] for e in ev if e['type'] == 'lock'][0]
put(modal([150, 330, 560], [1.0, 0.5, 0.2], [0.09, 0.05, 0.03], dur=0.4, att=0.003), tlock, gain=0.85)    # lock clunk
put(modal([520, 860, 240], [0.8, 0.3, 0.5], [0.02, 0.014, 0.03], dur=0.15), 5.01, pan=0.1, gain=0.35)     # catch meets the teeth
put(modal([600, 980, 260], [0.8, 0.3, 0.5], [0.02, 0.014, 0.03], dur=0.15), 10.68, pan=0.1, gain=0.35)    # catch lets go
# music bed: soft pad + low marimba, 4 bars over the loop, fundamentals < 1 kHz (same palette as p051)
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]; seg = DUR / 4; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.9) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + m))
        e = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.9 - t) / 0.9, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.45) * SR)) % N; np.add.at(mus, idx, s * e * 0.06)
bass = [38, 34, 31, 33]
for ci in range(4):
    for b, g in [(0, 1.0), (seg / 2, 0.6)]:
        f = note(bass[ci] + 12); s = modal([f, f * 3.9], [1.0, 0.2], [0.5, 0.1], dur=1.2, att=0.004); idx = (np.arange(len(s)) + int((ci * seg + b) * SR)) % N; np.add.at(mus, idx, s * 0.2 * g)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N); L += 0.5 * mus; R += 0.5 * mus
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st):
    st = st / (np.abs(st).max() * 1.25); f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.stack([vo, vo], 1))
print('lock at', tlock)
