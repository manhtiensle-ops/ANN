#!/usr/bin/env python3
"""Shared White-Ocean-Yellow IEEE Slide Engine, CSS Theme & Standard IEEE SVG Symbols."""
from __future__ import annotations

import html
from dataclasses import dataclass

WEEK_NAV = [
    ("index", "index.html", "Trọn Bộ 4 Tuần"),
    ("w1", "week1_slides.html", "Tuần 1: Lý Thuyết"),
    ("w2", "week2_slides.html", "Tuần 2: Python & Sizing"),
    ("w3", "week3_slides.html", "Tuần 3: Xschem & SPICE"),
    ("w4", "week4_slides.html", "Tuần 4: Layout & PEX"),
]


@dataclass
class SlideSpec:
    act_tag: str
    title: str
    badge: str
    badge_tone: str  # "ocean" | "gold" | "blue"
    body_html: str
    next_question: str
    footer_text: str
    speaker_notes: str
    is_cover: bool = False
    is_act_divider: bool = False
    section_id: str = ""


def badge_cls(tone: str) -> str:
    return {
        "ocean": "badge-ocean",
        "gold": "badge-gold",
        "blue": "badge-blue",
    }.get(tone, "badge-ocean")


# ---------------------------------------------------------------------------
# Standard IEEE / ANSI Inline SVG Component Builders (Crisp White/Blue/Gold)
# ---------------------------------------------------------------------------
def svg_defs() -> str:
    return """
    <defs>
      <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
      </marker>
      <marker id="arr-gold" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#D97706" />
      </marker>
      <marker id="arr-navy" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#0C4A6E" />
      </marker>
    </defs>
    """


def svg_not(cx: float, cy: float, scale: float = 1.0, label: str = "NOT", name: str = "") -> str:
    """Standard IEEE NOT (Inverter) gate centered at (cx, cy). Input at cx-28*s, Output at cx+28*s."""
    s = scale
    x0, x1, xr = cx - 22 * s, cx + 10 * s, cx + 22 * s
    y0, y1 = cy - 16 * s, cy + 16 * s
    br = 4.8 * s
    bx = x1 + br
    name_txt = f'<text x="{cx}" y="{y0 - 5*s}" text-anchor="middle" font-size="{10*s:.1f}" font-weight="700" fill="#0369A1">{html.escape(name)}</text>' if name else ""
    lbl_txt = f'<text x="{cx - 9*s}" y="{cy + 3.5*s}" text-anchor="middle" font-size="{9.5*s:.1f}" font-weight="800" fill="#0C4A6E">{html.escape(label)}</text>' if label else ""
    return f"""
    <g>
      <line x1="{cx - 32*s}" y1="{cy}" x2="{x0}" y2="{cy}" stroke="#0284C7" stroke-width="2" />
      <polygon points="{x0},{y0} {x0},{y1} {x1},{cy}" fill="#FFFFFF" stroke="#0369A1" stroke-width="2.1" />
      <circle cx="{bx}" cy="{cy}" r="{br}" fill="#FFFBEB" stroke="#0369A1" stroke-width="2" />
      <line x1="{bx + br}" y1="{cy}" x2="{xr + 10*s}" y2="{cy}" stroke="#0284C7" stroke-width="2" />
      {lbl_txt}{name_txt}
    </g>
    """


