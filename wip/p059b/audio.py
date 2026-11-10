# p059b audio (track A): Kokoro VO placed on its steps + music bed + mechanical sounds from the same timeline as the picture (events.json).
# writes vo_stem.wav and bed_stem.wav (48 kHz stereo, LOOP s, seamless). All SFX fundamentals < 1 kHz, low-passed; no beeps/chimes/hiss.
import json, wave, numpy as np, soundfile as sf
TL = json.load(open('geom.json')); SR = 48000; DUR = TL['LOOP']; N = int(SR * DUR); rng = np.random.default_rng(591)
VO_AT = [0.3, 5.6, 9.0, 12.4, 16.0, 19.4, 23.4, 28.0, 30.45, 34.5]   # each sentence on its step (Locked. lands 0.5 s after the lock clunk)
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
# ---- VO ----
vj = json.load(open('vo/vo.json'))
for d, t in zip(vj, VO_AT):
    s, sr = sf.read(f"vo/vo{d['i']}.wav"); s = s if s.ndim == 1 else s.mean(1)
    if sr != SR: s = np.interp(np.arange(int(len(s) * SR / sr)) / SR, np.arange(len(s)) / sr, s)
    assert t + len(s) / SR < DUR; put(s, t, dst=V)
for a, b in zip(VO_AT, VO_AT[1:]): pass
ends = [t + d['dur'] for d, t in zip(vj, VO_AT)]; assert all(e < s2 for e, s2 in zip(ends, VO_AT[1:])), 'VO overlap'
# ---- SFX ----
EV = json.load(open('events.json'))
for e in EV:
    if e['type'] == 'select':  # lever moves across the gate: soft low thud
        put(modal([120, 240], [1.0, 0.3], [0.06, 0.03], dur=0.25, att=0.004), e['t'], pan=-0.1, gain=0.35)
    if e['type'] == 'push': put(modal([210, 420, 640], [1.0, 0.35, 0.2], [0.06, 0.03, 0.02], dur=0.3, att=0.002), e['t'], pan=0.1, gain=0.55)
    if e['type'] == 'rub':
        n = int((e['t1'] - e['t0']) * SR); u = np.arange(n) / n; sp = np.clip(u / 0.06, 0, 1) * (1 - u) ** 1.3; put(bandnoise(n, 140, 650) * sp, e['t0'], pan=-0.05, gain=0.12)
    if e['type'] == 'align': put(modal([520, 860], [1.0, 0.3], [0.015, 0.008], dur=0.12), e['t'], gain=0.35)
    if e['type'] == 'lock':
        put(modal([130, 260, 410], [1.0, 0.5, 0.25], [0.12, 0.06, 0.03], dur=0.5, att=0.003), e['t'], gain=0.85)
        put(bandnoise(int(0.03 * SR), 200, 1000) * env(int(0.03 * SR), 0.0008, 0.006), e['t'], gain=0.22)
    if e['type'] == 'release': put(modal([150, 300], [1.0, 0.4], [0.08, 0.04], dur=0.4, att=0.003), e['t'], gain=0.4)
    if e['type'] == 'crash':  # GRIND: rough low rattle (teeth butting 14x per second) + low rumble bed, all below ~1 kHz
        n = int((e['t1'] - e['t0'] + 0.3) * SR); u = np.arange(n) / SR; envc = np.clip(u / 0.02, 0, 1) * np.exp(-u * 0.5) * np.clip((e['t1'] - e['t0'] + 0.3 - u) / 0.3, 0, 1)
        put(bandnoise(n, 90, 800) * envc * (0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 14 * u))), e['t0'], gain=0.38)
for ti in TL['IMPACTS']: put(modal([170, 330, 560, 780], [1.0, 0.6, 0.35, 0.15], [0.05, 0.03, 0.02, 0.012], dur=0.12, att=0.001), ti, pan=rng.uniform(-0.2, 0.2), gain=0.42)
# dive inside the gearbox: low swell (no hiss), 3.4-5.6 s
n = int(2.2 * SR); u = np.arange(n) / n; put(bandnoise(n, 60, 380) * np.sin(np.pi * u) ** 2, 3.4, gain=0.10)
# ---- music bed: 8 bars over the 42 s loop (D major-ish, warm, low register) ----
def note(m): return 440 * 2 ** ((m - 69) / 12)
chords = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]] * 2; seg = DUR / 8; mus = np.zeros(N)
for ci, ch in enumerate(chords):
    for m in ch:
        f = note(m); n = int((seg + 0.9) * SR); t = np.arange(n) / SR; s = (np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + m))
        en = np.clip(t / 0.9, 0, 1) * np.clip((seg + 0.9 - t) / 0.9, 0, 1); idx = (np.arange(n) + int((ci * seg - 0.45) * SR)) % N; np.add.at(mus, idx, s * en * 0.06)
bass = [38, 35, 31, 33] * 2
for ci in range(8):
    for b, g in [(0, 1.0), (seg / 2, 0.6)]:
        f = note(bass[ci] + 12); s = modal([f, f * 3.9], [1.0, 0.2], [0.5, 0.1], dur=1.2, att=0.004); idx = (np.arange(len(s)) + int((ci * seg + b) * SR)) % N; np.add.at(mus, idx, s * 0.2 * g)
for ci, ch in enumerate(chords):
    for q in range(8):
        f = note(ch[q % 4] + 12); s = modal([f, f * 4.0], [1.0, 0.12], [0.18, 0.04], dur=0.5, att=0.003); idx = (np.arange(len(s)) + int((ci * seg + q * seg / 8) * SR)) % N; np.add.at(mus, idx, s * 0.045)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1100) ** 4); mus = np.fft.irfft(M, N)
# duck the music a little under the grind so the problem reads
tt = np.arange(N) / SR; duck = 1 - 0.5 * np.clip(np.minimum((tt - 15.8) / 0.1, (17.9 - tt) / 0.3), 0, 1); mus *= duck
L += 0.55 * mus; R += 0.55 * mus
def reverb(x, sec=0.6, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h))) * 1.6
L = reverb(L); R = reverb(R)
def wr(p, st):
    st = st / (np.abs(st).max() * 1.25); f = wave.open(p, 'wb'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR); f.writeframes((st * 32767).astype(np.int16).tobytes()); f.close()
wr('bed_stem.wav', np.stack([L, R], 1)); wr('vo_stem.wav', np.stack([V, V], 1))
print('VO ends', [round(e, 2) for e in ends])
