# p050 reversible ratchet (Part 2 of p048) - track B (wordless) - Instagram 8 Nov 2026 01:00
Done: geom.py (symmetric 24-tooth gear, rocking double-nose pawl, head/pocket, shapely), kin.js (one-loop collision sim; a spring
plunger on the reversing lever sets which pawl end is pushed in; loop 15.8 s = 2 tighten cycles, flip, 2 loosen cycles, flip back;
gear angle closes exactly), check.js (HARD GATE 5.2: max overlap 0.0007 mm, pawl always inside pocket, plunger 6.0-7.2 mm),
scene.html (from p048; served from repo root, uses tools/render/node_modules), audio.py (clicks derived from the pawl angle,
lever thunk, pad + marimba) -> tools/render/master.sh at -18 LUFS, post.json (caption, first comment, sources, alt text).
Rebuild: cd tools/render && npm i; python3 -m pip install shapely; cd posts/p050 && python3 geom.py && node runkin.js;
python3 -m http.server 8765 (repo root); node tools/render/render.js posts/p050/scene.html <out> 30 1 0 474 0.85 1 <w> 3  (3 workers ~17 min)
Audio: python3 audio.py; ffmpeg -f lavfi -i anullsrc=r=48000:cl=stereo -t 15.8 silence.wav; master.sh silence.wav mix_raw.wav mix.wav -60 0 -18
Encode: tools/render/encode.sh <frames> mix.wav ratchet2_reel.mp4 15.8
Reviewer: round 1 = 5/10 (flat gear/housing values, aliased shadows, top-down static camera, cropped arrows) -> fixes applied.
Ideas next: brushed/bevelled housing edges, shallow depth of field, a real hex bolt under the socket turning.
