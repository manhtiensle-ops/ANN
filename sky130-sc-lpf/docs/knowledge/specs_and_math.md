# Nền Tảng Toán Học & Lý Thuyết Thiết Kế Mạch (`sky130-sc-lpf`)

> **Nguồn chân lý kỹ thuật (Single Source of Truth):** Mọi phương trình, thứ nguyên và mốc chuẩn cho Golden Model (Tuần 2), Schematic/Ngspice (Tuần 3) và Post-Layout PEX (Tuần 4).

---

## 1. Cơ Sở Chọn Thông Số (Design Rationale)

### 1.1 Vì sao không tích hợp điện trở $R = 1\text{ M}\Omega$ trên Sky130A?
- Điện trở thanh đa tinh thể độ trở cao nhất phổ biến của `sky130A` (`sky130_fd_pr__res_high_po`, $R_{\square} \approx 2\text{ k}\Omega/\square$; hoặc poly thường $R_{\square} \approx 48\ \Omega/\square$):
  - Với poly thường ($W = 0.5\ \mu\text{m}$): $N_{\square} \approx 20{,}833 \implies L \approx 10{,}417\ \mu\text{m}$ (không khả thi).
  - Với high-sheet-rho poly ($W = 0.35\ \mu\text{m}$, $500\ \square$): diện tích vẫn rất lớn kèm tụ ký sinh xuống nền và **dung sai tuyệt đối $\Delta R / R \approx \pm 20\%$** theo góc công nghệ & nhiệt độ (PVT) $\implies$ tần số cắt $f_c = \frac{1}{2\pi R C_2}$ trôi $\pm 25\text{–}30\%$.
- **Lợi thế Tụ chuyển mạch (Switched-Capacitor):**
  - Điện trở tương đương:
    $$R_{\text{eq}} = \frac{T_{\text{clk}}}{C_1} = \frac{1}{f_{\text{clk}} C_1} = \frac{1}{10\times 10^6\text{ Hz} \times 100\times 10^{-15}\text{ F}} = 1.00\text{ M}\Omega$$
  - Hằng số thời gian chỉ phụ thuộc vào **tỷ số hai tụ MIM cùng loại** và tần số thạch anh $f_{\text{clk}}$:
    $$f_{c,\text{RC}} = \frac{f_{\text{clk}}}{2\pi} \cdot \frac{C_1}{C_2}$$
  - Với mảng tụ đơn vị MIM + Dummy viền ngoài, độ lệch ghép đôi $\Delta(C_1/C_2) < 0.1\%$, diện tích tổng $(1+8)\times 50\ \mu\text{m}^2 = 450\ \mu\text{m}^2$ cực kỳ nhỏ gọn.

### 1.2 Lý do chọn từng thông số cốt lõi
| Thông số | Giá trị khóa cứng | Cơ sở Vật lý & Hệ thống |
| :--- | :--- | :--- |
| $f_{\text{clk}}$ | $10\text{ MHz}$ ($T_{\text{clk}}=100\text{ ns}$) | Tỷ lệ quá lấy mẫu $\text{OSR} = \frac{f_{\text{clk}}}{2 f_c} \approx 25 \gg 1$: đẩy tần số ảnh (image/aliasing quanh $f_{\text{clk}} - f_c \approx 9.8\text{ MHz}$) ra rất xa dải thông, nới lỏng yêu cầu lọc chống chồng phổ (Anti-Aliasing Filter) đầu vào. |
| $C_1, C_2$ | $100\text{ fF}, 800\text{ fF}$ ($1:8$) | Đủ lớn để áp đảo tụ ký sinh đường dây ($\sim 1\text{–}3\text{ fF}$) và giữ nhiễu nhiệt $\sqrt{kT/C_1} \approx 203.5\ \mu\text{V}_{\text{rms}}$ ($\sqrt{kT/C_2} \approx 72.0\ \mu\text{V}_{\text{rms}}$ ở $300\text{ K}$); đủ nhỏ để tổng diện tích MIM chỉ $\sim 450\ \mu\text{m}^2$ và giảm tải cho OTA. |
| $V_{DD}, V_{CM}$ | $1.8\text{ V}, 0.9\text{ V}$ | Đặt $V_{CM} = V_{DD}/2 = 0.9\text{ V}$ giúp biên độ dao động đầu vào/ra đối xứng cực đại ($\pm 0.4\text{ V}$ tuyến tính), đồng thời cả NMOS và PMOS của khóa `TG` đều dẫn mạnh ở điểm giữa dải. |

---

## 2. Dẫn Xuất Hàm Truyền Miền Z Chính Xác (2-Phase Passive SC + Unity-Gain Buffer)

