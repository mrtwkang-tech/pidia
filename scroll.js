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

  /** Hold the canvas inside the section it belongs to.
   *
   *  The canvas is one fixed element covering the whole viewport, but it is only
   *  meant to be part of two sections. Hero and kit are the only transparent
   *  ones, so wherever their edge sits mid-screen the object shows through into
   *  the neighbour — for 450px of scrolling either side of the kit it rises into
   *  the bottom of the solution section like a third thing on the page.
   *
   *  Clipping to the live section's own rect makes the fixed canvas behave as if
   *  it were painted inside that section: it ends where the section ends. */
  function clipTo(el) {
    if (!gl) return;
    if (!el) {
      gl.style.clipPath = "";
      return;
    }
    const r = el.getBoundingClientRect();
    const h = viewH();
    const top = Math.max(0, r.top);
    const bottom = Math.max(0, h - r.bottom);
    gl.style.clipPath =
      top || bottom ? `inset(${top}px 0 ${bottom}px 0)` : "none";
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
        stage.setStep(step, { instant: true });
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

    // Kit wins ties: it is the section that needs the stage interactive.
    const kitOn = midCrosser(section);
    const next = kitOn ? "kit" : midCrosser(hero) ? "hero" : null;

    if (next !== live) {
      live = next;
      gl?.classList.toggle("is-live", next !== null);
      stage.setScene(next);
      if (next !== "kit") {
        stage.setPhase(null);
        step = -1;
      }
      if (next === null) {
        // Let the fade finish before the renderer stops.
        setTimeout(() => {
          if (live === null) stage.setRunning(false);
        }, 520);
      }
    }

    // Re-clipped every frame, not just on the scene change: the section's edge
    // is moving the whole time it is on screen.
    clipTo(next === "kit" ? section : next === "hero" ? hero : null);

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
