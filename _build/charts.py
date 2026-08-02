#!/usr/bin/env python3
"""Inline SVG figures.

Every figure here is drawn from a number that is already stated in content.py
and already carries a source line there. Nothing on this page is invented to
make a chart look better — if a series needed a value the deck does not publish,
the chart was cut instead of filled in.

No runtime JavaScript and no chart library. These are static SVG built once at
build time, which keeps them identical in both outputs and keeps the page's only
script budget on the 3D stage.

Colour comes from CSS custom properties rather than literals, so the figures
follow the palette instead of pinning a copy of it.
"""

import regions
import worldmap

# ────────────────────────────────────────────────────────── dot fields


def _dot_path(count, cols, step):
    """`count` dots on a `cols`-wide grid as one path.

    Each dot is a zero-length subpath. With stroke-linecap:round the renderer
    caps it into a circle, so a thousand dots cost one node instead of a
    thousand — the same trick the world map uses for its 6,832 land cells.
    """
    parts = []
    for i in range(count):
        x = (i % cols) * step + step / 2
        y = (i // cols) * step + step / 2
        parts.append(f"M{x:.1f},{y:.1f}h0")
    return "".join(parts)


def dotfield(total, hit, cols, label, value, note, src_class="src"):
    """A field of `total` dots with the first `hit` marked.

    Proportions this extreme stop being readable as a bar — 0.17% of a bar is
    thinner than its own outline. As a field you can count the marked dots,
    which is the entire point of quoting the number.
    """
    rows = -(-total // cols)
    step = 10
    w, h = cols * step, rows * step
    rest = total - hit
    return f"""
<figure class="field">
  <svg class="field__svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMinYMid meet"
       role="img" aria-label="{label} — {hit} / {total}">
    <path class="field__rest" d="{_dot_path(total, cols, step)}" />
    <path class="field__hit" d="{_dot_path(hit, cols, step)}" />
  </svg>
  <figcaption class="field__cap">
    <b class="num">{value}</b>
    <span>{label}</span>
    <i>{note}</i>
  </figcaption>
</figure>
"""


# ────────────────────────────────────────────────────────── bar figures


def bars(rows, unit="", caption="", ours=None):
    """Horizontal bars on a shared linear scale.

    Linear, not log: the whole reason to draw the price ladder is that the top
    of the market is twenty-eight times the bottom, and a log axis is exactly
    the transform that hides that.
    """
    top = max(r[1] for r in rows) or 1
    out = []
    for name, val, text, note in rows:
        mine = ours is not None and name == ours
        cls = " bar__row--ours" if mine else ""
        out.append(
            f'  <div class="bar__row{cls}">'
            f'<span class="bar__name">{name}</span>'
            f'<span class="bar__track"><i style="--w: {val / top * 100:.1f}%"></i></span>'
            f'<span class="bar__val num">{text}</span>'
            f'<span class="bar__note">{note}</span>'
            f"</div>"
        )
    cap = f'<figcaption class="bar__cap">{caption}</figcaption>' if caption else ""
    nl = "\n"
    return f"""
<figure class="bar" role="img" aria-label="{caption}">
{nl.join(out)}
  {cap}
</figure>
"""


def gapbars(a, b, caption="", lead=None):
    """Two bars, with the caption led by whatever the comparison is *for*.

    `lead` defaults to the ratio between them, which is the point when the story
    is "the estimate is N times the reality". Pass "" where a ratio would be
    noise — a performance collapse is not a ratio, it is a floor.
    """
    (an, av, at), (bn, bv, bt) = a, b
    top = max(av, bv) or 1
    if lead is None:
        lead = f"{av / bv:.1f}&times;" if bv else ""
    lead = f'<b class="num">{lead}</b>' if lead else ""
    return f"""
<figure class="gap" role="img" aria-label="{an} {at} 대 {bn} {bt}">
  <div class="gap__row">
    <span class="gap__name">{an}</span>
    <span class="gap__track"><i style="--w: {av / top * 100:.1f}%"></i></span>
    <span class="gap__val num">{at}</span>
  </div>
  <div class="gap__row gap__row--real">
    <span class="gap__name">{bn}</span>
    <span class="gap__track"><i style="--w: {bv / top * 100:.1f}%"></i></span>
    <span class="gap__val num">{bt}</span>
  </div>
  <figcaption class="gap__cap">{lead}<span>{caption}</span></figcaption>  <!-- the caption is wrapped because a grid container promotes every child, including an inline <b>, to a grid item -->
</figure>
"""


def deltabars(rows, ref_label, caption="", axis_label="", subject=""):
    """Metrics against a reference value, drawn as deviation from a centre line.

    Georgia's case is not that any one number is alarming; it is that four
    unrelated indicators all lean the same way. Deviation bars off a shared
    baseline show that at a glance, where four separate stat cards do not.
    """
    span = max(abs(r[3]) for r in rows) or 1
    out = []
    for name, val, ref, delta, good in rows:
        side = "pos" if delta >= 0 else "neg"
        # "Worse" is what makes the market, so the colour follows the market
        # reading rather than the arithmetic sign.
        tone = " is-market" if not good else ""
        out.append(
            f'  <div class="delta__row">'
            f'<span class="delta__name">{name}</span>'
            f'<span class="delta__track">'
            f'<i class="delta__bar delta__bar--{side}{tone}"'
            f' style="--w: {abs(delta) / span * 50:.1f}%"></i></span>'
            f'<span class="delta__val num">{val}</span>'
            f'<span class="delta__ref num">{ref}</span>'
            f"</div>"
        )
    nl = "\n"
    return f"""
<figure class="delta" role="img" aria-label="{caption}">
  <div class="delta__head">
    <span></span><span>{axis_label}</span>
    <span>{subject}</span><span>{ref_label}</span>
  </div>
{nl.join(out)}
  <figcaption class="delta__cap">{caption}</figcaption>
</figure>
"""


# ────────────────────────────────────────────────────────── timeline bars


def timeline(cols, rows, caption=""):
    """Phase bars on a shared column grid.

    Revived from the retired pipeline figure. The grid is the schedule, so a bar
    that spans columns 1–3 is making a claim about duration, not decoration.
    """
    heads = "".join(f'<span class="tl__col">{c}</span>' for c in cols)
    body = []
    for label, note, spans in rows:
        cells = "".join(
            f'<span class="tl__bar tl__bar--{kind}"'
            f' style="grid-column: {a} / {b}">{text}</span>'
            for a, b, kind, text in spans
        )
        body.append(
            f'    <div class="tl__row">'
            f'<span class="tl__label"><b>{label}</b><i>{note}</i></span>'
            f'<span class="tl__track">{cells}</span></div>'
        )
    nl = "\n"
    cap = f'<figcaption class="tl__cap">{caption}</figcaption>' if caption else ""
    return f"""
<figure class="tl">
  <div class="tl__scroll">
    <div class="tl__grid" style="--cols: {len(cols)}">
      <div class="tl__row tl__row--head"><span class="tl__label"></span>
        <span class="tl__track">{heads}</span></div>
{nl.join(body)}
    </div>
  </div>
  {cap}
</figure>
"""


# ────────────────────────────────────────────────────────── world map



def wmap(stops, aria="", legend=()):
    """Dot-matrix world map where the territory fills in, stage by stage.

    The earlier version popped four rings and drew three arcs, which said the
    order but not the size — and the size is the whole argument. Now the actual
    country outlines fill over the dot raster and stay filled, so a single state
    is visibly a rounding error against the country, and the country is a
    rounding error against the continent that follows it.

    Regions accumulate. Nothing that has been entered is ever un-drawn, because
    the claim is coverage, not a tour.

    Motion is an enhancement: every number in it is also written into the stage
    cards underneath, so a reader who scrolls past the animation loses nothing.
    """
    xy = [worldmap.project(s["lon"], s["lat"]) for s in stops]

    def arc(a, b, bow):
        (x0, y0), (x1, y1) = a, b
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - bow
        return f"M{x0:.2f},{y0:.2f} Q{cx:.2f},{cy:.2f} {x1:.2f},{y1:.2f}"

    # Filled territory, back to front. Georgia is drawn last of the fills so its
    # outline survives the United States being painted over it.
    fills = []
    for i, stop in enumerate(stops):
        key = stop.get("region")
        if not key:
            continue
        fills.append(
            (
                stop.get("paint", 0),
                f'      <path class="wmap__fill wmap__fill--{key}" style="--i: {i}"'
                f' d="{regions.PATHS[key]}" />',
            )
        )
    # Paint order is by size, not by stage: Georgia sits inside the United States
    # and was being covered by the very fill that is supposed to dwarf it.
    fills = [p for _, p in sorted(fills, key=lambda f: f[0])]

    # Arcs only where the expansion is a jump. Georgia to the rest of the United
    # States is containment, not a journey, and drawing it as a flight line said
    # the opposite of what the two fills say.
    arcs = []
    leg = 0
    for i in range(len(stops) - 1):
        if stops[i + 1].get("jump"):
            arcs.append(
                f'      <path class="wmap__arc" style="--i: {i + 1}"'
                f' d="{arc(xy[i], xy[i + 1], stops[i + 1]["bow"])}" />'
            )
            leg += 1

    # No rings. The filled territory is the marker, and a ring big enough to see
    # at this scale was wider than Georgia — four of them, plus city dots,
    # stacked into a knot over the one region the figure is about.
    nodes = []
    for i, (stop, (x, y)) in enumerate(zip(stops, xy)):
        sats = "".join(
            f'\n        <circle class="wmap__sat" cx="{sx:.2f}" cy="{sy:.2f}" r="0.7" />'
            for sx, sy in (worldmap.project(lo, la) for lo, la, _ in stop["sats"])
        )
        dx, dy = stop["nudge"]
        anchor = "end" if dx < 0 else "start"
        nodes.append(
            f'      <g class="wmap__node" style="--i: {i}">'
            f"{sats}"
            f'\n        <circle class="wmap__pin" cx="{x:.2f}" cy="{y:.2f}" r="0.9" />'
            f'\n        <line class="wmap__leader" x1="{x:.2f}" y1="{y:.2f}"'
            f' x2="{x + dx * 0.82:.2f}" y2="{y + dy * 0.82:.2f}" />'
            f'\n        <text class="wmap__tag" text-anchor="{anchor}"'
            f' x="{x + dx:.2f}" y="{y + dy:.2f}">'
            f'<tspan class="wmap__tagseq">{stop["seq"]}</tspan>'
            f'<tspan dx="1.4">{stop["name"]}</tspan></text>'
            f'\n        <text class="wmap__sub" text-anchor="{anchor}"'
            f' x="{x + dx:.2f}" y="{y + dy + 4.2:.2f}">{stop["tag"]}</text>'
            f"\n      </g>"
        )

    cards = []
    for i, stop in enumerate(stops):
        facts = "".join(
            f'<li><b class="num">{v}</b><span>{l}</span></li>' for v, l in stop["facts"]
        )
        cards.append(
            f'    <li class="wmap__stage" style="--i: {i}">'
            f'<p class="wmap__seq num">{stop["seq"]}</p>'
            f"<h3>{stop['name']}</h3>"
            f'<p class="wmap__role">{stop["role"]}</p>'
            f'<ul class="wmap__facts">{facts}</ul>'
            f'<p class="wmap__why">{stop["why"]}</p></li>'
        )

    keys = "".join(f"<li><i></i>{t}</li>" for t in legend)
    nl = "\n"
    return f"""
<figure class="wmap">
  <div class="wmap__canvas">
    <svg class="wmap__svg" viewBox="{worldmap.VIEWBOX}" role="img" aria-label="{aria}">
      <path class="wmap__land" d="{worldmap.DOT_PATH}" />
{nl.join(fills)}
{nl.join(arcs)}
{nl.join(nodes)}
    </svg>
  </div>
  <ol class="wmap__stages">
{nl.join(cards)}
  </ol>
  <ul class="wmap__legend">{keys}</ul>
</figure>
"""


# ──────────────────────────────────────────────────── milestone descent


def milestones(rows, caption, note, axis_y="", axis_x=""):
    """Remaining uncertainty as a descending staircase.

    The section's claim is that the most uncertain thing is tested first, and a
    list cannot show that — every row of a list looks the same size. A descent
    can, because the first step is visibly the tallest.

    The *order* of the drops is the deck's own risk ranking. The *heights* are a
    rendering of that ranking and not a measured quantity, so the axis carries no
    numbers and the note under the figure says so outright.
    """
    W, H = 120.0, 26.0
    pad = 2.4
    n = len(rows)
    step = (W - pad * 2) / n
    levels = [r[3] for r in rows]

    def y(v):
        return pad + (100 - v) / 100 * (H - pad * 2)

    d = [f"M{pad:.1f},{y(100):.1f}"]
    marks, ticks = [], []
    for i, (_, _, _, lvl, _) in enumerate(rows):
        x1 = pad + step * (i + 1)
        prev = 100 if i == 0 else levels[i - 1]
        d.append(f"H{x1:.1f}V{y(lvl):.1f}")
        marks.append(
            f'    <circle class="msg__dot{" msg__dot--risk" if rows[i][4] else ""}"'
            f' cx="{x1:.1f}" cy="{y(lvl):.1f}" r="1.1" />'
        )
        ticks.append(
            f'    <line class="msg__drop" x1="{x1:.1f}" y1="{y(prev):.1f}"'
            f' x2="{x1:.1f}" y2="{y(lvl):.1f}" />'
        )
    nl = "\n"
    cells = "".join(
        f'    <li class="msg__item{" msg__item--risk" if risk else ""}" style="--i: {i}">'
        f'<b class="num">{tag}</b><span class="msg__when num">{when}</span>'
        f'<span class="msg__what">{what}</span></li>'
        for i, (tag, when, what, _, risk) in enumerate(rows)
    )
    return f"""
<figure class="msg">
  <svg class="msg__svg" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="{caption}">
    <line class="msg__axis" x1="{pad}" y1="{H - pad}" x2="{W - pad}" y2="{H - pad}" />
{nl.join(ticks)}
    <path class="msg__line" d="{" ".join(d)}" />
{nl.join(marks)}
  </svg>
  <p class="msg__axislabel"><span>{axis_y}</span><span>{axis_x}</span></p>
  <ol class="msg__items">
{cells}
  </ol>
  <figcaption class="msg__cap">{caption}</figcaption>
</figure>
{note}
"""
