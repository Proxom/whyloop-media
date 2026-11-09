# p054 track B (wordless): soft nylon ticks on each pawl snap, a dull thunk on the lock, a muted thump on the 2nd tug,
# a soft slide rustle while the tape moves, and a warm pad + low marimba loop. All fundamentals < 1.3 kHz; seamless loop (circular mix).
import json, numpy as np, wave
SR = 48000; DUR = 13.0; N = int(SR * DUR); rng = np.random.default_rng(54)
ev = json.load(open('events.json')); kin = json.load(open('kin_240.json'))
L = np.zeros(N); R = np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0):
    i0 = int(round(t * SR)); idx = (np.arange(len(sig)) + i0) % N
    np.add.at(L, idx, sig * gain * np.cos((pan + 1) * np.pi / 4)); np.add.at(R, idx, sig * gain * np.sin((pan + 1) * np.pi / 4))
def env(n, att, dec):
    t = np.arange(n) / SR; a = np.clip(t / att, 0, 1); return np.exp(-t / dec) * a * a * (3 - 2 * a)
def modal(freqs, amps, decs, dur=0.25, att=0.0015):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f, a, d in zip(freqs, amps, decs): s += a * np.sin(2 * np.pi * f * (1 + rng.uniform(-0.02, 0.02)) * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
    return s * env(n, att, 10)
def bandnoise(n, lo, hi):
    x = rng.standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
for e in ev:
    if e['type'] == 'tick':   # plastic 'tk': short, woody, low partials
        s = modal([540, 910, 1240, 210], [1.0, 0.4, 0.15, 0.6], [0.018, 0.012, 0.008, 0.03], dur=0.12)
        n = int(0.005 * SR); s[:n] += 0.3 * bandnoise(n, 300, 1500) * env(n, 0.0006, 0.0015)
        put(s, e['t'], pan=-0.1, gain=0.6)
    else:                     # lock: dull thunk
        s = modal([120, 260, 470], [1.0, 0.55, 0.2], [0.09, 0.05, 0.03], dur=0.35, att=0.003); put(s, e['t'], gain=0.75)
s = modal([105, 230], [1.0, 0.4], [0.06, 0.04], dur=0.25, att=0.004); put(s, 8.02, gain=0.45)   # 2nd tug: muffled, nothing moves
# slide rustle proportional to tape speed
Y = np.array([k['Y'] for k in kin]); v = np.abs(np.gradient(Y) * 240); v[-3:] = v[-4]
tt = np.arange(N) / SR; vs = np.interp(tt, np.arange(len(v)) / 240, v)
rus = bandnoise(N, 150, 900) * (vs / (vs.max() + 1e-9)) ** 1.2; L += 0.06 * rus; R += 0.06 * rus
# music: pad A - F#m - D - E (3.25 s each) + low marimba, 1.2 kHz low-pass
note = lambda m: 440 * 2 ** ((m - 69) / 12)
chords = [[45, 52, 57, 61], [42, 49, 54, 57], [38, 45, 50, 54], [40, 47, 52, 56]]; seg = DUR / 4
pad = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.6) * SR); t = np.arange(n) / SR
        w = (np.sin(2 * np.pi * f * t) + 0.12 * np.sin(4 * np.pi * f * t + 1.0)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t + m))
        e = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.6 - t) / 0.9, 0, 1)
        idx = (np.arange(n) + int((ci * seg - 0.3) * SR)) % N; np.add.at(pad, idx, w * e * 0.07)
mar = np.zeros(N); bass = [33, 30, 26, 28]
for ci in range(4):
    for b, gn in [(0, 1.0), (seg / 2, 0.6)]:
        f = note(bass[ci] + 12); s = modal([f, f * 3.9, f * 9.2], [1.0, 0.25, 0.06], [0.5, 0.12, 0.04], dur=1.2, att=0.004)
        idx = (np.arange(len(s)) + int((ci * seg + b) * SR)) % N; np.add.at(mar, idx, s * 0.22 * gn)
mus = pad + mar; Mf = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); Mf *= 1 / np.sqrt(1 + (fq / 1200) ** 4); mus = np.fft.irfft(Mf, N)
L += 0.5 * mus; R += 0.5 * mus
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum())
    h = np.zeros(N); h[:n] = ir; y = np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))); return (1 - wet) * x + wet * y * 1.6
L = reverb(L); R = reverb(R)
st = np.stack([L, R], 1); st /= np.abs(st).max() * 1.25
w = wave.open('mix_raw.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes()); w.close()
print('ok', len(ev), 'events')
