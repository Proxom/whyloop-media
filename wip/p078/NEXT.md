# p078 bike floor pump "HOW DOES AIR GO / ONLY ONE WAY?" - track A (Kokoro af_heart) - group E
topic key: bike pump - not in learnings/topics-used.md (checked 63 rows; no pump / cup seal / tire valve row; toilet fill valve and engines are different mechanisms).
Built from kit/kit.js: lathe barrel (cut), cap, rod + T-handle, alu piston holder + rebuilt lathe cup seal (lip radius 16 sealed -> 13.8 bent, drawn larger than real), wheel arc + rim + spokes, brass valve stem (cut) + core, rubber hose; air particles on an intake path (past the lip) and an outflow path (barrel -> hose -> valve -> tire).
kin.py checks PASS: piston stays inside its travel, lip never enters the wall, cup never open while pushing, tire valve never open while pulling, loop seam within 0.5 mm.
Facts: Wikipedia Bicycle pump (cupped piston seals on the forward stroke and provides its own valve; air drawn in on the up-stroke; the valve shuts on the up-stroke). Copy spellchecked (only hashtag/handle flags).
Audio PASS: -15.0 LUFS, -3.1 dBTP, HP4k gap 21.4 dB.
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p078/scene.html <out> 30 1 0 879 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p078/mix.wav pump_reel.mp4 29.3 30
Left: final render -> encode -> HARD GATE -> clarity + visual review -> schedule 22 Nov 17:00 (next empty slot after p077).

STATUS (19 Nov 05:09 run): NOT SCHEDULED. HARD GATE PASS (1080x1920 H.264 High yuv420p 30 fps, AAC, 29.3 s, no black ends, -15.0 LUFS, -3.1 dBTP, HP4k gap 21.5 dB). Final v1 = wip/p078/pump_reel.mp4.
VISUAL 4/10 (kit rule B: not scheduled). Reviewer: hook title covers the piston and the circle frames bare wall (barrel only 290 px wide); cup = flat black trapezoid (needs rubber shading + rim light, pull/push shapes clearly different); white retainer reads as plastic; hose looks broken in the wide shot, wheel has no hub; valve close-up shows no mechanism; EDGE BENDS IN / SEALED anchors sit 150 px below the lip; air dots pass through the cup.
CLARITY: FAIL (14yo NO). Lip bend not visible on pull, no arrows for air from the top around the lip, camera follows the piston so up/down is unclear, valve step static (nothing shuts), "none comes back out" is pinned on the cup then handed to the valve (script: two one-way doors), no air shown going down the hose, PISTON tag over the step-1 title, cup orange then black, last 0.5 s shows an empty barrel (piston above the frame).
Next: only redo with a stronger cup lip deformation (curl + visible gap), flow arrows, a moving valve core, and the camera framing the whole stroke.
