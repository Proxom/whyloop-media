// HARD GATE 2: moving-pair clearance over one full loop (mm). Run: node check.js
const K = require('./kin.js'); const P = K.P; let r = { springPitchMin: 1e9, springPostGap: 1e9, springHubGap: 1e9, tapeWallGap: 1e9, hookWallGap: 1e9, hookBenchGap: 1e9, eMin: 1e9 };
const wallIn = { x0: -37.8, x1: 35.8, y0: -35.3, y1: 34.3 }, hubIn = P.rd - 1.0;
for (let i = 0; i < 18 * 240; i++) {
  const t = i / 240, e = K.eAt(t), s = K.tape(e); r.eMin = Math.min(r.eMin, e);
  const pts = K.spring(s.alpha, 3000);
  for (let a = 0; a < pts.length; a += 7) { let j = a; while (j < pts.length - 1 && pts[j][3] < pts[a][3] + 2 * Math.PI) j++; if (j < pts.length - 1) r.springPitchMin = Math.min(r.springPitchMin, pts[j][2] - pts[a][2] - P.sThick); }
  r.springPostGap = Math.min(r.springPostGap, P.s0 - P.sThick / 2 - P.post); r.springHubGap = Math.min(r.springHubGap, hubIn - (P.s1 + P.sThick / 2));
  const Rout = s.R + P.tBlade / 2 + 0.02; r.tapeWallGap = Math.min(r.tapeWallGap, wallIn.x1 - Rout, -wallIn.y0 - Rout, wallIn.y1 - Rout, -wallIn.x0 - Rout);
  r.hookWallGap = Math.min(r.hookWallGap, (P.mouthX + 0.05 + e) - P.mouthX); r.hookBenchGap = Math.min(r.hookBenchGap, (P.G[1] - 2.95 - 3.3) - (-37.5));
}
for (const k in r) r[k] = +r[k].toFixed(3); console.log(JSON.stringify(r)); const ok = Object.entries(r).every(([k, v]) => k === 'eMin' ? v >= 0 : v > 0); console.log(ok ? 'PASS' : 'FAIL');
