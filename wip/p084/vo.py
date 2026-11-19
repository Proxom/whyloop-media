# p084 mixer tap. Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does one lever give you hot, or cold?",
 "Inside, two flat ceramic discs sit on top of each other.",
 "The bottom one never moves: a hot hole, a cold hole, and a way out.",
 "The top one has a pocket underneath. Water only gets in where it covers a hole.",
 "Lift the lever: the pocket slides over the holes, so more water flows.",
 "Swing it: the pocket turns over more of the hot hole, or more of the cold.",
 "One moving pocket. Two fixed holes.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
