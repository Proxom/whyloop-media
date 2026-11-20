# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why does this little tab stop the glare?",
 "The mirror glass is a wedge. It's thicker at the top, with silver on the back.",
 "In day mode, the bright silver back sends the headlights straight into your eyes.",
 "Flip the tab, and the whole wedge tilts. Now the bright silver beam misses your eyes.",
 "You only see the plain glass front. It reflects about four percent, so the lights look dim.",
 "One flip: you see the weak glass, not the bright silver.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