def svg_nand2(cx: float, cy: float, scale: float = 1.0, label: str = "NAND2", name: str = "") -> str:
    """Standard IEEE NAND2 D-body + output bubble centered at (cx, cy). Inputs at y=cy-/+11*s."""
    s = scale
    xl = cx - 26 * s
    xm = cx - 2 * s
    r = 20 * s
    xr = xm + r
    br = 4.8 * s
    bx = xr + br
    name_txt = f'<text x="{cx}" y="{cy - r - 6*s}" text-anchor="middle" font-size="{10.5*s:.1f}" font-weight="800" fill="#0369A1">{html.escape(name)}</text>' if name else ""
    lbl_txt = f'<text x="{cx - 5*s}" y="{cy + 3.5*s}" text-anchor="middle" font-size="{9.5*s:.1f}" font-weight="800" fill="#0C4A6E">{html.escape(label)}</text>' if label else ""
    return f"""
    <g>
      <line x1="{xl - 12*s}" y1="{cy - 10*s}" x2="{xl}" y2="{cy - 10*s}" stroke="#0284C7" stroke-width="2" />
      <line x1="{xl - 12*s}" y1="{cy + 10*s}" x2="{xl}" y2="{cy + 10*s}" stroke="#0284C7" stroke-width="2" />
      <path d="M {xl} {cy - r} L {xm} {cy - r} A {r} {r} 0 0 1 {xm} {cy + r} L {xl} {cy + r} Z" fill="#F0F9FF" stroke="#0369A1" stroke-width="2.2" />
      <circle cx="{bx}" cy="{cy}" r="{br}" fill="#FFFBEB" stroke="#0369A1" stroke-width="2" />
      <line x1="{bx + br}" y1="{cy}" x2="{bx + br + 12*s}" y2="{cy}" stroke="#0284C7" stroke-width="2" />
      {lbl_txt}{name_txt}
    </g>
    """


def svg_and2(cx: float, cy: float, scale: float = 1.0, label: str = "AND2", name: str = "") -> str:
    """Standard IEEE AND2 D-body (no bubble)."""
    s = scale
    xl = cx - 26 * s
    xm = cx - 2 * s
    r = 20 * s
    xr = xm + r
    name_txt = f'<text x="{cx}" y="{cy - r - 6*s}" text-anchor="middle" font-size="{10.5*s:.1f}" font-weight="800" fill="#0369A1">{html.escape(name)}</text>' if name else ""
    lbl_txt = f'<text x="{cx - 5*s}" y="{cy + 3.5*s}" text-anchor="middle" font-size="{9.5*s:.1f}" font-weight="800" fill="#0C4A6E">{html.escape(label)}</text>' if label else ""
    return f"""
    <g>
      <line x1="{xl - 12*s}" y1="{cy - 10*s}" x2="{xl}" y2="{cy - 10*s}" stroke="#0284C7" stroke-width="2" />
      <line x1="{xl - 12*s}" y1="{cy + 10*s}" x2="{xl}" y2="{cy + 10*s}" stroke="#0284C7" stroke-width="2" />
      <path d="M {xl} {cy - r} L {xm} {cy - r} A {r} {r} 0 0 1 {xm} {cy + r} L {xl} {cy + r} Z" fill="#FFFBEB" stroke="#D97706" stroke-width="2.2" />
      <line x1="{xr}" y1="{cy}" x2="{xr + 16*s}" y2="{cy}" stroke="#0284C7" stroke-width="2" />
      {lbl_txt}{name_txt}
    </g>
    """


def svg_tg(cx: float, cy: float, scale: float = 1.0, title: str = "TG1", sub: str = "") -> str:
    """Standard IEEE CMOS Transmission Gate bow-tie symbol with top PMOS bubble and bottom NMOS gate."""
    s = scale
    w, h = 26 * s, 16 * s
    t_lbl = f'<text x="{cx}" y="{cy - h - 22*s}" text-anchor="middle" font-size="{11.5*s:.1f}" font-weight="800" fill="#0369A1">{html.escape(title)}</text>' if title else ""
    s_lbl = f'<text x="{cx}" y="{cy + h + 24*s}" text-anchor="middle" font-size="{10*s:.1f}" font-weight="700" fill="#B45309">{html.escape(sub)}</text>' if sub else ""
    return f"""
    <g>
      <polygon points="{cx - w},{cy - h} {cx - w},{cy + h} {cx},{cy}" fill="#E0F2FE" stroke="#0369A1" stroke-width="2" />
      <polygon points="{cx + w},{cy - h} {cx + w},{cy + h} {cx},{cy}" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
      <line x1="{cx - 12*s}" y1="{cy - 11*s}" x2="{cx + 12*s}" y2="{cy - 11*s}" stroke="#D97706" stroke-width="2" />
      <circle cx="{cx}" cy="{cy - 16*s}" r="{4.5*s}" fill="#FFFBEB" stroke="#D97706" stroke-width="1.8" />
      <line x1="{cx}" y1="{cy - 20.5*s}" x2="{cx}" y2="{cy - 30*s}" stroke="#D97706" stroke-width="1.8" />
      <line x1="{cx - 12*s}" y1="{cy + 11*s}" x2="{cx + 12*s}" y2="{cy + 11*s}" stroke="#0369A1" stroke-width="2" />
      <line x1="{cx}" y1="{cy + 11*s}" x2="{cx}" y2="{cy + 30*s}" stroke="#0369A1" stroke-width="1.8" />
      {t_lbl}{s_lbl}
    </g>
    """


