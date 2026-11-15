# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv>/python vo.py <ttsdir> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "Why do you spin a combination lock three times first?",
 "Behind the dial hide three loose wheels. Each one has a notch.",
 "A latch rests on top. It can only drop when all three notches line up.",
 "Turn right. A pin on the dial catches wheel one.",
 "Wheel one's pin catches wheel two. Then wheel two catches wheel three.",
 "Three spins, three wheels picked up.",
 "Stop at the first number. The back wheel's notch is now under the latch.",
 "Turn left two turns. The back wheel stays put, and the pins pick up the other two.",
 "Stop at the second number. The middle notch lines up.",
 "Turn right to the last number. The front notch lines up.",
 "All three notches line up. The latch drops in, and the lock opens!",
 "Each spin picks up one more wheel.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.08, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info, indent=0))
