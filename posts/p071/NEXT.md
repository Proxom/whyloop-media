# p071 umbrella spring catch "WHAT HOLDS AN / UMBRELLA OPEN?" - track A (Kokoro af_heart VO) - group E - scorecard #5 - for Instagram 19 Nov 2026 01:00
topic key: umbrella catch - not in learnings/topics-used.md (checked 69 rows; no umbrella / runner / spring catch row).
Built from kit/kit.js (materials, backdrop, light rig, text style, glow, camera keys) + scene-local lathe tube with a catch slit, rib/stretcher linkage and a per-frame canopy mesh.
Done: kin.py (runner top yt drives the rib angle through the stretcher (L 260 from the runner collar to 200 mm along the rib); catch pushed in by
d = max(required by the runner bore 4.2 over the 2.5 mm slanted tab, thumb press); snaps 0.50 s + 11.45 s; open 72.0 deg, closed 6.0 deg; loop 24.9 s),
check inside kin.py PASS (min runner-bore-to-catch gap 0.05 mm over every 1/60 s row; runner rests ON the flat top), scene.html, vo.py (7 lines),
audio.py + master (-15.1 LUFS, -3.1 dBTP, HP4k gap 19.8 dB), post.json (spellchecked: only whyloop/hq/howitworks flagged = handle/hashtag).
Facts: US 8,459,281 + US 6,810,895 (Firecrawl scrape of patents.google.com this run; direct fetch blocked by the network policy).
Rebuild: python3 kin.py (needs vo/vo.json); venv(kokoro-onnx soundfile pyspellchecker): python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p071/scene.html <out> 30 1 0 747 0.75 0 0 1 1080 1920 1 (~0.42 s/frame, ~5 min)
then tools/render/encode.sh <out> wip/p071/mix.wav umbrella_reel.mp4 24.9 30
