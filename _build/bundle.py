#!/usr/bin/env python3
"""Asset bundling for the inline (Artifact) build.

Moved verbatim out of the retired gen_deploy.py. Two jobs:

  bundle_three()  flattens the three.js ES module graph into inline script.
                  three.core.min.js and three.module.min.js are minified
                  separately and both use short local names, so concatenating
                  them into one scope collides. Each is wrapped in its own IIFE:
                  the import becomes a destructure from the previous IIFE's
                  return value, the export block becomes that return value.

  font_css()      inlines the three subset woff2 faces as data URIs.

patch_script() is format-only. The behaviour patches it used to carry now live
in script.js itself.
"""

import base64
import pathlib
import re

VENDOR = pathlib.Path(
    "/private/tmp/claude-501/-Users-taewookang------/"
    "948d7c34-7b28-4aff-ab82-088267f60a81/scratchpad/vendor"
)


def read(p):
    return pathlib.Path(p).read_text()


def _brace_end(src, open_idx):
    """Index of the brace closing the one at open_idx."""
    depth = 0
    i = open_idx
    while i < len(src):
        if src[i] == "{":
            depth += 1
        elif src[i] == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("unbalanced brace")


def _split_specifiers(body):
    """`A as b, C` -> [("A", "b"), ("C", "C")] in (left, right) order."""
    out = []
    for item in body.split(","):
        item = item.strip()
        if not item:
            continue
        if " as " in item:
            left, right = [x.strip() for x in item.split(" as ")]
        else:
            left = right = item
        out.append((left, right))
    return out


def comment_spans(src):
    """(start, end) ranges of comments, so statement scanning can skip them.

    The addons carry `@three_import import { X } from '...'` lines inside JSDoc,
    which look exactly like real import statements to a regex.
    """
    spans = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c in "\"'`":
            quote = c
            i += 1
            while i < n:
                if src[i] == "\\":
                    i += 2
                    continue
                if src[i] == quote:
                    break
                i += 1
            i += 1
        elif c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            j = n if j == -1 else j
            spans.append((i, j))
            i = j
        elif c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            j = n if j == -1 else j + 2
            spans.append((i, j))
            i = j
        else:
            i += 1
    return spans


def strip_module_statements(src):
    """Remove every top-level import/export and classify what they declared.

    Three forms appear in the three.js builds and they mean different things:

      import{A as b}from"M"   -> b is a local alias for M's public A
      export{A,B}from"M"      -> pure forwarding; the names never become locals
                                 here, so this is dropped outright
      export{x as A}          -> local x is published as A
    """
    imports, exports = [], []
    pieces = []
    i = 0
    skip = comment_spans(src)
    in_comment = lambda pos: any(a <= pos < b for a, b in skip)
    for m in re.finditer(r"\b(import|export)\s*\{", src):
        if m.start() < i or in_comment(m.start()):
            continue
        kind = m.group(1)
        open_idx = src.index("{", m.start())
        close_idx = _brace_end(src, open_idx)
        specs = _split_specifiers(src[open_idx + 1 : close_idx])

        # consume an optional `from "..."` and the trailing semicolon
        rest = src[close_idx + 1 :]
        tail = re.match(r'\s*from\s*["\'][^"\']+["\']\s*;?|\s*;?', rest)
        end = close_idx + 1 + tail.end()
        has_from = "from" in tail.group(0)

        if kind == "import":
            # (public, localAlias)
            imports.extend(specs)
        elif not has_from:
            # (public, local) — specifiers read `local as public`
            exports.extend((pub, loc) for loc, pub in specs)
        # else: forwarding re-export, nothing to bind

        pieces.append(src[i : m.start()])
        i = end
    pieces.append(src[i:])
    out = "".join(pieces)
    # bare side-effect imports
    out = re.sub(r'^\s*import\s+["\'][^"\']+["\']\s*;?', "", out, flags=re.M)
    return out, imports, exports


def obj_literal(pairs):
    return "{" + ",".join((p if p == l else f"{p}:{l}") for p, l in pairs) + "}"


def destructure(pairs, source):
    return (
        "const{"
        + ",".join((p if p == l else f"{p}:{l}") for p, l in pairs)
        + "}="
        + source
        + ";"
    )


