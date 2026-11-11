# p061 bike quick release "WHY DOES IT / STAY SHUT?" - track B (wordless) - group V - for Instagram 12 Nov 2026 01:00
Done: kin.py (eccentric cam E 1.1 / R 7 on the rod-end pin; lever gamma 95 -> 0 deg from the wheel plane, cam beta = 188 - gamma; body touches the dropout at gamma 70
(4.8 s), peak at gamma 8 (9.4 s), snap home 9.62 s (closed squeeze 98 % of peak = over the top), tug 10.8-11.5, pull open 12.6-14.4; loop 17 s), check.py (cam-face 0.02 mm, lever clear of fork/body),
scene.html, audio.py (-18.2 LUFS, -3.1 dBTP, HP4k gap 48.9 dB), post.json (copy spellchecked; Sheldon Brown + Park Tool + US 8,905,492).
Rebuild: python3 kin.py && python3 check.py && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 0 0 -18
Render: python3 -m http.server 8765 (repo root); 3 workers: node tools/render/render.js wip/p061/scene.html <out> 30 1 0 510 1 1 <w> 3 1080 1920 1 (~2.5 s/frame effective, ~21 min)
Left: final render -> encode -> HARD GATE -> review -> schedule 12 Nov 01:00.
