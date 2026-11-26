#!/usr/bin/env python3
"""Slide specifications for Week 3 (20 slides) and Week 4 (19 slides) — White/Blue/Gold theme."""
from __future__ import annotations

from slide_theme import (
    SlideSpec,
    svg_and2,
    svg_defs,
    svg_nand2,
    svg_nmos,
    svg_not,
    svg_pmos,
    svg_tg,
)


def _svg_w3_寄生_rootcause() -> str:
    """Clean white/blue/gold diagram explaining Iter 1 (+22.69%) vs Iter 2 (+3.36%) parasitic Cp,V1."""
    return f"""
    <svg viewBox="0 0 640 230" class="w-full h-[215px]">
      {svg_defs()}
      <text x="320" y="16" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0369A1">
        Giải phẫu Ký sinh Nút Nhạy V1 &amp; VX Khi Ghép Toàn Mạch
      </text>

      <!-- Left: VIN -> TG1 -> V1 -> TG2 -> VX -->
      <text x="20" y="96" font-size="11" font-weight="800" fill="#0C4A6E">V_IN</text>
      <line x1="50" y1="92" x2="78" y2="92" stroke="#0284C7" stroke-width="2" />
      {svg_tg(112, 92, scale=0.82, title="TG1 (2/6)", sub="Φ₁")}
      <line x1="146" y1="92" x2="225" y2="92" stroke="#D97706" stroke-width="2.6" />
      <circle cx="188" cy="92" r="4" fill="#D97706" />
      <text x="188" y="76" text-anchor="middle" font-size="11.5" font-weight="800" fill="#B45309">Nút V1 (rất nhạy!)</text>

      <!-- C1 downward at V1 -->
      <line x1="188" y1="92" x2="188" y2="128" stroke="#0369A1" stroke-width="2" />
      <line x1="168" y1="128" x2="208" y2="128" stroke="#0369A1" stroke-width="3" />
      <line x1="168" y1="138" x2="208" y2="138" stroke="#0369A1" stroke-width="3" />
      <line x1="188" y1="138" x2="188" y2="162" stroke="#0369A1" stroke-width="2" />
      <line x1="176" y1="162" x2="200" y2="162" stroke="#0C4A6E" stroke-width="2" />
      <text x="148" y="140" text-anchor="end" font-size="10.5" font-weight="800" fill="#0369A1">C₁ = 100 fF</text>

      <!-- Stray Cp,V1 dashed beside C1 -->
      <line x1="218" y1="92" x2="218" y2="128" stroke="#D97706" stroke-width="1.8" stroke-dasharray="3,2" />
      <line x1="208" y1="128" x2="228" y2="128" stroke="#D97706" stroke-width="2.2" />
      <line x1="208" y1="136" x2="228" y2="136" stroke="#D97706" stroke-width="2.2" />
      <line x1="218" y1="136" x2="218" y2="162" stroke="#D97706" stroke-width="1.8" stroke-dasharray="3,2" />
      <text x="234" y="136" font-size="10" font-weight="800" fill="#B45309">ΔC_p,V1</text>

      <!-- TG2 -->
      {svg_tg(260, 92, scale=0.82, title="TG2 (2/6)", sub="Φ₂")}
      <line x1="294" y1="92" x2="360" y2="92" stroke="#0284C7" stroke-width="2.4" />
      <circle cx="332" cy="92" r="4" fill="#0369A1" />
      <text x="332" y="76" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">Nút VX</text>

      <!-- C2 feedback -->
      <rect x="308" y="116" width="84" height="38" rx="6" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.8" />
      <text x="350" y="133" text-anchor="middle" font-size="10" font-weight="800" fill="#0369A1">C₂ = 800 fF</text>
      <text x="350" y="147" text-anchor="middle" font-size="9" font-weight="700" fill="#B45309">+ XDUM2 (1/3 µm)</text>

      <!-- Comparison Boxes on Right -->
      <rect x="415" y="34" width="212" height="84" rx="10" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2" />
      <text x="521" y="54" text-anchor="middle" font-size="11" font-weight="800" fill="#B45309">Iter 1 (TG 4/12 + DUM1,2)</text>
      <text x="521" y="73" text-anchor="middle" font-size="10.5" fill="#0C4A6E">ΔC_p,V1 ≈ 22.7 fF (cộng thẳng C₁)</text>
      <text x="521" y="90" text-anchor="middle" font-size="10.5" fill="#0C4A6E">f_c = 230.26 kHz (+22.69% ❌)</text>
      <text x="521" y="107" text-anchor="middle" font-size="10" font-weight="700" fill="#B45309">SFDR = 47.84 dB • ENOB = 7.61 b</text>

      <rect x="415" y="130" width="212" height="86" rx="10" fill="#E0F2FE" stroke="#0284C7" stroke-width="2.2" />
      <text x="521" y="150" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">Iter 2 (TG 2/6 + Bỏ DUM1)</text>
      <text x="521" y="169" text-anchor="middle" font-size="10.5" fill="#0C4A6E">Cắt bớt tụ vùng cống trên V1</text>
      <text x="521" y="186" text-anchor="middle" font-size="10.5" font-weight="800" fill="#0369A1">f_c = 193.97 kHz (+3.36% ✓)</text>
      <text x="521" y="203" text-anchor="middle" font-size="10" font-weight="700" fill="#0C4A6E">SFDR = 54.14 dB • ENOB = 8.62 b</text>
    </svg>
    """


def _svg_w4_isolation_cross_section() -> str:
    """3-layer Mixed-Signal & MIM shielding diagram (white/blue/gold)."""
    return f"""
    <svg viewBox="0 0 640 225" class="w-full h-[210px]">
      {svg_defs()}
      <text x="320" y="16" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0369A1">
        Mặt Cắt 3 Lớp Chống Nhiễu Nền &amp; Chắn Faraday Cho Mảng Tụ MIM Sky130A
      </text>

      <!-- Substrate & P+ Guard ring -->
      <rect x="24" y="164" width="592" height="44" rx="8" fill="#F0F9FF" stroke="#0284C7" stroke-width="1.8" />
      <text x="320" y="191" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0C4A6E">
        Đế Silicon P-Substrate (Nối đất chuẩn qua P+ Guard Ring bao quanh Clock, TG &amp; OTA — Cách ly Digital/Analog &gt; 20 µm)
      </text>

      <!-- Left: Digital / Clock vs Guard Ring -->
      <rect x="34" y="96" width="128" height="52" rx="8" fill="#FFFBEB" stroke="#D97706" stroke-width="2" />
      <text x="98" y="118" text-anchor="middle" font-size="11" font-weight="800" fill="#B45309">Xung Nhịp Số</text>
      <text x="98" y="135" text-anchor="middle" font-size="10" fill="#0C4A6E">dV/dt lớn (Tây)</text>

      <rect x="172" y="102" width="38" height="58" rx="5" fill="#E0F2FE" stroke="#0369A1" stroke-width="2" />
      <text x="191" y="128" text-anchor="middle" font-size="9.5" font-weight="800" fill="#0369A1">P+</text>
      <text x="191" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#0369A1">Ring</text>

      <!-- Center: MIM Faraday Shield -->
      <rect x="228" y="34" width="218" height="30" rx="6" fill="#0284C7" stroke="#0369A1" stroke-width="1.8" />
      <text x="337" y="53" text-anchor="middle" font-size="10.5" font-weight="800" fill="#FFFFFF">Top-Plate (capm / met4) → Nút VX, V1</text>

      <rect x="236" y="68" width="202" height="16" rx="4" fill="#FEF3C7" stroke="#F59E0B" stroke-width="1.4" />
      <text x="337" y="79" text-anchor="middle" font-size="9" font-weight="800" fill="#B45309">Oxide Cách Điện MIM (2.0 fF/µm²)</text>

      <rect x="228" y="88" width="218" height="28" rx="6" fill="#FFFBEB" stroke="#D97706" stroke-width="2" />
      <text x="337" y="106" text-anchor="middle" font-size="10.5" font-weight="800" fill="#B45309">Bottom-Plate (met3) → Nối VSS (Chắn ồn)</text>

      <line x1="228" y1="130" x2="446" y2="130" stroke="#0369A1" stroke-width="2" stroke-dasharray="5,3" />
      <text x="337" y="148" text-anchor="middle" font-size="9.5" font-weight="700" fill="#0369A1">met3=VSS hút toàn bộ nhiễu nền từ Đế Si!</text>

      <!-- Right: OTA Analog -->
      <rect x="466" y="102" width="38" height="58" rx="5" fill="#E0F2FE" stroke="#0369A1" stroke-width="2" />
      <text x="485" y="128" text-anchor="middle" font-size="9.5" font-weight="800" fill="#0369A1">P+</text>
      <text x="485" y="142" text-anchor="middle" font-size="9" font-weight="700" fill="#0369A1">Ring</text>

      <rect x="514" y="96" width="94" height="52" rx="8" fill="#E0F2FE" stroke="#0284C7" stroke-width="2" />
      <text x="561" y="118" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">5T-OTA</text>
      <text x="561" y="135" text-anchor="middle" font-size="10" fill="#0C4A6E">36-finger ABBA</text>
    </svg>
    """


def _svg_w4_5x5_mim_grid() -> str:
    """5x5 MIM Common-Centroid matrix (16 Dummy + 8 C2 + 1 C1 at center (2,2))."""
    cells = []
    size = 38
    gap = 4
    ox, oy = 32, 26
    for r in range(5):
        for c in range(5):
            x = ox + c * (size + gap)
            y = oy + r * (size + gap)
            if r == 2 and c == 2:
                fill, stroke, txt_c, lbl = "#F59E0B", "#B45309", "#FFFFFF", "C1"
            elif 1 <= r <= 3 and 1 <= c <= 3:
                fill, stroke, txt_c, lbl = "#0284C7", "#0369A1", "#FFFFFF", "C2"
            else:
                fill, stroke, txt_c, lbl = "#E0F2FE", "#7DD3FC", "#0369A1", "D"
            cells.append(
                f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="5" fill="{fill}" stroke="{stroke}" stroke-width="1.6" />'
                f'<text x="{x + size/2}" y="{y + size/2 + 4}" text-anchor="middle" font-size="10.5" font-weight="800" fill="{txt_c}">{lbl}</text>'
            )
    grid_svg = "\n".join(cells)
    return f"""
    <svg viewBox="0 0 280 245" class="w-full h-[230px]">
      <text x="137" y="16" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">Ma Trận 5×5 MIM Common-Centroid</text>
      {grid_svg}
      <text x="137" y="238" text-anchor="middle" font-size="10" font-weight="700" fill="#0C4A6E">
        C₁ tại tâm (2,2) • 8× C₂ bao quanh • 16× Dummy D (VSS)
      </text>
    </svg>
    """


def _svg_w4_closing_roadmap() -> str:
    """4-week closed-loop visual summary."""
    return f"""
    <svg viewBox="0 0 1080 175" class="w-full h-[165px]">
      {svg_defs()}
      <rect x="14" y="20" width="232" height="132" rx="12" fill="#E0F2FE" stroke="#0369A1" stroke-width="2.2" />
      <text x="130" y="45" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">Tuần 1: Lý Thuyết &amp; Specs</text>
      <text x="130" y="68" text-anchor="middle" font-size="11" fill="#0C4A6E">H(z), f_c = 187.675 kHz</text>
      <text x="130" y="88" text-anchor="middle" font-size="11" fill="#0C4A6E">Kiến trúc 4 khối • Gate 1</text>
      <text x="130" y="114" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284C7">week1_theory_notes.md</text>

      <line x1="246" y1="86" x2="288" y2="86" stroke="#0284C7" stroke-width="2.6" marker-end="url(#arr-blue)" />

      <rect x="294" y="20" width="232" height="132" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
      <text x="410" y="45" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">Tuần 2: Golden Model</text>
      <text x="410" y="68" text-anchor="middle" font-size="11" fill="#0C4A6E">Python Float64 + kT/C 72.1 dB</text>
      <text x="410" y="88" text-anchor="middle" font-size="11" fill="#0C4A6E">Error Budget &amp; gm/ID Sizing</text>
      <text x="410" y="114" text-anchor="middle" font-size="10.5" font-weight="700" fill="#D97706">metrics_golden.json • Gate 2</text>

      <line x1="526" y1="86" x2="568" y2="86" stroke="#D97706" stroke-width="2.6" marker-end="url(#arr-gold)" />

      <rect x="574" y="20" width="232" height="132" rx="12" fill="#E0F2FE" stroke="#0284C7" stroke-width="2.2" />
      <text x="690" y="45" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">Tuần 3: Pre-Layout SPICE</text>
      <text x="690" y="68" text-anchor="middle" font-size="11" fill="#0C4A6E">9 file Xschem IEEE + BSIM4</text>
      <text x="690" y="88" text-anchor="middle" font-size="11" fill="#0C4A6E">f_c=193.97 kHz (+3.36%), SFDR 54.1 dB</text>
      <text x="690" y="114" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0284C7">metrics_week3_prelayout.json</text>

      <line x1="806" y1="86" x2="848" y2="86" stroke="#0284C7" stroke-width="2.6" marker-end="url(#arr-blue)" />

      <rect x="854" y="20" width="212" height="132" rx="12" fill="#FFFBEB" stroke="#D97706" stroke-width="2.6" />
      <text x="960" y="45" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">Tuần 4: Tape-Out GDSII</text>
      <text x="960" y="68" text-anchor="middle" font-size="11" fill="#0C4A6E">149.3×101.3 µm • DRC=0</text>
      <text x="960" y="88" text-anchor="middle" font-size="11" fill="#0C4A6E">LVS Unique • PEX 203.45 kHz</text>
      <text x="960" y="114" text-anchor="middle" font-size="10.5" font-weight="800" fill="#B45309">top_sc_lpf.gds • Gate 4 PASS</text>
    </svg>
    """


