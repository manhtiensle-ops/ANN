# TUẦN 1: NỀN TẢNG LÝ THUYẾT, PHÂN TÍCH BÀI TOÁN & CHỐT KIẾN TRÚC (`sky130-sc-lpf`)

**Dự án:** Thiết kế Mạch lọc thông thấp tụ chuyển mạch trên tiến trình SkyWater 130nm (`sky130-sc-lpf`)  
**Tài liệu:** Deliverable Tuần 1 — Hồ sơ Lý thuyết, Cơ sở Chọn Thông số & Kiểm định Thứ nguyên (Verification Gate 1)  
**Dữ liệu kiểm chứng đi kèm:** [week1_numbers.json](file:///headless/ANN/sky130-sc-lpf/python/week1_numbers.json) | Script kiểm định: [week1_verify.py](file:///headless/ANN/sky130-sc-lpf/python/week1_verify.py) | Hình dẫn dắt: [week1_story_figs.py](file:///headless/ANN/sky130-sc-lpf/python/week1_story_figs.py)

---

## 0. Mạch Dẫn Dắt 3 Tầng (Top-Down Engineering Narrative) & Chiến Lược Kiểm Định

### 0.1 Cầu nối 3 tầng: Từ Bài toán Lọc nhiễu đến Kiến trúc Tụ chuyển mạch
1. **Tầng 1 — Vấn đề Vật lý (Physical Problem):**
   - Tại đầu thu vô tuyến sau khối hạ tần (*Downconverter* — hoặc tiền xử lý cảm biến MEMS/siêu âm, làm mịn sau DAC), tín hiệu mong muốn nằm ở dải tần thấp ($\le 50\text{ kHz}$, biên độ tuyến tính $\pm 0.4\text{ V}$ quanh $V_{CM} = 0.9\text{ V}$ trên nguồn đơn $1.8\text{ V}$).
   - Tuy nhiên, tín hiệu luôn bị bao vây bởi sóng nhiễu kênh lân cận, gợn chuyển mạch DC–DC và nhiễu xung nhịp số rất mạnh ở tần số cao ($\ge 2\text{ MHz}$). Nếu đưa thẳng vào ADC sẽ gây **chồng phổ (*Aliasing*)** và **bão hòa dải động ADC**.
2. **Tầng 2 — Ý tưởng Xử lý Thông tin (Signals & Systems Domain):**
   - Thiết kế bộ lọc thông thấp bậc 1 có tần số cắt $f_{c,\text{RC}} \approx 198.94\text{ kHz}$ để giữ nguyên dải thông ($\le 50\text{ kHz}: -0.30\text{ dB} \approx 0\text{ dB}$) và nén giảm nhiễu tại $2\text{ MHz}$ đi **$-20\text{ dB}$** ($10\times$).
   - Rời rạc hóa bộ lọc ở tần số lấy mẫu cao $f_{\text{clk}} = 10\text{ MHz}$ ($\text{OSR} = 26.64 \gg 1$, đẩy dải ảnh Aliasing ra tận $9.81\text{ MHz}$) thành phương trình sai phân bảo toàn điện tích 2 pha:
     $$(C_1 + C_2)V_{\text{out}}[n] - C_2 V_{\text{out}}[n-1] = C_1 V_{\text{in}}[n] \implies H(z) = \frac{1/9}{1 - \frac{8}{9}z^{-1}}$$
     với tần số cắt rời rạc chính xác $f_{c,\text{SC}} = 187.675\text{ kHz}$ và điểm cực $|z_p| = 8/9 < 1$ (ổn định BIBO tuyệt đối).
3. **Tầng 3 — Hiện thực hóa Vi mạch Analog (`sky130A` Implementation):**
   - Điện trở thực $R = 1\text{ M}\Omega$ (ứng với $C_2 = 800\text{ fF}$) tốn diện tích lớn ($7.26\text{ mm}$ Poly thường) và có sai số chế tạo PVT lên tới $-24.2\%$ đến $+36.0\%$.
   - Thay thế bằng tụ chuyển mạch MIM $C_1 = 100\text{ fF}$ đóng ngắt ở $10\text{ MHz}$ ($R_{\text{eq}} = \frac{1}{f_{\text{clk}}C_1} = 1\text{ M}\Omega$) ghép mảng $1:8$ với $C_2 = 800\text{ fF}$ để tần số cắt chỉ phụ thuộc tỷ số tụ (chính xác $< 0.1\%$, trôi PVT $= 0.0\%$, diện tích $450\ \mu\text{m}^2$), hoàn thiện thành **4 khối** (`non_overlap_clk`, `tg_switch`, `sc_core`, `ota_5t`) trên nguồn $1.8\text{ V}$.

### 0.2 Sau khi hoàn thiện sản phẩm: Năng lực xử lý, INPUT & OUTPUT dự kiến
- **Năng lực sản phẩm (`top_sc_lpf` trên Sky130A):** Khối IP lọc thông thấp tích hợp hoàn chỉnh, diện tích siêu gọn (không điện trở ngoài), tự tạo xung 2 pha không chồng lấn, lọc sạch nhiễu cao tần và đệm ngõ ra trở kháng thấp kéo trực tiếp tải $C_L = 1\text{ pF}$.
- **INPUT đầu vào:**
  - Tín hiệu tương tự $V_{\text{in}}(t) \in [0.5\text{ V}, 1.3\text{ V}]$ quanh $V_{CM} = 0.9\text{ V}$. Ví dụ kịch bản kiểm thử chuẩn:
    $$V_{\text{in}}(t) = 0.9 + 0.30\sin(2\pi\cdot 50\text{ kHz}\,t) + 0.12\sin(2\pi\cdot 2\text{ MHz}\,t)$$
  - Xung nhịp chuẩn $V_{\text{clk}}$ ($0 \leftrightarrow 1.8\text{ V}$, $f_{\text{clk}} = 10\text{ MHz}$) và nguồn $V_{DD} = 1.8\text{ V}, V_{SS} = 0\text{ V}$.
- **OUTPUT dự kiến tại $V_{\text{out}}$ (tải $C_L = 1\text{ pF}$):**
  - Bảo toàn tín hiệu có ích $50\text{ kHz}$: suy hao chỉ **$-0.30\text{ dB}$** ($96.6\%$ biên độ, $\approx 0.290\text{ V}_p$).
  - Nén mạnh nhiễu cao tần $2\text{ MHz}$: suy giảm **$-20.02\text{ dB}$** (giảm **$10\times$**, từ $120\text{ mV}_p \to 12\text{ mV}_p$); tại Nyquist $5\text{ MHz}$ giảm $-24.61\text{ dB}$.
  - Chỉ tiêu chất lượng đầu ra mục tiêu: $f_{c,\text{SC}} = 187.67\text{ kHz} \pm 5\%$ ($178.3\text{–}197.1\text{ kHz}$), $\text{SFDR} > 50\text{ dB}$, $\text{THD} < -48\text{ dB}$ ($< 0.4\%$).

![Đầu vào và đầu ra dự kiến của SC-LPF theo miền thời gian và tần số](file:///headless/ANN/sky130-sc-lpf/slides/figs/week1_io_expected.png)

### 0.3 Phương pháp kiểm tra mạch hoạt động ổn định & Lý do lựa chọn
| Lớp ổn định / Khối | Phương pháp kiểm tra | Chỉ tiêu ổn định | Tại sao chọn phương pháp đó? |
| :--- | :--- | :--- | :--- |
| **Ổn định BIBO lõi lọc** (`sc_core`) | Phân tích điểm cực $H(z)$ | $|z_p| = 1-\alpha = \frac{8}{9} < 1$ | Đảm bảo đầu vào hữu hạn luôn cho đầu ra hữu hạn. |
| **Ổn định vòng kín LTI** (`ota_5t`) | `.op` + `.ac` vòng hở + `.tran` step | `M1–M5` bão hòa; $\text{PM} \ge 60^\circ$ | Chuẩn Bode/Nyquist ngăn bộ đệm $\beta=1$ tự dao động hay rung vọt lố. |
| **An toàn chuyển mạch** (`non_overlap_clk`, `tg_switch`) | `.tran` ($t_{\text{nov}}$) + `.dc` ($R_{\text{on}}$) | $t_{\text{nov}} \in [2,5]\text{ ns}$; $R_{\text{on}} < 5\text{ k}\Omega$ | Cấm rò điện tích trực tiếp $V_{\text{in}} \to C_2$ và đảm bảo nạp $> 90\tau$. |
| **Đáp ứng & Tuyến tính LPTV** (`top_sc_lpf`) | **`.tran` + lấy mẫu cuối $\Phi_2$ + Coherent FFT** | $|\Delta f_c|<5\%$, $\text{SFDR}>50\text{ dB}$ | `.ac` đóng băng tại $t=0$ làm `TG2` hở ($10^{11}\ \Omega$); Coherent FFT ($f_{\text{in}}=\frac{M}{N}f_{\text{clk}}$) triệt rò rỉ phổ để đo đúng từng dB phi tuyến thực. |
| **Ổn định Quy trình & Silicon** (Tuần 3–4) | Quét PVT (`tt/ss/ff/hh/ll`, $-40\to 125^\circ\text{C}$) + DRC/LVS/PEX | DRC=0, LVS Clean, khớp 3 cột | Xác minh ký sinh kim loại thực tế trên chip không phá vỡ $f_c$ hay $\text{PM}$. |

---

## 1. Nhiệm vụ 1.1 — Phân Tích Bài Toán & Cơ Sở Chọn Thông Số (Design Rationale)

### 1.1.1 Chứng minh định lượng: Vì sao không tích hợp điện trở $R = 1\text{ M}\Omega$ lên chip Sky130A?

Để tạo mạch lọc thông thấp bậc 1 có tần số cắt vùng âm thanh/cảm biến ($f_c \approx 188\text{–}199\text{ kHz}$) với tụ tích hợp hợp lý $C_2 = 800\text{ fF}$, hằng số thời gian yêu cầu là:
$$\tau = R \cdot C_2 = 800\text{ ns} \implies R = \frac{\tau}{C_2} = \frac{800\times 10^{-9}\text{ s}}{800\times 10^{-15}\text{ F}} = 1.00\text{ M}\Omega$$

Kết quả trích xuất trực tiếp từ mô hình SPICE thực tế của PDK `sky130A` (`/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice`) cho 3 loại điện trở Polysilicon chuẩn (với bề rộng tối thiểu khuyến nghị $W = 0.35\ \mu\text{m}$ để giảm sai số khắc quang học):

| Loại linh kiện trong `sky130A` | Điện trở vuông thực đo ($R_{\square}$, `tt 27°C`) | Số ô vuông $N_{\square}$ cần cho $1\text{ M}\Omega$ | Tổng chiều dài $L$ ($W=0.35\ \mu\text{m}$) | Dung sai góc công nghệ & Hệ quả |
| :--- | :---: | :---: | :---: | :--- |
| `sky130_fd_pr__res_generic_po` | $48.20\ \Omega/\square$ | $20{,}747\ \square$ | $7{,}261\ \mu\text{m}$ ($7.26\text{ mm}$) | Phi thực tế; diện tích và tụ ký sinh xuống nền cực lớn. |
| `sky130_fd_pr__res_high_po` | $357.86\ \Omega/\square$ | $2{,}794\ \square$ | $978.0\ \mu\text{m}$ | Dài gần $1\text{ mm}$, tụ phân bố làm hỏng đáp ứng tần số. |
| `sky130_fd_pr__res_xhigh_po` | $2{,}579.45\ \Omega/\square$ | $387.7\ \square$ | $135.7\ \mu\text{m}$ | Sai số góc công nghệ $\Delta R/R = \pm 15.0\%$ (`ll`/`hh`). |

**Phép đo độ trôi tần số cắt PVT thực tế trên `sky130A` (`week1_verify.py`):**
Khi ghép điện trở `res_xhigh_po` với tụ MIM `cap_mim_m3_1` để tạo bộ lọc $RC$ trên chip, ở góc công nghệ `hh` ($R$ tăng $+15.0\%$, $C_{\text{mim}}$ tăng $+14.7\%$) và góc `ll` ($R$ giảm $-15.0\%$, $C_{\text{mim}}$ giảm $-13.5\%$):
- Tại góc **`hh` ($27^\circ\text{C}$ và $125^\circ\text{C}$):** $\Delta f_{c,\text{RC}} = \mathbf{-24.19\%}$ ($f_c$ sụt từ $198.9\text{ kHz}$ xuống $150.8\text{ kHz}$).
- Tại góc **`ll` ($27^\circ\text{C}$ và $-40^\circ\text{C}$):** $\Delta f_{c,\text{RC}} = \mathbf{+36.04\%}$ ($f_c$ vọt lên $270.6\text{ kHz}$).
- **Tổng dải trôi PVT của mạch $RC$ liên tục trên chip lên tới $60.2\%$!**

Ngược lại, khi thay điện trở $R$ bằng **tụ chuyển mạch $C_1 = 100\text{ fF}$ đóng ngắt ở $f_{\text{clk}} = 10\text{ MHz}$**:
1. **Điện trở tương đương chính xác:**
   $$R_{\text{eq}} = \frac{T_{\text{clk}}}{C_1} = \frac{1}{f_{\text{clk}} C_1} = \frac{1}{10\times 10^6\text{ Hz} \times 100\times 10^{-15}\text{ F}} = 1.000\text{ M}\Omega$$
2. **Bất biến tuyệt đối theo góc công nghệ (PVT Invariance):**
   Tần số cắt chỉ phụ thuộc vào $f_{\text{clk}}$ (xung thạch anh ngoài, độ ổn định $< 50\text{ ppm}$) và **tỷ số hình học của hai tụ MIM cùng tầng kim loại `m3–m4`**:
   $$\frac{C_1}{C_2} = \frac{1 \times C_{\text{unit}}}{8 \times C_{\text{unit}}} = \frac{1}{8} \implies \Delta f_{c,\text{SC}}(\text{PVT}) = \mathbf{0.00\%}$$
   Khi bố trí theo mảng ô đơn vị đồng nhất kèm vòng tụ giả (*Dummy Cap*) quanh biên, sai số ghép đôi cục bộ (*Local Mismatch*) đạt $\frac{\sigma(\Delta C/C)}{\sqrt{\text{Area}}} < 0.1\%$.
3. **Tiết kiệm diện tích Silicon:** Ô đơn vị MIM $C_{\text{unit}} = 100\text{ fF}$ có kích thước vẽ $W = 4.85\ \mu\text{m}, L = 9.85\ \mu\text{m}$ (diện tích hiệu dụng $5.00 \times 10.00 = 50.00\ \mu\text{m}^2$). Tổng diện tích 9 ô tụ ($C_1 + C_2$) chỉ chiếm **$450\ \mu\text{m}^2$**.

![So sánh độ trôi PVT giữa RC trên chip và Tụ chuyển mạch](file:///headless/ANN/sky130-sc-lpf/slides/figs/week1_rc_vs_sc_pvt.png)

---

### 1.1.2 Dẫn xuất Toán học Từng Thông số Chip trực tiếp từ Lý thuyết Tín hiệu & Hệ thống (Cầu nối Tầng 2 $\Longrightarrow$ Tầng 3)

Không một thông số nào của chip `sky130-sc-lpf` được chọn cảm tính. Dưới đây là hệ chứng minh nhân quả khép kín giải thích cách lý thuyết **Tín hiệu & Hệ thống** khóa chặt từng thông số phần cứng:

1. **Từ Yêu cầu Phổ Dải thông / Dải chắn $\Longrightarrow$ Chọn bậc lọc $N = 1$ và miền nghiệm $f_c \in [143.14, 201.01]\text{ kHz}$:**
   - Khoảng cách tần số từ biên tín hiệu hữu ích ($B_{\text{sig}} = 50\text{ kHz}$) đến nhiễu mạnh ngoài băng ($f_{\text{int}} = 2\text{ MHz}$) là $\log_{10}(2000/50) = \mathbf{1.602\text{ decade}}$. Một bộ lọc thông thấp bậc $N=1$ có độ dốc $-20\text{ dB/decade}$ đủ sức đạt độ nén $> 20\text{ dB}$ mà không cần bậc cao (giúp mạch chỉ tốn 1 OTA, không có cực phức gây vọt lố, và độ trễ nhóm phẳng nhất).
   - Giải hệ bất phương trình biên độ $|H(jf)|^2 = \frac{1}{1 + (f/f_c)^2}$:
     - **Điều kiện dải thông** (suy hao tại $50\text{ kHz} \le 0.5\text{ dB}$):
       $$10\log_{10}\!\left[1 + \left(\frac{50\text{ kHz}}{f_c}\right)^2\right] \le 0.5 \implies \mathbf{f_c \ge 143.14\text{ kHz}}$$
     - **Điều kiện dải chắn** (độ nén tại $2\text{ MHz} \ge 20\text{ dB}$):
       $$10\log_{10}\!\left[1 + \left(\frac{2000\text{ kHz}}{f_c}\right)^2\right] \ge 20 \implies \mathbf{f_c \le 201.01\text{ kHz}}$$

2. **Từ Định lý Lấy mẫu Nyquist, Phổ tuần hoàn $X_s(f)$ & Méo tần số $\Omega_c \Longrightarrow$ Chốt $f_{\text{clk}} = 10\text{ MHz}$ ($\text{OSR} = 26.64$):**
   - Trong hệ rời rạc, đáp ứng $H(e^{j2\pi f/f_{\text{clk}}})$ lặp lại tuần hoàn tại mọi bội số $k f_{\text{clk}}$ (mở thông $0\text{ dB}$ trở lại quanh $f_{\text{clk}}$!).
   - Nếu chọn $f_{\text{clk}} = 1\text{ MHz}$ ($\text{OSR} \approx 2.6$): vùng ảnh chồng phổ nằm ngay ở $\sim 812\text{ kHz}$ và góc tần số cắt rời rạc $\Omega_c = \omega_c T_{\text{clk}} \approx 1.18\text{ rad}$ gây méo tần số (*frequency warping*) nặng.
   - Nếu chọn $f_{\text{clk}} = 100\text{ MHz}$: tỷ số tụ $C_2/C_1$ phải tăng lên $80$ (tốn diện tích MIM gấp $10\times$) và bán chu kỳ chỉ còn $5\text{ ns}$ làm tăng vọt công suất OTA.
   - Chọn **$f_{\text{clk}} = 10\text{ MHz}$** cho $\text{OSR} = \mathbf{26.64} \gg 1$, góc nhỏ $\Omega_c = \mathbf{0.1179\text{ rad}} \ll 1$ ($H(z)$ bám sát $H(s)$), đẩy cửa sổ ảnh Aliasing đầu tiên ra tận **$9.81\text{ MHz}$**, trong khi bán chu kỳ $50\text{ ns}$ rộng rãi cho quá trình nạp tụ.

3. **Từ Lượng tử hóa Tỷ số Nguyên & Đối xứng Hình học $\Longrightarrow$ Chốt $K = C_2/C_1 = 8$ ($\alpha = 1/9$):**
   - Để triệt sai số khắc quang học trên wafer, $K = C_2/C_1$ phải là số nguyên dương. Đánh giá chính xác trên $H(z)$ ở $f_{\text{clk}} = 10\text{ MHz}$:
     - Với $K \le 7$: tại $K=7$, $f_{c,\text{SC}} = 212.7\text{ kHz}$ làm độ nén ở $2\text{ MHz}$ tụt xuống **$18.9\text{ dB} < 20\text{ dB}$ (Trượt chuẩn dải chắn)**.
     - Với $K \ge 11$: suy hao ở $50\text{ kHz}$ vượt quá **$0.5\text{ dB}$ (Trượt chuẩn dải thông)**.
     - Chọn **$K = 8$** là số nguyên nhỏ nhất thỏa mãn đồng thời cả hai chuẩn (**$-0.30\text{ dB}$** tại $50\text{ kHz}$ và **$-20.02\text{ dB}$** tại $2\text{ MHz}$), đồng thời tổng số ô tụ đơn vị $1 + 8 = 9 = 3\times 3$ lập thành **ma trận vuông đối xứng tâm Common-Centroid hoàn hảo**!

![Không gian thiết kế từ Tín hiệu & Hệ thống khóa chặt K = 8 và f_clk = 10 MHz](file:///headless/ANN/sky130-sc-lpf/slides/figs/week1_ss_spec_window.png)

4. **Từ Tích phân Mật độ Phổ Nhiễu (PSD) qua Băng thông Nhiễu Tương đương (NEB) $\Longrightarrow$ Chốt $C_1 = 100\text{ fF}, C_2 = 800\text{ fF}$:**
   - Nhiễu nhiệt trắng $S_v(f) = 4k_B T R_{\text{on}}$ của khóa đóng ngắt đi qua mắt lọc $RC$ có $\text{NEB} = \int_0^\infty |1 + j2\pi f R_{\text{on}}C|^{-2}df = \frac{1}{4 R_{\text{on}}C}$ làm $R_{\text{on}}$ tự triệt tiêu, gập toàn bộ công suất nhiễu thành $\overline{v_{n,\text{out}}^2} \approx \frac{k_B T}{C_2}$.
   - Với biên độ đỉnh $V_p = 0.4\text{ V}$ ($282.8\text{ mV}_{\text{rms}}$), chọn **$C_1 = 100\text{ fF}, C_2 = 800\text{ fF}$** giữ nhiễu đầu ra ở $71.95\ \mu\text{V}_{\text{rms}}$, đạt trần **$\text{SNR}_{kT/C} = 71.9\text{ dB}$** ($\sim 11.6\text{ bit}$), đồng thời áp đảo tụ ký sinh dây nối ($\sim 1.5\text{ fF} < 1.5\%\,C_1$) và giữ tải OTA nhẹ ($\le 1\text{ pF}$).

5. **Từ Lý thuyết Sai số Xác lập Rời rạc, Méo hài THD & Đáp ứng Quá độ Bậc 2 Vòng kín $\Longrightarrow$ Chốt chỉ tiêu Khóa TG & 5T-OTA:**
   - **Khóa TG ($R_{\text{on}} < 5\text{ k}\Omega$):** Nạp tĩnh $99.9\%$ trong $t_{\text{on}} = 47\text{ ns}$ chỉ cần $R_{\text{on}} < 68\text{ k}\Omega$ ($6.9\tau$). Tuy nhiên, vì $R_{\text{on}}(V_{\text{in}})$ là hàm phi tuyến theo tín hiệu vào, ta phải ép $R_{\text{on}} < 5\text{ k}\Omega$ ($\tau \le 0.5\text{ ns} \implies t_{\text{on}} = \mathbf{94\tau}$, phần dư $e^{-94} \approx 0$) để triệt tiêu hoàn toàn méo hài động $\text{HD}_2, \text{HD}_3$ trên phổ FFT.
   - **Bộ đệm 5T-OTA ($A_{OL} > 40\text{ dB}, \text{GBW} > 10\text{ MHz}, \text{PM} \ge 60^\circ$):** Hồi tiếp âm đơn vị ($\beta = 1$) cần $A_{OL} \ge 100\text{ V/V}$ ($40\text{ dB}$) để sai số biên độ dải thông $\epsilon_A = \frac{1}{1+A_{OL}} < 1\%$. Với OTA 2 cực, hàm truyền vòng kín là hệ bậc 2 có hệ số tắt dần $\zeta = \frac{1}{2}\sqrt{f_{p2}/\text{GBW}}$: yêu cầu **$\text{PM} \ge 60^\circ \iff f_{p2} \ge \sqrt{3}\,\text{GBW}$** để triệt rung vọt lố trước thời điểm lấy mẫu cuối pha $47\text{ ns}$.
   - **Phân cực nguồn đơn ($V_{DD} = 1.8\text{ V}, V_{CM} = 0.9\text{ V}$):** Dịch mức DC lên đúng $V_{DD}/2 = 0.9\text{ V}$ để tín hiệu tổng ($\pm 0.42\text{ V}$) không bị xén biên (*Clipping*) sinh hài lẻ.

![Phổ nhiễu kT/C và đáp ứng bước nhảy hệ bậc 2 vòng kín lý giải cỡ tụ và PM >= 60 độ](file:///headless/ANN/sky130-sc-lpf/slides/figs/week1_ss_ota_noise_bridge.png)

---

## 2. Nhiệm vụ 1.2 — Hệ Thống Hóa Lý Thuyết MOSFET & Mạch Lọc SC (Razavi Ch. 2–9)

### 2.1 Nguyên lý hoạt động 2 pha & Dẫn xuất hàm truyền miền Z chính xác

Xét lõi lọc thông thấp tụ chuyển mạch bậc 1 điều khiển bởi hai pha xung không chồng lấn $\Phi_1, \Phi_2$ ($t_{\text{nov}} \in [2\text{ ns}, 5\text{ ns}]$):
- **Trong pha $\Phi_1$ (Pha lấy mẫu — Sampling Phase):**
  - Khóa `TG1` đóng ($\Phi_1 = 1.8\text{ V}, \overline{\Phi_1} = 0\text{ V}$), khóa `TG2` ngắt ($\Phi_2 = 0\text{ V}, \overline{\Phi_2} = 1.8\text{ V}$).
  - Tụ $C_1$ nạp tới điện áp đầu vào hiện tại $V_{\text{in}}[n]$:
    $$Q_{C_1}^{(\Phi_1)} = C_1 V_{\text{in}}[n]$$
  - Tụ $C_2$ bị cô lập khỏi $C_1$ và bảo toàn điện tích từ cuối chu kỳ trước $n-1$:
    $$Q_{C_2}^{(\Phi_1)} = C_2 V_{\text{out}}[n-1]$$
- **Trong khoảng chết $t_{\text{nov}}$ (Dead-time):**
  - Cả `TG1` và `TG2` đều ngắt hoàn toàn trước khi chuyển pha $\implies$ tuyệt đối không có đường dẫn trực tiếp từ $V_{\text{in}}$ sang $C_2$ (chống thất thoát điện tích).
- **Trong pha $\Phi_2$ (Pha chia sẻ điện tích — Charge-Sharing / Integration Phase):**
  - Khóa `TG1` ngắt, khóa `TG2` đóng nối song song $C_1$ và $C_2$ tại nút tích phân $V_X$ (được đệm ra $V_{\text{out}}[n] = V_X[n]$ qua bộ đệm hồi tiếp đơn vị 5T-OTA có dòng cực cổng $I_G = 0$).
  - Áp dụng **Định luật Bảo toàn Điện tích** tại nút $V_X$ từ pha $\Phi_1$ sang cuối pha $\Phi_2$:
    $$Q_{C_1}^{(\Phi_2)} + Q_{C_2}^{(\Phi_2)} = Q_{C_1}^{(\Phi_1)} + Q_{C_2}^{(\Phi_1)}$$
    $$\implies C_1 V_{\text{out}}[n] + C_2 V_{\text{out}}[n] = C_1 V_{\text{in}}[n] + C_2 V_{\text{out}}[n-1]$$
    $$\implies \boxed{(C_1 + C_2)V_{\text{out}}[n] - C_2 V_{\text{out}}[n-1] = C_1 V_{\text{in}}[n]}$$

Chia hai vế cho $(C_1 + C_2)$ và đặt hệ số chia điện tích $\alpha = \frac{C_1}{C_1 + C_2} = \frac{100\text{ fF}}{100\text{ fF} + 800\text{ fF}} = \frac{1}{9}$ (suy ra $1 - \alpha = \frac{C_2}{C_1 + C_2} = \frac{8}{9}$):
$$V_{\text{out}}[n] = (1 - \alpha)V_{\text{out}}[n-1] + \alpha V_{\text{in}}[n]$$

Thực hiện biến đổi $\mathcal{Z}$ ($V_{\text{out}}[n-1] \leftrightarrow z^{-1}V_{\text{out}}(z)$):
$$\boxed{H(z) = \frac{V_{\text{out}}(z)}{V_{\text{in}}(z)} = \frac{\alpha}{1 - (1 - \alpha)z^{-1}} = \frac{1/9}{1 - \frac{8}{9}z^{-1}}}$$

#### Dẫn xuất tần số cắt $-3\text{ dB}$ rời rạc chính xác ($f_{c,\text{SC}}$) vs. Xấp xỉ liên tục ($f_{c,\text{RC}}$)
Đánh giá đáp ứng tần số trên vòng tròn đơn vị $z = e^{j\omega T_{\text{clk}}}$:
- Tại DC ($\omega = 0 \implies z = 1$): $H(e^{j0}) = \frac{\alpha}{1 - (1 - \alpha)} = 1 = 0\text{ dB}$.
- Bình phương biên độ theo tần số góc $\omega = 2\pi f$:
  $$\left|H\left(e^{j\omega T_{\text{clk}}}\right)\right|^2 = \frac{\alpha^2}{\left|1 - (1-\alpha)e^{-j\omega T_{\text{clk}}}\right|^2} = \frac{\alpha^2}{1 + (1-\alpha)^2 - 2(1-\alpha)\cos(\omega T_{\text{clk}})}$$
- Tại tần số cắt $-3\text{ dB}$ ($\omega_c = 2\pi f_{c,\text{SC}}$), $\left|H\left(e^{j\omega_c T_{\text{clk}}}\right)\right|^2 = \frac{1}{2}$:
  $$1 + (1-\alpha)^2 - 2(1-\alpha)\cos(\omega_c T_{\text{clk}}) = 2\alpha^2$$
  $$\implies \cos(\omega_c T_{\text{clk}}) = \frac{1 + (1-\alpha)^2 - 2\alpha^2}{2(1-\alpha)} = \frac{2(1-\alpha) - \alpha^2}{2(1-\alpha)} = 1 - \frac{\alpha^2}{2(1-\alpha)}$$
- Thay $\alpha = \frac{1}{9}$ và $1 - \alpha = \frac{8}{9}$:
  $$\cos(\omega_c T_{\text{clk}}) = 1 - \frac{1/81}{16/9} = 1 - \frac{1}{144} = \frac{143}{144} = 0.99305556$$
  $$\implies \boxed{f_{c,\text{SC}} = \frac{f_{\text{clk}}}{2\pi}\arccos\left(\frac{143}{144}\right) = \frac{10\text{ MHz}}{2\pi}\times 0.1179194\text{ rad} = \mathbf{187.675\text{ kHz}}}$$

- **So sánh với xấp xỉ miền liên tục $f_{c,\text{RC}}$:**
  $$f_{c,\text{RC}} = \frac{1}{2\pi R_{\text{eq}} C_2} = \frac{f_{\text{clk}} C_1}{2\pi C_2} = \frac{10\text{ MHz}}{16\pi} = \mathbf{198.944\text{ kHz}}$$
  - Độ lệch rời rạc hóa: $\frac{f_{c,\text{SC}} - f_{c,\text{RC}}}{f_{c,\text{RC}}} = \mathbf{-5.664\%}$.
  - **Bản chất vật lý:** Phép chia sẻ điện tích thụ động ở pha $\Phi_2$ tương ứng với phép ánh xạ **Backward-Euler** $s \leftarrow \frac{1 - z^{-1}}{T_{\text{clk}}}$ trên hằng số thời gian $\tau = R_{\text{eq}} C_2 = \frac{C_2}{C_1}T_{\text{clk}}$, đặt điểm cực rời rạc tại $p_{\text{SC}} = \frac{C_2}{C_1 + C_2} = \frac{8}{9} = 0.88889$, lớn hơn điểm cực bất biến xung của mạch $RC$ liên tục $p_{\text{RC}} = e^{-C_1/C_2} = e^{-1/8} = 0.88250$. Điểm cực tiến gần $z=1$ hơn làm tần số cắt thực tế giảm từ $198.94\text{ kHz}$ xuống $187.67\text{ kHz}$.

---

### 2.2 Mô hình Tín hiệu lớn (Large-Signal) vs. Tín hiệu nhỏ (Small-Signal) & Quy tắc `.op`, `.ac`, `.tran`

1. **Chế độ Tín hiệu lớn (Large-Signal — Phương trình Shichman-Hodges / BSIM4):**
   - **Vùng tuyến tính (Triode — dùng cho khóa truyền dẫn `TG1, TG2` khi dẫn với $V_{DS} \approx 0$):**
     $$I_D = \mu C_{ox}\frac{W}{L}\left[(V_{GS} - V_{TH})V_{DS} - \frac{1}{2}V_{DS}^2\right] \implies R_{\text{on}} = \left(\frac{\partial I_D}{\partial V_{DS}}\bigg|_{V_{DS}\to 0}\right)^{-1} = \frac{1}{\mu C_{ox}\frac{W}{L}(V_{GS} - V_{TH})}$$
   - **Vùng bão hòa (Saturation — dùng cho 5 transistor `M1–M5` của `ota_5t` với $V_{DS} > V_{ov} = V_{GS} - V_{TH}$):**
     $$I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}(V_{GS} - V_{TH})^2 (1 + \lambda V_{DS})$$
2. **Chế độ Tín hiệu nhỏ (Small-Signal Linearization quanh điểm tĩnh Q):**
   - Hỗ dẫn chính: $g_m = \frac{\partial I_D}{\partial V_{GS}} = \mu C_{ox}\frac{W}{L}V_{ov} = \sqrt{2\mu C_{ox}\frac{W}{L}I_D} = \frac{2 I_D}{V_{ov}}$.
   - Hỗ dẫn cực nền (Body-effect transconductance): $g_{mb} = \frac{\partial I_D}{\partial V_{BS}} = \eta g_m$ với $\eta = \frac{\gamma}{2\sqrt{2\phi_F + V_{SB}}}$.
   - Điện trở đầu ra: $r_o = \left(\frac{\partial I_D}{\partial V_{DS}}\right)^{-1} = \frac{1}{\lambda I_D} = \frac{1}{g_{ds}}$.
3. **Chứng minh chặt chẽ vì sao `.ac` trong Ngspice KHÔNG chạy được cho mạch lọc Tụ chuyển mạch:**
   - Thuật toán `.ac` của SPICE gồm 2 bước: (i) giải điểm làm việc tĩnh DC (`.op`) tại $t = 0$ bằng cách hở mạch mọi tụ điện ($I_C = 0$), sau đó (ii) thay mọi linh kiện phi tuyến bằng ma trận đạo hàm riêng tĩnh $\mathbf{G}_{\text{op}} + j\omega \mathbf{C}_{\text{op}}$ cố định theo thời gian (**LTI — Linear Time-Invariant**).
   - Tại $t = 0$, hai pha xung không chồng lấn ở trạng thái tĩnh cố định (ví dụ $\Phi_1 = 1.8\text{ V}, \Phi_2 = 0\text{ V}$). Khi đó `TG1` có $R_{\text{on1}} \sim 2\text{ k}\Omega$ nhưng `TG2` luôn tắt với $R_{\text{off2}} \sim 10^{11}\ \Omega$! Tín hiệu AC từ $C_1$ không bao giờ truyền sang $C_2$ vì SPICE `.ac` không có khái niệm hệ thống biến thiên tuần hoàn theo thời gian (**LPTV — Linear Periodically Time-Varying**).
   - **Quy tắc bắt buộc trong dự án:**
     - `.op`: Kiểm tra vùng bão hòa ($V_{DS} > V_{dsat}$) và dòng phân cực tĩnh của `ota_5t`.
     - `.dc`: Quét đặc tuyến tĩnh $R_{\text{on}}(V_{\text{in}})$ của `tg_switch` khi cố định cổng bật.
     - `.ac`: Chỉ dùng riêng cho khối thời gian liên tục `ota_5t` (đo $A_{OL}, \text{GBW}, \text{PM}$).
     - `.tran` + **Coherent FFT (Python)**: Phương pháp chuẩn duy nhất để đo đáp ứng biên độ–tần số, bậc thang thời gian và phổ SFDR/THD của `top_sc_lpf`.

---

### 2.3 Các nguồn nhiễu ký sinh đặc thù trên Sky130A Planar CMOS (Số liệu đo BSIM4 thực tế)

#### (a) 6 Tụ ký sinh nội tại của MOSFET Planar 130nm
Trên cấu trúc Planar CMOS của `sky130A`, mỗi transistor mang 6 thành phần tụ ký sinh:
1. **Nhóm tụ cổng–kênh & chồng lấp ($C_{gs}, C_{gd}, C_{gb}$):**
   - Trong vùng dẫn triode (khóa `TG`): $C_{gs} \approx C_{gd} \approx \frac{1}{2}W L C_{ox} + W C_{ov}$.
   - Trong vùng bão hòa (`ota_5t`): $C_{gs} \approx \frac{2}{3}W L C_{ox} + W C_{ov}$, $C_{gd} = W C_{ov}$ (nhân hiệu ứng Miller tại ngõ vào/ra), $C_{gb}$ nhỏ.
2. **Nhóm tụ tiếp giáp P–N cực máng/nguồn xuống nền ($C_{sb}, C_{db}$) và giếng N xuống đế ($C_{\text{sub}}$):**
   $$C_{db} = \frac{C_{j0} \cdot A_D}{\left(1 + \frac{V_{DB}}{\phi_B}\right)^{m_j}} + \frac{C_{jsw0} \cdot P_D}{\left(1 + \frac{V_{DB}}{\phi_{Bsw}}\right)^{m_{jsw}}}$$
   - Tụ $C_{db}, C_{sb}$ của `TG1, TG2` nối trực tiếp vào nút nhạy $C_1$ và $V_X$; vì phụ thuộc phi tuyến vào điện áp tín hiệu $V_{\text{in}}$, chúng gây méo hài bậc 2, bậc 3 nếu chọn bề rộng $W$ của khóa `TG` quá lớn. Kỹ thuật **chia nhiều ngón (Multi-finger, $\text{nf} \ge 2$)** trong Tuần 4 giúp chia sẻ vùng khuếch tán Drain/Source, giảm gần $40\text{–}50\%$ diện tích $A_D$ và chu vi $P_D$.

#### (b) Hiệu ứng cực nền (Body Effect) và đặc tuyến $R_{\text{on}}(V_{\text{in}})$ của `tg_switch` trên `sky130A`
Trong khóa truyền dẫn CMOS, cực nền (Bulk) của NMOS nối cố định về $V_{SS} = 0\text{ V}$, còn N-well của PMOS nối về $V_{DD} = 1.8\text{ V}$. Khi $V_{\text{in}} = V_{CM} = 0.9\text{ V}$, cả hai transistor đều chịu phân cực ngược nguồn–nền $V_{SB,n} = 0.9\text{ V}$ và $V_{BS,p} = 0.9\text{ V}$:
$$V_{TH}(V_{SB}) = V_{TH0} + \gamma\left(\sqrt{2\phi_F + V_{SB}} - \sqrt{2\phi_F}\right)$$

Số liệu đo `.op` và `.dc` thực tế bằng `ngspice-47` (`python/week1_verify.py`) trên `sky130A` (`L = 0.15 µm`, góc `tt 27°C`):
- $V_{TH,n}$ của `nfet_01v8` ($L=0.15\ \mu\text{m}$) tăng từ **$0.740\text{ V}$** (ở $V_{SB}=0$) lên **$0.866\text{ V}$** (ở $V_{SB}=0.9\text{ V}$) $\implies$ điện áp quá điều khiển thực tế ở điểm giữa dải chỉ còn $V_{ov,n}(0.9\text{ V}) = 1.8 - 0.9 - 0.866 = 34.1\text{ mV}$!
- $|V_{TH,p}|$ của `pfet_01v8` ($L=0.15\ \mu\text{m}$) tăng từ **$0.688\text{ V}$** (ở $V_{BS}=0$) lên **$0.938\text{ V}$** (ở $V_{BS}=0.9\text{ V}$) $\implies$ quanh $V_{\text{in}} = 0.955\text{–}0.970\text{ V}$ xuất hiện đỉnh nội trở $R_{\text{on,peak}}$ nơi NMOS và PMOS chuyển giao quyền dẫn.

| Cấu hình `TG` ($L = 0.15\ \mu\text{m}$) | $R_{\text{on},n}$ tại $0.9\text{ V}$ | $R_{\text{on},p}$ tại $0.9\text{ V}$ | $R_{\text{on,TG}}$ tại $0.9\text{ V}$ | $R_{\text{on,max}}$ toàn dải (`tt 27°C`) | $R_{\text{on,max}}$ ở góc xấu `ss 27°C` | Đánh giá Gate ($< 5\text{ k}\Omega$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| $W_n = 2\ \mu\text{m}, W_p = 6\ \mu\text{m}$ | $4.97\text{ k}\Omega$ | $15.89\text{ k}\Omega$ | $3.78\text{ k}\Omega$ | $4.61\text{ k}\Omega$ (tại $0.955\text{ V}$) | $9.1\text{ k}\Omega$ | Đạt ở `tt`, sát ngưỡng ở `ss`. |
| **$W_n = 4\ \mu\text{m}, W_p = 12\ \mu\text{m}$** | **$2.19\text{ k}\Omega$** | **$8.51\text{ k}\Omega$** | **$1.74\text{ k}\Omega$** | **$2.26\text{ k}\Omega$ (tại $0.965\text{ V}$)** | **$4.53\text{ k}\Omega$** | **PASS vững chắc cả `tt` & `ss 27°C`** |
| $W_n = 8\ \mu\text{m}, W_p = 24\ \mu\text{m}$ | $0.95\text{ k}\Omega$ | $4.39\text{ k}\Omega$ | $0.78\text{ k}\Omega$ | $1.03\text{ k}\Omega$ (tại $0.970\text{ V}$) | $2.06\text{ k}\Omega$ | $R_{\text{on}}$ rất thấp nhưng tăng $Q_{\text{ch}}$ gấp đôi. |

![Đặc tuyến Ron(Vin) thực đo trên sky130A](file:///headless/ANN/sky130-sc-lpf/slides/figs/week1_tg_ron.png)

#### (c) Tiêm điện tích kênh dẫn (Charge Injection) & Xuyên nhiễu xung nhịp (Clock Feedthrough)
Từ thông số BSIM4 thực đo của `sky130A`:
- Điện dung oxit cổng đơn vị:
  $$C_{ox,n} = \frac{\varepsilon_0 \varepsilon_{\text{ox}}}{t_{oxe,n}} = \frac{8.854\times 10^{-12} \times 3.9}{4.148\times 10^{-9}} = \mathbf{8.325\text{ fF}/\mu\text{m}^2}, \qquad C_{ox,p} = \frac{8.854\times 10^{-12} \times 3.9}{4.230\times 10^{-9}} = \mathbf{8.163\text{ fF}/\mu\text{m}^2}$$
- **Sai số Charge Injection ($\Delta V_{\text{CI}}$):** Khi khóa tắt nhanh, khoảng $50\%$ điện tích lớp nghịch đảo tràn sang tụ giữ $C_{\text{hold}}$:
  $$\Delta V_{\text{CI,net}} = -\frac{Q_{\text{ch},n} - |Q_{\text{ch},p}|}{2 C_{\text{hold}}} = -\frac{W_n L C_{ox,n}(V_{DD} - V_{\text{in}} - V_{TH,n}) - W_p L C_{ox,p}(V_{\text{in}} - |V_{TH,p}|)}{2 C_{\text{hold}}}$$
  Tại $V_{\text{in}} = V_{CM} = 0.9\text{ V}$ với khóa `TG` ($2\ \mu\text{m} / 6\ \mu\text{m}$), do kênh dẫn ở sát ngưỡng ($V_{ov,n} = 34.1\text{ mV}$), điện tích kênh rất nhỏ: $Q_{\text{ch},n} = 0.0851\text{ fC} \implies \Delta V_{\text{CI}} = \mathbf{0.425\text{ mV}}$ trên $C_1 = 100\text{ fF}$ (và chỉ $\mathbf{0.053\text{ mV}}$ trên $C_2 = 800\text{ fF}$!).
- **Sai số Clock Feedthrough ($\Delta V_{\text{CF}}$):** Xung điều khiển $\Phi$ ($0 \leftrightarrow 1.8\text{ V}$) ghép qua tụ chồng lấp cổng–máng $C_{ov} = W \cdot C_{gdo}$:
  - Từ Ngspice `.op`: $C_{ov,n}(W_n=2\ \mu\text{m}) = 0.4926\text{ fF}$ ($\implies \Delta V_{\text{CF},n} = -8.824\text{ mV}$ trên $C_1$) và $C_{ov,p}(W_p=6\ \mu\text{m}) = 0.4441\text{ fF}$ ($\implies \Delta V_{\text{CF},p} = +7.959\text{ mV}$ trên $C_1$).
  - Nhờ hai xung $\Phi$ và $\overline{\Phi}$ ngược pha nhau, hai gai điện áp tự triệt tiêu hơn $90\%$:
    $$\Delta V_{\text{CF,net}} = \Delta V_{\text{CF},n} + \Delta V_{\text{CF},p} = -8.824 + 7.959 = \mathbf{-0.865\text{ mV}} \text{ (trên } C_1=100\text{ fF)}$$
    và trên nút tích phân $C_2 = 800\text{ fF}$ chỉ còn **$-0.108\text{ mV}$**!

---

### 2.4 Lý thuyết Bộ khuếch đại 5T-OTA: Độ lợi $A_{OL}$, Ổn định Phase Margin & Quỹ áp Sky130A

1. **Độ lợi vòng hở DC ($A_{OL}$) và sai số đệm hồi tiếp đơn vị:**
   $$A_{OL} = g_{m1,2}(r_{o2} \parallel r_{o4}) = \frac{2}{\left(\lambda_n + \lambda_p\right) V_{ov1,2}}$$
   Khi mắc hồi tiếp âm đơn vị ($\beta = 1$, nối $V_{\text{out}}$ về cổng đảo $V_{\text{in}-}$ và đưa nút tích phân $V_X$ vào cổng thuận $V_{\text{in}+}$):
   $$\frac{V_{\text{out}}}{V_X} = \frac{A_{OL}}{1 + A_{OL}} = 1 - \epsilon_A, \qquad \epsilon_A = \frac{1}{1 + A_{OL}}$$
   - Nếu $A_{OL} = 35\text{ dB}$ ($56.2\text{ V/V}$): sai số tĩnh $\epsilon_A = 1.75\%$.
   - Nếu $A_{OL} = 40\text{ dB}$ ($100\text{ V/V}$): sai số tĩnh $\epsilon_A = \mathbf{0.99\%} < 1\%$.
2. **Băng thông ($\text{GBW}$), Điểm cực phụ ($f_{p2}$) và Tiêu chuẩn ổn định ($\text{PM} \ge 60^\circ$):**
   - Cực chính tại ngõ ra: $f_{p1} = \frac{1}{2\pi (r_{o2}\parallel r_{o4}) C_L} \implies \text{GBW} = A_{OL} f_{p1} = \frac{g_{m1,2}}{2\pi C_L}$.
   - Với $C_L = 1\text{ pF}$ và mục tiêu $\text{GBW} \ge 10\text{ MHz}$: cần $g_{m1,2} \ge 2\pi \times 10\text{ MHz} \times 1\text{ pF} = \mathbf{62.83\ \mu\text{S}}$ (hằng số thời gian vòng kín $\tau_{\text{OTA}} = \frac{1}{2\pi\,\text{GBW}} \le 15.9\text{ ns} < \frac{T_{\text{clk}}}{2}$).
   - Cực phụ tại nút gương dòng PMOS (`M3/M4`): $f_{p2} = \frac{g_{m3}}{2\pi C_X}$ với $C_X \approx C_{gs3} + C_{gs4} + C_{db1} + C_{db3}$.
   - Biên dự trữ pha ở hồi tiếp đơn vị ($\beta = 1$):
     $$\text{PM} \approx 90^\circ - \arctan\left(\frac{\text{GBW}}{f_{p2}}\right) \ge 60^\circ \iff \boxed{f_{p2} \ge \sqrt{3}\,\text{GBW} \approx 1.732\,\text{GBW}}$$
3. **Phát hiện quan trọng về Quỹ áp (ICMR / Headroom) của 5T-OTA trên `sky130A`:**
   - Dải đồng pha đầu vào đảm bảo cả 5 transistor `M1–M5` bão hòa:
     $$V_{\text{in,cm,min}} = V_{GS1} + V_{dsat5}, \qquad V_{\text{in,cm,max}} = V_{DD} - V_{SG3} + V_{TH1}$$
   - Do `pfet_01v8` có $|V_{TH,p}| \approx 0.99\text{ V}$ ($V_{SG3} \approx 1.13\text{ V} \implies V_{D1} = 1.8 - 1.13 = 0.671\text{ V}$), trần trên là $V_{\text{in,cm,max}} \approx 0.671 + 0.669 = \mathbf{1.340\text{ V}}$ (dư $+0.44\text{ V}$ phía trên $V_{CM}=0.9\text{ V}$).
   - Ở phía dưới, nếu chọn $(W/L)_1 = 10/0.5$ ở $I_{D1}=20\ \mu\text{A}$ thì $V_{GS1} = 0.724\text{ V}$ và $V_{dsat5} = 0.162\text{ V} \implies V_{\text{in,cm,min}} = 0.886\text{ V}$ (rất sát $0.9\text{ V}$!).
   - **Chỉ dẫn thiết kế cho Tuần 2 (`sizing_calc.py`):** Tăng tỷ số $(W/L)_{1,2}$ (đưa `M1, M2` vào vùng nghịch đảo trung bình/yếu, hạ $V_{GS1} \le 0.62\text{–}0.65\text{ V}$) và tăng $(W/L)_5$ để $V_{dsat5} \le 0.10\text{ V}$ (hoặc giảm nhẹ $I_{\text{tail}} \approx 20\text{–}30\ \mu\text{A}$), giúp hạ $V_{\text{in,cm,min}}$ xuống $\le 0.72\text{ V}$ để mở rộng biên độ dao động tuyến tính đối xứng quanh $0.9\text{ V}$!

---

## 3. Nhiệm vụ 1.3 & Cổng Kiểm Định Tuần 1 (Verification Gate 1)

### 3.1 Kết quả kiểm định thứ nguyên tự động (22/22 công thức PASS tuyệt đối)
Script [week1_verify.py](file:///headless/ANN/sky130-sc-lpf/python/week1_verify.py) đã phân tích tự động số mũ hệ SI cơ sở $(\text{kg}, \text{m}, \text{s}, \text{A}, \text{K})$ cho toàn bộ 22 phương trình của dự án (trích từ [week1_numbers.json](file:///headless/ANN/sky130-sc-lpf/python/week1_numbers.json)):

| STT | Công thức | Thứ nguyên SI dẫn xuất | Đơn vị chuẩn | Kết quả |
| :-: | :--- | :---: | :---: | :---: |
| 1 | $R_{\text{eq}} = \frac{1}{f_{\text{clk}} C_1}$ | $\text{kg}\cdot\text{m}^2\cdot\text{s}^{-3}\cdot\text{A}^{-2}$ | $\Omega$ | ✅ PASS |
| 2 | $\tau = R \cdot C$ | $\text{s}$ | $\text{s}$ | ✅ PASS |
| 3 | $f_{c,\text{RC}} = \frac{1}{2\pi R_{\text{eq}} C_2} = \frac{f_{\text{clk}} C_1}{2\pi C_2}$ | $\text{s}^{-1}$ | $\text{Hz}$ | ✅ PASS |
| 4 | $\alpha = \frac{C_1}{C_1 + C_2}$ | $1$ | Không thứ nguyên | ✅ PASS |
| 5 | $Q = C \cdot V$ (Bảo toàn điện tích) | $\text{s}\cdot\text{A}$ | $\text{C}$ | ✅ PASS |
| 6 | $\omega_c T_{\text{clk}}$ (Đối số $\arccos$) | $1$ | $\text{rad}$ | ✅ PASS |
| 7 | $\text{OSR} = \frac{f_{\text{clk}}}{2 f_c}$ | $1$ | Không thứ nguyên | ✅ PASS |
| 8 | $\overline{v_n^2} = \frac{k_B T}{C}$ | $\text{kg}^2\cdot\text{m}^4\cdot\text{s}^{-6}\cdot\text{A}^{-2}$ | $\text{V}^2$ | ✅ PASS |
| 9 | $I_D = \frac{1}{2}\mu C_{ox}\frac{W}{L}V_{ov}^2$ | $\text{A}$ | $\text{A}$ | ✅ PASS |
| 10 | $g_m = \mu C_{ox}\frac{W}{L}V_{ov} = \frac{2 I_D}{V_{ov}}$ | $\text{kg}^{-1}\cdot\text{m}^{-2}\cdot\text{s}^3\cdot\text{A}^2$ | $\text{S}$ ($\Omega^{-1}$) | ✅ PASS |
| 11 | $R_{\text{on}} = \left[\mu C_{ox}\frac{W}{L}(V_{GS}-V_{TH})\right]^{-1}$ | $\text{kg}\cdot\text{m}^2\cdot\text{s}^{-3}\cdot\text{A}^{-2}$ | $\Omega$ | ✅ PASS |
| 12 | $r_o = \frac{1}{\lambda I_D}$ | $\text{kg}\cdot\text{m}^2\cdot\text{s}^{-3}\cdot\text{A}^{-2}$ | $\Omega$ | ✅ PASS |
| 13 | $A_{OL} = g_{m1,2}(r_{o2}\parallel r_{o4})$ | $1$ | $\text{V/V}$ | ✅ PASS |
| 14 | $\text{GBW} = \frac{g_{m1,2}}{2\pi C_L}$ và $f_{p2} = \frac{g_{m3}}{2\pi C_X}$ | $\text{s}^{-1}$ | $\text{Hz}$ | ✅ PASS |
| 15 | $\text{SR} = \frac{I_{\text{tail}}}{C_L}$ | $\text{kg}\cdot\text{m}^2\cdot\text{s}^{-4}\cdot\text{A}^{-1}$ | $\text{V/s}$ | ✅ PASS |
| 16 | $\Delta V_{\text{CI}} = \frac{W L C_{ox} V_{ov}}{2 C_{\text{hold}}}$ & $\Delta V_{\text{CF}} = V_{DD}\frac{W C_{ov}}{W C_{ov}+C_{\text{hold}}}$ | $\text{kg}\cdot\text{m}^2\cdot\text{s}^{-3}\cdot\text{A}^{-1}$ | $\text{V}$ | ✅ PASS |
| 17 | $C_{\text{mim}} = C_A(W+\Delta w)(L+\Delta w)$ | $\text{kg}^{-1}\cdot\text{m}^{-2}\cdot\text{s}^4\cdot\text{A}^2$ | $\text{F}$ | ✅ PASS |

### 3.2 Bảng Khóa Cứng Kiến Trúc 4 Khối Con (Architecture Lock — Gate 1)

| Khối chức năng | Mã định danh | Linh kiện PDK `sky130A` | Chỉ tiêu Verification Gate (Tuần 3 & 4) |
| :--- | :--- | :--- | :--- |
| **1. Tạo xung 2 pha không chồng lấn** | `non_overlap_clk` | `sky130_fd_pr__nfet_01v8`<br>`sky130_fd_pr__pfet_01v8` (NAND2 + chuỗi Inverter trễ) | $f_{\text{clk}} = 10\text{ MHz}$, khoảng chết $t_{\text{nov}} \in [2\text{ ns}, 5\text{ ns}]$ (mục tiêu $2.5\text{–}3.0\text{ ns}$), đầy đủ 4 pha $\Phi_1, \Phi_2, \overline{\Phi_1}, \overline{\Phi_2}$. |
| **2. Khóa truyền dẫn CMOS** | `tg_switch` (`TG1, TG2`) | `nfet_01v8` ($L=0.15\ \mu\text{m}$) $\parallel$ `pfet_01v8` ($L=0.15\ \mu\text{m}$) | $R_{\text{on}}(V_{\text{in}}) < 5\text{ k}\Omega$ phẳng trên toàn dải quanh $V_{CM} = 0.9\text{ V}$ (Baseline đề xuất: $W_n/W_p = 4\ \mu\text{m}/12\ \mu\text{m} \implies R_{\text{on}}(0.9\text{ V}) = 1.74\text{ k}\Omega$). |
| **3. Lõi tụ chuyển mạch MIM** | `sc_core` (`C1, C2`) | `sky130_fd_pr__cap_mim_m3_1`<br>($W=4.85\ \mu\text{m}, L=9.85\ \mu\text{m}$) | $C_1 = 1\times C_{\text{unit}} = 100.00\text{ fF}$, $C_2 = 8\times C_{\text{unit}} = 800.00\text{ fF}$ ($\alpha = 1/9, f_{c,\text{SC}} = 187.675\text{ kHz}$). |
| **4. Bộ đệm hồi tiếp đơn vị 5T-OTA** | `ota_5t` (`M1–M5`) | Cặp vi sai NMOS `M1, M2`; Gương dòng PMOS `M3, M4`; Nguồn dòng đuôi `M5` | Cả 5 MOSFET bão hòa ($V_{DS} > V_{dsat}$), $A_{OL} > 35\text{–}40\text{ dB}$, $\text{GBW} > 10\text{ MHz}$, $\text{PM} \ge 60^\circ$ ($C_L = 1\text{ pF}$). |
