# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does the gas pump know your tank is full?",
 "Squeeze, and fuel flows. Then, click! It stops all by itself.",
 "Near the tip there's a tiny hole, and a thin tube runs back to the handle.",
 "While fuel flows, it sucks air in through that hole, nonstop.",
 "When the tank is full, fuel covers the hole, so no more air can get in.",
 "Now the suction pulls on a rubber disc instead. It trips a latch, and a spring shuts the valve.",
 "Fuel covers the hole. The suction shuts it off.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
