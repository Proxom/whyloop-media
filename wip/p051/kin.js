// p051 freehub: ring (hub shell, wheel) with 24 internal ratchet teeth + driver (cog) with 2 spring pawls.
// Forward = clockwise seen from the drive side. a_d = driver forward angle, a_r = ring forward angle (rad).
// Coast: driver stops, ring overruns -> teeth push the pawls in, the spring snaps them out (click).
// Pedal: driver turns forward faster than the ring -> pawl tip jams on the steep tooth face -> ring is carried.
(function (root) {
  const TAU = Math.PI * 2, D = Math.PI / 180;
  const K = {};
  const P = { LOOP: 18.5, acc: 2600, T_ON: [10.3, 10.9], T_OFF: [14.0, 14.6], tau: 9.0 };
  function init(G) { K.G = G; K.N = G.N; K.Ri = G.Ri; K.Ro = G.Ro; K.pitch = TAU / G.N; K.PIV = G.pivot; K.LIM = G.lim; K.pawl = G.pawl; K.dense = resample(G.pawl, 0.05).filter(p => Math.hypot(p[0], p[1]) > 13.4); const tc = [14.45 * Math.cos(G.tipAng), 14.45 * Math.sin(G.tipAng)]; K.tipIdx = K.dense.map(p => Math.hypot(p[0] - tc[0], p[1] - tc[1]) < 0.9); }
  function resample(poly, step) { const out = []; for (let i = 0; i < poly.length; i++) { const a = poly[i], b = poly[(i + 1) % poly.length]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const n = Math.max(1, Math.ceil(L / step)); for (let k = 0; k < n; k++) out.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); } return out; }
  const sm = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
  // driver speed profile (rad/s forward); W_D set by init so the driver turns exactly 360 deg per loop
  let W_D = 1;
  function wd(t) { const [a0, a1] = P.T_ON, [b0, b1] = P.T_OFF; if (t < a0 || t > b1) return 0; if (t < a1) return W_D * sm((t - a0) / (a1 - a0)); if (t < b0) return W_D; return W_D * (1 - sm((t - b0) / (b1 - b0))); }
  function calib() { W_D = 1; let s = 0; const n = 20000; for (let i = 0; i < n; i++) s += wd((i + 0.5) / n * P.LOOP) * P.LOOP / n; W_D = TAU / s; }
  function rprof(psi) { let s = (psi / K.pitch) % 1; if (s < 0) s += 1; return K.Ro - (K.Ro - K.Ri) * s; }
  function rotP(pt, db, side) { const c = Math.cos(db), s = Math.sin(db), V = K.PIV; const x = pt[0] - V[0], y = pt[1] - V[1]; let q = [V[0] + c * x - s * y, V[1] + s * x + c * y]; if (side) q = [-q[0], -q[1]]; return q; }
  // rel = a_r - a_d ; ring-frame angle of a driver-frame point = atan2 + rel
  function tipCollides(db, rel) { for (let i = 0; i < K.dense.length; i++) { if (!K.tipIdx[i]) continue; const q = rotP(K.dense[i], db, 0); const r = Math.hypot(q[0], q[1]); if (r < K.Ri - 1e-9) continue; if (r > rprof(Math.atan2(q[1], q[0]) + rel) + 1e-6) return true; } return false; }
  function collides(db, rel, side = 0) { for (const p of K.dense) { const q = rotP(p, db, side); const r = Math.hypot(q[0], q[1]); if (r < K.Ri - 1e-9) continue; if (r > rprof(Math.atan2(q[1], q[0]) + rel) + 1e-6) return true; } return false; }
  function simulate(fps, wr0, wrEnd, db0 = 0.2, vdb0 = 0) {
    calib(); const H = 2400, dt = 1 / H; const L = P.LOOP;
    // ring free speed: exponential decay between releases; wr0 at t=0
    let ad = 0, ar = 0, wr = wr0, db = db0, vdb = vdb0; let rel = 0;
    while (collides(db, rel)) db -= 0.0005;
    const frames = [], events = []; const nF = Math.round(L * fps); let nextF = 0; let locked = 0, maxLockStart = null;
    for (let step = 0; step <= Math.round(L * H); step++) {
      const t = step * dt;
      if (nextF < nF && t + 1e-9 >= nextF / fps) { frames.push({ t: nextF / fps, ad, ar, db, wr, lock: locked }); nextF++; }
      const dad = wd(t) * dt; ad += dad;
      const k = Math.exp(-dt / P.tau); const wfree = wrEnd + (wr - wrEnd) * k; let dar = wfree * dt;
      // lock: driver pushes ring when the free ring would be passed
      let relN = (ar + dar) - ad;
      if (collides(db, relN)) {
        if (relN < rel && tipCollides(db, relN)) { // driver overtaking, tip face on the steep tooth face -> ring carried to contact
          let lo = 0, hi = 1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (collides(db, (ar + dar + m * (rel - relN) * 0) + 0 - ad + m * 0) ) lo = m; else hi = m; }
          // solve ring angle so contact just clears: search x in [ar+dar, ar+dar+(rel-relN)]
          let a = ar + dar, b = ad + rel + 1e-9; for (let i = 0; i < 40; i++) { const m = (a + b) / 2; if (collides(db, m - ad)) a = m; else b = m; }
          dar = b - ar; relN = b - ad; if (!locked) events.push({ t, type: 'lock' }); locked = 1;
        } else { // ring overruns -> pawl pushed in
          let b = db; while (collides(b, relN) && db - b < 0.4) b -= 0.0005; let a = db; for (let i = 0; i < 24; i++) { const m = (a + b) / 2; if (collides(m, relN)) a = m; else b = m; } db = b; vdb = 0; locked = 0;
        }
      } else locked = 0;
      ar += dar; wr = dar / dt; rel = relN;
      // spring dynamics on the pawl
      vdb += P.acc * dt; let dbn = db + vdb * dt; if (dbn > K.LIM) { if (vdb > 8) events.push({ t, v: vdb, type: 'click' }); dbn = K.LIM; vdb = 0; }
      if (collides(dbn, rel)) { let a = dbn, b = db; for (let i = 0; i < 24; i++) { const m = (a + b) / 2; if (collides(m, rel)) a = m; else b = m; }
        if (Math.abs(vdb) > 8) events.push({ t, v: Math.abs(vdb), type: 'click' }); db = b; vdb = -vdb * 0.1; if (Math.abs(vdb) < 1) vdb = 0; }
      else db = dbn;
    }
    return { frames, events, W_D, endWr: wr, endAr: ar, endAd: ad, endDb: db, endVdb: vdb };
  }
  Object.assign(K, { tipCollides, P, init, rprof, rotP, collides, simulate, wd, TAU, D, get W_D() { return W_D; } });
  if (typeof module !== 'undefined') module.exports = K; else root.KIN = K;
})(typeof window !== 'undefined' ? window : globalThis);
