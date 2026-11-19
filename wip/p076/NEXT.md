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
