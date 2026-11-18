# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "What holds an umbrella open?",
 "The ribs hang on a sleeve, the runner. Slide it up,",
 "and it meets a tiny spring catch, poking out of the tube.",
 "The catch is slanted, so the runner shoves it in.",
 "Once it passes, the spring pops the catch out. The runner sits on its flat top, so it can't slide down.",
 "To close, press the catch in. Nothing blocks the runner, so it slides down.",
 "One tiny spring catch holds the whole umbrella open.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
