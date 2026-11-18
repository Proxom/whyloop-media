# p072 toilet fill valve "HOW DOES A TOILET / KNOW IT'S FULL?" - track A (Kokoro af_heart VO) - group E - scorecard #10 - for Instagram 20 Nov 2026 01:00
topic key: toilet fill valve - not in learnings/topics-used.md (checked 70 rows incl. p071; no toilet / ballcock / float valve row).
Built from kit/kit.js (materials, backdrop, light rig, text style, glow, RBox) + scene-local ceramic tank, bowl, brass valve (lathe along x), float arm, water box/cap/stream.
Done: kin.py (Portsmouth-style ballcock: float arm L 230, short arm 24 (ratio 9.6), seal at arm angle -15 deg, arm stop -32 deg = 7.0 mm max gap;
water level ODE dh/dt = K*max(gap, 0.5) solved so the washer seals at 19.22 s; hook = flash-forward of the seal; loop 23.8 s), checks inside kin.py PASS
(gap >= 0 = washer never passes the seat, ball inside the tank walls), scene.html, vo.py (7 lines), audio.py + master (-15.1 LUFS, -3.1 dBTP, HP4k gap 20.0 dB),
post.json (spellchecked: only whyloop/hq/howitworks flagged).
Facts: Wikipedia Ballcock + Wikipedia Lever (Firecrawl scrape this run).
Rebuild: python3 kin.py (needs vo/vo.json); venv: python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p072/scene.html <out> 30 1 0 714 0.75 0 0 1 1080 1920 1 (~0.6-1.0 s/frame alone)
then tools/render/encode.sh <out> wip/p072/mix.wav toilet_reel.mp4 23.8 30