### Cấu trúc mạch lõi SC LPF (Bậc 1 nối tiếp — đệm đầu ra bằng 5T-OTA hồi tiếp đơn vị)
- `TG1` nối giữa $V_{\text{in}}$ và nút trên của $C_1$ (điều khiển bởi $\Phi_1, \overline{\Phi_1}$).
- `TG2` nối giữa nút trên của $C_1$ và nút lưu trữ $V_X$ (cực trên của $C_2$, đồng thời nối vào cổng thuận $V_{\text{in}+}$ của 5T-OTA mắc đệm đơn vị $V_{\text{out}} \approx V_X$, điều khiển bởi $\Phi_2, \overline{\Phi_2}$). Cực dưới của $C_1$ và $C_2$ nối về đất AC ($V_{SS}$ hoặc $V_{CM}$; điện tích AC tương đương hoàn toàn).
- **Pha $\Phi_1$ (Lấy mẫu — thời điểm $n - \frac{1}{2}$):** `TG1` đóng, `TG2` ngắt:
  - $C_1$ nạp tới $V_{\text{in}}\left[n-\frac{1}{2}\right]$ (xấp xỉ $V_{\text{in}}[n]$ với tín hiệu lấy mẫu giữ mẫu): $Q_1^{(1)} = C_1 V_{\text{in}}[n]$.
  - $C_2$ giữ nguyên điện áp chu kỳ trước: $Q_2^{(1)} = C_2 V_{\text{out}}[n-1]$.
- **Pha $\Phi_2$ (Chia sẻ điện tích — thời điểm $n$):** `TG1` ngắt (trước khi `TG2` đóng một khoảng $t_{\text{nov}}$), `TG2` đóng nối song song $C_1 \parallel C_2$ vào ngõ vào trở kháng cực cao của 5T-OTA ($I_G = 0$):
  $$Q_{\text{total}}^{(2)} = Q_{\text{total}}^{(1)} \implies (C_1 + C_2) V_{\text{out}}[n] = C_1 V_{\text{in}}[n] + C_2 V_{\text{out}}[n-1]$$
  $$\iff (C_1 + C_2)V_{\text{out}}[n] - C_2 V_{\text{out}}[n-1] = C_1 V_{\text{in}}[n]$$
- Đặt $\alpha = \frac{C_1}{C_1 + C_2} = \frac{100}{100 + 800} = \frac{1}{9}$ và $1 - \alpha = \frac{C_2}{C_1 + C_2} = \frac{8}{9}$, biến đổi Z cho:
  $$H(z) = \frac{V_{\text{out}}(z)}{V_{\text{in}}(z)} = \frac{\alpha}{1 - (1 - \alpha)z^{-1}} = \frac{1/9}{1 - \frac{8}{9}z^{-1}}$$

### Tần số cắt $-3\text{ dB}$ rời rạc chính xác ($f_{c,\text{SC}}$) vs. Xấp xỉ $RC$ ($f_{c,\text{RC}}$)
- Tại DC ($z = e^{j0} = 1$): $H(e^{j0}) = \frac{\alpha}{1 - (1-\alpha)} = 1 = 0\text{ dB}$.
- Tại tần số cắt $\omega_c$: $|H(e^{j\omega_c T_{\text{clk}}})|^2 = \frac{1}{2}$:
  $$\frac{\alpha^2}{1 + (1-\alpha)^2 - 2(1-\alpha)\cos(\omega_c T_{\text{clk}})} = \frac{1}{2} \implies \cos(\omega_c T_{\text{clk}}) = 1 - \frac{\alpha^2}{2(1-\alpha)}$$
- Thay $\alpha = \frac{1}{9}$:
  $$\cos(\omega_c T_{\text{clk}}) = 1 - \frac{1/81}{16/9} = 1 - \frac{1}{144} = \frac{143}{144} \implies f_{c,\text{SC}} = \frac{10\text{ MHz}}{2\pi}\arccos\left(\frac{143}{144}\right) \approx 187.67\text{ kHz}$$
- Lý do vật lý $f_{c,\text{SC}} = 187.67\text{ kHz} < f_{c,\text{RC}} = 198.94\text{ kHz}$ ($-5.66\%$): Ở pha $\Phi_2$, $C_1$ mắc song song với $C_2$ nên hằng số suy giảm mỗi chu kỳ là $\frac{C_2}{C_1+C_2} = \frac{8}{9}$ thay vì $1 - \frac{C_1}{C_2} = \frac{7}{8}$.

---

## 3. Các Hiệu Ứng Phi Lý Tưởng & Công Thức Ngân Sách Lỗi (Razavi Ch. 2, 9, 12)

