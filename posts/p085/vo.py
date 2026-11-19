# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why doesn't the air leak out of your tire?",
 "Inside the valve is a tiny door: a rubber seal on a pin.",
 "A spring pushes the seal up against its seat.",
 "And the air in the tire pushes it up too, so it seals even tighter.",
 "The pump presses the pin, and the door opens.",
 "Pump air is stronger, so it rushes into the tire.",
 "Pump off, and the tire's own air slams the door shut.",
 "The air inside holds the door shut.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
