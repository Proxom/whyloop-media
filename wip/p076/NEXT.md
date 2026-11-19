# p076 flint lighter "WHERE DOES THE / SPARK COME FROM?" - track A (Kokoro af_heart) - group E - scorecard next-10 #7
topic key: lighter flint - not in learnings/topics-used.md (checked 63 rows; no lighter / flint / spark / ferrocerium / piezo row).
Built from kit/kit.js: striker + thumb discs = kit spurGear (48 knurl teeth m0.15, 44 ribs m0.24), kit spring, RBox body/cap/hood, additive flame layers, instanced spark streaks + glow points + grey chips.
kin.py: wheel turns clockwise (bottom edge to -x, toward the nozzle), scene-time map (slow motion 0.3 hook, 0.12 scraping, 0.15 sparks), 480 sparks (115 cold chips in step 2, glow delay in step 4);
checks PASS: flint top on the tooth-tip circle (no tooth enters the flint), flint and tube clear of the thumb discs (tube top lowered after the check caught 0.23 mm), nozzle clear of the discs, sparks leave forward; wheel loop seam = multiple of 90 deg.
Facts: Wikipedia Ferrocerium (cerium ignites 150-180 C; friction -> hot fragments oxidize in air = sparks; steel wheel strikes the 'flint') + Wikipedia Lighter + US 5,509,799 (spring urges the flint against the wheel).
Audio PASS: -15.0 LUFS, -3.1 dBTP, HP4k gap 21.5 dB. Copy spellchecked: only ferrocerium, mischmetal, piezo, hashtag/handle flagged (valid).
Rebuild: python3 kin.py; venv python vo.py <ttsdir> vo; venv python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render (no HTTP server needed now, tools/render/lib/localfs.js): NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p076/scene.html <out> 30 1 0 831 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p076/mix.wav lighter_reel.mp4 27.7 30
Left: final render (running) -> encode -> HARD GATE -> clarity + visual review -> schedule 21 Nov 17:00.

STATUS (19 Nov 05:09 run): NOT SCHEDULED. HARD GATE PASS (1080x1920 H.264 High yuv420p 30 fps, AAC, 27.7 s, no black ends, -15.1 LUFS, -3.0 dBTP, HP4k gap 21.4 dB). CLARITY PASS (14yo YES).
VISUAL 4/10 -> kit rule B: 4 or lower = do not schedule. Final v1 = wip/p076/lighter_reel.mp4 (TINY BITS tag fix in scene.html not re-rendered).
Visual reviewer: (1) sparks look like matchsticks / bokeh balls / grey cubes -> one emitter at the wheel-flint contact, thin motion-blurred streaks (white-yellow core, orange tail), bloom, flickering point light; flame = flat 3-tone teardrop -> soft gradient glow with blue base;
 (2) wheel = thin saw blade with big teeth -> narrow knurled cylinder (fine teeth across the width) between thumb discs, brushed steel; chrome hood shows a big blurry env blob; red body corner artifacts; flint orange in step 3 reads as plastic/hot;
 (3) overlays: 2D strip panel covers the wheel-flint contact (move to the empty top area or drop), cerium bar has no meaning, labels collide (TINY BITS/step 2), ROUGH STEEL EDGE points at the face, HOT! leader goes off-screen, hook circle on the wheel face not the contact.
Clarity reviewer extras: say "friction" (why the bits get hot), keep the flint grey, show the gas jet before the sparks reach it, keep the flame lit during the recap.
Next: only redo with a kit spark/flame effect + knurled wheel part (worth adding to kit/), otherwise drop.
