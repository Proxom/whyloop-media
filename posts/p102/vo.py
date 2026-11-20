# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does the stick know your tire pressure?",
 "Press the gauge on. A pin opens the tire's valve, so air rushes in.",
 "The air pushes a rubber piston up the tube, and the piston pushes the stick out.",
 "But a spring pushes back. More pressure pushes it further, until the two balance.",
 "Lift it off. The spring pushes the piston back, but the stick stays, because friction holds it.",
 "So the number at the end shows your tire pressure.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
