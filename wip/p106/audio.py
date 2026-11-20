# p106 audio (pressure cooker weight, track A): Kokoro VO + soft music bed + soft LOW thumps on the real events (door shuts gently, what-if slam = bigger low thump)
# and a soft low oil rumble (70-400 Hz) only while oil is pushed through the tiny hole. No hiss, no clicks, no bells, no tones above ~1.5 kHz.
import json, wave, numpy as np, soundfile as sf
G = json.load(open('geom.json')); SR = 48000; DUR = G['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(1020)
T = G['T']; VO_AT = [T[f'vo{i}'] for i in range(6)]
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
def tock(f0=300, g=1.0): return modal([f0, f0 * 1.52, f0 * 0.5], [1.0, 0.3, 0.4], [0.03, 0.014, 0.05], dur=0.16, att=0.0015) * g
def thump(f0=110, g=1.0): return modal([f0, f0 * 1.5, f0 * 2.1], [1.0, 0.35, 0.15], [0.09, 0.04, 0.02], dur=0.35, att=0.002) * g
# p106 events (soft LOW only): a low tap each time the weight drops back on the pipe, a low steam puff (60-300 Hz) while it is lifted, soft boil rumble inside; no hiss
KN = json.load(open('kin.json')); hk = np.array([r[1] for r in KN]); tk = np.array([r[0] for r in KN])
for i in range(1, len(hk)):
    if hk[i - 1] > 0.02 and hk[i] <= 0.02: put(tock(230), tk[i], gain=0.42); put(thump(105), tk[i], gain=0.25)
for c in [T['cutIn'], T['outA'], T['ans']]: put(tock(200), c, gain=0.12)
tt = np.arange(N) / SR
lift = np.interp(tt, tk, np.clip(hk / 1.0, 0, 1))
rum = bandnoise(N, 60, 300); boil = bandnoise(N, 50, 220)
L += rum * 0.09 * lift; R += np.roll(rum, 307) * 0.09 * lift
bg = np.clip((tt - T['cutIn']) / 0.3, 0, 1) * np.clip((T['outA'] - tt) / 0.3, 0, 1) * 0.025
L += boil * bg; R += np.roll(boil, 911) * bg
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
