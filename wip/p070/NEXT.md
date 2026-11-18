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
