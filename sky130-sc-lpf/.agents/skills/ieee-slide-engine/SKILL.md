---
name: ieee-slide-engine
description: >-
  Use this skill whenever generating weekly progress presentations or final
  defense slides (/slide [1-4] [html|gamma|pptx]) or 300-DPI conference plots
  for sky130-sc-lpf. Enforces the IEEE/ISSCC Modern design system, strict word
  budgets, KaTeX math rendering, 16:9 keyboard/PDF HTML engine, and anti-overlap
  plot standards.
---

# Anti-Ugly IEEE/ISSCC Slide & Figure Engine

Activate this skill on every `/slide [1-4] [html|gamma|pptx]` command and whenever generating figures intended for slides.

## 1. IEEE Modern Color System (Strict)
- **Cover / Section Divider Slide:**
  - Background: `#0F172A` (Deep Navy)
  - Primary Accent: `#38BDF8` (Sky Cyan)
  - Body / Subtitle Text: `#F8FAFC` / `#94A3B8`
- **Content Slides:**
  - Canvas Background: `#F8FAFC` (Ice Slate)
  - Card Surface: `#FFFFFF` with `1px solid #E2E8F0` border & subtle shadow
  - Primary Technical Accent: `#2563EB` (Cobalt Blue)
  - Verification PASS / Spec Met: `#0D9488` (Teal)
  - Engineering Trade-off / Warning: `#D97706` (Amber)
  - Critical Error / Parasitic Limit: `#DC2626` (Crimson)
  - Primary Text: `#0F172A` | Muted Text: `#475569`

---

## 2. Anti-Clutter Visual Discipline (Zero Exceptions)
1. **Word Budget:** Maximum **45–60 words per slide** (excluding equations, axis labels, and table numbers).
2. **Bullet Discipline:** Maximum **14 words per bullet**; maximum 3–4 bullets per card.
3. **Whitespace:** Maintain **$\ge 30\%$ open whitespace** on every slide. Never overflow the `1280x720` (16:9) viewport (`overflow: hidden` on slide frame, verified so zero content clips!).
4. **Layout Alternation Rule:** Never repeat the same layout on two consecutive slides. Rotate among:
   - **Layout A — Bento KPI Grid:** 3–4 metric cards with giant numbers + physical takeaway.
   - **Layout B — Split Comparison (50/50):** e.g., On-chip Resistor vs. Switched-Cap Ratio; Ideal $RC$ vs. Discrete $H(z)$.
   - **Layout C — 4-Block Signal Flow SVG:** Clean inline vector block/circuit diagram (`non_overlap_clk` $\rightarrow$ `tg_switch` $\rightarrow$ `sc_core` $\rightarrow$ `ota_5t`).
   - **Layout D — Spec / Verification Gate Table:** Compact IEEE table with Pass/Fail Teal/Amber badges + KaTeX formulas.
   - **Layout E — 300-DPI Figure + 3 Core Insights:** Left 62% high-res chart/SVG, right 38% three numbered physical insights.

---

## 3. Output Format Specifications

### Mode 1: `html` (Default Recommended — Standalone 16:9 Conference Deck)
Save to `slides/week<N>_slides.html`. Must include:
- **Viewport & Scaling:** Fixed virtual canvas `1280px × 720px` (`aspect-ratio: 16/9`) auto-scaled via CSS transform/flex to fit any screen (`F11` fullscreen) without scrolling.
- **Typography & Math:** Inter / IBM Plex Sans + JetBrains Mono + **KaTeX** (`katex.min.css` + `katex.min.js` + `auto-render.min.js`) for razor-sharp LaTeX formulas.
- **Interactive Controls:** Left/Right arrow keys, Spacebar, slide counter (`03 / 10`), progress bar at bottom, and speaker-note toggle (`N`).
- **Pixel-Perfect Print-to-PDF (`Ctrl + P`):**
  ```css
  @media print {
    @page { size: 1280px 720px; margin: 0; }
    body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .slide { page-break-after: always; break-after: page; display: flex !important; transform: none !important; }
    .nav-controls { display: none !important; }
  }
  ```

### Mode 2: `gamma` (Structured Gamma.app Blueprint)
Save to `slides/week<N>_gamma.md` with `---` card separators, explicit layout directives (`[Layout: 2-Column Split]`, `[Layout: 4-Card Bento]`), LaTeX blocks, and figure embed paths.

### Mode 3: `pptx` (Programmatic PowerPoint)
Check `python3 -c "import pptx"` first; if unavailable in offline container, generate an HTML-to-PDF-ready deck plus self-contained `slides/build_week<N>_pptx.py` script and notify the user clearly.

---

## 4. 300-DPI Plot Standard
Import [ieee_plot_style.py](./resources/ieee_plot_style.py) in all Python plotting scripts:
- `dpi=300`, `bbox_inches="tight"`, `facecolor="#FFFFFF"`.
- Place legends/annotations with explicit offset boxes so curves, titles, and callouts **never collide**. Visually inspect generated `.png` files with `read_file` before finalizing!
