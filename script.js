import * as THREE from "three";
import { OrbitControls } from "jsm/controls/OrbitControls.js";
import { FontLoader } from "jsm/loaders/FontLoader.js";
import { TextGeometry } from "jsm/geometries/TextGeometry.js";
import { RoundedBoxGeometry } from "jsm/geometries/RoundedBoxGeometry.js";
import { RoomEnvironment } from "jsm/environments/RoomEnvironment.js";

// Every dimension below is the millimetre figure off the CAD sketch.
const MM = 0.05;
const mm = (v) => v * MM;

// ============================================
// SCENE / CAMERA / RENDERER
// ============================================
const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
  40,
  window.innerWidth / window.innerHeight,
  0.1,
  100,
);
camera.position.set(0, 2, 8);

const renderer = new THREE.WebGLRenderer({
  canvas: document.querySelector(".webgl"),
  antialias: true,
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
// Must equal --color-bg exactly, or the fixed canvas reads as a rectangle laid
// over the page instead of the page itself.
renderer.setClearColor(0xffffff, 1);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 0.95;

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.enablePan = false;
controls.minDistance = 2.4;
// Narrow viewports need a long pull-back to fit the case; a tighter cap here
// silently fights the computed step framing.
controls.maxDistance = 30;
controls.minPolarAngle = 0.2;
controls.maxPolarAngle = 2.05;

// The canvas is fixed across the whole viewport, so OrbitControls' two defaults
// would take the page's scrolling away from it entirely:
//   connect() writes touchAction:'none' inline on the canvas  (OrbitControls 478)
//   onMouseWheel preventDefault()s unless enableZoom is false (OrbitControls 1666)
// Zoom is redundant here — every step authors its own framing — so dropping it
// hands the wheel back, and pan-y hands back vertical touch while leaving
// horizontal drags to orbit. Elevation is authored per step, so losing the
// vertical touch-orbit costs nothing.
controls.enableZoom = false;
renderer.domElement.style.touchAction = "pan-y";

// ============================================
// ENVIRONMENT MAP + LIGHTS
// A neutral studio env — a medical device has to read as clear, colourless
// glass, which a tinted room map will not give.
// ============================================
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
pmrem.dispose();

// A neutral key from high right, and a fill the colour of the room. The page is
// white paper now, so the light coming back up from it is very nearly white —
// the fill keeps only a breath of the brand hue, enough that the kit is not
// rendered entirely in greys. The key stays neutral so white plastic stays white.
const keyLight = new THREE.DirectionalLight(0xffffff, 1.6);
keyLight.position.set(4, 6, 5);
const fillLight = new THREE.DirectionalLight(0xe4f2f0, 0.85);
fillLight.position.set(-5, -1, -4);
scene.add(keyLight, fillLight);

// No ground plane. Steps reframe the stage over a 4x range of camera distances,
// so any fixed-height shadow catcher ends up intersecting the geometry — and the
// reference's shadow falls on the wall behind its product, not on a floor.

// ============================================
// MELT EFFECT SETUP
// ============================================
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2(9999, 9999);
const pointerWorld = new THREE.Vector3();
const targetMouse = new THREE.Vector3(9999, 9999, 9999);
const currentMouse = new THREE.Vector3(9999, 9999, 9999);

// Uniforms compartidos para el efecto
const meltUniforms = {
  uMouse: { value: new THREE.Vector3(9999, 9999, 9999) },
  uTime: { value: 0 },
  uRadius: { value: 0.9 },
  uStrength: { value: 0.24 },
};

// Shader suave y liquido
const meltParsVertex = `
  uniform vec3 uMouse;
  uniform float uTime;
  uniform float uRadius;
  uniform float uStrength;

  // Suavizado extra (smootherstep)
  float liquid(float t) {
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0);
  }

  vec3 melt(vec3 pos, vec3 worldPos, float scale) {
    float dist = distance(worldPos, uMouse);

    // Influencia muy suave con doble suavizado
    float t = 1.0 - clamp(dist / uRadius, 0.0, 1.0);
    float influence = liquid(t) * scale;

    // Goteo suave hacia abajo
    pos.y -= influence * uStrength;

    // Deformacion lateral suave
    pos.x += sin(uTime * 0.8 + worldPos.y * 2.0) * influence * 0.05;

    // Bulge suave hacia afuera
    vec3 dir = worldPos - uMouse;
    pos += normalize(dir + 0.0001) * influence * 0.08;

    return pos;
  }
`;

// The per-part scale is baked into the source: a rigid medical shell should only
// breathe, while the blood and plasma inside are free to run.
const meltVertex = (scale) => `
  {
    vec4 meltWorldPos = modelMatrix * vec4( position, 1.0 );
    transformed = melt( transformed, meltWorldPos.xyz, ${scale.toFixed(3)} );
  }
`;

// Funcion para aplicar el shader de melt a cualquier material
function applyMeltEffect(material, scale = 1) {
  material.onBeforeCompile = (shader) => {
    shader.uniforms.uMouse = meltUniforms.uMouse;
    shader.uniforms.uTime = meltUniforms.uTime;
    shader.uniforms.uRadius = meltUniforms.uRadius;
    shader.uniforms.uStrength = meltUniforms.uStrength;

    shader.vertexShader = shader.vertexShader.replace(
      "#include <common>",
      `#include <common>\n${meltParsVertex}`,
    );

    shader.vertexShader = shader.vertexShader.replace(
      "#include <begin_vertex>",
      `#include <begin_vertex>\n${meltVertex(scale)}`,
    );
  };
  // Materials that inject different sources must not share a compiled program.
  material.customProgramCacheKey = () => `melt-${scale}`;
  material.needsUpdate = true;
  return material;
}

// ============================================
// MATERIALS
// Only the outer shells are transmissive: three.js excludes transmissive meshes
// from the transmission pass, so everything meant to be seen *through* the glass
// is kept opaque.
// ============================================
const shellMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  envMapIntensity: 1,
  metalness: 0,
  roughness: 0.06,
  transmission: 1,
  thickness: 0.7,
  ior: 1.52,
  attenuationColor: new THREE.Color(0xdaeae7),
  attenuationDistance: 3.2,
  clearcoat: 1,
  clearcoatRoughness: 0.04,
  iridescence: 0.24,
  iridescenceIOR: 1.3,
  iridescenceThicknessRange: [100, 640],
});
applyMeltEffect(shellMaterial, 0.16);

const plasticMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xf4f7f6,
  metalness: 0,
  roughness: 0.34,
  clearcoat: 0.7,
  clearcoatRoughness: 0.25,
  side: THREE.DoubleSide,
});
applyMeltEffect(plasticMaterial, 0.12);

const lidMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xd6dedc,
  metalness: 0,
  roughness: 0.42,
  clearcoat: 0.5,
  clearcoatRoughness: 0.2,
});
applyMeltEffect(lidMaterial, 0.16);

// Translucent polypropylene, like a real microcentrifuge tube. Clear glass this
// narrow just shows the dark page through it and reads as a black hole.
const frostedMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xf6faf9,
  metalness: 0,
  roughness: 0.42,
  transmission: 0.88,
  thickness: 0.35,
  ior: 1.49,
  clearcoat: 1,
  clearcoatRoughness: 0.2,
});
applyMeltEffect(frostedMaterial, 0.16);

// Back faces only, so bores read as a hollow cavity instead of a solid cone
const channelMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x9fabaa,
  metalness: 0,
  roughness: 0.5,
  side: THREE.BackSide,
});
applyMeltEffect(channelMaterial, 0.12);

const metalMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xc2cac9,
  metalness: 1,
  roughness: 0.22,
});
applyMeltEffect(metalMaterial, 0.12);

// Matte EVA foam, like the insert in any real instrument case. Without it the
// whole case is off-white inside an off-white shell and the bays vanish.
//
// It is deep mint rather than black because it is the largest coloured surface
// on the closed kit — seen straight through the clear lid, it is what the
// product's colour *is*. Same hue as the page, four stops down.
const foamMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x123331,
  metalness: 0,
  roughness: 0.96,
});
applyMeltEffect(foamMaterial, 0.12);

const rubberMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x0f1f1e,
  metalness: 0,
  roughness: 0.82,
});
applyMeltEffect(rubberMaterial, 0.12);

const darkMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x14302d,
  metalness: 0.3,
  roughness: 0.55,
  side: THREE.DoubleSide,
});
applyMeltEffect(darkMaterial, 0.12);

const bloodMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x8f0a18,
  metalness: 0,
  roughness: 0.1,
  clearcoat: 1,
  clearcoatRoughness: 0.05,
  emissive: new THREE.Color(0x2a0106),
  emissiveIntensity: 0.18,
});
applyMeltEffect(bloodMaterial, 1);

// Straw yellow — separated plasma, the only thing that actually ships
const plasmaMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xe8bd33,
  metalness: 0,
  roughness: 0.08,
  clearcoat: 1,
  clearcoatRoughness: 0.05,
  emissive: new THREE.Color(0x3a2c00),
  emissiveIntensity: 0.22,
});
applyMeltEffect(plasmaMaterial, 1);

// Fluid roles are declared by position, not by contents, because both parts are
// separated by radial acceleration rather than by gravity — which end each
// fraction lands at is a property of the machine, not of density under 1 g.
//
// The disc is a centrifugal-microfluidic rotor: red cells collect in the inner
// channel section and the supernatant is driven over a siphon into a peripheral
// collection ring, so plasma reads outboard. The step 03 copy states this.
const ROTOR_OUTER = plasmaMaterial;
const ROTOR_INNER = bloodMaterial;

// The cartridge carries that same result off the disc. Its outboard end is the
// end you stand it on, so the plasma the siphon drove outboard is the band at
// the bottom, and the cell fraction left behind sits above the valve.
const TUBE_BELOW_VALVE = plasmaMaterial;
const TUBE_ABOVE_VALVE = bloodMaterial;

const logoMaterial = new THREE.MeshPhysicalMaterial({
  color: 0x0d2b27,
  metalness: 0.2,
  roughness: 0.35,
});
applyMeltEffect(logoMaterial, 0.16);

// ============================================
// PROFILE HELPERS
// ============================================
function arcPoints(cx, cy, r, from, to, segments) {
  const points = [];
  for (let i = 1; i <= segments; i++) {
    const a = from + (to - from) * (i / segments);
    points.push(new THREE.Vector2(cx + Math.cos(a) * r, cy + Math.sin(a) * r));
  }
  return points;
}

class HelixCurve extends THREE.Curve {
  constructor(radius, height, turns) {
    super();
    this.radius = radius;
    this.height = height;
    this.turns = turns;
  }
  getPoint(t, target = new THREE.Vector3()) {
    const a = t * Math.PI * 2 * this.turns;
    return target.set(
      Math.cos(a) * this.radius,
      t * this.height - this.height / 2,
      Math.sin(a) * this.radius,
    );
  }
}

const stage = new THREE.Group();
scene.add(stage);

// ============================================
// PART 1 — 채혈펜 (spring lancet, Ø25 × 50 mm)
// The needle only ever travels inside the contact dome, so nothing sharp is
// exposed: safer for self-use and an easier FDA path.
// ============================================
const pen = new THREE.Group();
stage.add(pen);

const PEN = {
  width: mm(25),
  height: mm(40),
  base: mm(30),
  travel: mm(20),
  dome: mm(8),
};

const penShell = new THREE.Mesh(
  new RoundedBoxGeometry(PEN.width, PEN.height, PEN.width, 6, mm(4)),
  shellMaterial,
);
penShell.position.y = mm(13);
pen.add(penShell);

const penFlange = new THREE.Mesh(
  new RoundedBoxGeometry(PEN.base, mm(5), PEN.base, 4, mm(1.6)),
  lidMaterial,
);
penFlange.position.y = mm(-9.5);
pen.add(penFlange);

// Skin contact dome — Ø8 mm aperture, the only opening in the whole part
const penDome = new THREE.Mesh(
  new THREE.SphereGeometry(
    mm(9),
    48,
    20,
    0,
    Math.PI * 2,
    Math.PI * 0.5,
    Math.PI * 0.5,
  ),
  plasticMaterial,
);
penDome.position.y = mm(-6.5);
pen.add(penDome);

const penAperture = new THREE.Mesh(
  new THREE.TorusGeometry(PEN.dome / 2, mm(0.7), 8, 40),
  metalMaterial,
);
penAperture.rotation.x = Math.PI / 2;
penAperture.position.y = mm(-15);
pen.add(penAperture);

// Spring + plunger assembly — this is what moves
const penDrive = new THREE.Group();
pen.add(penDrive);

const penCap = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(7), mm(7), mm(3), 40),
  lidMaterial,
);
penCap.position.y = mm(34.5);
penDrive.add(penCap);

const penRod = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(2.4), mm(2.4), mm(26), 32),
  metalMaterial,
);
penRod.position.y = mm(20);
penDrive.add(penRod);

// The needle rides its own 2.7 mm throw, not the plunger's 20 mm stroke: at full
// press the tip reaches -14 mm, still inside a dome that closes at -15.5 mm.
const NEEDLE_REST = mm(-6.8);
const NEEDLE_THROW = mm(2.7);
const penNeedle = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(0.35), mm(0.12), mm(9), 12),
  metalMaterial,
);
penNeedle.position.y = NEEDLE_REST;
pen.add(penNeedle);

const penSpring = new THREE.Mesh(
  new THREE.TubeGeometry(
    new HelixCurve(mm(5.5), PEN.travel, 7),
    220,
    mm(0.9),
    8,
  ),
  metalMaterial,
);
penSpring.position.y = mm(19);
penDrive.add(penSpring);

// Parented to the stage, not the pen: a drop has to fall straight down in world
// space, and the pen is tipped over the cartridge.
const PEN_TIP = new THREE.Vector3(0, mm(-17), 0);
const penDrop = new THREE.Mesh(
  new THREE.SphereGeometry(mm(2.1), 32, 20),
  bloodMaterial,
);
stage.add(penDrop);

function seatDrop(fall = 0) {
  penDrop.position.copy(PEN_TIP).applyMatrix4(pen.matrixWorld);
  penDrop.position.y -= fall;
}

// ============================================
// PART 2 — 원판 (hand-spun rotor, Ø65 mm)
// A top: spun by hand about its own axis, so the radial channel throws the
// cells outward and leaves plasma at the hub. No power needed.
// ============================================
const rotor = new THREE.Group();
stage.add(rotor);

const spinner = new THREE.Group();
rotor.add(spinner);

const DISC = { radius: mm(32.5), top: mm(7), bottom: mm(-7), fillet: mm(3) };
const CAVITY = { radius: mm(29), floor: mm(-4), ledge: mm(5) };

