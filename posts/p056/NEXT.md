# p056 light switch "WHY DOES IT / SNAP?" - track A (Kokoro af_heart VO) - group E - for Instagram 10 Nov 2026 17:00
Done: kin.py (lever pivot A(-7,0), copper bar rocks on rod B(-24,0), plunger tip r 1.5 tangent to the bar by construction,
snap when the contact point crosses B at phi = 1.37 deg, spring 5.73 -> 4.00 mm, loop 18.3 s closes), check.py (shapely 240 Hz: 0 overlap, tip gap < 0.0001 mm),
scene.html (exterior plate+wall -> opacity fade 2.6-3.6 -> side section -> back 15.4-16.5), vo.py (Kokoro), audio.py (-15.1 LUFS, -3.1 dBTP, HP4k gap 20.2 dB).
Facts: Wikipedia Light switch + Switch (post.json sources). Copy spellchecked (flags: hashtags, handle, Holmes').
Rebuild: python3.13 kin.py && python3.13 check.py && python3.13 vo.py <ttsdir> vo && python3.13 audio.py vo && tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js posts/p056/scene.html <out> 30 0 0 549 1 1 0 1 1080 1920 (~2.2 s/frame, ~20 min)
Left: final render -> encode -> HARD GATE -> review -> schedule 10 Nov 17:00.
Round 1 final: HARD GATE pass, reviewer 5/10 (flat lighting/materials, cutaway framing cut the terminal, hook too tight, dark stop read as overlap) -> fixed.
Round 2 final v2: HARD GATE pass, reviewer 6/10 -> scheduled Instagram REEL 10 Nov 2026 17:00 (AGENT 6: 6+ after round 2).
Toolkit ideas from round 2: lighter backdrop/rim vs charcoal parts, shinier copper/silver (visible env reflection), mounting strap so the lever hub is grounded,
keep leader lines off the moving parts, avoid two bevelled pieces meeting on one edge (seam line), hook: show the whole plate centered.
