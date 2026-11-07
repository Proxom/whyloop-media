const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const [outdir, sub, ...frames] = process.argv.slice(2); fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } }); p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto('http://127.0.0.1:8765/scene.html'); await p.waitForFunction('window.ready === true', null, { timeout: 180000 });
  for (const f of frames) { const url = await p.evaluate(([t, S]) => window.renderFrame(t, S, 0.5, 30), [f / 30, +sub]); fs.writeFileSync(`${outdir}/qc_${String(f).padStart(4, '0')}.png`, Buffer.from(url.split(',')[1], 'base64')); }
  await b.close(); })();
