// usage: node kit/test/profile.js "<page?query>" <w> <h> <scale> <aa>  -> ms per phase (3D render, overlay, PNG encode, JPEG encode)
const { chromium } = require('playwright');
(async () => { const [page, w, h, scale, aa] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await b.newPage({ viewport: { width: +w, height: +h } }); p.setDefaultTimeout(180000);
  await p.goto(`http://127.0.0.1:8765/${page}&w=${w}&h=${h}&scale=${scale}&aa=${aa}`); await p.waitForFunction('window.ready === true');
  await p.evaluate(() => window.renderFrame(1, 1, 0.5, 30));
  const r = await p.evaluate(() => { const N = 6; let a = 0, c = 0, d = 0; const cv = document.querySelector('canvas:last-of-type');
    for (let i = 0; i < N; i++) { const t0 = performance.now(); window.renderFrame(1 + i / 30, 1, 0.5, 30); const t1 = performance.now(); cv.toDataURL('image/png'); const t2 = performance.now(); cv.toDataURL('image/jpeg', 0.95); const t3 = performance.now(); a += t1 - t0; c += t2 - t1; d += t3 - t2; }
    return { renderFrameIncludingPNG: (a / N) | 0, extraPNG: (c / N) | 0, jpeg: (d / N) | 0 }; });
  console.log(scale, aa, JSON.stringify(r)); await b.close(); })();
