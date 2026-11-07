// HARD GATE 5.2: moving pairs over the full loop (240 Hz samples)
const K = require('./kin.js'); const fs = require('fs'); const G = JSON.parse(fs.readFileSync('geom.json')); K.init(G);
const F = JSON.parse(fs.readFileSync('kin_240.json'));
const inPoly = (p, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) { const [xi, yi] = poly[i], [xj, yj] = poly[j]; if ((yi > p[1]) !== (yj > p[1]) && p[0] < (xj - xi) * (p[1] - yi) / (yj - yi) + xi) c = !c; } return c; };
let pen = 0, outPocket = 0, minPl = 1e9, maxPl = 0, maxTipX = 0, maxDepth = 0;
for (const f of F) {
  const thRel = f.thg - f.phi;
  // penetration depth: how far the pawl must lift to clear (rad -> mm at the nose, 13.5 mm arm)
  if (K.collides(f.db, thRel)) { pen++; let d = 0; const s = f.db > 0 ? -1 : 1; while (K.collides(f.db + s * d, thRel) && d < 0.05) d += 0.00005; maxDepth = Math.max(maxDepth, d * 13.5); }
  for (const p of G.pawl) { const q = K.rotP(p, f.db); if (!inPoly(q, G.pocket)) outPocket++; }
  const pl = K.plunger(f.lever, f.db); minPl = Math.min(minPl, pl.len); maxPl = Math.max(maxPl, pl.len); maxTipX = Math.max(maxTipX, Math.abs(pl.tip[0]));
}
console.log(JSON.stringify({ samples: F.length, contactSamples: pen, maxPenetrationMm: +maxDepth.toFixed(4), pawlPointsOutsidePocket: outPocket, plungerLenMm: [+minPl.toFixed(2), +maxPl.toFixed(2)], plungerTipMaxX: +maxTipX.toFixed(2), gearClosureDeg: +((F[F.length - 1].thg - F[0].thg) * 180 / Math.PI).toFixed(3) }));
