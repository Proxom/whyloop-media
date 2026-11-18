# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a pen click?",
 "Click, it's out. Click, it's in. The same push every time.",
 "Inside, a spring pushes the ink up. A little cam sits on top.",
 "Push: the button's teeth shove the cam down and turn it.",
 "Let go: it lands on a short ledge and can't go up. Tip out.",
 "Push again: it turns once more, into a long slot.",
 "No ledge here, so the spring lifts the ink. Tip in.",
 "Every click turns the cam. Ledge: out. Slot: in.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
