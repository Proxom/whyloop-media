// WhyLoop STUDIO KIT (KIT DAY 16 Nov 2026, AGENT.md override 15 Nov 14:23).
// One fixed look for every Reel: studio env + light rig, 9 materials, 4 camera presets, one text style, parametric parts.
// Units: mm, y up, z toward the viewer. Serve the REPO ROOT on :8765; import from a scene page:
//   import * as K from '/kit/kit.js';   const st = K.makeKit({ dof: { focus: 420, aperture: 0.6 } });
// Every Reel after KIT DAY builds from this file only (add a missing part HERE, then test it in kit/test/parts.html).
import * as S from '/tools/render/lib/studio.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { SMAAPass } from 'three/addons/postprocessing/SMAAPass.js';
import { BokehPass } from 'three/addons/postprocessing/BokehPass.js';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';
export { S };
export const THREE = S.THREE;
const V3 = (x, y, z) => new THREE.Vector3(x, y, z);
const D2R = Math.PI / 180;

// =====================================================================================================
// 1. STUDIO: renderer, procedural softbox environment (HDRI-like reflections), light rig, backdrop
// =====================================================================================================
// Procedural "photo studio" environment: dark grey dome, one big overhead softbox, a key softbox (left-front),
// a tall strip light (right-back, gives the rim streak on metal), a warm floor bounce. Reflections on metal read as a real studio.
function studioEnvScene() {
  const sc = new THREE.Scene();
  const dome = new THREE.Mesh(new THREE.SphereGeometry(50, 48, 24), new THREE.ShaderMaterial({ side: THREE.BackSide, depthWrite: false,
    vertexShader: 'varying vec3 vP; void main(){ vP = normalize(position); gl_Position = projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
    fragmentShader: 'varying vec3 vP; void main(){ float h = vP.y; vec3 top = vec3(0.16,0.17,0.19), hor = vec3(0.07,0.075,0.085), flo = vec3(0.035,0.032,0.03);'
      + ' vec3 c = h > 0.0 ? mix(hor, top, smoothstep(0.0, 0.9, h)) : mix(hor, flo, smoothstep(0.0, 0.35, -h)); gl_FragColor = vec4(c, 1.0); }' }));
  sc.add(dome);
  const box = (w, h, intensity, color, pos, look) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ color: new THREE.Color(color).multiplyScalar(intensity), side: THREE.DoubleSide }));
    m.position.copy(pos); m.lookAt(look); sc.add(m); return m; };
  const O = V3(0, 0, 0);
  box(30, 18, 2.2, 0xfff6ea, V3(0, 30, 6), O);           // overhead softbox
  box(16, 22, 4.0, 0xfff0dc, V3(-28, 12, 26), O);        // key softbox (left front)
  box(5, 34, 5.5, 0xe4efff, V3(30, 10, -22), O);         // strip light (right back) -> rim streak
  box(4, 26, 2.5, 0xe9f1ff, V3(-30, 6, -24), O);         // second strip (left back)
  box(40, 12, 0.35, 0xc9a77f, V3(0, -18, 20), V3(0, 0, 0)); // warm floor bounce (front, below)
  box(60, 26, 1.5, 0xfff4e6, V3(8, 4, 40), O);           // broad front fill (faces turned to the camera never go black)
  return sc;
}
// Brushed / streak roughness map (for brushed steel) and fine grain noise (cast metal, plastic)
function streakTex(seed = 3, size = 1024) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d'); const r = S.rng(seed);
  g.fillStyle = 'rgb(120,120,120)'; g.fillRect(0, 0, size, size);
  for (let i = 0; i < 2600; i++) { const y = r() * size, v = 80 + r() * 100 | 0, a = 0.08 + r() * 0.25; g.strokeStyle = `rgba(${v},${v},${v},${a})`; g.lineWidth = 0.6 + r() * 1.6;
    const x0 = r() * size - 200, L = 150 + r() * size; g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + L, y + (r() - 0.5) * 2); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
export const grainTex = (seed = 9, amp = 22) => S.noiseTex(seed, 140, amp, 512);