def bundle_three():
    core_body, core_imports, core_exports = strip_module_statements(
        read(VENDOR / "three.core.min.js")
    )
    assert not core_imports, "core should not import anything"
    assert len(core_exports) > 300, f"core exports look wrong: {len(core_exports)}"

    mod_body, mod_imports, mod_exports = strip_module_statements(
        read(VENDOR / "three.module.min.js")
    )
    assert mod_imports, "module import block not found"
    assert len(mod_exports) > 150, f"module exports look wrong: {len(mod_exports)}"
    for leftover in ("import", "export"):
        assert not re.search(
            rf"^\s*{leftover}\b|;\s*{leftover}\s*\{{", mod_body
        ), f"leftover {leftover} in module body"

    parts = [
        "const __threeCore=(()=>{",
        core_body,
        "\nreturn " + obj_literal(core_exports) + ";})();",
        "\nconst __threeMod=(()=>{",
        destructure(mod_imports, "__threeCore"),
        mod_body,
        "\nreturn " + obj_literal(mod_exports) + ";})();",
        # core first so the renderer-side definitions in the module build win
        "\nconst THREE={...__threeCore,...__threeMod};",
    ]

    # Addons: same treatment, but they import from the assembled THREE namespace
    for fname, exports in [
        ("OrbitControls.js", ["OrbitControls"]),
        ("RoomEnvironment.js", ["RoomEnvironment"]),
        ("RoundedBoxGeometry.js", ["RoundedBoxGeometry"]),
        ("FontLoader.js", ["FontLoader", "Font"]),
        ("TextGeometry.js", ["TextGeometry"]),
    ]:
        body, imports, _ = strip_module_statements(read(VENDOR / fname))
        parts += [
            f"\nconst {{{','.join(exports)}}}=(()=>{{",
            destructure(imports, "THREE") if imports else "",
            body,
            "\nreturn {" + ",".join(exports) + "};})();",
        ]
    return "\n".join(parts)


# ────────────────────────────────────────────────────────────────────── fonts


# ─────────────────────────────────────────────────────────── page assembly


def font_css():
    """The three faces style.css names, subset to the codepoints this page uses.

    All three are subsets of the same files the static build links from a CDN, so
    the two builds render the same text. Wanted Sans is the one that matters: the
    complete variable face is 4.7 MB and 568 codepoints of it is 90 KB. The
    weight range stays live rather than instanced — headings run at 600/700 and
    body at 400 off the one file.
    """
    # Noto Serif KR is deliberately absent. The complete variable face is 22 MB
    # and this build has no consumer today, so the inline page falls back to the
    # system serif for Hangul headings; Latin headings still get Newsreader.
    # Subset it here if the artifact build is ever put back into use.
    faces = [
        ("Wanted Sans Variable", "400 1000", "WantedSans-sub.woff2"),
        ("Newsreader", "200 800", "Newsreader-sub.woff2"),
        ("Roboto Mono", "100 700", "RobotoMono-sub.woff2"),
    ]
    out = []
    for family, weight, fname in faces:
        b64 = base64.b64encode((VENDOR / fname).read_bytes()).decode()
        out.append(
            "@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (family, weight, b64)
        )
    return "\n".join(out)


# ─────────────────────────────────────────────────────────── page assembly


def patch_script(src):
    """Format-only fixes for the inline build.

    The behaviour patches this used to carry — mutable MODE, ungating the kit
    inputs, installing the control hook — now live in script.js itself. They
    were only ever build-time because the Artifact was the sole consumer that
    folded eight pages into one; the site does that now too, and matching source
    text by exact string was one reformat away from breaking.
    """
    # 1. imports are satisfied by the flattened bundle
    src = re.sub(r'^import\s+.*?from\s+["\'][^"\']+["\']\s*;\s*$', "", src, flags=re.M)

    # 2. FontLoader.load() is a network fetch; parse the inlined JSON instead
    head = re.search(
        r"new FontLoader\(\)\.load\(\s*\n\s*\"https://[^\"]+\",\s*\n\s*\(font\) => \{",
        src,
    )
    assert head, "FontLoader call site not found"
    src = src[: head.start()] + "((font) => {" + src[head.end() :]
    tail = "  },\n);"
    idx = src.index(tail, head.start())
    src = (
        src[:idx] + "})(new FontLoader().parse(__HELVETIKER));" + src[idx + len(tail) :]
    )
    return src
