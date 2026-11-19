# Kokoro-82M int8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, os, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
LINES = [
 "How does a kettle know the water is boiling?",
 "Switch it on. When it boils, it clicks off all by itself.",
 "Boiling water makes steam. A thin tube carries the steam down to the switch.",
 "There, the steam heats a strip made of two metals, joined together.",
 "When it's hot, the copper grows more than the steel, so the strip has to bend.",
 "The bending strip lifts a rod, the rod flips the switch, and the power is cut.",
 "Steam bends the strip. The strip turns it off.",
]
k = Kokoro(f'{TTS}/kokoro.onnx', f'{TTS}/voices.bin')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.12, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