// Render-quality presets (benchmarked KIT DAY on 4 swiftshader cores, see kit/README.md):
//   preview: 540x960, no SMAA, shadow 1024 | final: 1080x1920, SMAA, shadow 2048, VSM soft shadows. AO is OFF in the kit
//   (it cost +65 % render time on p068); contact shadows come from the soft shadow map + contactBlob() instead.
// Quality knobs from the URL (benchmarking): sh = shadow map size, st = shadow type (vsm|pcf), shr = shadow blur radius
const QK = new URLSearchParams(location.search);
export const QUALITY = { sh: +(QK.get('sh') || 1024), st: QK.get('st') || 'pcf', shr: +(QK.get('shr') || 6) };
export function makeKit({ fov = 30, bg = 0x16181c, envIntensity = 1.0, exposure = 1.0, dof = null, near = 5, far = 12000 } = {}) {
  const P = S.params(); const W = P.w, H = P.h; const RW = Math.round(W * P.scale), RH = Math.round(H * P.scale);
  const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(RW, RH, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = exposure; renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = QUALITY.st === 'vsm' ? THREE.VSMShadowMap : THREE.PCFSoftShadowMap; renderer.localClippingEnabled = true;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(bg);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(studioEnvScene(), 0.0, 0.1, 100, { size: 512 }).texture; scene.environmentIntensity = envIntensity;
  const camera = new THREE.PerspectiveCamera(fov, W / H, near, far);
  const rt = new THREE.WebGLRenderTarget(RW, RH, { type: THREE.HalfFloatType, samples: 0 });
  const composer = new EffectComposer(renderer, rt); composer.setPixelRatio(1); composer.setSize(RW, RH);
  composer.addPass(new RenderPass(scene, camera));
  let bokeh = null;
  if (dof) { bokeh = new BokehPass(scene, camera, { focus: dof.focus, aperture: (dof.aperture ?? 0.5) * 1e-4, maxblur: dof.maxblur ?? 0.006 }); composer.addPass(bokeh); }
  composer.addPass(new OutputPass());
  if (P.aa) composer.addPass(new SMAAPass(RW, RH));
  const out = document.createElement('canvas'); out.width = W; out.height = H; document.body.appendChild(out);
  const g2 = out.getContext('2d');
  // focus(distance mm) keeps the subject sharp while the camera moves: call it in setScene with the camera-to-target distance
  const focus = (d) => { if (bokeh) bokeh.uniforms.focus.value = d; };
  return { P, W, H, renderer, scene, camera, composer, out, g2, bokeh, focus };
}

// Fixed light rig (the env does most of the look; ONE shadow light keeps frames cheap). ctr = subject centre, s = subject size (mm).
// Key from the upper left front (soft VSM shadow), cool rim from the back right, warm low fill. Returns the lights for per-shot tweaks.
export function lightRig(scene, ctr = V3(0, 0, 0), s = 100, { key = 2.4, rim = 2.0, fill = 0.35, shadow = QUALITY.sh } = {}) {
  const k = new THREE.DirectionalLight(0xfff1e0, key); k.position.copy(V3(-1.3 * s, 2.4 * s, 1.8 * s).add(ctr)); k.target.position.copy(ctr);
  k.castShadow = true; k.shadow.mapSize.set(shadow, shadow); const c = k.shadow.camera; c.left = -1.6 * s; c.right = 1.6 * s; c.top = 1.6 * s; c.bottom = -1.6 * s; c.near = 0.5 * s; c.far = 7 * s;
  k.shadow.radius = QUALITY.shr; k.shadow.blurSamples = 12; k.shadow.bias = -0.0006; k.shadow.normalBias = 0.0; scene.add(k, k.target);
  const r = new THREE.DirectionalLight(0xd6e6ff, rim); r.position.copy(V3(1.8 * s, 1.2 * s, -2.0 * s).add(ctr)); r.target.position.copy(ctr); scene.add(r, r.target);
  const f = new THREE.DirectionalLight(0xffd9b0, fill); f.position.copy(V3(1.2 * s, -0.4 * s, 2.2 * s).add(ctr)); f.target.position.copy(ctr); scene.add(f, f.target);
  return { key: k, rim: r, fill: f };
}

// Seamless backdrop (dark graphite by default: metal and coloured parts pop; reviewers called the beige wall "flat").
// Adds a soft radial light pool behind the subject so the background is never one flat colour.
export function backdrop(scene, { floorY = -100, zFront = 1200, zBack = -500, R = 400, h = 3000, width = 6000, floor = '#2a2c31', wall = '#3a3e46', pool = true, poolY = null, lit = false, catcher = 1600, shadowOpacity = 0.5 } = {}) {
  const cy = S.cyclorama(scene, { floorY, zFront, zBack, R, h, width, floor, wall, rough: 0.92 });
  // UNLIT backdrop (KIT DAY benchmark: a lit cyclorama cost ~250 ms of a 1.1 s frame). Shadows land on a separate shadow-catcher floor.
  if (!lit) { const map = cy.material.map; cy.material.dispose(); cy.material = new THREE.MeshBasicMaterial({ map, side: THREE.DoubleSide }); cy.receiveShadow = false;
    const sc = new THREE.Mesh(new THREE.PlaneGeometry(catcher, catcher), new THREE.ShadowMaterial({ color: 0x000000, opacity: shadowOpacity }));
    sc.rotation.x = -Math.PI / 2; sc.position.set(0, floorY + 0.2, 0); sc.receiveShadow = true; scene.add(sc); cy.userData.catcher = sc; }
  if (pool) { const c = document.createElement('canvas'); c.width = c.height = 512; const g = c.getContext('2d'); const gr = g.createRadialGradient(256, 256, 10, 256, 256, 256);
    gr.addColorStop(0, 'rgba(255,240,220,0.20)'); gr.addColorStop(0.5, 'rgba(255,240,220,0.07)'); gr.addColorStop(1, 'rgba(255,240,220,0)'); g.fillStyle = gr; g.fillRect(0, 0, 512, 512);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
    const m = new THREE.Mesh(new THREE.PlaneGeometry(2.6 * R + 1200, 2.6 * R + 1200), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, toneMapped: false }));
    m.position.set(0, poolY ?? floorY + R + 500, zBack + 2); scene.add(m); }
  return cy;
}
// Soft dark contact blob under a resting object (static, costs nothing per frame). y = floor height, r = footprint radius.
export function contactBlob(scene, x, y, z, r, strength = 0.55) {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128);
  gr.addColorStop(0, `rgba(0,0,0,${strength})`); gr.addColorStop(0.55, `rgba(0,0,0,${strength * 0.45})`); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
  const t = new THREE.CanvasTexture(c); const m = new THREE.Mesh(new THREE.PlaneGeometry(2.6 * r, 2.6 * r), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false }));
  m.rotation.x = -Math.PI / 2; m.position.set(x, y + 0.3, z); m.renderOrder = 1; scene.add(m); return m;
}

