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


def gapbars(a, b, caption=""):
    """Two bars where the story is the ratio between them."""
    (an, av, at), (bn, bv, bt) = a, b
    top = max(av, bv) or 1
    ratio = av / bv if bv else 0
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
  <figcaption class="gap__cap"><b class="num">{ratio:.1f}&times;</b>{caption}</figcaption>
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



def wmap(stops, aria=""):
    """Dot-matrix world map with the entry sequence drawn over it.

    Static rather than the stepper the retired version had. On a page that is
    one long scroll the reader is already moving; a figure that also demands to
    be clicked competes with the scroll instead of supporting it.
    """
    xy = [worldmap.project(s["lon"], s["lat"]) for s in stops]

    def arc(a, b, bow):
        (x0, y0), (x1, y1) = a, b
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 - bow
        return f"M{x0:.2f},{y0:.2f} Q{cx:.2f},{cy:.2f} {x1:.2f},{y1:.2f}"

    # Bow each leg away from the one before so three hops across one hemisphere
    # do not collapse into a single line. --leg drives the draw stagger in CSS.
    bows = [7, 30, -26]
    arcs = [
        f'      <path class="wmap__arc" style="--leg: {i}"'
        f' d="{arc(xy[i], xy[i + 1], bows[i])}" />'
        for i in range(len(stops) - 1)
    ]

    # Territory discs are emitted ahead of every pin. They are semi-transparent
    # and stop 02's disc contains stop 01, so drawing them in group order painted
    # the United States over Georgia's own marker.
    halos = [
        f'      <circle class="wmap__halo" style="--i: {i}" cx="{x:.2f}" cy="{y:.2f}" r="{st["r"]}" />'
        for i, (st, (x, y)) in enumerate(zip(stops, xy))
        if st.get("r")
    ]

    nodes = []
    for i, (stop, (x, y)) in enumerate(zip(stops, xy)):
        sats = "".join(
            f'\n        <circle class="wmap__sat" cx="{sx:.2f}" cy="{sy:.2f}" r="1.2" />'
            for sx, sy in (worldmap.project(lo, la) for lo, la, _ in stop["sats"])
        )
        # Stop 02 is a territory, not a place. Georgia sits inside it and the two
        # are five degrees apart at world scale, so drawing both as pins put one
        # marker on top of another and claimed they were different points.
        pin = (
            ""
            if stop.get("r")
            else f'\n        <circle class="wmap__ring" cx="{x:.2f}" cy="{y:.2f}" r="3.4" />'
            f'\n        <circle class="wmap__pin" cx="{x:.2f}" cy="{y:.2f}" r="1.6" />'
        )
        dx, dy = stop["nudge"]
        nodes.append(
            f'      <g class="wmap__node wmap__node--{stop["kind"]}" style="--i: {i}">'
            f"{sats}{pin}"
            f'\n        <text class="wmap__seqmark" x="{x + dx:.2f}" y="{y + dy:.2f}">'
            f'{stop["seq"]}</text>'
            f"\n      </g>"
        )
    labels = []

    stops = []
    for stop in stops:
        kpi = "".join(f"<li>{k}</li>" for k in stop["kpi"])
        tam = " wmap__stop--tam" if stop["kind"] == "tam" else ""
        stops.append(
            f'    <li class="wmap__stop{tam}">'
            f'<p class="wmap__seq num">{stop["seq"]}</p>'
            f"<h3>{stop['name']}</h3>"
            f'<p class="wmap__role">{stop["role"]}</p>'
            f'<p class="wmap__note">{stop["note"]}</p>'
            f'<ul class="wmap__kpi">{kpi}</ul></li>'
        )

    nl = "\n"
    return f"""
<figure class="wmap">
  <div class="wmap__canvas">
    <svg class="wmap__svg" viewBox="{worldmap.VIEWBOX}" role="img"
      aria-label="{aria}">
      <path class="wmap__land" d="{worldmap.DOT_PATH}" />
{nl.join(halos)}
{nl.join(arcs)}
{nl.join(nodes)}
    </svg>
  </div>
  <ol class="wmap__stops">
{nl.join(stops)}
  </ol>
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

    # Start at full uncertainty, then drop once per milestone.
    d = [f"M{pad:.1f},{y(100):.1f}"]
    marks, ticks = [], []
    for i, (_, _, _, lvl, _) in enumerate(rows):
        x0 = pad + step * i
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
        f"<span class=\"msg__what\">{what}</span></li>"
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
