# p053 seatbelt Part 2 "BRAKE HARD. / WHAT LOCKS?" - track A (Kokoro af_heart VO) - group V - for Instagram 9 Nov 2026 17:00
Delivers the Part 2 promised in p052 (vehicle sensor: a pendulum swings forward on hard braking and tips its catch into the lock wheel).
Done: kin.py (lock wheel 24 teeth RO 18 / RI 15, pendulum: brass bob on 15 mm rod + orange hooked catch arm 11 mm, pin P;
car deceleration ramps 0 -> 0.8 g (2.7-6.0 s), stop at 8.6 s, drive-off 11.8-13.4 s; pendulum 2nd order WN 2.6 ZETA 0.75 toward atan(a/g);
catch enters teeth 5.01 s, belt payout from 6.85 s, wall hits the catch 7.09 s = LOCK (on the VO word "Locked"), rewind 10.3-11.4 s lifts it out 10.68 s),
check.py (HARD GATE 5.2: overlap 0, wheel never moves while locked, loop closed), scene.html, vo.py.
Rebuild: python3 -m pip install shapely; python3 kin.py; python3 check.py
Render: python3 -m http.server 8765 (repo root); node tools/render/render.js wip/p053/scene.html <out> 30 0 0 450 1 1 0 1 1080 1920 (2.7 s/frame with AO)
