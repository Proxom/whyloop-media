# p058 handbrake "WHAT HOLDS / IT UP?" - track A (Kokoro af_heart VO) - group V - for Instagram 11 Nov 2026 01:00
Done: kin.py (fixed sector plate, 9 teeth: root r 40, height 2.6, pitch 4.5 deg, ramp rises with the lever going up + radial steep face;
orange pawl pivots on the lever at Q (ahead of and above the contact line -> load turns it IN = self-locking); pawl angle = smallest angle
keeping 0.05 mm clearance (shapely bisection), snap-in rate limit 320 deg/s; button spring pulls the push rod -> pawl into the teeth;
pull 3 clicks (0.50/0.84/1.20 s), let go -> lock 1.74 s, pull 2 clicks (7.58/8.25 s), push down -> lock 11.45 s, lift, press 12.6-13.6
(rod back, pawl out 12.5 deg), lower to rest, release button 15.9 s; loop 18.5 s closes), check.py (0 overlap, min pawl gap 0.024 mm, rod gap 3.5 mm),
scene.html (console + lever exterior -> opacity fade 2.5-3.4 -> side section close-up -> button close-up -> follow the rod back -> fade in 15.95-16.85),
vo.py (Kokoro af_heart), audio.py (-15.1 LUFS, -3.1 dBTP, HP4k gap 20.3 dB).
Facts: CarThrottle + CarGurus (post.json sources). Copy spellchecked (flags: brand names, hashtag, URL parts only).
Rebuild: python3.13 kin.py && python3.13 check.py && python3.13 vo.py <ttsdir> vo && python3.13 audio.py vo && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p058/scene.html <out> 30 1 0 555 1 1 <w> 2 1080 1920 1 (~1.5 s/frame effective, ~14 min)
Left: final render -> encode -> HARD GATE -> review -> schedule 11 Nov 01:00.
