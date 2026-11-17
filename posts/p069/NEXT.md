# p069 car clutch "HOW DOES A / CLUTCH WORK?" - track A (Kokoro af_heart VO) - group V - 1M+ list #9 - for Instagram 18 Nov 2026 17:00
topic key: car clutch - not in learnings/topics-used.md (checked 57 rows; the gearbox Reels p059/p059b only mention the pedal in the caption).
First Reel built from kit/kit.js (KIT DAY 16 Nov): kit materials/backdrop/light rig/text style + kit spurGear (starter ring gear), spring (disc dampers), wheel.
Done: kin.py (push-type diaphragm clutch: finger cone slope solved so the plate clamps the 9 mm disc exactly; lever ratio 20:53 -> plate lift 10 mm (gap drawn wide),
bearing travel 25.7 mm, fork angle from the bearing; disc slips 1.1 s after the clamp, stops 2.4 s after release; loop: engine 83 x 60 deg per loop, disc angle continuous at t=0),
check.py PASS (axisymmetric shapely check of every 1/60 s row: 0 overlaps, contact kept), scene.html, vo.py (8 lines, Kokoro v1.0 int8), audio.py + master (-15.1 LUFS, -3.1 dBTP, gap 20.5 dB), post.json (spellchecked).
Facts: Wikipedia Clutch; HowStuffWorks What Is a Clutch? (opened this run).
Rebuild: venv(kokoro-onnx numpy soundfile shapely pyspellchecker): python3 kin.py; python check.py; python vo.py <ttsdir: kokoro.onnx + voices.bin from thewh1teagle/kokoro-onnx model-files-v1.0> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 --bind 127.0.0.1 (repo root); node tools/render/render.js posts/p069/scene.html <out> 30 1 0 756 0.75 0 0 1 1080 1920 1 (1.3 s/frame, ~16 min)
then tools/render/encode.sh <out> posts/p069/mix.wav clutch_reel.mp4 25.2 30
Left: final render (started ~05:52 UTC) -> encode -> HARD GATE -> clarity gate + ONE visual review -> schedule 18 Nov 17:00.

STATUS (17 Nov 05:07 run, end): SCHEDULED 18 Nov 2026 17:00 Europe/London, Metricool 431036468 (PENDING). Media: media/p069/clutch_reel_v2.mp4 + clutch_cover_v2.jpg.
v1: HARD GATE PASS (1080x1920 30 fps H.264 High yuv420p + AAC 48 kHz, 25.2 s, -15.1 LUFS / -3.0 dBTP, HP4k gap 20.5 dB, first/last luma 56), CLARITY PASS (correct 2-sentence explanation, 14yo YES), visual 5/10.
Round-1 fixes once (rule 15 Nov 14:23, no re-score): stamped-steel cover (read as a tyre), smooth cast-aluminium block (blotchy noise), dark backdrop without the grey wall band + tighter wide shots;
clarity notes: PLATE PULLS BACK arrow during the press, <- ENGINE / WHEELS -> tags in the rim close-ups, SQUEEZED anchor on the disc, step-2 caption after the pedal moves, DIAPHRAGM SPRING label.
v2: HARD GATE PASS (same audio, loop seam 2.07, only spikes = planned 1.0 s white cut), render 15 min (1.2 s/frame, kit settings).
Reviewer points for the KIT: recognisable pedal + fork linkage part, box housing / bellhousing, wheel kept fully in frame in wide shots.
