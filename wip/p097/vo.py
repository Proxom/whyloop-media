# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a pepper grinder crush pepper?",
 "Inside, a grooved steel cone turns inside a grooved ring.",
 "The gap between them is wide at the top, and narrow at the bottom.",
 "So each peppercorn gets cracked into smaller and smaller pieces as it goes down.",
 "Only bits smaller than the bottom gap can fall out.",
 "Tighten the knob, and the cone moves up into the ring. Smaller gap, finer pepper.",
 "A narrowing gap crushes the pepper.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
