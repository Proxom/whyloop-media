# p062 car differential "TWO WHEELS. / TWO SPEEDS?" - track A (VO) - group V - 17:00 1M+ list #3 - target Instagram 12 Nov 2026 17:00
Done: kin.py (open diff: thR = c + d, thL = c - d; ring/pinion 41/11, side/spider 16/10 straight bevels on common apexes; gear phases solved),
check.py (mesh offset vs half pitch over the loop <1.7 % pitch = chord noise, constant -> no drift; L+R = 2c; 0.35/0.35, 0.263/0.438, 0/0.70 rev/s),
scene.html (ghost car turn + wheel tracks, skid, cutaway, ring/pinion/driveshaft, spiders/pin, side gears, locked cutaway camera for steps 1-3 + wheel dials, payoff, loop),
vo.py (Kokoro af_heart, speed 1.05), audio.py + master (-15.1 LUFS, -3.0 dBTP, HP4k gap 21 dB), post.json (copy spellchecked; Britannica, MIT 2.972, tec-science, Counterman).
Rebuild: venv(kokoro-onnx soundfile numpy pillow): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p062/scene.html <out> 30 1 0 1260 0.8 0 <w> 2 1080 1920 1 (~19 min; AO off, scale 0.8: AO/1.0 = 38-55 min)
then python finalize.py <frames> <fin>; tools/render/encode.sh <fin> mix.wav differential_reel.mp4 42 30
Reviews: visual R1 4 -> R2 5 (max 2 rounds reached); reference R1 5.0 -> R2 6.2; clarity R1 fail, R2 fail (14yo no: "don't spin" vs revolving spiders), R3 fixes rendered.
Clarity R3 (fresh reviewer, 11 Nov 14:41): explanation fully CORRECT (ring gear carries spiders; straight: ride along; turn: spin on pin, one wheel slows by as much as the other speeds up) but 14yo NO.
NOT SCHEDULED (clarity gate not passed; visual 5 also means: schedule only when the slot is < 2 h away). Latest final: differential_reel.mp4 (R3) + differential_cover.jpg.
LEFT (one render ~19 min + clarity check; the 21:07 run or the 05:07 run on 12 Nov; slot 12 Nov 17:00):
1. VO line 4 (12.8 s) -> name the side gears: "The driveshaft turns the ring gear. It carries spider gears, which mesh with a side gear on each axle." Highlight both side gears + tags INNER/OUTER SIDE GEAR at 15-18 s (not only in step 1).
2. Step 2 seesaw (25-32 s): two curved arrows on the side gears (blue backward/slower, yellow forward/faster) driven from k.d, plus the spider spin arrow; keep the wheel dials.
3. Step 3 (33-36 s): show a brake caliper/hand stopping the blue wheel (or a red STOP block on the blue shaft) and say "twice the ring gear's speed".
4. Rename tag LOCKED ON PIN -> NOT SPINNING ON PIN; drop the PINION tag (jargon, not narrated) or narrate it.
5. Visual (R2 reviewer, if time): smoother flanges (more segments), ring gear fully in frame in the payoff, darker top band (tire blobs) or lower camera elevation.