def svg_nmos(cx: float, cy: float, flip: bool = False, name: str = "M1", size_txt: str = "") -> str:
    """Standard IEEE NMOS symbol centered at (cx, cy). D=(cx, cy-26), S=(cx, cy+26), G=(cx-/+26, cy)."""
    d = -1 if flip else 1
    gx = cx - 24 * d
    gp = cx - 10 * d
    ch = cx - 4 * d
    dx = cx + 8 * d
    nt = f'<text x="{cx + 14*d}" y="{cy - 10}" text-anchor="{"end" if flip else "start"}" font-size="11.5" font-weight="800" fill="#0369A1">{html.escape(name)}</text>'
    st = f'<text x="{cx + 14*d}" y="{cy + 6}" text-anchor="{"end" if flip else "start"}" font-size="9.5" font-weight="600" fill="#475569">{html.escape(size_txt)}</text>' if size_txt else ""
    arr = f'<polygon points="{ch},{cy+12} {ch+6*d},{cy+9} {ch+6*d},{cy+15}" fill="#0369A1" />' if not flip else f'<polygon points="{ch},{cy+12} {ch+6*d},{cy+9} {ch+6*d},{cy+15}" fill="#0369A1" />'
    return f"""
    <g>
      <line x1="{gx}" y1="{cy}" x2="{gp}" y2="{cy}" stroke="#0284C7" stroke-width="2" />
      <line x1="{gp}" y1="{cy - 14}" x2="{gp}" y2="{cy + 14}" stroke="#0369A1" stroke-width="2.4" />
      <line x1="{ch}" y1="{cy - 16}" x2="{ch}" y2="{cy - 7}" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy - 4}" x2="{ch}" y2="{cy + 4}" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy + 7}" x2="{ch}" y2="{cy + 16}" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy - 12}" x2="{dx}" y2="{cy - 12}" stroke="#0C4A6E" stroke-width="2" />
      <line x1="{dx}" y1="{cy - 26}" x2="{dx}" y2="{cy - 12}" stroke="#0C4A6E" stroke-width="2" />
      <line x1="{ch}" y1="{cy + 12}" x2="{dx}" y2="{cy + 12}" stroke="#0C4A6E" stroke-width="2" />
      <line x1="{dx}" y1="{cy + 12}" x2="{dx}" y2="{cy + 26}" stroke="#0C4A6E" stroke-width="2" />
      <line x1="{ch}" y1="{cy}" x2="{dx}" y2="{cy}" stroke="#0284C7" stroke-width="1.4" />
      {arr}{nt}{st}
    </g>
    """


