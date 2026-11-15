# p067 gravity gate latch "HOW DOES IT / LOCK ITSELF?" - track A (Kokoro af_heart VO) - group E - 1M+ list #6 - for Instagram 16 Nov 2026 17:00
Done: kin.py (gate on hinge x=-900; bar lift at the catch solved with shapely: ramp lifts it, ballistic drop a=1.5g/slow^2, staple stop; hook close 6 deg, problem shot without latch (bounces to 9 deg),
slow close 10.6-16.2, pull 17.6-18.3 stops 0.3 mm from the wall, lift + open 23.6-25.6; LOOP 26.4 s), check.py PASS (no overlap, locked gap 0.3 mm, bar 14 mm under the lip top),
scene.html, vo.py (8 lines), audio.py + master (-15.0 LUFS, -3.1 dBTP, gap 19.7 dB), post.json (spellchecked: only hashtag/handle flags).
Facts: US 858,866; US 2,671,683; US 413,193 (opened 15 Nov 13:20 via Parallel fetch).
Rebuild: venv(kokoro-onnx 0.6.1 numpy soundfile shapely pyspellchecker): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); 3 workers: node tools/render/render.js wip/p067/scene.html <out> 30 1 0 792 0.7 0 <w> 3 1080 1920 1 (AO off: AO costs +65 % per frame)
then tools/render/encode.sh <out> wip/p067/mix.wav latch_reel.mp4 26.4 30
Left: final render -> encode -> HARD GATE -> clarity gate + visual review -> schedule 16 Nov 17:00.

STATUS (15 Nov 13:07 run, ig-sweet-lamport-1311): v1 = latch_reel.mp4 + latch_cover.jpg (render 13:27-13:42, ~15 min, 3 workers, scale 0.7, AO off).
HARD GATE v1 PASS: 1080x1920 30 fps H.264 High yuv420p + AAC 48 kHz, 26.4 s, -15.1 LUFS / -3.0 dBTP, HP4k gap 19.7 dB, first/last luma 93 (no black), loop seam 0.26,
frame spikes only at the planned hard cut 2.73 s and the push-in ~6.7 s; safe zones clear at 0.5 s; check.py PASS; spellcheck only hashtag/handle flags.
Clarity + visual review running.

ROUND 2 (15 Nov 14:10): v2 = media/p067/latch_reel_v2.mp4 + latch_cover_v2.jpg. HARD GATE PASS (same audio; -15.1 LUFS / -3.0 dBTP, gap 19.7 dB, loop seam 0.24,
spikes only at the planned cut 2.73 s and the push-in ~6.7 s; hook moved out of the right safe zone: HOOK cam target x 30, y Y0+55, dist 880). CLARITY PASS (round 1, story unchanged).
Visual round 1 = 5 -> fixes done; round 2 = 5 -> NOT scheduled (AGENT §6: 5 only when the slot is < 2 h away or late; max 2 rounds). RESERVE, gate-passed.
USE: if 16 Nov 17:00 is still EMPTY on Instagram and no 6+ Reel is ready, schedule p067 v2 once the slot is < 2 h away (from 15:00 Europe/London on 16 Nov), e.g. at the end of the 16 Nov 13:07 run.
Media is already on main (raw URL). Caption/firstComment/altText in post.json.
Round-2 reviewer points (for the toolkit, not for this Reel): steel still reads matte "CAD clay" (needs AO/contact shadows + stronger reflections: AO costs +65 % render time),
wood texture reads as smeared stripes (needs real grain/end grain), 40 % frame (10.6 s) has the caption before the bar is in frame, the wide no-latch shot cannot show the bounce in a still,
the stop strip seen through the gap in the hook reads as a loose plank (hide it or make it post trim on the far side).
