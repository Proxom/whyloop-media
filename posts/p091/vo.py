# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why doesn't the blind fall when you let go?",
 "In the top rail, the cord runs between a guide and a toothed roller.",
 "Pull down, and the cord rolls it down a slanted slot. The gap opens, so the cord runs free.",
 "Let go, and the blind's weight pulls the cord back up.",
 "The cord rolls the roller up the slot, where the gap is narrow, and gets pinched.",
 "To lower it, pull toward the middle, so the cord misses the roller.",
 "A tiny rolling wedge holds the whole blind.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
