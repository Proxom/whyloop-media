# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a spinning wheel light the lamp?",
 "The tire spins a small roller. The roller is tiny, so it spins really fast.",
 "Inside, the roller turns a magnet, right in the middle of a coil of copper wire.",
 "As the magnet's poles sweep past the coil, they push electricity through the wire, to the lamp.",
 "Ride faster: the magnet spins faster, so the light gets brighter. Stop, and it goes dark.",
 "Your legs spin the magnet, and the spinning magnet turns that motion into electricity.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
