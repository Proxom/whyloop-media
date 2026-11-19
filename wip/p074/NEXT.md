# p074 nail clipper "WHY DOES A TINY CLIPPER / CUT SO HARD?" - track A (Kokoro af_heart) - group E - scorecard #9
topic key: nail clipper - not in learnings/topics-used.md (checked 72 rows; no clipper / nail / compound lever row).
Built from kit/kit.js + scene-local extruded leaves, lever, pin, capsule finger, nail slabs.
Done: kin.py (Wikipedia Compound lever numbers: lever 1 x8 (effort 56 mm / load 7 mm, fulcrum on the pin top), lever 2 x0.75 (push 42 / blades 56 from the rear joint) = x6;
heel contact solved exactly, 65,934 clearance checks PASS: lever never enters the upper leaf, blades never pass each other, blade enters the nail only after the cut time), scene.html, vo.py, audio.py + master,
post.json (spellchecked: only whyloop/hq/howitworks/org flagged). Facts: Wikipedia Compound lever + Wikipedia Nail clipper.
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p074/scene.html <out> 30 1 0 807 0.75 0 0 1 1080 1920 1 (0.45-0.7 s/frame); encode.sh <out> wip/p074/mix.wav clipper_reel.mp4 26.9 30
STATUS (19 Nov 01:09 run): NOT SCHEDULED. HARD GATE technical PASS (26.9 s, -15.0 LUFS, -3.0 dBTP, HP4k gap 19.9 dB). VISUAL 4/10 (kit rule: 4 or lower = do not schedule). CLARITY 14yo NO.
Visual reviewer: steel reads as matte grey plastic, edges faceted; finger = plain capsule, nail = flat slab (looks like it passes the lower jaw); subject in a thin band with 40% empty frame;
 the clipped piece reads as white cubes at the blade tips; hook title over the handle; handle/finger cut at the frame edge.
Clarity reviewer: (1) 8x -> 6x has no reason: say "lever 2 is the other way round: the blades are farther from its hinge than the push, so 8 becomes 6" and animate 8x -> 6x;
 (2) one name per part: HANDLE (lever 1), TOP JAW (lever 2), PUSH only for the force between them; never "top lever"; title "HANDLE: 8X YOUR THUMB";
 (3) separate the pivot dot (pin head) from the push point (heel) with a visible SHORT bracket; mark the second pivot as "NEW PIVOT".
Next: only redo this if a later run has spare time after QUEUE is safe; it needs a better clipper model (curved, polished leaves, real fingertip) AND the script fixes above. Otherwise drop it.
