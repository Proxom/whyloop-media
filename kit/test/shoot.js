// usage: node kit/test/shoot.js <page path> "<extra query>" <out.png> <w> <h> <t> [aa=0|1] [reps=1]
// Renders one still (and times it; reps>1 repeats the frame to measure s/frame). Serve the repo root on :8765.
const { chromium } = require('playwright') ;
const fs = require('fs');
(async () => { const [page, q, out, w, h, t, aa = '0', reps = '1'] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } }); p.setDefaultTimeout(180000);
  p.on('pageerror', e => console.log('PAGEERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('PAGE', m.text()); });
  await p.goto(`http://127.0.0.1:8765/${page}?w=${w}&h=${h}&aa=${aa}&${q}`); await p.waitForFunction('window.ready === true', null, { timeout: 180000 });
  let url; const t0 = Date.now(); for (let i = 0; i < +reps; i++) url = await p.evaluate(([t]) => window.renderFrame(t + 0.0001 * Math.random(), 1, 0.5, 30), [+t + i / 30]);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); console.log(out, ((Date.now() - t0) / 1000 / +reps).toFixed(2) + ' s/frame'); await b.close(); })();
