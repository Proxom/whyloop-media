# p067 gravity gate latch "HOW DOES IT / LOCK ITSELF?" - track A (Kokoro af_heart VO) - group E - 1M+ list #6 - for Instagram 16 Nov 2026 17:00
Done: kin.py (gate on hinge x=-900; bar lift at the catch solved with shapely: ramp lifts it, ballistic drop a=1.5g/slow^2, staple stop; hook close 6 deg, problem shot without latch (bounces to 9 deg),
slow close 10.6-16.2, pull 17.6-18.3 stops 0.3 mm from the wall, lift + open 23.6-25.6; LOOP 26.4 s), check.py PASS (no overlap, locked gap 0.3 mm, bar 14 mm under the lip top),
scene.html, vo.py (8 lines), audio.py + master (-15.0 LUFS, -3.1 dBTP, gap 19.7 dB), post.json (spellchecked: only hashtag/handle flags).
Facts: US 858,866; US 2,671,683; US 413,193 (opened 15 Nov 13:20 via Parallel fetch).
Rebuild: venv(kokoro-onnx 0.6.1 numpy soundfile shapely pyspellchecker): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); 3 workers: node tools/render/render.js wip/p067/scene.html <out> 30 1 0 792 0.7 0 <w> 3 1080 1920 1 (AO off: AO costs +65 % per frame)
then tools/render/encode.sh <out> wip/p067/mix.wav latch_reel.mp4 26.4 30
Left: final render -> encode -> HARD GATE -> clarity gate + visual review -> schedule 16 Nov 17:00.
