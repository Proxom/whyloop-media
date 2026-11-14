# p065 audio (track B, wordless): warm music bed + low, soft mechanical sounds on the kin events. Writes bed_stem.wav and a silent
# vo_stem.wav (48 kHz stereo, LOOP s, seamless). All SFX fundamentals < 1 kHz, low-passed, soft attacks: no beeps, chimes, clinks, hiss.
import json, wave, numpy as np
G = json.load(open('geom.json')); EV = G['EV']; SR = 48000; DUR = G['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(65)
L = np.zeros(N); R = np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0):
    i0 = int(round(t * SR)); idx = (np.arange(len(sig)) + i0) % N
    gl = np.cos((pan + 1) * np.pi / 4); gr = np.sin((pan + 1) * np.pi / 4); np.add.at(L, idx, sig * gain * gl); np.add.at(R, idx, sig * gain * gr)
def env(n, att, dec): t = np.arange(n) / SR; a = np.clip(t / att, 0, 1); return np.exp(-t / dec) * a * a * (3 - 2 * a)
def modal(fr, am, de, dur=0.4, att=0.002):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f, a, d in zip(fr, am, de): s += a * np.sin(2 * np.pi * f * (1 + rng.uniform(-0.02, 0.02)) * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
    return s * env(n, att, 10)
def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
# ---- SFX ----
n = int(0.5 * SR); u = np.arange(n) / n
put(bandnoise(n, 90, 420) * np.sin(np.pi * u) ** 2, 13.3, pan=0.3, gain=0.05)                                   # pencil comes in (soft air)
put(modal([210, 330, 520], [1.0, 0.5, 0.2], [0.05, 0.03, 0.02], dur=0.25, att=0.004), EV['touch'], pan=0.25, gain=0.20)  # eraser meets the cheese: soft low tap
n = int(2.1 * SR); u = np.arange(n) / n
put(bandnoise(n, 70, 260) * np.clip(u * 3, 0, 1) * np.clip((1 - u) * 6, 0, 1), EV['touch'], pan=0.2, gain=0.06)            # slow press: low creak-free pressure swell
put(modal([180, 290, 430], [1.0, 0.45, 0.2], [0.06, 0.035, 0.02], dur=0.25, att=0.003), EV['release'], gain=0.30)          # the bar tip slips off: low wooden tick
n = int(1.2 * SR); u = np.arange(n) / n
put(bandnoise(n, 110, 520) * (u ** 1.5) * np.clip((1 - u) * 10, 0, 1), EV['release'], gain=0.16)                           # slow-motion swing whoosh
put(modal([62, 98, 150, 240], [1.0, 0.6, 0.35, 0.15], [0.45, 0.22, 0.12, 0.05], dur=1.4, att=0.005), EV['hit'], gain=0.75) # SNAP: deep wooden thock
n = int(0.35 * SR); u = np.arange(n) / n; put(bandnoise(n, 80, 600) * np.exp(-u * 9) * np.clip(u * 60, 0, 1), EV['hit'], gain=0.22)
put(modal([160, 250], [1.0, 0.4], [0.05, 0.03], dur=0.2, att=0.004), EV['bar_land'], pan=-0.3, gain=0.14)                  # bar falls back
for t0 in (2.75, 5.75, 8.6, 11.2, 13.8):                                                                                          # soft low step pulses
    put(modal([98, 147], [1.0, 0.4], [0.25, 0.12], dur=0.6, att=0.01), t0, gain=0.10)
# ---- music bed: 4 bars per 9 s, A minor-ish, warm, low register ----
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59], [40, 47, 52, 56]] * 2; seg = DUR / 8; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.8) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.23 * t + m))
        en = np.clip(t / 0.8, 0, 1) * np.clip((seg + 0.8 - t) / 0.8, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.4) * SR)) % N; np.add.at(mus, idx, s * en * 0.06)
for ci, ch in enumerate(chords):
    for q in range(8):
        f = note(ch[q % 4] + 12); s = modal([f, f * 4.0], [1.0, 0.1], [0.2, 0.04], dur=0.5, att=0.004); idx = (np.arange(len(s)) + int((ci * seg + q * seg / 8) * SR)) % N; np.add.at(mus, idx, s * 0.04)
    f = note(ch[0] - 12); s = modal([f, f * 2], [1.0, 0.3], [0.6, 0.2], dur=1.4, att=0.006); idx = (np.arange(len(s)) + int(ci * seg * SR)) % N; np.add.at(mus, idx, s * 0.16)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N)
tt = np.arange(N) / SR                                                                                                       # hush before the snap, swell after
duck = 1 - 0.55 * np.clip(np.minimum((tt - 13.9) / 0.6, (17.8 - tt) / 0.8), 0, 1); mus *= duck
L += 0.6 * mus; R += 0.6 * mus
def reverb(x, sec=0.5, wet=0.12):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st):
    st = st / (np.abs(st).max() * 1.25 + 1e-12); f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.zeros((N, 2)))
print('audio ok', DUR, 's')
