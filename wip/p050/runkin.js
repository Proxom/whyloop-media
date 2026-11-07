const K = require('./kin.js'); const fs = require('fs'); K.init(JSON.parse(fs.readFileSync('geom.json')));
const t0 = Date.now(); const r = K.simulate(240, 1);
fs.writeFileSync('kin_240.json', JSON.stringify(r.frames.map(f => ({ phi: +f.phi.toFixed(6), thg: +f.thg.toFixed(6), db: +f.db.toFixed(6), lever: +f.lever.toFixed(4) }))));
fs.writeFileSync('events.json', JSON.stringify(r.events));
const F = r.frames; const th = F.map(f => f.thg);
console.log('loop', K.P.LOOP, 'frames', F.length, 'clicks', r.events.length, 'sim s', (Date.now() - t0) / 1000);
const deg = x => (x * 180 / Math.PI).toFixed(2);
for (const tq of [0, 3.3, 6.6, 7.9, 11.2, 14.5, 15.7]) { const f = F[Math.round(tq * 240)]; console.log('t', tq, 'phi', deg(f.phi), 'thg', deg(f.thg), 'db', f.db.toFixed(3), 'lever', f.lever.toFixed(2)); }
console.log('closure thg end-start deg', deg(F[F.length - 1].thg - F[0].thg), 'db', F[0].db.toFixed(4), F[F.length - 1].db.toFixed(4));
console.log('penetrating frames', F.filter(f => f.pen).length);
console.log('click times', r.events.map(e => e.t.toFixed(2) + ':' + e.v.toFixed(0)).join(' '));
