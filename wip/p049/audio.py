# p049 audio: VO stem (placed on the kin.js timeline) + bed (music + SFX from kin_240.json). Circular mix -> seamless loop.
import json, numpy as np, wave, sys
SR = 48000; DUR = 18.0; N = int(SR * DUR); rng = np.random.default_rng(49)
kin = json.load(open('kin_240.json')); T = kin['T']; e = np.array(kin['e']); VOD = sys.argv[1]
def rd(fn):
    w = wave.open(fn); n = w.getnframes(); sr = w.getframerate(); x = np.frombuffer(w.readframes(n), np.int16 if w.getsampwidth() == 2 else np.int32).astype(float)
    x = x / (32768 if w.getsampwidth() == 2 else 2**31); ch = w.getnchannels(); x = x.reshape(-1, ch).mean(1)
    if sr != SR: t = np.arange(int(len(x) * SR / sr)) / SR; x = np.interp(t, np.arange(len(x)) / sr, x)
    return x
def put(buf, sig, t, gain=1.0):
    idx = (np.arange(len(sig)) + int(round(t * SR))) % N; np.add.at(buf, idx, sig * gain)
def env(n, att, dec): t = np.arange(n) / SR; a = np.clip(t / att, 0, 1); return np.exp(-t / dec) * a * a * (3 - 2 * a)
def modal(fr, am, de, dur=0.4, att=0.002):
    n = int(dur * SR); t = np.arange(n) / SR; s = sum(a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t / d) for f, a, d in zip(fr, am, de)); return s * env(n, att, 10)
def band(n, lo, hi):
    X = np.fft.rfft(rng.standard_normal(n)); f = np.fft.rfftfreq(n, 1 / SR); X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return y / (np.abs(y).max() + 1e-9)
# --- VO stem
vo = np.zeros(N); info = json.load(open(f'{VOD}/vo.json'))
for k, it in enumerate(info): put(vo, rd(f'{VOD}/vo{k}.wav'), T['vo'][k])
# --- SFX from blade speed
tt = np.arange(N) / SR; es = np.interp(tt, np.arange(len(e)) / 240, e); v = np.gradient(es) * SR  # mm/s
ret = np.clip(-v / 400, 0, 1.5); pul = np.clip(v / 120, 0, 1.5)
sfx = np.zeros(N)
sfx += 0.16 * band(N, 180, 1400) * ret ** 1.2          # blade rattle while it rewinds
sfx += 0.05 * band(N, 90, 600) * pul                   # soft drag while pulling
for th in [T['snap0'][1], T['snap1'][1]]:            # hook hits the case
    put(sfx, modal([140, 310, 520, 880], [1.0, 0.55, 0.3, 0.12], [0.09, 0.06, 0.04, 0.02], 0.5), th, 0.75)
    n = int(0.012 * SR); put(sfx, band(n, 200, 1400) * env(n, 0.0006, 0.003), th, 0.25)
for a, b in [T['coverOff'], T['coverOn']]:           # soft air swell under the cutaway sweep
    n = int((b - a + 0.4) * SR); w = np.sin(np.linspace(0, np.pi, n)) ** 2; put(sfx, band(n, 80, 700) * w, a - 0.2, 0.05)
# --- music: D - Bm - G - A, 4.5 s each (= 18 s loop), pad + low marimba, all fundamentals < 1 kHz
def note(m): return 440 * 2 ** ((m - 69) / 12)
mus = np.zeros(N); chords = [[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]]; bass = [38, 35, 31, 33]
for ci, ch in enumerate(chords):
    for m in ch:
        n = int(5.2 * SR); t = np.arange(n) / SR; f = note(m); w = np.sin(2 * np.pi * f * t) + 0.1 * np.sin(4 * np.pi * f * t + 1)
        w *= (0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t + m)) * np.clip(t / 1.0, 0, 1) * np.clip((5.2 - t) / 1.0, 0, 1); put(mus, w, ci * 4.5 - 0.35, 0.06)
    for b, g in [(0, 1.0), (1.5, 0.55), (3.0, 0.75)]:
        f = note(bass[ci] + 12); put(mus, modal([f, f * 3.9, f * 9.2], [1, 0.25, 0.05], [0.6, 0.12, 0.04], 1.4, 0.004), ci * 4.5 + b, 0.2 * g)
M = np.fft.rfft(mus); fq = np.fft.rfftfreq(N, 1 / SR); M *= 1 / np.sqrt(1 + (fq / 1200) ** 4); mus = np.fft.irfft(M, N)
# duck music under the voice (circular smoothing of the VO envelope)
ve = np.abs(vo); k = int(0.25 * SR); ker = np.zeros(N); ker[:k] = 1 / k; ve = np.real(np.fft.ifft(np.fft.fft(ve) * np.fft.fft(ker))); ve = np.roll(ve, -k // 2)
duck = 1 - 0.55 * np.clip(ve / (np.percentile(ve, 99) + 1e-9) * 2, 0, 1)
bed = mus * duck * 0.9 + sfx
def reverb(x, sec=0.8, wet=0.14):
    n = int(sec * SR); t = np.arange(n) / SR; ir = rng.standard_normal(n) * np.exp(-t / (sec / 5.5)); ir /= np.sqrt((ir ** 2).sum()); h = np.zeros(N); h[:n] = ir
    return (1 - wet) * x + wet * 1.6 * np.real(np.fft.ifft(np.fft.fft(x) * np.fft.fft(h)))
bed = reverb(bed); vo = reverb(vo, 0.4, 0.06)
C = max(np.abs(vo).max(), np.abs(bed).max()) * 1.12
def wr(fn, x):
    x = x / C; w = wave.open(fn, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
wr('vo_stem.wav', vo); wr('bed_stem.wav', bed); print('peaks vo/bed', np.abs(vo).max() / C, np.abs(bed).max() / C)
