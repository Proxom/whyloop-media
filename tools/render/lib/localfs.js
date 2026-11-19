// Serve the repo root to the page without an HTTP server: every request to http://127.0.0.1:8765/<path> is answered from disk.
// Used by render.js and stills.js (sessions where a local server cannot be started). Read-only, repo root only.
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../../..');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.wav': 'audio/wav', '.css': 'text/css' };
module.exports = async function localfs(page) {
  await page.route('http://127.0.0.1:8765/**', async (route) => {
    const u = new URL(route.request().url()); const f = path.resolve(ROOT, '.' + decodeURIComponent(u.pathname));
    if (!f.startsWith(ROOT + path.sep) || !fs.existsSync(f) || fs.statSync(f).isDirectory()) return route.fulfill({ status: 404, body: 'not found' });
    route.fulfill({ status: 200, contentType: TYPES[path.extname(f)] || 'application/octet-stream', body: fs.readFileSync(f) });
  });
};
