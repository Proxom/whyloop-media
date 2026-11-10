# p057 gas cap "WHY DOES IT / CLICK?" - track B (wordless) - group V - for Instagram 11 Nov 2026 01:00
Done: kin.py (12 inclined teeth r 12 -> 15.5, two flexible arms r 19.2 with round nubs r 1.3; deflection = smallest outward offset
keeping 0.05 mm clearance (shapely bisection); tighten -60 deg together, seal stop 4.4 s, 3 slips/clicks 5.92/7.07/8.22 s, loosen +150 deg,
loop closes: handle 0 -> 0, body +90 deg = 3 teeth (12-fold symmetric)), check.py (0 overlap, min gap 0.05 mm), scene.html, audio.py (-18.4 LUFS, -3.1 dBTP, HP4k gap 42.7 dB).
Facts: US 5,110,003; US 7,516,867; US 2006/0283860 (post.json). Copy spellchecked (flags: hashtags, handle, overtighten/overtightening = valid words used in the patents).
Rebuild: python3 kin.py && python3 check.py && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 0 0 -18
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p057/scene.html <out> 30 0 0 450 1 1 0 1 1080 1920 (~2.7 s/frame, ~21 min)
Left: final render -> encode -> HARD GATE -> review -> schedule 11 Nov 01:00.
