# p059b gearbox synchro REMAKE "HOW DOES IT / SHIFT GEARS?" - track A (Kokoro af_heart VO) - group V - 17:00 1M+ list #1 remake (Erkan 10 Nov 18:30)
SCHEDULED: Metricool 423615534, Instagram REEL 11 Nov 2026 17:00 Europe/London (PENDING). Media: media/p059b/gearbox_remake_reel_v3.mp4 + gearbox_remake_cover_v3.jpg.
Story (42 s): car interior + hand (sideways select) -> console/case fade -> parts named (gear, shaft, sleeve, fork, brass ring) + speed bars -> no-synchro what-if
(ring removed, sleeve bounces off the dog-teeth faces, GRIND!) -> 1 ring presses the cone (ring x-rayed) -> 2 friction matches speeds (video slowed 0.45x, bars turn green)
-> 3 sleeve slides in -> 4 locked: gear turns shaft -> payoff "RING MATCHES SPEEDS FIRST. NO GRIND." 3.6 s -> back out, hand returns the lever -> loop.
Gates: HARD GATE pass; CLARITY GATE round 1 fail -> round 2 pass; visual 5/5 (see post.json).
Rebuild: python3 kin.py && python3 check.py && <kokoro venv>/python vo.py <ttsdir> vo && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Kokoro: venv kokoro-onnx 0.6.1; model = cat kokoro-q8-shards@1.0.0 parts (sha256 fbae9257...a1478); voices.npz from kokoro-js@1.2.1 voices/*.bin (float32, -1,1,256).
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js posts/p059b/scene.html <out> 30 1 0 1260 0.8 0 <w> 2 1080 1920 1 (~1.9 s/frame/worker, ~20 min)
Optional v4 (to beat visual 5): AO on (+45% time -> render ~29 min: split over two runs or lower scale), darker backdrop + rim, 192+ segments on all cylinders, DOF on close-ups, better hand/dashboard. Replace with updateScheduledPost (full content).
