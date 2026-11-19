# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why does flipping this little tab stop the glare?",
 "The mirror glass is a wedge, thicker at the top, with silver on the back.",
 "By day, the bright silver back sends the headlights straight to your eyes.",
 "The front of the glass reflects too, but only about four percent.",
 "Flip the tab, and the whole wedge tilts up.",
 "Now the bright reflection hits the roof, and only the faint front one reaches you.",
 "So headlights look dim, but you can still see them.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
