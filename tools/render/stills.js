// usage: node tools/render/stills.js <scene path> <outdir> <sub> <scale> <ao> <w> <h> <t1> <t2> ...  (times in seconds)
const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [page, outdir, sub, scale, ao, w, h, ...times] = process.argv.slice(2); fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } }); p.setDefaultTimeout(180000); p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto(`http://127.0.0.1:8765/${page}?scale=${scale}&ao=${ao}&w=${w}&h=${h}`); await p.waitForFunction('window.ready === true', null, { timeout: 180000 });
  for (const t of times) { const t0 = Date.now(); const url = await p.evaluate(([t, S]) => window.renderFrame(t, S, 0.5, 30), [+t, +sub]);
    fs.writeFileSync(`${outdir}/s_${(+t).toFixed(2)}.png`, Buffer.from(url.split(',')[1], 'base64')); console.log('still', t, ((Date.now() - t0) / 1000).toFixed(1) + 's'); }
  await b.close(); })();
