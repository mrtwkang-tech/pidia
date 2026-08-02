# PIDIA

A one-page site for **PIDIA** — a home-collected, multi-omics screening concept
built around a single argument: the problem with cancer screening is not
accuracy, it is reach.

**Live · [pedia-rho.vercel.app](https://pedia-rho.vercel.app)**
&nbsp;·&nbsp; [한국어](https://pedia-rho.vercel.app/)
&nbsp;·&nbsp; [English](https://pedia-rho.vercel.app/en/)

Built for GRAFFITI 2026, Team 8.

---

## What it is

One long scroll, twelve sections, a fixed index rail, and an interactive 3D
walkthrough of the kit pinned mid-page. Two languages off one build.

The editorial rule the whole thing is written against:

> Every element on the page is a measurement, a source, or the object itself.

Every figure carries a source line. Where there is no source, the figure is
labelled an assumption in the same visual register rather than quietly presented
as fact — including the one chart whose vertical axis deliberately has no
numbers on it.

The section titled *What we do not claim* is load-bearing and sits in the middle
of the page, not at the end.

## How it is built

There is no framework and no bundler. `_build/` is a small Python generator that
writes static HTML.

```
_build/
  content.py      every Korean word on the page, as data
  content_en.py   the same sections in English
  steps.py        copy for the 3D walkthrough, both languages
  charts.py       inline SVG figures — no chart library
  worldmap.py     generated dot matrix (from gen_worldmap.py)
  render.py       one template: language × (static | inline)
  bundle.py       asset inlining for the self-contained build
  build.py        writes index.html, en/index.html, _deploy/pedia.html

style.css         one stylesheet, both languages
script.js         three.js scene, kit walkthrough
scroll.js         index rail, pinned scrub, figure reveal
```

```bash
python3 _build/build.py --static     # index.html + en/index.html
python3 _build/build.py              # …and the self-contained page
```

`build.py` refuses to write anything if `content.py` and `content_en.py`
disagree on the section list — that is the failure mode a parallel translation
actually has.

## Notes

**The 3D scene** is three.js. Every dimension in it is the millimetre figure off
the CAD sketch. `OrbitControls` is deliberately connected with `enableZoom`
off — its defaults write `touch-action: none` on a full-viewport fixed canvas
and swallow the page's own scrolling.

**The kit walkthrough** is scrubbed by scroll, not clicked. The scene's motion
functions are pure functions of time, so mapping scroll position onto phase
needed no change to the motion maths.

**The figures** are static SVG generated at build time. A thousand dots cost one
DOM node: each is a zero-length subpath drawn through a round line cap. The
world map's 6,832 land cells use the same trick.

**Colour** is one hue at two weights. `#b8e5e0` is unusable as ink on white
(1.37:1) and excellent as a fill, so it marks emphasis blocks only; `#0a5b52` is
the same hue with the lights off and carries all type and rules.

## Disclaimer

This is a student team project. Nothing here is medical advice, and nothing here
is an offer of any product or security. Figures were checked against their
original sources as of July 2026; pre-peer-review presentations and preprints
are marked as such in the text.
