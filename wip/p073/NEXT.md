# p073 bike V-brake "HOW DOES ONE CABLE / SQUEEZE BOTH SIDES?" - track A (Kokoro af_heart VO) - group V - for Instagram 20 Nov 2026 17:00
topic key: bike v-brake - not in learnings/topics-used.md (checked 71 rows incl. p071/p072; bike rows are freewheel (p004/p051) and the unpublished quick release p061 - different mechanism; no brake row except handbrake p058 = car parking brake ratchet).
Built from kit/kit.js (materials incl. paint, backdrop, light rig, text style, glow, RBox) + scene-local bike wheel (tyre torus, rim lathe, 24 spokes), fork, bars, lever, V-brake arms, noodle + housing tubes.
Done: kin.py (arms pivot at (+-40, -70); pad face corner contact solved exactly: closed -7.22 deg, open -3.57 deg (4 mm gap); cable pull = change of the arm-top distance, max 14.6 mm;
ratio S_TOP/S_PAD 1.92; wheel speed integrates, stops while the pads grip; loop 25.9 s), checks inside kin.py PASS (pad never enters the rim; arm tops clear of the tyre),
scene.html (front close-up cuts the wheel's front half at z 45 so the pads/rim section are visible), vo.py (7 lines), audio.py + master (-15.0 LUFS, -3.1 dBTP, HP4k gap 20.8 dB),
post.json (spellchecked: only whyloop/hq/howitworks/mm flagged = handle/hashtag/unit).
Facts: Wikipedia Bicycle brake + Wikipedia Lever (Firecrawl scrape this run).
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p073/scene.html <out> 30 1 0 777 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p073/mix.wav brake_reel.mp4 25.9 30
