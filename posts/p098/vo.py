# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does your car know the tank is empty?",
 "Inside the tank, a float rides on the fuel, on a hinged arm.",
 "The arm moves a small metal wiper over a resistor strip.",
 "As the fuel is used, the float sinks. The wiper slides along the strip, and the needle drops.",
 "Because now the current runs a long way through the strip. More resistance, so less current reaches the gauge.",
 "Fill it up, and the float rises. Short path, more current, back to full.",
 "A float and a resistor move the needle.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
