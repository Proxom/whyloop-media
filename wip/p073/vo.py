# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does one cable squeeze both sides?",
 "Squeeze the lever. The cable pulls, and the wheel stops.",
 "The brake has two arms, one on each side of the rim.",
 "Inside the cable, a wire pulls one way, so its casing shoves back the other way.",
 "The wire drags the right arm in. The casing pushes the left arm in.",
 "Both pads pinch the rim at once, and friction stops the wheel.",
 "One pull, two arms, both sides squeezed.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
