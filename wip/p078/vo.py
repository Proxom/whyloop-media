# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a bike pump push air only into the tire?",
 "Push down, and air goes in. Pull up, and none comes back out.",
 "The secret is the soft rubber cup on the end of the piston.",
 "Pulling up, its thin edge bends inward, so outside air slips past it into the pump.",
 "Pushing down, the trapped air presses the edge out against the wall. It seals, so the air can only go into the tire.",
 "Then the tire's valve shuts, so the air can't come back.",
 "The soft cup lets air in. Then it seals and pushes.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
