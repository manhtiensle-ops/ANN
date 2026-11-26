#!/usr/bin/env python3
"""Slide specifications for Week 1 (20 slides) and Week 2 (20 slides) — White/Blue/Gold theme."""
from __future__ import annotations

from slide_theme import (
    SlideSpec,
    svg_defs,
    svg_nand2,
    svg_nmos,
    svg_not,
    svg_pmos,
    svg_tg,
)


def _svg_w1_s11_clk() -> str:
    """Block 1 non_overlap_clk with true IEEE NAND2 and NOT gate symbols + waveform."""
    return f"""
    <svg viewBox="0 0 640 278" class="w-full h-[256px]">
      {svg_defs()}
      <text x="320" y="14" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">
        Kiến trúc Chốt Chéo NAND2 + Chuỗi Trễ NOT Chuẩn IEEE (Break-Before-Make)
      </text>

      <!-- Input CLK & XINV0 -->
      <text x="16" y="88" font-size="11" font-weight="800" fill="#0C4A6E">CLK</text>
      <line x1="42" y1="84" x2="72" y2="84" stroke="#0284C7" stroke-width="2" />
      <circle cx="56" cy="84" r="3" fill="#0369A1" />
      <path d="M 56 84 L 56 36 L 146 36" fill="none" stroke="#0284C7" stroke-width="1.8" />
      {svg_not(92, 84, scale=0.65, label="NOT", name="XINV0")}
      <line x1="120" y1="84" x2="146" y2="84" stroke="#0284C7" stroke-width="1.8" />

      <!-- Cross-coupled NAND2 gates -->
      {svg_nand2(174, 46, scale=0.72, label="NAND2", name="XNAND_A")}
      {svg_nand2(174, 94, scale=0.72, label="NAND2", name="XNAND_B")}

      <!-- Feedback wires between branches -->
      <line x1="210" y1="46" x2="236" y2="46" stroke="#0284C7" stroke-width="1.8" />
      <line x1="210" y1="94" x2="236" y2="94" stroke="#0284C7" stroke-width="1.8" />

      <!-- 6-stage delay chains shown cleanly as NOT -> [4x NOT] -> NOT -->
      {svg_not(258, 46, scale=0.58, label="", name="DA1")}
      <rect x="290" y="32" width="66" height="28" rx="6" fill="#FFFBEB" stroke="#D97706" stroke-width="1.6" />
      <text x="323" y="43" text-anchor="middle" font-size="8.8" font-weight="800" fill="#B45309">4× NOT</text>
      <text x="323" y="55" text-anchor="middle" font-size="8.2" font-weight="700" fill="#78350F">L = 0.95 µm</text>
      <line x1="278" y1="46" x2="290" y2="46" stroke="#0284C7" stroke-width="1.8" />
      <line x1="356" y1="46" x2="368" y2="46" stroke="#0284C7" stroke-width="1.8" />
      {svg_not(390, 46, scale=0.58, label="", name="DA6")}

      {svg_not(258, 94, scale=0.58, label="", name="DB1")}
      <rect x="290" y="80" width="66" height="28" rx="6" fill="#FFFBEB" stroke="#D97706" stroke-width="1.6" />
      <text x="323" y="91" text-anchor="middle" font-size="8.8" font-weight="800" fill="#B45309">4× NOT</text>
      <text x="323" y="103" text-anchor="middle" font-size="8.2" font-weight="700" fill="#78350F">L = 0.95 µm</text>
      <line x1="278" y1="94" x2="290" y2="94" stroke="#0284C7" stroke-width="1.8" />
      <line x1="356" y1="94" x2="368" y2="94" stroke="#0284C7" stroke-width="1.8" />
      {svg_not(390, 94, scale=0.58, label="", name="DB6")}

      <!-- Cross feedback taps -->
      <circle cx="422" cy="46" r="3" fill="#D97706" />
      <path d="M 422 46 L 422 65 L 136 65 L 136 86 L 146 86" fill="none" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,2" />
      <circle cx="430" cy="94" r="3" fill="#0369A1" />
      <path d="M 430 94 L 430 73 L 142 73 L 142 54 L 146 54" fill="none" stroke="#0369A1" stroke-width="1.5" stroke-dasharray="4,2" />

      <!-- Complementary output buffers -->
      <line x1="414" y1="46" x2="454" y2="46" stroke="#0284C7" stroke-width="1.8" />
      {svg_not(476, 46, scale=0.58, label="", name="BUF1A")}
      <circle cx="510" cy="46" r="2.8" fill="#0369A1" />
      <path d="M 510 46 L 510 24 L 584 24" fill="none" stroke="#0369A1" stroke-width="1.8" />
      <text x="590" y="28" font-size="10.5" font-weight="800" fill="#0369A1">Φ₁</text>
      {svg_not(542, 46, scale=0.58, label="", name="BUF1B")}
      <text x="590" y="50" font-size="10.5" font-weight="800" fill="#0284C7">Φ₁_b</text>

      <line x1="414" y1="94" x2="454" y2="94" stroke="#0284C7" stroke-width="1.8" />
      {svg_not(476, 94, scale=0.58, label="", name="BUF2A")}
      <circle cx="510" cy="94" r="2.8" fill="#D97706" />
      <path d="M 510 94 L 510 116 L 584 116" fill="none" stroke="#D97706" stroke-width="1.8" />
      <text x="590" y="120" font-size="10.5" font-weight="800" fill="#B45309">Φ₂</text>
      {svg_not(542, 94, scale=0.58, label="", name="BUF2B")}
      <text x="590" y="98" font-size="10.5" font-weight="800" fill="#D97706">Φ₂_b</text>

      <!-- Timing Waveform below -->
      <line x1="36" y1="132" x2="616" y2="132" stroke="#BAE6FD" stroke-width="1.2" />
      <text x="48" y="168" text-anchor="end" font-size="12" font-weight="800" fill="#0369A1">Φ₁</text>
      <path d="M 60 182 L 84 182 L 92 144 L 296 144 L 304 182 L 560 182 L 568 144 L 604 144" fill="none" stroke="#0369A1" stroke-width="2.6" />
      <rect x="92" y="144" width="204" height="38" fill="#E0F2FE" opacity="0.6" />
      <text x="194" y="167" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0369A1">t_on ≈ 47 ns (Nạp C₁)</text>

      <text x="48" y="230" text-anchor="end" font-size="12" font-weight="800" fill="#D97706">Φ₂</text>
      <path d="M 60 244 L 330 244 L 338 206 L 534 206 L 542 244 L 604 244" fill="none" stroke="#D97706" stroke-width="2.6" />
      <rect x="338" y="206" width="196" height="38" fill="#FEF3C7" opacity="0.7" />
      <text x="436" y="229" text-anchor="middle" font-size="10.5" font-weight="700" fill="#B45309">t_on ≈ 47 ns (Chia sẻ C₁∥C₂)</text>

      <rect x="304" y="140" width="34" height="110" fill="#FEF3C7" opacity="0.75" />
      <line x1="304" y1="138" x2="304" y2="254" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,2" />
      <line x1="338" y1="138" x2="338" y2="254" stroke="#D97706" stroke-width="1.5" stroke-dasharray="4,2" />
      <text x="321" y="268" text-anchor="middle" font-size="11" font-weight="800" fill="#B45309">Khoảng chết t_nov = 2–3 ns (Cả TG1 &amp; TG2 đều TẮT)</text>
    </svg>
    """


def _svg_w1_s14_ota() -> str:
    """Block 4 5T-OTA schematic with true IEEE NMOS & PMOS transistor symbols."""
    return f"""
    <svg viewBox="0 0 380 288" class="w-full h-[250px]">
      <!-- VDD Rail -->
      <line x1="55" y1="20" x2="310" y2="20" stroke="#D97706" stroke-width="2.8" />
      <text x="182" y="13" text-anchor="middle" font-size="11.5" font-weight="800" fill="#B45309">VDD = 1.8 V</text>
      <line x1="115" y1="20" x2="115" y2="38" stroke="#78350F" stroke-width="2" />
      <line x1="255" y1="20" x2="255" y2="38" stroke="#78350F" stroke-width="2" />

      <!-- M3 (left, flipped so gate faces right) and M4 (right, gate faces left) -->
      {svg_pmos(123, 64, flip=True, name="M3", size_txt="16/0.8")}
      {svg_pmos(247, 64, flip=False, name="M4", size_txt="16/0.8")}
      <!-- Mirror gate tie & M3 diode tie -->
      <line x1="149" y1="64" x2="221" y2="64" stroke="#D97706" stroke-width="2" />
      <circle cx="170" cy="64" r="3.2" fill="#D97706" />
      <line x1="170" y1="64" x2="170" y2="100" stroke="#D97706" stroke-width="1.8" />
      <line x1="115" y1="100" x2="170" y2="100" stroke="#D97706" stroke-width="1.8" />
      <circle cx="115" cy="100" r="3.2" fill="#0C4A6E" />

      <!-- Vertical links M3->M1 and M4->M2 -->
      <line x1="115" y1="90" x2="115" y2="124" stroke="#0C4A6E" stroke-width="2" />
      <line x1="255" y1="90" x2="255" y2="124" stroke="#0C4A6E" stroke-width="2" />
      <!-- Output VOUT -->
      <circle cx="255" cy="107" r="4" fill="#0284C7" />
      <line x1="255" y1="107" x2="332" y2="107" stroke="#0284C7" stroke-width="2.4" />
      <text x="336" y="111" font-size="11.5" font-weight="800" fill="#0369A1">Vout</text>

      <!-- Differential pair M1 (gate left) and M2 (gate right) -->
      {svg_nmos(107, 150, flip=False, name="M1", size_txt="32/0.8")}
      {svg_nmos(263, 150, flip=True, name="M2", size_txt="32/0.8")}
      <line x1="56" y1="150" x2="83" y2="150" stroke="#0284C7" stroke-width="2" />
      <text x="52" y="154" text-anchor="end" font-size="11" font-weight="800" fill="#0369A1">Vx (+)</text>
      <line x1="287" y1="150" x2="322" y2="150" stroke="#0284C7" stroke-width="2" />
      <text x="326" y="154" font-size="11" font-weight="800" fill="#0369A1">Vout (−)</text>

      <!-- Common Tail VTAIL -->
      <line x1="115" y1="176" x2="115" y2="196" stroke="#0C4A6E" stroke-width="2" />
      <line x1="255" y1="176" x2="255" y2="196" stroke="#0C4A6E" stroke-width="2" />
      <line x1="115" y1="196" x2="255" y2="196" stroke="#0C4A6E" stroke-width="2" />
      <circle cx="185" cy="196" r="3.5" fill="#0C4A6E" />
      <text x="200" y="191" font-size="10" font-weight="700" fill="#0369A1">Vtail</text>

      <!-- Tail NMOS M5 -->
      <line x1="185" y1="196" x2="185" y2="210" stroke="#0C4A6E" stroke-width="2" />
      {svg_nmos(177, 236, flip=False, name="M5", size_txt="24/1.0")}
      <line x1="118" y1="236" x2="153" y2="236" stroke="#0284C7" stroke-width="2" />
      <text x="112" y="240" text-anchor="end" font-size="11" font-weight="800" fill="#0369A1">Vbias</text>

      <!-- VSS Ground -->
      <line x1="185" y1="262" x2="185" y2="274" stroke="#0C4A6E" stroke-width="2" />
      <line x1="166" y1="274" x2="204" y2="274" stroke="#0C4A6E" stroke-width="2.5" />
      <text x="185" y="286" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0C4A6E">VSS = 0 V</text>
    </svg>
    """


def _svg_w1_s15_top() -> str:
    """Top-level 4-block architecture using IEEE NAND2/NOT, CMOS TG bow-tie, and OTA triangle."""
    return f"""
    <svg viewBox="0 0 1100 282" class="w-full h-[258px]">
      {svg_defs()}
      <!-- Block 1: Clock Generator Box with mini NAND2/NOT icons -->
      <rect x="20" y="12" width="265" height="96" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.2" />
      <text x="152" y="34" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0369A1">1. non_overlap_clk (10 MHz)</text>
      {svg_nand2(95, 62, scale=0.46, label="")}
      {svg_not(165, 62, scale=0.46, label="")}
      <text x="232" y="66" text-anchor="middle" font-size="11" font-weight="700" fill="#B45309">t_nov = 2–3 ns</text>
      <text x="152" y="96" text-anchor="middle" font-size="11" font-weight="600" fill="#0C4A6E">Xuất 4 pha: Φ₁, Φ₁_b, Φ₂, Φ₂_b</text>

      <path d="M 285 48 L 405 48 L 405 130" fill="none" stroke="#0284C7" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arr-blue)" />
      <path d="M 285 76 L 590 76 L 590 130" fill="none" stroke="#D97706" stroke-width="2" stroke-dasharray="5,3" marker-end="url(#arr-gold)" />
      <text x="355" y="40" font-size="11.5" font-weight="800" fill="#0369A1">Φ₁, Φ₁_b</text>
      <text x="538" y="68" font-size="11.5" font-weight="800" fill="#B45309">Φ₂, Φ₂_b</text>

      <!-- INPUT -->
      <rect x="88" y="144" width="136" height="52" rx="10" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2" />
      <text x="156" y="166" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">INPUT Vin(t)</text>
      <text x="156" y="185" text-anchor="middle" font-size="10.5" fill="#78350F">0.9 V ± 0.4 V</text>
      <line x1="224" y1="170" x2="368" y2="170" stroke="#0284C7" stroke-width="2.4" marker-end="url(#arr-blue)" />

      <!-- TG1 Bow-Tie -->
      {svg_tg(405, 170, scale=1.08, title="2. TG1 (Φ₁)", sub="Ron < 5 kΩ")}
      <line x1="433" y1="170" x2="554" y2="170" stroke="#0284C7" stroke-width="2.4" />
      <circle cx="496" cy="170" r="4" fill="#0C4A6E" />
      <text x="480" y="156" font-size="11" font-weight="800" fill="#0369A1">V₁</text>
      <line x1="496" y1="170" x2="496" y2="218" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="478" y1="218" x2="514" y2="218" stroke="#0369A1" stroke-width="3.2" />
      <line x1="478" y1="228" x2="514" y2="228" stroke="#0369A1" stroke-width="3.2" />
      <line x1="496" y1="228" x2="496" y2="256" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="484" y1="256" x2="508" y2="256" stroke="#0C4A6E" stroke-width="2" />
      <text x="466" y="232" text-anchor="end" font-size="12" font-weight="800" fill="#0C4A6E">3. C₁ = 100 fF</text>
      <text x="466" y="248" text-anchor="end" font-size="10.5" fill="#0369A1">(1× MIM)</text>

      <!-- TG2 Bow-Tie -->
      {svg_tg(590, 170, scale=1.08, title="2. TG2 (Φ₂)", sub="Ron < 5 kΩ")}
      <line x1="618" y1="170" x2="770" y2="170" stroke="#0284C7" stroke-width="2.4" marker-end="url(#arr-blue)" />
      <circle cx="696" cy="170" r="4" fill="#0C4A6E" />
      <text x="696" y="156" text-anchor="middle" font-size="12" font-weight="800" fill="#0369A1">Vx</text>
      <line x1="696" y1="170" x2="696" y2="218" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="676" y1="218" x2="716" y2="218" stroke="#0369A1" stroke-width="3.2" />
      <line x1="676" y1="228" x2="716" y2="228" stroke="#0369A1" stroke-width="3.2" />
      <line x1="696" y1="228" x2="696" y2="256" stroke="#0C4A6E" stroke-width="2.2" />
      <line x1="684" y1="256" x2="708" y2="256" stroke="#0C4A6E" stroke-width="2" />
      <text x="724" y="232" text-anchor="start" font-size="12" font-weight="800" fill="#0C4A6E">3. C₂ = 800 fF</text>
      <text x="724" y="248" text-anchor="start" font-size="10.5" fill="#0369A1">(8× MIM + Dummy)</text>

      <!-- Block 4: 5T-OTA Triangle -->
      <polygon points="776,112 776,248 932,180" fill="#FFFBEB" stroke="#D97706" stroke-width="2.4" />
      <text x="791" y="176" font-size="15" font-weight="800" fill="#0C4A6E">+</text>
      <text x="791" y="210" font-size="15" font-weight="800" fill="#0C4A6E">−</text>
      <text x="836" y="176" text-anchor="middle" font-size="13.5" font-weight="800" fill="#B45309">4. ota_5t</text>
      <text x="836" y="194" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0369A1">A_OL &gt; 40 dB</text>
      <text x="836" y="210" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0369A1">PM ≥ 60°</text>

      <line x1="932" y1="180" x2="984" y2="180" stroke="#0284C7" stroke-width="2.6" marker-end="url(#arr-blue)" />
      <circle cx="958" cy="180" r="4" fill="#0C4A6E" />
      <path d="M 958 180 L 958 268 L 750 268 L 750 205 L 776 205" fill="none" stroke="#D97706" stroke-width="2.2" />

      <rect x="990" y="152" width="100" height="56" rx="10" fill="#E0F2FE" stroke="#0284C7" stroke-width="2.2" />
      <text x="1040" y="176" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">OUTPUT</text>
      <text x="1040" y="195" text-anchor="middle" font-size="10.5" font-weight="600" fill="#0C4A6E">Vout (1 pF)</text>
    </svg>
    """


def _svg_w1_s17_ltv() -> str:
    return f"""
    <svg viewBox="0 0 460 112" class="w-full h-[104px]">
      <text x="230" y="16" text-anchor="middle" font-size="11.5" font-weight="800" fill="#B45309">
        Trạng thái đóng băng tĩnh tại t = 0 của thuật toán .ac
      </text>
      <text x="26" y="64" font-size="12" font-weight="800" fill="#0C4A6E">Vin</text>
      <line x1="56" y1="58" x2="96" y2="58" stroke="#0284C7" stroke-width="2.4" />
      {svg_tg(132, 58, scale=0.82, title="TG1 ĐÓNG", sub="~1.7 kΩ")}
      <line x1="162" y1="58" x2="232" y2="58" stroke="#0C4A6E" stroke-width="2.2" />
      <circle cx="198" cy="58" r="3.5" fill="#0C4A6E" />
      <line x1="198" y1="58" x2="198" y2="90" stroke="#0C4A6E" stroke-width="2" />
      <text x="198" y="104" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">C₁</text>
      <rect x="232" y="38" width="112" height="40" rx="8" fill="#FEF3C7" stroke="#D97706" stroke-width="2" stroke-dasharray="4,3" />
      <text x="288" y="55" text-anchor="middle" font-size="10.5" font-weight="800" fill="#B45309">TG2 HỞ MÃI MÃI!</text>
      <text x="288" y="70" text-anchor="middle" font-size="9.5" font-weight="600" fill="#78350F">R_off ~ 10¹¹ Ω</text>
      <line x1="344" y1="58" x2="395" y2="58" stroke="#94A3B8" stroke-width="2" stroke-dasharray="4,3" />
      <text x="424" y="63" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0369A1">C₂ (Cô lập)</text>
    </svg>
    """