// =====================================================================================================
// 2. MATERIALS (one call per scene; the same 9 looks everywhere). Scale = world mm per texture tile.
// =====================================================================================================
export function materials() {
  const streak = streakTex(3); streak.repeat.set(0.02, 0.02);
  const grain = grainTex(9, 26); grain.repeat.set(0.04, 0.04);
  const fine = grainTex(17, 14); fine.repeat.set(0.08, 0.08);
  const streakX = streak.clone(); streakX.rotation = Math.PI / 2; streakX.repeat.set(0.02, 0.02); streakX.needsUpdate = true;
  const phys = (o) => new THREE.MeshPhysicalMaterial(o);
  return {
    machined: phys({ color: 0xc8cdd3, metalness: 1, roughness: 0.48, roughnessMap: streakX, envMapIntensity: 1.3 }),             // gear steel: tool marks across the face width (no 'laminated' look)
    steel: phys({ color: 0xc3c8ce, metalness: 1, roughness: 0.34, roughnessMap: streak, anisotropy: 0.35, envMapIntensity: 1.15 }), // brushed steel
    alu: phys({ color: 0xb4b8bd, metalness: 1, roughness: 0.55, roughnessMap: grain, bumpMap: grain, bumpScale: 0.6 }),            // cast aluminium
    brass: phys({ color: 0xe7b85a, metalness: 1, roughness: 0.32, roughnessMap: fine, envMapIntensity: 1.2 }),
    chrome: phys({ color: 0xeef1f5, metalness: 1, roughness: 0.06, envMapIntensity: 1.4 }),
    plastic: phys({ color: 0x1d1f23, metalness: 0, roughness: 0.42, roughnessMap: fine, clearcoat: 0.15, clearcoatRoughness: 0.4 }), // black plastic
    rubber: phys({ color: 0x151515, metalness: 0, roughness: 0.88, bumpMap: grain, bumpScale: 0.3 }),
    cut: phys({ color: 0xd2261d, metalness: 0, roughness: 0.55, side: THREE.DoubleSide }),                    // cut-section red (cutaway faces)
    glass: phys({ color: 0xdfeaf2, metalness: 0, roughness: 0.04, transparent: true, opacity: 0.22, envMapIntensity: 1.6, depthWrite: false, side: THREE.DoubleSide }), // cheap glass (no transmission pass)
    paint: (color = 0xd8261c) => phys({ color, metalness: 0, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.1 }),      // enamel / painted housing
    innerWall: phys({ color: 0x6d737c, metalness: 0.3, roughness: 0.7 }),                                   // matte grey inside a housing (reads as depth, not a black hole)
    accent: phys({ color: 0xffb21f, metalness: 0.2, roughness: 0.35, emissive: 0x3a2400, emissiveIntensity: 0.6 }),          // highlight the active part
  };
}
// Highlight helper: blend a part's material toward the accent glow (a = 0..1). Keeps the original for restore.
export function glow(mesh, a, color = 0xffb21f) {
  mesh.traverse(o => { if (!o.isMesh) return; if (!o.userData.base) { o.userData.base = o.material; o.material = o.material.clone(); }
    const b = o.userData.base; o.material.emissive = new THREE.Color(color).multiplyScalar(0.55 * a); o.material.emissiveIntensity = 1;
    if (b.color) o.material.color.copy(b.color).lerp(new THREE.Color(color), 0.35 * a); });
}

// =====================================================================================================
// 3. CAMERA PRESETS -> keys for S.orbitCam: [t, tx, ty, tz, dist, elevDeg, azimDeg]. ctr = [x,y,z], s = subject size (mm).
//    hero: 3/4 view, whole object fills ~70 % of the width | cutaway: near-front, slightly closer | macro: the key contact fills the frame | top: plan view
// =====================================================================================================
export const CAM = {
  hero: (ctr, s) => [0, ...ctr, 3.3 * s, 16, 30],
  cutaway: (ctr, s) => [0, ...ctr, 2.7 * s, 8, 12],
  macro: (ctr, s) => [0, ...ctr, 1.15 * s, 6, 18],
  top: (ctr, s) => [0, ...ctr, 3.0 * s, 80, 0],
};
export const at = (t, key) => [t, ...key.slice(1)];               // retime a preset: at(4.5, CAM.macro([0,0,0], 40))
export function shoot(st, keys, t) { const c = S.orbitCam(keys, t); st.camera.position.copy(c.pos); st.camera.lookAt(c.target); st.camera.updateMatrixWorld(); st.focus(c.pos.distanceTo(c.target)); return c; }