def svg_pmos(cx: float, cy: float, flip: bool = False, name: str = "M3", size_txt: str = "") -> str:
    """Standard IEEE PMOS symbol with gate inversion bubble centered at (cx, cy). S=(cx+8*d, cy-26), D=(cx+8*d, cy+26)."""
    d = -1 if flip else 1
    gx = cx - 26 * d
    bx = cx - 15 * d
    gp = cx - 10 * d
    ch = cx - 4 * d
    dx = cx + 8 * d
    nt = f'<text x="{cx + 14*d}" y="{cy - 10}" text-anchor="{"end" if flip else "start"}" font-size="11.5" font-weight="800" fill="#B45309">{html.escape(name)}</text>'
    st = f'<text x="{cx + 14*d}" y="{cy + 6}" text-anchor="{"end" if flip else "start"}" font-size="9.5" font-weight="600" fill="#78350F">{html.escape(size_txt)}</text>' if size_txt else ""
    return f"""
    <g>
      <line x1="{gx}" y1="{cy}" x2="{bx - 4*d}" y2="{cy}" stroke="#D97706" stroke-width="2" />
      <circle cx="{bx}" cy="{cy}" r="4.2" fill="#FFFBEB" stroke="#D97706" stroke-width="2" />
      <line x1="{gp}" y1="{cy - 14}" x2="{gp}" y2="{cy + 14}" stroke="#B45309" stroke-width="2.4" />
      <line x1="{ch}" y1="{cy - 16}" x2="{ch}" y2="{cy - 7}" stroke="#78350F" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy - 4}" x2="{ch}" y2="{cy + 4}" stroke="#78350F" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy + 7}" x2="{ch}" y2="{cy + 16}" stroke="#78350F" stroke-width="2.2" />
      <line x1="{ch}" y1="{cy - 12}" x2="{dx}" y2="{cy - 12}" stroke="#78350F" stroke-width="2" />
      <line x1="{dx}" y1="{cy - 26}" x2="{dx}" y2="{cy - 12}" stroke="#78350F" stroke-width="2" />
      <line x1="{ch}" y1="{cy + 12}" x2="{dx}" y2="{cy + 12}" stroke="#78350F" stroke-width="2" />
      <line x1="{dx}" y1="{cy + 12}" x2="{dx}" y2="{cy + 26}" stroke="#78350F" stroke-width="2" />
      <line x1="{ch}" y1="{cy}" x2="{dx}" y2="{cy}" stroke="#D97706" stroke-width="1.4" />
      <polygon points="{dx},{cy-12} {dx-6*d},{cy-15} {dx-6*d},{cy-9}" fill="#D97706" />
      {nt}{st}
    </g>
    """


