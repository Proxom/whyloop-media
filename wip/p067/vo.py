# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "How does this gate lock itself?",
 "Without a latch, a gate you push shut just bounces back open.",
 "A steel bar hangs on a pin. On the post, a catch with a ramp.",
 "Close the gate. The ramp pushes the bar up.",
 "Past the top, gravity drops it into the notch.",
 "Now pull. The bar hits the flat wall. Locked.",
 "A ramp to get in. A wall to stop it.",
 "To open it, just lift the bar.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.08, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
