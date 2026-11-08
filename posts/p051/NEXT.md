# p051 bike freehub "WHY DOES IT / TICK?" - track A (Kokoro af_heart VO) - for Instagram 8 Nov 2026 17:00
Why this topic: the ratchet Reel p048 became the first winner (10.8K views, reach 7.3K) -> AGENT.md 4.9 close variant (same pawl + sawtooth idea).
Done: geom.py (24 internal teeth Ri 15 / Ro 16.6, 2 wedge pawls on pivots, driver pockets via shapely), kin.js (one loop 18.5 s: coast 0-10.3,
driver catches the ring at 11.02 s, drive to 14.0, coast again; ring exactly 4 turns, driver 1 turn, warm start so the pawl state loops),
check.js (HARD GATE 5.2), scene.html (tools/render/lib/studio.js; cog with upper half cut away by a clipping plane), vo.py, audio.py, post.json.
Rebuild: python3 -m pip install shapely; python3 geom.py; node runkin.js 79.6,53; node check.js
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p051/scene.html <out> 30 1 0 555 0.85 1 <w> 3
Audio: Kokoro venv (kokoro-onnx 0.6.1, model = cat kokoro-q8-shards@1.0.0 parts, voices.npz from kokoro-js@1.2.1 voices/*.bin as float32 (-1,1,256));
  <venv>/python vo.py <ttsdir> <vodir>; python3 audio.py <vodir>; tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
  -> -15.1 LUFS, -3.1 dBTP, HP4k gap 19.8 dB.
Reviewer round 1 = 4/10 (flat grey, wood bench cheap, pawl tiny in wide shots, cut not readable, labels crossing arcs) -> fixes: dark gradient backdrop, env 0.6 + exposure 1.1, no locknut, closer cameras, red section cap on the cut gear, labels at y 1390, coasting arc, dark index dots.
Speed: RectAreaLights cost ~1.5 s/frame and the MSAA half-float composer target ~3 s on swiftshader -> directional fills + samples 0 at full res = 2.8 s/frame (parallel workers do not help: swiftshader already uses all 4 cores).
Final: round-2 render had z-fighting stripes on the gear cut (coplanar plate + step at z=1) -> step moved to z=1.04, re-rendered at 0.8 scale (2 workers, 18 min). HARD GATE pass. Reviewer round 2 = 5/10 (wants reflective metal, AO, carrier smaller in frame, arrowheads clipped at the right edge).
Scheduled: Metricool 420523115, Instagram REEL 8 Nov 2026 17:00 Europe/London, media/p051/freehub_reel_v2.mp4 + freehub_cover_v2.jpg.