def get_week1_slides() -> list[SlideSpec]:
    f_foot = "SKY130-SC-LPF • Tuần 1: Lý Thuyết, Cầu Nối Tín Hiệu &amp; Hệ Thống $\\to$ Vi Mạch"
    return [
        # S01: COVER
        SlideSpec(
            act_tag="",
            title="",
            badge="",
            badge_tone="ocean",
            is_cover=True,
            section_id="w1-start",
            body_html="""
            <div class="flex items-center justify-between border-b-2 border-sky-200 pb-3 relative z-10">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-md bg-sky-600 text-white text-xs font-bold tracking-widest uppercase mono">IEEE / ISSCC DESIGN DECK</span>
                <span class="text-sky-900 text-sm font-semibold mono">SkyWater 130nm (sky130A) • Nguồn đơn 1.8 V</span>
              </div>
              <span class="px-3 py-1 rounded-full bg-amber-100 border border-amber-400 text-amber-900 text-xs font-bold mono">TUẦN 01 / 04 — LÝ THUYẾT &amp; KIẾN TRÚC</span>
            </div>

            <div class="my-auto py-1 relative z-10">
              <p class="text-amber-700 font-bold tracking-wider uppercase text-xs mono mb-1.5">Top-Down 3-Tier Analog IC Design • sky130-sc-lpf</p>
              <h1 class="text-[44px] font-extrabold tracking-tight leading-tight text-sky-950 max-w-5xl">
                Mạch Lọc Thông Thấp Tụ Chuyển Mạch<br />
                <span class="text-sky-600">Trên Tiến Trình SkyWater 130nm</span>
              </h1>
              <p class="text-sky-900 text-base mt-3 max-w-4xl">
                Báo cáo chuyên sâu Tuần 1: Dẫn xuất liền mạch từ <strong class="text-amber-800">Vấn đề vật lý đầu thu</strong> $\\rightarrow$ <strong class="text-sky-700">Lý thuyết Tín hiệu &amp; Hệ thống quyết định thông số</strong> $\\rightarrow$ <strong class="text-sky-950">Hiện thực Vi mạch 4 khối &amp; Kiểm định ổn định</strong>.
              </p>

              <div class="grid grid-cols-5 gap-3 mt-7">
                <div class="gold-card p-3.5">
                  <div class="text-amber-800 text-[11px] font-bold mono uppercase">Hồi I • Slide 02–03</div>
                  <div class="text-sm font-extrabold text-sky-950 mt-1">Bài Toán &amp; Đối Tượng</div>
                  <div class="text-sky-900/80 text-xs mt-1">Lỗi Aliasing ADC &amp; chân dung tín hiệu thực.</div>
                </div>
                <div class="ocean-card p-3.5">
                  <div class="text-sky-700 text-[11px] font-bold mono uppercase">Hồi II • Slide 04–09</div>
                  <div class="text-sm font-extrabold text-sky-950 mt-1">S&amp;S → Thông Số Chip</div>
                  <div class="text-sky-900/80 text-xs mt-1">Dẫn xuất $f_c, f_{\\text{clk}}, K=8, kT/C, \\text{PM}\\ge 60^\\circ$.</div>
                </div>
                <div class="ieee-card border-sky-400 p-3.5">
                  <div class="text-sky-700 text-[11px] font-bold mono uppercase">Hồi III • Slide 10–14</div>
                  <div class="text-sm font-extrabold text-sky-950 mt-1">Vi Mạch Sky130A</div>
                  <div class="text-sky-900/80 text-xs mt-1">PVT MIM, CLK, khóa TG, ký sinh &amp; 5T-OTA.</div>
                </div>
                <div class="gold-card p-3.5">
                  <div class="text-amber-800 text-[11px] font-bold mono uppercase">Hồi IV • Slide 15–16</div>
                  <div class="text-sm font-extrabold text-sky-950 mt-1">Sản Phẩm &amp; I/O</div>
                  <div class="text-sky-900/80 text-xs mt-1">Sơ đồ 4 khối chuẩn IEEE, INPUT &amp; OUTPUT.</div>
                </div>
                <div class="ocean-card p-3.5">
                  <div class="text-sky-700 text-[11px] font-bold mono uppercase">Hồi V • Slide 17–20</div>
                  <div class="text-sm font-extrabold text-sky-950 mt-1">Kiểm Định Ổn Định</div>
                  <div class="text-sky-900/80 text-xs mt-1">LTI vs LPTV, 22/22 SI &amp; Chốt Gate 1.</div>
                </div>
              </div>
            </div>
            """,
            next_question="Mọi con chip tương tự đều bắt đầu từ một sự cố vật lý của tín hiệu thực tế — vậy hệ thống thu đang gặp rủi ro gì?",
            footer_text="Principal Analog IC Architect • Phím N bật Speaker Notes • Ctrl+P xuất PDF",
            speaker_notes="Báo cáo Tuần 1 theo mạch 5 Hồi từ trên xuống: Hồi I đặt bài toán nhiễu tại đầu thu; Hồi II dùng Tín hiệu & Hệ thống dẫn xuất từng thông số chip; Hồi III hiện thực hóa 4 khối trên sky130A; Hồi IV đặc tả INPUT/OUTPUT; Hồi V chứng minh kiểm định ổn định LTI/LPTV và chốt Gate 1.",
        ),

        # S02: WHY LPF
        SlideSpec(
            act_tag="Hồi I (Tầng 1) — Bối Cảnh Hệ Thống &amp; Lý Do Chọn LPF",
            title="Tại Sao Chuỗi Thu Mixed-Signal Bắt Buộc Cần Mạch Lọc Thông Thấp?",
            badge="Tầng 1: Physical Problem",
            badge_tone="gold",
            body_html="""
            <div class="ieee-card py-2.5 px-4">
              <svg viewBox="0 0 1120 176" class="w-full h-[168px]">
                __SVG_DEFS__
                <rect x="12" y="30" width="214" height="114" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2" />
                <text x="119" y="56" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">1. Nguồn Hạ Tần / Cảm Biến</text>
                <text x="119" y="78" text-anchor="middle" font-size="11.5" fill="#0C4A6E">RF Downconverter / MEMS</text>
                <text x="119" y="104" text-anchor="middle" font-size="12" font-weight="800" fill="#0284C7">Tín hiệu đích: ≤ 50 kHz</text>
                <text x="119" y="124" text-anchor="middle" font-size="11" fill="#B45309">Lẫn nhiễu mạnh ≥ 2 MHz</text>
                <line x1="226" y1="87" x2="266" y2="87" stroke="#0284C7" stroke-width="2.4" marker-end="url(#arr-blue)" />

                <rect x="272" y="20" width="245" height="134" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
                <text x="394" y="45" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">2. Tín Hiệu Thô Chưa Lọc</text>
                <path d="M 294 94 Q 308 62, 322 90 T 350 66 T 378 100 T 406 118 T 434 90 T 462 68 T 496 94" fill="none" stroke="#D97706" stroke-width="2.4" />
                <text x="394" y="138" text-anchor="middle" font-size="11" font-weight="700" fill="#78350F">Nhiễu cao tần bao vây dải thông</text>

                <path d="M 517 58 L 572 58 L 572 41 L 615 41" fill="none" stroke="#D97706" stroke-width="2.2" stroke-dasharray="5,3" marker-end="url(#arr-gold)" />
                <rect x="622" y="10" width="484" height="60" rx="10" fill="#FEF3C7" stroke="#D97706" stroke-width="2" />
                <text x="864" y="34" text-anchor="middle" font-size="13" font-weight="800" fill="#92400E">✗ Nếu thiếu LPF trước ADC</text>
                <text x="864" y="55" text-anchor="middle" font-size="12" fill="#78350F">Gập phổ (Aliasing) đè lên 50 kHz + Quá tải biên độ (Clipping ADC)</text>

                <path d="M 517 114 L 572 114 L 572 130 L 615 130" fill="none" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />
                <rect x="622" y="92" width="215" height="74" rx="11" fill="#0369A1" stroke="#F59E0B" stroke-width="2.2" />
                <text x="729" y="121" text-anchor="middle" font-size="14" font-weight="800" fill="#FEF3C7">Lá Chắn SC-LPF</text>
                <text x="729" y="144" text-anchor="middle" font-size="11.5" fill="#E0F2FE">Giữ dải thấp • Triệt nhiễu cao</text>

                <line x1="837" y1="130" x2="873" y2="130" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />
                <rect x="880" y="92" width="226" height="74" rx="11" fill="#E0F2FE" stroke="#0284C7" stroke-width="2.2" />
                <text x="993" y="121" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">✓ SAR-ADC → Xử Lý Số DSP</text>
                <text x="993" y="144" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Phổ sạch • Bảo toàn SNR</text>
              </svg>
            </div>

            <div class="grid grid-cols-2 gap-5">
              <div class="gold-card border-l-4 border-l-amber-500 py-3">
                <div class="text-xs font-bold uppercase text-amber-800 mono">Thảm họa 1 • Chồng phổ bất khả nghịch</div>
                <p class="text-sm text-sky-950 mt-1">
                  Một khi nhiễu $\\ge 2\\text{ MHz}$ đã gập vào dải $0\\text{–}50\\text{ kHz}$ sau lấy mẫu ADC, <strong>không bộ lọc số DSP nào tách lại được</strong>.
                </p>
              </div>
              <div class="ocean-card border-l-4 border-l-sky-600 py-3">
                <div class="text-xs font-bold uppercase text-sky-800 mono">Thảm họa 2 • Sập dải động (Desensitization)</div>
                <p class="text-sm text-sky-950 mt-1">
                  Gai nhiễu lớn cộng chồng lên tín hiệu làm kịch trần nguồn $1.8\\text{ V}$, gây méo xén đỉnh nghiêm trọng.
                </p>
              </div>
            </div>
            """.replace("__SVG_DEFS__", svg_defs()),
            next_question="Ta đã biết vì sao cần LPF — vậy chân dung định lượng cụ thể của đối tượng tín hiệu và nhiễu trên chip $1.8\\text{ V}$ là gì?",
            footer_text=f_foot,
            speaker_notes="LPF tương tự đặt ngay trước ADC nhằm ngăn chặn chồng phổ (Aliasing) bất khả nghịch của nhiễu >= 2 MHz và tránh bão hòa thang đo 1.8 V của ADC.",
        ),

        # S03: SIGNAL PROFILE
        SlideSpec(
            act_tag="Hồi I (Tầng 1) — Đặc Tả Đối Tượng Xử Lý",
            title="Chân Dung Tín Hiệu Đích, Nguồn Nhiễu &amp; Ràng Buộc Nguồn Đơn $1.8\\text{ V}$",
            badge="Signal &amp; Interferer Profile",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-3 gap-5">
              <div class="ieee-card border-t-4 border-t-sky-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Tín hiệu hữu ích (Passband)</span>
                  <h3 class="font-extrabold text-sky-950 text-lg mt-1">Băng Gốc $\\le 50\\text{ kHz}$</h3>
                  <ul class="mt-3 space-y-2 text-sm text-sky-900 list-disc pl-4">
                    <li><strong>Nguồn gốc:</strong> Ngõ ra Mixer BLE/IoT, cảm biến MEMS, siêu âm, DAC.</li>
                    <li><strong>Biên độ điển hình:</strong> $A_{\\text{sig}} = 0.30\\text{ V}_p$.</li>
                    <li><strong>Bảo toàn:</strong> Suy hao $\\le 0.5\\text{ dB}$, trễ nhóm phẳng không méo dạng.</li>
                  </ul>
                </div>
                <div class="mt-4 p-2 rounded-lg bg-sky-50 border border-sky-200 text-xs font-bold text-sky-800 text-center">
                  Mục tiêu: Giữ nguyên $\\ge 95\\%$ biên độ gốc
                </div>
              </div>

              <div class="gold-card border-t-4 border-t-amber-500 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">2. Tạp nhiễu (Stopband)</span>
                  <h3 class="font-extrabold text-sky-950 text-lg mt-1">Can Nhiễu $\\ge 2\\text{ MHz}$</h3>
                  <ul class="mt-3 space-y-2 text-sm text-sky-900 list-disc pl-4">
                    <li><strong>Nguồn gốc:</strong> Kênh vô tuyến lân cận, gợn nguồn xung DC–DC, hài clock số.</li>
                    <li><strong>Biên độ nhiễu:</strong> $A_{\\text{int}} \\approx 0.12\\text{ V}_p$.</li>
                    <li><strong>Triệt tiêu:</strong> Nén tối thiểu <strong>$\\ge 20\\text{ dB}$</strong> (giảm $\\ge 10\\times$ biên độ).</li>
                  </ul>
                </div>
                <div class="mt-4 p-2 rounded-lg bg-white border border-amber-300 text-xs font-bold text-amber-900 text-center">
                  Mục tiêu: Giảm công suất nhiễu $\\ge 100\\times$
                </div>
              </div>

              <div class="ocean-card border-t-4 border-t-blue-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-blue-700 mono">3. Dịch mức DC trên Chip</span>
                  <h3 class="font-extrabold text-sky-950 text-lg mt-1">$V_{DD}=1.8\\text{ V}, V_{CM}=0.9\\text{ V}$</h3>
                  <div class="bg-white border border-sky-200 rounded-lg p-2 my-2.5 text-center text-sm">
                    $$v_{\\text{in}}(t) = \\underbrace{0.9\\text{ V}}_{V_{CM}} + x_{\\text{sig}}(t) + x_{\\text{int}}(t)$$
                  </div>
                  <ul class="space-y-1.5 text-sm text-sky-900 list-disc pl-4">
                    <li>Tổng biên độ đỉnh $0.30 + 0.12 = 0.42\\text{ V}$.</li>
                    <li>Đặt $V_{CM} = V_{DD}/2 = \\mathbf{0.9\\text{ V}}$ tối ưu dải đối xứng $[0.5, 1.3]\\text{ V}$.</li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded-lg bg-white border border-sky-300 text-xs font-bold text-blue-800 text-center">
                  Tránh méo hài lẻ $\\text{HD}_3, \\text{HD}_5$ do Clipping
                </div>
              </div>
            </div>
            """,
            next_question="Từ hai mốc $50\\text{ kHz}$ ($\\le 0.5\\text{ dB}$) và $2\\text{ MHz}$ ($\\ge 20\\text{ dB}$), lý thuyết Tín hiệu &amp; Hệ thống tính ra bậc lọc $N$ và tần số cắt $f_c$ như thế nào?",
            footer_text=f_foot,
            speaker_notes="Tín hiệu hữu ích nằm ở <= 50 kHz (0.30 Vp), nhiễu >= 2 MHz (0.12 Vp). Vì chip chạy nguồn đơn 1.8 V, mọi tín hiệu phải dịch lên điểm giữa VCM = 0.9 V để dao động đối xứng.",
        ),

        # S04: S&S DERIVATION N=1 & fc WINDOW
        SlideSpec(
            act_tag="Hồi II (Tầng 2) — Tín Hiệu &amp; Hệ Thống Quyết Định Bậc Lọc &amp; $f_c$",
            title="Giải Bất Phương Trình Phổ: Vì Sao Chọn Bậc $N=1$ &amp; $f_c \\in [143.1, 201.0]\\text{ kHz}$?",
            badge="S&amp;S Spec Derivation #1",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-6 ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Chứng minh bậc lọc tối giản $N = 1$</span>
                  <p class="text-sm text-sky-900 mt-1.5">Khoảng chuyển tiếp tần số từ dải thông đến nhiễu:</p>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2.5 my-2.5 text-center">
                    $$\\Delta_{\\text{dec}} = \\log_{10}\\!\\left(\\frac{2\\text{ MHz}}{50\\text{ kHz}}\\right) = \\log_{10}(40) = \\mathbf{1.602\\text{ decade}}$$
                  </div>
                  <ul class="text-sm text-sky-900 space-y-1.5 list-disc pl-4">
                    <li>Lọc bậc $N=1$ dốc <strong>$-20\\text{ dB/dec}$</strong> $\\implies$ dư khả năng nén $\\ge 20\\text{ dB}$ trong $1.6\\text{ dec}$ mà chỉ cần đúng 1 OTA.</li>
                    <li>Hàm truyền chuẩn: $H(s) = \\frac{1}{1 + s/(2\\pi f_c)}$, $|H(jf)|^2 = \\frac{1}{1 + (f/f_c)^2}$.</li>
                  </ul>
                </div>
                <div class="mt-3 p-2.5 rounded-lg bg-amber-50 border border-amber-300 text-xs text-amber-950">
                  <strong>Lợi ích Tín hiệu &amp; Hệ thống:</strong> Không cực phức liên hợp $\\implies$ <strong>0% vọt lố nội tại</strong>, pha gần tuyến tính ($-14.9^\\circ$ tại $50\\text{ kHz}$).
                </div>
              </div>

              <div class="col-span-6 ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-700 mono">2. Giải hệ bất phương trình đóng khung $f_c$</span>
                  <div class="mt-2.5 space-y-2.5 text-sm">
                    <div class="p-2.5 rounded-lg bg-sky-50 border border-sky-200">
                      <strong class="text-sky-900">Cận dưới (Dải thông $50\\text{ kHz}$ suy hao $\\le 0.5\\text{ dB}$):</strong>
                      $$10\\log_{10}\\!\\left[1 + \\left(\\frac{50\\text{ kHz}}{f_c}\\right)^2\\right] \\le 0.5 \\implies \\mathbf{f_c \\ge 143.14\\text{ kHz}}$$
                    </div>
                    <div class="p-2.5 rounded-lg bg-amber-50 border border-amber-300">
                      <strong class="text-amber-900">Cận trên (Dải chắn $2\\text{ MHz}$ nén $\\ge 20\\text{ dB}$):</strong>
                      $$10\\log_{10}\\!\\left[1 + \\left(\\frac{2000\\text{ kHz}}{f_c}\\right)^2\\right] \\ge 20 \\implies \\mathbf{f_c \\le 201.01\\text{ kHz}}$$
                    </div>
                  </div>
                </div>
                <div class="mt-3 p-3 rounded-xl ocean-card text-center">
                  <div class="text-xs text-sky-800 uppercase font-bold mono">Miền nghiệm bắt buộc từ Tín hiệu &amp; Hệ thống</div>
                  <div class="text-base font-extrabold text-sky-950 mt-0.5">$$\\mathbf{143.14\\text{ kHz} \\;\\le\\; f_c \\;\\le\\; 201.01\\text{ kHz}}$$</div>
                </div>
              </div>
            </div>
            """,
            next_question="Đã khóa miền nghiệm $f_c \\in [143.1, 201.0]\\text{ kHz}$ — vậy khi rời rạc hóa theo thời gian, Định lý Nyquist bắt buộc chọn $f_{\\text{clk}}$ bằng bao nhiêu?",
            footer_text=f_foot,
            speaker_notes="Khoảng cách 50 kHz -> 2 MHz là 1.602 decade. Bậc N=1 dốc -20 dB/dec là đủ và đơn giản nhất. Giải hai bất phương trình biên độ khóa chặt fc vào [143.14, 201.01] kHz.",
        ),

        # S05: NYQUIST & f_clk = 10 MHz
        SlideSpec(
            act_tag="Hồi II (Tầng 2) — Định Lý Lấy Mẫu Nyquist &amp; Sự Tuần Hoàn Phổ",
            title="Tại Sao Phổ Tuần Hoàn $X_s(f)$ Ép Xung Nhịp Lấy Mẫu Tại $f_{\\text{clk}} = 10\\text{ MHz}$?",
            badge="S&amp;S Spec Derivation #2",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card py-2 px-4">
              <svg viewBox="0 0 1120 150" class="w-full h-[142px]">
                __SVG_DEFS__
                <line x1="50" y1="120" x2="1080" y2="120" stroke="#0C4A6E" stroke-width="2" />
                <line x1="70" y1="18" x2="70" y2="128" stroke="#0C4A6E" stroke-width="2" />
                <text x="58" y="28" text-anchor="end" font-size="11" font-weight="700" fill="#0C4A6E">0 dB</text>
                <text x="1086" y="124" font-size="12" font-weight="800" fill="#0C4A6E">f</text>

                <path d="M 70 28 Q 150 28, 195 63 Q 270 108, 515 114" fill="none" stroke="#0284C7" stroke-width="3" />
                <polygon points="70,120 70,32 135,32 135,120" fill="#BAE6FD" opacity="0.65" />
                <text x="112" y="22" text-anchor="middle" font-size="11" font-weight="800" fill="#0369A1">Dải thông (≤ fc)</text>
                <line x1="195" y1="63" x2="195" y2="120" stroke="#D97706" stroke-width="1.6" stroke-dasharray="4,3" />
                <text x="195" y="138" text-anchor="middle" font-size="11" font-weight="800" fill="#B45309">fc ≈ 188 kHz</text>

                <line x1="340" y1="84" x2="340" y2="120" stroke="#D97706" stroke-width="4" />
                <text x="340" y="76" text-anchor="middle" font-size="10.5" font-weight="700" fill="#B45309">Nhiễu 2 MHz (−20 dB)</text>
                <text x="340" y="138" text-anchor="middle" font-size="11" fill="#0C4A6E">2 MHz</text>

                <line x1="515" y1="20" x2="515" y2="120" stroke="#64748B" stroke-width="1.6" stroke-dasharray="5,4" />
                <text x="515" y="138" text-anchor="middle" font-size="11" font-weight="700" fill="#475569">f_Nyquist = 5 MHz</text>

                <path d="M 515 114 Q 760 108, 835 63 Q 880 28, 960 28 Q 1015 28, 1050 63" fill="none" stroke="#0284C7" stroke-width="3" />
                <polygon points="895,120 895,32 1015,32 1015,120" fill="#FEF3C7" opacity="0.85" />
                <line x1="960" y1="20" x2="960" y2="120" stroke="#0C4A6E" stroke-width="1.8" stroke-dasharray="4,3" />
                <text x="960" y="138" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0C4A6E">f_clk = 10 MHz</text>
                <text x="955" y="20" text-anchor="middle" font-size="11" font-weight="800" fill="#B45309">Cửa sổ Ảnh Aliasing (9.81–10.19 MHz)</text>

                <line x1="210" y1="50" x2="880" y2="50" stroke="#0284C7" stroke-width="2" marker-end="url(#arr-blue)" />
                <text x="545" y="43" text-anchor="middle" font-size="12" font-weight="800" fill="#0369A1">Khoảng cách an toàn OSR = 26.64 → Đẩy dải ảnh cách xa 9.81 MHz!</text>
              </svg>
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div class="gold-card border-l-4 border-l-amber-600 py-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold uppercase text-amber-900 mono">Nếu $f_{\\text{clk}} = 1\\text{ MHz}$</span>
                  <span class="badge-gold">Quá thấp</span>
                </div>
                <ul class="mt-2 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>$\\text{OSR} \\approx 2.6$: Ảnh chồng phổ sát ngay <strong>$812\\text{ kHz}$</strong>.</li>
                  <li>Góc rời rạc $\\Omega_c = \\omega_c T_{\\text{clk}} = 1.18\\text{ rad}$ gây <strong>méo tần số nặng</strong>.</li>
                </ul>
              </div>

              <div class="ocean-card border-2 border-sky-600 py-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold uppercase text-sky-800 mono">Chốt $f_{\\text{clk}} = 10\\text{ MHz}$</span>
                  <span class="badge-ocean">Nghiệm Vàng</span>
                </div>
                <ul class="mt-2 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>$\\text{OSR} = \\mathbf{26.64}$, góc nhỏ $\\Omega_c = \\mathbf{0.118\\text{ rad}} \\ll 1$ ($H(z) \\approx H(s)$).</li>
                  <li>Ảnh ở $9.81\\text{ MHz}$; bán chu kỳ $50\\text{ ns}$ thoải mái cho OTA.</li>
                </ul>
              </div>

              <div class="ieee-card border-l-4 border-l-amber-500 py-3">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Nếu $f_{\\text{clk}} = 100\\text{ MHz}$</span>
                  <span class="badge-gold">Lãng phí</span>
                </div>
                <ul class="mt-2 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>Phải tăng tỷ số tụ $C_2/C_1 = \\mathbf{80}$ $\\implies$ tốn diện tích MIM gấp $10\\times$.</li>
                  <li>Bán chu kỳ còn $5\\text{ ns}$ ép $\\text{GBW} &gt; 100\\text{ MHz}$ (đốt dòng lớn).</li>
                </ul>
              </div>
            </div>
            """.replace("__SVG_DEFS__", svg_defs()),
            next_question="Khi đã khóa $f_{\\text{clk}} = 10\\text{ MHz}$ và miền nghiệm $f_c \\in [143.1, 201.0]\\text{ kHz}$, tại sao tỷ số tụ nguyên bắt buộc phải là $K = C_2/C_1 = 8$?",
            footer_text=f_foot,
            speaker_notes="H(e^jwT) lặp lại tuần hoàn tại bội số f_clk. Chọn 10 MHz đạt OSR=26.64, đẩy dải ảnh ra 9.81 MHz mà chỉ cần tỷ số tụ 1:8 và bán chu kỳ 50 ns rất dễ thiết kế OTA.",
        ),

        # S06: DESIGN SPACE PLOT K=8
        SlideSpec(
            act_tag="Hồi II (Tầng 2 → Tầng 3) — Lượng Tử Hóa Tỷ Số Tụ Nguyên",
            title="Đồ Thị Không Gian Thiết Kế: Vì Sao Khóa Chặt Tỷ Số $K = C_2/C_1 = 8$?",
            badge="Exact Design Space Proof",
            badge_tone="ocean",
            body_html="""
            <div class="fig-frame">
              <img src="figs/week1_ss_spec_window.png" alt="Design space K=8" class="max-h-[330px] w-auto object-contain" />
            </div>
            <div class="grid grid-cols-3 gap-4">
              <div class="gold-card border-l-4 border-l-amber-600 py-2.5">
                <div class="text-xs font-bold uppercase text-amber-900 mono">1. Loại $K \\le 7$ &amp; $K \\ge 11$</div>
                <p class="text-xs text-sky-950 mt-1">$K=7$ cho nén $2\\text{ MHz} = \\mathbf{18.9\\text{ dB}} &lt; 20\\text{ dB}$ (trượt dải chắn); $K \\ge 11$ gây suy hao $50\\text{ kHz} &gt; 0.5\\text{ dB}$.</p>
              </div>
              <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono">2. Nghiệm tối ưu $K = 8$ ($\\alpha = 1/9$)</div>
                <p class="text-xs text-sky-950 mt-1">Đạt vừa khít <strong>$-20.02\\text{ dB}$</strong> tại $2\\text{ MHz}$, chỉ mất <strong>$-0.30\\text{ dB}$</strong> tại $50\\text{ kHz}$ với số ô tụ nhỏ nhất.</p>
              </div>
              <div class="ieee-card border-l-4 border-l-blue-600 py-2.5">
                <div class="text-xs font-bold uppercase text-blue-700 mono">3. Hình học Vàng $1 + 8 = 9 = 3\\times 3$</div>
                <p class="text-xs text-sky-950 mt-1">Đặt $C_1$ tại tâm $(2,2)$ và $8$ ô $C_2$ bao quanh tạo <strong>ma trận đối xứng tâm Common-Centroid</strong> triệt gradient!</p>
              </div>
            </div>
            """,
            next_question="Tại sao với $K = 8$ và $R_{\\text{eq}} = 1\\text{ M}\\Omega$, mạch $RC$ liên tục cắt ở $198.94\\text{ kHz}$ nhưng mạch tụ chuyển mạch lại cắt chính xác ở $187.675\\text{ kHz}$?",
            footer_text=f_foot,
            speaker_notes="Để ghép đôi chính xác <0.1%, K=C2/C1 phải là số nguyên. K=7 trượt 20 dB tại 2 MHz; K>=11 trượt 0.5 dB tại 50 kHz. K=8 vừa đạt chuẩn vừa cho tổng 9 ô tụ (3x3 đối xứng tâm hoàn hảo).",
        ),

        # S07: Z-DOMAIN H(z) & BACKWARD EULER
        SlideSpec(
            act_tag="Hồi II (Tầng 2) — Phương Trình Sai Phân &amp; Ánh Xạ Miền $\\mathcal{Z}$",
            title="Bảo Toàn Điện Tích 2 Pha, Ánh Xạ Backward-Euler &amp; Ổn Định BIBO",
            badge="Exact Z-Domain Model",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-6 ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Từ bảo toàn điện tích đến Phương trình sai phân</span>
                  <div class="mt-2 space-y-2 text-sm text-sky-950">
                    <div class="p-2 rounded-lg bg-sky-50 border border-sky-200">
                      <strong>Pha $\\Phi_1$ (Lấy mẫu):</strong> $Q_1^{(1)} = C_1 V_{\\text{in}}[n], \\quad Q_2^{(1)} = C_2 V_{\\text{out}}[n-1]$
                    </div>
                    <div class="p-2 rounded-lg bg-amber-50 border border-amber-200">
                      <strong>Pha $\\Phi_2$ (Chia sẻ $C_1 \\parallel C_2$):</strong> $(C_1 + C_2)V_{\\text{out}}[n] = C_1 V_{\\text{in}}[n] + C_2 V_{\\text{out}}[n-1]$
                    </div>
                  </div>
                  <p class="text-xs text-sky-900 mt-2">
                    Chia cho $T_{\\text{clk}}$: tương đương thay đạo hàm $s \\leftarrow \\frac{1 - z^{-1}}{T_{\\text{clk}}}$ (<strong>Ánh xạ Backward-Euler</strong> của mạch $RC$ có $\\tau = \\frac{C_2}{C_1}T_{\\text{clk}}$):
                  </p>
                </div>
                <div class="mt-2 p-2.5 rounded-xl ocean-card text-center">
                  <div class="text-xs text-sky-800 uppercase font-bold mono">Hàm truyền chính xác ($\\alpha = \\frac{C_1}{C_1+C_2} = \\frac{1}{9}$)</div>
                  $$H(z) = \\frac{\\alpha}{1 - (1-\\alpha)z^{-1}} = \\frac{1/9}{1 - \\frac{8}{9}z^{-1}}$$
                </div>
              </div>

              <div class="col-span-6 ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-700 mono">2. Giải chính xác $f_{c,\\text{SC}}$ &amp; Lý giải độ lệch $-5.66\\%$</span>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2 my-2 text-center text-sm">
                    $$\\left|H(e^{j\\omega_c T_{\\text{clk}}})\\right|^2 = \\frac{1}{2} \\implies \\cos(\\omega_c T_{\\text{clk}}) = 1 - \\frac{\\alpha^2}{2(1-\\alpha)} = \\frac{143}{144}$$
                  </div>
                  <div class="gold-card p-2 my-2 text-center">
                    $$f_{c,\\text{SC}} = \\frac{10\\text{ MHz}}{2\\pi}\\arccos\\!\\left(\\frac{143}{144}\\right) = \\mathbf{187.675\\text{ kHz}}$$
                  </div>
                </div>
                <div class="space-y-2 text-xs">
                  <div class="p-2 rounded-lg bg-amber-50 border border-amber-200 text-sky-950">
                    <strong class="text-amber-800">So sánh điểm cực:</strong> Mạch $RC$ liên tục có cực $p_{\\text{RC}} = e^{-1/8} = \\mathbf{0.8825}$ ($198.94\\text{ kHz}$), còn SC thụ động có cực $p_{\\text{SC}} = \\mathbf{8/9 = 0.8889}$ gần $z=1$ hơn $\\implies f_c$ giảm $-5.66\\%$.
                  </div>
                  <div class="p-2 rounded-lg bg-sky-50 border border-sky-200 text-sky-950">
                    <strong class="text-sky-800">Định lý ổn định BIBO:</strong> Cực duy nhất $|z_p| = \\frac{8}{9} &lt; 1$ nằm sâu trong vòng tròn đơn vị $\\implies \\sum |h[n]| &lt; \\infty$.
                  </div>
                </div>
              </div>
            </div>
            """,
            next_question="Hàm truyền $H(z)$ chỉ phụ thuộc tỷ số $C_2/C_1 = 8$ — vậy lý thuyết Tín hiệu Ngẫu nhiên nào quyết định giá trị tuyệt đối $C_1 = 100\\text{ fF}, C_2 = 800\\text{ fF}$ và chuẩn $\\text{PM} \\ge 60^\\circ$?",
            footer_text=f_foot,
            speaker_notes="Bảo toàn điện tích 2 pha cho ra hàm truyền Backward-Euler H(z) = (1/9)/(1 - (8/9)z^-1). Cực 8/9 > e^(-1/8) làm tần số cắt dịch xuống 187.675 kHz (-5.66%).",
        ),

        # S08: kT/C & 2ND ORDER STEP
        SlideSpec(
            act_tag="Hồi II (Tầng 2 → Tầng 3) — Phổ Nhiễu $kT/C$ &amp; Động Học Vòng Kín Bậc 2",
            title="Từ Băng Thông Nhiễu NEB &amp; Đáp Ứng Bậc 2 → Chốt $C_1, C_2$ &amp; $\\text{PM} \\ge 60^\\circ$",
            badge="S&amp;S Spec Derivation #3 &amp; #4",
            badge_tone="ocean",
            body_html="""
            <div class="fig-frame">
              <img src="figs/week1_ss_ota_noise_bridge.png" alt="kT/C and 2nd order step" class="max-h-[325px] w-auto object-contain" />
            </div>
            <div class="grid grid-cols-2 gap-5">
              <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono">1. Tích phân PSD nhiễu qua $\\text{NEB} = \\frac{1}{4 R_{\\text{on}} C}$</div>
                <p class="text-xs text-sky-950 mt-1">
                  $\\overline{v_{n,\\text{out}}^2} = \\int_0^\\infty 4k_B T R_{\\text{on}}|H|^2 df \\approx \\frac{k_B T}{C_2}$ (độc lập $R_{\\text{on}}$!). Chọn <strong>$C_1 = 100\\text{ fF}, C_2 = 800\\text{ fF}$</strong> cho $v_n = 72.0\\ \\mu\\text{V}_{\\text{rms}} \\implies \\mathbf{\\text{SNR} = 71.9\\text{ dB}}$ và ký sinh dây $&lt; 1.5\\%$.
                </p>
              </div>
              <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                <div class="text-xs font-bold uppercase text-amber-900 mono">2. Hệ bậc 2 vòng kín $\\beta=1$: $\\zeta = \\frac{1}{2}\\sqrt{f_{p2}/\\text{GBW}}$</div>
                <p class="text-xs text-sky-950 mt-1">
                  Nếu $\\text{PM} &lt; 45^\\circ$, đáp ứng bước nhảy rung mạnh trong cửa sổ $47\\text{ ns}$ làm sai mẫu. Bắt buộc <strong>$\\text{PM} \\ge 60^\\circ \\iff f_{p2} \\ge \\sqrt{3}\\,\\text{GBW}$</strong> để xác lập êm.
                </p>
              </div>
            </div>
            """,
            next_question="Hãy đặt toàn bộ các định lý Tín hiệu &amp; Hệ thống cạnh bảng thông số phần cứng để nhìn trọn bức tranh ánh xạ Tầng 2 $\\Longrightarrow$ Tầng 3.",
            footer_text=f_foot,
            speaker_notes="Nhiễu nhiệt kT/C quyết định cỡ tụ tuyệt đối C1=100 fF, C2=800 fF để đạt SNR >= 71.9 dB và thắng tụ ký sinh dây. Đáp ứng bậc 2 vòng kín buộc PM >= 60 độ để không rung vọt lố trong 47 ns.",
        ),

        # S09: MASTER MAPPING TABLE
        SlideSpec(
            act_tag="Hồi II Tổng Hợp — Cầu Nối Toàn Diện Tầng 2 ⟹ Tầng 3",
            title="Bảng Ánh Xạ Nhân Quả: Từ Lý Thuyết Tín Hiệu &amp; Hệ Thống Sang Thông Số Chip",
            badge="Zero Arbitrary Specs",
            badge_tone="gold",
            body_html="""
            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-xs">
                <thead>
                  <tr class="uppercase tracking-wider">
                    <th class="py-2.5 px-3.5 text-left">Bài toán Tín hiệu &amp; Hệ thống (Tầng 2)</th>
                    <th class="py-2.5 px-3.5 text-left">Phương trình / Ràng buộc Toán học</th>
                    <th class="py-2.5 px-3.5 text-left">Thông số Chip Khóa Cứng (Tầng 3)</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950 text-[12.5px]">
                  <tr>
                    <td class="py-2 px-3.5 font-semibold">Giữ $\\le 50\\text{ kHz}$ ($\\le 0.5\\text{ dB}$), cắt $2\\text{ MHz}$ ($\\ge 20\\text{ dB}$)</td>
                    <td class="py-2 px-3.5">$f_c \\in [143.1, 201.0]\\text{ kHz}$, Backward-Euler</td>
                    <td class="py-2 px-3.5 font-bold text-sky-700">Lọc bậc $N=1$, $K = C_2/C_1 = 8$ ($f_{c,\\text{SC}} = 187.67\\text{ kHz}$)</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-semibold">Chống chồng phổ (Aliasing) &amp; tránh méo góc $\\Omega_c$</td>
                    <td class="py-2 px-3.5">$\\text{OSR} = \\frac{f_{\\text{clk}}}{2 f_c} \\gg 1$, $\\Omega_c = 0.118\\text{ rad}$</td>
                    <td class="py-2 px-3.5 font-bold text-amber-800">$f_{\\text{clk}} = 10\\text{ MHz}$ (Ảnh xa ở $9.81\\text{ MHz}$, $T_{\\text{clk}}=100\\text{ ns}$)</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-semibold">Sàn nhiễu gập phổ $\\text{SNR} &gt; 70\\text{ dB}$ ($\\sim 11.6\\text{ bit}$)</td>
                    <td class="py-2 px-3.5">$\\overline{v_{n,\\text{out}}^2} = \\frac{k_B T}{C_2}$, $C_1 \\gg C_p$</td>
                    <td class="py-2 px-3.5 font-bold text-sky-900">$C_1 = 100\\text{ fF}, C_2 = 800\\text{ fF}$ ($v_n = 72\\ \\mu\\text{V}_{\\text{rms}}$, mảng $3\\times 3$)</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-semibold">Không rò mẫu &amp; triệt sai số xác lập / méo THD</td>
                    <td class="py-2 px-3.5">$\\Phi_1\\cdot\\Phi_2 = 0$; $\\epsilon_{\\text{set}} = e^{-t_{\\text{on}}/(R_{\\text{on}}C_1)} \\to 0$ ($94\\tau$)</td>
                    <td class="py-2 px-3.5 font-bold text-sky-700">$t_{\\text{nov}} \\in [2,5]\\text{ ns}$, khóa TG $R_{\\text{on}} &lt; 5\\text{ k}\\Omega$</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-semibold">Cách ly tải $C_L=1\\text{ pF}$, sai số DC $&lt;1\\%$, không rung</td>
                    <td class="py-2 px-3.5">$\\epsilon_A = \\frac{1}{1+A_{OL}} &lt; 1\\%$, $f_{p2} \\ge \\sqrt{3}\\,\\text{GBW}$</td>
                    <td class="py-2 px-3.5 font-bold text-amber-800">5T-OTA ($\\beta=1$): $A_{OL}&gt;40\\text{ dB}, \\text{GBW}&gt;10\\text{ MHz}, \\text{PM}\\ge 60^\\circ$</td>
                  </tr>
                  <tr class="row-gold">
                    <td class="py-2 px-3.5 font-semibold">Tránh xén đỉnh (Clipping $\\to \\text{HD}_3$) trên nguồn đơn</td>
                    <td class="py-2 px-3.5">$v_{\\text{in}}(t) = V_{CM} \\pm 0.42\\text{ V} \\subset [V_{\\min}, V_{\\max}]$</td>
                    <td class="py-2 px-3.5 font-bold text-amber-900">$V_{DD} = 1.8\\text{ V}, V_{SS} = 0\\text{ V}, V_{CM} = 0.9\\text{ V}$</td>
                  </tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Bộ thông số hệ thống đã được chứng minh trọn vẹn — bước vào Hồi III: hiện thực từng thông số này lên mặt phẳng Silicon Sky130A gặp thách thức gì?",
            footer_text=f_foot,
            speaker_notes="Mỗi con số của con chip đều xuất phát trực tiếp từ ràng buộc Tín hiệu & Hệ thống ở cột trái, hoàn toàn không có thông số cảm tính.",
        ),

        # S10: RC VS SC PVT
        SlideSpec(
            act_tag="Hồi III (Tầng 3) — Khối 3 (<span class=\"code-tag\">sc_core</span>) Trên Wafer Sky130A",
            title="Vì Sao Mạch $RC$ Phá Vỡ Cửa Sổ $f_c$ &amp; Giải Pháp Ô Tụ Đơn Vị MIM",
            badge="PVT Drift: 60.2% → 0.0%",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="flex items-center justify-between">
                    <h3 class="font-bold text-sky-950 text-sm">3 loại điện trở Poly trên <span class="code-tag-gold">sky130A</span></h3>
                    <span class="badge-gold">Vi phạm S&amp;S</span>
                  </div>
                  <ul class="mt-1.5 space-y-1 text-xs text-sky-950 list-disc pl-4">
                    <li><span class="code-tag">res_generic_po</span> ($48.2\\ \\Omega/\\square$): dài <strong>$7.26\\text{ mm}$</strong>.</li>
                    <li><span class="code-tag">res_high_po</span> ($357.9\\ \\Omega/\\square$): dài <strong>$978\\ \\mu\\text{m}$</strong>.</li>
                    <li><span class="code-tag">res_xhigh_po</span> ($2.58\\text{ k}\\Omega/\\square$): trôi $f_c$ từ $150.8\\text{ kHz}$ (<span class="code-tag">hh</span>) lên <strong>$270.6\\text{ kHz}$</strong> (<span class="code-tag">ll</span>, trượt chuẩn!).</li>
                  </ul>
                </div>

                <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                  <div class="flex items-center justify-between">
                    <h3 class="font-bold text-sky-950 text-sm">Ô tụ MIM chuẩn <span class="code-tag">cap_mim_m3_1</span></h3>
                    <span class="badge-ocean">Khóa cứng $f_c$</span>
                  </div>
                  <div class="bg-white rounded-lg p-1.5 my-1.5 text-center border border-sky-200 text-xs">
                    $$C_{\\text{unit}} = 2.0\\frac{\\text{fF}}{\\mu\\text{m}^2}(4.85+0.15)(9.85+0.15) = \\mathbf{100.000\\text{ fF}}$$
                  </div>
                  <ul class="space-y-1 text-xs text-sky-950 list-disc pl-4">
                    <li>Chẵn bước lưới Magic $0.05\\ \\mu\\text{m}$, tổng $9$ ô chỉ <strong>$450\\ \\mu\\text{m}^2$</strong>.</li>
                    <li>Tỷ số $1:8$ bất biến PVT ($\\mathbf{0.0\\%}$), mismatch cục bộ $&lt; 0.1\\%$.</li>
                  </ul>
                </div>
              </div>

              <div class="col-span-7 fig-frame">
                <img src="figs/week1_rc_vs_sc_pvt.png" alt="PVT Drift Comparison RC vs SC" class="max-h-[385px] w-auto object-contain" />
                <p class="text-xs text-sky-800 mt-1 mono">Số liệu đo Ngspice-47 trên 7 góc công nghệ &amp; nhiệt độ của PDK sky130A</p>
              </div>
            </div>
            """,
            next_question="Mảng tụ $1:8$ đã có — làm sao điều khiển hai pha lấy mẫu và chia sẻ điện tích mà tuyệt đối không bao giờ nối tắt $V_{\\text{in}}$ sang $C_2$?",
            footer_text=f_foot,
            speaker_notes="Điện trở Poly trên Sky130A có độ trôi PVT từ -24.2% đến +36.0% (tổng 60.2%), phá vỡ cửa sổ [143.1, 201.0] kHz. Tụ chuyển mạch MIM tỷ số 1:8 giữ độ trôi PVT = 0.0% và gọn chỉ 450 um2.",
        ),

        # S11: BLOCK 1 NON-OVERLAP CLK (IEEE NAND2 & NOT SVG)
        SlideSpec(
            act_tag="Hồi III (Tầng 3) — Khối 1 (<span class=\"code-tag\">non_overlap_clk</span>)",
            title="Xung Hai Pha Không Chồng Lấn: Bảo Vệ Định Luật Bảo Toàn Điện Tích",
            badge="$t_{\\text{nov}} \\in [2\\text{ ns}, 5\\text{ ns}]$",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-7 ieee-card py-2.5 px-3.5 flex flex-col justify-between">
                <div class="text-xs font-bold uppercase text-sky-800 mono mb-1">Chốt Chéo NAND2 + Chuỗi NOT Chuẩn IEEE &amp; Giản Đồ Thời Gian ($T_{\\text{clk}} = 100\\text{ ns}$)</div>
                __SVG_CLK__
              </div>
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">1. Cận dưới $t_{\\text{nov}} \\ge 2\\text{ ns}$</div>
                  <p class="text-sm text-sky-950 mt-1">Đảm bảo <span class="code-tag">TG1</span> khóa hẳn ($V_{GS} = 0$) trước khi <span class="code-tag">TG2</span> dẫn qua mọi góc nhanh/chậm PVT, giữ $\\Phi_1 \\cdot \\Phi_2 \\approx 0$.</p>
                </div>
                <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">2. Cận trên $t_{\\text{nov}} \\le 5\\text{ ns}$</div>
                  <p class="text-sm text-sky-950 mt-1">Không ăn lẹm quá $10\\%$ bán chu kỳ $50\\text{ ns}$, bảo toàn cửa sổ dẫn <strong>$t_{\\text{on}} \\ge 45\\text{–}47\\text{ ns}$</strong> cho tụ và OTA xác lập.</p>
                </div>
                <div class="ieee-card border-l-4 border-l-blue-600 py-2.5">
                  <div class="text-xs font-bold uppercase text-blue-700 mono">3. Đồng bộ 4 pha ($\\Phi, \\overline{\\Phi}$)</div>
                  <p class="text-sm text-sky-950 mt-1">Cân bằng sườn lên/xuống giữa $\\Phi_1$ và $\\overline{\\Phi_1}$ giúp NMOS và PMOS tắt đồng thời, tối ưu triệt <em>Clock Feedthrough</em>.</p>
                </div>
              </div>
            </div>
            """.replace("__SVG_CLK__", _svg_w1_s11_clk()),
            next_question="Trong cửa sổ hữu ích $t_{\\text{on}} = 47\\text{ ns}$ đó, khóa truyền dẫn CMOS <span class=\"code-tag\">tg_switch</span> phải có nội trở bao nhiêu để không làm méo hàm truyền $H(z)$?",
            footer_text=f_foot,
            speaker_notes="Sơ đồ sử dụng hai cổng NAND2 chốt chéo kết hợp chuỗi NOT kênh dài L=0.95 um để ấn định khoảng chết t_nov = 2-3 ns giữa Phi1 và Phi2, loại bỏ tuyệt đối dòng rò nối tắt Vin -> C2.",
        ),

        # S12: BLOCK 2 TG RON
        SlideSpec(
            act_tag="Hồi III (Tầng 3) — Khối 2 (<span class=\"code-tag\">tg_switch</span>) &amp; Méo Hài Động",
            title="Tại Sao Phải Ép $R_{\\text{on}} &lt; 5\\text{ k}\\Omega$ ($94\\tau$) Thay Vì $68\\text{ k}\\Omega$?",
            badge="Settling &amp; THD Immunity",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">1. Bẫy phi tuyến $R_{\\text{on}}(V_{\\text{in}}) \\to \\text{THD}$</div>
                  <p class="text-xs text-sky-950 mt-1">Nạp $99.9\\%$ chỉ cần $R_{\\text{on}} &lt; 68\\text{ k}\\Omega$ ($6.9\\tau$). Nhưng do $R_{\\text{on}}(V_{\\text{in}})$ biến thiên mạnh theo tín hiệu, nếu $\\tau$ lớn sẽ gây <strong>méo hài động $\\text{HD}_2, \\text{HD}_3$</strong>!</p>
                </div>
                <div class="ieee-card border-l-4 border-l-blue-600 py-2.5">
                  <div class="text-xs font-bold uppercase text-blue-700 mono">2. Đỉnh Body Effect trên <span class="code-tag">sky130A</span></div>
                  <p class="text-xs text-sky-950 mt-1">Tại $V_{CM}=0.9\\text{ V}$ ($V_{SB}=0.9\\text{ V}$), $V_{TH,n}$ tăng từ $0.74\\text{ V} \\to \\mathbf{0.866\\text{ V}}$ và $|V_{TH,p}| = \\mathbf{0.938\\text{ V}}$, tạo đỉnh nội trở tại $V_{\\text{in}} \\approx 0.965\\text{ V}$.</p>
                </div>
                <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">3. Chốt $W_n/W_p = 4/12\\ \\mu\\text{m}$ ($L = 0.15\\ \\mu\\text{m}$)</div>
                  <p class="text-xs text-sky-950 mt-1">Tỷ lệ $W_p/W_n = 3$ bù $\\mu_n/\\mu_p \\approx 2.7$: đạt $R_{\\text{on,max}} = \\mathbf{2.26\\text{ k}\\Omega}$ (góc <span class="code-tag">ss</span>: $4.53\\text{ k}\\Omega &lt; 5\\text{ k}\\Omega$), nạp đủ <strong>$94\\tau$</strong> ($e^{-94} \\approx 0$)!</p>
                </div>
              </div>
              <div class="col-span-7 fig-frame">
                <img src="figs/week1_tg_ron.png" alt="Sky130A TG Ron Sweep" class="max-h-[385px] w-auto object-contain" />
                <p class="text-xs text-sky-800 mt-1 mono">Quét DC Ngspice-47 trên dải tín hiệu $0.9 \\pm 0.4\\text{ V}$ (vùng tô xanh)</p>
              </div>
            </div>
            """,
            next_question="Tại sao không tăng vọt khóa TG lên $20/60\\ \\mu\\text{m}$ cho $R_{\\text{on}}$ càng nhỏ hơn nữa? Vì các tụ ký sinh Planar CMOS sẽ trừng phạt ta ngay lập tức!",
            footer_text=f_foot,
            speaker_notes="Hiệu ứng cực nền đẩy ngưỡng NMOS lên 0.866V và PMOS lên 0.938V quanh VCM=0.9V, tạo đỉnh Ron hình chuông. Ép Ron < 5 kOhm đạt 94 tau giúp xóa sạch méo hài động khi bám mẫu.",
        ),

        # S13: PLANAR PARASITICS & CI/CF
        SlideSpec(
            act_tag="Hồi III (Tầng 3) — Giới Hạn Vật Lý Bán Dẫn Planar 130nm",
            title="6 Tụ Ký Sinh, Charge Injection &amp; Cơ Chế Tự Triệt Clock Feedthrough",
            badge="BSIM4 Parasitic Audit",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-3 gap-4">
              <div class="ieee-card border-t-4 border-t-sky-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. 6 Tụ Ký Sinh MOSFET</span>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$C_{ox,n} = 8.33\\ \\frac{\\text{fF}}{\\mu\\text{m}^2}, \\quad C_{ox,p} = 8.16\\ \\frac{\\text{fF}}{\\mu\\text{m}^2}$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li><strong>Cổng ($C_{gs}, C_{gd}, C_{gb}$):</strong> Ghép xung nhịp và nhân Miller.</li>
                    <li><strong>Tiếp giáp P–N ($C_{sb}, C_{db}, C_{\\text{sub}}$):</strong> Biến thiên phi tuyến theo $V_{\\text{in}}$, gây méo nếu $W$ quá lớn.</li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded bg-sky-50 border border-sky-200 text-xs text-sky-900">
                  <strong>Hướng Tuần 4:</strong> Chia ngón (<span class="code-tag">nf ≥ 2</span>) giảm $\\sim 45\\%$ $A_D, P_D$.
                </div>
              </div>

              <div class="gold-card border-t-4 border-t-amber-500 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">2. Channel Charge Injection</span>
                  <div class="bg-white border border-amber-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$\\Delta V_{\\text{CI}} = -\\frac{Q_{\\text{ch},n} - |Q_{\\text{ch},p}|}{2 C_{\\text{hold}}}$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Kênh dẫn xả $Q_{\\text{ch}} = W L C_{ox}(V_{GS}-V_{TH})$ khi tắt.</li>
                    <li>Tại $V_{CM}=0.9\\text{ V}$ (<span class="code-tag">TG 2/6</span>): $V_{ov,n} = 34\\text{ mV}$ rất nhỏ $\\implies \\Delta V_{\\text{CI}} = \\mathbf{0.43\\text{ mV}}$ trên $C_1$ ($\\mathbf{0.05\\text{ mV}}$ trên $C_2$).</li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded bg-white border border-amber-300 text-xs text-amber-900">
                  <strong>Hướng Tuần 3:</strong> Bổ sung <strong>Dummy Switch $W/2$</strong> hấp thụ điện tích dư.
                </div>
              </div>

              <div class="ocean-card border-t-4 border-t-blue-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-blue-700 mono">3. Clock Feedthrough</span>
                  <div class="bg-white border border-sky-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$\\Delta V_{\\text{CF}} = \\pm V_{DD}\\frac{W C_{ov}}{W C_{ov} + C_{\\text{hold}}}$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Đo BSIM4: $C_{ov,n} = 0.493\\text{ fF}$, $C_{ov,p} = 0.444\\text{ fF}$.</li>
                    <li>Đơn lẻ trên $C_1$: $-8.82\\text{ mV}$ và $+7.96\\text{ mV}$.</li>
                    <li>Hai xung đảo $\\Phi, \\overline{\\Phi}$: tự triệt <strong>$&gt;90\\%$</strong>, còn $\\mathbf{-0.87\\text{ mV}}$!</li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded bg-white border border-sky-300 text-xs text-sky-900">
                  <strong>Trên $C_2 = 800\\text{ fF}$:</strong> Sụt áp ròng chỉ còn <strong>$-0.108\\text{ mV}$</strong>.
                </div>
              </div>
            </div>
            """,
            next_question="Lõi đóng ngắt và mảng tụ đã được bảo vệ — tiếp theo, hiện thực bộ đệm 5T-OTA trên nguồn thấp $1.8\\text{ V}$ gặp thách thức quỹ áp gì?",
            footer_text=f_foot,
            speaker_notes="Nếu làm khóa TG quá to, tụ tiếp giáp Cdb, Qch và Cov tăng vọt gây sai lệch tỷ số tụ và méo hài. Khóa CMOS 2/6 hoặc 4/12 giữ hai gai xuyên xung ngược pha tự triệt >90%.",
        ),

        # S14: BLOCK 4 5T-OTA WITH IEEE MOSFET SYMBOLS
        SlideSpec(
            act_tag="Hồi III (Tầng 3) — Khối 4 (<span class=\"code-tag\">ota_5t</span>) &amp; Phát Hiện Quỹ Áp BSIM4",
            title="Cấu Trúc 5T-OTA: Độ Lợi $A_{OL}$, Hỗ Dẫn $g_m$ &amp; Bài Toán Quỹ Áp ICMR",
            badge="Target: $A_{OL}&gt;40\\text{ dB}, \\text{PM}\\ge 60^\\circ$",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 ieee-card flex flex-col items-center justify-center py-2">
                __SVG_OTA__
                <p class="text-xs text-sky-800 font-semibold mono mt-1">5T-OTA hồi tiếp đơn vị ($V_{\\text{in}-} = V_{\\text{out}}$)</p>
              </div>
              <div class="col-span-7 flex flex-col gap-3 justify-center">
                <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                  <span class="text-xs font-bold uppercase text-sky-800 mono">1. Độ lợi vòng hở &amp; Sai số truyền đạt tĩnh ($\\beta = 1$)</span>
                  <div class="bg-white border border-sky-200 rounded p-1.5 my-1 text-center text-xs">
                    $$A_{OL} = g_{m1,2}(r_{o2}\\parallel r_{o4}) = \\frac{2}{(\\lambda_n+\\lambda_p)V_{ov1}} \\ge 100\\text{ V/V}\\ (40\\text{ dB}) \\implies \\epsilon_A \\le \\mathbf{0.99\\%}$$
                  </div>
                  <p class="text-xs text-sky-950">Cần chọn chiều dài kênh $L_{1..4} \\ge 0.5\\text{–}1.0\\ \\mu\\text{m}$ để giảm hệ số điều biến chiều dài kênh $\\lambda$.</p>
                </div>
                <div class="ieee-card border-l-4 border-l-blue-600 py-2.5">
                  <span class="text-xs font-bold uppercase text-blue-700 mono">2. Điều kiện băng thông &amp; hỗ dẫn ($C_L = 1\\text{ pF}$)</span>
                  <p class="text-xs text-sky-950 mt-1">$\\text{GBW} = \\frac{g_{m1,2}}{2\\pi C_L} &gt; 10\\text{ MHz} \\implies g_{m1,2} &gt; \\mathbf{62.8\\ \\mu\\text{S}}$ và cực gương dòng $f_{p2} = \\frac{g_{m3}}{2\\pi C_X} &gt; \\mathbf{17.3\\text{ MHz}}$.</p>
                </div>
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <span class="text-xs font-bold uppercase text-amber-800 mono">3. Phát hiện Quỹ áp ICMR trên Sky130A ($|V_{TH,p}| \\approx 0.98\\text{ V}$)</span>
                  <p class="text-xs text-sky-950 mt-1">$V_{\\text{in,cm}} \\in [V_{GS1} + V_{dsat5},\\ V_{DD} - V_{SG3} + V_{TH1}]$. Để biên dưới $\\le 0.50\\text{ V}$ cần mở rộng $(W/L)_{1,2}$ (vào nghịch đảo trung bình, hạ $V_{GS1}$) ở Tuần 2!</p>
                </div>
              </div>
            </div>
            """.replace("__SVG_OTA__", _svg_w1_s14_ota()),
            next_question="Bốn khối phần cứng đã được mổ xẻ tường tận — bây giờ bước sang Hồi IV: ghép chúng thành sản phẩm hoàn chỉnh và xem INPUT / OUTPUT thực tế!",
            footer_text=f_foot,
            speaker_notes="Sơ đồ 5T-OTA với cặp PMOS M3/M4 (có vòng tròn đảo cổng) và 3 NMOS M1/M2/M5 chuẩn IEEE. Phát hiện quan trọng của Tuần 1: |Vth,p| cao trên sky130A đòi hỏi thiết kế M1/M2 ở nghịch đảo trung bình tại Tuần 2.",
        ),

        # S15: COMPLETE 4-BLOCK SYSTEM ARCHITECTURE
        SlideSpec(
            act_tag="Hồi IV — Kiến Trúc Sản Phẩm Hoàn Chỉnh",
            title="Hợp Nhất 4 Khối Chức Năng Toàn Chip (<span class=\"code-tag\">top_sc_lpf</span>)",
            badge="Architecture Sign-Off",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card py-3 px-5">
              __SVG_TOP__
              <div class="grid grid-cols-4 gap-3 mt-2 pt-2.5 border-t border-sky-200 text-xs">
                <div><strong class="text-sky-800">Khối 1:</strong> Phân phối xung không chồng lấn.</div>
                <div><strong class="text-blue-700">Khối 2:</strong> Chuyển giao gói điện tích $94\\tau$.</div>
                <div><strong class="text-sky-950">Khối 3:</strong> Mảng tụ MIM $3\\times 3$ khóa $H(z)$.</div>
                <div><strong class="text-amber-800">Khối 4:</strong> Cách ly nút $V_X$ &amp; kéo tải ADC.</div>
              </div>
            </div>
            """.replace("__SVG_TOP__", _svg_w1_s15_top()),
            next_question="Khi cấp tín hiệu thực tế vào chân <span class=\"code-tag\">V_in</span> của con chip này, dạng sóng và phổ tại <span class=\"code-tag\">V_out</span> dự kiến đạt những con số nào?",
            footer_text=f_foot,
            speaker_notes="Sơ đồ hợp nhất 4 khối chức năng theo đúng ký hiệu chuẩn IEEE: Khối xung clock, cặp khóa CMOS TG1/TG2 điều khiển ngược pha, tụ MIM 1:8 và bộ đệm tam giác 5T-OTA hồi tiếp âm đơn vị.",
        ),

        # S16: EXPECTED I/O
        SlideSpec(
            act_tag="Hồi IV — Năng Lực Sản Phẩm Hoàn Thiện",
            title="Sản Phẩm Xử Lý Được Gì? — Đặc Tả INPUT &amp; OUTPUT Dự Kiến",
            badge="Expected Chip Performance",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-7 fig-frame p-2">
                <img src="figs/week1_io_expected.png" alt="Expected I/O" class="max-h-[410px] w-auto object-contain" />
              </div>
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">INPUT Đưa Vào Chip</div>
                  <ul class="mt-1 space-y-1 text-xs text-sky-950 list-disc pl-4">
                    <li>Điện áp tương tự $V_{\\text{in}}(t) \\in [0.48, 1.32]\\text{ V}$ quanh $0.9\\text{ V}$.</li>
                    <li>Thử chuẩn: $0.30\\sin(2\\pi\\cdot 50\\text{ kHz}\\,t) + 0.12\\sin(2\\pi\\cdot 2\\text{ MHz}\\,t)$.</li>
                    <li>Nguồn $V_{DD} = 1.8\\text{ V}$ &amp; xung vuông $V_{\\text{clk}} = 10\\text{ MHz}$.</li>
                  </ul>
                </div>
                <div class="ocean-card border-l-4 border-l-sky-600 py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">OUTPUT Dự Kiến Tại Chân <span class="code-tag">Vout</span> ($C_L = 1\\text{ pF}$)</div>
                  <ul class="mt-1 space-y-1 text-xs text-sky-950 list-disc pl-4">
                    <li><strong>Dải thông $50\\text{ kHz}$:</strong> giữ $96.6\\%$ biên độ ($\\mathbf{-0.30\\text{ dB}} \\to 0.290\\text{ V}_p$).</li>
                    <li><strong>Nhiễu $2\\text{ MHz}$:</strong> nén <strong>$-20.02\\text{ dB}$</strong> ($120\\text{ mV}_p \\to \\mathbf{12\\text{ mV}_p}$).</li>
                    <li><strong>Tại Nyquist $5\\text{ MHz}$:</strong> nén sâu tới <strong>$-24.61\\text{ dB}$</strong> ($17\\times$).</li>
                  </ul>
                </div>
                <div class="ieee-card border-sky-400 py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Chỉ Tiêu Cam Kết Trên Silicon (Gate 3 &amp; 4)</div>
                  <div class="grid grid-cols-3 gap-2 mt-1.5 text-center">
                    <div class="bg-sky-50 border border-sky-200 rounded-lg p-1.5">
                      <div class="text-sm font-extrabold text-sky-700 mono">$|\\Delta f_c| &lt; 5\\%$</div>
                      <div class="text-[10px] text-sky-900">$178.3\\text{–}197.1\\text{ kHz}$</div>
                    </div>
                    <div class="bg-sky-50 border border-sky-200 rounded-lg p-1.5">
                      <div class="text-sm font-extrabold text-blue-700 mono">$\\text{SFDR} &gt; 50\\text{ dB}$</div>
                      <div class="text-[10px] text-sky-900">Không gai hài lạ</div>
                    </div>
                    <div class="bg-amber-50 border border-amber-300 rounded-lg p-1.5">
                      <div class="text-sm font-extrabold text-amber-800 mono">$\\text{THD} &lt; -48\\text{ dB}$</div>
                      <div class="text-[10px] text-amber-900">Méo hài $&lt; 0.4\\%$</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            """,
            next_question="Bước sang Hồi V: Làm sao đo kiểm đáp ứng tần số của con chip này trên Ngspice — tại sao tuyệt đối không được dùng lệnh <span class=\"code-tag\">.ac</span> quen thuộc?",
            footer_text=f_foot,
            speaker_notes="Ngõ ra Vout dự kiến giữ 96.6% tín hiệu 50 kHz và nén nhiễu 2 MHz đi 10 lần (-20.02 dB). Các cổng kiểm định Tuần 3 và 4 cam kết sai số fc < 5%, SFDR > 50 dB, THD < -48 dB.",
        ),

        # S17: LTI VS LPTV
        SlideSpec(
            act_tag="Hồi V — Cơ Sở Toán–Lý Của Phương Pháp Mô Phỏng",
            title="Hệ LTI vs. Hệ LPTV: Chứng Minh Vì Sao Lệnh <span class=\"code-tag\">.ac</span> Bất Lực Với Lõi SC",
            badge="SPICE Engine Physics",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-6 ieee-card border-t-4 border-t-amber-500 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">1. Điều gì xảy ra khi gõ lệnh <span class="code-tag">.ac</span> lên lõi SC?</span>
                  <div class="my-2.5 p-2.5 rounded-xl bg-amber-50/70 border border-amber-200">
                    __SVG_LTV__
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>SPICE giải 1 ma trận tĩnh duy nhất: $(\\mathbf{G}_{\\text{op}} + j\\omega\\mathbf{C}_{\\text{op}})\\mathbf{V}(\\omega) = \\mathbf{I}(\\omega)$.</li>
                    <li>Vì $\\mathbf{G}_{\\text{op}}$ cố định theo $t=0$, đường truyền sang $C_2$ bị <strong>đứt mạch hoàn toàn</strong>!</li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded bg-amber-100 border border-amber-300 text-xs font-bold text-amber-950 text-center">
                  Kết luận: <span class="code-tag">.ac</span> chỉ hợp lệ cho hệ LTI (như khối <span class="code-tag">ota_5t</span> độc lập)
                </div>
              </div>

              <div class="col-span-6 ocean-card border-t-4 border-t-sky-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-800 mono">2. Bản chất LPTV &amp; Giải pháp Coherent FFT miền thời gian</span>
                  <p class="text-xs text-sky-950 mt-2">
                    Mạch tụ chuyển mạch là hệ <strong>Biến thiên Tuần hoàn theo Thời gian (LPTV)</strong>: $\\mathbf{G}(t + T_{\\text{clk}}) = \\mathbf{G}(t)$. Để đo đúng hàm truyền &amp; méo phi tuyến:
                  </p>
                  <div class="bg-white border border-sky-200 rounded-lg p-2 my-2.5 text-center text-xs">
                    $$f_{\\text{in}} = \\frac{M_{\\text{sig}}}{N_{\\text{FFT}}} \\cdot f_{\\text{clk}} \\qquad \\left(\\gcd(M_{\\text{sig}}, N_{\\text{FFT}}) = 1,\\ N_{\\text{FFT}} = 2^k\\right)$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li><strong>Chạy <span class="code-tag">.tran</span> thực tế:</strong> Đóng ngắt xung $10\\text{ MHz}$ qua hàng trăm chu kỳ.</li>
                    <li><strong>Lấy mẫu cuối pha $\\Phi_2$ (Strobe):</strong> Thu chuỗi $V_{\\text{out}}[n]$ khi đã ổn định.</li>
                    <li><strong>Coherent FFT:</strong> Đúng số nguyên $M_{\\text{sig}}$ chu kỳ $\\implies$ <strong>0 rò rỉ phổ!</strong></li>
                  </ul>
                </div>
                <div class="mt-3 p-2 rounded bg-white border border-sky-300 text-xs font-bold text-sky-900 text-center">
                  Đo đồng thời chính xác $|H(f)|, f_{c,\\text{SC}}, \\text{SFDR}, \\text{THD}, \\text{SNDR}, \\text{ENOB}$
                </div>
              </div>
            </div>
            """.replace("__SVG_LTV__", _svg_w1_s17_ltv()),
            next_question="Từ sự khác biệt LTI vs. LPTV đó, toàn bộ quy trình 4 lớp để kiểm tra mạch hoạt động ổn định từ sơ đồ đến Silicon được thiết lập như thế nào?",
            footer_text=f_foot,
            speaker_notes="Lệnh .ac đóng băng khóa ở t=0 làm TG2 hở mạch vĩnh viễn (~10^11 Ohm). Do đó toàn mạch SC (hệ LPTV) bắt buộc kiểm tra bằng .tran + lấy mẫu Strobe cuối Phi2 + Coherent FFT.",
        ),

        # S18: 4-LAYER STABILITY
        SlideSpec(
            act_tag="Hồi V — Chiến Lược Kiểm Tra Ổn Định Toàn Diện",
            title="Bốn Lớp Kiểm Chứng Độ Ổn Định Từ Phương Trình Đến Mặt Nạ Silicon",
            badge="Verification-First Methodology",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-4 gap-3.5">
              <div class="ieee-card border-t-4 border-t-sky-600 py-2.5 px-3.5">
                <div class="text-[11px] font-bold uppercase text-sky-700 mono">Lớp 1 • Toán học</div>
                <div class="font-bold text-sky-950 text-sm mt-0.5">Ổn Định BIBO</div>
                <p class="text-xs text-sky-900 mt-1">Cực $|z_p| = 8/9 &lt; 1$ bảo đảm đáp ứng xung tắt dần tuyệt đối.</p>
              </div>
              <div class="ocean-card border-t-4 border-t-blue-600 py-2.5 px-3.5">
                <div class="text-[11px] font-bold uppercase text-blue-700 mono">Lớp 2 • Vòng kín LTI</div>
                <div class="font-bold text-sky-950 text-sm mt-0.5">Biên Pha $\\text{PM} \\ge 60^\\circ$</div>
                <p class="text-xs text-sky-900 mt-1"><span class="code-tag">.op</span> + <span class="code-tag">.ac</span> + Step ngăn 5T-OTA rung tự kích.</p>
              </div>
              <div class="gold-card border-t-4 border-t-amber-500 py-2.5 px-3.5">
                <div class="text-[11px] font-bold uppercase text-amber-800 mono">Lớp 3 • Toàn mạch LPTV</div>
                <div class="font-bold text-sky-950 text-sm mt-0.5">Coherent FFT</div>
                <p class="text-xs text-sky-900 mt-1"><span class="code-tag">.tran</span> đa tần &amp; đơn tần đo lệch $f_c &lt; 5\\%$, SFDR, THD.</p>
              </div>
              <div class="ieee-card border-t-4 border-t-sky-900 py-2.5 px-3.5">
                <div class="text-[11px] font-bold uppercase text-sky-900 mono">Lớp 4 • Vật lý Wafer</div>
                <div class="font-bold text-sky-950 text-sm mt-0.5">PVT + DRC/LVS/PEX</div>
                <p class="text-xs text-sky-900 mt-1">Đối chiếu 3 cột xác minh ký sinh dây kim loại thực tế.</p>
              </div>
            </div>

            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-xs">
                <thead>
                  <tr class="uppercase tracking-wider">
                    <th class="py-2 px-3.5 text-left">Đối tượng kiểm tra</th>
                    <th class="py-2 px-3.5 text-left">Phép đo SPICE / EDA</th>
                    <th class="py-2 px-3.5 text-left">Ngưỡng đạt (Gate Pass)</th>
                    <th class="py-2 px-3.5 text-left">Lý do kỹ thuật chọn phương pháp</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950 text-[12px]">
                  <tr>
                    <td class="py-2 px-3.5 font-bold"><span class="code-tag">non_overlap_clk</span></td>
                    <td class="py-2 px-3.5 mono font-semibold">.tran</td>
                    <td class="py-2 px-3.5">$t_{\\text{nov}} \\in [2,5]\\text{ ns}$, $\\Phi_1\\cdot\\Phi_2 \\approx 0$</td>
                    <td class="py-2 px-3.5">Xác minh khoảng chết thực tế chống rò điện tích trực tiếp.</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-bold"><span class="code-tag">tg_switch</span></td>
                    <td class="py-2 px-3.5 mono font-semibold">.dc ($0 \\to 1.8\\text{ V}$) + PVT</td>
                    <td class="py-2 px-3.5">$R_{\\text{on,max}} &lt; 5\\text{ k}\\Omega$</td>
                    <td class="py-2 px-3.5">Bắt đúng đỉnh Body Effect tại $0.96\\text{ V}$, bảo đảm $94\\tau$.</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-3.5 font-bold"><span class="code-tag">ota_5t</span></td>
                    <td class="py-2 px-3.5 mono font-semibold">.op + .ac + .tran step</td>
                    <td class="py-2 px-3.5">5 FET bão hòa, $A_{OL}&gt;40\\text{ dB}, \\text{PM}\\ge 60^\\circ$</td>
                    <td class="py-2 px-3.5">Tiêu chuẩn Bode/Nyquist + kiểm chứng Slew Rate thực.</td>
                  </tr>
                  <tr class="row-gold font-semibold">
                    <td class="py-2 px-3.5 font-bold text-amber-900"><span class="code-tag-gold">top_sc_lpf</span> (Pre &amp; PEX)</td>
                    <td class="py-2 px-3.5 mono font-bold text-amber-900">.tran + Strobe + FFT</td>
                    <td class="py-2 px-3.5">$|\\Delta f_c|&lt;5\\%, \\text{SFDR}&gt;50\\text{ dB}$, LVS Clean</td>
                    <td class="py-2 px-3.5">Đo chính xác hệ LPTV và hậu kiểm tụ ký sinh sau Layout.</td>
                  </tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Trước khi viết dòng code mô phỏng đầu tiên cho Tuần 2, làm sao chắc chắn toàn bộ 22 phương trình của Tuần 1 không hề sai thứ nguyên đơn vị?",
            footer_text=f_foot,
            speaker_notes="Quy trình kiểm định ổn định gồm 4 lớp độc lập: BIBO toán học, Bode/Step cho OTA, .tran+Strobe+FFT cho toàn mạch LPTV, và PVT+DRC/LVS/PEX cho vật lý silicon.",
        ),

        # S19: 22/22 SI DIMENSIONAL AUDIT
        SlideSpec(
            act_tag="Hồi V — Bằng Chứng Định Lượng Verification Gate 1",
            title="Kiểm Định Tự Động Thứ Nguyên Hệ SI: Khớp Tuyệt Đối 22 / 22 Công Thức",
            badge="22 / 22 SI Formulas PASS",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-4 flex flex-col gap-3.5 justify-center">
                <div class="ocean-card py-4">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Script Kiểm Chứng Tự Động</div>
                  <div class="text-lg font-extrabold mono text-sky-950 mt-1">week1_verify.py</div>
                  <p class="text-xs text-sky-900 mt-2">Phân tích vector số mũ cơ sở $(\\text{kg}, \\text{m}, \\text{s}, \\text{A}, \\text{K})$ cho mọi vế phương trình.</p>
                  <div class="mt-3 p-2.5 rounded-lg bg-white border-2 border-sky-500 text-center">
                    <span class="text-2xl font-extrabold text-sky-700 mono">22 / 22 PASS</span>
                  </div>
                </div>
                <div class="gold-card border-l-4 border-l-amber-500 py-3">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Tệp dữ liệu xuất chuẩn</div>
                  <p class="text-xs text-sky-950 mt-1">Lưu toàn bộ thông số khóa cứng và kết quả đo Ngspice PDK vào <span class="code-tag-gold">python/week1_numbers.json</span> làm đầu vào cho Tuần 2.</p>
                </div>
              </div>

              <div class="col-span-8 ieee-card p-0 overflow-hidden">
                <table class="ieee-table text-xs">
                  <thead>
                    <tr class="uppercase tracking-wider">
                      <th class="py-2 px-3 text-left">Nhóm công thức</th>
                      <th class="py-2 px-3 text-left">Biểu thức tiêu biểu</th>
                      <th class="py-2 px-3 text-left">Thứ nguyên SI dẫn xuất</th>
                      <th class="py-2 px-3 text-center">Đơn vị</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-sky-100 text-sky-950 text-[12px]">
                    <tr><td class="py-2 px-3 font-semibold">Điện trở SC tương đương</td><td class="py-2 px-3">$R_{\\text{eq}} = \\frac{1}{f_{\\text{clk}} C_1}$</td><td class="py-2 px-3 mono">$\\text{kg}\\cdot\\text{m}^2\\cdot\\text{s}^{-3}\\cdot\\text{A}^{-2}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\Omega$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Tần số cắt &amp; Băng thông</td><td class="py-2 px-3">$f_{c,\\text{RC}}, \\text{GBW} = \\frac{g_m}{2\\pi C_L}, f_{p2}$</td><td class="py-2 px-3 mono">$\\text{s}^{-1}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{Hz}$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Bảo toàn điện tích 2 pha</td><td class="py-2 px-3">$Q = C \\cdot V$</td><td class="py-2 px-3 mono">$\\text{s}\\cdot\\text{A}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{C}$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Phương sai nhiễu nhiệt</td><td class="py-2 px-3">$\\overline{v_n^2} = \\frac{k_B T}{C}$</td><td class="py-2 px-3 mono">$\\text{kg}^2\\cdot\\text{m}^4\\cdot\\text{s}^{-6}\\cdot\\text{A}^{-2}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{V}^2$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Hỗ dẫn &amp; Nội trở MOSFET</td><td class="py-2 px-3">$g_m = \\frac{2I_D}{V_{ov}},\\ R_{\\text{on}},\\ r_o$</td><td class="py-2 px-3 mono">$\\text{S}$ và $\\Omega$ tương ứng</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{S}, \\Omega$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Sụt áp ký sinh đóng ngắt</td><td class="py-2 px-3">$\\Delta V_{\\text{CI}} = \\frac{W L C_{ox}V_{ov}}{2 C_H},\\ \\Delta V_{\\text{CF}}$</td><td class="py-2 px-3 mono">$\\text{kg}\\cdot\\text{m}^2\\cdot\\text{s}^{-3}\\cdot\\text{A}^{-1}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{V}$ ✓</td></tr>
                    <tr><td class="py-2 px-3 font-semibold">Tụ MIM &amp; Slew Rate</td><td class="py-2 px-3">$C_{\\text{mim}} = C_A(W+dw)(L+dw),\\ \\text{SR}=\\frac{I_{\\text{tail}}}{C_L}$</td><td class="py-2 px-3 mono">$\\text{F}$ và $\\text{V}\\cdot\\text{s}^{-1}$</td><td class="py-2 px-3 text-center font-bold text-sky-700">$\\text{F}, \\text{V/s}$ ✓</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            """,
            next_question="Mọi phương trình, thông số và kiến trúc đã được kiểm chứng — cùng chốt bảng Tổng kết Gate 1 và lộ trình bước sang Tuần 2.",
            footer_text=f_foot,
            speaker_notes="Script week1_verify.py kiểm chứng tự động đại số thứ nguyên hệ SI (kg, m, s, A, K) cho toàn bộ 22 phương trình của dự án, đạt 22/22 PASS.",
        ),

        # S20: GATE 1 SIGN-OFF
        SlideSpec(
            act_tag="Tổng Kết Báo Cáo Tuần 1 — Verification Gate 1 Sign-Off",
            title="Bảng Khóa Cứng Kiến Trúc Tuần 1 &amp; Lộ Trình Triển Khai 4 Tuần",
            badge="GATE 1: VERIFIED &amp; LOCKED",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-4 gap-3">
              <div class="rounded-xl ocean-card p-2.5 text-xs border-2 border-sky-600"><div class="font-bold text-sky-800 mono">TUẦN 1 • ✓ PASS</div><div class="font-semibold text-sky-950 mt-0.5">Bài toán → S&amp;S → 4 Khối</div></div>
              <div class="rounded-xl gold-card p-2.5 text-xs"><div class="font-bold text-amber-800 mono">TUẦN 2 • TIẾP THEO</div><div class="font-semibold text-sky-950 mt-0.5">Golden Model FFT &amp; Sizing $W/L$</div></div>
              <div class="rounded-xl ieee-card p-2.5 text-xs"><div class="font-bold text-sky-700 mono">TUẦN 3</div><div class="font-semibold text-sky-900 mt-0.5">Xschem &amp; Pre-Layout Ngspice</div></div>
              <div class="rounded-xl ieee-card p-2.5 text-xs"><div class="font-bold text-sky-700 mono">TUẦN 4</div><div class="font-semibold text-sky-900 mt-0.5">Layout ABBA, DRC/LVS &amp; PEX</div></div>
            </div>

            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-sm">
                <thead>
                  <tr class="text-xs uppercase tracking-wider">
                    <th class="py-2 px-4 text-left">Hạng mục Chốt Gate 1</th>
                    <th class="py-2 px-4 text-left">Cơ sở Lý thuyết &amp; Cấu hình</th>
                    <th class="py-2 px-4 text-left">Thông số Khóa Cứng</th>
                    <th class="py-2 px-4 text-center">Trạng thái</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950 text-[12.8px]">
                  <tr><td class="py-2 px-4 font-semibold">1. Cầu nối S&amp;S $\\to$ Lõi lọc</td><td class="py-2 px-4">$H(z) = \\frac{1/9}{1 - (8/9)z^{-1}}$, $\\text{OSR} = 26.64$</td><td class="py-2 px-4">$f_{\\text{clk}}=10\\text{ MHz},\\ f_{c,\\text{SC}}=\\mathbf{187.675\\text{ kHz}}$</td><td class="py-2 px-4 text-center"><span class="badge-ocean">LOCKED</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">2. Mảng tụ MIM (<span class="code-tag">sc_core</span>)</td><td class="py-2 px-4">$\\text{SNR}_{kT/C} = 71.9\\text{ dB}$, ma trận $3\\times 3$</td><td class="py-2 px-4">$C_1=100\\text{ fF},\\ C_2=800\\text{ fF}$ ($4.85\\times 9.85\\ \\mu\\text{m}$)</td><td class="py-2 px-4 text-center"><span class="badge-ocean">LOCKED</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">3. Xung &amp; Khóa (<span class="code-tag">clk</span>, <span class="code-tag">tg</span>)</td><td class="py-2 px-4">Chống rò mẫu &amp; nạp $94\\tau$ kháng THD</td><td class="py-2 px-4">$t_{\\text{nov}} \\in [2,5]\\text{ ns},\\ W_n/W_p = 4/12\\ \\mu\\text{m}$ ($2.26\\text{ k}\\Omega$)</td><td class="py-2 px-4 text-center"><span class="badge-ocean">PASS</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">4. Bộ đệm đơn vị (<span class="code-tag">ota_5t</span>)</td><td class="py-2 px-4">$\\epsilon_A &lt; 1\\%$, hệ bậc 2 không rung ($\\zeta \\ge 0.66$)</td><td class="py-2 px-4">$A_{OL}&gt;40\\text{ dB},\\ \\text{GBW}&gt;10\\text{ MHz},\\ \\text{PM}\\ge 60^\\circ$</td><td class="py-2 px-4 text-center"><span class="badge-ocean">LOCKED</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">5. Thứ nguyên &amp; Hạ tầng EDA</td><td class="py-2 px-4"><span class="code-tag">week1_verify.py</span> + <span class="code-tag">env_sky130.sh</span></td><td class="py-2 px-4"><strong>22 / 22</strong> phương trình SI PASS • PDK <span class="code-tag">sky130A</span></td><td class="py-2 px-4 text-center"><span class="badge-gold">READY</span></td></tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Bước sang Tuần 2: Tuần 2 là gì, Golden Model là gì, và chúng ta mô phỏng gì trên Python trước khi vẽ Xschem?",
            footer_text=f_foot,
            speaker_notes="Gate 1 Tuần 1 hoàn tất 100%. Câu hỏi tự nhiên mở ra cho Tuần 2: tại sao không vẽ thẳng Schematic mà phải xây dựng Python Golden Model & tính Sizing W/L trước?",
        ),
    ]


