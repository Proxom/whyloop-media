# p054 zip tie "WHY ONLY / ONE WAY?" - track B (wordless) - group E - for Instagram 10 Nov 2026 01:00
Done: kin.py (P 1.6, H 0.62, pawl 30 deg / L 3.55, edge-sampled clearance sim 2400 Hz, rest gap G0 0.45 > tip rise so each 1-pitch pull ticks once,
lock at 7.306 s, loop closes at exactly 11 pitches), geom.py (head = block minus slot + swept pawl pocket), check.py (shapely overlap 0.00016 mm2 = PASS),
scene.html (cover plate clip sweep 3.0-4.1 / 10.0-10.9, macro 4.7-8.9), audio.py (ticks/lock/tug/rustle + pad, -18.5 LUFS, HP4k gap 38.6 dB).
Rebuild: python3.13 kin.py && python3.13 check.py && python3.13 audio.py
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p054/scene.html <out> 30 0 0 390 1 1 0 1 1080 1920 (~2.2 s/frame)
Left: final render -> encode -> HARD GATE -> review -> schedule 10 Nov 01:00.
Round 1 final: HARD GATE pass, reviewer 4/10 (circle on blank face, wood backdrop, wide-angle taper, cover ghost edge, white pocket walls) -> fixed.
Round 2 final v2: HARD GATE pass, reviewer 5/10. Scheduled anyway (AGENT 5: only the HARD GATE blocks): Metricool 421397183, Instagram REEL 10 Nov 2026 01:00 PENDING.
Toolkit ideas from round 2: tapered real tie head, satin nylon + bevels, rim light + contact shadow, darker backdrop, visible clearance.
