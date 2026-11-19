# p083 push-and-turn child-resistant cap "WHY DOES IT / JUST CLICK?" - track A (Kokoro af_heart) - group E - FINAL v2 READY, NOT SCHEDULED (19 Nov 15:10 run; coordinator holds it for Erkan's approval: possible ratchet repeat)
topic key: child-proof cap (child-resistant closure, push-and-turn cap, safety cap) - not in learnings/topics-used.md (checked 70 rows + mechanism: no child-cap / two-cap clutch row).
Repeat note: the patents call the top teeth "one-way ratchet ramps" (cousin of the ratchet wrench p048/p050); new object + new idea (two caps, a spring, and flat drive lugs that only lock when pushed). Coordinator sends the approval request.

## v2 (coordinator review of v1: CLARITY PASS, visual 6/10, mechanism-accuracy issue fixed)
Mechanism (HARD GATE 5.2) now follows the sources: a spring holds the outer cap up (G0 1.6 mm). SLOPED TEETH ring (r 5-10.5, 10 teeth, H 2.4 drawn): at rest the steep faces overlap 0.8 mm -> closing catches without a push;
turning to open the outer teeth ride up the slopes (lift to 2.4) and drop back = the click, inner cap still. FLAT DRIVE LUGS ring (r 11.5-14.5, 10 + 10 lugs, 9 deg): clear by 0.5 mm at rest; pushed (lift 0) they overlap 1.1 mm and the flat faces drive the inner cap.
New beats: spring in the exploded view; "PUSH: FLAT LUGS LOCK" (outer lugs drop beside the inner lugs, orange faces); payoff card adds "SO KIDS CAN'T EASILY OPEN IT"; step 5 "CLOSING: NO PUSH NEEDED" (cap back on, turns clockwise, steep sides catch, orange in the strip).
Strip: two lanes (SLOPED TEETH / FLAT LUGS), outer = off-white, inner = blue, dark outlines, gaps show the grey-blue panel (not black).
Look fixes: clipped outer saw ring hidden while the cutaway is open (was the garbled patch on the inner-cap top), outer lugs unclipped; stripes are thin lathe slices (no box sliver at the cut/edge); inner cap receives no shadow (no striped acne); PUSH arrow ends before the payoff card (no ghost);
hook red circle follows the orange stripe; CLICK pops removed; bottle label with blue band + small print lines.
kin.py checks PASS (every 1/120 s, 7200 angles): teeth min clearance 0.0000 (touching), lugs never overlap except side by side (clearance where they share an angle 0.500 mm), retaining lip >= 0.350 mm, inner cap only turns open while pushed, closing only on the steep faces at rest, phi frozen while pushed, loop start = end.
Facts: US 11104494 B2, US 8857638 B2 (driving/driven lugs disengaged unless pushed, spring fingers slip over ramps), US 2020/0385182 A1 (elastic members push the outer cap up), US 11279530 B2, US EPA cap sheet. URLs in post.json / first comment.
Copy spellchecked (flags: epa, howitworks, hq, whyloop = names/hashtag).
Audio PASS: -15.0 LUFS, -3.1 dBTP, HP4k gap 21.4 dB; 20 soft low ticks on the 20 tooth drops (modal 380-440 Hz, < 1.5 kHz), low tock when the lugs drop in and when closing catches, low thread rasp while both caps turn.
Technical: see qualityAudit below. Render: node tools/render/render.js wip/p083/scene.html <frames> 30 1 0 860 0.75 0 0 1 1080 1920 1 (~0.45 s/frame, ~7 min); tools/render/encode.sh <frames> wip/p083/mix.wav childcap_reel_v2.mp4 28.66 30
Rebuild: venv python kin.py; venv python vo.py <ttsdir> vo; venv python audio.py; bash master_p083.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15; python3 mkpost.py
Open for the kit: sawRing() (saw-tooth face ring), lugs() (annular sector lugs), clip-plane wedge cutaway with world-fixed section faces.
qualityAudit v2: technical PASS (1080x1920 H.264 High yuv420p 30 fps, AAC 48 kHz stereo, 28.67 s = planned 28.66, first/last frame luma 75/69, not black); mechanism PASS (kin.py); facts PASS; text PASS (all >= 44 px, nothing in the right 150 px, safe 0.5 s frame checked: hook cap above the bottom 480 px);
audio PASS (-15.0 LUFS, -3.1 dBTP, gap 21.4 dB); look PASS (6 stills in scratchpad p083/review_stills_v2 + 2-fps sheet checked: no garbled patch, no stripe sliver, no arrow ghost, no black gaps).
v1 reviews (coordinator): clarity PASS (14yo YES), visual 6/10. v2 not re-scored (rule B: one re-render). Cover: childcap_cover_v2.jpg (0.6 s hook frame).

HOLD (19 Nov 15:10 run): NOT scheduled - possible ratchet repeat, approval a-042 pending. v2 changed the story (flat lugs, closing beat, 28.7 s): run a fresh CLARITY GATE on v2 before scheduling if Erkan approves (a).
