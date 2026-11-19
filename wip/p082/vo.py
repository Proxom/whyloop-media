# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does your blinker know to turn itself off?",
 "Flick the lever up, and a notch holds it there.",
 "Inside, a hinged finger drops next to a bumpy ring on the steering shaft.",
 "Turn right, and the bump just folds the finger out of the way.",
 "Turn back, and the bump hits it from the other side, where it can't fold.",
 "So it shoves the lever out of its notch, and the blinker stops.",
 "Turning the wheel back knocks the lever home.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