// =====================================================================================================
// 4. TEXT STYLE (overlay, 1080x1920 design px; every size here passes the HARD GATE: hook >= 64, labels >= 44)
// =====================================================================================================
export const TXT = {
  // hook title: INSIDE IT badge + white/yellow two-line question (series template)
  hook: (g2, a, l1, l2, size = 124) => S.hookCard(g2, a, l1, l2, size, false),
  // red circle + arrow on the key part (screen px)
  circle: (g2, a, x, y, R = 90, from = [-240, 170]) => S.redCircle(g2, a, x, y, R, from),
  // numbered step label at the top of the action area
  step: (g2, a, n, text, size = 66) => S.caption(g2, a, text, 440, size, '#ffffff', n),
  // part tag pinned to a 3D point (screen px from toScreen)
  tag: (g2, a, text, px, py, dx = 120, dy = -90, color = '#ffd21f') => S.tag(g2, a, text, px, py, dx, dy, 46, color),
  // answer card: two lines, full opacity, dark plate (>= 2.5 s on screen)
  answer: (g2, a, l1, l2, y = 560) => { if (a <= 0) return; g2.save(); g2.globalAlpha = a; g2.fillStyle = 'rgba(10,12,16,0.72)'; S.rrect(g2, 90, y - 120, 810, 250, 28); g2.fill();
    g2.strokeStyle = '#ffd21f'; g2.lineWidth = 5; g2.stroke(); S.outlined(g2, l1, S.CX, y - 10, 70, '#ffffff'); S.outlined(g2, l2, S.CX, y + 90, 84, '#ffd21f'); g2.restore(); },
  // follow line (last 1-1.5 s, lower safe area)
  follow: (g2, a, text = 'FOLLOW → A NEW MACHINE EVERY DAY') => { if (a <= 0) return; g2.save(); g2.globalAlpha = a; g2.font = '44px Anton'; const w = g2.measureText(text).width + 44;
    S.rrect(g2, S.CX - w / 2, 1395 - 34, w, 68, 16); g2.fillStyle = 'rgba(12,14,20,0.86)'; g2.fill(); g2.strokeStyle = '#ffffff'; g2.lineWidth = 4; g2.stroke();
    g2.fillStyle = '#fff'; g2.textAlign = 'center'; g2.textBaseline = 'middle'; g2.fillText(text, S.CX, 1397); g2.restore(); },
  flash: (g2, a) => { if (a <= 0) return; g2.save(); g2.globalAlpha = a; g2.fillStyle = '#fff'; g2.fillRect(0, 0, 1080, 1920); g2.restore(); },
};

// =====================================================================================================
// 5. PARTS LIBRARY (all parametric, mm). Each returns a THREE.Group (axis conventions in the comment) plus helpers.
// =====================================================================================================
// lathe surfaces get a DoubleSide twin of their material (profile order then never matters)
const ds = (m) => { if (Array.isArray(m) || m.side === THREE.DoubleSide) return m; if (!m.userData.ds) { m.userData.ds = m.clone(); m.userData.ds.side = THREE.DoubleSide; } return m.userData.ds; };
const lathe = (prof, mat, seg = 96, phiStart = 0, phiLen = Math.PI * 2) => new THREE.Mesh(new THREE.LatheGeometry(prof.map(p => new THREE.Vector2(p[0], p[1])), seg, phiStart, phiLen), ds(mat));

