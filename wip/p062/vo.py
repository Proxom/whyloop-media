# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "How can two wheels on one axle turn at different speeds?",
 "In a turn, the outer wheel travels a longer path than the inner wheel.",
 "With a solid axle, one tire would have to skid.",
 "So in the middle, there's a differential.",
 "The driveshaft turns the big ring gear. It carries two small spider gears on a pin.",
 "Going straight, the spider gears ride along, but they don't turn on their pin. So both wheels turn at the same speed.",
 "In a turn, the road slows the inner wheel. Now the spider gears turn on their pin, and the outer wheel speeds up by the same amount.",
 "Hold one wheel still, and the other one spins twice as fast.",
 "The spider gears let one wheel slow down while the other speeds up.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.05, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
