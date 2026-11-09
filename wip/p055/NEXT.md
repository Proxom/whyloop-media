# p055 door latch "WHY DOES IT / CLICK?" - track A (Kokoro af_heart VO) - group E - NOT SCHEDULED (visual 4/10 after 2 rounds)
Done: kin.py (latch bolt 12.8 wide, 46 deg slant toward the closing side, throw 12 -> 1 mm, door on a hinge 800 mm away, strike hole 1.0 mm play;
contact 4.01 s, snap 6.34 s, door on the stop 6.40 s, flat side holds 8.38 s at d=0.99 mm, handle 10.0-12.35 s, loop closed), check.py (overlap ~0),
scene.html (outside view with lever -> upper half fades 2.45-3.4 -> top section -> back 12.55-13.45), vo.py, audio.py (-15.2 LUFS, -2.9 dBTP, HP4k gap 19.6 dB).
Facts verified (post.json sources): Wikipedia Latch, US 4,854,618, Inspire Hardware door latch parts. Caption/comment/alt text spellchecked.
Rebuild: python3 kin.py && python3 check.py; <kokoro venv>/python vo.py <ttsdir> vo; python3 audio.py vo; tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p055/scene.html <out> 30 0 0 450 1 1 0 1 1080 1920 (2.4-3.8 s/frame, 22-28 min)
Media: media/p055/door_latch_reel_v2.mp4 + door_latch_cover_v2.jpg (technical + audio + mechanism gate PASS).
Review: round 1 = 4/10 (tiny bolt in hook, wandering transition, hatch aliasing, flat materials, too few labels) -> fixed;
round 2 = 4/10 (flat 'CAD' materials, hook subject small / 20% frame shows only the door face, label at 12 s while the bolt is still in).
Visual defects still open (HARD GATE 5.6 look, must be fixed before any use): striped z-fighting near the spindle/retractor under the section (y~1530 and 1770-1860),
last spring coil enters the bolt's back by the wire radius (end the helix 0.8 mm short), faint dashed seam lines across the door in the hook frame.
AGENT 6: 4 or lower after round 2 = concept wrong -> do not polish; next run makes a SIMPLER object (E 2/3 still free, track A) for 10 Nov 17:00.
Keep this as a reserve only if a later toolkit pass fixes the defects and it scores 6+.
