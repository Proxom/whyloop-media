// p052 seatbelt retractor (webbing-sensitive lock), simplified: a fixed lock plate with 24 inward-facing ratchet teeth
// (the p051 ring, now part of the frame) + the spool's locking disc carrying 2 weighted levers (pawls) on pivots.
// A light spring holds each lever in. Slow pull: the spool turns slowly, the levers stay in, the belt runs free.
// Yank: the spool spins fast, centrifugal force swings the weighted levers out, the lever tip catches the steep face
// of a tooth and the spool stops (locked). Release: the rewind spring turns the spool back, the tip leaves the tooth,
// the lever spring pulls the levers in, and the belt winds back to where it started (seamless loop).
// Unwind (belt out) = driver forward = clockwise seen from the camera. a_d = spool angle (rad), ring fixed (a_r = 0).
(function (root) {
  const TAU = Math.PI * 2, D = Math.PI / 180;
  const K = {};
  const P = { LOOP: 13.0, wSlow: 30 * D, T_SLOW: [0.25, 0.7, 3.0, 3.45], T_YANK: 3.9, wYank: 240 * D, yankRise: 0.3,
    wOn: 110 * D, wFull: 210 * D, tauLever: 0.1, DB0: -0.26, T_REL: [7.3, 7.6], wBack: 18 * D, T_REW: [7.9, 12.25] };
  function init(G) { K.G = G; K.N = G.N; K.Ri = G.Ri; K.Ro = G.Ro; K.pitch = TAU / G.N; K.PIV = G.pivot; K.LIM = G.lim; K.pawl = G.pawl; K.dense = resample(G.pawl, 0.05).filter(p => Math.hypot(p[0], p[1]) > 13.4); const tc = [14.45 * Math.cos(G.tipAng), 14.45 * Math.sin(G.tipAng)]; K.tipIdx = K.dense.map(p => Math.hypot(p[0] - tc[0], p[1] - tc[1]) < 0.9); }
  function resample(poly, step) { const out = []; for (let i = 0; i < poly.length; i++) { const a = poly[i], b = poly[(i + 1) % poly.length]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const n = Math.max(1, Math.ceil(L / step)); for (let k = 0; k < n; k++) out.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); } return out; }
  const sm = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
  function rprof(psi) { let s = (psi / K.pitch) % 1; if (s < 0) s += 1; return K.Ro - (K.Ro - K.Ri) * s; }
  function rotP(pt, db, side) { const c = Math.cos(db), s = Math.sin(db), V = K.PIV; const x = pt[0] - V[0], y = pt[1] - V[1]; let q = [V[0] + c * x - s * y, V[1] + s * x + c * y]; if (side) q = [-q[0], -q[1]]; return q; }
  function collides(db, rel, side = 0, tipOnly = false) { for (let i = 0; i < K.dense.length; i++) { if (tipOnly && !K.tipIdx[i]) continue; const q = rotP(K.dense[i], db, side); const r = Math.hypot(q[0], q[1]); if (r < K.Ri - 1e-9) continue; if (r > rprof(Math.atan2(q[1], q[0]) + rel) + 1e-6) return true; } return false; }
  const both = (db, rel, tip = false) => collides(db, rel, 0, tip) || collides(db, rel, 1, tip);
  // commanded spool speed before the lock (rad/s, forward = unwind)
  function wCmd(t) { const [a0, a1, b0, b1] = P.T_SLOW; if (t < P.T_YANK) { if (t < a0 || t > b1) return 0; if (t < a1) return P.wSlow * sm((t - a0) / (a1 - a0)); if (t < b0) return P.wSlow; return P.wSlow * (1 - sm((t - b0) / (b1 - b0))); }
    return P.wYank * sm((t - P.T_YANK) / P.yankRise); }
  // after the lock: small back-off (belt slack) then the rewind spring winds the spool back to 0
  function wBackProf(t) { const [r0, r1] = P.T_REL; if (t >= r0 && t <= r1) return -P.wBack * Math.sin(Math.PI * (t - r0) / (r1 - r0)); return 0; }
  function bump(t, a, b) { if (t < a || t > b) return 0; return Math.sin(Math.PI * (t - a) / (b - a)) ** 2; }
  function simulate(fps) {
    const H = 2400, dt = 1 / H, L = P.LOOP; let ad = 0, db = P.DB0, locked = false, tLock = null, adLock = 0, rewA = 0;
    const frames = [], events = []; const nF = Math.round(L * fps); let nextF = 0; let w = 0;
    // pre-integrate rewind bump area
    let bumpArea = 0; for (let i = 0; i < 20000; i++) { const t = P.T_REW[0] + (i + 0.5) / 20000 * (P.T_REW[1] - P.T_REW[0]); bumpArea += bump(t, ...P.T_REW) * (P.T_REW[1] - P.T_REW[0]) / 20000; }
    let backTotal = 0; for (let i = 0; i < 20000; i++) { const t = P.T_REL[0] + (i + 0.5) / 20000 * (P.T_REL[1] - P.T_REL[0]); backTotal += wBackProf(t) * (P.T_REL[1] - P.T_REL[0]) / 20000; }
    for (let step = 0; step <= Math.round(L * H); step++) {
      const t = step * dt;
      if (nextF < nF && t + 1e-9 >= nextF / fps) { frames.push({ t: nextF / fps, ad, db, w, lock: locked ? 1 : 0 }); nextF++; }
      if (!locked && tLock === null) w = wCmd(t);
      else if (locked) { w = 0; if (t >= P.T_REL[0]) { locked = false; } }
      if (tLock !== null && !locked) { w = t < P.T_REW[0] ? wBackProf(t) : -rewA * bump(t, ...P.T_REW); }
      // lever: centrifugal swing-out target from spool speed (spring preload holds it in below wOn), first-order lag
      if (!locked) { const tgt = P.DB0 + (K.LIM - P.DB0) * sm((Math.abs(w) - P.wOn) / (P.wFull - P.wOn)); db += (tgt - db) * (1 - Math.exp(-dt / P.tauLever)); }
      let adN = ad + w * dt; const relN = -adN;
      if (both(db, relN)) {
        if (w > 0 && both(db, relN, true)) { // tip meets a steep tooth face -> spool stops at contact
          let a = ad, b = adN; for (let i = 0; i < 40; i++) { const m = (a + b) / 2; if (both(db, -m)) b = m; else a = m; }
          adN = a; locked = true; tLock = t; adLock = a; w = 0; events.push({ t, type: 'lock' });
          rewA = (adLock + backTotal) / bumpArea;
        } else { // a tooth slope pushes the lever in
          let b = db; while (both(b, relN) && db - b < 0.4) b -= 0.0005; let a = db; for (let i = 0; i < 24; i++) { const m = (a + b) / 2; if (both(m, relN)) a = m; else b = m; } db = b;
        }
      }
      ad = adN;
    }
    return { frames, events, tLock, adLock, end: ad, endDb: db };
  }
  Object.assign(K, { P, init, rprof, rotP, collides, both, simulate, TAU, D });
  if (typeof module !== 'undefined') module.exports = K; else root.KIN = K;
})(typeof window !== 'undefined' ? window : globalThis);
