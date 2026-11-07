// p049 tape measure: single source of truth for motion (browser + node). Units: mm, seconds, radians.
(function (root) {
  const LOOP = 18.0;
  const P = {
    rd: 15.0,          // drum (reel hub) outer radius: tape winds on this
    pitch: 0.72,       // radial pitch of tape layers (blade 0.45 thick + gap, shown thicker than real)
    tBlade: 0.45,
    R0: 25.0,          // outer radius of the wound tape when fully retracted
    G: [34.0, -31.0],  // guide point at the mouth, inside the case
    mouthX: 38.0,      // outer face of the case wall at the mouth
    hookT: 0.8,        // hook plate thickness
    post: 2.6,         // fixed center post radius
    s0: 2.95, s1: 13.6, sTurns: 6.0, sThick: 0.42, // spiral spring: inner radius, outer radius, turns at rest, thickness
    eMax1: 180, eMax0: 150,
  };
  // wound length when fully retracted
  const L0 = Math.PI * (P.R0 * P.R0 - P.rd * P.rd) / P.pitch;
  // spiral r(phi) = rd + pitch*phi/(2pi); length(Phi) = rd*Phi + pitch*Phi^2/(4pi)
  function PhiOf(Lw) { const a = P.pitch / (4 * Math.PI), b = P.rd; return (-b + Math.sqrt(b * b + 4 * a * Lw)) / (2 * a); }
  const Phi0 = PhiOf(L0);
  function tangent(R) { const [gx, gy] = P.G; const d = Math.hypot(gx, gy), phG = Math.atan2(gy, gx); return phG - Math.acos(R / d); }
  // tape state for extension e (mm of blade outside the retracted position)
  function tape(e) {
    const Phi = PhiOf(L0 - e); const R = P.rd + P.pitch * Phi / (2 * Math.PI);
    const thP = tangent(R); const c = tangent(P.R0) - Phi0; // drum angle 0 at e=0
    const alpha = thP - c - Phi; // CCW drum rotation (radians)
    return { e, Phi, R, thP, alpha, c, P: [R * Math.cos(thP), R * Math.sin(thP)] };
  }
  const sm = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
  const sm5 = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * u * (u * (u * 6 - 15) + 10); };
  // timeline
  const T = {
    snap0: [0.0, 1.70],      // release from eMax0 -> 0 (hook hits the case at 1.70)
    coverOff: [2.05, 3.55],  // housing cover sweeps away (cutaway)
    pull1: [4.35, 8.25],     // pull 0 -> eMax1 (arrow)
    release1: 9.35,          // let go
    snap1: [9.35, 11.30],    // eMax1 -> 0, hook clunk at 11.30
    coverOn: [12.6, 14.1],   // cover sweeps back
    pull2: [14.6, 18.0],     // pull 0 -> eMax0, released exactly at loop point
    vo: [0.12, 2.15, 4.35, 8.95, 13.35],
  };
  // spring-driven retraction: e = e0 * (1 - u^2) (constant pull, accelerates until the hook hits the case)
  function snap(e0, t, a, b) { const u = Math.max(0, Math.min(1, (t - a) / (b - a))); return e0 * (1 - u * u); }
  function eAt(t) {
    t = ((t % LOOP) + LOOP) % LOOP;
    if (t < T.snap0[1]) return snap(P.eMax0, t, T.snap0[0], T.snap0[1]);
    if (t < T.pull1[0]) return 0;
    if (t < T.pull1[1]) return P.eMax1 * sm5((t - T.pull1[0]) / (T.pull1[1] - T.pull1[0]));
    if (t < T.snap1[0]) return P.eMax1;
    if (t < T.snap1[1]) return snap(P.eMax1, t, T.snap1[0], T.snap1[1]);
    if (t < T.pull2[0]) return 0;
    // pull 2 ends at rest (velocity 0) at the loop point, matching the start of snap0
    const u = (t - T.pull2[0]) / (T.pull2[1] - T.pull2[0]); return P.eMax0 * sm(u);
  }
  // pulling force visible? (arrow alpha) - present whenever the tape is being pulled or held
  function pullAt(t) {
    t = ((t % LOOP) + LOOP) % LOOP;
    const win = (a, b, f = 0.18) => Math.max(0, Math.min(1, (t - a) / f, (b - t) / f));
    return Math.max(win(T.pull1[0] - 0.2, T.release1 + 0.05, 0.15), win(T.pull2[0] - 0.2, LOOP + 0.06, 0.15), t < 0.06 ? 1 - t / 0.06 : 0);
  }
  // cover clip fraction: 0 = cover on, 1 = fully cut away
  function coverAt(t) {
    t = ((t % LOOP) + LOOP) % LOOP;
    if (t < T.coverOff[0]) return 0;
    if (t < T.coverOff[1]) return sm((t - T.coverOff[0]) / (T.coverOff[1] - T.coverOff[0]));
    if (t < T.coverOn[0]) return 1;
    if (t < T.coverOn[1]) return 1 - sm((t - T.coverOn[0]) / (T.coverOn[1] - T.coverOn[0]));
    return 0;
  }
  // spiral spring: inner end hooked on the fixed post, outer end riveted to the drum (rotates with alpha)
  const aMax = tape(P.eMax1).alpha;
  function spring(alpha, n = 900) {
    const Th = P.sTurns * 2 * Math.PI + alpha; const w = Math.max(0, Math.min(1, alpha / aMax));
    const p = 0.62 + 0.75 * w; // coils crowd toward the drum wall at rest, toward the post when wound
    const psi0 = Math.PI / 2; const pts = [];
    for (let i = 0; i <= n; i++) { const u = i / n; const r = P.s0 + (P.s1 - P.s0) * Math.pow(u, p); const a = psi0 + u * Th; pts.push([r * Math.cos(a), r * Math.sin(a), r, a]); }
    return pts;
  }
  root.KIN = { LOOP, P, L0, Phi0, tape, eAt, pullAt, coverAt, spring, aMax, T, sm, sm5 };
  if (typeof module !== 'undefined') module.exports = root.KIN;
})(typeof window !== 'undefined' ? window : globalThis);
