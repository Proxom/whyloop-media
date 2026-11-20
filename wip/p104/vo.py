# Kokoro-82M (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a flask keep coffee hot for hours?",
 "Cut it open. There are two steel walls, and the gap between them has almost no air. It's a vacuum.",
 "Heat needs something to travel through. If the gap had air, the air would carry the heat out.",
 "But a vacuum has nothing to carry it, so the heat stays in, and the outside stays cool.",
 "Shiny walls bounce heat rays back, and the lid seals the top.",
 "No air in the gap, so the heat can't get out.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.15, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
