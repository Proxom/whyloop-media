# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why is there a tiny hole in a plane window?",
 "The window is three panes: inner, middle and outer.",
 "Up high, the cabin air pushes hard to get out.",
 "The tiny hole lets cabin air into the gap behind the middle pane.",
 "Now the middle pane has the same push on both sides, so only the outer pane takes the load. The middle one is the backup.",
 "The hole also lets moisture out, so the window doesn't fog up.",
 "One tiny hole: the outer pane does the work.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
