/* ============================================================
   Scroll layer — rail, section spy, and the pinned kit scrub.

   One mechanism: a rAF loop that reads element rects. No scroll listeners and
   no IntersectionObserver.

   That is a deliberate simplification, not an oversight. A scrub wants the
   position every frame regardless — sampling on `scroll` lags behind momentum
   and lands the steps late — so the loop has to exist anyway, and once it does,
   the other two mechanisms are redundant surface area. Three rect reads per
   frame is nothing; the expensive thing on this page is the WebGL renderer, and
   that is gated separately through stage.setRunning().
   ============================================================ */
(() => {
  "use strict";

  const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // The inline (Artifact) build owns its own scroller: the host frame sizes
  // itself to content height, so a seven-viewport spacer would push scrolling up
  // to the parent where getBoundingClientRect stops changing. Everything below
  // reads rects rather than scroll offsets, so this is the only place it shows.
  const doc = document.querySelector(".doc");

  const section = document.getElementById("kit");
  const pin = section?.querySelector(".kitscroll__pin");
  const hero = document.getElementById("hero");
  const gl = document.querySelector("canvas.webgl");
  const railCount = document.querySelector(".rail__count");

  const railLinks = [...document.querySelectorAll(".rail a")];
  const targets = railLinks.map((a) =>
    document.querySelector(a.getAttribute("href")),
  );

  // Figures that play once when they arrive. The loop below already reads rects
  // every frame, so this is a comparison rather than a new mechanism, and the
  // element drops out of the list the moment it fires.
  let pending = [...document.querySelectorAll(".wmap")];

  let stage = null;
  let step = -1;
  let live = null;
  let activeRail = -1;

  const HYST = 0.02; // step-widths of deadband at a boundary
  const pad = (n) => String(n + 1).padStart(2, "0");
  const viewH = () => (doc ? doc.clientHeight : innerHeight);

  function midCrosser(el) {
    if (!el) return false;
    const r = el.getBoundingClientRect();
    const mid = viewH() / 2;
    return r.top < mid && r.bottom > mid;
  }

  /** Which transparent section the canvas is currently standing in.
   *
   *  The canvas is one fixed element covering the whole viewport, but only two
   *  of the twelve sections are transparent and meant to show it. Kit is tested
   *  first because it is the one that needs the stage interactive.
   *
   *  Contact, not the midpoint: gating on the middle of the screen meant the
   *  object switched on when the section was already half-way up, so it appeared
   *  in a strip and then grew. Riding in on the section's own edge is what makes
   *  it read as part of the page rather than as a layer behind it. */
  function stageWindow() {
    const h = viewH();
    for (const el of [section, hero]) {
      if (!el) continue;
      const r = el.getBoundingClientRect();
      if (r.bottom > 0 && r.top < h) return { el, r };
    }
    return null;
  }

  // Length of the soft edge where the window cuts through the middle of the
  // screen. The two sections either side of the canvas are white on white, so a
  // hard clip guillotines the object across a line the reader cannot see and
  // reads as a rendering fault rather than as a boundary.
  const FEATHER = 72;

  /** Mask the canvas to that window, so a fixed element behaves as if it were
   *  painted inside the section.
   *
   *  A mask rather than clip-path: same window, but the edges can ramp. The ramp
   *  is applied only to an edge that is actually inside the viewport — once the
   *  section fills the screen both edges are off-screen and the object is whole.
   *
   *  Never cleared. Clearing was the bug: past the kit's midpoint the clip came
   *  off while 450px of the kit section was still on screen and still
   *  transparent, so the object hung behind the section after it. */
  function maskTo(r) {
    if (!gl) return;
    if (!r) {
      gl.style.maskImage = gl.style.webkitMaskImage = "linear-gradient(#0000,#0000)";
      return;
    }
    const h = viewH();
    const top = Math.max(0, r.top);
    const bot = Math.min(h, r.bottom);
    // Never let the two ramps overlap and cancel the window out entirely.
    const room = Math.max(bot - top, 1);
    const f = Math.min(FEATHER, room / 2);
    const a = r.top > 0 ? top + f : top;
    const b = r.bottom < h ? bot - f : bot;

    // Ride the section in, then lock.
    //
    // Before the pin sticks, the panel is still scrolling up the page while the
    // canvas is fixed, so the two halves of the same figure move at different
    // rates and the section reads as a layer the page is passing over. Centring
    // the object in the *visible* strip instead of the viewport puts it back on
    // the section's own clock; the offset falls to zero the moment the section
    // fills the screen, which is also the moment the pin takes over.
    const shift = (top + bot) / 2 - h / 2;
    gl.style.transform = shift ? `translateY(${shift.toFixed(1)}px)` : "";

    // The mask is resolved against the element's own box, and the transform
    // above has just moved that box — so the stops are written in the element's
    // space, not the viewport's. Subtracting the shift puts the window back on
    // the section edge where it belongs; without it the object bleeds `shift`
    // pixels past the boundary, which is the leak this whole function exists to
    // close.
    const px = (v) => `${(v - shift).toFixed(1)}px`;
    gl.style.maskImage = gl.style.webkitMaskImage =
      `linear-gradient(to bottom,#0000 ${px(top)},#000 ${px(a)},` +
      `#000 ${px(b)},#0000 ${px(bot)})`;
  }

  /** Travel is measured, not assumed, so CSS can change --kit-dwell without
   *  this file knowing. Zero travel — short viewport, or reduced motion
   *  collapsing the spacer — falls through to discrete click mode. */
  function kitProgress() {
    if (!section || !pin) return null;
    const travel = section.offsetHeight - pin.offsetHeight;
    if (travel <= 0) return null;
    return clamp(-section.getBoundingClientRect().top / travel, 0, 1);
  }

  function applyScrub(p) {
    const n = stage.stepCount;
    const raw = clamp(p * n, 0, n - 1e-4);
    const want = Math.floor(raw);

    if (want !== step) {
      // Deadband the crossing, not the band: flooring alone chatters under
      // trackpad inertia. A multi-step jump has past > 1 and fires at once.
      const past = step < 0 ? 1 : want > step ? raw - (step + 1) : step - raw;
      if (past > HYST) {
        step = want;
        // Eased, not instant. The parts and camera already lerp toward their
        // staged transform in about a third of a second, and a hard cut between
        // two smoothly scrubbing stretches was the jolt that made the whole
        // section feel unfinished.
        stage.setStep(step);
        if (railCount) railCount.textContent = `${pad(step)} / ${pad(n - 1)}`;
      }
    }
    stage.setPhase(clamp(raw - step, 0, 1));
    document.documentElement.style.setProperty("--kit-p", (raw / n).toFixed(4));
  }

  function updateRail() {
    let found = -1;
    for (let i = 0; i < targets.length; i++) {
      const el = targets[i];
      if (!el) continue;
      if (el.getBoundingClientRect().top <= viewH() / 2) found = i;
    }
    if (found === activeRail) return;
    activeRail = found;
    railLinks.forEach((a, i) => {
      const on = i === found;
      a.classList.toggle("is-active", on);
      if (on) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  }

  /** Fire once, when two thirds of the figure is above the viewport floor. */
  function revealPending() {
    if (!pending.length) return;
    const h = viewH();
    pending = pending.filter((el) => {
      const r = el.getBoundingClientRect();
      if (r.top < h * 0.85 && r.bottom > 0) {
        el.classList.add("is-drawn");
        return false;
      }
      return true;
    });
  }

  function update() {
    updateRail();
    revealPending();
    if (!stage) return;

    // Re-measured every frame, not just on the scene change: the section's edge
    // is moving the whole time it is on screen.
    const win = stageWindow();
    maskTo(win?.r ?? null);

    const kitOn = win?.el === section;
    const next = win ? (kitOn ? "kit" : "hero") : null;

    if (next !== live) {
      live = next;
      stage.setScene(next);
      if (next !== "kit") {
        stage.setPhase(null);
        step = -1;
      }
      // The clip has already hidden it, so there is nothing to wait for.
      if (next === null) stage.setRunning(false);
    }

    if (kitOn) {
      const p = kitProgress();
      if (p !== null) applyScrub(p);
      else stage.setPhase(null);
    }
  }

  function loop() {
    update();
    requestAnimationFrame(loop);
  }

  function attach(s) {
    stage = s;
    // Keep the rail honest when the viewer uses the step buttons or the arrow
    // keys instead of the scroll.
    stage.onStep = (i) => {
      step = i;
      if (railCount) {
        railCount.textContent = `${pad(i)} / ${pad(stage.stepCount - 1)}`;
      }
    };
    update();
  }

  if (window.__pediaStage) attach(window.__pediaStage);
  else {
    document.addEventListener("pedia:stage-ready", () =>
      attach(window.__pediaStage),
    );
  }

  // The rail works before three.js finishes downloading.
  requestAnimationFrame(loop);

  // ─────────────────────────────────────────────── anchor jumps
  // html { scroll-behavior: smooth } would otherwise play a fly-through of every
  // intervening step on the way to a rail target.
  for (const a of document.querySelectorAll(
    '.rail a, .skip, .topbar a[href^="#"]',
  )) {
    a.addEventListener("click", (e) => {
      const el = document.querySelector(a.getAttribute("href"));
      if (!el) return;
      e.preventDefault();
      const base = doc ? doc.scrollTop : scrollY;
      (doc || window).scrollTo({
        top: base + el.getBoundingClientRect().top,
        behavior: "instant",
      });
      el.setAttribute("tabindex", "-1");
      el.focus({ preventScroll: true });
    });
  }

  if (reduced) document.documentElement.classList.add("reduced-motion");
})();
