# p063 stapler "WHY DO STAPLES / BEND IN?" - track A (Kokoro af_heart VO) - group E - for Instagram 13 Nov 2026 01:00
Done: kin.py (staple crown 12.2 mm, legs 6.0, wire r 0.32, paper 1.5; head lowers onto the paper 2.4-3.3 s, blade drives 7.0-9.6 (pierce) and
10.0-14.4 (curl, slow); below the paper each leg follows its groove: quarter circle r 0.6 then flat inward; folded tips end 3.9 mm apart),
check.py (wire centreline >= 0.369 mm from the anvil over the whole loop = clear by 0.05 mm; blade 6.40 in a 6.54 slot) PASS,
scene.html (hook 3/4 view -> front halves fade 3.4-4.2 -> front section -> left-groove macro 10.7-14.1 -> fade back 16.6-17.4; LOOP 20.0 s),
vo.py (Kokoro af_heart, 6 lines), audio.py (-15.1 LUFS, -3.0 dBTP, HP4k gap 20.0 dB), post.json (copy spellchecked: only hashtag/handle flags).
Facts: Wikipedia Stapler + US 4,315,589 (post.json sources).
Rebuild: venv(kokoro-onnx 0.6.1 numpy soundfile shapely): python kin.py; python check.py; python vo.py <ttsdir> vo; python audio.py vo; ../../tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); 2 workers: node tools/render/render.js wip/p063/scene.html <out> 30 1 0 600 0.9 1 <w> 2 1080 1920 1 (~4.5 s/frame/worker, ~23 min)
then tools/render/encode.sh <out> wip/p063/mix.wav stapler_reel.mp4 20 30
Left: final render -> encode -> HARD GATE -> clarity gate + visual review -> schedule 13 Nov 01:00.
