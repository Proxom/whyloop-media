# p052 seatbelt retractor "WHY DOES IT / LOCK?" - track B (wordless) - group V - for Instagram 9 Nov 2026 01:00
Done: geom.py (p051 geometry, lever travel widened to -0.30..LIM), kin.js (13.0 s loop: slow pull 30 deg/s free, yank to 240 deg/s,
centrifugal lever swing from 110 deg/s, tip catches a steep tooth face at 4.227 s, hold, back-off, rewind to exactly 0),
check.js (HARD GATE 5.2: max overlap 0.014 mm, no lever/disc overlap, loop closed), scene.html, audio.py, post.json.
Rebuild: python3 -m pip install shapely; python3 geom.py; node runkin.js; node check.js
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p052/scene.html <out> 30 0 0 390 0.85 1 <w> 2
Audio: python3 audio.py; master.sh silence.wav mix_raw.wav mix.wav -60 0 -18 -> -18.2 LUFS, -3.1 dBTP, HP4k gap 39 dB.
Reviewer round 1 = 5/10 (flat mustard plate, saw-blade read, dark belt wall) -> fixes: clearcoat brass/steel, env 0.95, rim 2.2, push-in on the catch, muted dot, coarser webbing.
Reviewer round 2 = 6/10 -> scheduled. Next toolkit ideas: dark gap ring between disc and teeth, texture anisotropy 16, CTA in the yellow caption style.
Final: media/p052/seatbelt_reel_v2.mp4 + seatbelt_cover_v2.jpg (13.0 s, 1080x1920 30 fps, -18.2 LUFS).
Render paths now posts/p052 (served from repo root).
Part 2 PROMISED (caption + end frame): vehicle sensor (pendulum/ball locks the spool on hard braking) -> next 1-2 slots.
