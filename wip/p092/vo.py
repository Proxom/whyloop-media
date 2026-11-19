# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does the needle know your speed?",
 "Behind the dial, a cable from the wheels spins a magnet.",
 "Around it sits the cup that holds the needle. They never touch.",
 "The spinning magnet makes currents in the cup. They turn it into a weak magnet that gets pulled along.",
 "A spring pulls back. The cup turns until the pull and the spring are equal, then stops.",
 "Spin faster, and the pull gets stronger, so the needle stops higher.",
 "A spinning magnet moves the needle without ever touching it.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
