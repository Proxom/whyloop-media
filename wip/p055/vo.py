# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv python> vo.py <ttsdir with model_q8.onnx + voices.npz> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "Why does a door click shut by itself?",
 "Close it, and the frame pushes the slanted side in.",
 "Then a spring snaps it into the hole.",
 "Pull, and the flat side holds.",
 "Turn the handle to pull it back.",
 "Follow for a new machine every day.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.0, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
