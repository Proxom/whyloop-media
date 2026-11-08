# Kokoro-82M q8 (Apache-2.0) voiceover, one wav per line. usage: <venv python> vo.py <ttsdir with model_q8.onnx + voices.npz> <outdir>
import sys, json, soundfile as sf
from kokoro_onnx import Kokoro
TTS = sys.argv[1]; OUT = sys.argv[2]
LINES = [
 "What locks your seatbelt when the car brakes hard?",
 "Brake, and this little pendulum swings forward.",
 "It tips a pawl into the teeth. Locked.",
 "Sit back, the belt goes slack, and it lets go.",
 "Follow for a new machine every day.",
]
k = Kokoro(f'{TTS}/model_q8.onnx', f'{TTS}/voices.npz')
info = []
for i, L in enumerate(LINES):
    s, sr = k.create(L, voice='af_heart', speed=1.0, lang='en-us')
    sf.write(f'{OUT}/vo{i}.wav', s, sr); info.append({'i': i, 'text': L, 'dur': round(len(s) / sr, 3)})
json.dump(info, open(f'{OUT}/vo.json', 'w'), indent=1); print(json.dumps(info))