// A hollow bowl: out along the floor, up the outer wall, over the rim, then
// back down the inside. The cavity is what the lid closes and the channel fills.
const { radius: DR, top: DT, bottom: DB, fillet: DF } = DISC;
const discProfile = [
  new THREE.Vector2(0.004, DB),
  new THREE.Vector2(DR - DF, DB),
  ...arcPoints(DR - DF, DB + DF, DF, -Math.PI / 2, 0, 8),
  new THREE.Vector2(DR, DT - mm(2)),
  ...arcPoints(DR - mm(2), DT - mm(2), mm(2), 0, Math.PI / 2, 6),
  new THREE.Vector2(DR - mm(3), DT),
  new THREE.Vector2(DR - mm(3), CAVITY.ledge),
  new THREE.Vector2(CAVITY.radius, CAVITY.ledge),
  new THREE.Vector2(CAVITY.radius, CAVITY.floor),
  new THREE.Vector2(0.004, CAVITY.floor),
];

spinner.add(
  new THREE.Mesh(new THREE.LatheGeometry(discProfile, 180), shellMaterial),
);

// Lid plate seated on the cavity ledge, leaving the glass rim proud around it
const LID_TOP = DT + mm(0.2);
const lidProfile = [
  new THREE.Vector2(0.004, CAVITY.ledge),
  new THREE.Vector2(DR - mm(3.2), CAVITY.ledge),
  new THREE.Vector2(DR - mm(3.2), LID_TOP - mm(1)),
  ...arcPoints(DR - mm(4.2), LID_TOP - mm(1), mm(1), 0, Math.PI / 2, 6),
  new THREE.Vector2(0.004, LID_TOP),
];
spinner.add(
  new THREE.Mesh(new THREE.LatheGeometry(lidProfile, 180), lidMaterial),
);

const seam = new THREE.Mesh(
  new THREE.TorusGeometry(DR - mm(0.05), mm(0.4), 8, 200),
  darkMaterial,
);
seam.rotation.x = Math.PI / 2;
seam.position.y = mm(2.4);
spinner.add(seam);

// Side inlet port — the cartridge couples here
const port = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(4.5), mm(4.5), mm(5), 48),
  metalMaterial,
);
port.rotation.z = -Math.PI / 2;
port.position.x = DR - mm(1);
spinner.add(port);

const portBore = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(3), mm(1.4), mm(12), 32),
  darkMaterial,
);
portBore.rotation.z = -Math.PI / 2;
portBore.position.x = DR - mm(5);
spinner.add(portBore);

// Hourglass separation channel — 58 mm span, tip to tip at the hub
const CH = { inner: mm(2), outer: mm(29), rIn: mm(0.9), rOut: mm(3.8) };
const CH_LEN = CH.outer - CH.inner;
const funnelGeometry = new THREE.CylinderGeometry(
  CH.rOut,
  CH.rIn,
  CH_LEN,
  64,
  1,
  true,
);

[1, -1].forEach((side) => {
  const funnel = new THREE.Mesh(funnelGeometry, channelMaterial);
  funnel.rotation.z = (-side * Math.PI) / 2;
  funnel.position.x = side * (CH.inner + CH_LEN / 2);
  spinner.add(funnel);
});

// Graduation rings along the channel
[0.35, 0.6, 0.85].forEach((f) => {
  const x = CH.inner + CH_LEN * f;
  const r = CH.rIn + (CH.rOut - CH.rIn) * f;
  [1, -1].forEach((side) => {
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(r + mm(0.2), mm(0.35), 8, 48),
      metalMaterial,
    );
    ring.rotation.y = Math.PI / 2;
    ring.position.x = side * x;
    spinner.add(ring);
  });
});

// Puncture / fill bore, straight down through the lid
const bore = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(1.4), mm(1.4), mm(11), 32),
  darkMaterial,
);
bore.position.y = mm(2.5);
spinner.add(bore);

// Whole blood -> plasma collected outboard + packed cells held at the hub side.
// Named by position, not by contents: which fluid each band carries is set by
// ROTOR_OUTER / ROTOR_INNER above.
const bands = [];
[1, -1].forEach((side) => {
  const outerBand = new THREE.Mesh(
    new THREE.CylinderGeometry(CH.rOut - mm(0.6), CH.rIn, CH_LEN, 48),
    ROTOR_OUTER,
  );
  // Taper sized for the hub-side fraction it occupies once separated, so it
  // never pushes through the funnel wall.
  const innerBand = new THREE.Mesh(
    new THREE.CylinderGeometry(mm(2.2), CH.rIn, CH_LEN, 48),
    ROTOR_INNER,
  );
  [outerBand, innerBand].forEach((m) => {
    m.rotation.z = (-side * Math.PI) / 2;
    spinner.add(m);
  });
  bands.push({ side, outerBand, innerBand });
});

const hubDrop = new THREE.Mesh(
  new THREE.SphereGeometry(mm(1.6), 32, 20),
  ROTOR_INNER,
);
spinner.add(hubDrop);

// Ø5 mm axle it is spun on, with the 2 mm rubber rings from the sketch
const axle = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(2.5), mm(2.5), mm(46), 32),
  metalMaterial,
);
rotor.add(axle);

[mm(9), mm(-9)].forEach((y) => {
  const ring = new THREE.Mesh(
    new THREE.TorusGeometry(mm(3.4), mm(1), 8, 40),
    rubberMaterial,
  );
  ring.rotation.x = Math.PI / 2;
  ring.position.y = y;
  rotor.add(ring);
});

const axleTip = new THREE.Mesh(
  new THREE.ConeGeometry(mm(2.5), mm(5), 32),
  metalMaterial,
);
axleTip.rotation.x = Math.PI;
axleTip.position.y = mm(-25.5);
rotor.add(axleTip);

// ============================================
// PART 3 — 밀폐 카트리지 (sealed E-tube, Ø12 × 45 mm)
// Two chambers: whole blood below, plasma isolated above a quarter-turn valve.
// ============================================
const cartridge = new THREE.Group();
stage.add(cartridge);

const TUBE = { r: mm(6), body: mm(30), cone: mm(9) };
const tubeProfile = [
  new THREE.Vector2(0.004, mm(-22)),
  new THREE.Vector2(mm(1), mm(-21.5)),
  new THREE.Vector2(TUBE.r, mm(-13)),
  new THREE.Vector2(TUBE.r, mm(17)),
  new THREE.Vector2(TUBE.r + mm(0.8), mm(17)),
  new THREE.Vector2(TUBE.r + mm(0.8), mm(20)),
  new THREE.Vector2(TUBE.r - mm(0.6), mm(20)),
  new THREE.Vector2(TUBE.r - mm(0.6), mm(-12.6)),
  new THREE.Vector2(0.004, mm(-20.4)),
];
cartridge.add(
  new THREE.Mesh(new THREE.LatheGeometry(tubeProfile, 96), frostedMaterial),
);

const tubeCap = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(7), mm(6.6), mm(5), 48),
  lidMaterial,
);
tubeCap.position.y = mm(22.5);
cartridge.add(tubeCap);

const capRing = new THREE.Mesh(
  new THREE.TorusGeometry(mm(6.4), mm(1), 8, 48),
  rubberMaterial,
);
capRing.rotation.x = Math.PI / 2;
capRing.position.y = mm(19.6);
cartridge.add(capRing);

