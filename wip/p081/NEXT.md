# p081 prism pencil sharpener "HOW DOES IT MAKE / A PERFECT POINT?" - track A (Kokoro af_heart) - group E - target 22 Nov 2026 01:00 (19 Nov 10:09 run)
topic key: pencil sharpener - not in learnings/topics-used.md (checked 66 rows + mechanism: no sharpener / cone shaping / blade-shaving row; pencil only as a prop in p065).
Built from kit/kit.js (lightRig, backdrop, materials) + scene-local: clear plastic body (extruded trapezoid: right face = blade tangent plane), shaping cone + guide bore (lathe), steel blade on the tangent plane with a bright edge strip + screw,
pencil rebuilt each frame from lathe profiles (lead core, wood cone, painted barrel), fan-shaped shaving (vertex-colour ribbon) growing with the cut.
kin.py: cone half angle 11 deg, guide bore r 3.75, pencil r 3.6, lead r 1.0, 0.6 mm clearance hole; 0.75 mm advance per turn (20.6 turns); profile r(y) = min(R, rc(y)).
Checks PASS: pencil never outside the hole/cone (min clearance 0.000 = touching the cone = the blade edge), blade face never inside the pencil (tangent plane, convex), uncut pencil never inside the cone.
Facts: Wikipedia Pencil sharpener (prism type). Copy spellchecked (flags: howitworks, whyloop, hq).
Audio PASS: -15.1 LUFS, -3.1 dBTP, HP4k gap 20.4 dB.
Render: render.js wip/p081/scene.html <out> 30 1 0 730 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p081/mix.wav sharpener_reel_v2.mp4 24.3 30
Review v1: visual 5/10, clarity PASS (14yo YES). Rule B: top 3 fixed once in v2 (no re-score): no green paint stripe (read as lead) + dark graphite lead + bright blade edge; shaving comes off the blade edge in the cutting zone; tighter framing, subject left of the Reels button column, arrows out of the top zone.
Open for the kit: hex pencil facets, real slot in the body, contact shadow, show "only goes deeper once it fits" as small steps per turn.
