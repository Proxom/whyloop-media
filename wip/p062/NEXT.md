# p062 car differential "TWO WHEELS. / TWO SPEEDS?" - track A (VO) - group V - 17:00 1M+ list #3 - target Instagram 12 Nov 2026 17:00
Done: kin.py (open diff: thR = c + d, thL = c - d; ring/pinion 41/11, side/spider 16/10 straight bevels on common apexes; gear phases solved),
check.py (mesh offset vs half pitch over the loop <1.7 % pitch = chord noise, constant -> no drift; L+R = 2c; 0.35/0.35, 0.263/0.438, 0/0.70 rev/s),
scene.html (ghost car turn + wheel tracks, skid, cutaway, ring/pinion/driveshaft, spiders/pin, side gears, locked cutaway camera for steps 1-3 + wheel dials, payoff, loop),
vo.py (Kokoro af_heart, speed 1.05), audio.py + master (-15.1 LUFS, -3.0 dBTP, HP4k gap 21 dB), post.json (copy spellchecked; Britannica, MIT 2.972, tec-science, Counterman).
Rebuild: venv(kokoro-onnx soundfile numpy pillow): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p062/scene.html <out> 30 1 0 1260 0.8 0 <w> 2 1080 1920 1 (~19 min; AO off, scale 0.8: AO/1.0 = 38-55 min)
then python finalize.py <frames> <fin>; tools/render/encode.sh <fin> mix.wav differential_reel.mp4 42 30
Reviews: visual R1 4 -> R2 5 (max 2 rounds reached); reference R1 5.0 -> R2 6.2; clarity R1 fail, R2 fail (14yo no: "don't spin" vs revolving spiders), R3 fixes rendered.
