# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does the needle know your speed?",
 "Behind the dial, a cable from the wheels spins a magnet.",
 "Around it sits an aluminum cup. They never touch.",
 "The spinning magnet stirs up tiny electric currents in the cup, and they drag it along.",
 "A thin spring pulls back, so the cup only turns a little.",
 "Drive faster, the magnet spins faster, the drag gets stronger, and the needle climbs.",
 "A spinning magnet moves the needle without ever touching it.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
