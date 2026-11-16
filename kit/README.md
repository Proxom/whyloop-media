# WhyLoop studio kit (KIT DAY, 16 Nov 2026)

Every Reel after 16 Nov builds from `kit/kit.js` (AGENT.md override 15 Nov 14:23, part B). Do not rebuild a studio, a material or a part inside a Reel: if the kit lacks a part, add it to `kit.js`, test it once in `kit/test/parts.html`, commit.

Contact sheet of every part with the final look: `kit/test/stills/contact_sheet.jpg` (hero composite at final settings: `kit/test/stills/hero_final_settings.png`).

## Use in a scene page

```html
<script type="importmap">{"imports":{"three":"/tools/render/node_modules/three/build/three.module.js","three/addons/":"/tools/render/node_modules/three/examples/jsm/"}}</script>
<script type="module">
import * as K from '/kit/kit.js'; const { THREE, S } = K;
const st = K.makeKit();                     // renderer, softbox env, composer (SMAA with ?aa=1), 2D overlay canvas
const M = K.materials();                    // steel, machined, alu, brass, chrome, plastic, rubber, cut, glass, paint(color), innerWall, accent
K.backdrop(st.scene, { floorY: -60 });      // dark seamless backdrop (unlit) + shadow-catcher floor + light pool
K.lightRig(st.scene, new THREE.Vector3(0,0,0), 90);   // key (soft shadow) + rim + fill; size = subject size in mm
const g = K.spurGear(M.machined, { z: 24, m: 2.5, w: 10, bore: 8 }); st.scene.add(g);
S.shadowAll(st.scene);
const CAMK = [K.at(0, K.CAM.hero([0,0,0], 90)), K.at(3, K.CAM.macro([20,0,0], 40)), K.at(25, K.CAM.macro([20,0,0], 40))];
function setScene(t) { g.rotation.z = t; K.shoot(st, CAMK, t); }
function overlay(t) { S.vignette(st.g2, 0); K.TXT.hook(st.g2, t < 2 ? 1 : 0, 'HOW DOES IT', 'CLICK?'); }
S.install(st, setScene, overlay); window.ready = false; await document.fonts.load('40px Anton'); window.ready = true;
</script>
```
Render with the existing harness: `node tools/render/render.js <scene> <out> 30 1 0 <frames> 0.75 0 0 1 1080 1920 1` (scale 0.75, AO off, ONE worker, SMAA on), then `tools/render/encode.sh`.

## Parts (all mm, parametric)
| function | what | animation helper |
|---|---|---|
| `spurGear(mat, {z,m,w,bore,holes})` | true involute teeth (20 deg), chamfered | `meshAngle(theta1, z1, z2)` for the mating gear |
| `bevelGear(mat, {z,m,w,cone,bore})` | tapered teeth, axis z, apex +z | 1:1 miter pair: same speed, opposite sense |
| `rack(mat, {m,L,w,h})` | pitch line y=0, teeth +y | x shift = theta x pinion pitch radius |
| `spring(mat, {R,wire,turns,len})` | closed ground ends, along +y | `setLength(L)` every frame |
| `shaft(mat, {d,L})`, `ballBearing(M, {d,D,B,balls})` | shaft axis z; bearing races + balls | `setSpin(a)` (cage ~0.4x) |
| `ratchet(M, {z,Ro,depth,pivot,pawlLen})` | sawtooth wheel + brass pawl on a pin | `pose(wheelAngle)` drops the pawl tip onto the teeth (bisection, no overlap) |
| `pistonCrank(M, {r,l,bore})` | crank web + counterweight, rod, piston with rings | `pose(theta)` exact slider-crank |
| `camFollower(M, {base,lift,profile})` | disc cam + flat follower | `pose(theta)` exact lift for a flat follower |
| `lever(M, {L,w,t,knob})` | bar + pivot boss + knob | rotate about z |
| `wheel(M, {R,W,spokes})` | rubber tyre, alloy rim, 5 spokes | rotate about z |
| `housing(M, {R,t,H,skin,inner})` | cylinder shell, open top | `setCut(deg)`: animated cutaway, cut faces in section red |

Still run the Reel's own `check.py` on moving pairs (HARD GATE 5.2); the helpers keep contact but the Reel's numbers decide.

## Camera presets and text style
- `K.CAM.hero / cutaway / macro / top (ctr, size)` -> orbit keys; `K.at(t, key)` retimes; `K.shoot(st, keys, t)` also sets the DOF focus when DOF is on.
- `K.TXT.hook` (INSIDE IT + white/yellow question), `circle` (red circle + arrow), `step` (numbered step label), `tag` (part tag pinned to a 3D point), `answer` (payoff card), `follow` (follow line), `flash` (white cut flash). All sizes pass the HARD GATE (hook >= 64 px, labels >= 44 px) and stay in the safe area.
- `K.glow(mesh, a)` highlights the active part (accent orange), `K.contactBlob()` adds a cheap static contact shadow.

## Render settings (benchmarked on this 4-core swiftshader box, hero composite, 1080x1920)
| setting | s/frame |
|---|---|
| old: lit cyclorama + 2048 VSM shadows, scale 1, SMAA | 1.94 |
| scale 1, SMAA, unlit backdrop, 1024 PCF | 1.24 |
| **FINAL: scale 0.75 (text stays full-res), SMAA, unlit backdrop, 1024 PCF** | **0.81** |
| + depth of field (BokehPass) | +1.4 (not worth it on CPU; keep `dof: null`) |
| 3 parallel workers | no gain (swiftshader already uses all cores) -> use ONE worker |
Final render budget: 0.81 s x 30 fps = ~24 s of render per second of video: 20 s Reel ~8 min, 25 s ~10 min, 30 s ~12 min. Keep Reels at 20-25 s.
Cost split at scale 1 (before the fixes): objects 475 ms, shadow map 350 ms, lit backdrop 250 ms, post 150-250 ms, PNG encode 50 ms.
AO stays off (it cost +65 % on p068). Motion blur: only on fast shots, 2 sub-frames max.

## Known limits (fix in the kit, not in a Reel)
- Bevel gear: steel flanks catch the strip lights very bright; prefer brass for the visible bevel gear.
- Housing is a cylinder only; a box housing with cutaway is the next part to add when a topic needs it.
- Glass is the cheap kind (transparent + reflections, no refraction).
