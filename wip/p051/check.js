// HARD GATE 5.2: moving pairs over the full loop (240 Hz samples): pawl vs ring teeth (both pawls), pawl inside its driver pocket,
// loop closure (ring 4 full turns, driver 1 turn, pawl angle continuous).
const K = require('./kin.js'); const fs = require('fs'); const G = JSON.parse(fs.readFileSync('geom.json')); K.init(G);
const F = JSON.parse(fs.readFileSync('kin_240.json'));
const inPoly = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi) c = !c; } return c; };
let pen = 0, maxDepth = 0, inBody = 0, minDb = 9, maxDb = -9;
for (const f of F) { const rel = f.ar - f.ad; minDb = Math.min(minDb, f.db); maxDb = Math.max(maxDb, f.db);
  for (const side of [0, 1]) if (K.collides(f.db, rel, side)) { pen++; let d = 0; while (K.collides(f.db - d, rel, side) && d < 0.05) d += 0.00005; maxDepth = Math.max(maxDepth, d * 6.24); }
  // pawl must never overlap the driver body material (body polygon is the driver outline with the pockets cut out)
  for (const p of G.pawl) { const q = K.rotP(p, f.db, 0); const sh = [q[0] * 0.999, q[1] * 0.999]; if (Math.hypot(q[0], q[1]) < G.RD - 0.02 && inPoly(sh, G.body)) inBody++; } }
const D = 180 / Math.PI; const a = F[0], b = F[F.length - 1];
console.log(JSON.stringify({ samples: F.length, contactSamples: pen, maxPenetrationMm: +maxDepth.toFixed(4), pawlPointsInsideDriverBody: inBody, dbRange: [+minDb.toFixed(3), +maxDb.toFixed(3)],
  ringTotalDeg: +((b.ar - a.ar) * D).toFixed(3), driverTotalDeg: +((b.ad - a.ad) * D).toFixed(3), dbStartEnd: [a.db, b.db] }));
