// WhyLoop render toolkit: studio scene, materials, post-processing, overlay helpers, frame harness.
// Import from a scene page:  import * as S from '/tools/render/lib/studio.js'  (serve repo root on :8765)
import * as THREE from 'three';
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { GTAOPass } from 'three/addons/postprocessing/GTAOPass.js';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
export { THREE };

// Design space is always 1080x1920; previews render smaller (w/h query) and the overlay is scaled.
export const DW = 1080, DH = 1920;
export const SAFE = { top: 320, bottom: 480, right: 150, left: 60 };

export function params() {
  const Q = new URLSearchParams(location.search);
  return { scale: parseFloat(Q.get('scale') || '1'), ao: Q.get('ao') !== '0', w: +(Q.get('w') || 1080), h: +(Q.get('h') || 1920), safe: Q.get('safe') === '1' };
}

export function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

// NaN/Inf guard (swiftshader occasionally produces NaN pixels that bloom turns into black boxes)
const Sanitize = { uniforms: { tDiffuse: { value: null } }, vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }',
  fragmentShader: 'uniform sampler2D tDiffuse; varying vec2 vUv; void main(){ vec4 c=texture2D(tDiffuse,vUv); if(any(isnan(c))||any(isinf(c))) c=vec4(0.0,0.0,0.0,1.0); gl_FragColor=c; }' };

export function makeStudio({ fov = 32, bg = 0x0b0f16, envIntensity = 0.35, bloom = 0.1, near = 2, far = 4000, samples = 4 } = {}) {
  RectAreaLightUniformsLib.init();
  const P = params(); const W = P.w, H = P.h; const RW = Math.round(W * P.scale), RH = Math.round(H * P.scale);
  const renderer = new THREE.WebGLRenderer({ antialias: false, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(RW, RH, false);
  renderer.toneMapping = THREE.ACESFilmicToneMapping; renderer.toneMappingExposure = 1.0;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.shadowMap.enabled = true; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.localClippingEnabled = true;
  const scene = new THREE.Scene(); scene.background = new THREE.Color(bg);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.02, 0.1, 100, { size: 512 }).texture;
  scene.environmentIntensity = envIntensity;
  const camera = new THREE.PerspectiveCamera(fov, W / H, near, far);
  const rt = new THREE.WebGLRenderTarget(RW, RH, { type: THREE.HalfFloatType, samples });
  const composer = new EffectComposer(renderer, rt); composer.setPixelRatio(1); composer.setSize(RW, RH);
  composer.addPass(new RenderPass(scene, camera));
  composer.addPass(new ShaderPass(Sanitize));
  if (P.ao) { const g = new GTAOPass(scene, camera, RW, RH); g.output = GTAOPass.OUTPUT.Default; g.blendIntensity = 0.85;
    g.updateGtaoMaterial({ radius: 3, distanceExponent: 1.5, thickness: 2.0, scale: 1.0, samples: 8 }); g.updatePdMaterial({ lumaPhi: 10, depthPhi: 2, normalPhi: 3, radius: 5, rings: 2, samples: 8 }); composer.addPass(g); }
  if (bloom > 0) composer.addPass(new UnrealBloomPass(new THREE.Vector2(RW / 2, RH / 2), bloom, 0.45, 0.95));
  composer.addPass(new OutputPass());
  const out = document.createElement('canvas'); out.width = W; out.height = H; document.body.appendChild(out);
  const g2 = out.getContext('2d');
  return { P, W, H, renderer, scene, camera, composer, out, g2 };
}

// Standard 3-point studio lighting with a soft key shadow. ctr = subject center, size = subject size (scene units)
export function studioLights(scene, ctr = new THREE.Vector3(), size = 100, up = 'y') {
  const s = size; const V = (x, y, z) => up === 'y' ? new THREE.Vector3(x, y, z) : new THREE.Vector3(x, -z, y);
  const key = new THREE.DirectionalLight(0xfff1df, 2.2); key.position.copy(V(-1.2 * s, 2.6 * s, 2.0 * s).add(ctr)); key.target.position.copy(ctr);
  key.castShadow = true; key.shadow.mapSize.set(2048, 2048); const sc = key.shadow.camera; sc.left = -2 * s; sc.right = 2 * s; sc.top = 2 * s; sc.bottom = -2 * s; sc.near = 0.5 * s; sc.far = 8 * s;
  key.shadow.bias = -0.0004; key.shadow.normalBias = 0.04 * s / 100; key.shadow.radius = 4; scene.add(key, key.target);
  const rim = new THREE.DirectionalLight(0xcfe0ff, 1.2); rim.position.copy(V(2 * s, 1.6 * s, -2.2 * s).add(ctr)); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xdde6ff, 0x2a2420, 0.3));
  const soft = new THREE.RectAreaLight(0xfff0e0, 3.0, 2.4 * s, 1.2 * s); soft.position.copy(V(-1.8 * s, 0.8 * s, 1.6 * s).add(ctr)); soft.lookAt(ctr); scene.add(soft);
  return { key, rim, soft };
}

