# p055 audio stems. usage: python3 audio.py <vo dir with vo0..5.wav> -> vo_stem.wav, bed_stem.wav (48 kHz stereo, LOOP s)
# SFX come from the same simulation as the picture (kin_240.json, events.json): bolt rub while the strike pushes it in,
# the latch click when the spring snaps it out, the door thud on the stop, a dull clunk when the flat side holds, handle clicks.
# All SFX are low modal sounds (fundamentals < 1 kHz): no beeps, chimes, squeaks or metal clinks.
import json, sys, wave, numpy as np
SR = 48000; DUR = 15.0; N = int(SR * DUR); rng = np.random.default_rng(55)
VO_AT = [0.15, 2.75, 5.65, 7.9, 9.8, 12.85]
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
kin = json.load(open('kin_240.json')); ev = {e['type']: e['t'] for e in json.load(open('events.json'))}
tk = np.arange(len(kin)) / 240.0; tt = np.arange(N) / SR
e = np.interp(tt, tk, [k['e'] for k in kin], period=DUR); d = np.interp(tt, tk, [k['d'] for k in kin], period=DUR)
de = np.gradient(e) * SR; dd = np.gradient(d) * SR
# bolt rubbing on the strike while it is pushed in (no handle): level from the inward speed
push = np.clip(-de / 12.0, 0, 1) * (np.interp(tt, tk, [k['phi'] for k in kin], period=DUR) < 1e-4)
rub = bandnoise(N, 180, 900); L += 0.10 * rub * push; R += 0.10 * np.roll(rub, 311) * push
# soft air movement of the swinging door
air = bandnoise(N, 60, 380); sw = np.clip(np.abs(dd) / 40.0, 0, 1); L += 0.05 * air * sw; R += 0.05 * np.roll(air, 977) * sw
put(modal([480, 820, 260], [0.9, 0.35, 0.6], [0.025, 0.015, 0.04], dur=0.2), ev['snap'], pan=0.1, gain=0.8)         # latch click
put(modal([85, 150, 240], [1.0, 0.6, 0.3], [0.12, 0.07, 0.04], dur=0.5, att=0.004), ev['stop'], gain=0.9)            # door on the stop
put(bandnoise(int(0.08 * SR), 60, 500) * env(int(0.08 * SR), 0.002, 0.02), ev['stop'], gain=0.35)
put(modal([140, 300, 520], [1.0, 0.45, 0.2], [0.09, 0.05, 0.03], dur=0.35, att=0.003), ev['hold'], gain=0.75)        # flat side holds
put(modal([380, 690, 220], [0.7, 0.25, 0.4], [0.02, 0.012, 0.03], dur=0.15), ev['handle'] + 0.05, pan=-0.2, gain=0.4)  # handle turns
put(modal([420, 760, 240], [0.8, 0.3, 0.5], [0.022, 0.013, 0.03], dur=0.15), ev['handle_back'] + 0.12, pan=-0.2, gain=0.45)  # bolt springs back out
# music bed: soft pad + low marimba, 4 bars over the loop, fundamentals < 1 kHz (same palette as p051/p053)
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[50, 57, 62, 65], [46, 53, 58, 62], [43, 50, 55, 58], [45, 52, 57, 61]]; seg = DUR / 4; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.9) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + m))
        en = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.9 - t) / 0.9, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.45) * SR)) % N; np.add.at(mus, idx, s * en * 0.06)
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
print('events', ev)
