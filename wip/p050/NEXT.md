# p050 reversible ratchet (Part 2 of p048) - track B (wordless) - for 8 Nov 01:00
Done: geom.py (symmetric 24-tooth gear, rocking double-nose pawl, head/pocket, shapely), kin.js (one-loop collision sim with
mode switch by a spring plunger on the reversing lever; loop 15.8 s = 2 tighten cycles, flip, 2 loosen cycles, flip back;
gear angle closes exactly, 0 penetrating frames), scene.html (from p048, served from repo root, uses tools/render/node_modules),
audio.py (clicks derived from the pawl angle, lever thunk, pad + marimba) -> tools/render/master.sh (-18 LUFS), post.json.
Rebuild: cd tools/render && npm i; python3 -m pip install shapely; cd wip/p050 && python3 geom.py && node runkin.js;
python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p050/scene.html <out> 30 1 0 474 0.85 1 <w> 3
Audio: python3 audio.py; ffmpeg anullsrc 15.8 s -> silence.wav; master.sh silence.wav mix_raw.wav mix.wav -60 0 -18
Left: final render, HARD GATE, review, schedule.
