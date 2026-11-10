# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "You move the gear lever. What happens inside the gearbox?",
 "This gear spins freely on the shaft, and faster than it.",
 "The sleeve turns with the shaft. The fork slides it.",
 "Without the brass ring, the sleeve hits teeth spinning at a different speed.",
 "Grind!",
 "So first, the sleeve presses the brass synchro ring onto a cone on the gear.",
 "Friction slows the gear, until both spin at the same speed.",
 "Now the sleeve slides over the dog teeth.",
 "Locked. Now the gear turns the shaft.",
 "The brass ring matches the speeds first. No grind.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.0, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
