# p065 snap mousetrap "WHAT HOLDS / IT BACK?" - track B (wordless) - group E - for Instagram 15 Nov 2026 01:00
Done: kin.py (Hooker US 528,671 layout: coil axis A (0,14.5), jaw crossbar R 38.2, locking bar 60 mm from the rear staple P (-47.5,11.2),
tip under the catch lip (1.0 mm overlap) on the trigger hinged at Q (13,12); release when the press tilts the trigger 9.0 deg;
pencil eraser presses the cheese 10.9-12.05 s; slow-motion swing 12.05-12.85 s, jaw pins the pencil at 27.9 deg; bar rides the
crossbar, flips and falls back on the tilted catch 13.39 s; loop 18 s with a dissolve back to the set pose 16.7-18.0),
check.py PASS (bar-lip 0.05 mm, crossbar-pencil 0.05 mm, crossbar-base 0.01 mm), scene.html (hook 3/4 -> 3/4 jaw/spring ->
bar -> side macro of tip + lip -> press -> wide slow-motion snap -> payoff -> follow -> dissolve), audio.py (-18.1 LUFS, -3.1 dBTP, HP4k gap 49.6 dB),
post.json (copy spellchecked: only handle/hashtag flags; sources Hooker patent + Wikipedia Mousetrap, opened 14 Nov 13:15).
Rebuild: python3 kin.py && python3 check.py && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 0 0 -18
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); 3 workers: node tools/render/render.js wip/p065/scene.html <out> 30 0 0 540 1 1 <w> 3 1080 1920 1
then tools/render/encode.sh <out> wip/p065/mix.wav mousetrap_reel.mp4 18 30
Left: final render -> encode -> HARD GATE -> clarity gate + visual review -> schedule 15 Nov 01:00.
