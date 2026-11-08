const K = require('./kin.js'); const fs = require('fs'); K.init(JSON.parse(fs.readFileSync('geom.json')));
const D = Math.PI / 180; const r = K.simulate(240); const F = r.frames;
console.log('tLock', r.tLock && r.tLock.toFixed(3), 'adLock deg', (r.adLock / D).toFixed(2), 'end ad deg', (r.end / D).toFixed(4), 'end db', r.endDb.toFixed(5));
for (const tq of [0, 1, 3, 3.9, 4.0, 4.1, 4.2, 4.3, 5, 7.3, 7.6, 8, 10, 12.3, 12.9]) { const f = F[Math.min(F.length - 1, Math.round(tq * 240))]; console.log('t', tq, 'ad', (f.ad / D).toFixed(2), 'db', f.db.toFixed(3), 'w', (f.w / D).toFixed(1), 'lock', f.lock); }
fs.writeFileSync('kin_240.json', JSON.stringify(F.map(f => ({ ad: +f.ad.toFixed(6), db: +f.db.toFixed(5), w: +f.w.toFixed(4), lock: f.lock }))));
fs.writeFileSync('events.json', JSON.stringify(r.events));
