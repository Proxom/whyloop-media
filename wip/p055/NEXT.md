# p055 door latch "WHY DOES IT / CLICK?" - track A (Kokoro af_heart VO) - group E - for Instagram 10 Nov 2026 17:00
Done: kin.py (latch bolt 12.8 wide, 46 deg slant toward the closing side, throw 12 -> 1 mm, door on a hinge 800 mm away, strike hole 1.0 mm play;
contact 4.01 s, snap 6.34 s, door on the stop 6.40 s, flat side holds 8.38 s at d=0.99 mm, handle 10.0-12.35 s, loop closed), check.py (overlap ~0),
scene.html (outside view with lever -> top cut sweep 2.45-3.5 -> section -> back 12.55-13.45), vo.py, audio.py (-15.2 LUFS, HP4k gap 19.6 dB).
Rebuild: python3 kin.py && python3 check.py; <kokoro venv>/python vo.py <ttsdir> vo; python3 audio.py vo; tools/render/master.sh vo_stem.wav bed_stem.wav mix.wav 4 -5 -15
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p055/scene.html <out> 30 0 0 450 1 1 0 1 1080 1920
Left: final render -> encode -> HARD GATE -> review -> schedule 10 Nov 17:00.
