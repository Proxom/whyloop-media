# p063 audio stems (adapted from p058). usage: python3 audio.py <vo dir> -> vo_stem.wav, bed_stem.wav (48 kHz stereo, LOOP s, seamless)
# SFX come from the same timeline as the picture (events.json): a faint plastic rub while the finger pushes,
# and the snap = copper bar hitting its contact + lever hitting its stop. All low modal sounds (fundamentals < 1 kHz).
import json, sys, wave, numpy as np
GM = json.load(open('geom.json')); SR = 48000; DUR = GM['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(63)
def readwav(p):
    w = wave.open(p); sr = w.getframerate(); ch = w.getnchannels(); sw = w.getsampwidth(); x = np.frombuffer(w.readframes(w.getnframes()), dtype={2: np.int16, 4: np.int32}[sw]).astype(float)
    x = x.reshape(-1, ch).mean(1) / (32768 if sw == 2 else 2 ** 31); n = int(len(x) * SR / sr); return np.interp(np.arange(n) * sr / SR, np.arange(len(x)), x)
vo = np.zeros(N)
for i, t in enumerate(GM['VO_AT']):
    x = readwav(f'{sys.argv[1]}/vo{i}.wav'); i0 = int(t * SR); idx = (np.arange(len(x)) + i0) % N; np.add.at(vo, idx, x)
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
EV = json.load(open('events.json'))
for e in EV:
    t = e.get('t')
    if e['type'] == 'press':      # palm on the cover: soft low thump
        put(modal([140, 260], [1.0, 0.4], [0.06, 0.03], dur=0.3, att=0.004), t, gain=0.6)
    if e['type'] == 'seat':       # magazine nose lands on the paper
        put(modal([210, 380], [1.0, 0.3], [0.04, 0.02], dur=0.2), t, pan=-0.1, gain=0.55)
    if e['type'] == 'pierce':     # tips start through the paper: low paper crunch
        n = int(2.3 * SR); u = np.arange(n) / n; put(bandnoise(n, 150, 900) * (0.3 + 0.7 * u) * np.sin(np.pi * u) ** 0.5, t, gain=0.05)
    if e['type'] == 'pierce_out': put(bandnoise(int(0.08 * SR), 200, 1000) * env(int(0.08 * SR), 0.001, 0.02), t, gain=0.25)
    if e['type'] == 'bend':       # wire scraping round the groove: low, slowly rising rub
        n = int((e['t1'] - e['t0']) * SR); u = np.arange(n) / n; put(bandnoise(n, 180, 800) * np.sin(np.pi * u) ** 0.4 * (0.5 + 0.5 * u), e['t0'], gain=0.05)
    if e['type'] == 'clinch':     # the crunch: legs flatten, the stapler bottoms out
        put(modal([170, 310, 520], [1.0, 0.55, 0.3], [0.08, 0.04, 0.025], dur=0.45, att=0.002), t, gain=1.0)
        put(bandnoise(int(0.07 * SR), 120, 900) * env(int(0.07 * SR), 0.001, 0.015), t, gain=0.35)
    if e['type'] == 'blade_up':   put(modal([330, 560], [1.0, 0.3], [0.02, 0.012], dur=0.12), t, pan=0.2, gain=0.45)
    if e['type'] == 'head_up':    put(modal([150, 280], [1.0, 0.4], [0.05, 0.03], dur=0.25), t, gain=0.5)
# music bed: soft pad + low marimba, 4 bars over the loop, fundamentals < 1 kHz
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]]; seg = DUR / 4; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.9) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + m))
        en = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.9 - t) / 0.9, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.45) * SR)) % N; np.add.at(mus, idx, s * en * 0.06)
bass = [38, 35, 31, 33]
for ci in range(4):
    for b, g in [(0, 1.0), (seg / 2, 0.6)]:
        f = note(bass[ci] + 12); s = modal([f, f * 3.9], [1.0, 0.2], [0.5, 0.1], dur=1.2, att=0.004); idx = (np.arange(len(s)) + int((ci * seg + b) * SR)) % N; np.add.at(mus, idx, s * 0.2 * g)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N)
duck = np.ones(N); va = np.abs(vo); k = int(0.25 * SR); sm = np.convolve(va, np.ones(k) / k, 'same'); duck = 1 - 0.45 * np.clip(sm / (sm.max() * 0.3), 0, 1)
L += 0.5 * mus * duck; R += 0.5 * mus * duck
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st):
    st = st / (np.abs(st).max() * 1.25); f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.stack([vo, vo], 1))
print('events', len(EV))
