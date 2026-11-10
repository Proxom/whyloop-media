// Generic frame renderer (Playwright + swiftshader). Serve the REPO ROOT on :8765 (python3 -m http.server 8765).
// usage: node tools/render/render.js <scene path from repo root> <outdir> <fps> <sub|0=adaptive> <startFrame> <endFrame> [scale] [ao] [worker] [nworkers] [w] [h] [aa=0|1 SMAA]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [page, outdir, fps, sub, start, end, scale = '1', ao = '1', worker = '0', nworkers = '1', w = '1080', h = '1920', aa = '0'] = process.argv.slice(2);
  fs.mkdirSync(outdir, { recursive: true });
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } });
  p.setDefaultTimeout(180000);
  p.on('console', m => { if (m.type() === 'error') console.log('PAGE', m.text()); });
  p.on('pageerror', e => console.log('PAGEERR', e.message));
  await p.goto(`http://127.0.0.1:8765/${page}?scale=${scale}&ao=${ao}&w=${w}&h=${h}&aa=${aa}`);
  await p.waitForFunction('window.ready === true', null, { timeout: 180000 });
  const F = +fps, S = +sub; const t0 = Date.now(); let n = 0;
  for (let f = +start; f < +end; f++) {
    if (f % +nworkers !== +worker) continue;
    const file = `${outdir}/f${String(f).padStart(4, '0')}.png`;
    if (fs.existsSync(file)) continue; // resume support
    const t = f / F;
    let SS = S; if (S === 0) { const m = await p.evaluate(([t, F]) => window.motionPx ? window.motionPx(t, F) : 0, [t, F]); SS = Math.max(1, Math.min(4, Math.ceil(0.5 * m / 3.0))); }
    const url = await p.evaluate(([t, S, F]) => window.renderFrame(t, S, 0.5, F), [t, SS, F]);
    fs.writeFileSync(file, Buffer.from(url.split(',')[1], 'base64'));
    n++; if (n % 10 === 0) console.log(`w${worker} ${n} frames, ${((Date.now() - t0) / n / 1000).toFixed(2)} s/frame`);
  }
  console.log(`w${worker} done ${n} frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  await b.close();
})();