1. **Nội trở khóa truyền dẫn CMOS ($R_{\text{on}}$):**
   $$R_{\text{on,TG}}(V_{\text{in}}) = R_{\text{on},n} \parallel R_{\text{on},p} = \left[\mu_n C_{ox}\left(\frac{W}{L}\right)_n (V_{DD} - V_{\text{in}} - V_{TH,n}) + \mu_p C_{ox}\left(\frac{W}{L}\right)_p (V_{\text{in}} - |V_{TH,p}|)\right]^{-1}$$
   - Để sai số nạp tụ tĩnh $\epsilon_{\text{set}} = e^{-t_{\text{on}}/\tau} < 0.1\%$ trong $t_{\text{on}} \approx 47\text{ ns}$ ($50\text{ ns} - t_{\text{nov}}$), cần $\tau = R_{\text{on}} C_1 < \frac{47\text{ ns}}{\ln 1000} \approx 6.8\text{ ns} \implies R_{\text{on,max}} \ll 68\text{ k}\Omega$. Đặt **ngưỡng thiết kế chặt $R_{\text{on}} < 5\text{ k}\Omega$** ($\tau < 0.5\text{ ns}$, tức $>90\tau$) nhằm triệt tiêu luôn méo hài động THD do $R_{\text{on}}(V_{\text{in}})$ biến thiên theo tín hiệu!
2. **Tiêm điện tích kênh dẫn (Charge Injection) & Xuyên nhiễu xung nhịp (Clock Feedthrough):**
   - Kênh dẫn NMOS khi tắt giải phóng điện tích $Q_{\text{ch}} = -W L C_{ox}(V_{DD} - V_{\text{in}} - V_{TH,n})$:
     $$\Delta V_{\text{CI}} \approx -\frac{W L C_{ox}(V_{GS} - V_{TH})}{2 C_{\text{hold}}}, \qquad \Delta V_{\text{CF}} = -V_{DD}\frac{W C_{ov}}{W C_{ov} + C_{\text{hold}}}$$
   - Khóa truyền dẫn CMOS (`NMOS || PMOS`) tự triệt tiêu một phần điện tích ngược dấu quanh $V_{CM}=0.9\text{ V}$; có thể bổ sung **Dummy Switch** ($W_{\text{dummy}} = W/2$, nối chập D–S, điều khiển bằng pha đảo) nếu gai chuyển mạch vượt ngưỡng.
3. **Độ lợi vòng hở hữu hạn ($A_{OL}$), Băng thông ($\text{GBW}$) & Biên pha ($\text{PM}$) của 5T-OTA:**
   - Độ lợi vòng hở tín hiệu nhỏ: $A_{OL} = g_{m1,2}(r_{o2} \parallel r_{o4})$.
   - Trong mắc đệm hồi tiếp đơn vị ($\beta = 1$): hệ số truyền thực tế của bộ đệm là:
     $$A_{\text{buf}} = \frac{A_{OL}}{1 + A_{OL}} \approx 1 - \frac{1}{A_{OL}}$$
     Với $A_{OL} = 40\text{ dB}$ ($100\text{ V/V}$), sai số biên độ DC chỉ $\approx 1\%$ ($-0.086\text{ dB}$) và không làm lệch vị trí điểm cực rời rạc của lõi tụ $C_1, C_2$ (vì $C_1, C_2$ chia sẻ điện tích thụ động ở ngõ vào $V_{\text{in}+}$ trở kháng cao của 5T-OTA, còn tụ vào $C_{\text{in,OTA}} = C_{gs1}/(1+A_{OL}) + C_{gd1} \ll C_2 = 800\text{ fF}$!).
   - Băng thông hồi tiếp đơn vị: $\text{GBW} = \frac{g_{m1,2}}{2\pi C_L} > 10\text{ MHz}$ ($\tau_{\text{OTA}} = \frac{1}{2\pi\,\text{GBW}} < 15.9\text{ ns}$, nạp ổn định trong bán chu kỳ $50\text{ ns}$).
   - Tiêu chuẩn ổn định vòng kín ($\beta = 1$): cực phụ tại nút gương dòng $p_2 = \frac{g_{m3}}{2\pi C_X}$ phải thỏa $f_{p2} \ge \sqrt{3}\,\text{GBW} \implies \text{PM} = 90^\circ - \arctan(\text{GBW}/f_{p2}) \ge 60^\circ$.
4. **Quy tắc Ngspice `.op`, `.ac`, `.tran` cho mạch Tụ chuyển mạch:**
   - Lệnh `.ac` tuyến tính hóa mạch tại **một điểm làm việc tĩnh duy nhất** (`.op`) tại $t=0$: tại đó $\Phi_1$ đang ở 1 trạng thái cố định và $\Phi_2$ ở trạng thái ngược lại $\implies$ một khóa luôn hở vĩnh viễn ($R_{\text{off}} \sim \text{G}\Omega$), không bao giờ mô phỏng được cơ chế chuyển gói điện tích rời rạc theo chu kỳ!
   - Do đó: `.op` và `.ac` chỉ dùng để kiểm định khối tuyến tính thời gian liên tục (`ota_5t`); còn đáp ứng tần số và phổ của `top_sc_lpf` **bắt buộc đo bằng `.tran` + Coherent FFT**.
