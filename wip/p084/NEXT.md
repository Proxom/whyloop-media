# p084 single-lever mixer tap "ONE LEVER: / HOT OR COLD?" - track A (Kokoro af_heart, speed 1.15) - group E - NOT YET SCHEDULED (19 Nov 15:10 run, fork)
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
Render: render.js wip/p084/scene.html <out> 30 1 0 798 0.75 0 0 1 1080 1920 1 (0.28 s/frame, ~4 min); encode.sh <out> wip/p084/mix.wav mixer_reel_v1.mp4 26.6 30
Rebuild: venv python kin.py; vo.py <ttsdir> vo; audio.py; bash master_p084.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15; mkpost.py
LEFT: CLARITY GATE + ONE visual review (fork cannot spawn reviewers; inputs in the session scratchpad p084/clar and p084/qc). Rule B after the visual score.
Known weak spots: the control disc is see-through (x-ray, reviewer of p079 disliked transparency); the lever stem crosses the pocket in the top view during the swing; the overlap at full lift is small (about half of each hole).
