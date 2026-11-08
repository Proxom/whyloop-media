# p053 seatbelt Part 2 "BRAKE HARD. / WHAT LOCKS?" - track A (Kokoro af_heart VO) - group V - for Instagram 9 Nov 2026 17:00
Delivers the Part 2 promised in p052 (vehicle sensor: a pendulum swings forward on hard braking and tips its catch into the lock wheel).
Done: kin.py (lock wheel 24 teeth RO 18 / RI 15, pendulum: brass bob on 15 mm rod + orange hooked catch arm 11 mm, pin P;
car deceleration ramps 0 -> 0.8 g (2.7-6.0 s), stop at 8.6 s, drive-off 11.8-13.4 s; pendulum 2nd order WN 2.6 ZETA 0.75 toward atan(a/g);
catch enters teeth 5.01 s, belt payout from 6.85 s, wall hits the catch 7.09 s = LOCK (on the VO word "Locked"), rewind 10.3-11.4 s lifts it out 10.68 s),
check.py (HARD GATE 5.2: overlap 0, wheel never moves while locked, loop closed), scene.html, vo.py.
Rebuild: python3 -m pip install shapely; python3 kin.py; python3 check.py
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js posts/p053/scene.html <out> 30 0 0 450 1 1 0 1 1080 1920 (2.7 s/frame with AO)
Audio: Kokoro venv (kokoro-onnx 0.6.1; model = cat kokoro-q8-shards@1.0.0 parts, sha256 fbae9257...a1478 verified; voices.npz from kokoro-js@1.2.1),
  VO at 0.15/2.75/5.4/8.95/12.8 s ("Locked." lands on the lock at 7.09 s); python3 audio.py <vodir>; master.sh vo_stem bed_stem mix 4 -5 -15 -> -15.1 LUFS, -2.8 dBTP, HP4k gap 19.6 dB.
Round 1 final (2.1-2.6 s/frame with AO, 20.6 min): HARD GATE pass. Reviewer 6/10 (wants shadows/contrast, belt roll visible in the wide shot, hook text off the busy teeth, arrow style).
Round 2 fixes: wide camera azim -36 (roll + webbing visible), key 2.9 / fill 0.55 / rim 2.8, dark radial backing behind the hook card, bigger inertia arrow -> re-render.
