# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a bike shoe click into the pedal?",
 "A metal cleat on the sole hooks under the front jaw first.",
 "Push your heel down, and the cleat pushes the spring-loaded back jaw out of the way.",
 "Then the spring snaps the jaw back over the cleat. Click. Locked in.",
 "Pulling up can't free it, because both jaws hold the cleat's ends from above.",
 "To get out, twist your heel outward. The cleat's corner pushes the back jaw open, and the shoe lifts free.",
 "Push down to click in. Twist your heel to get out.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
