# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "How does a car engine really run?",
 "Burning fuel can only push. But the wheels need to spin.",
 "Inside, a piston slides in a cylinder. A rod links it to the crankshaft.",
 "One: intake. The intake valve opens, and the piston pulls in fuel and air.",
 "Two: compression. Both valves close, and the piston squeezes the mixture.",
 "Three: power. The spark plug fires!",
 "The burning gas pushes the piston down, hard. That push turns the crankshaft.",
 "Four: exhaust. The exhaust valve opens, and the piston pushes the burnt gas out.",
 "Spark, push, and the crankshaft spins. Again and again.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.05, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
