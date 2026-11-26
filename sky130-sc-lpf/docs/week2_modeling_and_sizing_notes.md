# TUẦN 2: MÔ HÌNH HÓA PYTHON (GOLDEN MODEL), NGÂN SÁCH PHI LÝ TƯỞNG & SIZING $W/L$ (`sky130-sc-lpf`)

**Dự án:** Thiết kế Mạch lọc thông thấp tụ chuyển mạch trên tiến trình SkyWater 130nm (`sky130-sc-lpf`)  
**Tài liệu:** Deliverable Tuần 2 — Hồ sơ Golden Model, Ngân sách Lỗi Transistor & Bảng Sizing $W/L$ Sẵn sàng Nhập Xschem  
**Mã nguồn & Dữ liệu JSON:**
- [golden_model.py](file:///headless/ANN/sky130-sc-lpf/python/golden_model.py) $\rightarrow$ [metrics_golden.json](file:///headless/ANN/sky130-sc-lpf/python/metrics_golden.json)
- [nonideal_budget.py](file:///headless/ANN/sky130-sc-lpf/python/nonideal_budget.py) $\rightarrow$ [nonideal_budget.json](file:///headless/ANN/sky130-sc-lpf/python/nonideal_budget.json)
- [sizing_calc.py](file:///headless/ANN/sky130-sc-lpf/python/sizing_calc.py) $\rightarrow$ [sizing_table.json](file:///headless/ANN/sky130-sc-lpf/python/sizing_table.json)

---

## 1. Nhiệm vụ 2.1 — Mô Hình Chuẩn Lý Tưởng (`python/golden_model.py`)

### 1.1 Đối chiếu Đáp ứng Tần số Bode: $H(z)$ Rời rạc vs. $RC$ Liên tục
Từ phương trình sai phân bảo toàn điện tích 2 pha quanh $V_{CM} = 0.9\text{ V}$:
$$V_{\text{out}}[n] = \frac{8}{9}V_{\text{out}}[n-1] + \frac{1}{9}V_{\text{in}}[n], \qquad H\left(e^{j2\pi f T_{\text{clk}}}\right) = \frac{1/9}{1 - \frac{8}{9}e^{-j2\pi f / 10\text{ MHz}}}$$

| Chỉ số đặc trưng | Mạch $RC$ liên tục xấp xỉ | Golden Model SC $H(z)$ chính xác | Độ lệch / Ý nghĩa Vật lý |
| :--- | :---: | :---: | :--- |
| Điện trở tương đương $R_{\text{eq}}$ | $1.000\text{ M}\Omega$ | $1/(f_{\text{clk}} C_1) = 1.000\text{ M}\Omega$ | Khớp tuyệt đối ở giới hạn $f \ll f_{\text{clk}}$. |
| Tần số cắt $-3\text{ dB}$ ($f_c$) | $198.944\text{ kHz}$ | **$187.675\text{ kHz}$** | **$-5.664\%$** do $C_1 \parallel C_2$ ở $\Phi_2$ (cực $8/9 = 0.8889 > e^{-1/8}$). |
| Độ lợi dải thông tại $50\text{ kHz}$ | $-0.266\text{ dB}$ | **$-0.298\text{ dB}$** ($0.966\text{ V/V}$) | Bảo toàn biên độ tín hiệu dải thông. |
| Độ suy hao nhiễu tại $2\text{ MHz}$ | $-20.09\text{ dB}$ | **$-20.022\text{ dB}$** ($0.0997\text{ V/V}$) | Triệt nhiễu cao tần **$10.03\times$** về biên độ. |
| Độ suy hao tại Nyquist ($5\text{ MHz}$) | $-28.04\text{ dB}$ | **$-24.609\text{ dB}$** ($\angle H = 0^\circ$) | Điểm gấp phổ rời rạc $z = -1 \implies H(-1) = \frac{1/9}{17/9} = \frac{1}{17}$. |

![Đồ thị Bode H(z) rời rạc vs RC liên tục](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_bode_sc_vs_rc.png)

### 1.2 Đáp ứng Quá độ Đa tần (Multi-Tone Staircase Transient)
Kích thích đầu vào đồng thời gồm sóng mang dải thông $f_{\text{sig}} = 50\text{ kHz}$ ($A_{\text{sig}} = 0.30\text{ V}$) cộng nhiễu cản cao tần $f_{\text{int}} = 2\text{ MHz}$ ($A_{\text{int}} = 0.12\text{ V}$):
- Ngõ ra $V_{\text{out}}[n]$ cập nhật mỗi chu kỳ $T_{\text{clk}} = 100\text{ ns}$ tạo dạng sóng bậc thang giữ mẫu bậc không (*Zero-Order Hold*), nén thành phần nhiễu $2\text{ MHz}$ từ $120\text{ mV}_{\text{p}}$ xuống còn **$11.97\text{ mV}_{\text{p}}$** ($-20.02\text{ dB}$) trong khi giữ nguyên hình sin $50\text{ kHz}$.

![Đáp ứng quá độ đa tần bậc thang](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_multitone_transient.png)

### 1.3 Phân tích Phổ Coherent FFT ($N = 16384$, Cửa sổ Hann)
Để triệt tiêu hoàn toàn rò phổ (*Spectral Leakage*) mà không làm sai lệch công suất hài, phép đo FFT tuân thủ điều kiện lấy mẫu đồng bộ nguyên tố cùng nhau ($\gcd(M_{\text{sig}}, N) = 1$):
- Số điểm FFT: $N = 16{,}384$ mẫu (sau khi bỏ $2{,}048$ chu kỳ đầu để quá độ tắt hẳn $< 10^{-100}$).
- Chỉ số bin tín hiệu: $M_{\text{sig}} = 83 \implies f_{\text{in}} = \frac{83}{16384}\times 10\text{ MHz} = \mathbf{50{,}659.180\text{ Hz}}$, biên độ đỉnh đầu vào $A_{\text{in}} = 0.40\text{ V}$ ($V_{\text{in}} \in [0.50\text{ V}, 1.30\text{ V}]$).

| Chế độ Mô phỏng Golden FFT | $V_{\text{out,rms}}$ | SNR (dB) | SNDR (dB) | SFDR (dB) | THD (dB) | ENOB (bits) | Vai trò Đối chiếu |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1. Lý tưởng toán học (Float64)** | $273.06\text{ mV}$ | $288.69$ | $288.68$ | **$296.20$** | **$-316.22$** | $47.66$ | Xác nhận thuật toán FFT 0 rò phổ. |
| **2. Vật lý nhiệt động ($+ kT/C$ ở $300\text{ K}$)** | $273.06\text{ mV}$ | **$72.09$** | **$71.95$** | **$90.44$** | **$-86.87$** | **$11.66$** | Trần vật lý tối đa của lõi tụ $C_2=800\text{ fF}$ (lý thuyết $71.58\text{ dB}$). |

![Phổ Coherent FFT N=16384 của Golden Model](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_coherent_fft.png)

---

## 2. Nhiệm vụ 2.2 — Phân Tích Phi Lý Tưởng & Chốt Chỉ Tiêu Transistor (`python/nonideal_budget.py`)

1. **Ngân sách Nội trở Khóa `TG` ($R_{\text{on}}$ Sweep):**
   - **Xác lập tĩnh trong $t_{\text{on}} = 47\text{ ns}$:** Để sai số nạp tụ tĩnh $\epsilon_{\text{set}} = e^{-t_{\text{on}}/(R_{\text{on}} C_1)} < 0.1\%$, ngưỡng tĩnh tối đa là $R_{\text{on}} < \mathbf{68.04\text{ k}\Omega}$ ($\tau < 6.80\text{ ns}$).
   - **Méo hài bám mẫu động (Nonlinear Track-and-Hold THD ở sát biên dải thông $f_{\text{in}} = 178.2\text{ kHz}$):** Khi khóa `TG1` bám theo tín hiệu biến thiên $V_{\text{in}}(t)$ qua nội trở hình chuông $R_{\text{on}}(V_{\text{in}})$, độ trễ pha phụ thuộc biên độ $\Delta V_{\text{track}} \approx -R_{\text{on}}(V_{\text{in}}) C_1 \frac{dV_{\text{in}}}{dt}$ sinh ra hài bậc 3 ($HD_3$).
   - Tại ngưỡng chốt **$R_{\text{on,peak}} < 5\text{ k}\Omega$**: thời gian nạp đạt $94\tau$ ($\tau = 0.5\text{ ns}$) và méo hài bám mẫu đạt **$\text{THD} = -105.1\text{ dB}$** (tại cấu hình chọn `TG 4/12 µm` với $R_{\text{on,peak}} = 2.26\text{ k}\Omega$, $\text{THD} = \mathbf{-148.9\text{ dB}}$!).
2. **Ngân sách Độ lợi Vòng hở 5T-OTA ($A_{OL}$ Sweep):**
   - Khi $A_{OL} = 35\text{ dB}$ ($56.2\text{ V/V}$): sai số suy hao DC là $1.75\%$ ($0.153\text{ dB}$), độ dịch điểm cực SC là $1.65\%$.
   - Khi chốt **$A_{OL} \ge 40\text{ dB}$ ($100\text{ V/V}$)**: sai số biên độ DC giảm còn **$0.99\%$ ($0.086\text{ dB}$)** và độ dịch tần số cắt chỉ **$0.94\% \ll 5\%$**.
3. **Đánh đổi Diện tích Kênh $W \times L$ của `TG` (Nội trở $R_{\text{on}}$ vs. Charge Injection $\Delta V_{\text{CI}}$):**
   - Tăng $W_n$ giúp giảm $R_{\text{on}}$ theo $1/W_n$ nhưng làm tăng điện tích kênh $Q_{\text{ch}} \propto W_n L C_{ox}$ gây gai chuyển mạch tuyến tính theo $W_n$.
   - **Điểm ngọt thiết kế (Design Sweet Spot):** $W_n = 4.0\ \mu\text{m}, W_p = 12.0\ \mu\text{m}, L = 0.15\ \mu\text{m}$ (tổng diện tích cổng $2.40\ \mu\text{m}^2$), cho $R_{\text{on,peak}} = 2.26\text{ k}\Omega < 5\text{ k}\Omega$ và biên độ tiêm điện tích cực đại trên ngõ ra $\Delta V_{\text{CI}}(V_{\text{out}}) = 3.84\text{ mV}$ (giảm xuống **$0.77\text{ mV}$** khi gắn thêm Dummy Switch $W/2$).

![3 Biểu đồ Ngân sách Phi lý tưởng Tuần 2](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_nonideal_budgets.png)

---

## 3. Nhiệm vụ 2.3 — Tính Toán & Tiền Kiểm Chứng BSIM4 Bảng Sizing $W/L$ (`python/sizing_calc.py`)

### 3.1 Phương pháp thiết kế $g_m/I_D$ cho `5T-OTA` trên `sky130A`
- **Bài toán quỹ áp thực tế trên `sky130A`:** Như đã phát hiện ở Tuần 1, `pfet_01v8` có $|V_{TH,p}| \approx 0.98\text{ V}$, còn `nfet_01v8` có $V_{TH,n} \approx 0.63\text{–}0.68\text{ V}$. Nếu thiết kế `M1, M2` ở vùng nghịch đảo mạnh ($V_{ov} = 200\text{ mV} \implies V_{GS1} > 0.85\text{ V}$), điện áp nút đuôi $V_{\text{tail}} = V_{CM} - V_{GS1} < 0.05\text{ V}$ sẽ ép `M5` rơi vào vùng tuyến tính!
- **Giải pháp Thiết kế Chuẩn xác:**
  1. Chọn dòng phân cực chuẩn $I_{\text{ref}} = 30\ \mu\text{A}$ ($I_{\text{tail}} = 28.16\ \mu\text{A} \implies I_{D1,2} = 14.08\ \mu\text{A}$, công suất tĩnh chỉ **$104.7\ \mu\text{W}$**, tốc độ quét lý thuyết $\text{SR} = I_{\text{tail}}/C_L = \mathbf{28.2\text{ V}/\mu\text{s}}$).
  2. Đưa cặp vi sai `M1, M2` vào **vùng nghịch đảo trung bình** ($g_m/I_D = 20.48\ \text{V}^{-1}$) với $W_{1,2} = 32.0\ \mu\text{m}, L_{1,2} = 0.80\ \mu\text{m}$ (`nf = 8` ngón $\times 4.0\ \mu\text{m}$): vừa hạ $V_{GS1} = 0.662\text{ V}$ (giữ $V_{\text{tail}} = \mathbf{237.5\text{ mV}} \gg V_{dsat5} = 100.8\text{ mV}$, dư biên bão hòa $+136.8\text{ mV}$ cho `M5`!), vừa đẩy $g_{m1} = \mathbf{289.5\ \mu\text{S}}$ ($\text{GBW} = \mathbf{43.91\text{ MHz}} > 4.3\times$ mục tiêu $10\text{ MHz}$).
  3. Chọn chiều dài kênh $L_{1,2} = L_{3,4} = 0.80\ \mu\text{m}$ và $L_{5,6} = 1.00\ \mu\text{m}$ để triệt tiêu điều chế chiều dài kênh ngắn ($r_{o2} = 452.8\text{ k}\Omega, r_{o4} = 1.78\text{ M}\Omega$), đạt **$A_{OL} = \mathbf{41.62\text{ dB}}$** và biên dự trữ pha **$\text{PM} = \mathbf{81.27^\circ} \ge 60^\circ$**!
  4. **Đồng bộ hóa Layout Tuần 4:** Toàn bộ transistor tương tự `M1–M6` dùng chung **bề rộng mỗi ngón $W_{\text{finger}} = 4.00\ \mu\text{m}$**, sẵn sàng ghép mảng Common-Centroid ABBA chuẩn xác trên Magic VLSI.

### 3.2 Bảng Kích Thước Linh Kiện Đầy Đủ Cho 4 Khối (Sẵn sàng nhập Xschem Tuần 3)

| Khối con | Ký hiệu Linh kiện | Model PDK `sky130A` | $W$ ($\mu\text{m}$) | $L$ ($\mu\text{m}$) | `nf` | `mult` | Ghi chú Vật lý & Layout |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1. `non_overlap_clk`** | `XINV_IN` (N / P) | `nfet_01v8` / `pfet_01v8` | $1.0\ /\ 2.5$ | $0.15$ | $1$ | $1$ | Chuẩn hóa sườn xung đầu vào $10\text{ MHz}$. |
| | `XNAND_A, B` (N / P) | `nfet_01v8` / `pfet_01v8` | $1.6\ /\ 2.0$ | $0.15$ | $1$ | $1$ | Chốt chéo NAND2; $2\times$ NMOS nối tiếp mở rộng $W_n$. |
| | `XDEL1..6` ($\times 2$ nhánh) | `nfet_01v8` / `pfet_01v8` | $0.6\ /\ 1.5$ | **$0.95$** | $1$ | $1$ | 6 tầng trễ kênh dài tạo đúng **$t_{\text{nov}} = 2.92\text{ ns}$**. |
| | `XBUF1, 2` ($\Phi, \overline{\Phi}$) | `nfet_01v8` / `pfet_01v8` | $2.0\ /\ 6.0$ | $0.15$ | $2$ | $1$ | Đệm xuất sườn dốc $< 150\text{ ps}$ lái cổng `TG`. |
| **2. `tg_switch`** | `XTG1_N, XTG2_N` | `sky130_fd_pr__nfet_01v8` | **$4.00$** | $0.15$ | $2$ | $1$ | $W_f = 2.0\ \mu\text{m}$; dẫn mạnh vùng $0 \to 1.0\text{ V}$. |
| | `XTG1_P, XTG2_P` | `sky130_fd_pr__pfet_01v8` | **$12.00$** | $0.15$ | $4$ | $1$ | $W_f = 3.0\ \mu\text{m}$; $R_{\text{on,max}} = 2.26\text{ k}\Omega < 5\text{ k}\Omega$. |
| | `XDUM1, 2` *(Tùy chọn)* | `nfet_01v8` / `pfet_01v8` | $2.0\ /\ 6.0$ | $0.15$ | $1 / 2$ | $1$ | Khóa giả $W/2$ nối tắt D–S triệt $80\%$ $\Delta V_{\text{CI}}$. |
| **3. `sc_core`** | `XC1` ($100.00\text{ fF}$) | `sky130_fd_pr__cap_mim_m3_1` | **$4.85$** | **$9.85$** | — | **$1$** | $1\times$ Ô đơn vị MIM ($W_{\text{eff}}=5\ \mu\text{m}, L_{\text{eff}}=10\ \mu\text{m}$). |
| | `XC2` ($800.00\text{ fF}$) | `sky130_fd_pr__cap_mim_m3_1` | **$4.85$** | **$9.85$** | — | **$8$** | $8\times$ Ô đơn vị ghép song song + vòng Dummy ngoài. |
| **4. `ota_5t`** | `XM1, XM2` (Cặp vi sai) | `sky130_fd_pr__nfet_01v8` | **$32.00$** | **$0.80$** | **$8$** | $1$ | $W_f = 4.0\ \mu\text{m}$ (ABBA); $g_{m1} = 289.5\ \mu\text{S}$, dư bão hòa $+380\text{ mV}$. |
| | `XM3, XM4` (Gương PMOS) | `sky130_fd_pr__pfet_01v8` | **$16.00$** | **$0.80$** | **$4$** | $1$ | $W_f = 4.0\ \mu\text{m}$ (ABBA); $r_{o4} = 1.78\text{ M}\Omega$, dư bão hòa $+758\text{ mV}$. |
| | `XM5, XM6` (Đuôi & Bias) | `sky130_fd_pr__nfet_01v8` | **$24.00$** | **$1.00$** | **$6$** | $1$ | $W_f = 4.0\ \mu\text{m}$; $I_{\text{ref}} = 30\ \mu\text{A} \implies I_{\text{tail}} = 28.16\ \mu\text{A}$. |

![Đáp ứng AC 5T-OTA và Sườn xung không chồng lấn BSIM4](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_ota_bode_and_clk.png)

---

## 4. Tổng Kết Cổng Kiểm Định Tuần 2 (Verification Gate 2 — PASS)

- [x] File chỉ số chuẩn [python/metrics_golden.json](file:///headless/ANN/sky130-sc-lpf/python/metrics_golden.json) đã xuất đầy đủ ($f_{c,\text{SC}} = 187.675\text{ kHz}$, Coherent FFT $N=16384$ cả lý tưởng và có nhiễu $kT/C$).
- [x] File ngân sách phi lý tưởng [python/nonideal_budget.json](file:///headless/ANN/sky130-sc-lpf/python/nonideal_budget.json) và bảng Sizing [python/sizing_table.json](file:///headless/ANN/sky130-sc-lpf/python/sizing_table.json) đã chốt.
- [x] **4 biểu đồ PNG 300 DPI** chuẩn hội nghị IEEE (đã kiểm tra thị giác 100% không đè chữ):
  1. [week2_bode_sc_vs_rc.png](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_bode_sc_vs_rc.png)
  2. [week2_multitone_transient.png](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_multitone_transient.png)
  3. [week2_coherent_fft.png](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_coherent_fft.png)
  4. [week2_nonideal_budgets.png](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_nonideal_budgets.png) & [week2_ota_bode_and_clk.png](file:///headless/ANN/sky130-sc-lpf/slides/figs/week2_ota_bode_and_clk.png)
- [x] Tiền kiểm chứng BSIM4 trên `sky130A`: `t_nov = 2.92 ns`, `R_on,max = 2.26 kΩ`, `A_OL = 41.62 dB`, `GBW = 43.91 MHz`, `PM = 81.27°` — đảm bảo Tuần 3 vào Xschem/Ngspice đạt chuẩn ngay từ lần chạy đầu.