// Quarter-turn valve that seals the plasma chamber off from the cell layer
const valve = new THREE.Group();
valve.position.y = mm(6);
cartridge.add(valve);

valve.add(
  new THREE.Mesh(
    new THREE.CylinderGeometry(mm(5.3), mm(5.3), mm(1.6), 48),
    lidMaterial,
  ),
);
const valveSlot = new THREE.Mesh(
  new THREE.BoxGeometry(mm(7), mm(2.2), mm(2.6)),
  darkMaterial,
);
valve.add(valveSlot);

const valveHandle = new THREE.Mesh(
  new THREE.BoxGeometry(mm(14), mm(1.6), mm(3)),
  plasticMaterial,
);
valveHandle.position.y = mm(6);
cartridge.add(valveHandle);

// Liquid bands, named by where they sit rather than by what they hold: the tip
// carries whole blood at step 02 and plasma from step 04 on, so its material is
// set per step. Top edge y=18, valve at y≈4, tube floor y=-19.
const tubeTip = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(5.2), mm(1.2), mm(12), 48),
  TUBE_BELOW_VALVE,
);
tubeTip.position.y = mm(-13);
cartridge.add(tubeTip);

const tubeMid = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(5.2), mm(5.2), mm(10), 48),
  TUBE_BELOW_VALVE,
);
tubeMid.position.y = mm(-1);
cartridge.add(tubeMid);

const tubeTop = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(5.2), mm(5.2), mm(11), 48),
  TUBE_ABOVE_VALVE,
);
tubeTop.position.y = mm(12.5);
cartridge.add(tubeTop);

// What the packed cells keep once the plasma has drained out from under them.
// The isolation motion ends here and the resting poses start here, so the two
// agree by construction instead of by matching hand-copied numbers.
const CELL_KEEP = 0.45;
// Lowest the conical tip can be squashed before its full-width top face clears
// the tube's own taper and shows outside the shell.
const TIP_FLOOR = 0.25;
const tubeTopY = (s) => mm(18) - (s * mm(11)) / 2;
const tubeMidY = (s) => mm(-6) + (s * mm(10)) / 2;
const tubeTipY = (s) => mm(-19) + (s * mm(12)) / 2;

// 검체 안정화 시약 앰플 — pressed to mix into the plasma before shipping
const ampoule = new THREE.Mesh(
  new THREE.CapsuleGeometry(mm(3.4), mm(7), 16, 32),
  frostedMaterial,
);
ampoule.position.set(mm(13), mm(13), 0);
cartridge.add(ampoule);

// ============================================
// PART 4 — 배송 케이스 (105 × 80 × 26 mm)
// Sized backwards from the parts: a Ø65 rotor bay alone eats 67 mm of width,
// and a 45 mm cartridge and a 50 mm pen both have to lie flat in a 26 mm case.
// ============================================
const kitCase = new THREE.Group();
stage.add(kitCase);

const caseShell = new THREE.Mesh(
  new RoundedBoxGeometry(mm(105), mm(26), mm(80), 6, mm(5)),
  shellMaterial,
);
kitCase.add(caseShell);

const caseTray = new THREE.Mesh(
  new RoundedBoxGeometry(mm(99), mm(15), mm(74), 4, mm(3.5)),
  foamMaterial,
);
caseTray.position.y = mm(-3.5);
kitCase.add(caseTray);

// Bay centres, checked against each other so nothing overlaps
const ROTOR_BAY = { x: mm(-17), z: 0 };
const PEN_BAY = { x: mm(36), z: mm(-12) };
const TUBE_BAY = { x: mm(30), z: mm(28) };

const rotorBay = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(33.5), mm(33.5), mm(10), 64, 1, true),
  channelMaterial,
);
rotorBay.position.set(ROTOR_BAY.x, mm(1), ROTOR_BAY.z);
kitCase.add(rotorBay);

const penBay = new THREE.Mesh(
  new RoundedBoxGeometry(mm(28), mm(10), mm(54), 3, mm(3)),
  channelMaterial,
);
penBay.position.set(PEN_BAY.x, mm(1), PEN_BAY.z);
kitCase.add(penBay);

const tubeBay = new THREE.Mesh(
  new THREE.CylinderGeometry(mm(7.5), mm(7.5), mm(44), 40, 1, true),
  channelMaterial,
);
tubeBay.rotation.z = Math.PI / 2;
tubeBay.position.set(TUBE_BAY.x, mm(1), TUBE_BAY.z);
kitCase.add(tubeBay);

// Dark floors, so each bay reads as a recess rather than a ring on a slab
[
  [ROTOR_BAY.x, 0, mm(66), mm(66)],
  [PEN_BAY.x, PEN_BAY.z, mm(27), mm(53)],
  [TUBE_BAY.x, TUBE_BAY.z, mm(43), mm(14)],
].forEach(([x, z, w, d]) => {
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(w, d), darkMaterial);
  floor.rotation.x = -Math.PI / 2;
  floor.position.set(x, mm(-3.6), z);
  kitCase.add(floor);
});

// Parting line as a perimeter frame, not a plate. A full-footprint box at this
// height is opaque from above and hides all three bays behind a blank lid.
[
  [mm(105.4), mm(2), 0, mm(39.2)],
  [mm(105.4), mm(2), 0, mm(-39.2)],
  [mm(2), mm(76.4), mm(51.7), 0],
  [mm(2), mm(76.4), mm(-51.7), 0],
].forEach(([w, d, x, z]) => {
  const bar = new THREE.Mesh(new THREE.BoxGeometry(w, mm(0.5), d), lidMaterial);
  bar.position.set(x, mm(5), z);
  kitCase.add(bar);
});

// Where the cartridge lands when it is packed, in case-local space
const TUBE_DOCK = new THREE.Vector3(TUBE_BAY.x, mm(1), TUBE_BAY.z);

// ============================================
// EMBOSSED "PIDIA" MARKS
// ============================================
new FontLoader().load(
  "https://raw.githubusercontent.com/danielyl123/person/refs/heads/main/fonts/helvetiker_regular.typeface.json",
  (font) => {
    const brand = (size) => {
      const geometry = new TextGeometry("PIDIA", {
        font,
        size,
        depth: mm(0.7),
        curveSegments: 8,
        bevelEnabled: false,
      });
      geometry.center();
      return geometry;
    };

    // On the rotor lid, angled like the CAD top view
    const discLogo = new THREE.Mesh(brand(mm(7)), logoMaterial);
    discLogo.rotation.x = -Math.PI / 2;
    discLogo.position.set(0, LID_TOP + mm(0.3), mm(-17));
    const discLogoPivot = new THREE.Group();
    discLogoPivot.rotation.y = Math.PI / 4;
    discLogoPivot.add(discLogo);
    spinner.add(discLogoPivot);

    // On the lid of the shipping case
    const caseLogo = new THREE.Mesh(brand(mm(4.5)), logoMaterial);
    caseLogo.rotation.x = -Math.PI / 2;
    caseLogo.position.set(mm(-17), mm(13.4), mm(-34));
    kitCase.add(caseLogo);
  },
);

// ============================================
// STEP SCRIPT
// Each screen holds one object, or two that are actually interacting.
// ============================================
const PARTS = { pen, rotor, cartridge, kitCase };

// The walkthrough's prose is content, so the build owns it: __pediaStepText
// carries one object per step and is merged over the Korean written below.
// Keeping the Korean here rather than emptying it means this file still runs
// standalone, which is how the scene gets debugged.
const STEP_TEXT = globalThis.__pediaStepText ?? null;
// Argument order is Array.map's, not mine — (element, index).
const localise = (step, i) => (STEP_TEXT ? { ...step, ...STEP_TEXT[i] } : step);

