# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why does a tiny clipper cut so hard?",
 "Press the lever, and the jaws snap shut.",
 "It's really two levers, one on top of the other.",
 "The top lever turns on the pin. Your thumb is far from it, the push is close to it, so the push is eight times stronger.",
 "That push bends the top jaw down. It loses a little on the way, so the blades still get six times your thumb.",
 "The two sharp edges meet, and the nail is cut.",
 "Two levers. Six times the force.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
