# p076 audio (track A): Kokoro VO + soft music bed + a low wheel rasp that follows the wheel speed (band noise 250-1300 Hz, no hiss),
# a low flame roar + whump when the gas catches, soft tocks on the lever. No high clicks or crackle. All SFX are low-passed by the master chain.
import json, wave, numpy as np, soundfile as sf
G = json.load(open('geom.json')); SR = 48000; DUR = G['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(766)
T = G['T']; VO_AT = [T[f'vo{i}'] for i in range(7)]
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
def clack(g=1.0):
    n = int(0.04 * SR); nz = bandnoise(n, 200, 1200) * np.exp(-np.arange(n) / SR / 0.006)
    s = modal([310, 520, 180], [1.0, 0.45, 0.6], [0.03, 0.018, 0.05], dur=0.22, att=0.0012); s[:n] += 0.5 * nz; return s * g
def tock(f0=420, g=1.0): return modal([f0, f0 * 1.5], [1.0, 0.3], [0.025, 0.012], dur=0.15, att=0.0015) * g
KN = json.load(open('kin.json'))
kt = np.array([r[0] for r in KN]); kph = np.array([r[2] for r in KN]); kfl = np.array([r[4] for r in KN]); klv = np.array([r[3] for r in KN])
tt = np.arange(N) / SR
# wheel rasp: low-mid band noise whose level follows the wheel speed (video time), slowed sections sound darker/softer
w = np.abs(np.gradient(kph, kt)); w = np.interp(tt, kt, w); w = np.clip(w / 12.0, 0, 1)
rasp = bandnoise(N, 250, 1300) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * tt)))
L += 0.10 * rasp * w; R += 0.10 * np.roll(rasp, 211) * w
# flame: soft low roar while it burns + a low 'whump' when it catches
fl = np.interp(tt, kt, kfl); roar = bandnoise(N, 60, 420)
L += 0.07 * roar * fl; R += 0.07 * np.roll(roar, 517) * fl
def whump(g=1.0):
    n = int(0.35 * SR); t = np.arange(n) / SR; nz = bandnoise(n, 50, 300); return (nz * np.exp(-t / 0.09) * np.clip(t / 0.01, 0, 1) + 0.6 * np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.08)) * g
for tl in [T['lit1'], T['lit2']]: put(whump(), tl, pan=-0.2, gain=0.45)
# lever press: soft plastic tock
for tp in [T['roll1'] - 0.05, T['lit2'] - 0.35]: put(tock(300), tp, pan=-0.2, gain=0.3)
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