const STEPS = [
  {
    no: "00",
    phase: "home",
    tab: "키트",
    kicker: "Kit · 4 parts",
    title: "채혈 · 혈장분리 · 안정화 · 용기",
    lede: "4개 파트 분리 설계. 채혈펜과 채혈침에 기능을 집약해 부피를 축소하고, 잔여 파트는 단일 트레이에 안착. 운송 비용과 키트 부피의 동시 절감을 목적으로 함.",
    specs: [
      ["케이스", "105 × 80 × 26 mm"],
      ["구성", "4 파트 / 1 트레이"],
      ["배송", "상온 · 왕복"],
    ],
    note: "가정 수행 범위 — 1차 혈장 분리까지. 장비 의존 공정은 전량 랩 이관.",
    parts: { kitCase: { position: [0, 0, 0], rotation: [0, -0.5, 0] } },
    camera: {
      target: [0, 0, 0],
      fit: 3.45,
      elevation: 0.62,
      azimuth: 0.52,
    },
    motion: "idle",
  },
  {
    no: "01",
    phase: "home",
    tab: "채혈",
    kicker: "Step 01 · 가정",
    title: "혈액 자가 채취",
    lede: "스프링 장전식 채혈펜. 캡 가압 시 침이 접촉 돔 내부에서만 왕복하며 외부로 노출되지 않음. 자가 사용 안전성과 인허가 적합성을 동시에 고려한 구조.",
    specs: [
      ["외형", "Ø25 × 50 mm"],
      ["플런저 행정", "20 mm"],
      ["접촉 돔", "Ø8 mm"],
      ["침 노출", "2.7 mm (내부)"],
    ],
    note: "침 외부 노출 없음 → 폐기 단계 자상 위험 배제.",
    parts: { pen: { position: [0, 0, 0], rotation: [0, 0.35, 0] } },
    camera: {
      target: [0, 0.1, 0],
      fit: 1.55,
      elevation: 0.16,
      azimuth: 0.3,
    },
    motion: "press",
  },
  {
    no: "02",
    phase: "home",
    tab: "수집",
    kicker: "Step 02 · 가정",
    title: "밀폐 카트리지에 혈액 수집",
    lede: "펜과 카트리지 주입구 결합 시 혈액이 밀폐 상태로 이송. 사용자의 검체 직접 조작 단계가 없어 오염 경로 차단.",
    specs: [
      ["카트리지", "Ø12 × 45 mm"],
      ["채취량", "약 300 µL"],
      ["실링", "고무링 2 mm"],
    ],
    note: "원심분리용 E tube 규격 적용 시 카트리지 부피 추가 축소 가능.",
    parts: {
      // Pen tipped so its dome sits directly over the cartridge mouth
      pen: { position: [0.27, 1.64, 0], rotation: [0, 0.2, 0.3] },
      cartridge: { position: [0.5, -0.75, 0], rotation: [0, 0.3, 0] },
    },
    camera: {
      target: [0, 0.75, 0],
      fit: 2.75,
      elevation: 0.16,
      azimuth: 0.26,
    },
    motion: "transfer",
  },
  {
    no: "03",
    phase: "home",
    tab: "혈장분리",
    kicker: "Step 03 · 가정",
    title: "팽이형 수동 회전 · 1차 혈장 분리",
    lede: "카트리지를 원판 측면 포트에 결합 후 축을 회전. 반경 방향 모래시계형 채널에서 적혈구가 침강해 내측 구간에 포집되고, 상청액인 혈장은 원심 압력으로 사이펀을 넘어 외주 수집링으로 이송. 외부 전원 불필요.",
    specs: [
      ["원판", "Ø65 mm"],
      ["채널 스팬", "58 mm"],
      ["축", "Ø5 mm · 고무링 2 mm"],
      ["로터 전장", "135 mm (E tube 방식)"],
    ],
    note: "대량생산 단가 확보 시 모터 구동 전환 검토.",
    // Rotor alone: the cartridge has already emptied into it, and a tube bolted
    // to a spinning top would fly off. Viewed low, so the separation inside the
    // channel is actually visible through the side wall.
    parts: { rotor: { position: [0, 0, 0], rotation: [0, 0, 0] } },
    camera: {
      target: [0, 0, 0],
      fit: 1.95,
      elevation: 0.14,
      azimuth: 0.2,
    },
    motion: "spin",
  },
  {
    no: "04",
    phase: "home",
    tab: "격리",
    kicker: "Step 04 · 가정",
    title: "혈장 격리",
    lede: "회전 정지 후 외주에 모인 혈장을 밸브를 통해 하부 챔버로 이송, 밸브 1/4 회전으로 잠금. 적혈구층과 물리적 차단 상태이므로 이송 중 재혼합 없음.",
    specs: [
      ["혈장 챔버", "약 150 µL"],
      ["밸브", "1/4 회전 잠금"],
      ["잔여 세포층", "상부 챔버 격리"],
    ],
    note: "잔여 세포·입자 완전 제거를 위한 2차 원심분리 — 랩 공정.",
    parts: { cartridge: { position: [0, 0, 0], rotation: [0, 0.25, 0] } },
    camera: {
      target: [0, 0.1, 0],
      fit: 1.45,
      elevation: 0.12,
      azimuth: 0.3,
    },
    motion: "valve",
  },
  {
    no: "05",
    phase: "home",
    tab: "안정화·배송",
    kicker: "Step 05 · 가정",
    title: "검체 안정화 및 반송 준비",
    lede: "안정화 시약 앰플 압착 후 혈장과 혼합, 카트리지를 케이스 슬롯에 안착. 상온 배송 구간의 cfDNA 분해 억제를 목적으로 함.",
    specs: [
      ["안정화 시약", "앰플 1 · 압착 혼합"],
      ["보관", "상온 72시간"],
      ["반송", "케이스 그대로"],
    ],
    note: "운반·보관 중 위생 오염 가능성 — 별도 검증 항목.",
    // Case left unrotated so the cartridge can drop straight into its bay; the
    // three-quarter look comes from the camera azimuth instead.
    parts: {
      cartridge: { position: [1.5, 1.5, 1.4], rotation: [0, 0, 0] },
      kitCase: { position: [0, -0.4, 0], rotation: [0, 0, 0] },
    },
    camera: {
      target: [0.3, 0.1, 0.2],
      fit: 3.75,
      elevation: 0.46,
      azimuth: 0.62,
    },
    motion: "dock",
  },
  {
    no: "06",
    phase: "lab",
    tab: "LepiDyne",
    kicker: "Lab · LepiDyne",
    title: "랩 수행 공정",
    lede: "마이크로피펫 · vortex · heating bath · 원심분리기 · 자석 스탠드 · 멸균 튜브 의존 공정 전량. 가정용 키트의 수행 범위를 1차 분리까지로 한정한 근거.",
    specs: [
      ["도착 검체", "안정화 혈장 약 150 µL"],
      ["추출", "LepiMag · magnetic bead"],
      ["판독", "MS-HRM real-time PCR"],
    ],
    lists: [
      {
        label: "cfDNA 추출 — LepiMag",
        items: [
          "Proteinase K와 SDS 처리",
          "60℃에서 20분 가열",
          "얼음에서 5분 냉각",
          "Lysis / Binding Solution 첨가",
          "Magnetic Bead 첨가",
          "10분간 강한 vortex",
          "자석을 이용한 bead 분리",
          "Wash Solution 세척",
          "80% 에탄올 세척 2회",
          "bead 건조",
          "50 µL 용출",
          "재차 자석 분리",
        ],
      },
      {
        label: "분석 및 리포트",
        items: [
          "잔여 세포·입자 제거 2차 원심분리",
          "cfDNA 추출",
          "cfDNA 품질 및 농도 확인",
          "메틸화 표적 처리",
          "메틸화 특이 PCR",
          "세포노화 점수 산출",
          "앱 또는 웹 리포트 제공",
        ],
      },
    ],
    parts: { cartridge: { position: [0, 0, 0], rotation: [0, -0.4, 0.22] } },
    camera: { target: [0, 0, 0], fit: 1.45, elevation: 0.2, azimuth: -0.3 },
    motion: "idle",
  },
];

