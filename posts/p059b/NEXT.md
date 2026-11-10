# p059b gearbox synchro REMAKE "HOW DOES IT / SHIFT GEARS?" - track A (Kokoro af_heart VO) - group V - 17:00 1M+ list #1 remake (Erkan 10 Nov 18:30)
Slot: Instagram 11 Nov 2026 17:00 Europe/London. 42 s loop, clarity rules (car interior + hand -> inside -> problem (no synchro = GRIND) -> 4 steps -> payoff -> loop).
Done: kin.py (reuses p059 geometry; ring removed 12.2-19.3 for the "without a synchro" demo, sleeve bounces off the dog-teeth end faces 15.9-17.6, never inside;
slow motion 0.45x 22.4-28.0; shaft 13 turns/loop, gear +6; H-pattern lever: sideways select 1.0-2.4 / back 40.0-41.2), check.py (PASS: overlap 0, dog-face gap 0.15 mm, loop seam 0),
vo.py (10 Kokoro lines, start times in geom.json VO_AT), scene.html (car interior with hand, case/car fades, per-part highlight + dim, pinned part tags, step captions 1-4,
speed meter, GRIND!, slow-motion badge, payoff 34.4-38.0), toolkit: studio.js tag/caption/speedMeter.
Rebuild: python3 kin.py && python3 check.py && <kokoro venv>/python vo.py <ttsdir> vo && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p059b/scene.html <out> 30 1 0 1260 0.8 0 <w> 2 1080 1920 1 (~1.25 s/frame effective, ~26 min)
Left: final render -> encode -> HARD GATE + CLARITY GATE -> visual review -> schedule 11 Nov 17:00.
