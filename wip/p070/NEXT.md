# p070 click pen "HOW DOES A PEN / CLICK?" - track A (Kokoro af_heart VO) - group E - scorecard #3 - for Instagram 19 Nov 2026 17:00
topic key: click pen - not in learnings/topics-used.md (checked 69 rows; no pen/retractable/click-pen row).
Built from kit/kit.js (materials, backdrop, light rig, text style, spring part) + a new wrapped-cylinder helper (wrapPoly, scene.html) for cam teeth.
Done: kin.py (push-push rotating cam in the unrolled plane: 8 ridge cells of 45 deg alternating short ledge / long slot, plunger sawtooth offset T/2, cam with 4 lugs;
snap on press when the plunger is below Y0 - h/2, slide on release; 4 clicks = 180 deg = loop), check.py PASS (all 4 lugs vs ridges + plunger, every 1/60 s row, 0 overlaps, rest rows touching),
scene.html, vo.py (8 lines), audio.py + master (-15.1 LUFS, -3.1 dBTP, HP4k gap 19.9 dB), post.json (spellchecked: only Hammack, UMA, hq flagged = names).
Facts: Wikipedia Retractable pen; Make: (Hammack); Pen Vibe; UMA Technology (search excerpts read this run; wikipedia.org fetch blocked by the network policy).
Rebuild: venv(kokoro-onnx numpy soundfile shapely pyspellchecker): python3 kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p070/scene.html <out> 30 1 0 768 0.75 0 0 1 1080 1920 1 (~1.1-1.3 s/frame)
then tools/render/encode.sh <out> wip/p070/mix.wav pen_reel.mp4 25.6 30
Left: final render (started ~05:27 UTC) -> encode -> HARD GATE -> clarity gate + ONE visual review -> schedule 19 Nov 17:00.

STATUS (18 Nov 05:07 run, end ~06:45 UTC): NOT SCHEDULED - CLARITY GATE not passed yet (3 tests). 19 Nov 17:00 is EMPTY -> the 13:07 run continues p070 FIRST.
- v1: HARD GATE PASS; visual 5/10 -> 3 fixes applied once (shadow bias/normalBias, roughness, step plates, hook framing). No re-score (rule).
- Clarity test 1 (v1): explanation correct, 14yo NO (label pile-up, word mismatch, tip never visible, which spring). Fixed in v2.
- Clarity test 2 (v2): explanation correct, 14yo NO (WHY slot = tip in not said). Fixed in v3: VO line 6 "The slot is deep, so the spring lifts the ink. Tip in.", rise arrow, grey cam body, cyan button teeth, badge right.
- Clarity test 3 (v3 = wip/p070/pen_reel_v3.mp4, HARD GATE technical+audio PASS: 25.6 s, -15.0 LUFS, -3.0 dBTP, gap 20.1 dB): explanation correct, 14yo NO.
TODO for v4 (one render ~21 min at 1.1 s/frame, then clarity test 4):
 1. ONE word for the turning parts: VO line 3 -> "Push: the button's teeth shove the cam down and turn it." ; labels 'BUTTON TEETH' (cyan) only; ridges = 'RIDGES' only for the barrel; drop "slanted teeth" wording.
 2. Remove the 'BUTTON SPRING' tag (it makes viewers think that spring lifts the ink). During 18.8-21.6 add a small 2D inset (like penBadge) of the BOTTOM spring stretching as the ink rises, or extend penBadge with the spring drawn.
 3. A 2-s flat "unrolled ring" strip (2D overlay, ~5.0-7.0 s or during the 14.7-15.8 pan): alternating SHORT LEDGE (yellow) / LONG SLOT (cyan) cells with the cam block stepping one cell per click; use LONG SLOT everywhere (VO line 6 -> "The slot is long, so the spring lifts the ink. Tip in.").
 4. SHORT LEDGE pointer: draw a yellow outline on the ledge corner (overlay polyline from pw() points) instead of a dot on the grey wall; same for LONG SLOT (outline the slot).
 5. Keep labels out from under the TIP badge (check 1.5-4.5 'TIP: OUT' wide tag, 5.5 spring tag, 13.0 / 18.0 slide pills): move the slide pills left (x - 150).
