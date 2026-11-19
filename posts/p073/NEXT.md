# p073 bike V-brake "HOW DOES ONE CABLE / SQUEEZE BOTH SIDES?" - track A (Kokoro af_heart VO) - group V - for Instagram 20 Nov 2026 17:00
topic key: bike v-brake - not in learnings/topics-used.md (checked 71 rows incl. p071/p072; bike rows are freewheel (p004/p051) and the unpublished quick release p061 - different mechanism; no brake row except handbrake p058 = car parking brake ratchet).
Built from kit/kit.js (materials incl. paint, backdrop, light rig, text style, glow, RBox) + scene-local bike wheel (tyre torus, rim lathe, 24 spokes), fork, bars, lever, V-brake arms, noodle + housing tubes.
Done: kin.py (arms pivot at (+-40, -70); pad face corner contact solved exactly: closed -7.22 deg, open -3.57 deg (4 mm gap); cable pull = change of the arm-top distance, max 14.6 mm;
ratio S_TOP/S_PAD 1.92; wheel speed integrates, stops while the pads grip; loop 25.9 s), checks inside kin.py PASS (pad never enters the rim; arm tops clear of the tyre),
scene.html (front close-up cuts the wheel's front half at z 45 so the pads/rim section are visible), vo.py (7 lines), audio.py + master (-15.0 LUFS, -3.1 dBTP, HP4k gap 20.8 dB),
post.json (spellchecked: only whyloop/hq/howitworks/mm flagged = handle/hashtag/unit).
Facts: Wikipedia Bicycle brake + Wikipedia Lever (Firecrawl scrape this run).
Render: NODE_PATH=/opt/node22/lib/node_modules node tools/render/render.js wip/p073/scene.html <out> 30 1 0 777 0.75 0 0 1 1080 1920 1; encode.sh <out> wip/p073/mix.wav brake_reel.mp4 25.9 30

STATUS (18 Nov 22:06 run, end ~23:30 UTC): NOT SCHEDULED - CLARITY GATE failed twice (v1 + v2). 20 Nov 17:00 is EMPTY -> next run: either finish p073 v3 (fixes below, new render ~9 min alone) or make a simpler topic.
- v1 (brake_reel.mp4): HARD GATE PASS; visual 5/10; clarity 14yo NO ("tube" confused with the fork tubes, arms barely move, lever not shown, SPIN/STOP flips).
- v2 (brake_reel_v2.mp4, current files): VO line 3 "Its outer casing pushes back...", GAP 4 -> 6 mm (pull 21.8 mm), OUTER CASING / INNER CABLE tags, ticks sliding into the casing, GAP bracket, PIVOT dots + long/short lines,
  "SQUEEZE ≈ 2× THE PULL", badge only in wide/3-4 shots, TIRE (CUT OPEN) tag, hook circle on the pad. HARD GATE PASS (26.2 s, -15.1 LUFS, -3.0 dBTP, gap 21.0 dB). Clarity retest: explanation correct, 14yo NO.
TODO for v3 (reviewer 2):
 1. WHY the casing pushes: a short cutaway of the wire inside its casing (casing end resting on the left arm, wire end on the right arm) + equal-and-opposite arrows; VO: "The wire pulls one way, so its casing shoves back the other way."
 2. Leverage step must NOT reopen the brake: show the travel readouts during the first squeeze (step 1/2) or say "Watch it again"; one name for the travel ("CABLE PULLED: 22 MM" everywhere, drop the separate GAP readout or start it at 0);
    explain the yellow/blue lines with LONG / SHORT pills or remove them; say "small pad move, big force" instead of "2×" (or show force bars).
 3. Opening: label the circled part PAD in the hook; show the lever moving (bigger blade, a hand outline) and drop the SPIN->STOP->SPIN flip (badge off until the friction beat);
    fewer labels at 6-8 s (no TIRE tag; tilt the camera 20-25 deg so the cut tyre reads as a tyre); fix clipped OUTER CASING tag; step header "4 FRICTION STOPS THE WHEEL" at the friction beat.

STATUS (19 Nov 01:09 run, ig-awesome-curie-0109-19nov):
- v3 (brake_reel_v3.mp4): leverage step REMOVED; VO lines 3-5 new ("Inside the cable, a wire pulls one way, so its casing shoves back the other way." / "The wire drags the right arm in. The casing pushes the left arm in." / "Both pads pinch the rim at once, and friction stops the wheel.");
  2D strip of wire + casing; PAD pill in the hook; lever blade bigger; parts shot tilted 22 deg, no TIRE tag; badge only at the friction beat. HARD GATE PASS (24.8 s, -15.0 LUFS, -2.9 dBTP, gap 20.1 dB).
  VISUAL 5/10 (fixes: friction beat stays front with both pads, FRICTION pill off the rim, brake lower under the hook title). CLARITY 14yo NO (borderline: casing push-back not shown).
- v4 (brake_reel_v4.mp4) = v3 + visual fixes + clarity fixes (see-through CASING (TUBE) strip with both arrows at once, CASING/WIRE tags on the 3D view from step 1, GAP 6 -> 10 mm (bigger swing), PIVOTS marked, wheel 0.4 rev/s + red reflector so the stop is visible).
  HARD GATE PASS (24.8 s, -15.0 LUFS, -2.9 dBTP, gap 20.1 dB). CLARITY PASS (explanation correct; 14yo YES, "only just").
- v5 (brake_reel_v5.mp4) = v4 + WIRE tag hidden in step 2 (it overlapped the WIRE PULLS pill). This is the scheduled file.
