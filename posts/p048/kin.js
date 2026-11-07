// Single source of truth: ratchet geometry + kinematics (works in node and browser).
// Units mm, radians. Gear axis = +Z. Handle frame rotates by phi about origin.
(function (root) {
  const TAU = Math.PI * 2;
  const P = {
    N: 24, Rr: 12.0, Rt: 14.4, sSteep: 0.86,      // sawtooth: gentle rise s 0..0.86, steep drop 0.86..1
    pivot: [-10.5, 16.2],                          // pawl pivot in handle frame
    amp: 15.8 * Math.PI / 180,                     // stroke 31.6 deg = 2 teeth + 1.6 deg backlash
    phase: 0.55,                                   // video t=0 is mid-drive (pawl locked on a tooth)                       // handle swings +-17 deg (34 deg stroke)
    T: 3.0,                                        // seconds per cycle
    cycles: 4,                                     // loop = 4 cycles = 12 s, gear turns 120 deg (hex + 24-tooth symmetric)
    spring: { anchor: [1.2, 21.6], acc: 2200 },    // spring pushes pawl toward gear, angular accel rad/s^2
  };
  P.pitch = TAU / P.N;

  // gear profile radius at gear-frame angle psi
  function rprof(psi) {
    let s = (psi / P.pitch) % 1; if (s < 0) s += 1;
    if (s < P.sSteep) { const u = s / P.sSteep; return P.Rr + (P.Rt - P.Rr) * u; }
    const u = (s - P.sSteep) / (1 - P.sSteep); return P.Rt - (P.Rt - P.Rr) * u;
  }
  // gear outline polygon (gear frame), dense
  function gearOutline() {
    const pts = [];
    for (let k = 0; k < P.N; k++) {
      const a0 = k * P.pitch;
      const nA = 26, nB = 5;
      for (let i = 0; i < nA; i++) { const s = (i / nA) * P.sSteep; const a = a0 + s * P.pitch; const r = P.Rr + (P.Rt - P.Rr) * (s / P.sSteep); pts.push([r * Math.cos(a), r * Math.sin(a)]); }
      for (let i = 0; i < nB; i++) { const u = i / nB; const s = P.sSteep + u * (1 - P.sSteep); const a = a0 + s * P.pitch; const r = P.Rt - (P.Rt - P.Rr) * u; pts.push([r * Math.cos(a), r * Math.sin(a)]); }
    }
    return pts;
  }

  // Pawl outline defined at nominal pose (handle frame, tip in the valley at angle 90 deg), CCW order.
  const PIV = P.pivot;
  const nominal = [];
  (function buildPawl() {
    const add = (x, y) => nominal.push([x, y]);
    // nose (tip) - rounded
    add(-0.30, 12.32); add(-0.13, 12.30); add(-0.03, 12.40);
    // front (engaging) face up to top
    add(0.37, 14.95); add(0.30, 15.55);
    // top edge back toward pivot (spring seat around x ~ 0)
    add(-0.6, 16.05); add(-3.5, 17.2); add(-7.0, 18.35);
    // pivot boss arc (radius 2.7 around pivot), from top to bottom going left
    const R = 2.7;
    const aStart = Math.atan2(18.35 - PIV[1], -7.0 - PIV[0]);
    const aEnd = Math.atan2(14.0 - PIV[1], -8.6 - PIV[0]) + TAU;
    for (let i = 1; i < 22; i++) { const a = aStart + (aEnd - aStart) * i / 22; add(PIV[0] + R * Math.cos(a), PIV[1] + R * Math.sin(a)); }
    // lower edge toward the nose
    add(-8.6, 14.0); add(-5.0, 14.75); add(-2.55, 14.62);
    // back face of the nose (follows gentle slope but steeper so only the tip touches)
    add(-1.25, 13.55); add(-0.6, 12.7);
  })();
  // spring seat point on the pawl top edge (nominal)
  const seatNominal = [-0.9, 16.15];

  function resample(poly, step) {
    const out = [];
    for (let i = 0; i < poly.length; i++) {
      const a = poly[i], b = poly[(i + 1) % poly.length];
      const L = Math.hypot(b[0] - a[0], b[1] - a[1]); const n = Math.max(1, Math.ceil(L / step));
      for (let k = 0; k < n; k++) out.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]);
    }
    return out;
  }
  const pawlDense = resample(nominal, 0.06);
  // rotate a nominal point about the pivot by db
  function rotP(pt, db) { const c = Math.cos(db), s = Math.sin(db); const x = pt[0] - PIV[0], y = pt[1] - PIV[1]; return [PIV[0] + c * x - s * y, PIV[1] + s * x + c * y]; }
  function insideGear(x, y, thRel) { // point in handle frame; gear rotated by thRel relative to handle
    const r = Math.hypot(x, y); if (r > P.Rt + 1e-9) return false; if (r < P.Rr - 1e-9) return true;
    const psi = Math.atan2(y, x) - thRel; return r < rprof(psi) - 1e-6;
  }
  // db = pawl rotation from nominal (positive = CCW = lifts the nose, since pivot is to the left)
  function collides(db, thRel) {
    for (const p of pawlDense) { const q = rotP(p, db); if (insideGear(q[0], q[1], thRel)) return true; }
    return false;
  }
  const DB_LO = -0.06, DB_HI = 0.36;
  function dbContact(thRel) { // smallest collision-free db (assuming collision below, free above)
    if (!collides(DB_LO, thRel)) return DB_LO;
    if (collides(DB_HI, thRel)) return null;
    let lo = DB_LO, hi = DB_HI;
    for (let i = 0; i < 34; i++) { const m = (lo + hi) / 2; if (collides(m, thRel)) lo = m; else hi = m; }
    return hi;
  }

  function ease(u) { return u < 0 ? 0 : u > 1 ? 1 : u * u * u * (u * (6 * u - 15) + 10); }
  // handle angle over one cycle: drive CW (+amp -> -amp), pause, return CCW (-amp -> +amp), pause
  const SEG = { d0: 0.0, d1: 1.15, r0: 1.45, r1: 2.6 };
  function phiAt(t) {
    let u = (t % P.T + P.T) % P.T;
    if (u < SEG.d1) return P.amp - 2 * P.amp * ease(u / SEG.d1);
    if (u < SEG.r0) return -P.amp;
    if (u < SEG.r1) return -P.amp + 2 * P.amp * ease((u - SEG.r0) / (SEG.r1 - SEG.r0));
    return P.amp;
  }

  // Simulate: warm-up cycles then record. Returns sampled frames + click events.
  function simulate(fps, warm = 2) {
    const H = 2400, dt = 1 / H;
    const total = (warm + P.cycles) * P.T;
    let thg = 0.0, db = 0.0, vdb = 0.0;
    let phiPrev = phiAt(0);
    // start: gear placed so the tip sits in a valley at phi(0)
    thg = phiPrev; // thRel = 0 -> nominal valley
    db = dbContact(thg - phiPrev); if (db === null) db = 0;
    const tStart = warm * P.T;
    const frames = []; const events = [];
    const nF = Math.round(P.cycles * P.T * fps);
    let nextF = 0;
    let carrying = false;
    for (let step = 0; step <= Math.round(total * H) + 2; step++) {
      const t = step * dt;
      const phi = phiAt(t);
      let thRel = thg - phi;
      const dPhi = phi - phiPrev;
      if (collides(db, thRel)) {
        if (dPhi < 0) {
          // blocked direction: pawl cannot lift (self-engaging), gear is carried along
          let lo = 0, hi = 1;
          for (let i = 0; i < 30; i++) { const m = (lo + hi) / 2; const tr = (thg + m * dPhi) - phi; if (collides(db, tr)) lo = m; else hi = m; }
          thg = thg + hi * dPhi; thRel = thg - phi; carrying = true;
        } else if (dPhi > 0) {
          // free direction: the gentle slope lifts the pawl (continuous search upward)
          let a = db, b = db;
          while (collides(b, thRel) && b < db + 0.03) b += 0.0005;
          if (!collides(b, thRel)) { for (let i = 0; i < 22; i++) { const m = (a + b) / 2; if (collides(m, thRel)) a = m; else b = m; } db = b; vdb = 0; }
          carrying = false;
        } // dPhi == 0: numerical contact only, keep pose

      } else {
        carrying = false;
        vdb -= P.spring.acc * dt; let dbn = db + vdb * dt; if (dbn < DB_LO) { dbn = DB_LO; vdb = 0; }
        if (collides(dbn, thRel)) {
          let a = dbn, b = db; // a collides, b free
          for (let i = 0; i < 22; i++) { const m = (a + b) / 2; if (collides(m, thRel)) a = m; else b = m; }
          if (t >= tStart && -vdb > 12.0) events.push({ t: t - tStart, v: -vdb, type: 'click' });
          db = b; vdb = -vdb * 0.1; if (Math.abs(vdb) < 1.5) vdb = 0;
        } else db = dbn;
      }
      phiPrev = phi;
      if (t >= tStart - 1e-9) {
        while (nextF < nF && (tStart + nextF / fps) <= t + 1e-9) { frames.push({ t: nextF / fps, phi, thg, db, carrying }); nextF++; }
      }
    }
    return { frames, events, P };
  }

  const api = { P, rprof, gearOutline, nominal, pawlDense, seatNominal, rotP, collides, dbContact, phiAt, simulate, SEG, DB_LO, DB_HI, TAU };
  if (typeof module !== 'undefined') module.exports = api; else root.KIN = api;
})(typeof window !== 'undefined' ? window : globalThis);
