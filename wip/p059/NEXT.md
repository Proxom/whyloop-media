# p059 gearbox synchro "WHY DOESN'T / IT GRIND?" - track B (wordless) - group V - 17:00 outlier #1 (urgent: 10 Nov 17:00, else 11 Nov 17:00)
Done: kin.py (involute gears 30/20 teeth m3, 24-tooth hub/ring/dog splines; shaft 5 rev/loop, gear +2 rev/loop relative, marks line up at sync end;
sleeve -2.95 mm contact, ring pushed 1 mm onto the cone, sync 4.5-7.3 s, ring turns back 7.35-7.7, engage 7.8-8.6, release 11.0-11.7, gear spin-up 11.9-12.9 behind the case),
check.py (mesh/ring/dog overlap 0, ring blocks while turned), scene.html, audio.py (-18.1 LUFS, -3.1 dBTP, gap 45.8 dB), post.json (facts: Wikipedia Manual transmission + Lesics; spellcheck clean).
Rebuild: python3 kin.py && python3 check.py && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 0 0 -18
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p059/scene.html <out> 30 1 0 420 1 1 <w> 2 1080 1920 1 (~2.2 s/frame effective, ~15 min)
Left: final render -> encode -> HARD GATE -> review -> schedule.
