#!/usr/bin/env python3
"""Compile all 4 weekly HTML decks + combined master index deck and verify palette & images."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path("/headless/ANN/sky130-sc-lpf")
PYTHON_DIR = ROOT / "python"
SLIDES_DIR = ROOT / "slides"
FIGS_DIR = SLIDES_DIR / "figs"

if str(PYTHON_DIR) not in sys.path:
    sys.path.insert(0, str(PYTHON_DIR))

from slide_theme import build_deck_html  # noqa: E402
from slides_w1_w2 import get_week1_slides, get_week2_slides  # noqa: E402
from slides_w3_w4 import get_week3_slides, get_week4_slides  # noqa: E402


FORBIDDEN_DARK_TOKENS = [
    "bg-slate-900",
    "bg-slate-800",
    "bg-slate-950",
    "bg-gray-900",
    "bg-black",
    "#0F172A",
    "#1E293B",
    "#090D16",
    "#0B1120",
]


def main() -> None:
    w1 = get_week1_slides()
    w2 = get_week2_slides()
    w3 = get_week3_slides()
    w4 = get_week4_slides()
    all_slides = w1 + w2 + w3 + w4

    chapter_bar = (
        '<span class="text-sky-300 px-1">|</span>'
        '<button onclick="jumpToId(\'w1-start\')" class="nav-link" title="Nhảy tới Tuần 1">#T1</button>'
        '<button onclick="jumpToId(\'w2-start\')" class="nav-link" title="Nhảy tới Tuần 2">#T2</button>'
        '<button onclick="jumpToId(\'w3-start\')" class="nav-link" title="Nhảy tới Tuần 3">#T3</button>'
        '<button onclick="jumpToId(\'w4-start\')" class="nav-link" title="Nhảy tới Tuần 4">#T4</button>'
    )

    outputs = [
        (
            SLIDES_DIR / "week1_slides.html",
            build_deck_html("SKY130-SC-LPF — Tuần 1: Cơ Sở Lý Thuyết & Kiến Trúc", "w1", w1),
            len(w1),
        ),
        (
            SLIDES_DIR / "week2_slides.html",
            build_deck_html("SKY130-SC-LPF — Tuần 2: Mô Hình Hóa Python & Sizing", "w2", w2),
            len(w2),
        ),
        (
            SLIDES_DIR / "week3_slides.html",
            build_deck_html("SKY130-SC-LPF — Tuần 3: Schematic Xschem & Ngspice Pre-Layout", "w3", w3),
            len(w3),
        ),
        (
            SLIDES_DIR / "week4_slides.html",
            build_deck_html("SKY130-SC-LPF — Tuần 4: Layout Magic GDSII & Post-Layout PEX", "w4", w4),
            len(w4),
        ),
        (
            SLIDES_DIR / "index.html",
            build_deck_html(
                "SKY130-SC-LPF — Trọn Bộ Thuyết Trình 4 Tuần (79 Slides)",
                "index",
                all_slides,
                extra_chapter_bar=chapter_bar,
            ),
            len(all_slides),
        ),
    ]

    all_fig_files = sorted(p.name for p in FIGS_DIR.glob("*.png"))
    used_figs: set[str] = set()
    missing_srcs: list[str] = []
    dark_hits: list[str] = []

    bad_ctrl_hits: list[str] = []

    for out_path, content, count in outputs:
        out_path.write_text(content, encoding="utf-8")
        print(f"Wrote {out_path.name:18s}: {count:2d} slides ({len(content)//1024:4d} KB)")

        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", content):
            bad_ctrl_hits.append(f"{out_path.name}: unexpected control char (un-doubled \\f/\\b/\\r in string?)")
        for m in re.finditer(r"\$[^$]+\$", content):
            if re.search(r"(?<![\\])[\b\f\r\t]", m.group(0)):
                bad_ctrl_hits.append(f"{out_path.name}: tab/ctrl inside KaTeX span: {m.group(0)[:40]!r}")
        deck_m = re.search(r'<div id="deck">(.*?)</div>\s*<!-- Speaker Notes Drawer', content, re.S)
        if deck_m and "{{" in deck_m.group(1):
            bad_ctrl_hits.append(f"{out_path.name}: unescaped double-opening braces '{{{{' inside <div id='deck'>")

        low = content.lower()
        for tok in FORBIDDEN_DARK_TOKENS:
            if tok.lower() in low:
                dark_hits.append(f"{out_path.name}: forbidden token '{tok}'")

        for m in re.finditer(r'src="figs/([^"]+)"', content):
            fname = m.group(1)
            if not (FIGS_DIR / fname).is_file():
                missing_srcs.append(f"{out_path.name}: missing figs/{fname}")
            if out_path.name != "index.html":
                used_figs.add(fname)

    unused_figs = sorted(set(all_fig_files) - used_figs)
    print("\n--- STATIC VERIFICATION REPORT ---")
    print(f"Total PNGs in slides/figs/: {len(all_fig_files)}")
    print(f"Used across W1-W4 decks   : {len(used_figs)}")
    print(f"Unused PNGs               : {len(unused_figs)} -> {unused_figs}")
    print(f"Broken fig references     : {len(missing_srcs)} -> {missing_srcs}")
    print(f"Dark/black token hits     : {len(dark_hits)} -> {dark_hits}")
    print(f"Ctrl-char / LaTeX hits    : {len(bad_ctrl_hits)} -> {bad_ctrl_hits}")

    if unused_figs or missing_srcs or dark_hits or bad_ctrl_hits:
        raise SystemExit("Verification FAILED!")
    print("ALL STATIC CHECKS PASSED 100%!")


if __name__ == "__main__":
    main()
