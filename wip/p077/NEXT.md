# p077 fuel nozzle auto shut-off "HOW DOES THE PUMP / KNOW IT'S FULL?" - track A (Kokoro af_heart) - group E
topic key: fuel nozzle shutoff - not in learnings/topics-used.md (checked 63 rows; no fuel / gas pump / nozzle / venturi row; p057 gas cap was a different ratchet mechanism and never published).
Built from kit/kit.js: extruded handle section (passage + Venturi throat + valve pocket + diaphragm chamber + port + bores) with a grey section cap, kit spring, RBox poppet, segmented rubber diaphragm, latch balls, plunger, lever; spout TubeGeometry; filler pipe + fuel column; instanced fuel/air particles.
kin.py: level, squeeze, stem, pivot drop, diaphragm, flow, air by episode (hook: squeeze with a full tank -> trips at once; step 0: fill -> click; steps 1-4: new fill, air in, fuel covers the hole, diaphragm pulls -> latch lets go -> pivot drops 9 mm -> spring shuts the valve; end: squeeze again = hook).
Checks PASS: lever is one straight bar through pivot and stem in both states, valve never open while unlatched, air never flows with the hole covered, 3 clicks at hook / "click!" / step 4 (19.72 s vs planned 19.82 s), spout-pipe radial gap 7 mm.
Facts: Wikipedia Gasoline pump (sensing tube to a Venturi in the handle, mechanical valve closes on the pressure change) + HowStuffWorks + VST Hose note (vacuum rises -> diaphragm -> trigger disengaged). Copy spellchecked (flags: hashtags, handle, HowStuffWorks, Venturi, VST).
Audio PASS: -15.1 LUFS, -3.1 dBTP, HP4k gap 19.7 dB.
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p077/scene.html <out> 30 1 0 840 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p077/mix.wav nozzle_reel.mp4 28.0 30
Left: final render -> encode -> HARD GATE -> clarity + visual review -> schedule 22 Nov 01:00.

STATUS (19 Nov 05:09 run): NOT SCHEDULED. HARD GATE PASS (1080x1920 H.264 High yuv420p 30 fps, AAC, 28.0 s, no black ends, -15.1 LUFS, -3.1 dBTP, HP4k gap 19.7 dB). Final v1 = wip/p077/nozzle_reel.mp4.
VISUAL 4/10 -> kit rule B: not scheduled. Reviewer: (1) green handle = stepped box ('Lego brick') -> rounded ergonomic body, hose boot, bevels, varied roughness; blue slab + black pole -> car panel, open fuel door, filler neck; gradient backdrop; 20% frame cut on the right with empty top;
 (2) spring reads as broken arcs above the section -> one coil seated between valve and cap; diaphragm = thin orange line -> thicker disc spanning the chamber, visibly linked to the latch rod; flat red/grey section faces -> shading + edge lines; air = bead chain -> translucent bubbles;
 (3) fuel = amber rod with kinks + resin pool -> smooth translucent liquid, rippling surface; step caption overlaps the housing corner (80%) and filler ring (60%); SPRING SHUTS THE VALVE label sits on its part.
Clarity review: see below (if any). Next: only redo with a better nozzle body model + kit liquid/bubble look.
CLARITY: FAIL (14yo NO). Reviewer: (1) step 2 never shows WHY flowing fuel sucks air -> show the narrow throat + "fast fuel = low pressure" and bubbles entering it; thicker animated fuel in the handle;
 (2) step 4 payoff too small: zoom on the disc, then disc up -> latch releases -> lever drops -> valve closes, grey out the fuel after the click;
 (3) exterior: no fuel visible in the opaque pipe and the lever barely moves at the click; early CLICK badge at 0.5 s comes before anything happens;
 (4) air reads as a bead chain, hole is a tiny dot, filler neck unlabeled (FUEL RISING looks like it fills the nozzle), AIR TUBE tag hits the step-1 title.
