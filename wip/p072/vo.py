# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a toilet know it's full?",
 "Flush, and the water drops. So does this floating ball.",
 "The ball hangs on a long arm that works a valve.",
 "The ball is down, so the arm pulls the valve open. Water rushes in.",
 "As the water rises, it lifts the ball.",
 "The arm is long, so that gentle lift becomes a strong push. A rubber washer presses on the hole, and the water stops.",
 "The floating ball turns the water off.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
