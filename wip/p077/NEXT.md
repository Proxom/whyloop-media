# p077 fuel nozzle auto shut-off "HOW DOES THE PUMP / KNOW IT'S FULL?" - track A (Kokoro af_heart) - group E
topic key: fuel nozzle shutoff - not in learnings/topics-used.md (checked 63 rows; no fuel / gas pump / nozzle / venturi row; p057 gas cap was a different ratchet mechanism and never published).
Built from kit/kit.js: extruded handle section (passage + Venturi throat + valve pocket + diaphragm chamber + port + bores) with a grey section cap, kit spring, RBox poppet, segmented rubber diaphragm, latch balls, plunger, lever; spout TubeGeometry; filler pipe + fuel column; instanced fuel/air particles.
kin.py: level, squeeze, stem, pivot drop, diaphragm, flow, air by episode (hook: squeeze with a full tank -> trips at once; step 0: fill -> click; steps 1-4: new fill, air in, fuel covers the hole, diaphragm pulls -> latch lets go -> pivot drops 9 mm -> spring shuts the valve; end: squeeze again = hook).
Checks PASS: lever is one straight bar through pivot and stem in both states, valve never open while unlatched, air never flows with the hole covered, 3 clicks at hook / "click!" / step 4 (19.72 s vs planned 19.82 s), spout-pipe radial gap 7 mm.
Facts: Wikipedia Gasoline pump (sensing tube to a Venturi in the handle, mechanical valve closes on the pressure change) + HowStuffWorks + VST Hose note (vacuum rises -> diaphragm -> trigger disengaged). Copy spellchecked (flags: hashtags, handle, HowStuffWorks, Venturi, VST).
Audio PASS: -15.1 LUFS, -3.1 dBTP, HP4k gap 19.7 dB.
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p077/scene.html <out> 30 1 0 840 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p077/mix.wav nozzle_reel.mp4 28.0 30
Left: final render -> encode -> HARD GATE -> clarity + visual review -> schedule 22 Nov 01:00.