def _svg_w2_pipeline() -> str:
    """Visual workflow of Week 2 Python modeling -> JSON -> Week 3 Ngspice."""
    return f"""
    <svg viewBox="0 0 1100 185" class="w-full h-[170px]">
      {svg_defs()}
      <rect x="16" y="22" width="235" height="132" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
      <text x="133" y="48" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">1. Lý Thuyết Tuần 1</text>
      <text x="133" y="72" text-anchor="middle" font-size="11.5" fill="#0C4A6E">H(z), fc=187.675 kHz</text>
      <text x="133" y="92" text-anchor="middle" font-size="11.5" fill="#0C4A6E">kT/C, Ron, A_OL, ICMR</text>
      <text x="133" y="114" text-anchor="middle" font-size="11" font-weight="700" fill="#D97706">week1_numbers.json</text>
      <text x="133" y="136" text-anchor="middle" font-size="10.5" fill="#78350F">Đầu vào toán-lý khóa cứng</text>

      <line x1="251" y1="88" x2="292" y2="88" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="298" y="22" width="245" height="132" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.2" />
      <text x="420" y="48" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">2. golden_model.py</text>
      <text x="420" y="72" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Bode H(z) vs RC</text>
      <text x="420" y="92" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Quá độ đa tần ZOH</text>
      <text x="420" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Coherent FFT N=16384 + kT/C</text>
      <text x="420" y="136" text-anchor="middle" font-size="11" font-weight="700" fill="#0284C7">→ metrics_golden.json</text>

      <line x1="543" y1="88" x2="584" y2="88" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="590" y="22" width="245" height="132" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
      <text x="712" y="48" text-anchor="middle" font-size="13" font-weight="800" fill="#B45309">3. nonideal_budget.py</text>
      <text x="712" y="72" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Quét Ron(V) → Track THD</text>
      <text x="712" y="92" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Quét A_OL → Sai số DC/cực</text>
      <text x="712" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Đánh đổi W×L vs ΔV_CI</text>
      <text x="712" y="136" text-anchor="middle" font-size="11" font-weight="700" fill="#D97706">→ nonideal_budget.json</text>

      <line x1="835" y1="88" x2="876" y2="88" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="882" y="22" width="205" height="132" rx="12" fill="#E0F2FE" stroke="#0369A1" stroke-width="2.4" />
      <text x="984" y="48" text-anchor="middle" font-size="13" font-weight="800" fill="#0369A1">4. sizing_calc.py</text>
      <text x="984" y="72" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Tính gm/ID 5T-OTA</text>
      <text x="984" y="92" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Sizing W/L 4 khối</text>
      <text x="984" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Gọi BSIM4 kiểm trước</text>
      <text x="984" y="136" text-anchor="middle" font-size="11" font-weight="700" fill="#0369A1">→ sizing_table.json</text>
    </svg>
    """


