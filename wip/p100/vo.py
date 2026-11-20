# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does it pull the soap up?",
 "Inside: a piston, a spring, and two little balls. Each ball is a one-way door.",
 "Press down, and the piston squeezes the soap. That shuts the bottom ball and lifts the top ball, so the soap goes up and out.",
 "Let go, and the spring pushes the piston back up.",
 "That sucks on the chamber. The top ball drops shut, and the bottom ball lifts.",
 "Because the top is shut, new soap can only come up the tube.",
 "Two one-way balls: soap only goes up.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
