# p061 bike quick release "WHY DOES IT / STAY SHUT?" - track B (wordless) - group V - target Instagram 12 Nov 2026 01:00 - NOT SCHEDULED (round 2: visual 5, CLARITY GATE fail)
Done: kin.py (eccentric cam E 1.8 / R 6.2 on the rod-end pin; lever gamma 95 -> 0 deg from the wheel plane, cam beta = 188 - gamma; body touches the dropout at gamma 70
(4.8 s, open gap 0.75 mm), peak at gamma 8 (9.4 s), snap home 9.62 s (closed squeeze 98 % of peak = over the top, Sheldon Brown), tug 10.8-11.5, pull open 13.3-14.8; loop 17 s),
check.py (cam-face 0.02 mm, lever clear of fork/body, slot/tang clearances), scene.html (hook 3/4 -> front view, front shell fades, OFF-CENTER CAM tag, SQUEEZE curve panel, captions, follow line),
audio.py (-18.2 LUFS, -2.9 dBTP, HP4k gap 49.0 dB), post.json (copy spellchecked; sources Sheldon Brown + Park Tool + US 8,905,492).
Rebuild: python3 kin.py && python3 check.py && python3 audio.py && ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 0 0 -18
Render: python3 -m http.server 8765 (repo root); 3 workers: node tools/render/render.js wip/p061/scene.html <out> 30 1 0 510 1 1 <w> 3 1080 1920 1 (~7.4 s/frame/worker, ~21 min)
Latest final: wip/p061/quick_release_reel.mp4 + quick_release_cover.jpg (technical + audio + mechanism + facts + text PASS; CLARITY FAIL).
Round 1 (fresh reviewer): 5/10, 14yo NO (cam looked centred, peak never shown, arrows cut at edges, captions cross-faded, fork 'translucent') -> fixed: E 1.1->1.8 / R 7->6.2, SQUEEZE curve, arrows only inside safe area, caption timing, hook circle on lever root.
Round 2 (fresh reviewer): 5/10, 14yo NO. Explanation: lever turns cam, cam pushes cup onto fork, graph passes a dashed peak - but WHY it stays shut only from prior knowledge.
LEFT (do these, then ONE final render + fresh clarity check; slot 12 Nov 01:00, reserve p057 if still not 6+ at 23:00):
1. Show the over-center torque: after the peak, an orange curved arrow on the lever labelled "SQUEEZE PUSHES IT SHUT" (instead of the caption), lever lands on a modelled stop tab (thunk = stop). Graph: label the dashed line PEAK, x axis "LEVER CLOSES ->", draw the 2 % dip visibly (thicker line, zoomed y range near the top).
2. Cam reads as off-center: pin dot + cam-centre dot joined by a short yellow line on the front cheek; highlight the cup-to-dropout gap (yellow bar) until it closes at 4.8 s.
3. Ending: do not let the open swing read as failure - caption "TO OPEN: PULL IT BACK OVER THE PEAK" during 13.3-14.8, or hold closed and cross-fade to the open hook.
4. Investigate the 'translucent/pink' fork strip in the front close-ups (blade side reflection? set M.paint envMapIntensity 0.4, check blade normals) and hide tire/rim in the front close-ups (edge-on tire reads as a wrong arc next to the axle).
5. Graph panel overlaps the bottom of the cup at 4.5-13 s: frame the mechanism ~120 px higher or shrink the panel to 230 px tall.
6. Visual (both reviewers): contact shadows, slight DOF on spokes, a shaped cam body instead of the plain black block behind the cam.
