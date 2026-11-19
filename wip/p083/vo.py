# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Why does this cap just click when you turn it?",
 "It's really two caps. The inner one is screwed on. The outer one is loose, held up by a spring.",
 "Between them are sloped teeth. Turn to open, and the top teeth ride up the slopes and slip off.",
 "Click. The inner cap never moves.",
 "Push down, and flat lugs drop into place. Now they lock, and both caps turn together.",
 "So small kids can't easily open it. Turning alone just slips.",
 "Closing needs no push. The steep sides catch.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
