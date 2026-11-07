# p048 ratchet Reel (published 7 Nov 2026, late post for the 01:00 slot)
Done: kin.js (single-source pawl/gear contact sim, 2400 Hz, loop = 4 cycles = 12 s, gear 120 deg), scene.html (three.js 0.170, Anton font via @fontsource/anton), audio.py (modal-synth clicks from events.json), render.js (Playwright swiftshader, adaptive motion blur: sub = ceil(0.5*px/3), max 12).
Rebuild: npm i three@0.170.0 @fontsource/anton@5; python3 geom.py (needs geo_in.json from kin.js, see run notes); node -e "kin -> kin_240.json/events.json" (phase 0.55 s); http-server on :8765; node render.js out 30 0 0 360 1 1 <w> 2; python3 audio.py; ffmpeg encode 14 Mbps.
Reviewer history: 5/10 -> 4/10 -> 6/10 -> 6/10 (gear anisotropy blow-out, fixed in final: rotating parts must NOT use anisotropic materials).
Ideas for a Part 2: dual-pawl / reversing-lever ratchet, bike freewheel click.
