// usage: node render.js outdir fps sub start end [scale] [ao] [times...]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [outdir, fps, sub, start, end, scale = '1', ao = '1', worker = '0', nworkers = '1'] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') console.log('PAGE', m.type(), m.text()); });
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto(`http://127.0.0.1:8765/scene.html?scale=${scale}&ao=${ao}`);
  await p.waitForFunction('window.ready === true', null, { timeout: 180000 });
  const F = +fps, S = +sub;
  const t0 = Date.now(); let n = 0;
  for (let f = +start; f < +end; f++) {
    if (f % +nworkers !== +worker) continue;
    const t = f / F;
    let SS = S; if (S === 0) { const m = await p.evaluate(([t, F]) => window.motionPx(t, F), [t, F]); SS = Math.max(1, Math.min(12, Math.ceil(0.5 * m / 3.0))); }
    const url = await p.evaluate(([t, S, F]) => window.renderFrame(t, S, 0.5, F), [t, SS, F]);
    fs.writeFileSync(`${outdir}/f${String(f).padStart(4, '0')}.png`, Buffer.from(url.split(',')[1], 'base64'));
    n++; if (n % 10 === 0) console.log(`w${worker} ${n} frames, ${((Date.now() - t0) / n / 1000).toFixed(2)} s/frame`);
  }
  console.log(`w${worker} done ${n} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  await b.close();
})();