def get_week3_slides() -> list[SlideSpec]:
    f_foot = "SKY130-SC-LPF • Tuần 3: Thiết Kế Schematic Xschem Chuẩn IEEE &amp; Kiểm Chứng BSIM4 Pre-Layout"
    return [
        # S01: COVER
        SlideSpec(
            act_tag="",
            title="",
            badge="",
            badge_tone="ocean",
            is_cover=True,
            section_id="w3-start",
            body_html="""
            <div class="flex items-center justify-between border-b-2 border-sky-200 pb-3 relative z-10">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-md bg-sky-600 text-white text-xs font-bold tracking-widest uppercase mono">IEEE / ISSCC DESIGN SERIES</span>
                <span class="text-sky-900 text-sm font-semibold mono">PDK: SkyWater 130nm (sky130A) • Xschem + Ngspice BSIM4</span>
              </div>
              <span class="px-3 py-1 rounded-full bg-amber-100 border border-amber-400 text-amber-900 text-xs font-bold mono">TUẦN 03 / 04 — SCHEMATIC &amp; PRE-LAYOUT</span>
            </div>

            <div class="my-auto py-2 relative z-10">
              <p class="text-amber-700 font-bold tracking-wider uppercase text-xs mono mb-1.5">From $g_m/I_D$ Sizing to Verified Transistor-Level Schematic Netlists</p>
              <h1 class="text-[44px] font-extrabold tracking-tight leading-tight text-sky-950 max-w-5xl">
                Thiết Kế Schematic Chuẩn IEEE<br />
                <span class="text-sky-600">&amp; Mô Phỏng Ngspice BSIM4 Pre-Layout</span>
              </h1>
              <p class="text-sky-900 text-base mt-3 max-w-4xl">
                Tuần 3 trả lời chuỗi câu hỏi thực chiến: <strong class="text-amber-800">Tuần 3 là gì?</strong> $\\to$ <strong class="text-sky-700">Ký hiệu cổng IEEE &amp; cấu trúc phân cấp?</strong> $\\to$ <strong class="text-sky-950">Đo từng khối qua Testbench ra sao?</strong> $\\to$ <strong class="text-amber-800">Tại sao phải sửa Iter 1 $\\to$ Iter 2 mới thắng Gate 3?</strong>
              </p>

              <div class="grid grid-cols-4 gap-4 mt-8">
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">1. Tần số cắt Pre-Layout</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$193.972\\text{ kHz}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Sai lệch $+3.36\\%$ &lt; Ngưỡng $5\\%$</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">2. Độ tuyến tính Phổ FFT</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$\\text{SFDR} = 54.14\\text{ dB}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">$\\text{ENOB} = 8.62\\text{ bits},\\ \\text{THD} = 0.207\\%$</div>
                </div>
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">3. Bão hòa 5T-OTA (.op)</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$5/5\\text{ MOS PASS}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">$A_{OL}=41.62\\text{ dB},\\ \\text{PM}=81.05^\\circ$</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">4. Sạch Schematic Xschem</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$9\\text{ Cells} • \\text{ERC}=0$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Xuất đủ $AD, AS, PD, PS$</div>
                </div>
              </div>
            </div>
            """,
            next_question="Ở Tuần 2 ta đã có bảng kích thước $W/L$ và Golden Model — vậy chính xác Tuần 3 là gì và tại sao mô hình Python vẫn chưa đủ để thay thế Ngspice BSIM4?",
            footer_text="Data Source: xschem/*.sch • ngspice/tb_*.spice • metrics_week3_prelayout.json",
            speaker_notes="Mở đầu Tuần 3: dẫn người xem đi từ câu hỏi Tại sao cần Schematic BSIM4 dù Python Tuần 2 đã mô phỏng gần đủ.",
        ),

        # S02: WHAT IS WEEK 3 & WHY BSIM4
        SlideSpec(
            act_tag="Hồi I — Định Nghĩa &amp; Mục Đích Chiến Lược Của Tuần 3",
            title="Tuần 3 Là Gì? Vì Sao Đã Có Python Vẫn Phải Lên Schematic BSIM4?",
            badge="Transistor-Level Truth",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Giới hạn tất yếu của mô hình toán học Tuần 2</span>
                  <h3 class="text-lg font-extrabold text-sky-950 mt-1">Python Chỉ Thấy Những Gì Ta Tự Viết Vào</h3>
                  <ul class="mt-3 space-y-2 text-sm text-sky-950 list-disc pl-4">
                    <li>Trong Python, khóa là 1 điện trở đơn $R_{\\text{on}}$; trong silicon thật, BSIM4 có thêm <strong>tụ chồng cổng–máng $C_{gd}, C_{gs}$</strong> và <strong>tụ vùng khuếch tán $C_{db}, C_{sb}$</strong> (<span class="code-tag">AD, AS, PD, PS</span>).</li>
                    <li>5T-OTA thật có cực nội bộ $V_{D1}$, giới hạn biên độ ra, độ lệch hệ thống ($-1.85\\text{ mV}$) và dòng rò dưới ngưỡng.</li>
                    <li>Mỗi transistor cần ký hiệu kết nối chuẩn xác 4 cực (<span class="code-tag">D, G, S, B</span>) để Tuần 4 chạy LVS không gãy.</li>
                  </ul>
                </div>
                <div class="bg-white border border-amber-300 rounded-lg p-2.5 text-xs font-bold text-amber-900 text-center mt-2">
                  Tuần 3 biến “con số giấy” $W/L$ thành lưới Transistor sống!
                </div>
              </div>

              <div class="col-span-7 flex flex-col gap-3 justify-center">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Nhiệm vụ 1 • Dựng Thư viện 9 Schematic &amp; Symbol Chuẩn IEEE</div>
                  <p class="text-sm text-sky-950 mt-1">Vẽ phân cấp trên Xschem với ký hiệu chuẩn quốc tế (<span class="code-tag">NOT, NAND2, AND2, TG, OTA</span>) — bảo đảm sạch <span class="code-tag">ERC = 0</span> và xuất chính xác tham số diện tích/chu vi nguồn–máng.</p>
                </div>
                <div class="ieee-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Nhiệm vụ 2 • Kiểm chứng Đơn vị (Unit Verification) Bằng Testbench</div>
                  <p class="text-sm text-sky-950 mt-1">Cô lập từng khối qua 4 testbench chuyên biệt: đo $t_{\\text{nov}}$ (<span class="code-tag">tb_clk</span>), quét $R_{\\text{on}}(V)$ (<span class="code-tag">tb_tg</span>), kiểm <span class="code-tag">.op/.ac/.tran</span> (<span class="code-tag">tb_ota</span>) trước khi ghép chung.</p>
                </div>
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Nhiệm vụ 3 • Gỡ Lỗi Toàn Mạch (Iter 1 → Iter 2) &amp; So Golden</div>
                  <p class="text-sm text-sky-950 mt-1">Chạy mô phỏng LPTV toàn mạch (<span class="code-tag">tb_top_sc_lpf</span> + <span class="code-tag">tb_top_bode</span>), xử lý ký sinh nút $V_1$ và kéo sai lệch $f_c$ xuống còn $+3.36\\%$ (&lt; $5\\%$).</p>
                </div>
              </div>
            </div>
            """,
            next_question="Bước đầu tiên vẽ Schematic, làm sao để sơ đồ nguyên lý nhìn vào là hiểu ngay chức năng của từng cổng logic và từng khối thay vì toàn những hộp chữ nhật vô hồn?",
            footer_text=f_foot,
            speaker_notes="Tuần 3 giúp kiểm chứng toàn bộ hành vi phi tuyến thực của model BSIM4PDK sky130A mà Python đơn giản hóa.",
        ),

        # S03: STANDARD IEEE SYMBOLS & LEAF CELLS
        SlideSpec(
            act_tag="Hồi I — Chuẩn Hóa Ký Hiệu Logic IEEE/ANSI Trên Xschem",
            title="Sửa Lại Toàn Bộ Ký Hiệu Logic Chuẩn IEEE &amp; Các Tế Bào Cơ Sở CMOS",
            badge="Standard IEEE Symbols",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_logic_and_cells.png" alt="IEEE Symbols and Leaf Cells" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_logic_and_cells.png:</span> 6 ký hiệu chuẩn IEEE/ANSI (<span class="code-tag">NOT, NAND2, AND2, TG, Dummy, 5T-OTA</span>) &amp; sơ đồ transistor bên trong.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Tại sao sửa ký hiệu hộp → IEEE?</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Thay thế toàn bộ hộp chữ nhật chung chung bằng: <strong>tam giác + bóng đảo (<span class="code-tag">NOT</span>)</strong>, <strong>thân chữ D + bóng (<span class="code-tag">NAND2</span>)</strong>, <strong>chữ D không bóng (<span class="code-tag">AND2</span>)</strong>, <strong>2 tam giác đối đầu (<span class="code-tag">TG</span>)</strong> và <strong>Op-Amp (<span class="code-tag">5T-OTA</span>)</strong>.
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Bảo toàn tọa độ chân &amp; LVS 100%</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Tất cả tọa độ chân cắm (<span class="code-tag">pin</span>) giữ nguyên đúng lưới <span class="mono">20 mil</span> Xschem và bổ sung thêm cell <span class="code-tag-gold">and2_cell.sch</span> (<span class="code-tag">NAND2 + NOT</span>) — hoàn toàn không làm sai netlist SPICE.
                  </p>
                </div>
                <div class="ieee-card py-2 text-xs text-sky-900">
                  <strong>9 file sạch ERC=0:</strong> <span class="code-tag">inv_cell</span>, <span class="code-tag">nand2_cell</span>, <span class="code-tag">and2_cell</span>, <span class="code-tag">non_overlap_clk</span>, <span class="code-tag">tg_switch</span>, <span class="code-tag">tg_dummy</span>, <span class="code-tag">sc_core</span>, <span class="code-tag">ota_5t</span>, <span class="code-tag">top_sc_lpf</span>.
                </div>
              </div>
            </div>
            """,
            next_question="Từ 9 tế bào chuẩn IEEE này, làm thế nào chúng được ghép thành sơ đồ hệ thống top_sc_lpf.sch và đi dây tránh chéo nhau?",
            footer_text=f_foot,
            speaker_notes="Nêu bật việc thiết kế lại hình ảnh ký hiệu logic trên Xschem để đạt chuẩn hội nghị và trực quan hóa hướng dòng tín hiệu.",
        ),

        # S04: TOP-LEVEL HIERARCHY
        SlideSpec(
            act_tag="Hồi I — Kiến Trúc Phân Cấp Top-Level Schematic",
            title="Sơ Đồ Hệ Thống Phân Cấp Toàn Chip (<span class='code-tag'>top_sc_lpf.sch</span>)",
            badge="Hierarchical Schematic",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_top_sc_lpf.png" alt="Top SC LPF Schematic" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_top_sc_lpf.png:</span> Đường dẫn dòng $I_{\\text{BIAS}}$ rẽ gọn phía trên-phải, hoàn toàn tách bạch vòng hồi tiếp $V_{\\text{OUT}} \\to V_{\\text{INN}}$.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Luồng tín hiệu &amp; Phân cấp</div>
                  <ul class="text-xs text-sky-950 mt-1 space-y-1 list-disc pl-4">
                    <li><strong>Phía trên:</strong> Khối <span class="code-tag">XCLK (non_overlap_clk)</span> nhận <span class="code-tag">CLK</span> tạo 4 pha sạch <span class="code-tag">PHI1/1B/2/2B</span>.</li>
                    <li><strong>Đường chính:</strong> <span class="code-tag">VIN</span> $\\to$ <span class="code-tag">XSC (sc_core)</span> $\\to$ nút ảo <span class="code-tag">VX</span> $\\to$ <span class="code-tag">XOTA (ota_5t)</span> $\\to$ <span class="code-tag">VOUT</span>.</li>
                    <li><strong>Hồi tiếp đơn vị:</strong> <span class="code-tag">VOUT</span> nối trực tiếp về <span class="code-tag">VINN</span>, giữ nút $V_X$ ở đất ảo $V_{\\text{CM}} = 0.9\\text{ V}$.</li>
                  </ul>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Xuất tham số Vùng Khuếch Tán (AD/AS)</div>
                  <p class="text-xs text-sky-950 mt-1">
                    Xschem tự xuất công thức hình học S/D (<span class="mono">AD=W*0.29, AS=W*0.29, PD=2W+0.58</span>) — giúp mô phỏng Pre-Layout <strong>thấy trước ~75% tụ ký sinh của bản thân transistor</strong>!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Sơ đồ tổng thể đã khép kín — nhưng nếu chạy thẳng toàn mạch ngay mà lỗi thì làm sao biết khối nào hỏng? Ta cần thiết kế 4 Testbench kiểm tra ra sao?",
            footer_text=f_foot,
            speaker_notes="Giới thiệu schematic top_sc_lpf.sch sau khi đã dọn sạch các đường dây chéo và tách nhánh IBIAS.",
        ),

        # S05: 4 TESTBENCHES OVERVIEW
        SlideSpec(
            act_tag="Hồi II — Phương Pháp Luận Kiểm Chứng Với 4 Testbench",
            title="Xây Dựng Hệ Thống 4 Testbench (<span class='code-tag'>tb_clk, tb_tg, tb_ota, tb_top</span>)",
            badge="Divide &amp; Conquer",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_testbenches.png" alt="Four Ngspice Testbenches" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_testbenches.png:</span> 4 bàn thử nghiệm SPICE độc lập — từ đo thời gian trễ, quét DC $R_{\\text{on}}$, phá vòng AC OTA đến Coherent FFT.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ieee-card py-2 border-l-4 border-l-sky-600">
                  <div class="text-xs font-bold text-sky-800 mono">1. tb_clk.spice (.tran 10p 250n)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Nguồn xung $10\\text{ MHz}$ ($t_r=t_f=100\\text{ ps}$) + 4 tụ tải $25\\text{ fF}$ đại diện cực cổng của <span class="code-tag">TG1, TG2</span>.</p>
                </div>
                <div class="ieee-card py-2 border-l-4 border-l-amber-500">
                  <div class="text-xs font-bold text-amber-800 mono">2. tb_tg.spice (.dc Vin 0 1.8 5m)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Áp sai thế nhỏ $\\Delta V_{DS} = 1\\text{ mV}$ để đo chuẩn xác $R_{\\text{on}}(V_{\\text{in}}) = 1\\text{ mV} / |I_{\\text{test}}|$.</p>
                </div>
                <div class="ieee-card py-2 border-l-4 border-l-blue-600">
                  <div class="text-xs font-bold text-blue-800 mono">3. tb_ota.spice (.op + .ac + .tran)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Kỹ thuật <strong>phá vòng AC siêu lớn</strong> (<span class="code-tag">L=1GH, C=1GF</span>): giữ điểm DC tự động đóng vòng nhưng cắt đứt hồi tiếp khi quét AC!</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold text-amber-900 mono">4. tb_top_sc_lpf + tb_top_bode</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Ghép tải $C_L = 1\\text{ pF}$, $I_{\\text{ref}} = 30\\ \\mu\\text{A}$, nguồn $58.59\\text{ kHz}$ Coherent hoặc 11-tone Multisine.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Bắt đầu từ Khối 1 (<span class='code-tag'>non_overlap_clk</span>): bên trong mạch tạo xung không chồng lấn gồm những cổng CMOS nào và tạo trễ 3 ns bằng cách gì?",
            footer_text=f_foot,
            speaker_notes="Giới thiệu tổng quan 4 testbench mô phỏng đơn vị và toàn mạch trong ngspice/.",
        ),

        # S06: BLOCK 1 NON_OVERLAP_CLK SCHEMATIC
        SlideSpec(
            act_tag="Hồi II — Thiết Kế &amp; Kiểm Định Từng Khối Con (1/4)",
            title="Khối 1 (<span class='code-tag'>non_overlap_clk</span>): Chốt Chéo NAND2 &amp; Chuỗi Trễ 6 Tầng",
            badge="Block 1 Schematic",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_non_overlap_clk.png" alt="Non Overlap Clock Schematic" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_non_overlap_clk.png:</span> Giao tiếp ký hiệu IEEE <span class="code-tag">XINV0</span>, cặp chốt chéo <span class="code-tag">XNAND_A/B</span>, chuỗi 6 <span class="code-tag">NOT</span> tạo trễ $t_{\\text{nov}}$ &amp; đệm pha đảo.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Cơ chế Break-Before-Make</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Xung ra của nhánh $\\Phi_1$ đi ngược về chân thứ 2 của <span class="code-tag">XNAND_B</span>. Vì phải đợi tín hiệu TẮT của nhánh này truyền qua hết <strong>6 tầng trễ <span class="code-tag">NOT</span> ($L = 0.95\\ \\mu\\text{m}$)</strong>, nhánh $\\Phi_2$ buộc phải mở chậm lại đúng bằng $t_{\\text{nov}}$!
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Cân bằng tải đối xứng $\\Phi_1 / \\overline{\\Phi_1}$</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Đệm ra dùng <span class="code-tag">inv_cell</span> ($L=0.15\\ \\mu\\text{m}$, $W_n=1.2\\ \\mu\\text{m}, W_p=2.8\\ \\mu\\text{m}$) cho sườn dốc $174\\text{ ps}$ — giảm rung chuyển thời gian (jitter) lúc lấy mẫu.
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Sơ đồ mạch tạo xung nhìn rất hợp lý trên giấy — khi bấm nút chạy Ngspice <span class='code-tag'>tb_clk.spice</span>, 4 pha xung thực tế đo được bao nhiêu ns?",
            footer_text=f_foot,
            speaker_notes="Phân tích chi tiết schematic non_overlap_clk.sch với các cổng NAND2 và NOT chuẩn IEEE.",
        ),

        # S07: BLOCK 1 WORKSTATION VERIFICATION
        SlideSpec(
            act_tag="Hồi II — Kiểm Chứng Khối 1 Trên Xschem &amp; Ngspice",
            title="Kết Quả Đo Kiểm Khối 1: Khoảng Chết Đối Xứng $3.116\\text{ ns} / 3.092\\text{ ns}$",
            badge="Gate Block 1: PASS",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_gui_clk_workstation.png" alt="Clock Workstation Light Mode" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_gui_clk_workstation.png:</span> Ảnh chụp Xschem nền sáng + Terminal đo BSIM4 + Đồ thị dạng sóng 4 pha <span class="code-tag">PHI1, PHI1B, PHI2, PHI2B</span>.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Bảng số liệu đo Ngspice (Load <span class="normal-case">25 fF</span>)</div>
                  <table class="ieee-table text-xs mt-1.5">
                    <thead><tr><th class="p-1.5 text-left">Thông số</th><th class="p-1.5 text-right">Đo thực</th><th class="p-1.5 text-right">Mục tiêu</th></tr></thead>
                    <tbody>
                      <tr><td class="p-1.5 font-semibold">$t_{\\text{nov}, 1\\to 2}$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">3.116 ns</td><td class="p-1.5 text-right">2–5 ns ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">$t_{\\text{nov}, 2\\to 1}$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">3.092 ns</td><td class="p-1.5 text-right">2–5 ns ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">$t_r / t_f$ (20–80%)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">174 / 220 ps</td><td class="p-1.5 text-right">&lt; 500 ps ✓</td></tr>
                      <tr class="row-gold"><td class="p-1.5 font-semibold">$\\max(V_{\\Phi_1} V_{\\Phi_2})$</td><td class="p-1.5 text-right font-bold text-amber-800 mono">0.00295 V²</td><td class="p-1.5 text-right">≈ 0 ✓</td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="gold-card py-2 text-xs text-sky-950">
                  <strong>Ý nghĩa vật lý:</strong> Tích $V_{\\Phi_1} V_{\\Phi_2} = 2.95\\text{ mV}^2$ khẳng định tại mọi thời điểm chuyển mạch, chưa bao giờ cả hai khóa $TG_1$ và $TG_2$ cùng mở để làm rò điện tích $C_1$!
                </div>
              </div>
            </div>
            """,
            next_question="Xung điều khiển 4 pha đã sạch tuyệt đối — tiếp theo, Khối 2 (<span class='code-tag'>tg_switch</span> &amp; <span class='code-tag'>tg_dummy</span>) được vẽ ra sao để truyền cả dải điện áp quanh $V_{\\text{CM}} = 0.9\\text{ V}$?",
            footer_text=f_foot,
            speaker_notes="Khối 1 vượt Gate Tuần 3 trọn vẹn với khoảng chết đối xứng ~3.1 ns, sườn dốc sub-220 ps.",
        ),

        # S08: BLOCK 2 TG_SWITCH & TG_DUMMY SCHEMATIC
        SlideSpec(
            act_tag="Hồi II — Thiết Kế &amp; Kiểm Định Từng Khối Con (2/4)",
            title="Khối 2 (<span class='code-tag'>tg_switch</span> &amp; <span class='code-tag'>tg_dummy</span>): Cặp Song Song CMOS &amp; Khóa Bù W/2",
            badge="Block 2 Schematic",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_tg_switch.png" alt="TG Switch Schematic" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_tg_switch.png:</span> Mắc song song <span class="code-tag">XM_N</span> ($W=2\\ \\mu\\text{m}, nf=1$) và <span class="code-tag">XM_P</span> ($W=6\\ \\mu\\text{m}, nf=2$), nối body chuẩn về <span class="code-tag">VSS / VDD</span>.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Cấu tạo &amp; Tỷ lệ $W_p / W_n = 3$</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Trong Sky130A, độ linh động lỗ trống $\\mu_p \\approx \\mu_n / 3$. Khi lấy $W_p = 6.0\\ \\mu\\text{m}$ và $W_n = 2.0\\ \\mu\\text{m}$ ($L = 0.15\\ \\mu\\text{m}$), độ dẫn $g_{ds,n}$ và $g_{ds,p}$ cân bằng nhau tại vùng giữa $V_{\\text{CM}} = 0.9\\text{ V}$.
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Khóa Bù <span class="code-tag-gold">tg_dummy</span> ($W/2$)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Chập ngắn chân $D \\equiv S$ và kích bởi xung ngược pha $\\overline{\\Phi}$: khi khóa chính tắt nhả $Q_{ch}/2$, khóa Dummy bật lên để hút đúng lượng điện tích đó vào kênh mới!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Khi rút kích thước $W_n/W_p$ từ $4/12\\ \\mu\\text{m}$ (nháp ban đầu) xuống $2/6\\ \\mu\\text{m}$ để giảm ký sinh, điện trở thông $R_{\\text{on}}(V_{\\text{in}})$ có bị vượt trần $5\\text{ k}\\Omega$ không?",
            footer_text=f_foot,
            speaker_notes="Trình bày cấu trúc tg_switch và vai trò khóa bù tg_dummy W/2.",
        ),

        # S09: BLOCK 2 TG WORKSTATION VERIFICATION
        SlideSpec(
            act_tag="Hồi II — Quét DC Đo Đường Đặc Tuyến $R_{\\text{on}}(V_{\\text{in}})$",
            title="Kết Quả Đo Kiểm Khối 2: $R_{\\text{on,max}} = 4.431\\text{ k}\\Omega &lt; 5\\text{ k}\\Omega$ &amp; Nạp $105.8\\tau$",
            badge="Gate Block 2: PASS",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_gui_tg_workstation.png" alt="TG Switch Workstation" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_gui_tg_workstation.png:</span> Đường cong $R_{\\text{on}}(V_{\\text{in}})$ toàn dải $0 \\to 1.8\\text{ V}$ tại điểm cực đại đỉnh giữa $4.431\\text{ k}\\Omega$.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Thông số đo BSIM4 (.dc)</div>
                  <table class="ieee-table text-xs mt-1.5">
                    <thead><tr><th class="p-1.5 text-left">Điểm đo</th><th class="p-1.5 text-right">Giá trị</th><th class="p-1.5 text-right">Chuẩn</th></tr></thead>
                    <tbody>
                      <tr><td class="p-1.5 font-semibold">$R_{\\text{on}}(0.90\\text{ V})$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">3.713 kΩ</td><td class="p-1.5 text-right">Rất phẳng ✓</td></tr>
                      <tr class="row-gold"><td class="p-1.5 font-semibold">$R_{\\text{on,max}}$ (@$0.955\\text{ V}$)</td><td class="p-1.5 text-right font-bold text-amber-800 mono">4.431 kΩ</td><td class="p-1.5 text-right">&lt; 5.0 kΩ ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">$R_{\\text{on,min}}$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">0.463 kΩ</td><td class="p-1.5 text-right">Vùng rìa ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">$\\tau_{\\max} = R_{\\text{on,max}} C_1$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">0.443 ns</td><td class="p-1.5 text-right">105.8τ ✓</td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="gold-card py-2 text-xs text-sky-950">
                  <strong>Biên độ nạp siêu dư:</strong> Trong thời gian mở $T_{\\text{on}} \\approx 46.9\\text{ ns}$, tụ $C_1 = 100\\text{ fF}$ được nạp qua <strong>$105.8$ hằng số thời gian $\\tau$</strong> (sai số chưa nạp $e^{-105.8} \\approx 0$)!
                </div>
              </div>
            </div>
            """,
            next_question="Đã có xung sạch (Khối 1) và khóa dẫn tốt (Khối 2) — chúng được ghép với hai tụ MIM trong Khối 3 (<span class='code-tag'>sc_core</span>) ra sao và đặt Dummy ở đâu cho tối ưu?",
            footer_text=f_foot,
            speaker_notes="Phân tích đường cong Ron của tg_switch (2um/6um) đảm bảo phẳng dưới 5 kOhm trên toàn dải.",
        ),

        # S10: BLOCK 3 SC_CORE SCHEMATIC
        SlideSpec(
            act_tag="Hồi II — Thiết Kế &amp; Kiểm Định Từng Khối Con (3/4)",
            title="Khối 3 (<span class='code-tag'>sc_core</span>): Mảng Tụ Đơn Vị MIM &amp; Bù Điện Tích Chọn Lọc",
            badge="Block 3 Schematic",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_sc_core.png" alt="SC Core Schematic" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_sc_core.png:</span> Nhánh rẽ hình chữ T gồm <span class="code-tag">XTG1, XTG2</span>, <span class="code-tag">XC1 (MF=1)</span>, <span class="code-tag">XC2 (MF=8)</span> và khóa bù chọn lọc <span class="code-tag-gold">XDUM2</span> tại nút $V_X$.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Chuẩn hóa Tụ Đơn vị MIM ($100\\text{ fF}$)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Cả $C_1$ và $C_2$ dùng chung 1 tế bào gốc <span class="code-tag">cap_mim_m3_1</span> kích thước $W=4.85\\ \\mu\\text{m}, L=9.85\\ \\mu\\text{m}$ ($C_u = 100.0\\text{ fF}$ đã tính trừ bù $dw=0.15\\ \\mu\\text{m}$): <span class="mono font-bold">XC1 (MF=1)</span> và <span class="mono font-bold">XC2 (MF=8)</span> $\\implies$ bảo toàn tuyệt đối tỷ lệ $C_2/C_1 = 8.000$.
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Quyết định Kỹ thuật: Bỏ <span class="code-tag-gold">XDUM1</span> ở $V_1$!</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Ta <strong>chỉ giữ <span class="code-tag-gold">XDUM2</span> ($1.0 / 3.0\\ \\mu\\text{m}$) tại nút ảo $V_X$</strong> để chặn lệch áp DC (với $\\Phi_2 \\implies Q_{ci}$ đổi thẳng thành $V_{\\text{offset}}$), còn ở nút $V_1$ ta loại bỏ Dummy để không làm phình $C_{p,V1}$!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Đó là lõi thụ động $C_1, C_2$ — nhưng để vận chuyển điện tích từ $C_1$ sang $C_2$ mà không sụt áp, ta cần Khối 4: Bộ khuếch đại <span class='code-tag'>ota_5t</span> thiết kế ra sao?",
            footer_text=f_foot,
            speaker_notes="Giới thiệu cấu trúc sc_core dùng tụ đơn vị MIM MF=1 vs MF=8 và lý do chỉ gắn XDUM2 tại VX.",
        ),

        # S11: BLOCK 4 5T-OTA SCHEMATIC
        SlideSpec(
            act_tag="Hồi II — Thiết Kế &amp; Kiểm Định Từng Khối Con (4/4)",
            title="Khối 4 (<span class='code-tag'>ota_5t</span>): Khuếch Đại Vi Sai 5-Transistor &amp; Nguồn Dòng Đuôi",
            badge="Block 4 Schematic",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_sch_ota_5t.png" alt="5T OTA Schematic" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_sch_ota_5t.png:</span> Cặp vi sai NMOS <span class="code-tag">XM1/XM2</span> ($32/0.5$), Gương PMOS <span class="code-tag">XM3/XM4</span> ($16/0.5$), và Nguồn dòng đuôi <span class="code-tag">XM5/XM6</span> ($24/1.0$).
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Ưu điểm Vàng của 5T-OTA Một Tầng</div>
                  <ul class="text-xs text-sky-950 mt-1 space-y-1 list-disc pl-4">
                    <li><strong>Tự bù pha bởi tải $C_L$:</strong> Chỉ có 1 cực chính tại đầu ra $V_{\\text{OUT}}$ ($C_L = 1\\text{ pF}$ + $C_2$), cực nội bộ $V_{D1}$ nằm rất cao $\\implies$ PM đạt $81^\\circ$ không cần tụ bù Miller!</li>
                    <li>Chiều dài $L = 0.50\\ \\mu\\text{m}$ (&gt;$3\\times L_{\\min}$) nâng trở kháng ra $r_o$, giúp $A_{OL} = g_m (r_{o2} \\parallel r_{o4})$ vượt $40\\text{ dB}$.</li>
                  </ul>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Gương dòng $I_{\\text{ref}} = 30\\ \\mu\\text{A}$ &amp; Phân cực</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Dòng <span class="code-tag">XM6</span> ($12/1.0$) nhân bản $2\\times$ sang <span class="code-tag">XM5</span> ($24/1.0$, $L=1.0\\ \\mu\\text{m}$) cho dòng đuôi đo thực $I_{\\text{tail}} = 28.17\\ \\mu\\text{A}$ (độ ổn định cao quanh điểm $V_{\\text{CM}} = 0.9\\text{ V}$).
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Dùng bàn đo <span class='code-tag'>tb_ota.spice</span> phá vòng AC ($L=1\\text{ GH}, C=1\\text{ GF}$), đáp ứng tần số Bode và tốc độ quay (Slew Rate) của 5T-OTA thực đo đạt bao nhiêu?",
            footer_text=f_foot,
            speaker_notes="Phân tích sơ đồ nguyên lý ota_5t với cặp vi sai NMOS, gương PMOS và dòng đuôi gấp đôi từ Iref=30 uA.",
        ),

        # S12: BLOCK 4 OTA WORKSTATION VERIFICATION
        SlideSpec(
            act_tag="Hồi II — Đo Kiểm Vòng Hở &amp; Quá Độ Của 5T-OTA",
            title="Kết Quả Đo Kiểm Khối 4: $A_{OL}=41.62\\text{ dB},\\ \\text{GBW}=43.61\\text{ MHz},\\ \\text{PM}=81.05^\\circ$",
            badge="Gate Block 4: PASS",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_gui_ota_workstation.png" alt="OTA Workstation" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_gui_ota_workstation.png:</span> Xschem 5T-OTA, nhật ký kiểm tra bão hòa <span class="code-tag">.op</span> và đồ thị Bode AC vòng hở ổn định biên độ–pha.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Hiệu năng AC &amp; Tran (.ac / .tran)</div>
                  <table class="ieee-table text-xs mt-1.5">
                    <thead><tr><th class="p-1.5 text-left">Tiêu chí OTA</th><th class="p-1.5 text-right">Ngspice</th><th class="p-1.5 text-right">Gate 3</th></tr></thead>
                    <tbody>
                      <tr><td class="p-1.5 font-semibold">Độ lợi $A_{OL}$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">41.62 dB</td><td class="p-1.5 text-right">&gt; 35–40 dB ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">Băng thông $\\text{GBW}$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">43.61 MHz</td><td class="p-1.5 text-right">&gt; 10 MHz ✓</td></tr>
                      <tr class="row-gold"><td class="p-1.5 font-semibold">Dự trữ pha $\\text{PM}$</td><td class="p-1.5 text-right font-bold text-amber-800 mono">81.05°</td><td class="p-1.5 text-right">&ge; 60° ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">$\\text{SR}^+ / \\text{SR}^-$</td><td class="p-1.5 text-right font-bold text-sky-700 mono">22.9 / 21.7 V/µs</td><td class="p-1.5 text-right">Nhanh ✓</td></tr>
                      <tr><td class="p-1.5 font-semibold">DC Offset (@$0.9\\text{ V}$)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−1.85 mV</td><td class="p-1.5 text-right">Nhỏ ✓</td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="gold-card py-2 text-xs text-sky-950">
                  <strong>Ý nghĩa thiết kế:</strong> $\\text{GBW} = 43.61\\text{ MHz} \\approx 4.36 \\times f_{\\text{clk}}$ giúp đầu ra OTA xác lập trọn vẹn trong $46.9\\text{ ns}$ mỗi bán chu kỳ $\\Phi_2$!
                </div>
              </div>
            </div>
            """,
            next_question="Các chỉ số AC đã quá đẹp — nhưng về mặt vật lý bán dẫn, cả 5 transistor <span class='code-tag'>XM1–XM5</span> có đang thực sự nằm sâu trong vùng bão hòa hay sắp chạm ranh giới triode?",
            footer_text=f_foot,
            speaker_notes="Trình bày kết quả đo AC và Slew Rate của 5T-OTA trên bàn đo tb_ota.spice.",
        ),

        # S13: SATURATION TABLE & 4-BLOCK SUMMARY
        SlideSpec(
            act_tag="Hồi II — Kiểm Định Bão Hòa (.op) &amp; Tổng Hợp 4 Khối Đơn Vị",
            title="Bảng Biên Bão Hòa 5 Transistor (<span class='code-tag'>.op</span>) &amp; Bảng Tổng Kết 4 Khối",
            badge="All 4 Blocks: PASS",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-6 fig-frame">
                <img src="figs/w3_unit_blocks_summary.png" alt="Unit Blocks Summary Plots" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_unit_blocks_summary.png:</span> 4 biểu đồ kiểm chứng độc lập đồng thời trên BSIM4 (Clock, TG $R_{\\text{on}}$, OTA Bode, Slew Step).
                </p>
              </div>
              <div class="col-span-6 flex flex-col gap-3">
                <div class="ieee-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono mb-1.5">Kiểm tra vùng hoạt động BSIM4 ($V_{DS} - V_{DSAT} > 0$)</div>
                  <table class="ieee-table text-xs">
                    <thead><tr><th class="p-1.5 text-left">Transistor</th><th class="p-1.5 text-left">Vai trò</th><th class="p-1.5 text-right">$g_m$ / $I_D$</th><th class="p-1.5 text-right">Biên Bão Hòa</th></tr></thead>
                    <tbody>
                      <tr><td class="p-1.5 font-bold text-sky-800 mono">XM1 (N)</td><td class="p-1.5">Cặp vi sai $V_{\\text{in}}+$</td><td class="p-1.5 text-right mono">289.5 µS</td><td class="p-1.5 text-right font-bold text-sky-700 mono">+379.2 mV ✓</td></tr>
                      <tr><td class="p-1.5 font-bold text-sky-800 mono">XM2 (N)</td><td class="p-1.5">Cặp vi sai $V_{\\text{in}}-$</td><td class="p-1.5 text-right mono">289.5 µS</td><td class="p-1.5 text-right font-bold text-sky-700 mono">+592.9 mV ✓</td></tr>
                      <tr><td class="p-1.5 font-bold text-amber-800 mono">XM3 (P)</td><td class="p-1.5">Gương tải diode</td><td class="p-1.5 text-right mono">14 µA</td><td class="p-1.5 text-right font-bold text-sky-700 mono">+970.5 mV ✓</td></tr>
                      <tr><td class="p-1.5 font-bold text-amber-800 mono">XM4 (P)</td><td class="p-1.5">Gương tải ra</td><td class="p-1.5 text-right mono">14 µA</td><td class="p-1.5 text-right font-bold text-sky-700 mono">+757.6 mV ✓</td></tr>
                      <tr class="row-gold"><td class="p-1.5 font-bold text-sky-900 mono">XM5 (N)</td><td class="p-1.5">Nguồn dòng đuôi</td><td class="p-1.5 text-right mono">28.17 µA</td><td class="p-1.5 text-right font-bold text-amber-800 mono">+136.6 mV ✓</td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="gold-card py-2.5 text-xs text-sky-950">
                  <strong>Ý nghĩa Biên $+136.6\\text{ mV}$ tại XM5:</strong> Cả 5 transistor nằm sâu trong vùng bão hòa; ngay cả khi tín hiệu xoay chiều dao động quanh $0.9\\text{ V}$, <span class="code-tag-gold">XM5</span> vẫn giữ dòng đuôi ổn định $28.17\\ \\mu\\text{A}$ không bị sập vào vùng tuyến tính!
                </div>
              </div>
            </div>
            """,
            next_question="Tất cả 4 khối đơn vị đều PASSED xuất sắc — vậy khi ghép chung chúng thành <span class='code-tag'>top_sc_lpf</span>, mọi thứ có tự động chạy đúng $187.675\\text{ kHz}$ luôn không? (Cú ngoặt Lịch sử Tuần 3!)",
            footer_text=f_foot,
            speaker_notes="Bảng điểm .op khẳng định 5/5 transistor bão hòa vững vàng kèm tóm tắt 4 khối đơn vị.",
        ),

        # S14: ROOT CAUSE DEBUGGING (ITER 1 FAILURE)
        SlideSpec(
            act_tag="Hồi III — Ghép Toàn Mạch &amp; Truy Tìm Nguyên Nhân Lệch +22.69%",
            title="Cú Sốc Ghép Mạch (Iter 1): Tại Sao 4 Khối Tốt Lại Cho $f_c = 230.26\\text{ kHz}$ (+22.69% FAIL)?",
            badge="Engineering Debugging",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-7 fig-frame">
                __SVG_ROOTCAUSE__
              </div>
              <div class="col-span-5 flex flex-col gap-2.5">
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Hiện trường Lỗi Iter 1 (TG 4/12 + DUM1 &amp; DUM2)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Khi chạy toàn mạch lần đầu, tần số cắt vọt lên <strong>$230.260\\text{ kHz}$ (lệch $+22.69\\%$ $\\gg$ ngưỡng $5\\%$)</strong>, độ méo <span class="mono">SFDR</span> chỉ còn $47.84\\text{ dB}$, mất hơn $1\\text{ bit}$ ENOB ($7.61\\text{ b}$)!
                  </p>
                </div>
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Phân tích Nguyên nhân Vật lý (BSIM4 Parasitics)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Tụ $C_1$ chỉ bằng $100\\text{ fF}$! Nhưng nút đỉnh <span class="code-tag">V1</span> ở giữa hai khóa lớn phải cõng đồng thời tụ vùng khuếch tán &amp; tụ chồng của: <strong>TG1 ($4/12$) + TG2 ($4/12$) + XDUM1 ($2/6$)</strong>.
                  </p>
                  <div class="bg-white border border-sky-200 rounded p-2 mt-1.5 text-center text-xs font-bold text-sky-900">
                    $\\Delta C_{p,V1} \\approx 22.7\\text{ fF} \\implies C_{1,\\text{eff}} = C_1 + \\Delta C_{p,V1} \\approx 122.7\\text{ fF} \\implies f_c \\uparrow +22.7\\%!$
                  </div>
                </div>
              </div>
            </div>
            """.replace("__SVG_ROOTCAUSE__", _svg_w3_寄生_rootcause()),
            next_question="Khi đã bắt đúng “thủ phạm” là $\\Delta C_{p,V1} = 22.7\\text{ fF}$ làm phình $C_1$ hữu dụng, ta phải phẫu thuật mạch ra sao ở Vòng lặp 2 (Iter 2) mà vẫn giữ nguyên $R_{\\text{on}} &lt; 5\\text{ k}\\Omega$?",
            footer_text=f_foot,
            speaker_notes="Đây là bài học Analog Design đắt giá nhất Tuần 3: nút nhạy V1 rất dễ bị phình dung lượng bởi S/D của khóa quá lớn và Dummy thừa.",
        ),

        # S15: ITER 2 OPTIMIZATION SOLUTION
        SlideSpec(
            act_tag="Hồi III — Tối Ưu Kiến Trúc (Iter 1 → Iter 2)",
            title="Phẫu Thuật Iter 2: Thu Gọn TG (2/6) &amp; Bỏ Dummy Trên Nút $V_1$ → Kéo $f_c$ Về $+3.36\\%$",
            badge="Root-Cause Solved",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 flex flex-col gap-3">
                <div class="ocean-card py-3 border-l-4 border-l-sky-600">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Quyết định 1 • Thu gọn TG1 &amp; TG2 từ 4/12 → <span class="normal-case">2/6 µm</span></div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Nhờ phát hiện ở Sl.09 rằng <span class="code-tag">TG 2/6</span> vẫn cho $R_{\\text{on,max}} = 4.431\\text{ k}\\Omega &lt; 5\\text{ k}\\Omega$ và thời gian nạp $105.8\\tau$, việc cắt đôi bề rộng khóa lập tức <strong>giảm $50\\%$ điện tích bơm $Q_{ch}$ lẫn tụ ký sinh nút $V_1$</strong>!
                  </p>
                </div>
                <div class="gold-card py-3 border-l-4 border-l-amber-500">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Quyết định 2 • Gỡ bỏ XDUM1 khỏi nút V1, chỉ giữ XDUM2 tại VX</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Ở nút ảo $V_X$, bơm điện tích gây trôi áp DC nên cần <span class="code-tag-gold">XDUM2</span> ($1.0/3.0\\ \\mu\\text{m}$) và ký sinh $C_{p,VX}$ được OTA hồi tiếp hấp thụ vô hại! Ngược lại tại $V_1$, bỏ <span class="code-tag">XDUM1</span> giúp giữ $C_{1,\\text{eff}}$ sát $100\\text{ fF}$ nhất.
                  </p>
                </div>
              </div>

              <div class="col-span-6 ieee-card py-3">
                <div class="text-xs font-bold uppercase text-sky-800 mono mb-2">Bảng Đối Chiếu Trước &amp; Sau Phẫu Thuật (Pre-Layout)</div>
                <table class="ieee-table text-xs">
                  <thead>
                    <tr><th class="p-2 text-left">Thông số Toàn mạch</th><th class="p-2 text-right">Iter 1 (Cũ)</th><th class="p-2 text-right">Iter 2 (Chốt)</th><th class="p-2 text-right">Cải thiện</th></tr>
                  </thead>
                  <tbody>
                    <tr class="row-gold"><td class="p-2 font-bold">Tần số cắt $f_c$</td><td class="p-2 text-right mono">230.260 kHz</td><td class="p-2 text-right font-extrabold text-sky-700 mono">193.972 kHz</td><td class="p-2 text-right font-bold text-amber-800">+22.7% → +3.36% ✓</td></tr>
                    <tr><td class="p-2 font-semibold">SFDR (Phổ FFT)</td><td class="p-2 text-right mono">47.84 dB</td><td class="p-2 text-right font-bold text-sky-700 mono">54.14 dB</td><td class="p-2 text-right font-bold text-sky-700">+6.30 dB ✓</td></tr>
                    <tr><td class="p-2 font-semibold">THD (%)</td><td class="p-2 text-right mono">−47.57 (0.418%)</td><td class="p-2 text-right font-bold text-sky-700 mono">−53.67 (0.207%)</td><td class="p-2 text-right font-bold text-sky-700">Giảm 2× méo ✓</td></tr>
                    <tr><td class="p-2 font-semibold">ENOB hiệu dụng</td><td class="p-2 text-right mono">7.61 bits</td><td class="p-2 text-right font-bold text-sky-700 mono">8.62 bits</td><td class="p-2 text-right font-bold text-sky-700">+1.01 bit ✓</td></tr>
                    <tr><td class="p-2 font-semibold">Charge-Inj DC Shift</td><td class="p-2 text-right mono">−1.90 mV</td><td class="p-2 text-right font-bold text-amber-800 mono">−52 µV</td><td class="p-2 text-right font-bold text-amber-800">Triệt tiêu 36× ✓</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            """,
            next_question="Nhưng trong Ngspice, mạch tụ chuyển mạch (LPTV) không chạy được lệnh <span class='code-tag'>.ac</span> bình thường! Vậy ta đo đường Bode và Coherent FFT toàn mạch bằng thủ thuật gì?",
            footer_text=f_foot,
            speaker_notes="So sánh định lượng giữa Iter 1 (thất bại +22.69%) và Iter 2 (thành công +3.36%) nhờ tối ưu tụ ký sinh.",
        ),

        # S16: TOP WORKSTATION & LPTV METHODOLOGY
        SlideSpec(
            act_tag="Hồi III — Thủ Thuật Mô Phỏng LPTV Trên Ngspice",
            title="Đo Toàn Mạch BSIM4: Lệnh <span class='code-tag'>.tran</span> + <span class='code-tag'>Strobe 98 ns</span> + <span class='code-tag'>method=gear</span>",
            badge="LPTV Verification",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_gui_top_workstation.png" alt="Top Level Workstation" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_gui_top_workstation.png:</span> Sơ đồ phân cấp <span class="code-tag">top_sc_lpf.sch</span> đang chạy Ngspice BSIM4 sóng vào–ra mượt mà &amp; log đo kết quả.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">1. Vì sao cấm dùng lệnh .ac trên mạch SC?</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Lệnh <span class="code-tag">.ac</span> đóng băng khóa tại một điểm DC ($t=0$): nó thấy $R_{\\text{on}}$ nối liên tục hoặc đứt hẳn chứ <strong>không thấy xung chuyển mạch $10\\text{ MHz}$</strong>!</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">2. Giải pháp: Strobe cuối pha $\\Phi_2$ ($t = kT + 98\\text{ ns}$)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Trích mẫu sóng <span class="code-tag">.tran</span> tại đúng thời điểm $98\\text{ ns}$ mỗi chu kỳ $100\\text{ ns}$ (khi $C_1$ và $C_2$ vừa ổn định xong) để khớp từng điểm với chuỗi $y[n]$ của Python Golden!</p>
                </div>
                <div class="ieee-card py-2">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">3. Tham số chuẩn xác SPICE (.options)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Chạy <span class="code-tag">64 + 512 = 576 chu kỳ</span> ($57.6\\ \\mu\\text{s}$), <span class="code-tag-gold">method=gear</span> chống rung tích phân số, <span class="code-tag">maxstep=2 ns</span> &amp; nguồn $58.59375\\text{ kHz}$ ($M=3, N=512$).</p>
                </div>
              </div>
            </div>
            """,
            next_question="Dùng đúng dữ liệu sóng 11-tần Multisine và sóng bậc thang chuẩn hóa ấy đặt đè lên Golden Model — hai đường cong khớp nhau đến mức nào?",
            footer_text=f_foot,
            speaker_notes="Giải thích lý do không thể chạy .ac cho mạch tụ chuyển mạch và quy trình Strobe cuối pha Phi2 + method=gear.",
        ),

        # S17: TIME & MULTISINE BODE OVERLAY
        SlideSpec(
            act_tag="Hồi IV — Đối Chiếu Sóng Thời Gian &amp; Đáp Ứng Tần Số Multisine",
            title="Khớp Sóng Thời Gian &amp; Bode Đa Tần: Golden ($187.68$) vs. Pre-Layout ($193.97\\text{ kHz}$)",
            badge="Overlay Δfc = +3.36%",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_prelayout_vs_golden_time_bode.png" alt="Pre-Layout vs Golden Time & Bode" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_prelayout_vs_golden_time_bode.png:</span> Sóng bậc thang ra $V_{\\text{out}}(t)$ khớp biên độ ($189.38$ vs $190.90\\text{ mV}_p$) &amp; 11 điểm Bode Multisine bám sát lý thuyết $H(z)$.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Kỹ thuật Schroeder 11-Tone (<span class="code-tag">tb_top_bode</span>)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Thay vì chạy 11 file <span class="code-tag">.tran</span> rời rạc, ta cộng 11 sóng sin pha Schroeder ($39.06\\text{ kHz} \\to 3.125\\text{ MHz}$) vào duy nhất 1 lần chạy $N=256$ rồi lấy $H(f) = Y(f)/X(f)$!
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Kết quả So khớp Bode 3-dB</div>
                  <ul class="text-xs text-sky-950 mt-1 space-y-1 list-disc pl-4">
                    <li><strong>Golden Model:</strong> $187.675\\text{ kHz}$</li>
                    <li><strong>Pre-Layout SPICE:</strong> <span class="mono font-bold text-sky-800">$193.972\\text{ kHz}$</span></li>
                    <li><strong>Độ lệch $\\Delta f_c$:</strong> <span class="mono font-bold text-amber-900">$+3.36\\%$</span> (Nhỏ hơn hẳn ngưỡng Gate 3 là $\\pm 5\\%$ ✓).</li>
                  </ul>
                </div>
              </div>
            </div>
            """,
            next_question="Đáp ứng tần số và sóng thời gian đã rất sát Golden Model — còn phổ méo hài phi tuyến trên miền tần số FFT (<span class='code-tag'>SFDR, THD, ENOB</span>) đạt chuẩn bao nhiêu bit?",
            footer_text=f_foot,
            speaker_notes="Phân tích đồ thị đè hình giữa Python Golden và Ngspice BSIM4 qua phép đo 11-tone Schroeder Multisine.",
        ),

        # S18: COHERENT FFT SPECTRUM OVERLAY
        SlideSpec(
            act_tag="Hồi IV — Phân Tích Phổ Coherent FFT 512-Điểm",
            title="Phổ Coherent FFT Ngspice BSIM4: $\\text{SFDR}=54.14\\text{ dB},\\ \\text{ENOB}=8.62\\text{ bits}$",
            badge="Spectral Integrity",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w3_prelayout_vs_golden_fft.png" alt="Pre-Layout vs Golden FFT" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w3_prelayout_vs_golden_fft.png:</span> Phổ FFT $N=512$ ($f_0=58.59375\\text{ kHz}, A_{\\text{in}}=0.20\\text{ V}_p$) — Đáy nhiễu &amp; đỉnh hài bậc 2, bậc 3 lộ rõ trên BSIM4.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Các Chỉ số Phổ Đo Thực (Iter 2)</div>
                  <table class="ieee-table text-xs mt-1.5">
                    <thead><tr><th class="p-1.5 text-left">Chỉ số FFT</th><th class="p-1.5 text-right">Pre-Layout</th></tr></thead>
                    <tbody>
                      <tr class="row-gold"><td class="p-1.5 font-semibold">SFDR (Khoảng động)</td><td class="p-1.5 text-right font-bold text-amber-800 mono">54.14 dB</td></tr>
                      <tr><td class="p-1.5 font-semibold">THD (Độ méo tổng)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−53.67 dB (0.207%)</td></tr>
                      <tr><td class="p-1.5 font-semibold">SNDR / ENOB</td><td class="p-1.5 text-right font-bold text-sky-700 mono">53.66 dB / 8.62 b</td></tr>
                      <tr><td class="p-1.5 font-semibold">HD₂ / HD₃</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−54.06 / −59.13 dBc</td></tr>
                    </tbody>
                  </table>
                </div>
                <div class="gold-card py-2 text-xs text-sky-950">
                  <strong>Bản chất vật lý:</strong> Đỉnh hài bậc 2 ($HD_2=-54.06\\text{ dBc}$) xuất phát từ tính bất đối xứng tự nhiên của kiến trúc Single-Ended + bơm điện tích phụ thuộc áp tín hiệu của <span class="code-tag">TG1</span> — hoàn toàn khớp dự đoán lý thuyết!
                </div>
              </div>
            </div>
            """,
            next_question="Tất cả kết quả đo từng khối và toàn mạch BSIM4 đã có — đối chiếu từng điều kiện một với bảng Cổng Kiểm Định Tuần 3 (Gate 3), chúng ta đạt 100% chưa?",
            footer_text=f_foot,
            speaker_notes="Phân tích phổ Coherent FFT và nguồn gốc vật lý của hài bậc 2/bậc 3 trong cấu trúc Single-Ended.",
        ),

        # S19: GATE 3 VERIFICATION SCORECARD
        SlideSpec(
            act_tag="Hồi IV — Nghiệm Thu Cổng Kiểm Định Tuần 3 (Verification Gate 3)",
            title="Bảng Đối Chiếu 2 Cột Chính Thức: Golden Model vs. Pre-Layout SPICE BSIM4",
            badge="Verification Gate 3: PASSED",
            badge_tone="gold",
            body_html="""
            <div class="ieee-card py-2.5">
              <table class="ieee-table text-xs">
                <thead>
                  <tr>
                    <th class="p-2 text-left">Hạng mục Kiểm định (Gate Tuần 3)</th>
                    <th class="p-2 text-right">Yêu cầu Chốt (Spec)</th>
                    <th class="p-2 text-right">Golden (Tuần 2)</th>
                    <th class="p-2 text-right">Pre-Layout (Tuần 3)</th>
                    <th class="p-2 text-center">Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr><td class="p-2 font-semibold">Khoảng không chồng lấn $t_{\\text{nov},12} / t_{\\text{nov},21}$</td><td class="p-2 text-right">$2.0\\text{–}5.0\\text{ ns}$</td><td class="p-2 text-right mono">2.92 ns (ref)</td><td class="p-2 text-right font-bold text-sky-700 mono">3.116 / 3.092 ns</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-2 font-semibold">Nội trở khóa $R_{\\text{on}}(0.9\\text{ V}) / R_{\\text{on,max}}$</td><td class="p-2 text-right">$&lt; 5.0\\text{ k}\\Omega$</td><td class="p-2 text-right mono">5.0 kΩ (budget)</td><td class="p-2 text-right font-bold text-sky-700 mono">3.713 / 4.431 kΩ</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-2 font-semibold">Bão hòa 5T-OTA <span class="code-tag">XM1–XM5</span> (.op)</td><td class="p-2 text-right">$V_{DS} > V_{DSAT}$</td><td class="p-2 text-right mono">Lý tưởng</td><td class="p-2 text-right font-bold text-sky-700 mono">+136.6 đến +970.5 mV</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-2 font-semibold">Độ lợi &amp; Tốc độ OTA ($A_{OL} / \\text{GBW} / \\text{PM}$)</td><td class="p-2 text-right">&gt;$35\\text{ dB}$ / &gt;$10\\text{ M}$ / $\\ge 60^\\circ$</td><td class="p-2 text-right mono">41.6 / 43.9 / 81.3</td><td class="p-2 text-right font-bold text-sky-700 mono">41.62 dB / 43.61 M / 81.05°</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr class="row-gold"><td class="p-2 font-bold">Tần số cắt toàn mạch $f_{c,\\text{SC}}$</td><td class="p-2 text-right font-bold">$|\\Delta f_c| &lt; 5\\%$</td><td class="p-2 text-right font-bold mono">187.675 kHz</td><td class="p-2 text-right font-extrabold text-amber-800 mono">193.972 kHz (+3.36%)</td><td class="p-2 text-center"><span class="badge-gold">PASS ✓</span></td></tr>
                  <tr><td class="p-2 font-semibold">Phổ FFT (<span class="code-tag">SFDR / THD / ENOB</span>)</td><td class="p-2 text-right">&gt;$50\\text{ dB}$</td><td class="p-2 text-right mono">149.50 dB (float64)</td><td class="p-2 text-right font-bold text-sky-700 mono">54.14 dB / 0.207% / 8.62 b</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-2 font-semibold">Biên độ ra tại $58.59\\text{ kHz}$ &amp; Sạch ERC</td><td class="p-2 text-right">ERC = 0</td><td class="p-2 text-right mono">190.90 mVp</td><td class="p-2 text-right font-bold text-sky-700 mono">189.38 mVp • 9 Cell ERC=0</td><td class="p-2 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Sơ đồ Schematic đã xanh mướt 100% qua Gate Tuần 3 — nhưng nếu ta cứ thế gửi bản Schematic này đi sản xuất thì có ra được con chip chạy thật không? Bước cuối cùng Tuần 4 là gì?",
            footer_text=f_foot,
            speaker_notes="Tất cả tiêu chí Gate Tuần 3 đều đạt vượt mức, đặc biệt fc=+3.36% < 5% và SFDR=54.14 dB.",
        ),

        # S20: BRIDGE WEEK 3 -> WEEK 4
        SlideSpec(
            act_tag="Kết Luận Tuần 3 &amp; Khởi Động Giai Đoạn Thực Thi Silicon",
            title="Sẵn Sàng Sang Tuần 4: Từ Schematic Xschem Đến Bản Vẽ Vật Lý GDSII",
            badge="Handoff to Week 4",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 ocean-card py-4">
                <div class="text-xs font-bold uppercase text-sky-800 mono">Tài sản Bàn giao Sau Tuần 3</div>
                <ul class="mt-2.5 space-y-2 text-sm text-sky-950 list-disc pl-4">
                  <li><strong>9 file Schematic &amp; Symbol Xschem</strong> chuẩn IEEE (<span class="code-tag">ERC = 0</span>), sạch lỗi kết nối.</li>
                  <li><strong>Cấu hình chốt tối ưu:</strong> <span class="code-tag">TG 2/6 µm</span> + tụ đơn vị MIM <span class="code-tag">100 fF</span> + bù chọn lọc <span class="code-tag">XDUM2</span> tại $V_X$.</li>
                  <li><strong>Netlist tham chiếu <span class="code-tag">top_sc_lpf_xschem.spice</span>:</strong> Làm “chân lý đối chiếu” bắt buộc cho bài kiểm tra <span class="mono font-bold text-amber-800">Netgen LVS</span> ở Tuần 4!</li>
                </ul>
              </div>
              <div class="col-span-6 gold-card py-4">
                <div class="text-xs font-bold uppercase text-amber-800 mono">Cạm bẫy Chờ đón Trên Silicon Thật (Tuần 4)</div>
                <ul class="mt-2.5 space-y-2 text-sm text-sky-950 list-disc pl-4">
                  <li>Khi đi dây đồng/nhôm (<span class="code-tag">met1–met4</span>), mỗi đoạn dây kim loại đều sinh thêm <strong>tụ ghép ký sinh $C_{\\text{wire}}$</strong>. Nút $V_1$ rất nhỏ ($100\\text{ fF}$) chỉ cần vướng thêm $5\\text{ fF}$ dây là $f_c$ dịch $+5\\%$!</li>
                  <li>Xung số $10\\text{ MHz}$ có thể xuyên qua đế Silicon làm nhiễu OTA.</li>
                  <li>Lệch oxit trên phiến wafer dễ phá hỏng tỷ lệ vàng $C_2 / C_1 = 8.0$.</li>
                </ul>
              </div>
            </div>
            """,
            next_question="Bước sang <strong>Tuần 4</strong>: Ta phải bố trí mặt bằng, vẽ tụ Common-Centroid, kiểm định DRC/LVS và chạy mô phỏng ký sinh PEX thế nào để con chip thực sự sẵn sàng Tape-out?",
            footer_text=f_foot,
            speaker_notes="Kết thúc Tuần 3 và mở ra chuỗi câu hỏi cho Tuần 4: Thiết kế Layout vật lý GDSII & Post-Layout PEX.",
        ),
    ]


def get_week4_slides() -> list[SlideSpec]:
    f_foot = "SKY130-SC-LPF • Tuần 4: Thiết Kế Layout Magic GDSII, Sign-Off DRC/LVS &amp; Trích Xuất Ký Sinh Post-Layout (PEX)"
    return [
        # S01: COVER
        SlideSpec(
            act_tag="",
            title="",
            badge="",
            badge_tone="gold",
            is_cover=True,
            section_id="w4-start",
            body_html="""
            <div class="flex items-center justify-between border-b-2 border-sky-200 pb-3 relative z-10">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-md bg-sky-600 text-white text-xs font-bold tracking-widest uppercase mono">IEEE / ISSCC DESIGN SERIES</span>
                <span class="text-sky-900 text-sm font-semibold mono">PDK: SkyWater 130nm (sky130A) • Magic GDSII + Netgen LVS + PEX</span>
              </div>
              <span class="px-3 py-1 rounded-full bg-amber-100 border border-amber-400 text-amber-900 text-xs font-bold mono">TUẦN 04 / 04 — TAPE-OUT SIGN-OFF</span>
            </div>

            <div class="my-auto py-2 relative z-10">
              <p class="text-amber-700 font-bold tracking-wider uppercase text-xs mono mb-1.5">Physical Analog Layout, DRC/LVS Verification &amp; Post-Layout PEX Extraction</p>
              <h1 class="text-[44px] font-extrabold tracking-tight leading-tight text-sky-950 max-w-5xl">
                Thiết Kế Layout Vật Lý GDSII<br />
                <span class="text-sky-600">&amp; Kiểm Định Ký Sinh Post-Layout (PEX)</span>
              </h1>
              <p class="text-sky-900 text-base mt-3 max-w-4xl">
                Tuần 4 khép kín hành trình làm chip bằng 5 câu hỏi lớn: <strong class="text-amber-800">Tuần 4 làm gì?</strong> $\\to$ <strong class="text-sky-700">Chống nhiễu &amp; ghép đối xứng (ABBA/MIM $5\\times 5$) ra sao?</strong> $\\to$ <strong class="text-sky-950">DRC &amp; LVS là gì?</strong> $\\to$ <strong class="text-amber-800">PEX phơi bày thêm $284\\text{ fF}$ tụ dây làm $f_c$ dịch bao nhiêu?</strong>
              </p>

              <div class="grid grid-cols-4 gap-4 mt-8">
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">1. Kích thước Die Chip GDSII</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$149.3 \\times 101.3\\ \\mu\\text{m}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Diện tích $0.0151\\text{ mm}^2$ • 10 Cells</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">2. Sạch Hình học &amp; Mạch</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$\\text{DRC}=0 • \\text{LVS PASS}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Magic 8.3 &amp; KLayout 0.30 • 10/10 Cell</div>
                </div>
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">3. Tần số cắt Post-PEX</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$203.453\\text{ kHz}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Lệch $+4.89\\%$ so Pre (khớp lý thuyết $+5.04\\%$)</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">4. Phổ &amp; Công suất PEX</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$53.60\\text{ dB} • 116.1\\ \\mu\\text{W}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">$\\text{ENOB}=8.49\\text{ b}$ (@1.8 V, $64.48\\ \\mu\\text{A}$)</div>
                </div>
              </div>
            </div>
            """,
            next_question="Ở Tuần 3 ta đã chứng minh Schematic chạy tuyệt đẹp trên BSIM4 — vậy bản chất Tuần 4 là gì và tại sao bản vẽ dây kim loại thật lại cần nhiều kỹ thuật hình học phức tạp đến thế?",
            footer_text="Data Source: layout/*.mag • layout/top_sc_lpf.gds • metrics_week4_postlayout.json • metrics_comparison.json",
            speaker_notes="Mở đầu Tuần 4: giai đoạn cuối cùng biến netlist logic/analog thành bản đồ đa giác silicon GDSII và trích ký sinh PEX.",
        ),

        # S02: WHAT IS WEEK 4 & WHY LAYOUT MATTERS
        SlideSpec(
            act_tag="Hồi I — Định Nghĩa &amp; Mục Đích Chiến Lược Của Tuần 4",
            title="Tuần 4 Là Gì? Vì Sao “Sạch Schematic” Không Đồng Nghĩa Với “Chip Chạy Thật”?",
            badge="Physical Silicon Reality",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Khoảng cách từ Màn hình Schematic đến Nhà máy Fab</span>
                  <h3 class="text-lg font-extrabold text-sky-950 mt-1">Thế giới Ngspice Tuần 3 Vẫn Là “Không Gian 0-D”</h3>
                  <ul class="mt-3 space-y-2 text-sm text-sky-950 list-disc pl-4">
                    <li>Mọi sợi dây nối trong Schematic là siêu dẫn vô hình: <strong>tụ ghép dây–dây và dây–đế = 0 fF</strong>.</li>
                    <li>Hai tụ hay hai transistor mặc định giống hệt nhau 100%, phớt lờ <strong>độ dốc độ dày oxit trên tấm wafer</strong>.</li>
                    <li>Nhà máy đúc chip SkyWater chỉ nhận bản đồ đa giác lớp mặt nạ chuẩn công nghiệp <span class="code-tag-gold">.gds (GDSII)</span> chứ không đúc từ ảnh Schematic!</li>
                  </ul>
                </div>
                <div class="bg-white border border-amber-300 rounded-lg p-2.5 text-xs font-bold text-amber-900 text-center mt-2">
                  Tuần 4 là bài thi Tốt nghiệp đưa mạch chạm mặt Vật lý 3 chiều!
                </div>
              </div>

              <div class="col-span-7 flex flex-col gap-3 justify-center">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Nhiệm vụ 1 • Vẽ Layout Analog Chuẩn Thẩm mỹ &amp; Đối xứng</div>
                  <p class="text-sm text-sky-950 mt-1">Quy hoạch mặt bằng 4 vùng tách nhiễu, dựng mảng tụ MIM $5\\times 5$ Common-Centroid, cặp vi sai <span class="code-tag">ABBA–BAAB</span> 36 ngón và vòng bảo vệ <span class="code-tag">P+ Guard Ring</span>.</p>
                </div>
                <div class="ieee-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Nhiệm vụ 2 • Kiểm định Sign-Off (DRC = 0 &amp; LVS Unique Match)</div>
                  <p class="text-sm text-sky-950 mt-1">Quét sạch vi phạm luật thiết kế hình học trên cả 2 bộ kiểm tra độc lập (Magic + KLayout) và chứng minh Netgen LVS khớp 1-1 với Schematic Tuần 3.</p>
                </div>
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Nhiệm vụ 3 • Trích xuất Ký sinh PEX &amp; Bảng So Sánh 3 Cột</div>
                  <p class="text-sm text-sky-950 mt-1">Nhổ toàn bộ tụ ghép dây (<span class="code-tag">ext2spice cthresh 0</span>) đưa ngược vào Ngspice, lập Bảng 3 Cột (Golden vs. Pre vs. Post-PEX) để chốt nghiệm thu.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Bước vào phòng vẽ Layout Magic, nguyên tắc đầu tiên ta phải quyết định là quy hoạch mặt bằng chip (Floorplan) như thế nào để khối số $10\\text{ MHz}$ không “đầu độc” mạch tương tự?",
            footer_text=f_foot,
            speaker_notes="Giải thích bản chất Tuần 4: cầu nối từ sơ đồ nguyên lý 0-D sang đa giác 3-D thực tế trên wafer Sky130A.",
        ),

        # S03: TOP FLOORPLAN
        SlideSpec(
            act_tag="Hồi I — Quy Hoạch Mặt Bằng (Mixed-Signal Floorplanning)",
            title="Bản Đồ Mặt Bằng Toàn Chip (<span class='code-tag'>149.30 × 101.30 µm</span>): Chia 4 Khu Cách Ly",
            badge="Chip Area 0.0151 mm²",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_layout_top_floorplan.png" alt="Top Floorplan GDSII" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_layout_top_floorplan.png:</span> Bản vẽ GDSII hoàn chỉnh 10 cell phân cấp: Tây (Clock), Nam (Switch Bay), Bắc (MIM $5\\times 5$), Đông (5T-OTA).
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ieee-card py-2 border-l-4 border-l-amber-500">
                  <div class="text-xs font-bold text-amber-800 mono">Khu Tây • non_overlap_clk ($48.0\\times 36.6\\ \\mu\\text{m}$)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">2 hàng logic chuẩn cao thống nhất, bao trọn trong <span class="code-tag-gold">P+ Guard Ring</span> thoát xung nền digital.</p>
                </div>
                <div class="ieee-card py-2 border-l-4 border-l-sky-600">
                  <div class="text-xs font-bold text-sky-800 mono">Khu Nam • Switch Bay ($26.4\\times 21.0\\ \\mu\\text{m}$)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Đặt <span class="code-tag">TG1, TG2</span> ($nf=2$) &amp; <span class="code-tag">XDUM2</span> ($0.5/1.5$) sát biên dưới cụm tụ để dây nối $V_1$ ngắn nhất!</p>
                </div>
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold text-sky-800 mono">Khu Bắc • Mảng MIM $5\\times 5$ ($59.8\\times 63.8\\ \\mu\\text{m}$)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Đặt tâm tụ $C_1$ tại $(0,\\ 33.5\\ \\mu\\text{m})$, bao quanh bởi 8 ô $C_2$ và 16 tụ giả bảo vệ.</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold text-amber-900 mono">Khu Đông • 5T-OTA ($26.0\\times 39.8\\ \\mu\\text{m}$)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Cách xa khối Clock <strong>$&gt; 20\\ \\mu\\text{m}$</strong>, bọc vòng bảo vệ riêng &amp; đường <span class="code-tag">VX</span> đi ngắn sang cửa vào <span class="code-tag">VINN</span>.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Chỉ đặt cách nhau 20 µm vẫn chưa đủ: ở góc độ cắt ngang 3 chiều trên đế Silicon, ta dựng thêm “lá chắn điện từ” nào cho đường dây $V_1, V_X$ và cụm Clock?",
            footer_text=f_foot,
            speaker_notes="Phân tích mặt bằng 149.30 x 101.30 um giúp giảm tối đa tụ ký sinh dây nút nhạy và cách ly Clock số.",
        ),

        # S04: 3-LAYER ISOLATION & GUARD RINGS
        SlideSpec(
            act_tag="Hồi I — Kỹ Thuật Chống Nhiễu Hỗn Hợp (Mixed-Signal Isolation)",
            title="Lá Chắn 3 Lớp: <span class='code-tag'>P+ Guard Ring</span>, Màn Chắn Faraday <span class='code-tag'>met3=VSS</span> &amp; <span class='code-tag'>met4</span> Top-Plate",
            badge="Noise Shielding",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-7 fig-frame">
                __SVG_ISOLATION__
              </div>
              <div class="col-span-5 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">1. Vòng Bảo vệ <span class="code-tag">P+ Guard Ring</span> Kép</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Xung vuông $10\\text{ MHz}$ bơm dòng điện dung xuống đế P-Substrate mỗi lần chuyển trạng thái. Hai vòng tiếp xúc <span class="code-tag">P+</span> nối trực tiếp <span class="code-tag">VSS</span> đóng vai trò “hào thoát nước” gom sạch dòng rò nền trước khi chạm OTA!
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">2. Quy tắc Đấu Bản Cực MIM Chống Ồn Nền</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    <strong>Bản đáy (<span class="code-tag-gold">Bottom-Plate met3</span>)</strong> diện tích rộng giáp đế nhất luôn nối <span class="code-tag">VSS</span> (hoặc ngõ ra <span class="code-tag">VOUT</span>) làm màn chắn Faraday; nút nhạy cao trở <span class="code-tag">V1, VX</span> đi trên <strong>Bản đỉnh (<span class="code-tag">Top-Plate met4</span>)</strong>!
                  </p>
                </div>
              </div>
            </div>
            """.replace("__SVG_ISOLATION__", _svg_w4_isolation_cross_section()),
            next_question="Đã che chắn nhiễu từ dưới đế lên — còn sai lệch tĩnh do máy khắc và độ dày oxit trên wafer thì sao? Ma trận tụ MIM $5\\times 5$ Common-Centroid xử lý điều đó thế nào?",
            footer_text=f_foot,
            speaker_notes="Minh họa cơ chế chắn Faraday của bottom-plate MIM và vòng Guard Ring P+ trong thiết kế Mixed-Signal.",
        ),

        # S05: MIM 5x5 COMMON CENTROID MATH
        SlideSpec(
            act_tag="Hồi I — Thiết Kế Độ Chính Xác Tỷ Lệ Tụ $C_2 / C_1 = 8.000$",
            title="Mảng Tụ MIM $5\\times 5$ Common-Centroid: Triệt Tiêu Gradient Tuyến Tính &amp; Khắc Cạnh",
            badge="Unit-Cap Matching",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-5 fig-frame">
                __SVG_MIM__
              </div>
              <div class="col-span-7 flex flex-col gap-3">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Tại sao không vẽ 1 tụ $100\\text{ fF}$ và 1 tụ lớn $800\\text{ fF}$ rời nhau?</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Axít khắc ăn mòn cạnh ngoài tụ mạnh hơn phần giữa (sai số chu vi $\\Delta W$). Nếu hai tụ có tỷ lệ Chu vi / Diện tích khác nhau, tỷ số $C_2/C_1$ sẽ sai lệch làm méo $f_c$. Dùng <strong>9 tụ đơn vị giống hệt nhau</strong> ($1+8$) khóa chặt tỷ số $P/A$ bằng nhau tuyệt đối!
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Toán học Đồng Tâm (Common-Centroid) &amp; 16 Tụ Giả</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Độ dày oxit thay đổi tuyến tính $d(x,y) = d_0 + g_x x + g_y y$. Khi đặt $C_1$ tại đúng tâm $(2,2)$ và 8 ô $C_2$ đối xứng xung quanh, trọng tâm hình học của $C_1$ và $C_2$ trùng khít $(0,\\ 33.5\\ \\mu\\text{m})$ $\\implies$ <strong>gradient tuyến tính triệt tiêu bằng 0!</strong> 16 tụ Dummy <span class="code-tag-gold">VSS–VSS</span> ở vành ngoài hứng trọn sai số ăn mòn cạnh!
                  </p>
                </div>
              </div>
            </div>
            """.replace("__SVG_MIM__", _svg_w4_5x5_mim_grid()),
            next_question="Tụ điện đã có mảng $5\\times 5$ đồng tâm — vậy các cặp transistor tương tự bên trong <span class='code-tag'>ota_5t</span> được sắp xếp theo mẫu hình học nào để tránh điện áp lệch Offset?",
            footer_text=f_foot,
            speaker_notes="Giải thích lý do thiết kế ma trận 5x5 (1 C1 tâm, 8 C2 vòng trong, 16 Dummy vòng ngoài) để giữ tỷ lệ 8:1 chính xác.",
        ),

        # S06: ZOOM MIM & ABBA-BAAB OTA
        SlideSpec(
            act_tag="Hồi I — Soi Kính Hiển Vi Cấu Trúc Analog Đối Xứng Bậc 2",
            title="Cận Cảnh Mảng MIM $5\\times 5$ &amp; Bố Trí 36 Ngón <span class='code-tag'>ABBA–BAAB</span> Cho 5T-OTA",
            badge="2nd-Order Centroid",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_layout_mim_and_abba_zoom.png" alt="MIM and ABBA Zoom" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_layout_mim_and_abba_zoom.png:</span> Trái: tụ trung tâm $C_1$ nối dây <span class="code-tag">met4</span> | Phải: 36 ngón ($W_f=4.0\\ \\mu\\text{m}$) chia 3 hàng cực chuẩn.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold text-sky-800 mono">Hàng 3 (Trên) • Gương PMOS M3 / M4</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">8 ngón bố trí xen kẽ đối xứng <span class="mono font-bold">A2 – B2 – B2 – A2</span> ($W=16, L=0.5$), cân bằng dòng phản chiếu.</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold text-amber-800 mono">Hàng 2 (Giữa) • Cặp Vi Sai M1 / M2</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">16 ngón sắp kiểu đối xứng bậc 2 <span class="mono font-bold">ABBA – BAAB</span> ($W=32, L=0.5$): triệt tiêu đồng thời gradient tuyến tính lẫn parabol!</p>
                </div>
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold text-sky-800 mono">Hàng 1 (Dưới) • Nguồn Dòng M6 / M5</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">12 ngón ($L=1.0\\ \\mu\\text{m}$) xếp kiểu <span class="mono font-bold">A3 – B6 – A3</span> giúp $I_{\\text{tail}} / I_{\\text{ref}}$ khớp chính xác tỷ số $2:1$.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Chia nhiều ngón rất tốt cho cặp vi sai OTA — nhưng khi ta chia ngón (<span class='code-tag'>nf=2</span>) cho khóa nhỏ <span class='code-tag'>TG</span> ở khu Nam, một hiện tượng vật lý bất ngờ đã xảy ra với $R_{\\text{on}}$ — đó là gì?",
            footer_text=f_foot,
            speaker_notes="Chi tiết cách sắp xếp 36 ngón của 5T-OTA trên 3 hàng và đường đi dây met4 trong mảng MIM.",
        ),

        # S07: WINT & STI NARROW-WIDTH TRADE-OFF IN TG
        SlideSpec(
            act_tag="Hồi I — Phản Tác Dụng Vật Lý Khi Bẻ Ngón Transistor Nhỏ",
            title="Hiệu Ứng Layout Thực Tế (<span class='code-tag'>WINT</span> &amp; <span class='code-tag'>LOD/STI</span>): Vì Sao $R_{\\text{on}}(V_{\\text{CM}})$ Tăng $+23\\%$ Sau Layout?",
            badge="BSIM4 Layout Physics",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 ocean-card py-3.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono">Giải phẫu Hai Biến thể Hình học Của Khóa TG1/TG2</div>
                <p class="text-sm text-sky-950 mt-1.5 leading-relaxed">
                  Trong Schematic Tuần 3, NMOS của khóa <span class="code-tag">TG</span> dùng 1 ngón ($nf=1, W=2.0\\ \\mu\\text{m}$). Khi qua trình sinh Layout tham số hóa Magic (`TG nf=2`), NMOS bị chia thành <strong>2 ngón hẹp $W_f = 1.0\\ \\mu\\text{m}$</strong>. Kết quả đo $R_{\\text{on}}(0.9\\text{ V})$ tăng từ <strong>$3.713\\text{ k}\\Omega \\to 4.566\\text{ k}\\Omega$</strong> (đỉnh $5.059\\text{ k}\\Omega$).
                </p>
                <div class="bg-white border border-sky-200 rounded-lg p-2.5 mt-2.5 text-center">
                  $$W_{\\text{eff,total}} = nf \\cdot (W_f - 2 W_{\\text{INT}}) = 2.0 - 2 \\cdot nf \\cdot W_{\\text{INT}}$$
                </div>
              </div>

              <div class="col-span-6 flex flex-col gap-3">
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">1. Thu hẹp Bề rộng Hữu dụng ($2\\cdot W_{\\text{INT}}$)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Mỗi ngón transistor bị ăn lẹm hai bên mép khuếch tán một đoạn $W_{\\text{INT}}$ (hiệu ứng rãnh cách ly cạn STI). Bẻ đôi số ngón đồng nghĩa <strong>gấp đôi số mép bị mất dẫn</strong> $\\implies$ bề rộng kênh hiệu dụng bị bóp hẹp!
                  </p>
                </div>
                <div class="ieee-card py-2.5 border-l-4 border-l-sky-600">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">2. Hệ quả Thời gian Nạp &amp; Lời khuyên Tape-Out</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Dù $R_{\\text{on}}(V_{\\text{CM}}) = 4.566\\text{ k}\\Omega$ vẫn &lt; $5\\text{ k}\\Omega$ và thời gian nạp $T_{\\text{on}} = 91.3\\tau$ vẫn dư xác lập, kết quả này dạy ta: với khóa tổng $W$ nhỏ ($\\le 2\\ \\mu\\text{m}$), bản sửa sau nên giữ nguyên $nf=1$ hoặc bù thêm $+10\\%$ chiều rộng!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Bản vẽ GDSII 10 cell đã xong xuôi — trước khi xuất ký sinh, làm sao ta chứng minh với nhà máy rằng bản vẽ không có vết chạm chập hình học (DRC) và đấu đúng 100% dây với Schematic (LVS)?",
            footer_text=f_foot,
            speaker_notes="Phân tích nguyên nhân vật lý cực kỳ sâu sắc về WINT và STI làm Ron của TG nf=2 tăng nhưng vẫn hoàn toàn đủ 91.3 tau.",
        ),

        # S08: DRC & LVS CONCEPTS + MAGIC/NETGEN WORKSTATION
        SlideSpec(
            act_tag="Hồi II — Kiểm Định Hình Học &amp; Mạng Lưới (DRC / LVS Sign-Off)",
            title="Kiểm Định Sign-Off (<span class='code-tag'>DRC = 0</span> &amp; <span class='code-tag'>LVS Unique Match</span>) Trên Magic &amp; Netgen",
            badge="DRC &amp; LVS: CLEAN",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_gui_magic_drc_lvs.png" alt="Magic DRC and Netgen LVS Workstation" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_gui_magic_drc_lvs.png:</span> Magic 8.3 <span class="code-tag">drc(full)=0</span>, KLayout 0.30 <span class="code-tag">sky130A_mr.drc=0</span>, và Netgen <span class="code-tag">Circuits match uniquely</span>!
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">1. DRC là gì? (Design Rule Check)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Kiểm tra hàng trăm luật khoảng cách, độ rộng tối thiểu, mật độ kim loại &amp; lưới $0.005\\ \\mu\\text{m}$. Kết quả: <strong>Magic = 0 lỗi</strong> (10/10 cell) &amp; <strong>KLayout FEOL+BEOL = 0 vi phạm</strong>.</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">2. LVS là gì? (Layout vs. Schematic)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">Nhổ netlist từ các đa giác GDSII rồi đối chiếu đồ thị từng nút, từng kích thước $W/L$, số lượng tụ MIM với netlist Xschem Tuần 3.</p>
                </div>
                <div class="ieee-card py-2 text-[11.5px] text-sky-950 font-semibold">
                  Chứng nhận Netgen 1.5.324: <span class="text-sky-700 font-bold mono">10/10 subcircuits matched uniquely, 0 property errors!</span>
                </div>
              </div>
            </div>
            """,
            next_question="Đạt trạng thái “Circuits match uniquely” không hề dễ dàng ngay từ lần chạy đầu tiên — trong quá trình làm LVS cho Sky130A, đội kỹ thuật đã phải giải 2 lỗi hóc búa nào?",
            footer_text=f_foot,
            speaker_notes="Giới thiệu kết quả thực nghiệm DRC (0 lỗi trên cả Magic và KLayout) và LVS (Netgen 10/10 khớp duy nhất).",
        ),

        # S09: 2 REAL LVS DEBUGGING PITFALLS
        SlideSpec(
            act_tag="Hồi II — Nhật Ký Xử Lý 2 Lỗi Thực Nghiệm Sky130A LVS",
            title="Hai Bài Học Kinh Nghiệm Khó Quên Để Netgen LVS Khớp 100% Trên Sky130A",
            badge="Sky130A LVS Pitfalls",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 ocean-card py-3.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold uppercase text-sky-800 mono">Lỗi 1 • Bóng ma “Blackbox” Tụ Giả MIM (Dummy)</span>
                  <span class="badge-ocean">Resolved ✓</span>
                </div>
                <h4 class="text-sm font-extrabold text-sky-950 mt-1.5">Netgen không tự gộp 16 tụ Dummy nối ngắn mạch <span class="code-tag">VSS–VSS</span></h4>
                <ul class="text-xs text-sky-950 mt-2 space-y-1.5 list-disc pl-4 leading-relaxed">
                  <li><strong>Nguyên nhân:</strong> Ở vành ngoài ma trận $5\\times 5$, 16 tụ giả có cả hai cực nối tắt về <span class="code-tag">VSS</span>. Trình nhổ <span class="code-tag">extract</span> gộp cả 16 phần tử song song, còn Schematic nếu không khai báo rõ thì Netgen coi tụ Dummy bị hở/lệch cực!</li>
                  <li><strong>Cách sửa:</strong> Khai báo đồng bộ <span class="code-tag">XCDUM VSS VSS ... MF=16 m=16</span> trong Xschem và đồng nhất thứ tự chân trong file tham chiếu <span class="code-tag">sc_core</span>.</li>
                </ul>
              </div>

              <div class="col-span-6 gold-card py-3.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Lỗi 2 • Nhầm Biến Thể Inverter Trong Cụm Clock</span>
                  <span class="badge-gold">Resolved ✓</span>
                </div>
                <h4 class="text-sm font-extrabold text-sky-950 mt-1.5">Cùng tên cổng <span class="code-tag-gold">NOT</span> nhưng kích thước $L$ khác nhau</h4>
                <ul class="text-xs text-sky-950 mt-2 space-y-1.5 list-disc pl-4 leading-relaxed">
                  <li><strong>Nguyên nhân:</strong> Khối <span class="code-tag">non_overlap_clk</span> dùng 3 vai trò cổng đảo khác hẳn kích thước nhau (đầu vào, tầng trễ $L=0.95\\ \\mu\\text{m}$, đệm ra $L=0.15\\ \\mu\\text{m}$). Nếu để chung tên cell trong Magic thì LVS báo sai thuộc tính $L$!</li>
                  <li><strong>Cách sửa:</strong> Tách rạch ròi 3 subcell chuyên biệt trong Magic: <span class="code-tag">inv_in</span>, <span class="code-tag">inv_del</span> và <span class="code-tag">inv_buf</span> — từ đó 10/10 khối khớp duy nhất với 0 lỗi thuộc tính.</li>
                </ul>
              </div>
            </div>
            """,
            next_question="Chip đã sạch 0 DRC và khớp 100% LVS — vậy bước tiếp theo <strong>PEX (Parasitic Extraction)</strong> là gì, nó trích ra bao nhiêu tụ ký sinh ẩn trong các đường dây kim loại?",
            footer_text=f_foot,
            speaker_notes="Chia sẻ kinh nghiệm gỡ lỗi LVS thực tế trên PDK sky130A mà bất kỳ kỹ sư nào đi làm đều gặp phải.",
        ),

        # S10: PEX PARASITIC BREAKDOWN
        SlideSpec(
            act_tag="Hồi III — Trích Xuất Ký Sinh Post-Layout (<span class='code-tag'>ext2spice cthresh 0</span>)",
            title="Giải Phẫu 123 Tụ Ký Sinh PEX (<span class='code-tag'>284.191 fF</span> Tổng): Dây Đồng Đã “Cộng” Bao Nhiêu?",
            badge="PEX Netlist Analysis",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-5 flex flex-col gap-3">
                <div class="ocean-card py-3">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Lệnh Trích xuất Chính xác Tuyệt đối</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Dùng lệnh Magic <span class="code-tag">ext2spice cthresh 0</span> để không bỏ sót bất kỳ phần tử tụ ghép kim loại nào dù chỉ vài chục atto-Farad ($10^{-18}\\text{ F}$), xuất thẳng thành <span class="code-tag">top_sc_lpf_pex.spice</span>.
                  </p>
                </div>
                <div class="gold-card py-3">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Điểm Nóng Tập Trung Ảnh Hưởng $f_c$</div>
                  <ul class="text-xs text-sky-950 mt-1 space-y-1 list-disc pl-4">
                    <li>Nút <span class="code-tag">V1</span> cõng thêm <strong>$6.569\\text{ fF}$</strong> ($+6.57\\%$ của $C_1 = 100\\text{ fF}$!).</li>
                    <li>Nút <span class="code-tag">VX</span> cõng thêm <strong>$11.614\\text{ fF}$</strong> (chỉ $+1.45\\%$ của $C_2 = 800\\text{ fF}$).</li>
                    <li>Phần lớn điện dung ($59.30\\text{ fF}$) nằm ở nút <span class="code-tag">VTAIL</span> lớn — không hại tốc độ mà còn lọc nhiễu đuôi!</li>
                  </ul>
                </div>
              </div>

              <div class="col-span-7 ieee-card py-2.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono mb-1.5">Phân Bố 123 Tụ Ghép Ký Sinh Trích Từ GDSII (Tổng = <span class="normal-case">284.191 fF</span>)</div>
                <table class="ieee-table text-xs">
                  <thead><tr><th class="p-1.5 text-left">Nút mạch (Net)</th><th class="p-1.5 text-right">$C_{\\text{pex}}$ đo được</th><th class="p-1.5 text-right">Tỷ lệ / Tụ chính</th><th class="p-1.5 text-left">Tác động Mạch học</th></tr></thead>
                  <tbody>
                    <tr class="row-gold"><td class="p-1.5 font-bold text-amber-900 mono">V1 (Đỉnh $C_1$)</td><td class="p-1.5 text-right font-extrabold text-amber-800 mono">6.569 fF</td><td class="p-1.5 text-right font-bold mono">+6.57% ($C_1$)</td><td class="p-1.5 font-semibold text-amber-900">Tăng thẳng $C_{1,\\text{eff}} \\implies$ Kéo $f_c \\uparrow$!</td></tr>
                    <tr><td class="p-1.5 font-bold text-sky-800 mono">VX (Đất ảo OTA)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">11.614 fF</td><td class="p-1.5 text-right mono">+1.45% ($C_2$)</td><td class="p-1.5">Giảm nhẹ hệ số hồi tiếp $\\beta$ &amp; $f_c$</td></tr>
                    <tr><td class="p-1.5 font-semibold mono">VOUT (Ngõ ra)</td><td class="p-1.5 text-right mono">11.389 fF</td><td class="p-1.5 text-right mono">~1.1% ($C_L$)</td><td class="p-1.5">Nằm chung tải $C_L=1\\text{ pF}$, hầu như vô hại</td></tr>
                    <tr><td class="p-1.5 font-semibold mono">PHI1 / PHI1B</td><td class="p-1.5 text-right mono">6.613 / 7.285 fF</td><td class="p-1.5 text-right mono">Nối dây Clock</td><td class="p-1.5">Làm $t_r/t_f$ chậm lại ~50–75 ps</td></tr>
                    <tr><td class="p-1.5 font-semibold mono">PHI2 / PHI2B</td><td class="p-1.5 text-right mono">8.414 / 6.173 fF</td><td class="p-1.5 text-right mono">Ghép $1.6\\text{ fF} \\to V_X$</td><td class="p-1.5">Gây lệch DC thêm $-3.55\\text{ mV}$ tại ngõ ra</td></tr>
                    <tr><td class="p-1.5 font-semibold mono">VD1 / VTAIL (OTA)</td><td class="p-1.5 text-right mono">13.78 / 59.30 fF</td><td class="p-1.5 text-right mono">Nội bộ 36 ngón</td><td class="p-1.5">Hạ nhẹ GBW $43.6 \\to 42.9\\text{ MHz}$</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            """,
            next_question="Chỉ nhìn vào 2 con số tụ ký sinh mới lộ diện tại $V_1$ ($+6.57\\%$) và $V_X$ ($+1.45\\%$), ta có thể <strong>dùng công thức giấy đoán trước chính xác</strong> tần số cắt Post-PEX mà chưa cần đợi SPICE chạy xong không?",
            footer_text=f_foot,
            speaker_notes="Thống kê chi tiết 123 tụ ghép PEX tổng cộng 284.191 fF và vai trò riêng của từng nút.",
        ),

        # S11: ANALYTICAL PEX SHIFT PREDICTION VS MEASURED FFT/PARASITICS
        SlideSpec(
            act_tag="Hồi III — Chứng Minh Toán Học Khớp Đo Đạc PEX",
            title="Dự Đoán Giải Tích $+5.04\\%$ vs. Thực Đo PEX $+4.89\\%$ (Khớp Tới $0.15\\%$)!",
            badge="Physics Verified 0.15%",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_3col_fft_and_parasitics.png" alt="3-Col FFT and Parasitics Breakdown" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_3col_fft_and_parasitics.png:</span> Trái: Phân bố tụ ký sinh từng nút; Phải: Phổ FFT 3 cột (Golden vs. Pre vs. Post-PEX $53.60\\text{ dB}$).
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Công thức Dự đoán Dịch cực PEX</div>
                  <p class="text-xs text-sky-950 mt-1">Với mạch SC có tụ ký sinh phụ thêm ở cả $V_1$ và $V_X$:</p>
                  <div class="bg-white border border-amber-300 rounded p-2 mt-1 text-center text-xs font-bold text-sky-950">
                    $$\\frac{f_{c,\\text{PEX}}}{f_{c,\\text{Pre}}} \\approx \\frac{1 + C_{p,V1}/C_1}{1 + C_{p,VX}/C_2} = \\frac{1.06569}{1.01452} = +5.04\\%$$
                  </div>
                </div>
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Thực đo từ Netlist Ngspice PEX</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Ngspice đo thực tế: $f_{c,\\text{PEX}} = \\mathbf{203.453\\text{ kHz}}$ (so với Pre $193.972\\text{ kHz}$ là <strong class="text-sky-700">$+4.89\\%$</strong> — chỉ lệch $0.15\\%$ so với nhẩm tay!) và phổ giữ vững <span class="mono font-bold">SFDR = $53.60\\text{ dB}$</span>!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Trước khi chốt kết quả toàn mạch, ta hãy rà soát từng khối con một (<span class='code-tag'>clk, tg, ota_5t</span>) sau khi đã “đeo ba lô ký sinh dây” xem có khối nào bị đuối sức không?",
            footer_text=f_foot,
            speaker_notes="Kết hợp phép tính phân số 1.06569 / 1.01452 = +5.04% khớp kỳ diệu với thực đo +4.89% từ PEX.",
        ),

        # S12: SUB-BLOCKS PRE VS POST-PEX
        SlideSpec(
            act_tag="Hồi III — Kiểm Tra Lại 4 Khối Đơn Vị Sau Trích Xuất PEX",
            title="Hiệu Năng 4 Khối Con Pre-Layout vs. Post-Layout PEX: Vững Vàng Trên Silicon",
            badge="Sub-Blocks Post-PEX: PASS",
            badge_tone="blue",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_unit_blocks_pre_vs_post.png" alt="Unit Blocks Pre vs Post-PEX" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_unit_blocks_pre_vs_post.png:</span> Đường so trực tiếp Pre-Layout vs. Post-Layout PEX cho Clock $t_{\\text{nov}}$, Khóa TG $R_{\\text{on}}(V)$ &amp; Bode 5T-OTA.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2">
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold text-sky-800 mono">1. Clock (non_overlap_clk)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">$t_{\\text{nov}}$ tăng từ $3.12/3.09\\text{ ns} \\to \\mathbf{3.81/3.73\\text{ ns}}$ (vẫn lọt đẹp vùng $[2,5]\\text{ ns}$!); $t_r/t_f$: $217.8/295.5\\text{ ps}$.</p>
                </div>
                <div class="gold-card py-2">
                  <div class="text-xs font-bold text-amber-800 mono">2. Khóa TG (tg_switch nf=2)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">$R_{\\text{on}}(V_{\\text{CM}})=\\mathbf{4.566\\text{ k}\\Omega} &lt; 5\\text{ k}\\Omega$ (đỉnh $5.059\\text{ k}\\Omega$ do $2W_{\\text{INT}}$); $\\tau=505.9\\text{ ps}$, vẫn nạp $91.3\\tau$ mỗi bán chu kỳ!</p>
                </div>
                <div class="ocean-card py-2">
                  <div class="text-xs font-bold text-sky-800 mono">3. Khuếch đại 5T-OTA (36 ngón)</div>
                  <p class="text-[11.5px] text-sky-950 mt-0.5">$A_{OL}$ giữ nguyên $\\mathbf{41.62\\text{ dB}}$, $\\text{GBW}$ hạ nhẹ $43.61 \\to \\mathbf{42.87\\text{ MHz}}$, $\\text{PM}=\\mathbf{80.45^\\circ}$, 5/5 MOS bão hòa ($+136.8\\text{ mV} \\dots +970.7\\text{ mV}$).</p>
                </div>
              </div>
            </div>
            """,
            next_question="Từng khối riêng lẻ sau PEX vẫn giữ phong độ đỉnh cao — bây giờ hãy nhìn vào cửa sổ chạy mô phỏng toàn mạch <span class='code-tag'>top_sc_lpf_pex.spice</span> thực tế trên máy trạm EDA!",
            footer_text=f_foot,
            speaker_notes="Tất cả các khối con sau PEX đều ổn định và duy trì biên độ an toàn cao.",
        ),

        # S13: LIVE PEX WORKSTATION CAPTURE
        SlideSpec(
            act_tag="Hồi III — Môi Trường Chạy Netlist Post-Layout PEX Thực Tế",
            title="Buồng Chạy PEX Toàn Mạch (<span class='code-tag'>top_sc_lpf_pex.spice</span>): Nạp Đủ 123 Tụ Vào BSIM4",
            badge="PEX Co-Simulation",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_gui_pex_workstation.png" alt="Live PEX Workstation Light Mode" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_gui_pex_workstation.png:</span> Magic layout phía trái, terminal log trích xuất PEX + Ngspice ở giữa, và sóng Ngspice Post-Layout sắc nét!
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Quy trình Tự động Hóa Tuần 4</div>
                  <ol class="text-xs text-sky-950 mt-1 space-y-1.5 list-decimal pl-4">
                    <li>Mở file <span class="code-tag">top_sc_lpf.mag</span>, trích xuất <span class="code-tag">ext2spice lvs</span> để chạy Netgen.</li>
                    <li>Chạy <span class="code-tag">ext2spice cthresh 0</span> xuất netlist có đầy đủ 123 tụ ghép $C_{ij}$ + tụ xuống nền.</li>
                    <li>Nạp vào cùng hai bàn đo <span class="code-tag">tb_top_sc_lpf</span> &amp; <span class="code-tag">tb_top_bode</span> như Tuần 3 để đảm bảo phép so sánh <strong>công bằng tuyệt đối (Apples-to-Apples)</strong>!</li>
                  </ol>
                </div>
                <div class="gold-card py-2.5 text-xs text-sky-950">
                  <strong>Giá trị của quy trình này:</strong> Không đoán mò độ suy giảm sau layout — toàn bộ kết quả dưới đây đến trực tiếp từ chính file GDSII chuẩn bị gửi Fab!
                </div>
              </div>
            </div>
            """,
            next_question="Đặt cả 3 đường cong: <strong>Golden Model (Tuần 2)</strong>, <strong>Pre-Layout (Tuần 3)</strong> và <strong>Post-Layout PEX (Tuần 4)</strong> lên cùng một đồ thị Thời gian &amp; Bode — chúng khác nhau những gì?",
            footer_text=f_foot,
            speaker_notes="Minh họa trực tiếp môi trường chạy trích xuất và mô phỏng PEX trên Workstation nền sáng.",
        ),

        # S14: 3-COL TIME & BODE OVERLAY
        SlideSpec(
            act_tag="Hồi IV — Đối Chiếu 3 Cấp Độ Thiết Kế Trên Miền Thời Gian &amp; Tần Số",
            title="Đồ Thị 3 Cột (Golden vs. Pre-Layout vs. Post-Layout PEX): Sóng Bậc Thang &amp; Bode",
            badge="3-Tier Correlation",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-4 items-center">
              <div class="col-span-8 fig-frame">
                <img src="figs/w4_3col_time_and_bode.png" alt="3-Col Time and Bode" class="max-h-[385px] w-auto object-contain rounded" />
                <p class="text-[11px] text-sky-900 mt-1.5 font-medium text-center">
                  <span class="mono font-bold text-sky-700">w4_3col_time_and_bode.png:</span> Đường sóng bậc thang &amp; 11 điểm Bode chồng khít: <span class="mono font-bold">187.675 → 193.972 → 203.453 kHz</span>.
                </p>
              </div>
              <div class="col-span-4 flex flex-col gap-2.5">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Nhận xét Đường Sóng Thời Gian</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Dạng sóng ra <span class="code-tag">VOUT</span> của Post-PEX vẫn giữ độ trễ pha mượt mà, hầu như không bị quá vọt (overshoot) nhờ $\\text{PM} = 80.45^\\circ$ cực vững. Suy giảm biên thông dải chỉ <span class="mono font-bold text-sky-700">−0.104 dB</span>!
                  </p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Nhận xét Đáp ứng Bode &amp; Đánh giá Gate 4</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Tại dải chặn tần số cao (&gt;$1\\text{ MHz}$), độ dốc suy giảm $-20\\text{ dB/dec}$ bảo toàn nguyên vẹn. Sai lệch PEX so Pre là <strong>$+4.89\\%$ (&lt; $5\\%$)</strong>, khẳng định chất lượng Layout!
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Tần số cắt dịch $+4.89\\%$ ta đã giải mã xong — thế còn sự dịch chuyển áp một chiều ở ngõ ra (từ $-1.90\\text{ mV}$ lên $-5.51\\text{ mV}$) xuất phát từ đâu và sửa cho lần Tape-out thứ 2 ra sao?",
            footer_text=f_foot,
            speaker_notes="Phân tích đồ thị 3 cột Golden, Pre-Layout và Post-Layout PEX trong miền thời gian và tần số.",
        ),

        # S15: DC SHIFT DIAGNOSIS & RESPIN PRE-DISTORTION
        SlideSpec(
            act_tag="Hồi IV — Chẩn Đoán DC Offset &amp; Chiến Lược Tiền Bù Tape-Out Lần 2",
            title="Giải Mã DC Shift $-5.51\\text{ mV}$ &amp; Bí Quyết Pre-Distortion Kéo $f_c$ Về Đúng $187.7\\text{ kHz}$",
            badge="Respin Engineering Tip",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 ieee-card py-3.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono">1. Giải phẫu Nguồn Gốc Độ Lệch $-5.51\\text{ mV}$ Ngõ Ra</div>
                <p class="text-xs text-sky-950 mt-1.5 leading-relaxed">
                  Ở Tuần 3, tổng lệch DC là $-1.90\\text{ mV}$ (chủ yếu do $-1.85\\text{ mV}$ offset hệ thống của 5T-OTA). Sang Post-Layout PEX, nó tăng thêm $-3.55\\text{ mV}$ lên thành <strong>$-5.51\\text{ mV}$</strong>. Thủ phạm là gì?
                </p>
                <div class="ocean-card mt-2.5 py-2.5 text-xs text-sky-950">
                  <strong>Thủ phạm — Ghép Xuyên Âm Dây Clock ($\\Delta C_{\\text{clk}-V_X} \\approx 1.6\\text{ fF}$):</strong>
                  <p class="mt-1">Đường dây kim loại của <span class="code-tag">PHI2</span> và <span class="code-tag">PHI2B</span> chạy song song gần nút ảo $V_X$ có độ chênh tụ ghép $1.6\\text{ fF}$. Mỗi chu kỳ tắt pha $\\Phi_2$, tụ ký sinh này kéo nhẹ một điện tích lệch $\\Delta Q = 1.6\\text{ fF}\\times 1.8\\text{ V}$ tích lên $C_2$:</p>
                  <div class="text-center font-bold mono text-sky-800 mt-1">$\\Delta V_{\\text{DC,wire}} \\approx -3.55\\text{ mV} \\ (0.197\\%\\text{ của } V_{DD})$</div>
                </div>
              </div>

              <div class="col-span-6 gold-card py-3.5">
                <div class="text-xs font-bold uppercase text-amber-800 mono">2. Khuyến Nghị Tinh Chỉnh Tape-Out Lần 2 (Pre-Distortion)</div>
                <ul class="mt-2 space-y-2 text-xs text-sky-950 list-disc pl-4 leading-relaxed">
                  <li><strong>Tiền bù chính xác chiều dài $C_1$ (Pre-Distortion):</strong> Ta biết Layout chắc chắn cộng thêm $+6.57\\text{ fF}$ vào nút $V_1$. Vì vậy chỉ cần rút ngắn chiều dài tụ MIM $C_1$ từ $L_{\\text{eff}} = 10.0 \\to \\mathbf{9.0\\ \\mu\\text{m}}$ (giảm chủ động $C_1$ xuống $\\sim 90\\text{ fF}$): khi cộng ký sinh $6.57\\text{ fF}$ vào sẽ chạm sát mức chuẩn!</li>
                  <li><strong>Cân bằng dây bọc chắn Clock:</strong> Đi đường <span class="code-tag">PHI2</span> và <span class="code-tag">PHI2B</span> đối xứng chéo qua nút $V_X$ để triệt tiêu $1.6\\text{ fF}$ chênh lệch.</li>
                  <li><strong>Giữ $nf=1$ cho khóa nhỏ:</strong> Thu hồi mức $R_{\\text{on}}(0.9\\text{ V}) = 3.71\\text{ k}\\Omega$.</li>
                </ul>
              </div>
            </div>
            """,
            next_question="Còn một thông số sống còn của chip thương mại: tổng công suất tiêu thụ thực tế sau khi gánh 123 tụ ký sinh dây là bao nhiêu micro-Watt?",
            footer_text=f_foot,
            speaker_notes="Đưa ra kiến thức thiết kế Analog cao cấp: dùng Pre-Distortion rút tụ C1 xuống 9.0 um để bù ngược ký sinh PEX.",
        ),

        # S16: POWER BUDGET POST-PEX
        SlideSpec(
            act_tag="Hồi IV — Phân Tích Công Suất Thực Post-Layout (@1.8 V)",
            title="Công Suất Đo Thực Post-PEX: <span class='code-tag-gold'>116.06 µW</span> ($64.48\\ \\mu\\text{A}$ @ $1.8\\text{ V}$)",
            badge="Low-Power Verified",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5 items-center">
              <div class="col-span-6 ocean-card py-4">
                <div class="text-xs font-bold uppercase text-sky-800 mono">Thống kê Dòng điện Trung bình Toàn chip ($V_{DD}=1.8\\text{ V}$)</div>
                <div class="grid grid-cols-2 gap-3 mt-3">
                  <div class="bg-white border border-sky-200 rounded-xl p-3 text-center">
                    <div class="text-[11px] font-bold text-sky-800 uppercase">Pre-Layout (Tuần 3)</div>
                    <div class="text-2xl font-extrabold text-sky-700 mono mt-1">107.56 µW</div>
                    <div class="text-xs text-sky-900 mt-0.5">$I_{DD,\\text{avg}} = 59.76\\ \\mu\\text{A}$</div>
                  </div>
                  <div class="bg-amber-50 border border-amber-400 rounded-xl p-3 text-center">
                    <div class="text-[11px] font-bold text-amber-800 uppercase">Post-PEX (Tuần 4)</div>
                    <div class="text-2xl font-extrabold text-amber-800 mono mt-1">116.06 µW</div>
                    <div class="text-xs text-sky-900 mt-0.5">$I_{DD,\\text{avg}} = 64.48\\ \\mu\\text{A}$</div>
                  </div>
                </div>
                <p class="text-xs text-sky-950 mt-3 leading-relaxed">
                  <strong>Ý nghĩa vật lý của phần tăng $+8.50\\ \\mu\\text{W}$ ($+4.72\\ \\mu\\text{A}$):</strong> Chính xác là công suất động $P_{\\text{dyn}} = f_{\\text{clk}} \\cdot C_{\\text{wire,clk}} \\cdot V_{DD}^2$ dùng để nạp–xả hàng chục femto-Farad tụ dây trên các đường xung nhịp $10\\text{ MHz}$!
                </p>
              </div>

              <div class="col-span-6 gold-card py-4">
                <div class="text-xs font-bold uppercase text-amber-800 mono">Phân tích Hiệu suất Tiêu thụ &amp; So sánh</div>
                <ul class="mt-2.5 space-y-2 text-sm text-sky-950 list-disc pl-4">
                  <li><strong>Phần lõi Tĩnh (5T-OTA + Phân cực):</strong> Dòng đuôi $I_{\\text{tail}} = 28.17\\ \\mu\\text{A}$ + nhánh chuẩn $I_{\\text{ref}} = 30.0\\ \\mu\\text{A}$ hoạt động liên tục hạng A ở $1.8\\text{ V}$ để đảm bảo $\\text{GBW} &gt; 42\\text{ MHz}$.</li>
                  <li><strong>Phần lõi Động (Clock $10\\text{ MHz}$ + Đóng cắt):</strong> Chưa tới $15\\text{–}20\\ \\mu\\text{W}$ nhờ tối ưu <span class="code-tag">TG 2/6</span> và rút gọn <span class="code-tag">inv_cell</span>!</li>
                  <li>Ở mức <strong>$0.116\\text{ mW}$</strong> toàn chip, mạch hoàn toàn đáp ứng yêu cầu cảm biến IoT/y sinh chạy pin công suất cực thấp.</li>
                </ul>
              </div>
            </div>
            """,
            next_question="Tất cả các phép đo từ Golden Model, Pre-Layout đến Post-Layout PEX đã nằm trên bàn — hãy tổng kết toàn bộ vào <strong>Bảng Ma Trận Đối Chiếu 3 Cột</strong> của Gate Tuần 4!",
            footer_text=f_foot,
            speaker_notes="Đối chiếu công suất tĩnh và công suất động $C V^2 f$ tăng thêm +8.5 uW do tụ dây xung nhịp sau PEX.",
        ),

        # S17: 3-COLUMN MASTER GATE 4 TABLE
        SlideSpec(
            act_tag="Hồi IV — Nghiệm Thu Chính Thức Cổng Kiểm Định Tuần 4 (Verification Gate 4)",
            title="Bảng Ma Trận Đối Chiếu 3 Cột Chính Thức: Golden vs. Pre-Layout vs. Post-Layout PEX",
            badge="Gate 4 Sign-Off: PASSED",
            badge_tone="gold",
            body_html="""
            <div class="ieee-card py-2">
              <table class="ieee-table text-[11.5px]">
                <thead>
                  <tr>
                    <th class="p-1.5 text-left">Thông số Kỹ thuật (Spec)</th>
                    <th class="p-1.5 text-right">Golden (Tuần 2)</th>
                    <th class="p-1.5 text-right">Pre-Layout (Tuần 3)</th>
                    <th class="p-1.5 text-right">Post-PEX (Tuần 4)</th>
                    <th class="p-1.5 text-center">Nhận xét / Trạng thái</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="row-gold"><td class="p-1.5 font-bold">Tần số cắt $-3\\text{ dB}$ ($f_c$)</td><td class="p-1.5 text-right font-bold mono">187.675 kHz</td><td class="p-1.5 text-right font-bold text-sky-700 mono">193.972 kHz (+3.36%)</td><td class="p-1.5 text-right font-extrabold text-amber-800 mono">203.453 kHz (+4.89% Pre)</td><td class="p-1.5 text-center"><span class="badge-gold">PASS (khớp +5.04%) ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">Suy hao thông dải (@39 kHz)</td><td class="p-1.5 text-right mono">−0.184 dB</td><td class="p-1.5 text-right mono">−0.244 dB</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−0.288 dB (Δ=−0.104)</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">SFDR (512-pt Coherent FFT)</td><td class="p-1.5 text-right mono">149.50 dB (math)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">54.14 dB</td><td class="p-1.5 text-right font-bold text-sky-700 mono">53.60 dB (Δ=−0.54 dB)</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">THD (%)</td><td class="p-1.5 text-right mono">−146.07 dB</td><td class="p-1.5 text-right mono">−53.67 dB (0.207%)</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−52.85 dB (0.228%)</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">ENOB hiệu dụng (bits)</td><td class="p-1.5 text-right mono">23.96 bits</td><td class="p-1.5 text-right mono">8.62 bits</td><td class="p-1.5 text-right font-bold text-sky-700 mono">8.49 bits (Δ=−0.13 b)</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">Hài bậc cao ($HD_2 / HD_3 / HD_4$)</td><td class="p-1.5 text-right mono">&lt; −146 dBc</td><td class="p-1.5 text-right mono">−54.1 / −59.1 / —</td><td class="p-1.5 text-right font-bold text-sky-700 mono">−53.47 / −57.83 / −67.83</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">DC Shift (@$V_{\\text{CM}}=0.9\\text{ V}$)</td><td class="p-1.5 text-right mono">0.00 mV</td><td class="p-1.5 text-right mono">−1.90 mV</td><td class="p-1.5 text-right mono">−5.51 mV (0.3% VDD)</td><td class="p-1.5 text-center"><span class="badge-ocean">Chẩn đoán xong ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">Clock $t_{\\text{nov}}$ &amp; Khóa $R_{\\text{on}}(V_{\\text{CM}})$</td><td class="p-1.5 text-right mono">[2,5] ns / &lt;5 kΩ</td><td class="p-1.5 text-right mono">3.12 ns / 3.713 kΩ</td><td class="p-1.5 text-right font-bold text-sky-700 mono">3.81 ns / 4.566 kΩ</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr><td class="p-1.5 font-semibold">OTA ($A_{OL} / \\text{GBW} / \\text{PM}$)</td><td class="p-1.5 text-right mono">&gt;35 / &gt;10M / ≥60°</td><td class="p-1.5 text-right mono">41.62 / 43.61M / 81.05°</td><td class="p-1.5 text-right font-bold text-sky-700 mono">41.62 / 42.87M / 80.45°</td><td class="p-1.5 text-center"><span class="badge-ocean">PASS ✓</span></td></tr>
                  <tr class="row-gold"><td class="p-1.5 font-bold">Công suất ($V_{DD}=1.8\\text{ V}$) • DRC/LVS</td><td class="p-1.5 text-right mono">—</td><td class="p-1.5 text-right mono">107.56 µW (59.8 µA)</td><td class="p-1.5 text-right font-extrabold text-amber-800 mono">116.06 µW • DRC=0 / LVS ✓</td><td class="p-1.5 text-center"><span class="badge-gold">TAPE-OUT READY ✓</span></td></tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Nhìn lại cả một tháng làm việc từ con số 0 ở Tuần 1 đến bản vẽ GDSII sạch sẽ hôm nay — điều gì là mạch nối xuyên suốt tạo nên thành công của dự án SKY130-SC-LPF?",
            footer_text=f_foot,
            speaker_notes="Bảng đối chiếu 3 cột toàn diện từ metrics_comparison.json — minh chứng không thể chối cãi cho chất lượng dự án.",
        ),

        # S18: 4-WEEK CLOSED-LOOP JOURNEY
        SlideSpec(
            act_tag="Tổng Kết Dự Án — Chuỗi Kiểm Chứng Khép Kín 4 Tuần",
            title="Hành Trình Trọn Vẹn 4 Tuần: Từ Phương Trình Sai Phân $H(z)$ Đến Silicon GDSII",
            badge="Closed-Loop Flow",
            badge_tone="blue",
            body_html="""
            <div class="flex flex-col gap-3">
              <div class="fig-frame py-2">
                __SVG_ROADMAP__
              </div>
              <div class="grid grid-cols-3 gap-4">
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold text-sky-800 uppercase mono">1. Triết lý Verification-First</div>
                  <p class="text-xs text-sky-950 mt-1">Không bao giờ phỏng đoán cảm tính: mỗi bước đều có thước đo số từ Python Golden và Cổng Kiểm Định định lượng.</p>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold text-amber-800 uppercase mono">2. Kỷ luật Vật lý Sky130A</div>
                  <p class="text-xs text-sky-950 mt-1">Từ $kT/C$, ký sinh nút $V_1$ ($22.7\\text{ fF}$), đến hiệu ứng $W_{\\text{INT}}$ &amp; dự đoán PEX $+5.04\\%$ — mọi con số đều cắt nghĩa rạch ròi theo BSIM4.</p>
                </div>
                <div class="ocean-card py-2.5">
                  <div class="text-xs font-bold text-sky-800 uppercase mono">3. Sẵn sàng Bảo vệ &amp; Tape-Out</div>
                  <p class="text-xs text-sky-950 mt-1">Trọn bộ 9 file Xschem chuẩn IEEE, 10 cell Magic GDSII (0 DRC, 10/10 LVS), và quy trình Ngspice tái lập tự động 100%.</p>
                </div>
              </div>
            </div>
            """.replace("__SVG_ROADMAP__", _svg_w4_closing_roadmap()),
            next_question="Kết thúc hành trình 4 tuần — kính mời Hội đồng &amp; Quý đồng nghiệp đặt câu hỏi phản biện kỹ thuật (Q&amp;A)!",
            footer_text=f_foot,
            speaker_notes="Tóm tắt chu trình thiết kế vi mạch analog chuẩn mực quốc tế qua 4 tuần.",
        ),

        # S19: FINALE Q&A
        SlideSpec(
            act_tag="",
            title="",
            badge="",
            badge_tone="ocean",
            is_cover=True,
            body_html="""
            <div class="flex items-center justify-between border-b-2 border-sky-200 pb-3 relative z-10">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-md bg-sky-600 text-white text-xs font-bold tracking-widest uppercase mono">SKY130-SC-LPF • TAPE-OUT DEFENSE</span>
                <span class="text-sky-900 text-sm font-semibold mono">SkyWater 130nm (sky130A) • Open-Source EDA Flow</span>
              </div>
              <span class="px-3 py-1 rounded-full bg-amber-100 border border-amber-400 text-amber-900 text-xs font-bold mono">ALL 4 VERIFICATION GATES PASSED ✓</span>
            </div>

            <div class="my-auto py-4 text-center relative z-10">
              <p class="text-amber-700 font-bold tracking-widest uppercase text-xs mono mb-2">Thank You For Your Attention</p>
              <h1 class="text-[48px] font-extrabold tracking-tight text-sky-950 leading-tight">
                Trân Trọng Cảm Ơn &amp;<br />
                <span class="text-sky-600">Phiên Thảo Luận Kỹ Thuật (Q&amp;A)</span>
              </h1>
              <p class="text-sky-900 text-base mt-3 max-w-3xl mx-auto">
                Toàn bộ dữ liệu mô phỏng Python, Schematic Xschem chuẩn IEEE, Layout GDSII, báo cáo DRC/LVS &amp; Post-Layout PEX đều sẵn sàng trình diễn trực tiếp.
              </p>

              <div class="grid grid-cols-4 gap-4 mt-8 text-left">
                <div class="ocean-card p-3.5">
                  <div class="text-[11px] font-bold text-sky-800 uppercase mono">Tuần 1 • Lý thuyết</div>
                  <div class="text-base font-extrabold text-sky-950 mt-1">Gate 1 PASS</div>
                  <div class="text-xs text-sky-900 mt-0.5">$f_{c,\\text{SC}} = 187.675\\text{ kHz}$</div>
                </div>
                <div class="gold-card p-3.5">
                  <div class="text-[11px] font-bold text-amber-800 uppercase mono">Tuần 2 • Python</div>
                  <div class="text-base font-extrabold text-amber-900 mt-1">Gate 2 PASS</div>
                  <div class="text-xs text-sky-900 mt-0.5">$kT/C$ $72.09\\text{ dB}$, $g_m/I_D$</div>
                </div>
                <div class="ocean-card p-3.5">
                  <div class="text-[11px] font-bold text-sky-800 uppercase mono">Tuần 3 • Xschem</div>
                  <div class="text-base font-extrabold text-sky-950 mt-1">Gate 3 PASS</div>
                  <div class="text-xs text-sky-900 mt-0.5">$193.97\\text{ kHz}$ ($+3.36\\%$)</div>
                </div>
                <div class="gold-card p-3.5">
                  <div class="text-[11px] font-bold text-amber-800 uppercase mono">Tuần 4 • GDSII/PEX</div>
                  <div class="text-base font-extrabold text-amber-900 mt-1">Gate 4 PASS</div>
                  <div class="text-xs text-sky-900 mt-0.5">DRC=0 • LVS=0 • $116.1\\ \\mu\\text{W}$</div>
                </div>
              </div>
            </div>
            """,
            next_question="Mời dùng thanh điều hướng phía góc dưới bên trái để nhảy nhanh về bất kỳ tuần nào (Tuần 1 / Tuần 2 / Tuần 3 / Tuần 4) khi trả lời câu hỏi Hội đồng!",
            footer_text="SKY130-SC-LPF Master Deck • Generated with IEEE White-Ocean-Yellow Engine",
            speaker_notes="Kết thúc trọn bộ 4 tuần thuyết trình. Giữ phím N để xem ghi chú hoặc dùng nút điều hướng tuần ở góc trái dưới.",
        ),
    ]