def _svg_w2_w3_handoff() -> str:
    return f"""
    <svg viewBox="0 0 1080 205" class="w-full h-[190px]">
      {svg_defs()}
      <rect x="16" y="34" width="230" height="134" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
      <text x="131" y="64" text-anchor="middle" font-size="13.5" font-weight="800" fill="#B45309">1. sizing_table.json</text>
      <text x="131" y="90" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Nhập W, L, nf, mult</text>
      <text x="131" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">vào Schematic Xschem</text>
      <text x="131" y="140" text-anchor="middle" font-size="11" font-weight="700" fill="#D97706">NOT / NAND2 / TG / OTA</text>

      <line x1="246" y1="101" x2="296" y2="101" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="302" y="34" width="230" height="134" rx="12" fill="#F0F9FF" stroke="#0284C7" stroke-width="2.2" />
      <text x="417" y="64" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0369A1">2. Ngspice Unit Gates</text>
      <text x="417" y="90" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Kiểm định độc lập từng khối:</text>
      <text x="417" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">.tran (clk), .dc (TG),</text>
      <text x="417" y="140" text-anchor="middle" font-size="11" font-weight="700" fill="#0284C7">.op + .ac + .tran (ota_5t)</text>

      <line x1="532" y1="101" x2="582" y2="101" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="588" y="34" width="230" height="134" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="2.2" />
      <text x="703" y="64" text-anchor="middle" font-size="13.5" font-weight="800" fill="#B45309">3. Top Coherent .tran</text>
      <text x="703" y="90" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Ghép top_sc_lpf_xschem.spice</text>
      <text x="703" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">Strobe cuối pha Φ₂ (98 ns)</text>
      <text x="703" y="140" text-anchor="middle" font-size="11" font-weight="700" fill="#D97706">method=gear, maxstep ≤ 2 ns</text>

      <line x1="818" y1="101" x2="868" y2="101" stroke="#0284C7" stroke-width="2.5" marker-end="url(#arr-blue)" />

      <rect x="874" y="34" width="192" height="134" rx="12" fill="#E0F2FE" stroke="#0369A1" stroke-width="2.4" />
      <text x="970" y="64" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0369A1">4. Overlay &amp; Gate 3</text>
      <text x="970" y="90" text-anchor="middle" font-size="11.5" fill="#0C4A6E">ngspice_vs_golden.py</text>
      <text x="970" y="112" text-anchor="middle" font-size="11.5" fill="#0C4A6E">So với metrics_golden.json</text>
      <text x="970" y="140" text-anchor="middle" font-size="11" font-weight="800" fill="#0284C7">|Δf_c| &lt; 5% • SFDR &gt; 50 dB</text>
    </svg>
    """