// --- involute spur gear outline (z teeth, module m, pressure angle 20 deg), CCW points, centred at 0 ---
export function gearOutline(z, m, { pa = 20, backlash = 0.05, ptsPerFlank = 8 } = {}) {
  const rp = z * m / 2, rb = rp * Math.cos(pa * D2R), ra = rp + m, rf = Math.max(rp - 1.25 * m, 0.5 * m);
  const inv = (a) => Math.tan(a) - a; const half = (Math.PI / (2 * z)) - backlash / (2 * rp) + inv(pa * D2R); // half tooth angle at the base circle
  const pts = [];
  for (let i = 0; i < z; i++) { const c = i * 2 * Math.PI / z; const fl = [];
    for (let k = 0; k <= ptsPerFlank; k++) { const r = Math.max(rb, rf) + (ra - Math.max(rb, rf)) * k / ptsPerFlank; const a = Math.acos(Math.min(1, rb / r)); fl.push([r, inv(a)]); }
    const a0 = c - half, a1 = c + half; const gap = Math.PI / z;

    const ra0 = a0 - 0.012, ra1 = a1 + 0.012, rootArc = (from, to) => { for (let k = 1; k <= 3; k++) { const a = from + (to - from) * k / 3; pts.push([rf * Math.cos(a), rf * Math.sin(a)]); } };
    rootArc(c - 2 * gap + half + 0.012, ra0);   // root arc from the previous tooth's right flank to this tooth's left flank
    if (rb > rf) pts.push([rb * 0.995 * Math.cos(a0), rb * 0.995 * Math.sin(a0)]);
    for (const [r, e] of fl) pts.push([r * Math.cos(a0 + e), r * Math.sin(a0 + e)]);
    for (const [r, e] of fl.slice().reverse()) pts.push([r * Math.cos(a1 - e), r * Math.sin(a1 - e)]);
    if (rb > rf) pts.push([rb * 0.995 * Math.cos(a1), rb * 0.995 * Math.sin(a1)]);
    pts.push([rf * Math.cos(ra1), rf * Math.sin(ra1)]); }
  return pts;
}
// Spur gear: axis = z, faces at z = -w/2..w/2, hub bore + optional spokes holes. info: { rp, ra, rf, z, m }
export function spurGear(mat, { z = 20, m = 2, w = 8, bore = 0, holes = 0, chamfer = 0.4 } = {}) {
  const pts = gearOutline(z, m); const rp = z * m / 2;
  const holesArr = []; if (bore > 0) holesArr.push(S.circle(0, 0, bore / 2, 48, true));
  if (holes > 0 && rp > 10) { const rr = (rp - 1.25 * m) * 0.62, hr = (rp - 1.25 * m) * 0.22; for (let i = 0; i < holes; i++) { const a = i * 2 * Math.PI / holes; holesArr.push(S.circle(rr * Math.cos(a), rr * Math.sin(a), hr, 32, true)); } }
  const g = new THREE.Group(); g.add(S.extrude(S.shapeOf(pts, holesArr), -w / 2, w / 2, mat, chamfer, 6));
  g.userData = { rp, ra: rp + m, rf: rp - 1.25 * m, z, m };
  return g;
}
// Mesh angle for gear 2 driven by gear 1: theta2 = -theta1 * z1/z2 + phase (phase aligns a gap with a tooth on the centre line)
export const meshAngle = (theta1, z1, z2, dir = 0) => -theta1 * z1 / z2 + Math.PI / z2 + dir * (1 + z1 / z2);
// Bevel gear: tapered extrusion of the spur outline. Axis = z (teeth face +z / apex direction). cone = pitch cone half angle (deg, 45 for a 1:1 miter pair).
export function bevelGear(mat, { z = 20, m = 2, w = 7, cone = 45, bore = 0 } = {}) {
  const rp = z * m / 2, apex = rp / Math.tan(cone * D2R); const k = (apex - w * Math.cos(cone * D2R)) / apex; // outer face scale 1 at z=0, inner face scale k at z=w
  const outline = gearOutline(z, m); const n = outline.length;
  const pos = [], idx = [];
  const ring = (sc, zz) => { for (const [x, y] of outline) pos.push(x * sc, y * sc, zz); };
  ring(1, 0); ring(k, w * Math.sin(cone * D2R) * 0 + w);
  for (let i = 0; i < n; i++) { const j = (i + 1) % n; idx.push(i, j, n + i, j, n + j, n + i); }
  let side = new THREE.BufferGeometry(); side.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); side.setIndex(idx); side = side.toNonIndexed(); side.computeVertexNormals(); { const p = side.attributes.position, uv = []; for (let i = 0; i < p.count; i++) uv.push(Math.atan2(p.getY(i), p.getX(i)) * rp * 0.05, p.getZ(i) * 0.05); side.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); } // uv needed by anisotropic steel // flat facets: crisp tooth edges
  const g = new THREE.Group(); const sm = new THREE.Mesh(side, ds(mat)); g.add(sm);
  const holes = bore > 0 ? [S.circle(0, 0, bore / 2, 48, true)] : [];
  const cap0 = new THREE.Mesh(new THREE.ShapeGeometry(S.shapeOf(outline, holes)), mat); cap0.rotation.y = Math.PI; cap0.scale.x = -1; g.add(cap0);
  const cap1 = new THREE.Mesh(new THREE.ShapeGeometry(S.shapeOf(outline.map(([x, y]) => [x * k, y * k]), holes)), mat); cap1.position.z = w; g.add(cap1);
  // back hub
  const hub = lathe([[bore / 2 || 0.01, -0.01], [rp * 0.55, -0.01], [rp * 0.5, -w * 0.6], [bore / 2 || 0.01, -w * 0.6]], mat, 64); hub.rotation.x = Math.PI / 2; g.add(hub);
  g.userData = { rp, apex, z, m };
  return g;
}
// Rack: teeth along +x, tooth tips toward +y, pitch line at y = 0, length L, thickness w (z), body height h below the roots.
export function rack(mat, { m = 2, L = 120, w = 8, h = 8, pa = 20 } = {}) {
  const p = Math.PI * m, ad = m, de = 1.25 * m, t = Math.tan(pa * D2R); const pts = [];
  const n = Math.floor(L / p); const x0 = -n * p / 2;
  pts.push([x0, -de - h]); pts.push([x0 + n * p, -de - h]);
  for (let i = n - 1; i >= 0; i--) { const c = x0 + (i + 0.5) * p; const hw = p / 4; // half tooth width at the pitch line
    pts.push([c + hw + de * t, -de]); pts.push([c + hw - ad * t, ad]); pts.push([c - hw + ad * t, ad]); pts.push([c - hw - de * t, -de]); }
  pts.reverse();
  const g = new THREE.Group(); g.add(S.extrude(S.shapeOf(pts), -w / 2, w / 2, mat, 0.3, 2)); g.userData = { pitch: p, n, x0 }; return g;
}
// Helical spring along +y from y=0 to y=len. Call setLength(len) every frame to compress/stretch it (ends stay closed and ground).
export function spring(mat, { R = 8, wire = 1.2, turns = 8, len = 60, closed = 1 } = {}) {
  const mesh = new THREE.Mesh(new THREE.BufferGeometry(), mat);
  const build = (L) => { const N = Math.round(turns * 40), pts = []; const ce = closed * 2 * wire; // closed end turns pitch = wire diameter
    for (let i = 0; i <= N; i++) { const u = i / N, a = u * turns * 2 * Math.PI; const tc = closed / turns; let y;
      if (u < tc) y = wire + ce * (u / tc) * 0.5; else if (u > 1 - tc) y = L - wire - ce * ((1 - u) / tc) * 0.5; else y = wire + ce * 0.5 + (L - 2 * wire - ce) * ((u - tc) / (1 - 2 * tc));
      pts.push(V3(R * Math.cos(a), y, R * Math.sin(a))); }
    mesh.geometry.dispose(); mesh.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), N * 2, wire, 10); };
  build(len); mesh.userData.setLength = build; mesh.setLength = build; return mesh;
}
// Shaft with chamfered ends along the z axis, centred at 0.
export function shaft(mat, { d = 8, L = 80, ch = 0.6 } = {}) {
  const r = d / 2; const m = lathe([[0, -L / 2], [r - ch, -L / 2], [r, -L / 2 + ch], [r, L / 2 - ch], [r - ch, L / 2], [0, L / 2]], mat, 48); m.rotation.x = Math.PI / 2;
  const g = new THREE.Group(); g.add(m); return g; // wrapped: callers may set the group's rotation freely
}
// Deep-groove ball bearing, axis z. Returns group with .setSpin(innerAngle) (outer fixed; balls + cage at ~0.4x).
export function ballBearing(mats, { d = 10, D = 26, B = 8, balls = 8 } = {}) {
  const g = new THREE.Group(); const ri = d / 2, ro = D / 2, rm = (ri + ro) / 2, rb = (ro - ri) * 0.3;
  const outer = lathe([[rm + rb * 0.55, -B / 2], [ro, -B / 2], [ro, B / 2], [rm + rb * 0.55, B / 2], [rm + rb * 0.9, 0.0]], mats.steel ?? mats, 96); outer.rotation.x = Math.PI / 2; g.add(outer);
  const inner = lathe([[ri, -B / 2], [rm - rb * 0.55, -B / 2], [rm - rb * 0.9, 0.0], [rm - rb * 0.55, B / 2], [ri, B / 2]], mats.steel ?? mats, 96); inner.rotation.x = Math.PI / 2; g.add(inner);
  const cage = new THREE.Group(); g.add(cage);
  for (let i = 0; i < balls; i++) { const a = i * 2 * Math.PI / balls; const b = new THREE.Mesh(new THREE.SphereGeometry(rb, 24, 16), mats.chrome ?? mats); b.position.set(rm * Math.cos(a), rm * Math.sin(a), 0); cage.add(b); }
  g.setSpin = (a) => { inner.rotation.z = a; cage.rotation.z = a * ri / (ri + ro); };
  return g;
}
// Ratchet wheel (sawtooth, axis z, teeth point CCW-forward) + pawl on a pivot. pose(wheelAngle) drops the pawl tip onto the teeth (no overlap).
export function ratchet(mats, { z = 12, Ro = 30, depth = 6, w = 8, pivot = [0, 50], pawlLen = 30 } = {}) {
  const pts = []; for (let i = 0; i < z; i++) { const a0 = i * 2 * Math.PI / z, a1 = (i + 1) * 2 * Math.PI / z;
    for (let k = 0; k <= 6; k++) { const u = k / 6, a = a0 + (a1 - a0) * u * 0.92, r = Ro - depth + depth * u; pts.push([r * Math.cos(a), r * Math.sin(a)]); }
    pts.push([(Ro - depth) * Math.cos(a1), (Ro - depth) * Math.sin(a1)]); }
  const g = new THREE.Group(); const wheel = new THREE.Group(); wheel.add(S.extrude(S.shapeOf(pts, [S.circle(0, 0, 5, 32, true)]), -w / 2, w / 2, mats.steel, 0.3, 4)); g.add(wheel);
  // pawl: tapered arm from the pivot, tip pointing toward the wheel
  const pawl = new THREE.Group(); pawl.position.set(pivot[0], pivot[1], 0); g.add(pawl);
  const arm = [[-4, 4], [pawlLen * 0.2, 5], [pawlLen, 1.2], [pawlLen + 1.5, -1.5], [pawlLen * 0.2, -5], [-4, -4]];
  pawl.add(S.extrude(S.shapeOf(arm.concat([[-6.5, 0]]).reverse()), -w / 2 + 0.6, w / 2 - 0.6, mats.brass, 0.3, 4));
  const pin = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.2, w + 4, 24), mats.chrome); pin.rotation.x = Math.PI / 2; pawl.add(pin);
  // radius of the sawtooth at polar angle phi (wheel frame)
  const rAt = (phi) => { const per = 2 * Math.PI / z; let u = (((phi % per) + per) % per) / per; return u <= 0.92 ? Ro - depth + depth * (u / 0.92) : Ro - depth; };
  const base = Math.atan2(-pivot[1], -pivot[0]); // pawl angle pointing at the wheel centre
  g.pose = (wa) => { wheel.rotation.z = wa; let lo = base - 1.2, hi = base + 0.0; // rotate the pawl from 'lifted' (lo) toward the wheel until the tip touches
    const tipAt = (pa) => [pivot[0] + (pawlLen + 1) * Math.cos(pa), pivot[1] + (pawlLen + 1) * Math.sin(pa)];
    const inside = (pa) => { const [x, y] = tipAt(pa); return Math.hypot(x, y) < rAt(Math.atan2(y, x) - wa) + 0.25; };
    if (!inside(hi)) { pawl.rotation.z = hi; return hi; }
    for (let i = 0; i < 30; i++) { const mid = (lo + hi) / 2; if (inside(mid)) hi = mid; else lo = mid; } pawl.rotation.z = lo; return lo; };
  g.wheel = wheel; g.pawl = pawl; g.pose(0); return g;
}
// Slider-crank: crank (axis z at origin), connecting rod, piston sliding on +y. pose(theta) -> piston height. r = crank radius, l = rod length.
export function pistonCrank(mats, { r = 20, l = 70, bore = 44, w = 10 } = {}) {
  const g = new THREE.Group();
  const crank = new THREE.Group(); g.add(crank);
  { const web = S.extrude(S.shapeOf(S.roundRect(-9, -9, r + 9, 9, 9)), -w, -w / 2 + 0.5, mats.steel, 0.5, 6); crank.add(web);
    const cw = S.extrude(S.shapeOf((() => { const a = []; for (let i = 0; i <= 24; i++) { const t = Math.PI * 0.62 + i / 24 * Math.PI * 0.76; a.push([r * 1.1 * Math.cos(t), r * 1.1 * Math.sin(t)]); } a.push([0, 0]); return a; })().reverse()), -w, -w / 2 + 0.5, mats.steel, 0.5, 6); crank.add(cw);
    const pinM = new THREE.Mesh(new THREE.CylinderGeometry(4.5, 4.5, w + 2, 32), mats.chrome); pinM.rotation.x = Math.PI / 2; pinM.position.set(r, 0, -1); crank.add(pinM);
    const main = new THREE.Mesh(new THREE.CylinderGeometry(6, 6, w * 2.4, 32), mats.chrome); main.rotation.x = Math.PI / 2; main.position.z = -w; crank.add(main); }
  const rod = new THREE.Group(); g.add(rod);
  { const body = S.extrude(S.shapeOf(S.roundRect(-3.2, 4, 3.2, l - 4, 3)), -3, 3, mats.alu, 0.4, 4); rod.add(body);
    const big = lathe([[5, -3.5], [9, -3.5], [9, 3.5], [5, 3.5]], mats.alu, 48); big.rotation.x = Math.PI / 2; rod.add(big);
    const small = lathe([[3.5, -3.5], [6.5, -3.5], [6.5, 3.5], [3.5, 3.5]], mats.alu, 48); small.rotation.x = Math.PI / 2; small.position.y = l; rod.add(small); }
  const piston = new THREE.Group(); g.add(piston);
  { const R = bore / 2 - 0.4; const body = lathe([[0, 0], [R - 1, 0], [R, 1], [R, 30], [R - 0.8, 31], [0, 31]], mats.alu, 72); body.position.y = -10; piston.add(body);
    for (const y of [16, 20, 24]) { const ring = new THREE.Mesh(new THREE.TorusGeometry(R + 0.05, 0.7, 8, 72), mats.plastic); ring.rotation.x = Math.PI / 2; ring.position.y = -10 + y; piston.add(ring); }
    const pin = new THREE.Mesh(new THREE.CylinderGeometry(3.5, 3.5, bore - 6, 24), mats.chrome); pin.rotation.x = Math.PI / 2; piston.add(pin); }
  g.pose = (th) => { crank.rotation.z = th; const cx = r * Math.cos(th), cy = r * Math.sin(th); const py = cy + Math.sqrt(l * l - cx * cx); // piston pin on the y axis
    rod.position.set(cx, cy, 0); rod.rotation.z = Math.atan2(cx, py - cy); piston.position.set(0, py, 0); return py; };
  g.crank = crank; g.rod = rod; g.piston = piston; g.userData = { r, l }; g.pose(Math.PI / 2); return g;
}
// Disc cam (axis z) + flat-faced follower on +y. profile(phi) = radius at polar angle phi. pose(theta) -> follower lift (exact for a flat follower).
export function camFollower(mats, { base = 18, lift = 10, w = 8, profile = null } = {}) {
  const prof = profile ?? ((phi) => { const u = Math.cos(phi - Math.PI / 2); return base + lift * Math.pow(Math.max(0, u), 3); }); // pear lobe pointing +y at theta=0
  const pts = []; for (let i = 0; i < 180; i++) { const a = i / 180 * 2 * Math.PI; const rr = prof(a); pts.push([rr * Math.cos(a), rr * Math.sin(a)]); }
  const g = new THREE.Group(); const cam = new THREE.Group(); cam.add(S.extrude(S.shapeOf(pts, [S.circle(0, 0, 4, 32, true)]), -w / 2, w / 2, mats.steel, 0.4, 4)); g.add(cam);
  const fol = new THREE.Group(); g.add(fol);
  { const foot = S.extrude(S.shapeOf(S.roundRect(-14, 0, 14, 4, 1.5)), -w / 2 - 1, w / 2 + 1, mats.brass, 0.3, 4); fol.add(foot);
    const stem = new THREE.Mesh(new THREE.CylinderGeometry(3.5, 3.5, 50, 24), mats.chrome); stem.position.y = 29; fol.add(stem); }
  g.pose = (th) => { cam.rotation.z = th; let h = 0; for (const [x, y] of pts) { const yy = x * Math.sin(th) + y * Math.cos(th); if (yy > h) h = yy; } fol.position.y = h; return h; };
  g.cam = cam; g.follower = fol; g.pose(0); return g;
}
// Lever: flat bar with a pivot boss at the origin and a round knob at +x (length L). Rotate about z.
export function lever(mats, { L = 90, w = 12, t = 5, knob = 7 } = {}) {
  const g = new THREE.Group(); g.add(S.extrude(S.shapeOf(S.roundRect(-w / 2, -w / 2, L, w / 2, w / 2 - 0.5), [S.circle(0, 0, 2.6, 24, true)]), -t / 2, t / 2, mats.steel, 0.5, 6));
  const boss = lathe([[2.6, -t / 2 - 1.5], [w * 0.62, -t / 2 - 1.5], [w * 0.62, t / 2 + 1.5], [2.6, t / 2 + 1.5]], mats.steel, 48); boss.rotation.x = Math.PI / 2; g.add(boss);
  const k = new THREE.Mesh(new THREE.SphereGeometry(knob, 32, 20), mats.plastic); k.position.set(L, 0, 0); g.add(k); return g;
}
// Wheel: rubber tyre + aluminium rim + 5-spoke disc, axis z, radius R (outer tyre).
export function wheel(mats, { R = 60, W = 24, spokes = 5 } = {}) {
  const g = new THREE.Group(); const tr = W * 0.42, rr = R - tr * 1.6;
  const tyre = new THREE.Mesh(new THREE.TorusGeometry(R - tr, tr, 24, 96), mats.rubber); tyre.scale.z = W / (2 * tr); g.add(tyre);
  const rim = lathe([[rr - 3, -W / 2 + 2], [rr + 1.5, -W / 2 + 1], [rr + 2.5, -W / 2 + 3], [rr, -W / 2 + 5], [rr - 1, W / 2 - 5], [rr + 2.5, W / 2 - 3], [rr + 1.5, W / 2 - 1], [rr - 3, W / 2 - 2]], mats.alu, 96); rim.rotation.x = Math.PI / 2; g.add(rim);
  const hub = lathe([[0, 2], [rr * 0.22, 2], [rr * 0.25, -2], [0, -2]], mats.chrome, 48); hub.rotation.x = Math.PI / 2; hub.position.z = W * 0.12; g.add(hub);
  for (let i = 0; i < spokes; i++) { const a = i * 2 * Math.PI / spokes; const sp = S.extrude(S.shapeOf([[rr * 0.18, -5], [rr - 2, -3.5], [rr - 2, 3.5], [rr * 0.18, 5]]), -2.5, 2.5, mats.alu, 0.6, 2); sp.rotation.z = a; sp.position.z = W * 0.08; g.add(sp); }
  return g;
}
// Housing shell with a cutaway: cylinder (axis y) of outer radius R, wall t, height H (y = 0..H), closed at the bottom.
// cut = removed sector in degrees, centred on the camera side (+z). Cut faces are drawn in the cut-section red.
// setCut(deg) rebuilds it (animate 0 -> 120 for the reveal). The outer skin uses `skin` (e.g. paint/alu), inner wall `inner`.
export function housing(mats, { R = 50, t = 3, H = 80, skin = null, inner = null, seg = 96 } = {}) {
  const g = new THREE.Group(); const sk = skin ?? mats.alu, inn = inner ?? mats.innerWall;
  const parts = []; const clear = () => { for (const p of parts) { g.remove(p); p.geometry.dispose(); } parts.length = 0; };
  const add = (m) => { m.castShadow = m.receiveShadow = true; g.add(m); parts.push(m); };
  g.setCut = (deg) => { clear(); const cut = Math.max(0, Math.min(359, deg)) * D2R; const len = 2 * Math.PI - cut; const start = Math.PI / 2 + cut / 2; // lathe phi: x = r sin(phi), z = r cos(phi); +z is phi = 0
    const ph0 = cut / 2, phL = len;
    add(lathe([[R, H], [R, t * 0.5], [R - t * 0.5, 0]], sk, seg, ph0, phL));          // outer skin
    add(lathe([[R - t, t], [R - t, H]], inn, seg, ph0, phL));                           // inner wall
    add(lathe([[0.01, 0], [R - t * 0.5, 0]], sk, seg, ph0, phL));                       // bottom outside
    add(lathe([[R - t, t], [0.01, t]], inn, seg, ph0, phL));                            // floor inside
    add(lathe([[R - t, H], [R, H]], sk, seg, ph0, phL));                                // top rim
    if (cut > 0.001) for (const ph of [ph0, ph0 + phL]) {                               // red cut faces (wall + floor section)
      const shp = S.shapeOf([[0, 0], [R - t * 0.5, 0], [R, t * 0.5], [R, H], [R - t, H], [R - t, t], [0, t]]);
      const m = new THREE.Mesh(new THREE.ShapeGeometry(shp), mats.cut); m.rotation.y = ph - Math.PI / 2; add(m); }
    void start; };
  g.setCut(0); return g;
}
export const RBox = RoundedBoxGeometry;
// Point helper for overlays: 3D (x,y,z) in an object's local frame -> design px
export const screenOf = (st, obj, x, y, z) => { const v = V3(x, y, z); if (obj) v.applyMatrix4(obj.matrixWorld); return S.toScreen(st.camera, v); };
