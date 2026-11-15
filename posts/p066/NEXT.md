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

STATUS (15 Nov 05:07 run, ig-sweet-lamport-wi7v75):
v1 (lock_reel_v1.mp4 + lock_cover_v1.jpg): HARD GATE PASS (1080x1920 30 fps H.264 + AAC, 48.8 s, -15.1 LUFS / -3.0 dBTP, gap 19.3 dB, no black first/last, loop seam diff 0.26, no frame spikes except the smooth 39.7-40.0 s pull-back).
CLARITY GATE round 1 = PASS (fresh reviewer explained it correctly; 14yo YES). Visual round 1 = 5/10 (flat plastic wheels, foggy ghost housing, too tight; chip tick out of sync; ghost shackle half-disc over the latch).
Round-2 fixes DONE in code (not yet in a finished render): metal wheels (metalness 0.88 + brushed roughness), ghost body 6 %, shackle hidden in the latch close-up, wider inside camera (dist ~134),
chips in wheel order 1-2-3 + 42 px heading, a wheel only ticks when it is still (no flashing tick), chips gone before the wide open shot, pickup tags 1.5 s and anchored on the picked-up wheel's fly,
REAL DIAL DIRECTION: numbers now run clockwise on the face, so turning right counts DOWN (reviewer: a real 40-number lock reads downward) -> TH = [0, 1305, 405, 1035]; kin/check/audio re-run (check PASS, -15.0 LUFS, gap 19.5 dB).
v2 FINISHED: visual round 2 = 6 -> scheduled 15 Nov 17:00 (Metricool 428648486). Media: media/p066/lock_reel_v2.mp4 + lock_cover_v2.jpg.
IF lock_reel.mp4 in this folder is still v1 (48.8 s, dial counts UP): NEXT RUN = render v2 (command above, ~38 min) -> encode -> HARD GATE (qc_video/qc_audio + spike scan) -> visual round 2 review (6 stills) ->
  6+ = schedule 15 Nov 17:00 (move to media/p066 + posts/p066, wait for raw URL 200). Below 6 and the slot < 2 h away: schedule the best gate-passing version (5 allowed by AGENT 6). Clarity already PASSED (re-check only if the story changes).
