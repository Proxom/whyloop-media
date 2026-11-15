# p066 combination padlock "WHY SPIN IT / 3 TIMES?" - track A (Kokoro af_heart VO) - group E - 1M+ list #5 - for Instagram 15 Nov 2026 17:00
Done: kin.py (3 wheels + drive cam; pin/fly play 360 - 21.7 deg; right 1215 deg to 15 (pickups 12.84/15.36/17.88 s), left 900 deg to 35 (27.78/29.99), right 450 deg to 5 (37.68);
gates set so all line up at the end; bell-crank latch solved with shapely (tooth drops 38.93-39.11 s, hook leaves the shackle groove, shackle pops 39.08 s); LOOP 48.8 s with a dissolve from 47.3),
check.py PASS (pin/fly never overlap, lever rests on the rims until the line-up, lever-wheel gap >= 0.03 mm, drop monotonic, hook out by 2.2 mm > 1.1 groove),
scene.html (locker hook -> ghosted body 3.1-4.4 -> side 3/4 view; pickups marked at the pin/fly contact; notch status chips; latch close-up; body back at 39.9-40.8; payoff; follow; dissolve),
vo.py (12 lines), audio.py + master: -15.0 LUFS, -3.1 dBTP, HP4k gap 19.4 dB. post.json spellchecked (flag: whyloop only).
Facts: Wikipedia Rotary combination lock + Combination lock, HowStuffWorks (opened 15 Nov 05:15 via Parallel fetch).
Rebuild: venv(kokoro-onnx 0.6.1 numpy soundfile shapely pyspellchecker): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); 3 workers: node tools/render/render.js wip/p066/scene.html <out> 30 1 0 1464 0.7 1 <w> 3 1080 1920 1 (~1.5 s/frame effective, ~37 min)
then tools/render/encode.sh <out> wip/p066/mix.wav lock_reel.mp4 48.8 30
Left: final render -> encode -> HARD GATE -> clarity gate + visual review -> schedule 15 Nov 17:00.
