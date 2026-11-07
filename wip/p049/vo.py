# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. Run with the tts venv python.
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "Why does a tape measure snap back?",
 "There's a hidden spring inside.",
 "Pull the tape, and the reel winds a flat coiled spring tighter and tighter.",
 "Let go, and the spring unwinds, spinning the reel to pull the tape back in.",
 "Follow for a new machine every day.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.0, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': len(s) / sr})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=1))
