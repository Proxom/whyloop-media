# p057 audio (track B, wordless): music bed + mechanical sounds from the same timeline as the picture (events.json).
# writes bed_stem.wav and a silent vo_stem.wav (48 kHz stereo, LOOP s, seamless). All fundamentals < 1 kHz, no beeps/chimes.
import json, wave, numpy as np
TL = json.load(open('geom.json')); SR = 48000; DUR = TL['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(59)
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
    if e['type'] == 'push':  # sleeve meets the brass ring: soft low knock
        put(modal([210, 420, 640], [1.0, 0.35, 0.2], [0.06, 0.03, 0.02], dur=0.3, att=0.002), e['t'], pan=0.1, gain=0.55)
    if e['type'] == 'rub':  # cone friction: a soft brushed rub that fades as the speeds match
        n = int((e['t1'] - e['t0']) * SR); u = np.arange(n) / n; sp = np.clip(u / 0.08, 0, 1) * (1 - u) ** 1.3; put(bandnoise(n, 140, 650) * sp, e['t0'], pan=-0.05, gain=0.09)
    if e['type'] == 'align':  # ring turns back in line: tiny low tick
        put(modal([520, 860], [1.0, 0.3], [0.015, 0.008], dur=0.12), e['t'], gain=0.35)
    if e['type'] == 'lock':  # sleeve lands on the dog teeth: solid low clunk
        put(modal([130, 260, 410], [1.0, 0.5, 0.25], [0.12, 0.06, 0.03], dur=0.5, att=0.003), e['t'], gain=0.8)
        put(bandnoise(int(0.03 * SR), 200, 1200) * env(int(0.03 * SR), 0.0008, 0.006), e['t'], gain=0.25)
    if e['type'] == 'release':  # shifting out: softer clunk
        put(modal([150, 300], [1.0, 0.4], [0.08, 0.04], dur=0.4, att=0.003), e['t'], gain=0.4)
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
# soft marimba pulse (eighths of the bar), low register
for ci, ch in enumerate(chords):
    for q in range(8):
        f = note(ch[q % 4] + 12); s = modal([f, f * 4.0], [1.0, 0.12], [0.18, 0.04], dur=0.5, att=0.003); idx = (np.arange(len(s)) + int((ci * seg + q * seg / 8) * SR)) % N; np.add.at(mus, idx, s * 0.05)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N)
L += 0.55 * mus; R += 0.55 * mus
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st, norm=True):
    if norm: st = st / (np.abs(st).max() * 1.25)
    f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.zeros((N, 2)), norm=False)
print('events', [(e['type'], e.get('t', e.get('t0'))) for e in EV])
