# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "Why do handcuffs have a second lock?",
 "Inside, the arm has teeth. A spring pushes a pawl onto them.",
 "Push the arm in. Each tooth lifts the pawl, and it snaps back. Click.",
 "Pull it back, and the steep side of a tooth jams the pawl.",
 "But it can still click tighter, and too tight can hurt the wrist.",
 "So the key's small pin pushes a bolt in, right behind the pawl.",
 "Now the pawl can't lift. It can't get tighter, and it can't open.",
 "The bolt locks the pawl. No more tightening.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.0, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
