# p069 audio (track A): Kokoro VO on its steps + soft music bed + low mechanical sounds from kin.json
# (low engine hum all the time, a low thud when the plate clamps the disc, a short low slip rumble, a soft release). All SFX < 1 kHz; no beeps/chimes/hiss/clinks.
import json, wave, numpy as np, soundfile as sf
G = json.load(open('geom.json')); SR = 48000; DUR = G['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(691)
VO_AT = G['EV']['vo']
L = np.zeros(N); R = np.zeros(N); V = np.zeros(N)
def put(sig, t, pan=0.0, gain=1.0, dst=None):
    i0 = int(round(t * SR)); idx = (np.arange(len(sig)) + i0) % N
    if dst is not None: np.add.at(dst, idx, sig * gain); return
    gl = np.cos((pan + 1) * np.pi / 4); gr = np.sin((pan + 1) * np.pi / 4); np.add.at(L, idx, sig * gain * gl); np.add.at(R, idx, sig * gain * gr)
def env(n, att, dec): t = np.arange(n) / SR; a = np.clip(t / att, 0, 1); return np.exp(-t / dec) * a * a * (3 - 2 * a)
def modal(fr, am, de, dur=0.25, att=0.0015):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for f, a, d in zip(fr, am, de): f *= 1 + rng.uniform(-0.03, 0.03); s += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6.28)) * np.exp(-t / d)
    return s * env(n, att, 10)
def bandnoise(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
vj = json.load(open('vo/vo.json'))
for d, t in zip(vj, VO_AT):
    s, sr = sf.read(f"vo/vo{d['i']}.wav"); s = s if s.ndim == 1 else s.mean(1)
    if sr != SR: s = np.interp(np.arange(int(len(s) * SR / sr)) / SR, np.arange(len(s)) / sr, s)
    assert t + len(s) / SR < DUR - 0.8; put(s, t, dst=V)
ends = [t + d['dur'] for d, t in zip(vj, VO_AT)]; assert all(e < s2 for e, s2 in zip(ends, VO_AT[1:])), 'VO overlap'
KN = json.load(open('kin.json'))
thud = lambda: modal([85, 190, 340], [1.0, 0.4, 0.15], [0.14, 0.05, 0.03], dur=0.5, att=0.002) + 0.25 * np.pad(bandnoise(int(0.05 * SR), 60, 600) * np.exp(-np.arange(int(0.05 * SR)) / SR / 0.012), (0, int(0.45 * SR)))
clamps = [r[0] for r, q in zip(KN, KN[1:]) if q[3] == 0 and r[3] > 0]
for c in clamps: put(thud(), c, pan=0.0, gain=0.55)
# slip rumble while the disc catches up after each clamp (band 70-400 Hz, fades as speeds match)
for c in clamps:
    sl = 1.1 if c > 1 else 0.3; n = int(sl * SR); e = np.clip(1 - np.arange(n) / n, 0, 1) ** 1.5 * np.clip(np.arange(n) / (0.04 * SR), 0, 1)
    put(bandnoise(n, 70, 400) * e, c + 0.02, pan=0.0, gain=0.18)
# release: soft low 'tock' when the pedal reaches the floor (bearing on the fingers)
rel = [r[0] for r, q in zip(KN, KN[1:]) if r[1] < 0.5 <= q[1] and r[0] > 1.2]
for c in rel: put(modal([110, 240], [1.0, 0.3], [0.07, 0.03], dur=0.3, att=0.003), c, pan=0.15, gain=0.3)
# engine hum: idle-like low rumble (fundamental 42 Hz + harmonics, slow wobble), constant, loops seamlessly (integer cycles)
tt = np.arange(N) / SR; f0 = round(42 * DUR) / DUR
hum = sum(a * np.sin(2 * np.pi * f0 * h * tt + h) for h, a in [(1, 1.0), (2, 0.55), (3, 0.3), (4, 0.15)]) * (0.8 + 0.2 * np.sin(2 * np.pi * round(3 * DUR) / DUR * tt))
L += 0.05 * hum; R += 0.05 * hum
# ---- music bed: 8 bars over the loop (A minor-ish, warm, low register) ----
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[45, 52, 57, 60], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 59]] * 2; seg = DUR / 8; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.9) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + m))
        en = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.9 - t) / 0.9, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.45) * SR)) % N; np.add.at(mus, idx, s * en * 0.06)
bass = [33, 29, 36, 31] * 2
for ci in range(8):
    for b, g in [(0, 1.0), (seg / 2, 0.6)]:
        f = note(bass[ci] + 12); s = modal([f, f * 3.9], [1.0, 0.2], [0.5, 0.1], dur=1.2, att=0.004); idx = (np.arange(len(s)) + int((ci * seg + b) * SR)) % N; np.add.at(mus, idx, s * 0.2 * g)
for ci, ch in enumerate(chords):
    for q in range(8):
        f = note(ch[q % 4] + 12); s = modal([f, f * 4.0], [1.0, 0.12], [0.18, 0.04], dur=0.5, att=0.003); idx = (np.arange(len(s)) + int((ci * seg + q * seg / 8) * SR)) % N; np.add.at(mus, idx, s * 0.04)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N)
L += 0.55 * mus; R += 0.55 * mus
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st):
    st = st / (np.abs(st).max() * 1.25); f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.stack([V, V], 1))
print('VO ends', [round(e, 2) for e in ends])
