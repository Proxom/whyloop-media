# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "What flips the key out?",
 "Around the pivot, a coiled spring is wound up. It always wants to swing the blade out.",
 "But the button has two little teeth. They sit in notches in the case, so the blade can't turn.",
 "Press the button, and the teeth drop out of the notches.",
 "Now nothing holds the spring back, so it snaps the blade out.",
 "The button pops back up into the notches, and locks it open.",
 "Fold it back, and the spring winds up again.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
