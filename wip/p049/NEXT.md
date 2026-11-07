# p049 tape measure (track A, voiced) - WIP
Done: kin.js (blade extension timeline, spiral tape on reel with tangent exit, spiral spring post->drum), scene.html (uses tools/render/lib/studio.js), vo.py (Kokoro af_heart), audio.py (stems) + tools/render/master.sh (safe master), post.json (caption, first comment, sources, alt text).
Left: final render 1080x1920 30 fps (scale 0.85 3D, no motion blur), encode, HARD GATE, reviewer score, schedule 7 Nov 17:00.
Rebuild: cd tools/render && npm i; python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p049/scene.html <out> 30 1 0 540 0.85 0 <w> 2
Audio: venv kokoro-onnx 0.6.1 + npm kokoro-q8-shards@1.0.0 (sha256 fbae9257...a1478) + kokoro-js@1.2.1 voices -> vo.py <ttsdir> <outdir>; node dumps kin_240.json; python3 audio.py <vodir>; master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