// ---------- textures ----------
export function woodTex(seed = 7) {
  const c = document.createElement('canvas'); c.width = 2048; c.height = 2048; const g = c.getContext('2d'); const r = rng(seed);
  g.fillStyle = '#6b4a2f'; g.fillRect(0, 0, 2048, 2048); const plankH = 2048 / 6;
  for (let p = 0; p < 6; p++) { const y0 = p * plankH; const tone = 0.85 + r() * 0.3; g.fillStyle = `rgb(${[118, 82, 52].map(v => (v * tone) | 0).join(',')})`; g.fillRect(0, y0, 2048, plankH);
    const ph = r() * 100; for (let i = 0; i < 260; i++) { const yy = y0 + r() * plankH; const a = 0.025 + r() * 0.06; g.strokeStyle = r() < 0.5 ? `rgba(40,24,12,${a})` : `rgba(190,150,105,${a * 0.6})`; g.lineWidth = 0.8 + r() * 3;
      g.beginPath(); for (let x = 0; x <= 2048; x += 32) { const y = yy + Math.sin(x * 0.0021 + ph + i * 0.37) * 9 + Math.sin(x * 0.011 + i) * 2.5; x ? g.lineTo(x, y) : g.moveTo(x, y); } g.stroke(); }
    g.fillStyle = 'rgba(20,12,6,0.85)'; g.fillRect(0, y0, 2048, 3); }
  for (let i = 0; i < 40; i++) { g.fillStyle = `rgba(30,20,10,${0.03 + r() * 0.05})`; g.beginPath(); g.ellipse(r() * 2048, r() * 2048, 30 + r() * 140, 20 + r() * 90, r() * 3, 0, 7); g.fill(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 8; return t;
}
export function noiseTex(seed, base = 128, amp = 20, size = 512) {
  const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d'); const r = rng(seed);
  const id = g.createImageData(size, size); for (let i = 0; i < id.data.length; i += 4) { const v = base + (r() - 0.5) * amp * 2; id.data[i] = id.data[i + 1] = id.data[i + 2] = v; id.data[i + 3] = 255; }
  g.putImageData(id, 0, 0); const t = new THREE.CanvasTexture(c); t.wrapS = t.wrapT = THREE.RepeatWrapping; return t;
}
// Wooden workbench plane. up='y': plane y=level; up='z': plane z=level
export function bench(scene, level, up = 'y', size = 2000, repeat = 2) {
  const m = new THREE.MeshStandardMaterial({ map: woodTex(), roughness: 0.62, metalness: 0 }); m.map.repeat.set(repeat, repeat);
  const b = new THREE.Mesh(new THREE.PlaneGeometry(size, size), m); if (up === 'y') { b.rotation.x = -Math.PI / 2; b.position.y = level; } else b.position.z = level;
  b.receiveShadow = true; scene.add(b); return b;
}

// ---------- geometry helpers ----------
export const toV2 = (a) => a.map(p => new THREE.Vector2(p[0], p[1]));
export function shapeOf(ring, holes = []) { const s = new THREE.Shape(toV2(ring)); for (const h of holes) s.holes.push(new THREE.Path(toV2(h))); return s; }
export function circle(cx, cy, r, n = 48, cw = true) { const a = []; for (let i = 0; i < n; i++) { const t = (cw ? -1 : 1) * i / n * Math.PI * 2; a.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return a; }
export function roundRect(x0, y0, x1, y1, r, n = 10) { const a = []; const c = [[x1 - r, y1 - r, 0], [x0 + r, y1 - r, 90], [x0 + r, y0 + r, 180], [x1 - r, y0 + r, 270]];
  for (const [cx, cy, d] of c) for (let i = 0; i <= n; i++) { const t = (d + 90 * i / n) * Math.PI / 180; a.push([cx + r * Math.cos(t), cy + r * Math.sin(t)]); } return a; }
export function extrude(shape, z0, z1, mats, bevel = 0, curve = 24) {
  const g = new THREE.ExtrudeGeometry(shape, { depth: Math.max(0.001, z1 - z0 - 2 * bevel), bevelEnabled: bevel > 0, bevelThickness: bevel, bevelSize: bevel, bevelOffset: -bevel, bevelSegments: 5, curveSegments: curve });
  g.translate(0, 0, z0 + bevel); g.computeVertexNormals(); return new THREE.Mesh(g, mats);
}
export const shadowAll = (o) => o.traverse(m => { if (m.isMesh) { m.castShadow = true; m.receiveShadow = true; } });

// ---------- camera ----------
export const smooth = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
// KEYS: [t, tx, ty, tz, dist, elevDeg, azimDeg]; y-up orbit around target. Loops if loop>0.
export function orbitCam(KEYS, t, loop = 0) {
  if (loop) t = ((t % loop) + loop) % loop;
  let k = 0; while (k < KEYS.length - 2 && t > KEYS[k + 1][0]) k++;
  const A = KEYS[k], B = KEYS[k + 1]; const u = smooth((t - A[0]) / (B[0] - A[0])); const L = (i) => A[i] + (B[i] - A[i]) * u;
  const dist = Math.exp(Math.log(A[4]) + (Math.log(B[4]) - Math.log(A[4])) * u);
  const el = L(5) * Math.PI / 180, az = L(6) * Math.PI / 180; const target = new THREE.Vector3(L(1), L(2), L(3));
  const pos = new THREE.Vector3(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(dist).add(target);
  return { pos, target };
}
export function toScreen(camera, v) { const p = v.clone().project(camera); return [(p.x * 0.5 + 0.5) * DW, (-p.y * 0.5 + 0.5) * DH]; }

// ---------- 2D overlay (always in 1080x1920 design coordinates) ----------
export function overlayBegin(st) { const k = st.W / DW; st.g2.setTransform(k, 0, 0, k, 0, 0); }
export function vignette(g2, top = 560) {
  const vg = g2.createRadialGradient(DW / 2, DH * 0.48, DH * 0.28, DW / 2, DH * 0.5, DH * 0.75); vg.addColorStop(0, 'rgba(0,0,0,0)'); vg.addColorStop(1, 'rgba(0,0,0,0.42)'); g2.fillStyle = vg; g2.fillRect(0, 0, DW, DH);
  if (top > 0) { const tg = g2.createLinearGradient(0, 0, 0, top); tg.addColorStop(0, 'rgba(8,6,4,0.55)'); tg.addColorStop(1, 'rgba(8,6,4,0)'); g2.fillStyle = tg; g2.fillRect(0, 0, DW, top); }
}
export function outlined(g2, text, x, y, size, fill, font = 'Anton') {
  g2.font = `${size}px ${font}`; g2.textAlign = 'center'; g2.textBaseline = 'alphabetic'; g2.lineJoin = 'round';
  g2.shadowColor = 'rgba(0,0,0,0.55)'; g2.shadowBlur = 18; g2.shadowOffsetY = 6; g2.lineWidth = size * 0.14; g2.strokeStyle = '#000'; g2.strokeText(text, x, y);
  g2.shadowColor = 'transparent'; g2.shadowBlur = 0; g2.shadowOffsetY = 0; g2.fillStyle = fill; g2.fillText(text, x, y);
}
export function rrect(g2, x, y, w, h, r) { g2.beginPath(); g2.moveTo(x + r, y); g2.arcTo(x + w, y, x + w, y + h, r); g2.arcTo(x + w, y + h, x, y + h, r); g2.arcTo(x, y + h, x, y, r); g2.arcTo(x, y, x + w, y, r); g2.closePath(); }
// Series hook template: INSIDE IT badge, two-line question (white then yellow), WHYLOOP tag. Centered at x=495 (right 150 px kept free).
export const CX = (DW - SAFE.right + SAFE.left) / 2 - 10; // 495
export function hookCard(g2, a, line1, line2, size = 124, tag = true) {
  g2.save(); g2.globalAlpha = a; g2.font = '40px Anton'; const bw = g2.measureText('INSIDE IT').width + 44; const by = 368;
  g2.fillStyle = '#ffd21f'; rrect(g2, CX - bw / 2, by, bw, 58, 12); g2.fill(); g2.fillStyle = '#10141c'; g2.textAlign = 'center'; g2.fillText('INSIDE IT', CX, by + 45);
  outlined(g2, line1, CX, 540, size, '#ffffff'); outlined(g2, line2, CX, 540 + size * 1.03, size, '#ffd21f');
  if (tag) { g2.font = '36px Anton'; g2.letterSpacing = '8px'; g2.lineWidth = 6; g2.strokeStyle = '#000'; const ty = 540 + size * 1.03 + 64; g2.strokeText('WHYLOOP', CX, ty); g2.fillStyle = '#fff'; g2.fillText('WHYLOOP', CX, ty); g2.letterSpacing = '0px'; }
  g2.restore();
}
export function redCircle(g2, a, x, y, R = 80, from = [-280, 130]) {
  g2.save(); g2.globalAlpha = a; g2.lineWidth = 9; g2.strokeStyle = '#ff2a2a'; g2.shadowColor = 'rgba(0,0,0,0.5)'; g2.shadowBlur = 10;
  g2.beginPath(); g2.arc(x, y, R, 0, Math.PI * 2); g2.stroke();
  const ax = x + from[0], ay = y + from[1]; const d = Math.hypot(from[0], from[1]); const ex = x + from[0] / d * (R + 8), ey = y + from[1] / d * (R + 8);
  g2.lineWidth = 11; g2.lineCap = 'round'; g2.beginPath(); g2.moveTo(ax, ay); g2.lineTo(ex + from[0] / d * 26, ey + from[1] / d * 26); g2.stroke();
  const ang = Math.atan2(ey - ay, ex - ax); g2.fillStyle = '#ff2a2a'; g2.beginPath(); g2.moveTo(ex, ey); g2.lineTo(ex - 40 * Math.cos(ang - 0.45), ey - 40 * Math.sin(ang - 0.45)); g2.lineTo(ex - 40 * Math.cos(ang + 0.45), ey - 40 * Math.sin(ang + 0.45)); g2.closePath(); g2.fill();
  g2.restore();
}
// Label with leader line to a screen point (only if the point is inside the safe action area)
export function label(g2, a, text, px, py, ly = 470, size = 96) {
  g2.save(); g2.globalAlpha = a; outlined(g2, text, CX, ly, size, '#ffd21f');
  if (px != null && py > SAFE.top && py < DH - SAFE.bottom && px > SAFE.left && px < DW - SAFE.right) {
    g2.strokeStyle = '#ffd21f'; g2.lineWidth = 6; g2.lineCap = 'round'; g2.shadowColor = 'rgba(0,0,0,0.6)'; g2.shadowBlur = 8;
    g2.beginPath(); g2.moveTo(CX, ly + 28); g2.lineTo(px, py - 14); g2.stroke(); g2.fillStyle = '#ffd21f'; g2.beginPath(); g2.arc(px, py, 11, 0, Math.PI * 2); g2.fill(); }
  g2.restore();
}
// Force arrow (orange) from (x0,y0) to (x1,y1) in design px
export function forceArrow(g2, a, x0, y0, x1, y1, w = 26) {
  g2.save(); g2.globalAlpha = a; const ang = Math.atan2(y1 - y0, x1 - x0), L = Math.hypot(x1 - x0, y1 - y0);
  g2.translate(x0, y0); g2.rotate(ang); g2.shadowColor = 'rgba(0,0,0,0.55)'; g2.shadowBlur = 14; g2.fillStyle = '#ff7a1a'; g2.strokeStyle = '#000'; g2.lineWidth = 5;
  g2.beginPath(); g2.moveTo(0, -w / 2); g2.lineTo(L - w * 2, -w / 2); g2.lineTo(L - w * 2, -w * 1.25); g2.lineTo(L, 0); g2.lineTo(L - w * 2, w * 1.25); g2.lineTo(L - w * 2, w / 2); g2.lineTo(0, w / 2); g2.closePath(); g2.stroke(); g2.fill();
  g2.restore();
}
export function safeZones(g2) {
  g2.save(); g2.fillStyle = 'rgba(255,0,255,0.28)'; g2.fillRect(0, 0, DW, SAFE.top); g2.fillRect(0, DH - SAFE.bottom, DW, SAFE.bottom); g2.fillRect(DW - SAFE.right, 0, SAFE.right, DH); g2.fillRect(0, 0, SAFE.left, DH); g2.restore();
}

// ---------- frame harness ----------
// setScene(t) poses the 3D scene; overlay(t) draws 2D (design coords). Installs window.renderFrame.
export function install(st, setScene, overlay) {
  window.renderFrame = (t, sub = 1, shutter = 0.5, fps = 30) => {
    const { g2, W, H, renderer, composer, P } = st; g2.setTransform(1, 0, 0, 1, 0, 0); g2.globalAlpha = 1; g2.clearRect(0, 0, W, H);
    for (let i = 0; i < sub; i++) { const ts = t + (sub > 1 ? ((i + 0.5) / sub - 0.5) * shutter / fps : 0); setScene(ts); composer.render();
      g2.globalAlpha = 1 / (i + 1); g2.drawImage(renderer.domElement, 0, 0, renderer.domElement.width, renderer.domElement.height, 0, 0, W, H); }
    g2.globalAlpha = 1; setScene(t); overlayBegin(st); overlay(t); g2.fillStyle = 'rgba(255,255,255,0.004)'; g2.fillRect(0, 0, 1, 1);
    if (P.safe) safeZones(g2);
    return st.out.toDataURL('image/png');
  };
  window.ready = true;
}

// ---------- vehicle cue (group V): passing road-light streaks behind the subject ----------
// Returns { mesh, setTravel(u) }: u = car travel as a fraction of the loop's total travel (0..1); repeats seamlessly 'reps' times per loop.
// Scroll it from the car's speed integral so the streaks slow down and stop exactly when the car brakes (first used in p053).
export function streakBackdrop(scene, { seed = 11, count = 26, z = -700, y = 40, w = 2400, h = 1200, reps = 3, opacity = 0.9 } = {}) {
  const c = document.createElement('canvas'); c.width = 1024; c.height = 512; const g = c.getContext('2d'); const r = rng(seed);
  for (let i = 0; i < count; i++) { const yy = 20 + r() * 472, x = r() * 1024, L = 90 + r() * 260, hh = 2 + r() * 5; const a = 0.10 + r() * 0.22; const col = r() < 0.35 ? '255,190,120' : '190,215,255';
    for (const dx of [0, -1024, 1024]) { const gg = g.createLinearGradient(x + dx, 0, x + dx + L, 0); gg.addColorStop(0, `rgba(${col},0)`); gg.addColorStop(0.7, `rgba(${col},${a})`); gg.addColorStop(1, `rgba(${col},0)`); g.fillStyle = gg; g.fillRect(x + dx, yy, L, hh); } }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = THREE.RepeatWrapping;
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true, depthWrite: false, opacity }));
  mesh.position.set(0, y, z); scene.add(mesh);
  return { mesh, setTravel: (u) => { t.offset.x = ((u * reps) % 1 + 1) % 1; } };
}

// ---------- cutaway helpers (first used in p054) ----------
// Engineering cross-section texture for cut faces (extrude caps use world-unit UVs: repeat ~0.45 for mm scenes).
export function hatchTex(base = '#3c4552', line = '#56606f', repeat = 0.45) {
  const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.fillStyle = base; g.fillRect(0, 0, 256, 256);
  g.strokeStyle = line; g.lineWidth = 10; for (let i = -256; i < 512; i += 42) { g.beginPath(); g.moveTo(i, 0); g.lineTo(i + 256, 256); g.stroke(); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(repeat, repeat); return t;
}
// Clean dark radial-gradient floor that receives shadows (reviewer preferred it to the wood bench). Plane normal = +z.
export function gradientFloor(scene, z, size = 150, cx = 0, cy = 0, stops = ['#4a5262', '#262c37', '#0c0f14']) {
  const c = document.createElement('canvas'); c.width = c.height = 1024; const g = c.getContext('2d'); const gr = g.createRadialGradient(512, 470, 30, 512, 512, 620);
  gr.addColorStop(0, stops[0]); gr.addColorStop(0.5, stops[1]); gr.addColorStop(1, stops[2]); g.fillStyle = gr; g.fillRect(0, 0, 1024, 1024);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(size, size), new THREE.MeshStandardMaterial({ map: t, roughness: 0.85, metalness: 0 }));
  m.position.set(cx, cy, z); m.receiveShadow = true; scene.add(m); return m;
}