def get_week2_slides() -> list[SlideSpec]:
    f_foot = "SKY130-SC-LPF • Tuần 2: Mô Hình Hóa Python (Golden Model), Ngân Sách Phi Lý Tưởng &amp; Sizing W/L"
    return [
        # S01: COVER
        SlideSpec(
            act_tag="",
            title="",
            badge="",
            badge_tone="ocean",
            is_cover=True,
            section_id="w2-start",
            body_html="""
            <div class="flex items-center justify-between border-b-2 border-sky-200 pb-3 relative z-10">
              <div class="flex items-center gap-3">
                <span class="px-3 py-1 rounded-md bg-sky-600 text-white text-xs font-bold tracking-widest uppercase mono">IEEE / ISSCC DESIGN SERIES</span>
                <span class="text-sky-900 text-sm font-semibold mono">PDK: SkyWater 130nm (sky130A) • Behavioral + Sizing</span>
              </div>
              <span class="px-3 py-1 rounded-full bg-amber-100 border border-amber-400 text-amber-900 text-xs font-bold mono">TUẦN 02 / 04 — GOLDEN MODEL &amp; SIZING</span>
            </div>

            <div class="my-auto py-2 relative z-10">
              <p class="text-amber-700 font-bold tracking-wider uppercase text-xs mono mb-1.5">Behavioral Modeling, Error Budgeting &amp; gm/ID Transistor Sizing</p>
              <h1 class="text-[44px] font-extrabold tracking-tight leading-tight text-sky-950 max-w-5xl">
                Mô Hình Hóa Python (Golden Model)<br />
                <span class="text-sky-600">&amp; Tính Toán Sizing $W/L$ Cho Sky130A</span>
              </h1>
              <p class="text-sky-900 text-base mt-3 max-w-4xl">
                Tuần 2 giải đáp trọn vẹn 4 câu hỏi cốt lõi: <strong class="text-amber-800">Tuần 2 làm gì?</strong> $\\to$ <strong class="text-sky-700">Golden Model là gì?</strong> $\\to$ <strong class="text-sky-950">Python mô phỏng những gì?</strong> $\\to$ <strong class="text-amber-800">Ứng dụng công thức lý thuyết nào vào Sizing?</strong>
              </p>

              <div class="grid grid-cols-4 gap-4 mt-8">
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">1. Tần số cắt Golden</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$187.675\\text{ kHz}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Lệch $-5.66\\%$ so với $RC$ liên tục</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">2. Trần vật lý $kT/C$ FFT</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$\\text{SNR} = 72.09\\text{ dB}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">$\\text{ENOB} = 11.66\\text{ bits}$ ($V_p = 0.4\\text{ V}$)</div>
                </div>
                <div class="ocean-card p-4">
                  <div class="text-sky-800 text-xs uppercase font-bold">3. 5T-OTA BSIM4 Verified</div>
                  <div class="text-2xl font-extrabold text-sky-700 mt-1 mono">$A_{OL} = 41.62\\text{ dB}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">$\\text{GBW} = 43.9\\text{ MHz},\\ \\text{PM} = 81.3^\\circ$</div>
                </div>
                <div class="gold-card p-4">
                  <div class="text-amber-900 text-xs uppercase font-bold">4. Non-Overlap Clock</div>
                  <div class="text-2xl font-extrabold text-amber-800 mt-1 mono">$t_{\\text{nov}} = 2.92\\text{ ns}$</div>
                  <div class="text-sky-900/80 text-xs mt-1">Đối xứng 2 cạnh trong $[2, 5]\\text{ ns}$</div>
                </div>
              </div>
            </div>
            """,
            next_question="Đã có đầy đủ công thức lý thuyết ở Tuần 1 rồi — vậy bản chất Tuần 2 là gì và tại sao ta không nhảy thẳng sang vẽ Schematic Xschem luôn?",
            footer_text="Data Source: metrics_golden.json • nonideal_budget.json • sizing_table.json",
            speaker_notes="Slide mở đầu Tuần 2 đặt ra 4 câu hỏi dẫn dắt cho toàn bộ người xem: Tuần 2 là gì, Golden Model là gì, Python mô phỏng những việc gì, và các công thức Tuần 1 được lập trình ra sao.",
        ),

        # S02: WHAT IS WEEK 2 & PURPOSE
        SlideSpec(
            act_tag="Hồi I — Định Nghĩa &amp; Mục Đích Chiến Lược Của Tuần 2",
            title="Tuần 2 Là Gì? Tại Sao Phải Qua Bước Python Trước Khi Vẽ Schematic?",
            badge="Why Behavioral Modeling?",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Sai lầm phổ biến của người mới thiết kế IC</span>
                  <h3 class="text-lg font-extrabold text-sky-950 mt-1">Vẽ thẳng Transistor vào Xschem/SPICE</h3>
                  <ul class="mt-3 space-y-2 text-sm text-sky-950 list-disc pl-4">
                    <li>Khi mạch chạy sai $f_c$ hoặc méo hài, <strong>không biết do sai công thức hệ thống hay sai kích thước MOSFET</strong>.</li>
                    <li>Mỗi lần chạy <span class="code-tag">.tran</span> toàn mạch BSIM4 tốn hàng chục giây–phút, <strong>không thể quét hàng nghìn tổ hợp</strong> $R_{\\text{on}}, A_{OL}, W/L$.</li>
                    <li>Không có mốc chuẩn đối chiếu nên dễ chấp nhận sai số ngầm.</li>
                  </ul>
                </div>
                <div class="bg-white border border-amber-300 rounded-lg p-2.5 text-xs font-bold text-amber-900 text-center mt-2">
                  Tuần 2 là cầu nối Số hóa &amp; Định cỡ trước khi mở Xschem!
                </div>
              </div>

              <div class="col-span-7 flex flex-col gap-3 justify-center">
                <div class="ocean-card border-l-4 border-l-sky-600 py-3">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">Mục đích 1 • Dựng “Thước đo Chuẩn” (Golden Baseline)</div>
                  <p class="text-sm text-sky-950 mt-1">Biến các phương trình toán Tuần 1 thành bộ mô phỏng số chính xác trên Python để xuất ra phổ chuẩn, sóng bậc thang chuẩn và tần số cắt chuẩn $187.675\\text{ kHz}$.</p>
                </div>
                <div class="ieee-card border-l-4 border-l-amber-500 py-3">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">Mục đích 2 • Định lượng Ngân sách Lỗi Phi Lý Tưởng</div>
                  <p class="text-sm text-sky-950 mt-1">Tiêm từng khiếm khuyết vật lý ($R_{\\text{on}}$ phi tuyến, $A_{OL}$ hữu hạn, Charge Injection, $kT/C$) để tìm ngưỡng tối đa mà mạch còn đạt chuẩn.</p>
                </div>
                <div class="ocean-card border-l-4 border-l-blue-600 py-3">
                  <div class="text-xs font-bold uppercase text-blue-800 mono">Mục đích 3 • Tính Sizing $W/L$ &amp; Kiểm trước BSIM4</div>
                  <p class="text-sm text-sky-950 mt-1">Dùng phương pháp $g_m/I_D$ tính trọn bộ kích thước $W, L, \\text{nf}, \\text{mult}$ cho 4 khối rồi tự động gọi Ngspice xác minh trước khi bàn giao sang Tuần 3.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Trong 3 mục đích trên, khái niệm cốt lõi nhất là <strong>“Golden Model”</strong> — vậy chính xác Golden Model là gì và nó hoạt động ra sao?",
            footer_text=f_foot,
            speaker_notes="Tuần 2 là giai đoạn Mô hình hóa Hành vi (Behavioral Modeling) và Tính toán Kích thước (Sizing). Không có Tuần 2, kỹ sư sẽ mò mẫm thông số trong SPICE rất chậm và dễ nhầm nguyên nhân lỗi.",
        ),

        # S03: WHAT IS A GOLDEN MODEL
        SlideSpec(
            act_tag="Hồi I — Khái Niệm Cốt Lõi Trong Kiểm Chứng Vi Mạch",
            title="Golden Model (Mô Hình Vàng) Là Gì &amp; Vai Trò Trong Chuỗi Thiết Kế Chip?",
            badge="Single Source of Truth",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-6 ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">Định nghĩa chuẩn công nghiệp Bán dẫn</span>
                  <h3 class="text-lg font-extrabold text-sky-950 mt-1">“Chân Lý Tham Chiếu” Độc Lập Với Transistor</h3>
                  <p class="text-sm text-sky-900 mt-2">
                    <strong>Golden Model</strong> là chương trình mô phỏng thuần toán–vật lý (chính xác 64-bit <span class="code-tag">Float64</span>), chỉ giải phương trình bảo toàn điện tích $H(z)$ và các định luật vật lý cơ bản — hoàn toàn <strong>không phụ thuộc mô hình BSIM4 hay ký sinh dây</strong>.
                  </p>
                </div>
                <div class="gold-card mt-3 py-2.5">
                  <div class="text-xs font-bold text-amber-900 uppercase mono">Ví dụ so sánh dễ hiểu</div>
                  <p class="text-xs text-sky-950 mt-1">
                    Golden Model giống như <strong>bản thiết kế khí động học lý tưởng trong hầm gió số</strong>: nếu kết quả SPICE/Layout lệch xa Golden Model, ta biết ngay sự cố đến từ <em>nội trở khóa, cực phụ OTA hay tụ ký sinh dây</em>!
                  </p>
                </div>
              </div>

              <div class="col-span-6 flex flex-col gap-3 justify-center">
                <div class="ocean-card py-2.5">
                  <div class="flex items-center justify-between"><span class="text-xs font-bold uppercase text-sky-800 mono">1. Cột 1: Golden Model (Tuần 2)</span><span class="badge-ocean">Mốc Gốc 0.00%</span></div>
                  <p class="text-xs text-sky-950 mt-1">$f_{c,\\text{Golden}} = \\mathbf{187.675\\text{ kHz}}$, $\\text{THD} = -316\\text{ dB}$ (số học) &amp; $\\text{SNR}_{kT/C} = \\mathbf{72.09\\text{ dB}}$ (trần nhiệt động).</p>
                </div>
                <div class="ieee-card border-l-4 border-l-blue-600 py-2.5">
                  <div class="flex items-center justify-between"><span class="text-xs font-bold uppercase text-blue-700 mono">2. Cột 2: Pre-Layout SPICE (Tuần 3)</span><span class="badge-blue">Gate: $|\\Delta f_c| &lt; 5\\%$</span></div>
                  <p class="text-xs text-sky-950 mt-1">Đo lưới transistor thật trên Xschem so trực tiếp với sóng bậc thang &amp; phổ FFT của Golden Model ($+3.36\\%$ đạt chuẩn!).</p>
                </div>
                <div class="gold-card border-l-4 border-l-amber-500 py-2.5">
                  <div class="flex items-center justify-between"><span class="text-xs font-bold uppercase text-amber-800 mono">3. Cột 3: Post-Layout PEX (Tuần 4)</span><span class="badge-gold">Gate: 3-Col Match</span></div>
                  <p class="text-xs text-sky-950 mt-1">Ghép cả 3 đường cong (Golden, Pre-Layout, Post-Layout PEX) lên cùng một hệ trục để chứng minh chip thật sau sản xuất vẫn bảo toàn đặc tuyến.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Vậy cụ thể trong Tuần 2, <strong>mô phỏng trên Python là làm những việc gì</strong> và gồm mấy kịch bản mã nguồn?",
            footer_text=f_foot,
            speaker_notes="Golden Model là mô hình toán-lý chuẩn xác bằng số thực 64-bit, đóng vai trò cột tham chiếu số 1 trong bảng đối chiếu 3 cột xuyên suốt Tuần 2, Tuần 3 và Tuần 4.",
        ),

        # S04: WHAT PYTHON SIMULATION DOES
        SlideSpec(
            act_tag="Hồi I — Bức Tranh Toàn Cảnh 3 Mô-Đun Python",
            title="Mô Phỏng Trên Python Là Làm Những Việc Gì? (3 Kịch Bản &amp; 3 Tệp JSON)",
            badge="python/*.py Architecture",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card py-3 px-4">
              __SVG_PIPE__
            </div>

            <div class="grid grid-cols-3 gap-4">
              <div class="ocean-card py-2.5">
                <div class="text-xs font-bold uppercase text-sky-800 mono">Việc 1 • <span class="code-tag">golden_model.py</span></div>
                <ul class="mt-1.5 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>Vẽ &amp; đối chiếu Bode $H(z)$ với $RC$.</li>
                  <li>Chạy quá độ đa tần $50\\text{ kHz}+2\\text{ MHz}$.</li>
                  <li>Chạy <strong>Coherent FFT $N=16384$</strong> (có/không $kT/C$) xuất <span class="code-tag">metrics_golden.json</span>.</li>
                </ul>
              </div>
              <div class="gold-card py-2.5">
                <div class="text-xs font-bold uppercase text-amber-900 mono">Việc 2 • <span class="code-tag-gold">nonideal_budget.py</span></div>
                <ul class="mt-1.5 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>Quét $R_{\\text{on}}$ phi tuyến ($0.3\\to 100\\text{ k}\\Omega$) đo méo hài động Track-and-Hold.</li>
                  <li>Quét $A_{OL}$ ($10\\to 70\\text{ dB}$) đo sai số DC &amp; dịch cực.</li>
                  <li>Tìm điểm ngọt kích thước <span class="code-tag">TG</span> ($W_n/W_p$).</li>
                </ul>
              </div>
              <div class="ieee-card border-sky-400 py-2.5">
                <div class="text-xs font-bold uppercase text-blue-700 mono">Việc 3 • <span class="code-tag">sizing_calc.py</span></div>
                <ul class="mt-1.5 space-y-1 text-xs text-sky-950 list-disc pl-4">
                  <li>Tính tay $g_m/I_D$ giải cứu quỹ áp `ota_5t`.</li>
                  <li>Chốt bảng $W, L, \\text{nf}, \\text{mult}$ cả 4 khối.</li>
                  <li>Tự sinh netlist gọi <strong>Ngspice BSIM4</strong> tiền kiểm chứng trước Tuần 3.</li>
                </ul>
              </div>
            </div>
            """.replace("__SVG_PIPE__", _svg_w2_pipeline()),
            next_question="Mỗi dòng code trong 3 kịch bản Python trên không viết tùy tiện — vậy ta đã <strong>ứng dụng những công thức lý thuyết nào</strong> vào Python?",
            footer_text=f_foot,
            speaker_notes="Mô phỏng Python Tuần 2 gồm 3 việc lớn nối tiếp nhau: (1) Dựng Golden Model Bode/Transient/Coherent FFT; (2) Quét ngân sách lỗi phi lý tưởng; (3) Tính Sizing W/L và tự động gọi Ngspice kiểm tra sơ bộ.",
        ),

        # S05: THEORY -> PYTHON ALGORITHM MAPPING
        SlideSpec(
            act_tag="Hồi I → Hồi II — Cầu Nối Công Thức Lý Thuyết Vào Mã Nguồn Python",
            title="Ứng Dụng Những Công Thức Lý Thuyết Nào Vào Mô Phỏng Trên Python?",
            badge="8 Equations → Python Code",
            badge_tone="gold",
            body_html="""
            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-xs">
                <thead>
                  <tr class="uppercase tracking-wider">
                    <th class="py-2 px-3 text-left">Lý thuyết &amp; Công thức Gốc (Tuần 1)</th>
                    <th class="py-2 px-3 text-left">Hàm / Thuật toán Python (<span class="mono">python/*.py</span>)</th>
                    <th class="py-2 px-3 text-left">Kết quả Định lượng Thu được</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950 text-[11.8px]">
                  <tr><td class="py-1.5 px-3 font-semibold">1. Hàm truyền miền $\\mathcal{Z}$: $H(e^{j\\omega T}) = \\frac{\\alpha}{1-(1-\\alpha)e^{-j\\omega T}}$</td><td class="py-1.5 px-3 mono text-sky-800">freq_response_sc() + arccos(143/144)</td><td class="py-1.5 px-3">$f_{c,\\text{SC}} = \\mathbf{187.675\\text{ kHz}}$ ($-5.66\\%$ vs $RC$)</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">2. Bảo toàn điện tích: $V_{\\text{out}}[n] = \\frac{8}{9}V_{\\text{out}}[n-1]+\\frac{1}{9}V_{\\text{in}}[n]$</td><td class="py-1.5 px-3 mono text-sky-800">scipy.signal.lfilter([1/9],[1,-8/9], x)</td><td class="py-1.5 px-3">Sóng bậc thang ZOH, nén $2\\text{ MHz}$ đi $10.03\\times$</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">3. Lấy mẫu đồng bộ &amp; Hann: $f_0 = \\frac{M}{N}f_{\\text{clk}}, \\gcd(M,N)=1$</td><td class="py-1.5 px-3 mono text-sky-800">rfft(v_ac*hann(16384)) / ENBW(1.5)</td><td class="py-1.5 px-3">$\\text{SFDR}=296.2\\text{ dB}, \\text{THD}=-316.2\\text{ dB}$ (0 rò phổ)</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">4. Nhiễu nhiệt 2 pha: $\\sigma_{\\Phi_1}^2=\\frac{k_BT}{C_1},\\ \\sigma_{\\Phi_2}^2=\\frac{k_BT}{C_{\\text{eq}}}$</td><td class="py-1.5 px-3 mono text-sky-800">simulate_ktc_sc_filter() → $k_BT/C_2$</td><td class="py-1.5 px-3">$v_n = 72.0\\ \\mu\\text{V}_{\\text{rms}}$, $\\text{SNR} = \\mathbf{72.09\\text{ dB}}$ ($11.66\\text{ b}$)</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">5. Bám mẫu phi tuyến: $\\tau(V) = R_{\\text{on}}(V)C_1$, $N_{\\text{sub}}=24$</td><td class="py-1.5 px-3 mono text-sky-800">simulate_nonlinear_ron_thd()</td><td class="py-1.5 px-3">$R_{\\text{on}} &lt; 5\\text{ k}\\Omega \\implies \\text{THD} = \\mathbf{-105.1\\text{ dB}}$</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">6. Đệm hồi tiếp hữu hạn: $A_{\\text{buf}} = \\frac{A_{OL}}{1+A_{OL}}$, Miller $C_{\\text{in}}$</td><td class="py-1.5 px-3 mono text-sky-800">sweep_aol() (10 → 70 dB)</td><td class="py-1.5 px-3">$A_{OL} \\ge 40\\text{ dB} \\implies \\epsilon_A = 0.99\\%, |\\Delta f_c| = 0.94\\%$</td></tr>
                  <tr><td class="py-1.5 px-3 font-semibold">7. Tiêm điện tích &amp; Xuyên xung: $\\Delta V_{\\text{CI}}, \\Delta V_{\\text{CF}}$</td><td class="py-1.5 px-3 mono text-sky-800">sweep_charge_injection() ($W_n: 0.8\\to 16$)</td><td class="py-1.5 px-3">Điểm ngọt $4/12\\ \\mu\\text{m}$: $2.26\\text{ k}\\Omega$, $0.77\\text{ mV}$ (+DUM)</td></tr>
                  <tr class="row-gold"><td class="py-1.5 px-3 font-semibold">8. Định cỡ vùng trung bình: $g_m = (g_m/I_D)\\cdot I_D$, $\\text{GBW}=\\frac{g_m}{2\\pi C_L}$</td><td class="py-1.5 px-3 mono text-amber-900">sizing_calc.py + ngspice -b verify</td><td class="py-1.5 px-3">$A_{OL}=41.6\\text{ dB}, \\text{GBW}=43.9\\text{ MHz}, \\text{PM}=81.3^\\circ$</td></tr>
                </tbody>
              </table>
            </div>
            """,
            next_question="Hãy đi sâu vào chi tiết từng bước: Bước 1 trong <span class=\"code-tag\">golden_model.py</span> mô phỏng đáp ứng tần số Bode $H(z)$ vs. $RC$ như thế nào?",
            footer_text=f_foot,
            speaker_notes="Bảng tổng hợp 8 công thức lý thuyết Tuần 1 và cách chuyển hóa chính xác thành các hàm Python trong golden_model.py, nonideal_budget.py và sizing_calc.py.",
        ),

        # S06: GOLDEN MODEL MATH FOR BODE
        SlideSpec(
            act_tag="Hồi II — Nhiệm vụ 2.1a: Thuật Toán Đáp Ứng Tần Số (<span class=\"code-tag\">golden_model.py</span>)",
            title="Ứng Dụng Hàm Truyền $H(z)$ Để Giải Nghiệm Cắt Rời Rạc Chính Xác",
            badge="Frequency-Domain Math",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-2 gap-5">
              <div class="ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Mô hình Xấp xỉ Liên tục (Mạch RC tương đương)</span>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2.5 my-2.5 text-center text-sm">
                    $$R_{\\text{eq}} = \\frac{1}{f_{\\text{clk}} C_1} = 1\\text{ M}\\Omega \\implies H_{\\text{RC}}(jf) = \\frac{1}{1 + j\\,f / f_{c,\\text{RC}}}$$
                  </div>
                  <ul class="text-sm text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Công thức <span class="code-tag">FC_RC</span> $= \\frac{1}{2\\pi R_{\\text{eq}} C_2} = \\mathbf{198.944\\text{ kHz}}$.</li>
                    <li><strong>Hạn chế:</strong> Coi điện tích truyền liên tục vô hạn bước nhỏ, bỏ qua bản chất lấy mẫu rời rạc chu kỳ $T_{\\text{clk}} = 100\\text{ ns}$.</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-amber-50 border border-amber-200 text-xs text-amber-900 mt-2">
                  Tại Nyquist $5\\text{ MHz}$, $H_{\\text{RC}}$ đoán $-28.04\\text{ dB}, -87.7^\\circ$ (sai lệch vật lý!).
                </div>
              </div>

              <div class="ocean-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-800 mono">2. Mô hình Rời rạc Chính xác ($H(e^{j2\\pi f T_{\\text{clk}}})$)</span>
                  <div class="bg-white border border-sky-300 rounded-lg p-2.5 my-2.5 text-center text-sm">
                    $$H(e^{j\\omega T_{\\text{clk}}}) = \\frac{1/9}{1 - \\frac{8}{9}e^{-j2\\pi f / f_{\\text{clk}}}}, \\quad f_{c,\\text{SC}} = \\frac{f_{\\text{clk}}}{2\\pi}\\arccos\\!\\left(\\frac{143}{144}\\right)$$
                  </div>
                  <ul class="text-sm text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Python quét lưới logarit $2000$ điểm từ $1\\text{ kHz} \\to 5\\text{ MHz}$ (<span class="code-tag">f_clk/2</span>).</li>
                    <li>Tính chính xác $f_{c,\\text{SC}} = \\mathbf{187.675\\text{ kHz}}$ (lệch $-5.664\\%$).</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-white border border-sky-300 text-xs text-sky-950 mt-2">
                  Tại Nyquist ($z = -1$), $H(-1) = \\frac{1/9}{17/9} = \\frac{1}{17} = \\mathbf{-24.61\\text{ dB}},\\ \\angle H = \\mathbf{0^\\circ}$!
                </div>
              </div>
            </div>
            """,
            next_question="Khi chạy hai hàm <span class=\"code-tag\">freq_response_sc()</span> và <span class=\"code-tag\">freq_response_rc()</span> trên Python, đồ thị Bode thực tế khác nhau thế nào?",
            footer_text=f_foot,
            speaker_notes="So sánh trực tiếp công thức Python giữa mô hình RC liên tục (198.944 kHz) và mô hình miền Z chính xác (187.675 kHz), đặc biệt giải thích điểm Nyquist z=-1 cho pha quay về 0 độ.",
        ),

        # S07: WEEK2 BODE PLOT
        SlideSpec(
            act_tag="Hồi II — Nhiệm vụ 2.1a: Kết Quả Đồ Thị Bode Python",
            title="Đồ Thị Bode: Hàm Truyền Rời Rạc $H(z)$ vs. $RC$ Liên Tục",
            badge="week2_bode_sc_vs_rc.png",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-7 fig-frame py-2">
                <img src="figs/week2_bode_sc_vs_rc.png" alt="Bode SC vs RC" class="max-h-[430px] w-auto object-contain" />
              </div>
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="ocean-card border-l-4 border-l-sky-600 py-3">
                  <div class="text-xs font-bold uppercase text-sky-800 mono">1. Dịch tần số cắt $-5.664\\%$</div>
                  <p class="text-sm text-sky-950 mt-1">$f_{c,\\text{SC}} = \\mathbf{187.675\\text{ kHz}}$ thấp hơn $f_{c,\\text{RC}} = 198.944\\text{ kHz}$ do chia điện tích song song $C_1 \\parallel C_2$ ($p_{\\text{SC}} = 8/9 = 0.8889$).</p>
                </div>
                <div class="ieee-card border-l-4 border-l-blue-600 py-3">
                  <div class="text-xs font-bold uppercase text-blue-700 mono">2. Độ suy hao dải chắn chuẩn xác</div>
                  <p class="text-sm text-sky-950 mt-1">Dải thông $50\\text{ kHz}$ chỉ suy hao $\\mathbf{-0.298\\text{ dB}}$, trong khi nhiễu $2\\text{ MHz}$ bị nén $\\mathbf{-20.02\\text{ dB}}$ (giảm $10.03\\times$ biên độ).</p>
                </div>
                <div class="gold-card border-l-4 border-l-amber-500 py-3">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">3. Đặc tính pha tại tần số Nyquist</div>
                  <p class="text-sm text-sky-950 mt-1">Tại $f_{\\text{clk}}/2 = 5\\text{ MHz}$ ($z = -1$), biên độ dừng ở $-24.61\\text{ dB}$ ($1/17$) và pha quay về $0^\\circ$ đặc trưng hệ rời rạc.</p>
                </div>
              </div>
            </div>
            """,
            next_question="Đáp ứng tần số đã khớp — vậy trong miền thời gian thực, Python mô phỏng sóng đầu ra bậc thang khi trộn tín hiệu $50\\text{ kHz}$ với nhiễu $2\\text{ MHz}$ ra sao?",
            footer_text=f_foot,
            speaker_notes="Biểu đồ Bode 300 DPI trích từ golden_model.py xác nhận dịch tần số cắt -5.664%, suy hao 50 kHz -0.30 dB, nén nhiễu 2 MHz -20.02 dB và pha quay về 0 độ ở Nyquist 5 MHz.",
        ),

        # S08: MULTITONE TRANSIENT
        SlideSpec(
            act_tag="Hồi II — Nhiệm vụ 2.1b: Mô Phỏng Quá Độ Miền Thời Gian",
            title="Mô Phỏng Quá Độ Đa Tần: Giải Phương Trình Sai Phân &amp; Bậc Thang ZOH",
            badge="10.03× Interferer Rejection",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-5 flex flex-col gap-3 justify-center">
                <div class="ieee-card py-2.5">
                  <div class="text-xs font-bold uppercase text-sky-700 mono">1. Hàm <span class="code-tag">sc_difference_filter()</span> &amp; Đầu vào 2 tần</div>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$V_{\\text{in}}(t) = 0.9 + 0.30\\sin(2\\pi\\cdot 50\\text{k}\\cdot t) + 0.12\\sin(2\\pi\\cdot 2\\text{M}\\cdot t)$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1 list-disc pl-4">
                    <li>Chuyển về tọa độ AC $x = V_{\\text{in}}[n] - 0.9\\text{ V}$, giải bằng <span class="code-tag">scipy.signal.lfilter([1/9], [1, -8/9], x)</span>.</li>
                    <li><strong>50 kHz:</strong> giữ $289.9\\text{ mV}_p$ ($96.6\\%$); <strong>2 MHz:</strong> nén $120 \\to \\mathbf{11.97\\text{ mV}_p}$.</li>
                  </ul>
                </div>
                <div class="gold-card py-2.5">
                  <div class="text-xs font-bold uppercase text-amber-800 mono">2. Bài học quyết định cho Tuần 3 (Strobe Time)</div>
                  <p class="text-xs text-sky-950 mt-1 leading-relaxed">
                    Dạng sóng ra là bậc thang giữ mẫu bậc không (ZOH, $T_{\\text{clk}} = 100\\text{ ns}$). Do đó ở Tuần 3, ta phải trích mẫu Ngspice đúng tại <strong>cuối pha $\\Phi_2$</strong> ($t_n = nT_{\\text{clk}} + 98\\text{ ns}$) sau khi OTA xác lập xong!
                  </p>
                </div>
              </div>
              <div class="col-span-7 fig-frame py-2">
                <img src="figs/week2_multitone_transient.png" alt="Multi-tone Transient" class="max-h-[430px] w-auto object-contain" />
              </div>
            </div>
            """,
            next_question="Làm sao Python đo chính xác độ tinh khiết phổ ($\text{SFDR, SNR, THD, ENOB}$) tới mức $-300\\text{ dB}$ và mô phỏng trần nhiễu nhiệt $kT/C$?",
            footer_text=f_foot,
            speaker_notes="Hàm plot_multitone_transient chạy 800 chu kỳ (80 us) để minh họa rõ từng bậc thang ZOH 100 ns dập tắt sóng nhiễu 2 MHz từ 120 mVp xuống 11.97 mVp.",
        ),

        # S09: COHERENT FFT & kT/C MATH IN PYTHON
        SlideSpec(
            act_tag="Hồi II — Nhiệm vụ 2.1c: Thuật Toán Coherent FFT &amp; Nhiễu Nhiệt 2 Pha",
            title="Cách Ứng Dụng Lý Thuyết Coherent Sampling &amp; Nhiệt Động $kT/C$ Vào Python",
            badge="Zero Spectral Leakage",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-2 gap-5">
              <div class="ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Phép đo phổ Coherent FFT (<span class="code-tag">coherent_spectral_metrics()</span>)</span>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$f_{\\text{in}} = \\frac{M_{\\text{sig}}}{N_{\\text{FFT}}}f_{\\text{clk}} = \\frac{83}{16384}\\times 10\\text{ MHz} = \\mathbf{50.659\\text{ kHz}}$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li><strong>Loại bỏ quá độ:</strong> Bỏ $2048$ chu kỳ đầu ($(8/9)^{2048} &lt; 10^{-100}$).</li>
                    <li><strong>Nguyên tố cùng nhau:</strong> $\\gcd(83, 16384) = 1$ để mọi mẫu nằm ở pha khác nhau trên chu kỳ sóng, không trùng bin hài.</li>
                    <li><strong>Cửa sổ Hann chuẩn hóa:</strong> Chia cho <span class="code-tag">ENBW = 1.5</span> để tích phân chính xác công suất sóng hài $H_2..H_7$ (kể cả hài gập Nyquist).</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-sky-50 border border-sky-200 text-xs text-sky-900 mt-2">
                  Sàn nhiễu số học 64-bit đạt $\\text{SFDR} = 296.2\\text{ dB}$, chứng minh thuật toán FFT <strong>sạch 0% rò phổ</strong>.
                </div>
              </div>

              <div class="gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">2. Mô hình nhiễu nhiệt 2 pha (<span class="code-tag-gold">simulate_ktc_sc_filter()</span>)</span>
                  <div class="bg-white border border-amber-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$v_{n1} \\sim \\mathcal{N}\\!\\left(0, \\frac{k_B T}{C_1}\\right), \\quad v_{\\Phi_2} \\sim \\alpha\\,\\mathcal{N}\\!\\left(0, \\frac{k_B T}{C_1 \\parallel C_2}\\right)$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Pha $\\Phi_1$: khóa `TG1` lấy mẫu nhiễu phương sai $k_BT/C_1$ lên $C_1$.</li>
                    <li>Pha $\\Phi_2$: khóa `TG2` đóng thêm nhiễu vòng $C_1 \\parallel C_2$ ($C_{\\text{eq}} = \\frac{C_1 C_2}{C_1+C_2}$).</li>
                    <li>Chứng minh giải tích đẳng phân năng lượng: $\\text{Var}(V_{\\text{out}}[\\infty]) \\equiv \\frac{k_B T}{C_2}$!</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-white border border-amber-300 text-xs text-amber-950 mt-2">
                  Cả hai pha cộng lại cho đúng phương sai $\\frac{k_BT}{C_2} \\implies \\sigma = 71.95\\ \\mu\\text{V}_{\\text{rms}}$ ở $300\\text{ K}$.
                </div>
              </div>
            </div>
            """,
            next_question="Kết quả chạy phổ Coherent FFT của Golden Model (có và không có nhiễu $kT/C$) cho các con số trần vật lý nào?",
            footer_text=f_foot,
            speaker_notes="Giải thích chi tiết cách Python tính đúng công suất dBc bằng cửa sổ Hann + ENBW=1.5 và cách mô phỏng đúng cả 2 nguồn nhiễu nhiệt ở pha Phi1 và pha Phi2 để khớp chính xác định lý kT/C2.",
        ),

        # S10: WEEK2 COHERENT FFT RESULTS
        SlideSpec(
            act_tag="Hồi II — Nhiệm vụ 2.1c: Kết Quả Phổ Chuẩn Golden FFT",
            title="Phổ Coherent FFT ($N = 16384$, Hann) &amp; Mốc Chuẩn <span class=\"code-tag\">metrics_golden.json</span>",
            badge="metrics_golden.json",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-7 fig-frame py-2">
                <img src="figs/week2_coherent_fft.png" alt="Coherent FFT Spectrum" class="max-h-[420px] w-auto object-contain" />
              </div>
              <div class="col-span-5 flex flex-col justify-between gap-3">
                <div class="ocean-card py-2.5">
                  <span class="text-xs font-bold uppercase text-sky-800 mono">Thiết lập lấy mẫu đồng bộ (Zero Leakage)</span>
                  <div class="bg-white border border-sky-200 rounded p-2 my-1.5 text-center text-xs">
                    $$f_0 = \\frac{83}{16384}\\times 10\\text{ MHz} = \\mathbf{50.659\\text{ kHz}},\\quad V_{\\text{in,p}} = 0.40\\text{ V}$$
                  </div>
                  <p class="text-xs text-sky-900">Biên độ đỉnh ra: $V_{\\text{out,rms}} = 273.06\\text{ mV}$ ($\\text{SNR}_{\\text{lý thuyết}} = 71.58\\text{ dB}$).</p>
                </div>

                <div class="ieee-card p-0 overflow-hidden">
                  <table class="ieee-table text-xs">
                    <thead>
                      <tr><th class="p-2.5 text-left">Chỉ số Phổ</th><th class="p-2.5 text-right">Float64 Lý tưởng</th><th class="p-2.5 text-right">Kèm nhiễu $kT/C$</th></tr>
                    </thead>
                    <tbody class="divide-y divide-sky-100">
                      <tr><td class="p-2 font-semibold">SNR (dB)</td><td class="p-2 text-right mono">288.69</td><td class="p-2 text-right font-bold text-sky-700 mono">72.09</td></tr>
                      <tr><td class="p-2 font-semibold">SNDR (dB)</td><td class="p-2 text-right mono">288.68</td><td class="p-2 text-right font-bold text-sky-700 mono">71.95</td></tr>
                      <tr><td class="p-2 font-semibold">SFDR (dB)</td><td class="p-2 text-right mono">296.20</td><td class="p-2 text-right font-bold text-blue-700 mono">90.44</td></tr>
                      <tr><td class="p-2 font-semibold">THD (dB)</td><td class="p-2 text-right mono">−316.22</td><td class="p-2 text-right mono">−86.87</td></tr>
                      <tr class="row-gold"><td class="p-2 font-bold">ENOB (bits)</td><td class="p-2 text-right mono">47.66</td><td class="p-2 text-right font-extrabold text-amber-900 mono">11.66</td></tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            """,
            next_question="Lõi $H(z)$ lý tưởng đã đạt $11.66\\text{ bits}$ — nhưng khi dùng transistor thật có $R_{\\text{on}}(V)$ biến thiên phi tuyến, chuyện gì xảy ra với méo hài THD?",
            footer_text=f_foot,
            speaker_notes="Phổ Coherent FFT khẳng định trần vật lý kT/C của tụ C2=800 fF là SNR = 72.09 dB (ENOB = 11.66 bits), làm mốc tham chiếu cho mọi mô phỏng SPICE sau này.",
        ),

        # S11: NONIDEAL BUDGET PART 1 (RON TRACKING THD)
        SlideSpec(
            act_tag="Hồi III — Nhiệm vụ 2.2a: Ngân Sách Phi Lý Tưởng (<span class=\"code-tag\">nonideal_budget.py</span>)",
            title="Mô Phỏng Nội Trở Phi Tuyến $R_{\\text{on}}(V)$: Lý Giải Ngưỡng $R_{\\text{on}} &lt; 5\\text{ k}\\Omega$",
            badge="Dynamic Track-and-Hold THD",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-2 gap-5">
              <div class="gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">1. Hai mức tính toán hoàn toàn khác nhau</span>
                  <ul class="mt-2.5 space-y-2 text-sm text-sky-950 list-disc pl-4">
                    <li><strong>Bài toán Nạp Tĩnh ($\\epsilon_{\\text{set}} &lt; 0.1\\%$):</strong> Trong $t_{\\text{on}} = 47\\text{ ns}$, giải $e^{-47\\text{ ns}/(R_{\\text{on}}C_1)} &lt; 10^{-3}$ chỉ cần <strong>$R_{\\text{on}} &lt; 68.04\\text{ k}\\Omega$</strong>.</li>
                    <li><strong>Bài toán Bám Mẫu Động ($V_{\\text{in}}(t)$ biến thiên):</strong> Khóa `TG1` có đường cong chuông Body Effect đo từ Sky130A:
                      $$R_{\\text{on}}(V) = \\frac{R_{\\text{peak}}}{1 + 4.8\\left(\\frac{V - 0.965}{0.40}\\right)^2}$$
                    </li>
                    <li>Độ trễ bám mẫu $\\Delta V_{\\text{track}} \\approx -R_{\\text{on}}(V_{\\text{in}}) C_1 \\frac{dV_{\\text{in}}}{dt}$ làm biến dạng sóng hình sin thành <strong>hài bậc 3 ($\text{HD}_3$)</strong>!</li>
                  </ul>
                </div>
                <div class="bg-white border border-amber-300 rounded-lg p-2 text-xs font-bold text-amber-900 mt-2">
                  Tại sao phải quét Python? Vì phương trình tích phân theo $t$ liên tục không có nghiệm đóng giải tích!
                </div>
              </div>

              <div class="ocean-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-800 mono">2. Cách Python mô phỏng 24 bước con mỗi pha</span>
                  <div class="bg-white border border-sky-200 rounded-lg p-2 my-2 text-xs text-sky-950 mono">
                    for k in range(24): # dt = 47 ns / 24 = 1.96 ns<br/>
                    &nbsp;&nbsp;tau1 = r_tg(0.5*(v_src + v_c1)) * C1<br/>
                    &nbsp;&nbsp;v_c1 = v_src + (v_c1 - v_src)*exp(-dt/tau1)
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Kiểm tra tại sát biên dải thông $f_{\\text{in}} = \\frac{73}{4096}f_{\\text{clk}} = \\mathbf{178.22\\text{ kHz}}$, $A_{\\text{in}} = 0.40\\text{ V}$.</li>
                    <li>Tại $R_{\\text{peak}} = 60\\text{ k}\\Omega$: $\\text{THD}$ xấu tới $-61.6\\text{ dB}$.</li>
                    <li>Tại ngưỡng chốt <strong>$R_{\\text{peak}} = 5.0\\text{ k}\\Omega$</strong> ($94\\tau$): $\\text{THD} = \\mathbf{-105.1\\text{ dB}}$!</li>
                    <li>Tại cấu hình `TG 4/12 µm` ($2.26\\text{ k}\\Omega$): $\\text{THD} = \\mathbf{-148.9\\text{ dB}}$ (vô hiệu hóa hoàn toàn méo bám mẫu).</li>
                  </ul>
                </div>
                <div class="bg-white border border-sky-300 rounded-lg p-2 text-xs font-bold text-sky-800 text-center mt-2">
                  Khóa cứng chuẩn Gate: $R_{\\text{on,max}} &lt; 5.0\\text{ k}\\Omega$
                </div>
              </div>
            </div>
            """,
            next_question="Bên cạnh $R_{\\text{on}}$, hai khiếm khuyết còn lại là <strong>độ lợi hữu hạn $A_{OL}$ của OTA</strong> và <strong>tiêm điện tích khóa TG</strong> được Python tính như thế nào?",
            footer_text=f_foot,
            speaker_notes="Hàm simulate_nonlinear_ron_thd chia mỗi pha 47 ns thành 24 bước tích phân nhỏ để bắt chính xác méo hài bậc 3 sinh ra từ đường cong Ron(V) hình chuông, chứng minh lý do ép Ron < 5 kOhm.",
        ),

        # S12: NONIDEAL BUDGET PART 2 (AOL & CHARGE INJECTION)
        SlideSpec(
            act_tag="Hồi III — Nhiệm vụ 2.2b: Quét Độ Lợi $A_{OL}$ &amp; Đánh Đổi Diện Tích Khóa TG",
            title="Mô Hình Hóa Độ Lợi Hữu Hạn $A_{OL}$ &amp; Tìm Điểm Ngọt Kích Thước Khóa TG",
            badge="sweep_aol() &amp; sweep_ci()",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-2 gap-5">
              <div class="ieee-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">1. Hàm <span class="code-tag">sweep_aol()</span>: Sai số biên độ &amp; Dịch cực</span>
                  <div class="bg-sky-50 border border-sky-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$\\epsilon_A = 1 - \\frac{A_{OL}}{1+A_{OL}}, \\quad C_{\\text{in,eff}} = C_{gd1} + \\frac{C_{gs1}}{1 + A_{OL}}$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Quét $A_{OL} \\in [10\\text{ dB}, 70\\text{ dB}]$ đánh giá cả sai số đệm DC và độ dịch điểm cực SC.</li>
                    <li>Tại $A_{OL} = 35\\text{ dB}$ ($56.2\\text{ V/V}$): $\\epsilon_A = 1.75\\%$, dịch cực $1.65\\%$.</li>
                    <li>Tại ngưỡng chốt <strong>$A_{OL} \\ge 40\\text{ dB}$</strong> ($100\\text{ V/V}$): sai số biên độ hạ còn <strong>$0.99\\%$ ($0.086\\text{ dB}$)</strong> và dịch cực chỉ <strong>$0.94\\% \\ll 5\\%$</strong>.</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-sky-50 border border-sky-200 text-xs font-bold text-sky-900 mt-2">
                  Khóa cứng chuẩn Gate 5T-OTA: $A_{OL} \\ge 40\\text{ dB}$
                </div>
              </div>

              <div class="gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">2. Hàm <span class="code-tag-gold">sweep_charge_injection()</span>: Đánh đổi $W_n$</span>
                  <div class="bg-white border border-amber-200 rounded-lg p-2 my-2 text-center text-xs">
                    $$R_{\\text{on}} \\propto \\frac{1}{W_n}, \\qquad \\Delta V_{\\text{CI}} = \\frac{\\max(Q_n, Q_p)}{2(C_1+C_2)} \\propto W_n \\cdot L$$
                  </div>
                  <ul class="text-xs text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>Quét $W_n \\in [0.8, 16.0]\\ \\mu\\text{m}$ (giữ tỷ lệ bù $W_p = 3 W_n$, $L = 0.15\\ \\mu\\text{m}$) dùng hằng số BSIM4 thực đo ($C_{ox,n}=8.325, C_{ox,p}=8.163\\text{ fF}/\\mu\\text{m}^2$).</li>
                    <li><strong>Điểm ngọt ($W_n/W_p = 4/12\\ \\mu\\text{m}$, diện tích $2.4\\ \\mu\\text{m}^2$):</strong> $R_{\\text{peak}} = 2.26\\text{ k}\\Omega &lt; 5\\text{ k}\\Omega$, $\\Delta V_{\\text{CI}}(V_{\\text{out}}) = 3.84\\text{ mV}$ (chỉ còn $\\mathbf{0.77\\text{ mV}}$ khi bù Dummy $W/2$).</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-white border border-amber-300 text-xs font-bold text-amber-900 mt-2">
                  Ghi chú sang Tuần 3: Sẽ tinh chỉnh xuống $2/6\\ \\mu\\text{m}$ khi thấy ký sinh $C_{db}$ trên $C_1$!
                </div>
              </div>
            </div>
            """,
            next_question="Đặt cả 3 phép quét phi lý tưởng từ <span class=\"code-tag\">nonideal_budget.py</span> lên biểu đồ thì bức tranh tổng thể trông như thế nào?",
            footer_text=f_foot,
            speaker_notes="sweep_aol chứng minh AOL >= 40 dB giữ sai số dưới 1%; sweep_charge_injection vẽ đường đánh đổi giữa Ron (tỷ lệ nghịch W) và điện áp tiêm điện tích dV_CI (tỷ lệ thuận W) để chốt điểm ngọt ban đầu Wn=4, Wp=12 um.",
        ),

        # S13: NONIDEAL BUDGETS 3-PANEL PLOT
        SlideSpec(
            act_tag="Hồi III — Nhiệm vụ 2.2: Biểu Đồ Tổng Hợp Ngân Sách Phi Lý Tưởng",
            title="Quét Phi Lý Tưởng: Nội Trở $R_{\\text{on}}$, Độ Lợi $A_{OL}$ &amp; Charge Injection",
            badge="week2_nonideal_budgets.png",
            badge_tone="ocean",
            body_html="""
            <div class="fig-frame py-2 px-3">
              <img src="figs/week2_nonideal_budgets.png" alt="Non-ideal Error Budgets" class="max-h-[340px] w-full object-contain" />
            </div>
            <div class="grid grid-cols-3 gap-4 text-xs">
              <div class="ocean-card py-2.5">
                <strong class="text-sky-800">(a) Ngưỡng $R_{\\text{on}} &lt; 5\\text{ k}\\Omega$:</strong>
                <p class="mt-1 text-sky-950">Xác lập tĩnh $&lt;0.1\\%$ chỉ cần $68\\text{ k}\\Omega$, nhưng chốt $&lt;5\\text{ k}\\Omega$ để giữ méo hài bám mẫu động $\\text{THD} &lt; -105\\text{ dB}$.</p>
              </div>
              <div class="ieee-card border-sky-400 py-2.5">
                <strong class="text-blue-800">(b) Ngưỡng $A_{OL} \\ge 40\\text{ dB}$ ($100\\text{ V/V}$):</strong>
                <p class="mt-1 text-sky-950">Giữ sụt độ lợi DC $\\epsilon_A = 0.99\\%$ ($0.086\\text{ dB}$) và độ lệch tần số cắt $|\\Delta f_c / f_c| = 0.94\\% \\ll 5\\%$.</p>
              </div>
              <div class="gold-card py-2.5">
                <strong class="text-amber-900">(c) Điểm ngọt `TG` $W_n/W_p = 4/12\\ \\mu\\text{m}$:</strong>
                <p class="mt-1 text-sky-950">Đạt $R_{\\text{on,peak}} = 2.26\\text{ k}\\Omega$ với $\\Delta V_{\\text{CI}}(V_{\\text{out}}) = 3.84\\text{ mV}$ (còn $\\mathbf{0.77\\text{ mV}}$ khi bù Dummy $W/2$).</p>
              </div>
            </div>
            """,
            next_question="Đã khóa cứng mọi chỉ tiêu cho từng khối ($R_{\\text{on}}&lt;5\\text{ k}\\Omega, A_{OL}\\ge 40\\text{ dB}, \\text{GBW}&gt;10\\text{ MHz}, \\text{PM}\\ge 60^\\circ$) — vậy làm sao tính ra kích thước $W/L$ cụ thể của 5T-OTA trên Sky130A?",
            footer_text=f_foot,
            speaker_notes="3 biểu đồ trích từ nonideal_budget.py: Panel (a) chứng minh Ron < 5 kOhm đạt THD < -105 dB; Panel (b) chứng minh AOL >= 40 dB giữ sai số < 1%; Panel (c) chốt điểm ngọt Wn=4, Wp=12 um.",
        ),

        # S14: GM/ID METHODOLOGY FOR 5T-OTA
        SlideSpec(
            act_tag="Hồi IV — Nhiệm vụ 2.3a: Chiến Lược Sizing 5T-OTA (<span class=\"code-tag\">sizing_calc.py</span>)",
            title="Phương Pháp $g_m/I_D$ Giải Bài Toán Quỹ Áp 5T-OTA Trên Sky130A",
            badge="Moderate Inversion Design",
            badge_tone="gold",
            body_html="""
            <div class="grid grid-cols-2 gap-5">
              <div class="gold-card flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Thách thức Vật lý của PDK Sky130A</span>
                  <h3 class="font-extrabold text-sky-950 text-base mt-1">Tại sao Định luật Bình phương Cổ điển thất bại?</h3>
                  <div class="bg-white border border-amber-300 rounded-lg p-2.5 my-2.5 text-center text-sm">
                    $$V_{\\text{tail}} = V_{\\text{in,cm}} - V_{GS1} &gt; V_{dsat5}$$
                  </div>
                  <ul class="text-sm text-sky-950 space-y-1.5 list-disc pl-4">
                    <li>`nfet_01v8` có $V_{TH,n} \\approx 0.63\\text{–}0.68\\text{ V}$. Nếu chọn vùng nghịch đảo mạnh ($V_{ov1} \\approx 0.20\\text{ V} \\implies V_{GS1} \\approx 0.85\\text{ V}$), thì $V_{\\text{tail}} \\approx 0.05\\text{ V}$ làm `M5` <strong>rơi ngay khỏi bão hòa</strong> tại $V_{CM}=0.9\\text{ V}$!</li>
                    <li>Nếu dùng kênh ngắn $L = 0.15\\ \\mu\\text{m}$, $r_o$ quá nhỏ không thể đạt $A_{OL} &gt; 40\\text{ dB}$.</li>
                  </ul>
                </div>
                <div class="text-xs text-amber-900 font-bold mono mt-2">Phát hiện nhờ đo thực nghiệm BSIM4 từ Tuần 1</div>
              </div>

              <div class="ocean-card border-l-4 border-l-sky-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-800 mono">Giải pháp Sizing Chuẩn Xác bằng $g_m/I_D$</span>
                  <h3 class="font-extrabold text-sky-950 text-base mt-1">Nghịch Đảo Trung Bình ($g_m/I_D = 20.5\\ \\text{V}^{-1}$) + $L = 0.8\\ \\mu\\text{m}$</h3>
                  <div class="bg-white border border-sky-300 rounded-lg p-2.5 my-2.5 text-center text-sm">
                    $$I_{\\text{tail}} = 28.2\\ \\mu\\text{A} \\implies g_{m1} = \\mathbf{289.5\\ \\mu\\text{S}},\\quad r_{o2}\\parallel r_{o4} = \\mathbf{361\\text{ k}\\Omega}$$
                  </div>
                  <ul class="text-sm text-sky-950 space-y-1.5 list-disc pl-4">
                    <li><strong>`M1, M2` ($32 / 0.8\\ \\mu\\text{m}$, `nf=8`):</strong> Hạ $V_{GS1} = 0.662\\text{ V} \\implies V_{\\text{tail}} = \\mathbf{237.5\\text{ mV}}$.</li>
                    <li><strong>`M5, M6` ($24 / 1.0\\ \\mu\\text{m}$, `nf=6`):</strong> Giữ $V_{dsat5} = 100.8\\text{ mV}$ (dư bão hòa $+136.8\\text{ mV}$).</li>
                    <li><strong>Đồng nhất ngón:</strong> Cả `M1–M6` dùng $W_{\\text{finger}} = 4.0\\ \\mu\\text{m}$ cho Layout ABBA Tuần 4.</li>
                  </ul>
                </div>
                <div class="text-xs text-sky-800 font-bold mono mt-2">Công suất tĩnh toàn OTA + Bias: chỉ 104.7 µW • SR = 28.2 V/µs</div>
              </div>
            </div>
            """,
            next_question="Thế còn 3 khối còn lại (`non_overlap_clk`, `tg_switch`, `sc_core`) được tính kích thước $W/L$ và kích thước hình học MIM như thế nào?",
            footer_text=f_foot,
            speaker_notes="Phương pháp gm/Id = 20.5 V^-1 đưa M1, M2 vào vùng nghịch đảo trung bình, hạ VGS1 xuống 0.662 V để giữ Vtail = 237.5 mV dư bão hòa cho M5, đồng thời dùng L=0.8 um để nâng AOL lên 41.62 dB.",
        ),

        # S15: SIZING LOGIC FOR CLK, TG, MIM
        SlideSpec(
            act_tag="Hồi IV — Nhiệm vụ 2.3b: Tính Toán Kích Thước 3 Khối Còn Lại",
            title="Cách Chốt Kích Thước Xung Không Chồng Lấn, Khóa TG &amp; Ô Tụ MIM Đơn Vị",
            badge="Analytical + Grid-Clean Sizing",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-3 gap-4">
              <div class="ieee-card border-t-4 border-t-sky-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-sky-700 mono">Khối 1 • <span class="code-tag">non_overlap_clk</span></span>
                  <h3 class="font-extrabold text-sky-950 text-base mt-1">Chuỗi Trễ Kênh Dài $L=0.95\\ \\mu\\text{m}$</h3>
                  <ul class="mt-2.5 space-y-1.5 text-xs text-sky-950 list-disc pl-4">
                    <li><strong>Chốt `NAND2`:</strong> $W_n=1.6, W_p=2.0\\ \\mu\\text{m}$ (2 NMOS nối tiếp tăng $W_n$ để cân bằng sườn kéo xuống).</li>
                    <li><strong>6 cổng đảo trễ `XDEL1..6`:</strong> Số tầng chẵn giữ nguyên cực tính, tăng chiều dài kênh $L = 0.95\\ \\mu\\text{m}$ giảm dòng nạp tạo đúng <strong>$t_{\\text{nov}} = 2.92\\text{ ns}$</strong> rất gọn diện tích.</li>
                    <li><strong>Đệm xuất `XBUF`:</strong> $W_n/W_p = 2/6\\ \\mu\\text{m}$ (`nf=2`) cho sườn dốc $&lt; 200\\text{ ps}$.</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-sky-50 border border-sky-200 text-xs font-bold text-sky-900 text-center mt-2">
                  Chính giữa dải $[2.0, 5.0]\\text{ ns}$
                </div>
              </div>

              <div class="gold-card border-t-4 border-t-amber-500 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-amber-800 mono">Khối 2 • <span class="code-tag-gold">tg_switch</span></span>
                  <h3 class="font-extrabold text-sky-950 text-base mt-1">Bù Độ Linh Động $W_p / W_n = 3$</h3>
                  <ul class="mt-2.5 space-y-1.5 text-xs text-sky-950 list-disc pl-4">
                    <li>Dùng chiều dài kênh ngắn nhất $L_{\\min} = 0.15\\ \\mu\\text{m}$ để giảm điện tích kênh $Q_{\\text{ch}} \\propto L$ và giảm $R_{\\text{on}}$.</li>
                    <li>Bề rộng PMOS gấp $3\\times$ NMOS ($4/12\\ \\mu\\text{m}$ ở Tuần 2) để cân bằng $\\mu_n/\\mu_p \\approx 2.7$ và ngưỡng $|V_{TH,p}|$ cao.</li>
                    <li><strong>Dự phòng:</strong> Kèm cặp khóa giả `XDUM1,2` ($W/2$, nối tắt D–S) để kiểm chứng triệt gai.</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-white border border-amber-300 text-xs font-bold text-amber-900 text-center mt-2">
                  $R_{\\text{on,max}} = 2.26\\text{ k}\\Omega &lt; 5\\text{ k}\\Omega$
                </div>
              </div>

              <div class="ocean-card border-t-4 border-t-blue-600 flex flex-col justify-between">
                <div>
                  <span class="text-xs font-bold uppercase text-blue-700 mono">Khối 3 • <span class="code-tag">sc_core</span> MIM</span>
                  <h3 class="font-extrabold text-sky-950 text-base mt-1">Bù Độ Xói Biên $dw = 0.15\\ \\mu\\text{m}$</h3>
                  <div class="bg-white border border-sky-200 rounded p-1.5 my-2 text-center text-xs">
                    $$C_A(W+0.15)(L+0.15) = 100.00\\text{ fF}$$
                  </div>
                  <ul class="space-y-1.5 text-xs text-sky-950 list-disc pl-4">
                    <li>Chọn $W_{\\text{eff}}=5.00\\ \\mu\\text{m}, L_{\\text{eff}}=10.00\\ \\mu\\text{m} \\implies$ kích thước vẽ <strong>$4.85 \\times 9.85\\ \\mu\\text{m}$</strong>.</li>
                    <li>Chẵn bước lưới Magic $0.05\\ \\mu\\text{m}$ ($5\\text{ nm}$ grid clean).</li>
                    <li>$C_1$: `mult=1` ($100\\text{ fF}$); $C_2$: `mult=8` ($800\\text{ fF}$).</li>
                  </ul>
                </div>
                <div class="p-2 rounded bg-white border border-sky-300 text-xs font-bold text-blue-800 text-center mt-2">
                  Bảo toàn tuyệt đối $\\alpha = 1/9$
                </div>
              </div>
            </div>
            """,
            next_question="Làm sao biết chắc bảng kích thước $W/L$ vừa tính ở trên chạy đúng với mô hình bán dẫn BSIM4 thật trước khi mở Xschem Tuần 3?",
            footer_text=f_foot,
            speaker_notes="Giải thích rõ cơ sở chọn kích thước từng khối: L=0.95 um cho chuỗi trễ tạo t_nov = 2.92 ns; L=0.15 um & Wp/Wn=3 cho khóa TG; và bù dw=0.15 um cho tụ MIM 4.85x9.85 um khớp bước lưới Magic.",
        ),

        # S16: BSIM4 VERIFICATION IN PYTHON
        SlideSpec(
            act_tag="Hồi IV — Nhiệm vụ 2.3c: Tiền Kiểm Chứng BSIM4 Tự Động Trong Python",
            title="Tiền Kiểm Chứng Ngspice BSIM4: Đáp Ứng 5T-OTA &amp; Xung Không Chồng Lấn",
            badge="week2_ota_bode_and_clk.png",
            badge_tone="ocean",
            body_html="""
            <div class="fig-frame py-2 px-3">
              <img src="figs/week2_ota_bode_and_clk.png" alt="OTA Bode and Clock Verification" class="max-h-[330px] w-full object-contain" />
            </div>
            <div class="grid grid-cols-4 gap-3 text-xs">
              <div class="ocean-card py-2">
                <div class="text-sky-800 font-semibold">Độ lợi vòng hở $A_{OL}$</div>
                <div class="text-lg font-extrabold text-sky-700 mono">41.62 dB</div>
                <div class="text-sky-900 font-bold">✓ PASS (&gt; 40 dB)</div>
              </div>
              <div class="ocean-card py-2">
                <div class="text-sky-800 font-semibold">Băng thông $\\text{GBW}$ ($1\\text{ pF}$)</div>
                <div class="text-lg font-extrabold text-sky-700 mono">43.91 MHz</div>
                <div class="text-sky-900 font-bold">✓ PASS (&gt; 10 MHz)</div>
              </div>
              <div class="gold-card py-2">
                <div class="text-amber-900 font-semibold">Biên dự trữ pha $\\text{PM}$</div>
                <div class="text-lg font-extrabold text-amber-800 mono">81.27°</div>
                <div class="text-amber-900 font-bold">✓ PASS (≥ 60°)</div>
              </div>
              <div class="gold-card py-2">
                <div class="text-amber-900 font-semibold">Khoảng chết $t_{\\text{nov}}$</div>
                <div class="text-lg font-extrabold text-amber-800 mono">2.92 ns</div>
                <div class="text-amber-900 font-bold">✓ PASS (∈ [2, 5] ns)</div>
              </div>
            </div>
            """,
            next_question="Kết quả BSIM4 đã vượt xa mọi ngưỡng Gate — hãy tổng hợp toàn bộ bảng kích thước linh kiện Khối 1–3 để sẵn sàng nhập vào Xschem.",
            footer_text=f_foot,
            speaker_notes="sizing_calc.py tự động sinh netlist SPICE và gọi ngspice -b để tiền kiểm chứng ngay lập tức: 5T-OTA đạt AOL = 41.62 dB, GBW = 43.91 MHz, PM = 81.27 độ; Clock đạt t_nov = 2.92 ns.",
        ),

        # S17: SIZING TABLE BLOCKS 1-3
        SlideSpec(
            act_tag="Hồi IV — Bảng Kích Thước Linh Kiện Chuẩn (Khối 1, 2, 3)",
            title="Bảng Sizing $W/L$ Khối Xung Nhịp, Khóa TG &amp; Lõi Tụ MIM",
            badge="0.05 µm Magic Grid Clean",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-xs">
                <thead>
                  <tr class="uppercase tracking-wider">
                    <th class="py-2.5 px-3.5 text-left">Khối chức năng</th>
                    <th class="py-2.5 px-3.5 text-left">Phần tử</th>
                    <th class="py-2.5 px-3.5 text-left">Linh kiện Sky130A</th>
                    <th class="py-2.5 px-3.5 text-center">$W$ ($\\mu\\text{m}$)</th>
                    <th class="py-2.5 px-3.5 text-center">$L$ ($\\mu\\text{m}$)</th>
                    <th class="py-2.5 px-3.5 text-center">nf / mult</th>
                    <th class="py-2.5 px-3.5 text-left">Vai trò Thiết kế</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950">
                  <tr><td class="py-2 px-3.5 font-bold text-sky-800" rowspan="4">1. non_overlap_clk</td><td class="py-2 px-3.5 mono">XINV_IN</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-semibold">1.0 / 2.5</td><td class="py-2 px-3.5 text-center">0.15</td><td class="py-2 px-3.5 text-center">1 / 1</td><td class="py-2 px-3.5">Đảo pha &amp; làm sắc xung $10\\text{ MHz}$</td></tr>
                  <tr><td class="py-2 px-3.5 mono">XNAND_A, B</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-semibold">1.6 / 2.0</td><td class="py-2 px-3.5 text-center">0.15</td><td class="py-2 px-3.5 text-center">1 / 1</td><td class="py-2 px-3.5">Chốt chéo NAND2 cân bằng sườn</td></tr>
                  <tr><td class="py-2 px-3.5 mono">XDEL1..6 (×2)</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-semibold">0.6 / 1.5</td><td class="py-2 px-3.5 text-center font-bold text-blue-700">0.95</td><td class="py-2 px-3.5 text-center">1 / 1</td><td class="py-2 px-3.5">6 cổng NOT trễ tạo $t_{\\text{nov}} = 2.92\\text{ ns}$</td></tr>
                  <tr><td class="py-2 px-3.5 mono">XBUF1, 2</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-semibold">2.0 / 6.0</td><td class="py-2 px-3.5 text-center">0.15</td><td class="py-2 px-3.5 text-center">2 / 1</td><td class="py-2 px-3.5">Đệm xuất $\\Phi_1, \\overline{\\Phi_1}, \\Phi_2, \\overline{\\Phi_2}$</td></tr>
                  <tr class="row-gold"><td class="py-2 px-3.5 font-bold text-amber-900" rowspan="2">2. tg_switch</td><td class="py-2 px-3.5 mono">XTG1, XTG2</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-bold text-amber-900">4.0 / 12.0 → 2.0 / 6.0*</td><td class="py-2 px-3.5 text-center">0.15</td><td class="py-2 px-3.5 text-center">2,4 → 1,2</td><td class="py-2 px-3.5">Tuần 2: $2.26\\text{ k}\\Omega$; Tuần 3 tinh chỉnh giảm $C_{\\text{par}}$</td></tr>
                  <tr class="row-gold"><td class="py-2 px-3.5 mono">XDUM2</td><td class="py-2 px-3.5 mono">nfet / pfet_01v8</td><td class="py-2 px-3.5 text-center font-semibold">1.0 / 3.0</td><td class="py-2 px-3.5 text-center">0.15</td><td class="py-2 px-3.5 text-center">1 / 1</td><td class="py-2 px-3.5">Khóa giả $W/2$ đặt tại `VX` triệt tiêm điện tích</td></tr>
                  <tr><td class="py-2 px-3.5 font-bold text-sky-900">3. sc_core</td><td class="py-2 px-3.5 mono">XC1 / XC2</td><td class="py-2 px-3.5 mono">cap_mim_m3_1</td><td class="py-2 px-3.5 text-center font-bold">4.85</td><td class="py-2 px-3.5 text-center font-bold">9.85</td><td class="py-2 px-3.5 text-center font-bold text-sky-700">mult = 1 / 8</td><td class="py-2 px-3.5">$100.00\\text{ fF}$ &amp; $800.00\\text{ fF}$ ($1:8$)</td></tr>
                </tbody>
              </table>
            </div>
            <div class="gold-card py-2 px-4 text-xs font-medium text-sky-950">
              <strong>*Lưu ý chuyển tiếp Tuần 2 $\to$ Tuần 3:</strong> Baseline Tuần 2 xuất `TG 4/12 µm`, sau khi đưa vào mô phỏng BSIM4 toàn mạch có ký sinh `AD/AS` ở Tuần 3 sẽ tinh chỉnh gọn về `2.0/6.0 µm` để $C_1$ không bị phình ký sinh!
            </div>
            """,
            next_question="Vậy bảng kích thước chi tiết và biên độ dự trữ bão hòa của cả 5–6 transistor trong khối 4 (`ota_5t`) như thế nào?",
            footer_text=f_foot,
            speaker_notes="Bảng kích thước Block 1-3 tính theo micromet trần (scale=1u), ghi nhận cả giá trị khởi đầu Tuần 2 và bước tinh chỉnh xuống 2/6 um khi gặp ký sinh tụ nhỏ C1=100 fF ở Tuần 3.",
        ),

        # S18: SIZING TABLE BLOCK 4 (5T-OTA)
        SlideSpec(
            act_tag="Hồi IV — Bảng Kích Thước Linh Kiện Chuẩn (Khối 4: 5T-OTA)",
            title="Bảng Sizing <span class=\"code-tag\">ota_5t</span> &amp; Kiểm Chứng Biên Bão Hòa <span class=\"code-tag\">M1–M5</span>",
            badge="All 5 MOSFETs Saturated",
            badge_tone="ocean",
            body_html="""
            <div class="grid grid-cols-12 gap-5">
              <div class="col-span-7 ieee-card p-0 overflow-hidden">
                <table class="ieee-table text-xs">
                  <thead>
                    <tr class="uppercase">
                      <th class="p-3 text-left">Transistor</th>
                      <th class="p-3 text-left">Model</th>
                      <th class="p-3 text-center">$W / L$ ($\\mu\\text{m}$)</th>
                      <th class="p-3 text-center">nf</th>
                      <th class="p-3 text-right">$|V_{DS}| - V_{dsat}$</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-sky-100 text-sky-950">
                    <tr><td class="p-3 font-bold text-sky-700 mono">XM1 (In+)</td><td class="p-3 mono">nfet_01v8</td><td class="p-3 text-center font-bold">32.0 / 0.80</td><td class="p-3 text-center">8</td><td class="p-3 text-right font-bold text-sky-700 mono">+379.5 mV</td></tr>
                    <tr><td class="p-3 font-bold text-sky-700 mono">XM2 (In−)</td><td class="p-3 mono">nfet_01v8</td><td class="p-3 text-center font-bold">32.0 / 0.80</td><td class="p-3 text-center">8</td><td class="p-3 text-right font-bold text-sky-700 mono">+593.0 mV</td></tr>
                    <tr><td class="p-3 font-bold text-amber-700 mono">XM3 (Diode)</td><td class="p-3 mono">pfet_01v8</td><td class="p-3 text-center font-bold">16.0 / 0.80</td><td class="p-3 text-center">4</td><td class="p-3 text-right font-bold text-sky-700 mono">+970.7 mV</td></tr>
                    <tr><td class="p-3 font-bold text-amber-700 mono">XM4 (Mirror)</td><td class="p-3 mono">pfet_01v8</td><td class="p-3 text-center font-bold">16.0 / 0.80</td><td class="p-3 text-center">4</td><td class="p-3 text-right font-bold text-sky-700 mono">+758.0 mV</td></tr>
                    <tr class="row-gold"><td class="p-3 font-bold text-amber-900 mono">XM5, XM6</td><td class="p-3 mono">nfet_01v8</td><td class="p-3 text-center font-bold">24.0 / 1.00</td><td class="p-3 text-center">6</td><td class="p-3 text-right font-bold text-amber-900 mono">+136.8 mV</td></tr>
                  </tbody>
                </table>
              </div>

              <div class="col-span-5 flex flex-col justify-between gap-3">
                <div class="ocean-card py-3">
                  <span class="text-xs font-bold uppercase text-sky-800 mono">Điểm Tĩnh DC Tại $V_{CM} = 0.900\\text{ V}$</span>
                  <ul class="text-sm text-sky-950 space-y-1.5 list-disc pl-4 mt-2">
                    <li>Điện áp ngõ ra tĩnh: $V_{\\text{out}} = \\mathbf{0.8982\\text{ V}}$.</li>
                    <li>Sai số DC Offset hệ thống: $\\mathbf{-1.85\\text{ mV}}$.</li>
                    <li>Điện áp nút đuôi: $V_{\\text{tail}} = \\mathbf{0.2375\\text{ V}}$.</li>
                    <li>Tốc độ quét ước tính: $\\text{SR} = \\mathbf{28.16\\text{ V}/\\mu\\text{s}}$.</li>
                  </ul>
                </div>
                <div class="gold-card py-3">
                  <span class="text-xs font-bold uppercase text-amber-900 mono">Tối Ưu Sẵn Cho Layout ABBA Tuần 4</span>
                  <p class="text-xs text-sky-950 mt-1.5 leading-relaxed">
                    Cả 6 transistor `XM1–XM6` đều có bề rộng ngón đơn vị <strong>$W_{\\text{finger}} = 4.00\\ \\mu\\text{m}$</strong> chẵn, cho phép xếp chồng đối xứng tâm <strong>ABBA</strong> (`M1-M2-M2-M1`) không lệch bước cổng Poly.
                  </p>
                </div>
              </div>
            </div>
            """,
            next_question="Khi đã có trọn bộ `metrics_golden.json` và `sizing_table.json`, quy trình bàn giao tự động sang Tuần 3 Xschem/Ngspice diễn ra như thế nào?",
            footer_text=f_foot,
            speaker_notes="Cả 5 transistor M1-M5 của 5T-OTA đều bão hòa sâu (+136.8 mV trở lên) và đồng nhất W_finger = 4.0 um chuẩn bị sẵn cho bố cục Common-Centroid ABBA ở Tuần 4.",
        ),

        # S19: HANDOFF PIPELINE TO WEEK 3
        SlideSpec(
            act_tag="Hồi V — Quy Trình Ghép Nối Dữ Liệu Sang Tuần 3",
            title="Cầu Nối Tự Động Hóa: Golden Model Python $\\leftrightarrow$ Ngspice Tuần 3",
            badge="Ready for Xschem",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card py-4 px-5">
              __SVG_HANDOFF__
              <div class="grid grid-cols-3 gap-4 mt-3 pt-3 border-t border-sky-200 text-xs text-sky-950">
                <div class="p-2 rounded bg-sky-50 border border-sky-200"><strong>Dải $f_c$ cho phép ở Tuần 3 ($\\pm 5\\%$):</strong> $[178.29\\text{ kHz},\\ 197.06\\text{ kHz}]$ quanh $187.675\\text{ kHz}$.</div>
                <div class="p-2 rounded bg-amber-50 border border-amber-200"><strong>Tần số Coherent Testbench:</strong> $f_{\\text{in}} = \\frac{M}{N}10\\text{ MHz}$ khớp bin nguyên tố với Python FFT.</div>
                <div class="p-2 rounded bg-sky-50 border border-sky-200"><strong>Dự phòng tối ưu:</strong> Kích hoạt khóa giả <span class="code-tag">XDUM</span> ($W/2$) tại nút trở kháng cao nếu gai $\\Delta V_{\\text{CI}}$ gây méo hài.</div>
              </div>
            </div>
            """.replace("__SVG_HANDOFF__", _svg_w2_w3_handoff()),
            next_question="Trước khi chuyển sang vẽ Schematic trên Xschem, hãy chốt lại toàn bộ Cổng kiểm định Gate 2 của Tuần 2.",
            footer_text=f_foot,
            speaker_notes="Quy trình 4 bước khép kín bàn giao từ Tuần 2 sang Tuần 3: nhập sizing_table.json vào Xschem, chạy Gate từng khối, chạy Top Coherent .tran và chạy ngspice_vs_golden.py đối chiếu.",
        ),

        # S20: GATE 2 SIGN-OFF
        SlideSpec(
            act_tag="Hồi V — Verification Gate 2 Sign-Off",
            title="Tổng Kết Cổng Kiểm Định Tuần 2 &amp; Bàn Giao Sang Tuần 3",
            badge="GATE 2: 100% PASSED",
            badge_tone="ocean",
            body_html="""
            <div class="ieee-card p-0 overflow-hidden">
              <table class="ieee-table text-sm">
                <thead>
                  <tr class="text-xs uppercase tracking-wider">
                    <th class="py-2.5 px-4 text-left">Deliverable / Tiêu chuẩn Gate 2</th>
                    <th class="py-2.5 px-4 text-left">File Xuất Thực Tế</th>
                    <th class="py-2.5 px-4 text-left">Chỉ Số Định Lượng Đã Chốt</th>
                    <th class="py-2.5 px-4 text-center">Kết quả</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-sky-100 text-sky-950 text-[13px]">
                  <tr><td class="py-2 px-4 font-semibold">1. Golden Model &amp; Coherent FFT</td><td class="py-2 px-4 mono text-xs">python/metrics_golden.json</td><td class="py-2 px-4">$f_{c,\\text{SC}} = 187.675\\text{ kHz}$, $\\text{SNR}_{kT/C} = 72.09\\text{ dB}$, $\\text{ENOB} = 11.66\\text{ b}$</td><td class="py-2 px-4 text-center"><span class="badge-ocean">PASS</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">2. Ngân sách Phi lý tưởng</td><td class="py-2 px-4 mono text-xs">python/nonideal_budget.json</td><td class="py-2 px-4">$R_{\\text{on}} &lt; 5\\text{ k}\\Omega$ ($\\text{THD} = -105\\text{ dB}$), $A_{OL} \\ge 40\\text{ dB}$ ($\\epsilon_A &lt; 1\\%$)</td><td class="py-2 px-4 text-center"><span class="badge-ocean">PASS</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">3. Bảng Sizing $W/L$ 4 Khối</td><td class="py-2 px-4 mono text-xs">python/sizing_table.json</td><td class="py-2 px-4">$A_{OL} = 41.62\\text{ dB},\\ \\text{GBW} = 43.9\\text{ MHz},\\ \\text{PM} = 81.3^\\circ,\\ t_{\\text{nov}} = 2.92\\text{ ns}$</td><td class="py-2 px-4 text-center"><span class="badge-ocean">PASS</span></td></tr>
                  <tr><td class="py-2 px-4 font-semibold">4. Bộ Đồ Thị Hội Nghị 300 DPI</td><td class="py-2 px-4 mono text-xs">slides/figs/week2_*.png (5 bộ)</td><td class="py-2 px-4">Bode, Multi-tone ZOH, Coherent FFT, Budgets &amp; OTA/Clk</td><td class="py-2 px-4 text-center"><span class="badge-ocean">PASS</span></td></tr>
                  <tr class="row-gold"><td class="py-2 px-4 font-semibold">5. Hồ sơ &amp; Slide Báo cáo Tuần 2</td><td class="py-2 px-4 mono text-xs">slides/week2_slides.html</td><td class="py-2 px-4">20 Slides dẫn dắt Socratic + Công thức Python + Speaker Notes</td><td class="py-2 px-4 text-center"><span class="badge-gold">READY</span></td></tr>
                </tbody>
              </table>
            </div>
            <div class="ocean-card py-2.5 px-5 flex items-center justify-between">
              <div class="text-sm"><span class="text-sky-800 font-bold uppercase mono mr-2">Chuyển tiếp sang Tuần 3:</span>Vẽ 9 Schematic Xschem chuẩn IEEE &amp; chạy mô phỏng Ngspice Pre-Layout BSIM4.</div>
              <span class="badge-gold mono">Lệnh: /tuan 3</span>
            </div>
            """,
            next_question="Bước sang Tuần 3: Tuần 3 là gì, tại sao đã mô phỏng Python rồi vẫn cần vẽ Xschem và chạy Ngspice Pre-Layout BSIM4?",
            footer_text=f_foot,
            speaker_notes="Toàn bộ Verification Gate 2 đã PASS. Ta chuyển sang Tuần 3: hiện thực hóa 4 khối lên Xschem và đối đầu với mô hình transistor BSIM4 thật.",
        ),
    ]
