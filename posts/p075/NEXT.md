# p075 kettle auto switch-off "HOW DOES A KETTLE KNOW / IT'S BOILING?" - track A (Kokoro af_heart) - group E
topic key: kettle switch - not in learnings/topics-used.md (checked 73 rows; no kettle / bimetal / thermostat row).
Built from kit/kit.js + scene-local lathe kettle (cut open), tube handle, RBox switch housing, glass steam tube with puffs, 2-layer bimetal strip (24 segments bent as an arc), rod, rocker with contact + LED.
kin.py: strip lift 5 mm at full heat; rod stands on the strip and lifts the rocker arm (exact contact solve); toggle snaps to OFF at -2 deg; checks PASS (rod never enters the arm, contact kept while lifting).
Facts: Wikipedia Kettle (Russell Hobbs K1 1955: bimetallic strip heated through a pipe by the steam flexes and cuts the current; little steam before the boil) + Wikipedia Bimetallic strip (steel + copper, different expansion -> bends; opens/closes contacts).
v1: HARD GATE PASS; CLARITY PASS (14yo YES); VISUAL 5/10 -> top-3 fixes once (framing lower, inset bend + BENDS UP!, smaller rod arrow) -> v2 (scheduled, no re-score, rule B).
Rebuild: python3 kin.py; venv python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: render.js posts/p075/scene.html <out> 30 1 0 792 0.75 0 0 1 1080 1920 1; encode.sh <out> mix.wav kettle_reel_v2.mp4 26.4 30
Optional polish (clarity reviewer): say why only a full boil trips it; mention the contacts in the VO; label the rod before it moves; one meaning for SWITCH.
