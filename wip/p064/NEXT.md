# p064 four-stroke engine "HOW DOES AN / ENGINE RUN?" - track A (Kokoro af_heart VO) - group V - 17:00 1M+ list #4 - for Instagram 14 Nov 2026 17:00
Done (13 Nov 21:07 run): kin.py (slider-crank R 43 / L 145, DOHC cams at half crank speed, cam profile built from the flat-tappet lift so the cam drives the valve,
44 s loop = 10 whole cycles; slow cycle 12.0-38.3 s with 0.45x slow motion at the spark 24.1 s), check.py PASS (valve-piston >= 13 mm, rod-liner 4.7 mm, web-skirt 11 mm,
valves shut 235-480 deg, loop closes), scene.html (clip-plane cutaway with flat back-face caps, gas colour by stroke, flow particles, cycle dial "crank turn 1/2 of 2"),
vo.py (9 lines), audio.py (-15.1 LUFS, -3.1 dBTP, HP4k gap 22.6 dB), post.json (spellchecked: only hashtag/handle flags). Facts: Britannica four-stroke cycle + Wikipedia Four-stroke engine.
Rebuild: venv(kokoro-onnx 0.6.1 soundfile numpy pillow pyspellchecker): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p064/scene.html <out> 30 1 0 1320 0.8 0 <w> 2 1080 1920 1 (~20 min)
then tools/render/encode.sh <frames> mix.wav engine_reel.mp4 44 30