// The hero holds the closed case. It is not a walkthrough step, so it lives
// outside STEPS and the stepper never lists it.
const HERO = {
  no: "00",
  phase: "home",
  tab: "",
  kicker: "PIDIA",
  title: "PIDIA",
  lede: "",
  specs: [],
  parts: { kitCase: { position: [0, 0, 0], rotation: [0, -0.5, 0] } },
  // Loose framing on purpose: the hero copy sits over the object, so the case
  // has to clear the headline and the metrics row at the floor of the viewport.
  camera: { target: [0, 0, 0], fit: 7.2, elevation: 0.44, azimuth: 0.6 },
  motion: "idle",
};

// One place to localise, because every read of a step's copy goes through here.
const SCENES = [...STEPS, HERO].map(localise);
const HERO_STEP = STEPS.length;

// ============================================
// STEP STATE
// ============================================
const partStates = new Map();
for (const [name, group] of Object.entries(PARTS)) {
  group.userData.target = {
    position: new THREE.Vector3(),
    rotation: new THREE.Euler(),
    scale: 0,
  };
  group.scale.setScalar(0.001);
  group.visible = false;
  partStates.set(name, group);
}

const camGoal = {
  position: new THREE.Vector3(),
  target: new THREE.Vector3(),
};
const spherical = new THREE.Spherical();
let userOrbiting = false;
let stepIndex = -1;
let stepTime = 0;

controls.addEventListener("start", () => {
  userOrbiting = true;
});

function applyStep(index, { instant = false } = {}) {
  const step = SCENES[index];
  stepIndex = index;
  stepTime = 0;
  userOrbiting = false;

  for (const [name, group] of partStates) {
    const spec = step.parts[name];
    const t = group.userData.target;
    if (spec) {
      t.position.fromArray(spec.position);
      t.rotation.fromArray(spec.rotation);
      t.scale = 1;
      group.visible = true;
    } else {
      // Parked parts sink and shrink out rather than cross-fading: shared
      // materials make per-part opacity impossible without cloning them.
      // Far enough down to be out of frame even at the widest step.
      t.position.set(t.position.x, -6, t.position.z);
      t.scale = 0;
    }
    if (instant) {
      group.position.copy(t.position);
      group.rotation.copy(t.rotation);
      group.scale.setScalar(Math.max(t.scale, 0.001));
      group.visible = t.scale > 0;
    }
  }

  updateCamGoal();
  if (instant) {
    camera.position.copy(camGoal.position);
    controls.target.copy(camGoal.target);
  }

  renderPanel(step);
  renderChrome(index);
}

// Distance is derived, not authored: the panel eats part of the frustum, so the
// room actually left for the subject depends on viewport and panel width.
function updateCamGoal() {
  const step = SCENES[stepIndex];
  if (!step) return;

  const tan = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
  const usableW = tan * camera.aspect * (1 - 2 * view.shiftX);
  const usableH = tan * (1 - 2 * view.shiftY);
  const distance = THREE.MathUtils.clamp(
    (step.camera.fit * 1.24) / Math.min(usableW, usableH),
    2.6,
    26,
  );

  camGoal.target.fromArray(step.camera.target);
  spherical.set(
    distance,
    Math.PI / 2 - step.camera.elevation,
    step.camera.azimuth,
  );
  camGoal.position.setFromSpherical(spherical).add(camGoal.target);
}

// ============================================
// PANEL / CHROME
// ============================================
const panel = {
  root: document.querySelector(".panel"),
  kicker: document.querySelector(".panel__kicker"),
  title: document.querySelector(".panel__title"),
  lede: document.querySelector(".panel__lede"),
  specs: document.querySelector(".panel__specs"),
  lists: document.querySelector(".panel__lists"),
  note: document.querySelector(".panel__note"),
};

function renderPanel(step) {
  if (!panel.root) return;
  panel.kicker.innerHTML = `<b>${step.no}</b>${step.kicker}`;
  panel.title.textContent = step.title;
  panel.lede.textContent = step.lede;

  panel.specs.replaceChildren(
    ...step.specs.map(([term, value]) => {
      const row = document.createElement("div");
      const dt = document.createElement("dt");
      dt.textContent = term;
      const dd = document.createElement("dd");
      dd.textContent = value;
      row.append(dt, dd);
      return row;
    }),
  );

  panel.lists.replaceChildren(
    ...(step.lists ?? []).map((list) => {
      const section = document.createElement("section");
      const heading = document.createElement("h3");
      heading.textContent = list.label;
      const ol = document.createElement("ol");
      ol.append(
        ...list.items.map((item) => {
          const li = document.createElement("li");
          li.textContent = item;
          return li;
        }),
      );
      section.append(heading, ol);
      return section;
    }),
  );

  panel.note.textContent = step.note ?? "";
  panel.root.scrollTop = 0;
}

const stepper = document.querySelector(".stepper");
stepper?.replaceChildren(
  ...SCENES.slice(0, STEPS.length).map((step, i) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.step = String(i);
    const bar = document.createElement("i");
    const label = document.createElement("span");
    label.textContent = step.tab;
    button.append(bar, label);
    li.append(button);
    return li;
  }),
);

// ============================================
// SCENE MODE
// A layout mode, not a scene identity: "hero" centres the subject and drops it
// below the headline, "kit" shifts it out from under the step panel. One
// document now holds both, so an external controller owns this — see the
// __pediaStage hook at the foot of the file.
// ============================================
let MODE = document.body.dataset.scene || "hero";
const canvas = renderer.domElement;
const stepButtons = [...document.querySelectorAll(".stepbtn")];

function renderChrome(index) {
  if (!stepper) return;
  stepper.querySelectorAll("button").forEach((button) => {
    button.setAttribute(
      "aria-current",
      String(Number(button.dataset.step) === index),
    );
  });
  stepButtons.forEach((button) => {
    const next = index + Number(button.dataset.dir);
    button.disabled = next < 0 || next >= STEPS.length;
  });
}

function goTo(index) {
  const clamped = THREE.MathUtils.clamp(index, 0, STEPS.length - 1);
  if (clamped !== stepIndex) applyStep(clamped);
}

