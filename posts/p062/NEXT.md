# p062 car differential "TWO WHEELS. / TWO SPEEDS?" - track A (VO) - group V - 17:00 1M+ list #3 - READY for Instagram 12 Nov 2026 17:00
STATUS (11 Nov 21:07 run): round 4 final = differential_reel.mp4 (42.0 s) + differential_cover.jpg (hook frame unchanged).
HARD GATE PASS: 1080x1920 30 fps H.264 + AAC, 42.0 s, -15.0 LUFS / -3.0 dBTP, HP4k gap 20.7 dB, look/safe zones checked, copy spellchecked.
CLARITY GATE PASS (R4 fresh reviewer): explanation correct, "14-year-old: YES" (blue/yellow coding from road paths to gears to dials; NOT SPINNING vs SPINS ON PIN).
Visual score stays 5 (2 rounds used) -> per AGENT 6 schedule only when the slot is < 2 h away: the 12 Nov 13:07 run schedules it for 12 Nov 17:00 AFTER 15:00 London
(if the 13:07 run ends before 15:00, schedule at its end only if after 15:00; otherwise it is a LATE POST case for the 21:07 run -> now + 3 min is NOT wanted; keep the 17:00 slot rule).
Steps: move differential_reel.mp4 + differential_cover.jpg to media/p062/, source to posts/p062/, delete wip/p062, push, wait for raw URL HTTP 200, getScheduledPosts, createScheduledPost
(caption/firstComment/altText from post.json, instagramData type REEL, videoThumbnailUrl = cover), confirm PENDING at 17:00.
REFERENCE GATE: original frames were not reachable (YouTube blocked) in the 13:07 run; our-frames score was 6.2 in R2. Try once more in the 13:07 run (max 10 min), otherwise log "not reachable".
Round 4 changes: VO line 4 names the side gears ("Its spider gears mesh with a side gear on each axle"); INNER/OUTER SIDE GEAR tags 16.2-19.3 s + glow;
step 2 curved arrows around each side gear turning at the real wheel speed (SLOWER/FASTER); step 3 red brake clamps the inner axle ("HELD STILL", camera shifted left),
VO "the other spins at twice the ring gear's speed"; tag NOT SPINNING ON PIN; PINION and PIN tags dropped; payoff camera wider (ring gear in frame).
Reviewer leftovers (not blocking): "ring gear carries them" only as text (not in VO), 12.8-14.5 s pinion/ring close-up too tight, DRIVESHAFT leader runs off the left edge at 14.5 s.
Rebuild: venv(kokoro-onnx 0.6.1 soundfile numpy pillow): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p062/scene.html <out> 30 1 0 1260 0.8 0 <w> 2 1080 1920 1 (~18 min)
then python finalize.py <frames> <fin>; tools/render/encode.sh <fin> mix.wav differential_reel.mp4 42 30
SCHEDULED (13 Nov 21:07 run): Metricool 427480746, Instagram REEL 14 Nov 2026 01:00 Europe/London, PENDING. 12 Nov 17:00 was missed (no runs from 12 Nov 13:07 to 13 Nov 13:07), so this was a late post into the next normal slot.
