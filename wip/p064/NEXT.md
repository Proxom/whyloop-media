# p064 four-stroke engine "HOW DOES AN / ENGINE RUN?" - track A (Kokoro af_heart VO) - group V - 17:00 1M+ list #4 - for Instagram 14 Nov 2026 17:00
Done (13 Nov 21:07 run): kin.py (slider-crank R 43 / L 145, DOHC cams at half crank speed, cam profile built from the flat-tappet lift so the cam drives the valve,
44 s loop = 10 whole cycles; slow cycle 12.0-38.3 s with 0.45x slow motion at the spark 24.1 s), check.py PASS (valve-piston >= 13 mm, rod-liner 4.7 mm, web-skirt 11 mm,
valves shut 235-480 deg, loop closes), scene.html (clip-plane cutaway with flat back-face caps, gas colour by stroke, flow particles, cycle dial "crank turn 1/2 of 2"),
vo.py (9 lines), audio.py (-15.1 LUFS, -3.1 dBTP, HP4k gap 22.6 dB), post.json (spellchecked: only hashtag/handle flags). Facts: Britannica four-stroke cycle + Wikipedia Four-stroke engine.
Rebuild: venv(kokoro-onnx 0.6.1 soundfile numpy pillow pyspellchecker): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p064/scene.html <out> 30 1 0 1320 0.8 0 <w> 2 1080 1920 1 (~20 min)
then tools/render/encode.sh <frames> mix.wav engine_reel.mp4 44 30
STATUS (13 Nov 21:07 run, end): final v2 = engine_reel.mp4 (44.0 s) + engine_cover.jpg. HARD GATE PASS, CLARITY PASS. Visual R1 4, R2 4 -> NOT scheduled (AGENT 6: concept wrong).
Reviewer R2 fixes (for a rebuild, not polish): (1) the outside does not read as an engine: build a recognisable engine (finned cylinder or inline-4, ribbed valve cover,
manifolds, pulley + belt), 3/4 hero angle filling ~80% of the height, title only in the top 20%; (2) materials: cut caps satin dark red (lit, roughness 0.6) instead of flat unlit,
opaque cast-aluminium block/head, solid polished piston (no glassy look), crank + rod one steel material, contact shadow; (3) camera closer (chamber/piston/crank ~85% width),
step titles in a fixed dark band at the top clear of the geometry, subtitles 1.3x larger, soft gas sprites instead of white beads.
14 Nov 17:00 (1M+ #4) is EMPTY: the 05:07 run must rebuild #4 with these fixes (kin.py/check.py/vo/audio are reusable; only the model, materials and camera change),
or, if the rebuild cannot reach 5+, make the next list item (#5 combination lock) for 17:00 and come back to #4.
