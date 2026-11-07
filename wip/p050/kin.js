// p050 reversible ratchet: symmetric 24-tooth gear + rocking double-nose pawl + reversing lever (spring plunger).
// Units mm / radians, gear axis +Z, handle frame rotates by phi. Works in node (require) and browser (KIN.init(geom)).
(function (root) {
  const TAU = Math.PI * 2;
  const K = { G: null };
  const P = { amp: 15.8 * Math.PI / 180, acc: 2200, LOOP: 15.8 };
  // timeline: mode -1 = left nose A (tightens, gear CW seen from above), +1 = right nose B (loosens, gear CCW)
  // segments: [t0, t1, phiFrom(+1=+amp), phiTo]
  const DR = 1.3, PA = 0.35, FL = 1.3;
  const SEGS = []; let tt = 0;
  const seg = (a, b, d) => { SEGS.push([tt, tt + d, a, b]); tt += d; };
  for (let c = 0; c < 2; c++) { seg(1, -1, DR); seg(-1, -1, PA); seg(-1, 1, DR); seg(1, 1, PA); }
  const FLIP1 = [tt, tt + FL]; seg(1, 1, FL);
  for (let c = 0; c < 2; c++) { seg(1, -1, DR); seg(-1, -1, PA); seg(-1, 1, DR); seg(1, 1, PA); }
  const FLIP2 = [tt, tt + FL]; seg(1, 1, FL);
  P.LOOP = tt;
  function ease(u) { return u < 0 ? 0 : u > 1 ? 1 : u * u * u * (u * (6 * u - 15) + 10); }
  const sm = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
  function wrapT(t) { return ((t % P.LOOP) + P.LOOP) % P.LOOP; }
  function phiAt(t) { t = wrapT(t); for (const s of SEGS) if (t < s[1] + 1e-12) { const u = ease((t - s[0]) / (s[1] - s[0])); return P.amp * (s[2] + (s[3] - s[2]) * u); } return P.amp; }
  // lever: -1 (mode A) .. +1 (mode B); moves in the middle 0.5 s of each flip window
  function leverAt(t) { t = wrapT(t);
    const f = (W, a, b) => a + (b - a) * sm((t - (W[0] + 0.35)) / 0.5);
    if (t < FLIP1[0]) return -1; if (t < FLIP1[1]) return f(FLIP1, -1, 1);
    if (t < FLIP2[0]) return 1; return f(FLIP2, 1, -1); }
  function init(G) {
    K.G = G; K.N = G.N; K.Rr = G.Rr; K.Rt = G.Rt; K.pitch = TAU / G.N; K.PIV = G.pivot; K.SEL = G.sel;
    K.pawl = G.pawl; K.dense = resample(G.pawl, 0.06);
  }
  function rprof(psi) { let s = (psi / K.pitch) % 1; if (s < 0) s += 1; const u = 1 - Math.abs(2 * s - 1); return K.Rr + (K.Rt - K.Rr) * u; }
  function gearOutline(nPer = 24) { const pts = []; for (let k = 0; k < K.N; k++) for (let i = 0; i < nPer; i++) { const s = i / nPer; const a = (k + s) * K.pitch; const r = K.Rr + (K.Rt - K.Rr) * (1 - Math.abs(2 * s - 1)); pts.push([r * Math.cos(a), r * Math.sin(a)]); } return pts; }
  function resample(poly, step) { const out = []; for (let i = 0; i < poly.length; i++) { const a = poly[i], b = poly[(i + 1) % poly.length]; const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const n = Math.max(1, Math.ceil(L / step)); for (let k = 0; k < n; k++) out.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]); } return out; }
  function rotP(pt, db) { const c = Math.cos(db), s = Math.sin(db), V = K.PIV; const x = pt[0] - V[0], y = pt[1] - V[1]; return [V[0] + c * x - s * y, V[1] + s * x + c * y]; }
  function insideGear(x, y, thRel) { const r = Math.hypot(x, y); if (r > K.Rt + 1e-9) return false; if (r < K.Rr - 1e-9) return true; return r < rprof(Math.atan2(y, x) - thRel) - 1e-6; }
  function collides(db, thRel) { for (const p of K.dense) { const q = rotP(p, db); if (q[1] > -6) continue; if (insideGear(q[0], q[1], thRel)) return true; } return false; }
  // plunger: selector at SEL rotates by lever*LA; plunger axis points +y rotated; tip = first hit on the pawl outline
  const LA = 24 * Math.PI / 180;
  function plunger(lever, db) {
    const a = -lever * LA; const d = [-Math.sin(a), Math.cos(a)]; const o = K.SEL; let best = 1e9;
    const poly = K.pawl.map(p => rotP(p, db));
    for (let i = 0; i < poly.length; i++) { const A = poly[i], B = poly[(i + 1) % poly.length];
      const ex = B[0] - A[0], ey = B[1] - A[1]; const den = d[0] * ey - d[1] * ex; if (Math.abs(den) < 1e-12) continue;
      const tq = ((A[0] - o[0]) * ey - (A[1] - o[1]) * ex) / den; const u = ((A[0] - o[0]) * d[1] - (A[1] - o[1]) * d[0]) / den;
      if (tq > 0 && u >= 0 && u <= 1 && tq < best) best = tq; }
    return { ang: a, dir: d, len: best, tip: [o[0] + d[0] * best, o[1] + d[1] * best] };
  }
  // torque sign of the plunger on the pawl (tip x relative to pivot -> +x pushes nose B in = +db)
  function springDir(t, db) { const p = plunger(leverAt(t), db); const x = p.tip[0] - K.PIV[0]; return Math.max(-1, Math.min(1, x / 2.0)); }
  function simulate(fps, warm = 1) {
    const H = 2400, dt = 1 / H; const total = (warm + 1) * P.LOOP; const tStart = warm * P.LOOP;
    let phiPrev = phiAt(0); let thg = phiPrev + K.pitch * 0; let db = -0.155, vdb = 0;
    // settle start pose
    while (collides(db, thg - phiPrev)) db -= 0.0005;  // mode A lifts with -db
    const frames = [], events = []; const nF = Math.round(P.LOOP * fps); let nextF = 0; let maxPen = 0;
    for (let step = 0; step <= Math.round(total * H) + 2; step++) {
      const t = step * dt; const phi = phiAt(t); const dPhi = phi - phiPrev; let thRel = thg - phi;
      const sd = springDir(t, db); const s = sd >= 0 ? 1 : -1;   // engaged side: +1 -> nose B, -1 -> nose A
      if (collides(db, thRel)) {
        // nose B locks when thRel decreases (dPhi>0); nose A locks when thRel increases (dPhi<0)
        const lock = (s > 0 && dPhi > 0) || (s < 0 && dPhi < 0);
        if (lock) { let lo = 0, hi = 1; for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; if (collides(db, thg + m * dPhi - phi)) lo = m; else hi = m; } thg += hi * dPhi; thRel = thg - phi; }
        else { let b = db; while (collides(b, thRel) && Math.abs(b - db) < 0.05) b -= s * 0.0005; let a = db; for (let i = 0; i < 22; i++) { const m = (a + b) / 2; if (collides(m, thRel)) a = m; else b = m; } db = b; vdb = 0; }
      } else {
        const tw = wrapT(t); const inFlip = (tw > FLIP1[0] && tw < FLIP1[1]) || tw > FLIP2[0]; vdb += sd * (inFlip ? 70 : P.acc) * dt; let dbn = db + vdb * dt; const LIM = 0.2; if (dbn > LIM) { dbn = LIM; vdb = 0; } if (dbn < -LIM) { dbn = -LIM; vdb = 0; }
        if (collides(dbn, thRel)) { let a = dbn, b = db; for (let i = 0; i < 22; i++) { const m = (a + b) / 2; if (collides(m, thRel)) a = m; else b = m; }
          if (t >= tStart && Math.abs(vdb) > 12.0) events.push({ t: t - tStart, v: Math.abs(vdb), type: 'click' }); db = b; vdb = -vdb * 0.1; if (Math.abs(vdb) < 1.5) vdb = 0; }
        else db = dbn;
      }
      phiPrev = phi;
      if (t >= tStart - 1e-9) while (nextF < nF && (tStart + nextF / fps) <= t + 1e-9) { const tf = nextF / fps; frames.push({ t: tf, phi, thg, db, lever: leverAt(tf), pen: collides(db, thg - phi) ? 1 : 0 }); nextF++; }
    }
    return { frames, events, P };
  }
  Object.assign(K, { P, SEGS, FLIP1, FLIP2, phiAt, leverAt, init, rprof, gearOutline, rotP, collides, plunger, springDir, simulate, LA, TAU });
  if (typeof module !== 'undefined') module.exports = K; else root.KIN = K;
})(typeof window !== 'undefined' ? window : globalThis);
