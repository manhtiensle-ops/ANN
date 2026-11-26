# SKY130-SC-LPF — Switched-Capacitor Low-Pass Filter on SkyWater 130nm

Dự án thiết kế hoàn chỉnh vi mạch tương tự **Bộ lọc Thông thấp Tụ chuyển mạch (Switched-Capacitor Low-Pass Filter)** trên tiến trình thương mại mã nguồn mở **SkyWater 130nm (`sky130A`)**, thực hiện khép kín từ lý thuyết Razavi, mô hình hóa Python, schematic Xschem & Ngspice BSIM4 cho đến layout Magic GDSII, sign-off DRC/LVS và hậu kiểm ký sinh Post-Layout PEX.

---

## 1. Thông số Thiết kế Chính (Specifications)

| Thông số | Giá trị Chốt | Ghi chú |
| :--- | :--- | :--- |
| **Công nghệ & PDK** | SkyWater 130nm (`sky130A`) | Planar CMOS, $L_{\min} = 0.15\ \mu\text{m}$, $V_{DD} = 1.8\text{ V}$, $V_{CM} = 0.9\text{ V}$ |
| **Xung nhịp chuyển mạch** | $f_{\text{clk}} = 10\text{ MHz}$ | $T_{\text{clk}} = 100\text{ ns}$, bán chu kỳ $50\text{ ns}$ |
| **Tụ đơn vị MIM (`cap_mim_m3_1`)** | $C_1 = 100\text{ fF}$ ($1\times C_u$), $C_2 = 800\text{ fF}$ ($8\times C_u$) | Mảng $5\times 5$ Common-Centroid (+16 Dummy bảo vệ), $\alpha = \frac{1}{9}$ |
| **Điện trở tương đương SC** | $R_{\text{eq}} = \frac{1}{f_{\text{clk}} C_1} = 1\text{ M}\Omega$ | $f_{c,\text{RC}} \approx 198.94\text{ kHz}$ (xấp xỉ liên tục) |
| **Tần số cắt $-3\text{ dB}$ rời rạc** | $f_{c,\text{SC}} = 187.675\text{ kHz}$ | Hàm truyền miền $Z$: $H(z) = \frac{\alpha}{1 - (1-\alpha)z^{-1}}$ |
| **Kiến trúc 4 khối** | `non_overlap_clk`, `tg_switch`, `sc_core`, `ota_5t` | Ký hiệu chuẩn IEEE/ANSI trên Xschem (`9` cell, `ERC = 0`) |

---

## 2. Bảng Đối chiếu Kết quả 3 Cột (Verification Gates 1–4)

| Hạng mục Kiểm định | Golden (Tuần 2) | Pre-Layout (Tuần 3) | Post-Layout PEX (Tuần 4) | Trạng thái |
| :--- | :---: | :---: | :---: | :---: |
| **Tần số cắt $-3\text{ dB}$ ($f_c$)** | `187.675 kHz` | `193.972 kHz` (`+3.36%`) | `203.453 kHz` (`+4.89%` vs Pre) | **PASS** |
| **Suy hao thông dải (@ `39 kHz`)** | `-0.184 dB` | `-0.244 dB` | `-0.288 dB` (`Δ = -0.104 dB`) | **PASS** |
| **SFDR (512-pt Coherent FFT)** | `149.50 dB` (Float64) | `54.14 dB` | `53.60 dB` | **PASS** |
| **THD / ENOB** | `-146.07 dB` / `23.96 b` | `-53.67 dB` (`0.207%`) / `8.62 b` | `-52.85 dB` (`0.228%`) / `8.49 b` | **PASS** |
| **Clock $t_{\text{nov},12} / t_{\text{nov},21}$** | `2.92 ns` (ref) | `3.116 / 3.092 ns` | `3.81 / 3.73 ns` | **PASS** |
| **Khóa CMOS $R_{\text{on}}(0.9\text{ V})$** | `< 5.0 kΩ` | `3.713 kΩ` (max `4.431 kΩ`) | `4.566 kΩ` | **PASS** |
| **5T-OTA ($A_{OL} / \text{GBW} / \text{PM}$)** | `41.6 dB / 43.9 MHz / 81.3°` | `41.62 dB / 43.61 MHz / 81.05°` | `41.62 dB / 42.87 MHz / 80.45°` | **PASS** |
| **Công suất (@ `1.8 V`)** | — | `107.56 µW` (`59.76 µA`) | `116.06 µW` (`64.48 µA`) | **PASS** |
| **Physical Sign-Off (GDSII)** | — | `9` Xschem cells (`ERC = 0`) | Magic DRC=`0`, KLayout DRC=`0`, Netgen LVS=`Unique Match` (`10/10`) | **PASS** |

- **Kích thước Die (`layout/top_sc_lpf.gds`):** `149.30 × 101.30 µm` (`0.015124 mm²`).
- **Tổng tụ ký sinh PEX (`ext2spice cthresh 0`):** `123` tụ ghép (`284.191 fF`).

---

## 3. Cấu trúc Thư mục

```text
sky130-sc-lpf/
├── GEMINI.md                   # Quy tắc thiết kế & Single Source of Truth
├── env_sky130.sh               # Thiết lập biến môi trường PDK=sky130A trong iic-osic-tools
├── docs/                       # Kế hoạch 4 tuần (PROJECT_PLAN.md) & ghi chép kỹ thuật tuần 1–4
├── python/                     # Mô hình Golden, Error Budget, Sizing W/L, phân tích Ngspice & build slide
├── xschem/                     # 9 file Schematic & Symbol Xschem chuẩn IEEE/ANSI (ERC = 0)
├── ngspice/                    # Testbench (.spice) & log đo kiểm Pre-Layout / Post-Layout PEX
├── layout/                     # File Magic (.mag), GDSII (top_sc_lpf.gds), PEX netlist, báo cáo DRC & LVS
└── slides/                     # Bộ slide 16:9 Trắng–Xanh biển–Vàng + 31 hình 300 DPI (index + week1..4)
```

---

## 4. Tái lập & Trình chiếu Slide

1. **Nạp môi trường PDK `sky130A`:**
   ```bash
   source env_sky130.sh
   ```
2. **Biên dịch lại toàn bộ bộ slide HTML (79 slides):**
   ```bash
   python3 python/build_all_slides.py
   ```
   - Trọn bộ 4 tuần: `slides/index.html` (79 slides)
   - Từng tuần: `slides/week1_slides.html` (20), `week2_slides.html` (20), `week3_slides.html` (20), `week4_slides.html` (19)
   - Phím tắt trình chiếu: `←` / `→` chuyển slide, `N` bật/tắt Speaker Notes, `Ctrl + P` xuất PDF 16:9.
