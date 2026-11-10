# p060 handcuff double lock "WHY A / DOUBLE LOCK?" - track A - group E - SCHEDULED 11 Nov 2026 17:00 (Metricool 423789703, media/p060/handcuff_reel_v2.mp4)
Done: kin.py (arm teeth pitch 2 deg r 70.4-72 about the pivot; orange pawl on Q, lift = smallest angle keeping 0.03 mm clearance (shapely bisection),
snap-back 260 deg/s; bolt slides up behind the pawl pad (0.1 mm); housing spacer = outline minus arm/pawl/bolt sweeps; wrist ellipse 48x56 mm fitted:
3.0 mm gap at phi -22, 0.1 mm at -12), probe.py (overlap checks), scene.html, vo.py, audio.py (-15.1 LUFS, -3.1 dBTP, HP4k gap 20.0 dB), post.json (copy spellchecked).
Story 41 s: cuff on wrist + click -> front plate fades -> parts named -> 1 push in: 2 clicks -> 2 pull back: jams -> problem: 2 more clicks, wrist red, TOO TIGHT
-> 3 key pin pushes the bolt in -> 4 push/pull blocked -> payoff 3.6 s -> plate back, follow line -> loop (last 0.6 s cross-fades to frame 0).
Rebuild (venv with shapely/numpy/soundfile/kokoro-onnx): python kin.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 3 workers: node tools/render/render.js posts/p060/scene.html <out> 30 1 0 1230 0.9 1 <w> 3 1080 1920 1 (~2.2 s/frame effective, ~45 min)
Done: v2 final, HARD GATE + CLARITY pass, reference 6.2 -> 6.6, visual 5.5, scheduled. Toolkit next: metal pawl/bolt with tint, real hand, hide bolt until step 3, no text over the action, tighter framing.
