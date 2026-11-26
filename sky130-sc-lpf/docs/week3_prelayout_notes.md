# TUẦN 3: THIẾT KẾ SCHEMATIC (XSCHEM) & MÔ PHỎNG NGSPICE PRE-LAYOUT (`sky130-sc-lpf`)

**Dự án:** Thiết kế Mạch lọc thông thấp tụ chuyển mạch trên tiến trình SkyWater 130nm (`sky130-sc-lpf`)  
**Tài liệu:** Deliverable Tuần 3 — Hồ sơ Schematic Phân cấp Xschem, Kiểm chứng Ngspice Pre-Layout 4 Khối, Chẩn đoán Ký sinh & Đối chiếu Golden Model  
**Mã nguồn, Schematic & Dữ liệu Kiểm định:**
- Trình sinh Schematic & Netlist Xschem: [build_xschem_schematics.py](file:///headless/ANN/sky130-sc-lpf/python/build_xschem_schematics.py) $\rightarrow$ [xschem/](file:///headless/ANN/sky130-sc-lpf/xschem) & `ngspice/*_xschem.spice`
- Trình phân tích Đối chiếu Golden vs. Pre-Layout: [ngspice_vs_golden.py](file:///headless/ANN/sky130-sc-lpf/python/ngspice_vs_golden.py) $\rightarrow$ [metrics_week3_prelayout.json](file:///headless/ANN/sky130-sc-lpf/python/metrics_week3_prelayout.json)
- Trình chụp màn hình Trạm làm việc EDA 3 cửa sổ: [capture_eda_screenshots.py](file:///headless/ANN/sky130-sc-lpf/python/capture_eda_screenshots.py)
- Slide Báo cáo Tiến độ Tuần 3 (IEEE/ISSCC 16:9): [week3_slides.html](file:///headless/ANN/sky130-sc-lpf/slides/week3_slides.html)

---

## 1. Hệ Thống Schematic Phân Cấp Xschem & Trích Xuất Ký Sinh BSIM4

Toàn bộ cây phân cấp mạch gồm **8 bản vẽ nguyên lý (`.sch`) và ký hiệu đóng gói (`.sym`)** tuân thủ chuẩn thư viện `sky130_fd_pr` (`/foss/pdks/sky130A/libs.tech/xschem`), vượt qua kiểm tra quy tắc điện (ERC `EXIT=0`) và tự động trích xuất đầy đủ diện tích/chu vi tiếp giáp cực Máng – Nguồn (`AD, AS, PD, PS`) khi xuất SPICE netlist (`xschem -n -s`):

| Tầng phân cấp | Schematic (`.sch`) | Symbol (`.sym`) | Netlist SPICE xuất từ Xschem | Chức năng Vật lý |
| :--- | :--- | :--- | :--- | :--- |
| Cell chuẩn số | [inv_cell.sch](file:///headless/ANN/sky130-sc-lpf/xschem/inv_cell.sch) | [inv_cell.sym](file:///headless/ANN/sky130-sc-lpf/xschem/inv_cell.sym) | [inv_cell_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/inv_cell_xschem.spice) | Cổng đảo CMOS tham số hóa `WN, WP, LCH, NF`. |
| Cell chuẩn số | [nand2_cell.sch](file:///headless/ANN/sky130-sc-lpf/xschem/nand2_cell.sch) | [nand2_cell.sym](file:///headless/ANN/sky130-sc-lpf/xschem/nand2_cell.sym) | [nand2_cell_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/nand2_cell_xschem.spice) | Cổng `NAND2` CMOS cân bằng kéo lên / kéo xuống ($1.6 / 2.0\ \mu\text{m}$). |
| **Khối 1** | [non_overlap_clk.sch](file:///headless/ANN/sky130-sc-lpf/xschem/non_overlap_clk.sch) | [non_overlap_clk.sym](file:///headless/ANN/sky130-sc-lpf/xschem/non_overlap_clk.sym) | [non_overlap_clk_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/non_overlap_clk_xschem.spice) | Tạo 4 pha xung $\Phi_1, \overline{\Phi_1}, \Phi_2, \overline{\Phi_2}$ ở $10\text{ MHz}$, $t_{\text{nov}} \approx 3.1\text{ ns}$. |
| **Khối 2** | [tg_switch.sch](file:///headless/ANN/sky130-sc-lpf/xschem/tg_switch.sch) | [tg_switch.sym](file:///headless/ANN/sky130-sc-lpf/xschem/tg_switch.sym) | [tg_switch_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tg_switch_xschem.spice) | Khóa truyền dẫn CMOS tối ưu ($W_n=2\ \mu\text{m}, W_p=6\ \mu\text{m}, L=0.15\ \mu\text{m}$). |
| Cell triệt nhiễu | [tg_dummy.sch](file:///headless/ANN/sky130-sc-lpf/xschem/tg_dummy.sch) | [tg_dummy.sym](file:///headless/ANN/sky130-sc-lpf/xschem/tg_dummy.sym) | [tg_dummy_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tg_dummy_xschem.spice) | Khóa giả $W/2$ nối tắt D–S ($W_n=1\ \mu\text{m}, W_p=3\ \mu\text{m}$) bù điện tích kênh. |
| **Khối 3** | [sc_core.sch](file:///headless/ANN/sky130-sc-lpf/xschem/sc_core.sch) | [sc_core.sym](file:///headless/ANN/sky130-sc-lpf/xschem/sc_core.sym) | [sc_core_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/sc_core_xschem.spice) | Lõi lọc MIM $C_1 = 100\text{ fF}$ (`MF=1`), $C_2 = 800\text{ fF}$ (`MF=8`) + `XDUM2` tại `VX`. |
| **Khối 4** | [ota_5t.sch](file:///headless/ANN/sky130-sc-lpf/xschem/ota_5t.sch) | [ota_5t.sym](file:///headless/ANN/sky130-sc-lpf/xschem/ota_5t.sym) | [ota_5t_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/ota_5t_xschem.spice) | Bộ khuếch đại 5T-OTA + gương dòng phân cực `M6` ($I_{\text{ref}} = 30\ \mu\text{A}$). |
| **Top-Level** | [top_sc_lpf.sch](file:///headless/ANN/sky130-sc-lpf/xschem/top_sc_lpf.sch) | [top_sc_lpf.sym](file:///headless/ANN/sky130-sc-lpf/xschem/top_sc_lpf.sym) | [top_sc_lpf_xschem.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/top_sc_lpf_xschem.spice) | Ghép hoàn chỉnh `XCLK` + `XSC` + `XOTA` hồi tiếp đơn vị ($C_L = 1\text{ pF}$). |

![Schematic Top-Level SC-LPF](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_sch_top_sc_lpf.png)

---

## 2. Kiểm Chứng Độc Lập Từng Khối Con (Unit-Block Pre-Layout Verification)

### 2.1 Nhiệm vụ 3.1 — Khối 1: Bộ Tạo Xung Không Chồng Lấn (`non_overlap_clk`)
- **Testbench:** [tb_clk.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_clk.spice) (`.tran 10p 250n` ở $f_{\text{clk}} = 10\text{ MHz}$, góc công nghệ `tt`, $27^\circ\text{C}$, tải thực tế $25\text{ fF}$ trên cả 4 ngõ ra).
- **Cấu trúc Vật lý:** Chốt chéo `NAND2` kết hợp chuỗi **6 cổng đảo kênh dài** ($W_n = 0.6\ \mu\text{m}, W_p = 1.5\ \mu\text{m}, L = 0.95\ \mu\text{m}$) tạo khoảng chết đối xứng, theo sau bởi bộ đệm ngõ ra 2 tầng (`nf = 2`, $2.0 / 6.0\ \mu\text{m}$). Ngõ ra $\Phi_1, \Phi_2$ được trích ngay sau tầng đệm thứ nhất (`XBUF1A`, `XBUF2A` — số lẻ cổng đảo tính từ hồi tiếp chốt) đảm bảo tính chất **Break-Before-Make** tuyệt đối.
- **Số liệu đo Ngspice ([tb_clk.log](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_clk.log)):**
  - Khoảng chết cạnh $\Phi_1 \downarrow \to \Phi_2 \uparrow$: **$t_{\text{nov},12} = 3.116\text{ ns}$** $\in [2.0\text{ ns}, 5.0\text{ ns}]$ (**PASS**).
  - Khoảng chết cạnh $\Phi_2 \downarrow \to \Phi_1 \uparrow$: **$t_{\text{nov},21} = 3.092\text{ ns}$** $\in [2.0\text{ ns}, 5.0\text{ ns}]$ (**PASS**).
  - Thời gian lên / xuống sườn xung (10%–90%): $t_r = \mathbf{174.4\text{ ps}}$, $t_f = \mathbf{219.5\text{ ps}}$.
  - Tích giao thoa cực đại $\max\big(V(\Phi_1)\cdot V(\Phi_2)\big) = \mathbf{0.00295\text{ V}^2} \approx 0$ (không tồn tại xung nhọn dẫn xuyên).

![Schematic Khối 1 non_overlap_clk](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_sch_non_overlap_clk.png)

![Trạm làm việc Xschem + Xterm + Ngspice Khối 1](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_gui_clk_workstation.png)

---

### 2.2 Nhiệm vụ 3.2 — Khối 2: Khóa Truyền Dẫn CMOS (`tg_switch`)
- **Testbench:** [tb_tg.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_tg.spice) (`.dc Vin 0 1.8 0.005` với nguồn thử vi sai $\Delta V_{DS} = 1\text{ mV}$, đối chiếu trực tiếp khóa đơn NMOS, khóa đơn PMOS và khóa bù CMOS `TG`).
- **Lý giải Vật lý BSIM4:** Trên `sky130A`, PMOS `pfet_01v8` có ngưỡng cao ($|V_{TH,p}| \approx 0.98\text{ V}$ khi có hiệu ứng thân $V_{SB} > 0$) khiến nhánh PMOS chỉ bắt đầu dẫn mạnh khi $V_{\text{in}} > 0.95\text{ V}$, trong khi nhánh NMOS dẫn mạnh từ $0\text{ V} \to 1.05\text{ V}$. Tỷ lệ $W_p / W_n = 6.0\ \mu\text{m} / 2.0\ \mu\text{m} = 3$ san phẳng đỉnh nội trở ngay vùng chuyển giao $V_{\text{in}} \approx 0.955\text{ V}$ mà vẫn giữ điện dung ký sinh cực Máng/Nguồn tối thiểu.
- **Số liệu đo Ngspice ([tb_tg.log](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_tg.log)):**
  - Nội trở tại mức DC chung $V_{CM} = 0.90\text{ V}$: **$R_{\text{on}}(0.9\text{ V}) = 3.713\text{ k}\Omega$**.
  - Nội trở đỉnh toàn dải nguồn ($0\text{ V} \to 1.8\text{ V}$): **$R_{\text{on,max}} = 4.431\text{ k}\Omega < 5.0\text{ k}\Omega$** tại $V_{\text{in}} = 0.955\text{ V}$ (**PASS**).
  - Hằng số thời gian nạp tụ lớn nhất: $\tau_{\max} = R_{\text{on,max}} C_1 = 4.431\text{ k}\Omega \times 100\text{ fF} = \mathbf{0.443\text{ ns}}$, đảm bảo thời gian dẫn thực $t_{\text{on}} \approx 46.9\text{ ns}$ đạt **$105.8\,\tau_{\max}$** (sai số nạp tĩnh $< 10^{-45}$!).

![Schematic Khối 2 tg_switch](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_sch_tg_switch.png)

![Trạm làm việc Xschem + Xterm + Ngspice Khối 2](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_gui_tg_workstation.png)

---

### 2.3 Nhiệm vụ 3.3 — Khối 3 (`sc_core`) & Khối 4 (`ota_5t`: `.op`, `.ac`, `.tran`)
- **Cấu trúc Lõi Tụ MIM ([sc_core.sch](file:///headless/ANN/sky130-sc-lpf/xschem/sc_core.sch)):**
  - Tụ lấy mẫu $C_1$: `sky130_fd_pr__cap_mim_m3_1` kích thước vẽ $W = 4.85\ \mu\text{m}, L = 9.85\ \mu\text{m}, \text{MF} = 1$ ($C_1 = 100.00\text{ fF}$).
  - Tụ tích phân $C_2$: `sky130_fd_pr__cap_mim_m3_1` kích thước vẽ $W = 4.85\ \mu\text{m}, L = 9.85\ \mu\text{m}, \text{MF} = 8$ ($C_2 = 800.00\text{ fF}$, tỷ số ghép mảng đơn vị $C_2/C_1 = 8$).
  - Khóa bù giả `XDUM2` ($W_n = 1.0\ \mu\text{m}, W_p = 3.0\ \mu\text{m}$) đặt chọn lọc tại nút tích phân trở kháng cao `VX`.

![Schematic Khối 3 sc_core](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_sch_sc_core.png)

- **Kiểm chứng Bộ Đệm 5T-OTA ([tb_ota.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_ota.spice) & [tb_ota.log](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_ota.log)):**
  - Mạch đo vòng hở `.ac` dùng mắt lọc hồi tiếp DC siêu trầm ($L_{\text{fb}} = 1\text{ GH}, C_{\text{fb}} = 1\text{ GF}$) giữ điểm làm việc tự nhiên quanh $V_{CM} = 0.9\text{ V}$ với tải chuẩn $C_L = 1\text{ pF}$ và dòng chuẩn $I_{\text{ref}} = 30\ \mu\text{A}$ ($I_{\text{tail}} = 28.17\ \mu\text{A}$).
  - Mạch đo bước nhảy lớn `.tran` mắc hồi tiếp đơn vị trực tiếp, kích thích xung vuông $0.70\text{ V} \leftrightarrow 1.10\text{ V}$ ($\Delta V = 400\text{ mV}_{\text{pp}}$).

| Transistor / Thông số 5T-OTA | Kích thước ($W / L, \text{nf}$) | Điểm làm việc / Kết quả đo BSIM4 | Ngưỡng Gate 3 | Đánh giá |
| :--- | :---: | :---: | :---: | :---: |
| `XM1` (NMOS vi sai `+`) | $32.0 / 0.80\ \mu\text{m}$ (`nf=8`) | $V_{DS} - V_{dsat} = \mathbf{+379.2\text{ mV}}$ ($g_m = 289.5\ \mu\text{S}$) | $> 0\text{ mV}$ (Bão hòa) | **PASS** |
| `XM2` (NMOS vi sai `-`) | $32.0 / 0.80\ \mu\text{m}$ (`nf=8`) | $V_{DS} - V_{dsat} = \mathbf{+592.9\text{ mV}}$ | $> 0\text{ mV}$ (Bão hòa) | **PASS** |
| `XM3` (PMOS gương diode) | $16.0 / 0.80\ \mu\text{m}$ (`nf=4`) | $V_{SD} - V_{dsat} = \mathbf{+970.5\text{ mV}}$ | $> 0\text{ mV}$ (Bão hòa) | **PASS** |
| `XM4` (PMOS tải chủ động) | $16.0 / 0.80\ \mu\text{m}$ (`nf=4`) | $V_{SD} - V_{dsat} = \mathbf{+757.6\text{ mV}}$ | $> 0\text{ mV}$ (Bão hòa) | **PASS** |
| `XM5` (NMOS nguồn đuôi) | $24.0 / 1.00\ \mu\text{m}$ (`nf=6`) | $V_{DS} - V_{dsat} = \mathbf{+136.6\text{ mV}}$ ($I_D = 28.17\ \mu\text{A}$) | $> 0\text{ mV}$ (Bão hòa) | **PASS** |
| Độ lợi vòng hở DC ($A_{OL}$) | — | **$41.62\text{ dB}$** ($120.5\text{ V/V}$) | $> 35\text{–}40\text{ dB}$ | **PASS** |
| Băng thông độ lợi đơn vị ($\text{GBW}$) | $C_L = 1\text{ pF}$ | **$43.61\text{ MHz}$** ($4.36\times f_{\text{clk}}$) | $> 10\text{ MHz}$ | **PASS** |
| Dự trữ pha ($\text{PM}$) | $C_L = 1\text{ pF}$ | **$81.05^\circ$** (không vọt lố) | $\ge 60^\circ$ | **PASS** |
| Tốc độ quét ($\text{SR}^+ / \text{SR}^-$) | Bước $0.4\text{ V}$ | **$22.92\text{ V}/\mu\text{s}$ / $21.72\text{ V}/\mu\text{s}$** | Xác lập $< 18\text{ ns}$ | **PASS** |
| Điện áp lệch tĩnh (DC Offset) | Hồi tiếp đơn vị | **$-1.85\text{ mV}$** ($V_{\text{out,DC}} = 0.89815\text{ V}$) | $|\Delta V_{\text{os}}| < 5\text{ mV}$ | **PASS** |

![Schematic Khối 4 ota_5t](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_sch_ota_5t.png)

![Trạm làm việc Xschem + Xterm + Ngspice Khối 4](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_gui_ota_workstation.png)

![Tổng hợp Đặc tuyến Kiểm chứng 3 Khối Cơ sở](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_unit_blocks_summary.png)

---

## 3. Nhiệm Vụ 3.4 — Ghép Toàn Mạch (`top_sc_lpf`), Chẩn Đoán Ký Sinh & Tối Ưu Hóa

### 3.1 Phương pháp đo kiểm miền thời gian cho hệ Tụ Chuyển Mạch (Periodic Time-Varying)
Vì các khóa `XTG1, XTG2` đóng ngắt tuần hoàn theo xung nhịp lớn $1.8\text{ V}$, phép phân tích tuyến tính hóa quanh một điểm tĩnh duy nhất (`.ac`) bị vô hiệu (một nhánh khóa luôn hở ở $t=0$). Hai kịch bản `.tran` chính xác cao được xây dựng:
1. **Đo Đáp ứng Biên độ Bode Đa tần Đồng bộ ([tb_top_bode.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_top_bode.spice)):** Kích thích tổng 11 sóng sin đồng bộ pha Schroeder trải đều từ $39.06\text{ kHz}$ đến $3.125\text{ MHz}$ ($N = 256$ chu kỳ sau $64$ chu kỳ xác lập, tổng $32.0\ \mu\text{s}$), trích mẫu $V_{\text{out}}$ đúng vào thời điểm cuối pha tích phân $\Phi_2$ ($t_n = nT_{\text{clk}} + 98\text{ ns}$) để dựng hàm truyền rời rạc thực tế $|H_{\text{Pre}}(e^{j\omega T_{\text{clk}}})|$.
2. **Đo Độ Tinh Khiết Phổ Coherent FFT ([tb_top_sc_lpf.spice](file:///headless/ANN/sky130-sc-lpf/ngspice/tb_top_sc_lpf.spice)):** Sóng sin đơn âm đồng bộ $f_0 = \frac{3}{512} f_{\text{clk}} = \mathbf{58.59375\text{ kHz}}$ ($A_{\text{in}} = 0.20\text{ V}_{\text{p}}$ quanh $V_{CM} = 0.9\text{ V}$, $64$ chu kỳ xác lập + $512$ chu kỳ FFT = $57.6\ \mu\text{s}$).

![Trạm làm việc Xschem + Xterm + Ngspice Toàn mạch top_sc_lpf](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_gui_top_workstation.png)

### 3.2 Nhật Ký Kỹ Thuật: Chẩn Đoán Ký Sinh Nút `V1` & Đột Phá Tối Ưu Hóa (Iteration 1 $\rightarrow$ Iteration 2)

Khi chạy kiểm chứng toàn mạch lần đầu (**Iteration 1**) với kích thước dự kiến từ Tuần 2 (`TG 4.0/12.0 µm` kèm cả hai khóa giả `XDUM1 2.0/6.0 µm` tại nút giữa `V1` và `XDUM2 2.0/6.0 µm` tại nút tích phân `VX`), phân tích BSIM4 phát hiện hiệu ứng vật lý cực kỳ quan trọng:

1. **Nguyên nhân dịch tần số cắt $+22.69\%$ ở Iteration 1:**
   - Tụ chuyển mạch $C_1 = 100\text{ fF}$ có giá trị nhỏ. Khi đặt khóa lớn `TG 4/12 µm` (tổng bề rộng $16\ \mu\text{m}$ trên mỗi phía) **cộng thêm** khóa giả `XDUM1` ($8\ \mu\text{m}$ bật dẫn trong pha $\Phi_2$!), tổng điện dung kênh của `XDUM1` và điện dung tiếp giáp phi tuyến $C_{db}(V) + C_{sb}(V)$ của `XTG1, XTG2` mắc song song trực tiếp với $C_1$ lên tới **$\Delta C_{p,V1} \approx 22.7\text{ fF}$**!
   - Điện dung lấy mẫu hiệu dụng bị phình lên $C_{1,\text{eff}} \approx 122.7\text{ fF} \implies R_{\text{eq,eff}} = \frac{1}{f_{\text{clk}} C_{1,\text{eff}}}$ giảm còn $815\text{ k}\Omega$, đẩy tần số cắt vọt lên **$f_{c,\text{Iter1}} = 230.26\text{ kHz}$** (lệch $+22.69\%$ so với Golden $187.675\text{ kHz}$ — vượt ngưỡng $5\%$!), đồng thời điện dung tiếp giáp phụ thuộc điện áp $C_j(V)$ làm xuất hiện hài bậc hai $HD_2 = -47.78\text{ dBc}$ ($\text{SFDR} = 47.84\text{ dB}$).
2. **Giải pháp Thiết kế Tối ưu ở Iteration 2 (Chốt chính thức):**
   - **Loại bỏ hoàn toàn `XDUM1` khỏi nút `V1`:** Ở mỗi pha lấy mẫu $\Phi_1$, nguồn tín hiệu trở kháng thấp $V_{\text{in}}$ nạp trực tiếp lên $C_1$ và xóa sạch mọi điện tích dư của chu kỳ trước; do đó nút `V1` **không tích lũy sai số tiêm điện tích qua nhiều chu kỳ** và không cần khóa giả!
   - **Thu gọn `XTG1, XTG2` về kích thước tối ưu $W_n = 2.0\ \mu\text{m}\ (\text{nf}=1), W_p = 6.0\ \mu\text{m}\ (\text{nf}=2), L = 0.15\ \mu\text{m}$:** Giảm một nửa diện tích tiếp giáp S/D trên nút `V1` ($\Delta C_{p,V1}$ giảm xuống chỉ còn $\approx 3.36\text{ fF}$!) trong khi vẫn giữ chắc chắn $R_{\text{on,max}} = 4.43\text{ k}\Omega < 5.0\text{ k}\Omega$ ($106\tau$ nạp tụ).
   - **Giữ khóa giả nửa kích thước `XDUM2` ($W_n = 1.0\ \mu\text{m}, W_p = 3.0\ \mu\text{m}$) duy nhất tại nút tích phân `VX` ($C_2 = 800\text{ fF}$):** Đây là nút trở kháng cao thực sự lưu giữ trạng thái bộ lọc ở cuối pha $\Phi_2$. Nhờ `XDUM2`, độ lệch bệ DC (*DC Pedestal*) trên toàn mạch giảm còn **$-1.90\text{ mV}$** — sát khít mức Offset tĩnh tự nhiên của riêng bộ đệm 5T-OTA ($-1.85\text{ mV}$), tức **sai số tiêm điện tích ròng của khóa chuyển mạch chỉ còn $-52\ \mu\text{V}$** (giảm $36\times$ so với $-1.90\text{ mV}$ ròng ở Iteration 1!).

| Chỉ tiêu Toàn Mạch (`top_sc_lpf`) | Golden Model Lý Tưởng ($H(z)$) | Pre-Layout Iter 1 (`TG 4/12` + `DUM1,2`) | Pre-Layout Iter 2 Tối Ưu (`TG 2/6` + `VX DUM2`) | Mức Cải Thiện / Đánh Giá Gate 3 |
| :--- | :---: | :---: | :---: | :---: |
| Tần số cắt $-3\text{ dB}$ ($f_c$) | **$187.675\text{ kHz}$** | $230.260\text{ kHz}$ ($+22.69\%$) | **$193.972\text{ kHz}$** (**$+3.36\%$**) | **PASS** ($|\Delta f_c| < 5.0\%$) |
| Biên độ cơ bản $V_{\text{out,p}}$ ($58.59\text{ kHz}$) | $190.90\text{ mV}_{\text{p}}$ | $183.48\text{ mV}_{\text{p}}$ ($-0.34\text{ dB}$) | **$189.38\text{ mV}_{\text{p}}$** ($-0.07\text{ dB}$) | Khớp lý thuyết $1/(1+A_{OL}^{-1})$ |
| Dải động không nhiễu giả (**SFDR**) | $149.50\text{ dB}$ | $47.84\text{ dB}$ | **$54.14\text{ dB}$** | Tăng **$+6.30\text{ dB}$** (**PASS**) |
| Tổng méo hài (**THD**) | $-146.07\text{ dB}$ | $-47.57\text{ dB}$ ($0.418\%$) | **$-53.67\text{ dB}$** (**$0.207\%$**) | Giảm méo **$2.02\times$** (**PASS**) |
| Tỷ số Tín hiệu / Nhiễu + Méo (**SNDR**) | $146.02\text{ dB}$ | $47.56\text{ dB}$ ($7.61\text{ bits}$) | **$53.66\text{ dB}$** (**$8.62\text{ bits}$**) | Tăng **$+1.01\text{ ENOB bits}$** |
| Hài bậc 2 / bậc 3 ($HD_2 / HD_3$) | $<-148\text{ dBc}$ | $-47.78 / -53.42\text{ dBc}$ | **$-54.06 / -59.13\text{ dBc}$** | Triệt mạnh phi tuyến tiếp giáp |
| Độ lệch DC ngõ ra ($\overline{V_{\text{out}}} - V_{CM}$) | $0.00\text{ mV}$ | $-3.75\text{ mV}$ ($\Delta_{\text{CI}} = -1.90\text{ mV}$) | **$-1.90\text{ mV}$** ($\Delta_{\text{CI}} = \mathbf{-0.05\text{ mV}}$) | Khử $97.3\%$ lệch DC chuyển mạch |

![Đối chiếu Dạng sóng Bậc thang và Đáp ứng Bode Golden vs. Ngspice](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_prelayout_vs_golden_time_bode.png)

![Đối chiếu Phổ Coherent FFT Golden vs. Pre-Layout Iter 1 & Iter 2](file:///headless/ANN/sky130-sc-lpf/slides/figs/w3_prelayout_vs_golden_fft.png)

---

## 4. Tổng Kết Cổng Kiểm Định Tuần 3 (Verification Gate 3 — 100% PASS)

- [x] **Khối 1 (`non_overlap_clk`):** $t_{\text{nov},12} = 3.12\text{ ns},\ t_{\text{nov},21} = 3.09\text{ ns} \in [2, 5]\text{ ns}$, không chồng lấn pha.
- [x] **Khối 2 (`tg_switch`):** $R_{\text{on}}(0.9\text{ V}) = 3.71\text{ k}\Omega,\ R_{\text{on,max}} = 4.43\text{ k}\Omega < 5\text{ k}\Omega$ trên toàn dải $0 \to 1.8\text{ V}$.
- [x] **Khối 3 & 4 (`sc_core` & `ota_5t`):** Toàn bộ `M1–M5` bão hòa sâu ($\ge +136.6\text{ mV}$), $A_{OL} = 41.62\text{ dB}$, $\text{GBW} = 43.61\text{ MHz}$, $\text{PM} = 81.05^\circ \ge 60^\circ$.
- [x] **Toàn mạch Pre-Layout (`top_sc_lpf`):** $f_{c,\text{Pre}} = 193.972\text{ kHz}$, lệch **$+3.36\% < 5\%$** so với Golden Model ($187.675\text{ kHz}$); đạt $\text{SFDR} = 54.14\text{ dB}$, $\text{THD} = -53.67\text{ dB}$ ($0.207\%$).
- [x] **Trực quan hóa chuẩn IEEE/ISSCC:** 5 bản vẽ Schematic 300 DPI + 4 ảnh chụp trạm làm việc trực tiếp (`Xschem + Xterm + Ngspice Plot`) + 3 bộ đồ thị đối chiếu 300 DPI + bộ 12 Slide [week3_slides.html](file:///headless/ANN/sky130-sc-lpf/slides/week3_slides.html) sẵn sàng chuyển sang **Tuần 4 (Magic VLSI Layout, DRC/LVS & Post-Layout PEX)**.