if (stepper) {
  stepper.addEventListener("click", (e) => {
    const button = e.target.closest("button[data-step]");
    if (button) goTo(Number(button.dataset.step));
  });

  stepButtons.forEach((button) => {
    button.addEventListener("click", () => {
      goTo(stepIndex + Number(button.dataset.dir));
    });
  });

  // Arrows belong to the page unless the kit stage is the live scene, and to a
  // focused control regardless.
  window.addEventListener("keydown", (e) => {
    if (MODE !== "kit") return;
    const el = document.activeElement;
    if (el && el !== document.body && el.closest("input, textarea, select"))
      return;
    if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
    e.preventDefault();
    goTo(stepIndex + (e.key === "ArrowRight" ? 1 : -1));
  });

  // Tap the stage to advance; a drag is an orbit, so only count a still pointer
  let tapStart = null;
  canvas.addEventListener("pointerdown", (e) => {
    tapStart = { x: e.clientX, y: e.clientY };
  });
  canvas.addEventListener("pointerup", (e) => {
    if (!tapStart) return;
    const moved = Math.hypot(e.clientX - tapStart.x, e.clientY - tapStart.y);
    tapStart = null;
    if (moved < 6 && MODE === "kit") goTo(stepIndex + 1);
  });
}

// ============================================
// LAYOUT — the step panel owns the left column on wide screens,
// so the stage is shifted out from under it with a frustum offset.
// ============================================
const view = { shiftX: 0, shiftY: 0 };

function layout() {
  const { innerWidth: w, innerHeight: h } = window;
  if (MODE === "hero") {
    // The hero copy is centred over the object, so the stage stays centred too
    // and only drops enough for the headline to clear its top.
    view.shiftX = 0;
    view.shiftY = w <= 900 ? -0.3 : -0.26;
  } else if (w <= 900) {
    view.shiftX = 0;
    view.shiftY = 0.22;
  } else {
    // On the kit page the step panel owns the left column, so the stage is
    // shifted out from under it.
    const gutter = panel.root
      ? panel.root.offsetWidth
      : Math.min(w * 0.34, 480);
    view.shiftX = (gutter * 0.5) / w;
    view.shiftY = 0;
  }
  camera.setViewOffset(w, h, -w * view.shiftX, h * view.shiftY, w, h);
  updateCamGoal();
}

// ============================================
// MOUSE INTERACTION
// ============================================
const plane = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);

window.addEventListener("pointermove", (e) => {
  // This traverses every mesh in the kit. It has no business running while the
  // canvas is dark and a reading section owns the viewport.
  if (!running) return;
  pointer.x = (e.clientX / window.innerWidth) * 2 - 1;
  pointer.y = -(e.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);

  // Intentar interseccion con el kit
  const intersects = raycaster.intersectObject(stage, true);

  if (intersects.length > 0) {
    targetMouse.copy(intersects[0].point);
  } else if (raycaster.ray.intersectPlane(plane, pointerWorld)) {
    // Si no toca el kit, proyectar al plano
    targetMouse.copy(pointerWorld);
  }
});

window.addEventListener("pointerleave", () => {
  targetMouse.set(9999, 9999, 9999);
});

// ============================================
// MOTION — one choreography per step
// ============================================
const easeOut = (t) => 1 - Math.pow(1 - t, 3);
const smoother = (t) => t * t * t * (t * (t * 6 - 15) + 10);
const saw = (t, period) => (t % period) / period;

function setSeparation(sep) {
  // Plasma ends up filling the outer 55% of the channel and packed cells the
  // hub-side 45%, which is roughly a normal haematocrit split.
  const frac = THREE.MathUtils.lerp(1, 0.55, sep);
  const boundary = CH.outer - CH_LEN * frac;
  for (const { side, outerBand, innerBand } of bands) {
    // Scale on Y: that is the cylinder's own axis. Scaling X would squash the
    // radius and leave the band its full length.
    const outerLen = CH.outer - boundary;
    outerBand.scale.y = outerLen / CH_LEN;
    outerBand.position.x = side * (boundary + outerLen / 2);

    const innerLen = boundary - CH.inner;
    innerBand.scale.y = Math.max(innerLen / CH_LEN, 0.0001);
    innerBand.position.x = side * (CH.inner + innerLen / 2);
    innerBand.visible = innerLen > mm(0.4);
  }
  hubDrop.scale.setScalar(THREE.MathUtils.lerp(1, 0.25, sep));
}

function runMotion(step, t) {
  // Neutral pose first, so a step never inherits another step's state
  penDrive.position.y = 0;
  penSpring.scale.y = 1;
  penNeedle.position.y = NEEDLE_REST;
  penDrop.visible = false;
  penDrop.scale.setScalar(1);
  seatDrop();
  valve.rotation.y = 0;
  valveHandle.rotation.y = 0;
  tubeTop.visible = false;
  tubeMid.visible = true;
  tubeMid.scale.y = 1;
  tubeMid.position.y = tubeMidY(1);
  tubeTip.material = TUBE_BELOW_VALVE;
  tubeTip.visible = true;
  tubeTip.scale.y = 1;
  tubeTip.position.y = tubeTipY(1);
  ampoule.visible = false;
  ampoule.scale.y = 1;
  spinner.rotation.y = Math.sin(t * 0.25) * 0.5;
  setSeparation(0);

  switch (step.motion) {
    case "press": {
      const c = saw(t, 3.2);
      const down = c < 0.28 ? easeOut(c / 0.28) : c < 0.4 ? 1 : 0;
      penDrive.position.y = -PEN.travel * down;
      penSpring.scale.y = 1 - 0.55 * down;
      penNeedle.position.y = NEEDLE_REST - NEEDLE_THROW * down;
      penDrop.visible = c > 0.4;
      penDrop.scale.setScalar(c > 0.4 ? Math.min((c - 0.4) / 0.25, 1) : 0.001);
      break;
    }
    case "transfer": {
      const c = saw(t, 4);
      const fill = THREE.MathUtils.clamp((c - 0.15) / 0.5, 0, 1);
      penDrop.visible = fill < 1;
      seatDrop(fill * 1.05);
      tubeMid.visible = false;
      // Nothing has been separated yet, so what pools in the tip here is whole
      // blood — the one step where this band is red.
      tubeTip.material = bloodMaterial;
      tubeTip.scale.y = TIP_FLOOR + (1 - TIP_FLOOR) * fill;
      tubeTip.position.y = tubeTipY(tubeTip.scale.y);
      break;
    }
    case "spin": {
      const c = saw(t, 9);
      // Exactly 7 turns on a smootherstep, so it lands back broadside and the
      // separated bands are legible for most of the cycle rather than a moment.
      spinner.rotation.y =
        14 * Math.PI * smoother(THREE.MathUtils.clamp(c / 0.5, 0, 1));
      setSeparation(
        c < 0.5
          ? smoother(THREE.MathUtils.clamp((c - 0.06) / 0.44, 0, 1))
          : c < 0.9
            ? 1
            : 1 - smoother((c - 0.9) / 0.1),
      );
      break;
    }
    case "valve": {
      const c = saw(t, 4.4);
      const drain = easeOut(THREE.MathUtils.clamp((c - 0.1) / 0.35, 0, 1));
      const shut = easeOut(THREE.MathUtils.clamp((c - 0.5) / 0.25, 0, 1));
      // The separated column starts above the valve. Opening it lets the plasma
      // run down into the lower chamber; the packed cells are what is left up
      // there. The upper band shrinks from its underside — the top of the column
      // does not move — and it stops at CELL_KEEP rather than at nothing, so the
      // two ends still read as one conserved volume.
      tubeTop.visible = true;
      tubeTop.scale.y = 1 - (1 - CELL_KEEP) * drain;
      tubeTop.position.y = tubeTopY(tubeTop.scale.y);
      tubeMid.visible = drain > 0.02;
      tubeMid.scale.y = Math.max(drain, 0.0001);
      tubeMid.position.y = tubeMidY(tubeMid.scale.y);
      // The tip is a cone whose widest face is its top, so squashing it in y
      // alone leaves a full-width disc down where the tube has already tapered
      // past it, and it pokes out under the cartridge. TIP_FLOOR is the scale
      // below which that happens — step 02 fills this same band and carries the
      // same floor for the same reason.
      tubeTip.visible = drain > 0.02;
      tubeTip.scale.y = TIP_FLOOR + (1 - TIP_FLOOR) * drain;
      tubeTip.position.y = tubeTipY(tubeTip.scale.y);
      valve.rotation.y = (Math.PI / 2) * shut;
      valveHandle.rotation.y = (Math.PI / 2) * shut;
      break;
    }
    case "dock": {
      const c = saw(t, 5.2);
      const drop = smoother(THREE.MathUtils.clamp((c - 0.18) / 0.45, 0, 1));
      const press = easeOut(THREE.MathUtils.clamp((c - 0.04) / 0.12, 0, 1));
      // Lies down as it descends: a 45 mm tube cannot stand in a 26 mm case
      const dock = cartridge.userData.target;
      dock.position.y = THREE.MathUtils.lerp(1.5, TUBE_DOCK.y - 0.4, drop);
      dock.rotation.z = (-Math.PI / 2) * drop;
      // Settled: plasma locked below the valve, packed cells above it. The reset
      // above already leaves the two lower bands full.
      tubeTop.visible = true;
      tubeTop.scale.y = CELL_KEEP;
      tubeTop.position.y = tubeTopY(CELL_KEEP);
      valve.rotation.y = Math.PI / 2;
      valveHandle.rotation.y = Math.PI / 2;
      ampoule.visible = true;
      ampoule.scale.y = 1 - 0.45 * press;
      break;
    }
    default: {
      // idle — assembled and gently breathing
      // Settled: plasma locked below the valve, packed cells above it. The reset
      // above already leaves the two lower bands full.
      tubeTop.visible = true;
      tubeTop.scale.y = CELL_KEEP;
      tubeTop.position.y = tubeTopY(CELL_KEEP);
      valve.rotation.y = Math.PI / 2;
      valveHandle.rotation.y = Math.PI / 2;
      setSeparation(1);
    }
  }
}

