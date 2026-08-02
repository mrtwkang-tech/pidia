#!/usr/bin/env python3
"""Write every output.

  index.html          the Korean page Vercel serves at /
  en/index.html       the English page, at /en/
  _deploy/pedia.html  the self-contained page an Artifact can host (Korean)

The two language modules are checked against each other before anything is
written. They are separate files so each reads as prose rather than as a table
of string keys, and the cost of that choice is drift — so the drift is caught
here instead of being discovered on the page.
"""

import pathlib
import sys

import content
import content_en
import render

ROOT = pathlib.Path(__file__).resolve().parent.parent


def check_parity():
    """Same sections, same order, same anchors — or stop."""
    ko = [(s["id"], s["cls"]) for s in content.SECTIONS]
    en = [(s["id"], s["cls"]) for s in content_en.SECTIONS]
    if ko != en:
        only_ko = [i for i, _ in ko if i not in {j for j, _ in en}]
        only_en = [i for i, _ in en if i not in {j for j, _ in ko}]
        raise SystemExit(
            "content.py and content_en.py disagree on sections.\n"
            f"  ko only: {only_ko or '—'}\n"
            f"  en only: {only_en or '—'}\n"
            f"  ko: {[i for i, _ in ko]}\n"
            f"  en: {[i for i, _ in en]}"
        )
    for s in content_en.SECTIONS:
        if not s["label"].strip():
            raise SystemExit(f"en section {s['id']} has no rail label")


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    print(f"{str(path.relative_to(ROOT)):<22}{len(text) / 1024:7.0f} KB")


def main():
    check_parity()

    write(ROOT / "index.html", render.render(content, "ko"))
    write(ROOT / "en" / "index.html", render.render(content_en, "en"))

    if "--static" in sys.argv:
        return

    write(ROOT / "_deploy" / "pedia.html", render.render(content, "ko", inline=True))


if __name__ == "__main__":
    main()
