# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "Where does a lighter's spark come from?",
 "Roll the wheel, and sparks fly out and light the gas.",
 "Inside, a spring pushes a little rod, called the flint, up against the wheel.",
 "The wheel's edge is rough steel, so as it turns, it scrapes tiny bits off the flint.",
 "But the flint isn't stone. It's a special metal that catches fire very easily.",
 "Scraping makes the bits hot enough, so they burn in the air. Those are the sparks.",
 "The wheel scrapes the flint. The bits catch fire.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