// ============================================
// ANIMATION LOOP
// ============================================
// Loop length per motion. runMotion is driven entirely by saw(t, period), so
// feeding t = phase * period * scrubTo scrubs the animation with no change to
// the motion maths. scrubTo clips loops whose tail resets state for seamless
// replay — `spin` un-separates the bands after c > 0.9, which a scrub must
// never reach because the step has to rest on its separated result.
const MOTION = {
  press: { period: 3.2, scrubTo: 1 },
  transfer: { period: 4, scrubTo: 1 },
  spin: { period: 9, scrubTo: 0.88 },
  valve: { period: 4.4, scrubTo: 1 },
  dock: { period: 5.2, scrubTo: 1 },
  idle: { period: 25.1, scrubTo: 1 },
};

// null = free-running; 0..1 = driven by an external scrub
let scrubPhase = null;
let running = false;
let rafId = null;

const clock = new THREE.Clock();

const tick = () => {
  const delta = Math.min(clock.getDelta(), 0.05);
  const elapsedTime = clock.elapsedTime;
  if (scrubPhase == null) {
    stepTime += delta;
  } else {
    const m = MOTION[SCENES[stepIndex].motion] ?? MOTION.idle;
    stepTime = scrubPhase * m.period * m.scrubTo;
  }

  // Actualizar tiempo
  meltUniforms.uTime.value = elapsedTime;

  // Interpolacion muy suave - como liquido viscoso
  currentMouse.lerp(targetMouse, 0.025);
  meltUniforms.uMouse.value.copy(currentMouse);

  const step = SCENES[stepIndex];
  runMotion(step, stepTime);

  // Parts ease to their staged transform
  const k = 1 - Math.pow(0.0015, delta);
  for (const group of partStates.values()) {
    const t = group.userData.target;
    group.position.lerp(t.position, k);
    group.rotation.x += (t.rotation.x - group.rotation.x) * k;
    group.rotation.y += (t.rotation.y - group.rotation.y) * k;
    group.rotation.z += (t.rotation.z - group.rotation.z) * k;
    // Leaving parts drop out on a fixed clock — an eased approach to zero
    // lingers for most of a second as a shrinking speck.
    const s =
      t.scale === 0
        ? Math.max(group.scale.x - delta * 5, 0)
        : group.scale.x + (t.scale - group.scale.x) * k;
    group.scale.setScalar(Math.max(s, 0.001));
    group.visible = s > 0.01;
  }

  // Camera flies to the step framing until the viewer grabs it
  if (!userOrbiting) {
    camera.position.lerp(camGoal.position, k);
    controls.target.lerp(camGoal.target, k);
  }

  controls.update();

  renderer.render(scene, camera);

  if (running) rafId = requestAnimationFrame(tick);
};

function setRunning(on) {
  if (on === running) return;
  running = on;
  if (on) {
    clock.start();
    rafId = requestAnimationFrame(tick);
  } else if (rafId != null) {
    cancelAnimationFrame(rafId);
    rafId = null;
    clock.stop();
  }
}

// A transmissive shell makes three.js render the scene twice per frame, so
// stopping the loop off-screen is worth more here than usual.
document.addEventListener("visibilitychange", () => {
  if (document.hidden) setRunning(false);
  else if (sceneMode) setRunning(true);
});

layout();
applyStep(HERO_STEP, { instant: true });
canvas.style.opacity = "1";
setRunning(true);

// ============================================
// EXTERNAL CONTROL
// A global rather than an export: the Artifact build flattens every module into
// one lexical scope, and `stage` is already taken up top. One namespaced global
// has a single collision surface instead of one per export.
// ============================================
let sceneMode = MODE;

window.__pediaStage = {
  get step() {
    return stepIndex;
  },
  stepCount: STEPS.length,
  onStep: null,

  setRunning,

  // name: "hero" | "kit" | null (null = offscreen, keep the last pose)
  setScene(name) {
    if (name === null) {
      sceneMode = null;
      return;
    }
    if (name === sceneMode) return;
    sceneMode = name;
    MODE = name;
    // Order is load-bearing: layout() writes view.shiftX/shiftY and
    // updateCamGoal() reads them, so the frustum shift has to land first.
    layout();
    // HERO_STEP sits outside STEPS, so arriving from the hero has to land on a
    // real step rather than carrying index 7 into the walkthrough.
    applyStep(
      name === "kit"
        ? THREE.MathUtils.clamp(stepIndex, 0, STEPS.length - 1)
        : HERO_STEP,
    );
    setRunning(true);
  },

  setStep(i, opts) {
    const j = THREE.MathUtils.clamp(i, 0, STEPS.length - 1);
    if (j === stepIndex) return;
    applyStep(j, opts);
    this.onStep?.(j);
  },

  // 0..1 within the current step, or null to hand the loop back its own clock
  setPhase(p) {
    scrubPhase = p == null ? null : THREE.MathUtils.clamp(p, 0, 1);
  },
};

document.dispatchEvent(new CustomEvent("pedia:stage-ready"));

// ============================================
// RESIZE
// ============================================
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  layout();
});
