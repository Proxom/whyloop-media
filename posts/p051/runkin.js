const K = require('./kin.js'); const fs = require('fs'); K.init(JSON.parse(fs.readFileSync('geom.json')));
const D = Math.PI / 180; const [w0, wE] = (process.argv[2] || '95,62').split(',').map(Number);
const t0 = Date.now(); const r0 = K.simulate(240, w0 * D, wE * D); const r = K.simulate(240, r0.endWr, wE * D, r0.endDb, r0.endVdb); console.log('warm db', r0.endDb, '->', r.endDb, 'wr', r0.endWr / D, r.endWr / D);
const F = r.frames; const deg = x => (x / D).toFixed(2);
console.log('sim s', (Date.now() - t0) / 1000, 'frames', F.length, 'W_D deg/s', deg(r.W_D), 'end wr', deg(r.endWr), 'ring total', deg(r.endAr), 'driver total', deg(r.endAd), 'ring mod45', (r.endAr / D % 45).toFixed(3));
const clicks = r.events.filter(e => e.type === 'click'); console.log('clicks', clicks.length, clicks.slice(0, 8).map(e => e.t.toFixed(3) + ':' + e.v.toFixed(0)).join(' '), 'locks', r.events.filter(e => e.type === 'lock').map(e => e.t.toFixed(3)).join(' '));
for (const tq of [0, 2, 4, 8, 9, 9.6, 11, 12.9, 13.5, 16.9]) { const f = F[Math.round(tq * 240)]; console.log('t', tq, 'ad', deg(f.ad), 'ar', deg(f.ar), 'wr', deg(f.wr), 'db', f.db.toFixed(3), 'lock', f.lock); }
fs.writeFileSync('kin_240.json', JSON.stringify(F.map(f => ({ ad: +f.ad.toFixed(6), ar: +f.ar.toFixed(6), db: +f.db.toFixed(5) }))));
fs.writeFileSync('events.json', JSON.stringify(r.events.map(e => ({ t: +e.t.toFixed(4), type: e.type, v: e.v ? +e.v.toFixed(1) : 0 }))));