# ---------------------------------------------------------------------------
# HTML Deck Renderer (White - Ocean Blue - Amber Gold)
# ---------------------------------------------------------------------------
COMMON_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');
:root {
  --ink: #0C4A6E;
  --ink-dark: #082F49;
  --ocean: #0284C7;
  --ocean-deep: #0369A1;
  --ocean-soft: #E0F2FE;
  --sky-bg: #F7FBFF;
  --gold: #D97706;
  --gold-bright: #F59E0B;
  --gold-soft: #FEF3C7;
  --gold-pale: #FFFBEB;
  --white: #FFFFFF;
  --border-blue: #BAE6FD;
  --border-gold: #FDE68A;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: linear-gradient(135deg, #DBEAFE 0%, #F0F9FF 50%, #FEF3C7 100%);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  color: var(--ink-dark);
  overflow: hidden;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
}
.mono { font-family: 'JetBrains Mono', monospace; }
.katex, .code-tag, .code-tag-gold, .normal-case { text-transform: none !important; }
.code-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85em;
  font-weight: 600;
  background: #E0F2FE;
  color: #0369A1;
  border: 1px solid #BAE6FD;
  padding: 1px 6px;
  border-radius: 5px;
}
.code-tag-gold {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85em;
  font-weight: 600;
  background: #FEF3C7;
  color: #B45309;
  border: 1px solid #FDE68A;
  padding: 1px 6px;
  border-radius: 5px;
}
#deck {
  width: 1280px;
  height: 720px;
  position: relative;
  transform-origin: center center;
}
.slide {
  width: 1280px;
  height: 720px;
  position: absolute;
  top: 0;
  left: 0;
  display: none;
  flex-direction: column;
  justify-content: space-between;
  padding: 22px 44px 36px 44px;
  background: var(--sky-bg);
  border-top: 5px solid #0284C7;
  border-bottom: 3px solid #F59E0B;
  overflow: hidden;
  box-shadow: 0 22px 55px rgba(3, 105, 161, 0.16);
}
.slide::before {
  content: "";
  position: absolute;
  top: -80px;
  right: -80px;
  width: 260px;
  height: 260px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(245, 158, 11, 0.10) 0%, rgba(245, 158, 11, 0) 70%);
  pointer-events: none;
}
.slide.active { display: flex; }
.slide-cover {
  background: linear-gradient(135deg, #FFFFFF 0%, #E0F2FE 56%, #FEF3C7 100%);
  color: #082F49;
  border-top: 7px solid #0369A1;
  border-bottom: 5px solid #F59E0B;
}
.slide-cover::after {
  content: "";
  position: absolute;
  bottom: -110px;
  left: -90px;
  width: 340px;
  height: 340px;
  border-radius: 999px;
  background: radial-gradient(circle, rgba(2, 132, 199, 0.10) 0%, rgba(2, 132, 199, 0) 70%);
  pointer-events: none;
}
.ieee-card {
  background: #FFFFFF;
  border: 1px solid #BAE6FD;
  border-radius: 13px;
  padding: 14px 18px;
  box-shadow: 0 3px 10px rgba(2, 132, 199, 0.06);
}
.gold-card {
  background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
  border: 1.5px solid #F59E0B;
  border-radius: 13px;
  padding: 14px 18px;
  color: #082F49;
  box-shadow: 0 3px 10px rgba(217, 119, 6, 0.08);
}
.ocean-card {
  background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
  border: 1.5px solid #0284C7;
  border-radius: 13px;
  padding: 14px 18px;
  color: #082F49;
  box-shadow: 0 3px 10px rgba(2, 132, 199, 0.08);
}
.fig-frame {
  background: #FFFFFF;
  border: 1.5px solid #BAE6FD;
  border-radius: 14px;
  padding: 8px 12px;
  box-shadow: 0 4px 14px rgba(3, 105, 161, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.badge-ocean {
  background: #E0F2FE;
  color: #0369A1;
  border: 1px solid #7DD3FC;
  padding: 2px 11px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 11.5px;
  white-space: nowrap;
}
.badge-gold {
  background: #FEF3C7;
  color: #B45309;
  border: 1px solid #FCD34D;
  padding: 2px 11px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 11.5px;
  white-space: nowrap;
}
.badge-blue {
  background: #DBEAFE;
  color: #1D4ED8;
  border: 1px solid #93C5FD;
  padding: 2px 11px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 11.5px;
  white-space: nowrap;
}
.ieee-table { width: 100%; border-collapse: collapse; }
.ieee-table thead tr {
  background: linear-gradient(90deg, #0369A1 0%, #0284C7 100%);
  color: #FFFFFF;
  border-bottom: 2.5px solid #F59E0B;
}
.ieee-table tbody tr:nth-child(even) { background: #F0F9FF; }
.ieee-table tbody tr:nth-child(odd) { background: #FFFFFF; }
.ieee-table tbody tr.row-gold { background: #FFFBEB; }
.transition-hook {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(90deg, #FFFBEB 0%, #EFF6FF 100%);
  border: 1px solid #FDE68A;
  border-left: 5px solid #F59E0B;
  border-radius: 9px;
  padding: 6px 14px;
  font-size: 12.2px;
  color: #0C4A6E;
  font-weight: 500;
}
.katex { font-size: 0.99em !important; }
.progress-track {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: rgba(2, 132, 199, 0.14);
  z-index: 40;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #0284C7, #38BDF8, #F59E0B);
  transition: width 0.25s ease;
}
#notes-panel {
  position: fixed;
  left: 22px;
  bottom: 48px;
  max-width: 790px;
  background: #FFFFFF;
  color: #082F49;
  border: 2px solid #0284C7;
  border-top: 5px solid #F59E0B;
  border-radius: 13px;
  padding: 13px 18px;
  font-size: 13px;
  line-height: 1.52;
  box-shadow: 0 14px 36px rgba(3, 105, 161, 0.20);
  z-index: 55;
  display: none;
}
#notes-panel.open { display: block; }
.hud-pill {
  background: rgba(255, 255, 255, 0.96);
  border: 1.5px solid #7DD3FC;
  color: #0369A1;
  box-shadow: 0 4px 16px rgba(2, 132, 199, 0.14);
}
.nav-link {
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 10.5px;
  font-weight: 700;
  color: #0369A1;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.15s ease;
}
.nav-link:hover { background: #E0F2FE; }
.nav-link.current {
  background: linear-gradient(90deg, #0284C7, #0369A1);
  color: #FFFFFF;
  box-shadow: 0 1px 4px rgba(2, 132, 199, 0.35);
}
@media print {
  @page { size: 1280px 720px; margin: 0; }
  body {
    background: #FFFFFF;
    overflow: visible;
    height: auto;
    width: auto;
    display: block;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  #deck { transform: none !important; width: 1280px; height: auto; }
  .slide {
    position: relative !important;
    display: flex !important;
    page-break-after: always;
    break-after: page;
    box-shadow: none !important;
  }
  .nav-controls, .week-switcher, .progress-track, #notes-panel { display: none !important; }
}
"""


def render_slide_html(s: SlideSpec, idx_1: int, total: int) -> str:
    notes_attr = html.escape(s.speaker_notes, quote=True)
    sec_attr = f' id="{html.escape(s.section_id or f"s{idx_1}")}"'
    active_cls = " active" if idx_1 == 1 else ""
    if s.is_cover:
        return f"""
  <section class="slide slide-cover{active_cls}"{sec_attr} data-notes="{notes_attr}">
    {s.body_html}
    <div class="space-y-1.5 relative z-10">
      <div class="transition-hook">
        <span class="mono text-amber-700 font-bold text-xs uppercase shrink-0">Câu hỏi dẫn nhập →</span>
        <span>{s.next_question}</span>
      </div>
      <div class="text-center text-[11px] text-sky-900/75 font-medium pt-0.5">
        {s.footer_text} • <span class="mono font-bold">Slide {idx_1:02d} / {total:02d}</span>
      </div>
    </div>
  </section>
"""
    hook_html = ""
    if s.next_question:
        hook_html = f"""
      <div class="transition-hook">
        <span class="mono text-amber-700 font-bold text-xs uppercase shrink-0">Câu hỏi tiếp theo →</span>
        <span>{s.next_question}</span>
      </div>"""
    return f"""
  <section class="slide{active_cls}"{sec_attr} data-notes="{notes_attr}">
    <div class="flex items-center justify-between border-b-2 border-sky-200 pb-2 shrink-0">
      <div>
        <span class="text-[11.5px] font-bold uppercase tracking-wider text-sky-700 mono">{s.act_tag}</span>
        <h2 class="text-[22px] font-extrabold text-sky-950 leading-snug">{s.title}</h2>
      </div>
      <span class="{badge_cls(s.badge_tone)}">{s.badge}</span>
    </div>

    <div class="flex-1 min-h-0 flex flex-col justify-center gap-2.5 py-1.5">
      {s.body_html}
    </div>

    <div class="space-y-1.5 shrink-0">
      {hook_html}
      <div class="text-center text-[11px] text-sky-900/70 border-t border-sky-200/80 pt-1">
        {s.footer_text} • <span class="mono font-bold text-sky-900">Slide {idx_1:02d} / {total:02d}</span>
      </div>
    </div>
  </section>
"""


def build_deck_html(
    page_title: str,
    active_key: str,
    slides: list[SlideSpec],
    extra_chapter_bar: str = "",
) -> str:
    total = len(slides)
    slides_markup = "\n".join(render_slide_html(s, i + 1, total) for i, s in enumerate(slides))

    nav_links = []
    for k, href, label in WEEK_NAV:
        cls = "nav-link current" if k == active_key else "nav-link"
        nav_links.append(f'<a href="{href}" class="{cls}">{label}</a>')
    nav_strip = "\n  ".join(nav_links)

    pct = (1.0 / max(total, 1)) * 100.0
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(page_title)}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css" />
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
  <style>{COMMON_CSS}</style>
</head>
<body>

<div id="deck">
{slides_markup}
</div>

<!-- Speaker Notes Drawer (Press N) -->
<div id="notes-panel">
  <div class="flex items-center justify-between border-b border-sky-200 pb-1.5 mb-2">
    <span class="text-xs font-bold uppercase tracking-wider text-sky-700 mono">Kịch bản Dẫn dắt Thuyết trình (Phím N)</span>
    <button onclick="toggleNotes()" class="text-amber-700 hover:text-sky-800 text-xs font-bold mono">[Đóng]</button>
  </div>
  <div id="notes-text"></div>
</div>

<!-- Bottom-Left Week Switcher -->
<div class="week-switcher hud-pill fixed bottom-2 left-4 flex items-center gap-1 px-2 py-1 rounded-full z-50">
  {nav_strip}
  {extra_chapter_bar}
</div>

<!-- Bottom-Right Navigation HUD -->
<div class="nav-controls hud-pill fixed bottom-2 right-4 flex items-center gap-2 px-3 py-1 rounded-full text-xs mono z-50">
  <button onclick="toggleNotes()" class="px-2 py-0.5 hover:text-amber-600 font-bold border-r border-sky-200 pr-2.5" title="Speaker Notes (N)">Notes (N)</button>
  <button onclick="go(-1)" class="px-1.5 py-0.5 hover:text-amber-600 font-bold" title="Slide Trước (←)">◀</button>
  <span id="counter" class="font-bold text-sky-900">01 / {total:02d}</span>
  <button onclick="go(1)" class="px-1.5 py-0.5 hover:text-amber-600 font-bold" title="Slide Tiếp (→)">▶</button>
</div>

<!-- Progress Bar -->
<div class="progress-track">
  <div id="progress-fill" class="progress-fill" style="width: {pct:.2f}%;"></div>
</div>

<script>
  const slides = Array.from(document.querySelectorAll('.slide'));
  const deck = document.getElementById('deck');
  const counter = document.getElementById('counter');
  const progressFill = document.getElementById('progress-fill');
  const notesPanel = document.getElementById('notes-panel');
  const notesText = document.getElementById('notes-text');
  let idx = 0;

  function show(i) {{
    idx = (i + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('active', k === idx));
    counter.textContent = String(idx + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
    progressFill.style.width = (((idx + 1) / slides.length) * 100).toFixed(2) + '%';
    notesText.textContent = slides[idx].dataset.notes || '';
  }}
  function go(d) {{ show(idx + d); }}
  function jumpToId(id) {{
    const pos = slides.findIndex((s) => s.id === id);
    if (pos >= 0) show(pos);
  }}
  function toggleNotes() {{ notesPanel.classList.toggle('open'); }}
  function fit() {{
    const scale = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    deck.style.transform = `scale(${{scale}})`;
  }}
  window.addEventListener('resize', fit);
  window.addEventListener('keydown', (e) => {{
    if (['ArrowRight', 'PageDown', ' '].includes(e.key)) {{ e.preventDefault(); go(1); }}
    if (['ArrowLeft', 'PageUp'].includes(e.key)) {{ e.preventDefault(); go(-1); }}
    if (e.key === 'Home') show(0);
    if (e.key === 'End') show(slides.length - 1);
    if (e.key.toLowerCase() === 'n') toggleNotes();
  }});
  if (window.location.hash) {{
    const target = window.location.hash.slice(1);
    const pos = slides.findIndex((s) => s.id === target);
    if (pos >= 0) {{
      idx = pos;
    }} else {{
      const m = target.match(/^s(\\d+)$/);
      if (m) {{
        const n = parseInt(m[1], 10) - 1;
        if (n >= 0 && n < slides.length) idx = n;
      }}
    }}
  }}
  show(idx);
  fit();
</script>
</body>
</html>
"""
