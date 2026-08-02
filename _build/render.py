#!/usr/bin/env python3
"""One template, two languages, two output modes.

  static  — links /style.css, /scroll.js, /script.js and the three.js importmap.
            This is what Vercel serves, at / and /en/.
  inline  — everything embedded: flattened three.js, base64 subset fonts, the
            typeface JSON. This is what an Artifact can host, since its CSP
            blocks every external request.

Language changes the words and nothing else. Both pages load the same stylesheet
and the same 3D scene; the walkthrough's copy arrives as data through
`window.__pediaStepText` rather than by forking script.js.

Asset paths are absolute so /en/index.html resolves them from the site root
instead of looking for /en/style.css.
"""

import json
import pathlib

import bundle
import steps

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Per-language chrome. Everything else comes from the content module.
LANGS = {
    "ko": {
        "html": "ko",
        "href": "/",
        "title": "PIDIA — 검사의 문턱을 없앤다",
        "desc": (
            "채혈센터도 예약도 없이 집에서 시작하는 다중 오믹스 검사. 정확도가 아니라 "
            "도달 거리로 경쟁합니다. 조지아에서 시작합니다."
        ),
        "skip": "본문으로 건너뛰기",
        "nav": "섹션",
        "steps": steps.KO,
    },
    "en": {
        "html": "en",
        "href": "/en/",
        "title": "PIDIA — Removing the threshold to getting tested",
        "desc": (
            "Multi-omics screening that starts at home, with no draw centre and "
            "no appointment. We do not compete on accuracy. We compete on reach. "
            "We start in Georgia."
        ),
        "skip": "Skip to content",
        "nav": "Sections",
        "steps": steps.EN,
    },
}

IMPORTMAP = """  <script type="importmap">
    {
      "imports": {
        "three": "https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js",
        "jsm/": "https://cdn.jsdelivr.net/npm/three@0.182.0/examples/jsm/"
      }
    }
  </script>
"""

# Wanted Sans ships a split build: ~60 unicode-range slices of the variable
# font, so a page of Hangul pulls the few hundred KB it actually renders instead
# of the whole 2 MB face. The English page pulls almost none of them.
WEBFONTS = """  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin />
  <link rel="stylesheet"
    href="https://cdn.jsdelivr.net/gh/wanteddev/wanted-sans@v1.0.3/packages/wanted-sans/fonts/webfonts/variable/split/WantedSansVariable.min.css" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300..700&amp;family=Noto+Serif+KR:wght@300..800&amp;family=Roboto+Mono:wght@400;500&amp;display=swap" />
"""


def rail(content, cfg):
    """Section index. The kit entry carries a progress fill and a step readout;
    the seven labelled step controls stay inside the pin rather than being
    duplicated here."""
    items = []
    for s in content.SECTIONS:
        kit = s["id"] == "kit"
        count = (
            '<b class="rail__count num" aria-live="polite">01 / 07</b>' if kit else ""
        )
        items.append(
            f'      <li{" class=\"rail__kit\"" if kit else ""}>'
            f'<a href="#{s["id"]}"><i></i><span>{s["label"]}</span>{count}</a></li>'
        )
    nl = "\n"
    return f"""  <a class="skip" href="#hero">{cfg["skip"]}</a>
  <nav class="rail" aria-label="{cfg["nav"]}">
    <ol>
{nl.join(items)}
    </ol>
  </nav>
"""


def sections(content):
    out = []
    for s in content.SECTIONS:
        out.append(
            f'    <section class="{s["cls"]}" id="{s["id"]}">\n{s["html"]}\n    </section>'
        )
    return "\n\n".join(out)


def langswitch(lang, inline):
    """Absolute links, because the two pages sit at different depths. The inline
    build is a single self-contained file with nowhere to switch to."""
    if inline:
        return ""
    out = []
    for code, cfg in LANGS.items():
        on = ' class="is-on" aria-current="true"' if code == lang else ""
        out.append(f'<a href="{cfg["href"]}"{on}>{code.upper()}</a>')
    return f'    <nav class="langs" aria-label="Language">{"".join(out)}</nav>\n'


def alternates(inline):
    if inline:
        return ""
    return "".join(
        f'  <link rel="alternate" hreflang="{code}" href="{cfg["href"]}" />\n'
        for code, cfg in LANGS.items()
    )


def render(content, lang="ko", inline=False):
    cfg = LANGS[lang]
    css = (ROOT / "style.css").read_text()
    scroll_js = (ROOT / "scroll.js").read_text()

    # Emitted ahead of the scene so the merge is in place before SCENES is built.
    step_text = (
        "  <script>window.__pediaStepText = "
        + json.dumps(cfg["steps"], ensure_ascii=False)
        + ";</script>\n"
    )

    if inline:
        head_assets = f"<style>\n{bundle.font_css()}\n{css}\n</style>"
        typeface = bundle.read(bundle.VENDOR / "helvetiker_regular.typeface.json")
        scene = bundle.patch_script((ROOT / "script.js").read_text())
        tail = (
            f"{step_text}"
            f'<script type="module">\nconst __HELVETIKER = {typeface};\n'
            f"{bundle.bundle_three()}\n{scene}\n</script>\n"
            f"<script>\n{scroll_js}\n</script>"
        )
    else:
        head_assets = (
            WEBFONTS + '  <link rel="stylesheet" href="/style.css" />\n' + IMPORTMAP
        )
        # scroll.js first and deferred: the rail and the section spy come alive
        # while three.js is still downloading, and it no-ops until the stage
        # announces itself.
        tail = (
            f"{step_text}"
            '  <script defer src="/scroll.js"></script>\n'
            '  <script type="module" src="/script.js"></script>'
        )

    # The inline build owns its own scroller — the Artifact host frame sizes
    # itself to content height, and a seven-viewport spacer would push scrolling
    # up to the parent where getBoundingClientRect never changes.
    open_doc = '<div class="doc">' if inline else ""
    close_doc = "</div>" if inline else ""

    return f"""<!doctype html>
<html lang="{cfg["html"]}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{cfg["title"]}</title>
  <meta name="description" content="{cfg["desc"]}" />
{alternates(inline)}{head_assets}
</head>

<body{' class="is-inline"' if inline else ""}>
  <canvas class="webgl"></canvas>

{rail(content, cfg)}
{open_doc}
  <header class="topbar">
    <a href="#hero" class="logo">
      <svg class="logo__icon" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
        <polygon points="0,0 32,16 0,32" />
      </svg>
      <span class="logo__text">PIDIA</span>
    </a>
{langswitch(lang, inline)}  </header>

  <main id="main">
{sections(content)}
  </main>

  <footer class="footer">
{content.FOOTER}
  </footer>
{close_doc}
{content.PAGE_SCRIPTS}
{tail}
</body>
</html>
"""
