# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why do you have to pull the mask down?",
 "The mask hangs from a cord. The cord is tied to a pin in a small can above you.",
 "That pin holds back a striker, pushed by a spring.",
 "Pull the mask, and the cord yanks the pin out.",
 "Now the spring snaps the striker into a tiny cap, and that starts the chemical core.",
 "The core makes oxygen for about twelve to twenty minutes, and it flows down the tube to your mask.",
 "Pull the mask, start the oxygen.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
