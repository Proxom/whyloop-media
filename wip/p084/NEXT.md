# p084 v2 single-lever mixer tap "ONE LEVER: / HOT OR COLD?" - track A (Kokoro af_heart, speed 1.15) - group E - NOT YET SCHEDULED (19 Nov 15:10 run, fork)
topic key: mixer tap cartridge - not in learnings/topics-used.md (checked 70 rows + mechanism: no ceramic disc / sliding-port valve row; toilet fill valve p072 = float valve, kettle p075 = bimetal switch: different mechanisms).
Built from kit/kit.js (backdrop, lightRig, materials chrome/black, contactBlob, TXT) + scene-local: lathe chrome mixer tap (body, tube spout, aerator, cap with red/blue dots, lever arm) over a lathe vessel basin;
water stream whose radius follows the flow and whose colour follows the hot share; cartridge (x6): black base, fixed ceramic inlet disc (extruded, hot + cold holes + outlet slot),
see-through control disc (ellipse, pocket recess on its underside + yellow pocket outline), slim chrome lever stem riding on the disc; per-frame canvas texture at the disc interface
(dim water in the inlets, bright water where the pocket uncovers them, mixed colour in the pocket, flow arrows), 2D spout inset (stream width = flow, colour = mix).
kin.py: p_world = R(theta) * (p_frame + (0, s)); inlets r 3 at (+-5, 5.2); pocket 8.4 x 16.5 (r 2.5); s 0..7 (lift), theta -32..+32 deg (swing); areas by 0.05 mm raster.
Checks PASS (HARD GATE 5.2): inlet area outside the control disc = 0 at every frame (always sealed by ceramic or the pocket); pocket never outside the control disc; s = 0 -> overlap 0 for every theta (closed);
total overlap non-decreasing with s at theta -32/0/+32 (0 -> 12.6/14.0/12.6 mm2); hot share monotonic with theta (0.02 -> 0.98); pocket always joined to the outlet when water flows (>= 36 mm2); interior hold s=0 -> no flow.
Facts: US 8,109,292 B2 (fixed inlet disc: warm + cold inlet + outlet; control disc above; tilt = amount, rotate = temperature), US 9,115,819 B2 (indentation: none covered = closed, both + outlet covered = mixing in the indentation),
Builders Squad ceramic disc guide (fixed lower disc, upper disc moved by the handle, seal by flatness, no rubber washer). Also seen: Kluber single-lever mixer white paper (lever motion split into flow + temperature via ceramic discs with holes).
Copy spellchecked (flags: howitworks, whyloop, hq).
Audio PASS: -15.0 LUFS mix (-15.1 in the mp4), -3.0 dBTP, HP4k gap 21.1 dB. SFX: low thumps on cuts and lever moves, low ceramic tocks (250-260 Hz), water = 70-450 Hz rumble following the flow; no hiss/clicks.
Render: render.js wip/p084/scene.html <out> 30 1 0 777 0.75 0 0 1 1080 1920 1 (0.29 s/frame, 223 s); encode.sh <out> wip/p084/mix.wav mixer_reel_v2.mp4 25.9 30
Rebuild: venv python kin.py; vo.py <ttsdir> vo; audio.py; bash master_p084.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15; mkpost.py

REVIEWS (v1): CLARITY GATE PASS (explanation correct, 14-year-old YES). VISUAL 5/10 -> Rule B: top 3 fixed ONCE in v2, no re-score, one re-render only.
v2 changes (geometry re-checked in kin.py, all checks PASS: inlets always sealed, closed at s=0, flow monotonic 0 -> 15.0 mm2, hot share 0.06 -> 0.94 monotonic, pocket always joined to the outlet >= 5.4 mm2):
1. water + faucet: see-through stream (opacity 0.66) + bright specular streak + two splash rings in the basin; spout/aerator/lever on the same bright chrome as the column; stone counter slab under basin and tap.
2. hook: camera lower so the headline sits ABOVE the lever; red circle on the lever end, arrow from the lower right (never over text).
3. discs: matte ceramic with slight sheen, 3 mm / 2.5 mm bevels; top disc = solid white 2D outline + 50 % ceramic (no near-invisible x-ray); pocket = yellow outline, dark 'dip' when off;
   pink rectangle + texture triangles removed -> clean dashed flow arrows: inlet -> up into the pocket -> across -> down the way-out slot (colour = mix); smiley read removed: inlets = near-side radial slots, outlet = far crescent.
Defects: grey smudges gone (exterior contact blobs now belong to EXT, interior lever stem removed); BOTTOM DISC tag moved to the left; FOLLOW bar moved to the top (y 420), off the spout; inside/outside white flashes removed (hard cuts).
Clarity fixes: flow arrows as above; 'HOLE SHUT BY CERAMIC' leader points at the cold slot under solid ceramic; LEVER inset (side view: lever tilts while a DISC bar slides; then top view: lever LEFT = HOT / RIGHT = COLD, red/blue dots like the tap cap);
lever LEFT = HOT everywhere (cap dots, exterior swing, inset, disc turn clockwise seen from above = the same rigid rotation as the lever); VO 3 'Water only flows where the pocket sits over a hole.', VO 5 'Swing it left: the pocket turns onto the hot hole. Right: onto the cold one.' (speed 1.2); length 25.9 s.
qualityAudit v2 (HARD GATE): 1080x1920 H.264 High yuv420p 30 fps, AAC 48 kHz stereo, 25.9 s (777 frames); first/last frame luma 66.5 / 63.8 (not black); audio -15.1 LUFS, -2.9 dBTP, HP4k gap 20.8 dB;
text: hook 104 px, steps 54-60 px, tags 48-54 px, inset labels 44 px, all inside the safe zones (safe_0.5s checked); 6 stills (scratchpad p084/qc2) looked at: no glitches, black frames or cut-off text.
Cover = frame at 0.4 s (mixer_cover_v2.jpg). Copy spellchecked (flags: howitworks, whyloop, hq).
Renders: v1, v2, then ONE extra v2 pass forced by the HARD GATE (my own self-check found two inset sub-labels at 30/38 px < 44 px: 'DISC' removed, LEFT = HOT / RIGHT = COLD set to 44 px); the same pass lowered the second ghost lift so the sinking top disc no longer reaches the step-3 caption, and the settle tocks were re-timed to the new disc landing.
Left open: the cold flow arrow at mid-lift is short (small overlap); the tap body chrome reads darker than the spout on the dark backdrop.
