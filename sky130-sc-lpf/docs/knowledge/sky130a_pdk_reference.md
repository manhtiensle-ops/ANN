# Tham Chiếu Thực Nghiệm PDK `sky130A` & Hệ Sinh Thái `iic-osic-tools`

> Tất cả đường dẫn và số liệu dưới đây đã được kiểm chứng trực tiếp bằng `ngspice-47` trên `/foss/pdks/sky130A` trong môi trường hiện tại (`IIC_OSIC_TOOLS_VERSION=2026.10`).

---

## 1. Đường Dẫn Chuẩn Của PDK `sky130A`
- **Thư mục gốc PDK:** `/foss/pdks/sky130A`
- **Script chuyển môi trường dự án:** [env_sky130.sh](file:///headless/ANN/sky130-sc-lpf/env_sky130.sh) *(Bắt buộc `source` vì container mặc định đang đặt `PDK=ihp-sg13g2`)*
- **Mô hình BSIM4 liên tục (Continuous Models — Khuyên dùng cho Ngspice & Xschem):**
  ```spice
  .lib "/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice" tt
  ```
  Các góc công nghệ hỗ trợ sẵn: `tt`, `ss`, `sf`, `fs`, `ff`, `hh`, `ll`, `tt_mm`, `mc`.
- **Cấu hình Ngspice bắt buộc (`.spiceinit`):**
  ```spice
  set ngbehavior=hsa
  set ng_nomodcheck
  ```
- **Cấu hình Xschem / Magic / Netgen:**
  - Xschem RC: `/foss/pdks/sky130A/libs.tech/xschem/xschemrc` (hoặc bản cục bộ `/headless/ANN/sky130-sc-lpf/xschem/xschemrc`)
  - Magic RC: `/foss/pdks/sky130A/libs.tech/magic/sky130A.magicrc`
  - Netgen LVS Setup: `/foss/pdks/sky130A/libs.tech/netgen/sky130A_setup.tcl`

---

## 2. Quy Ước Đơn Vị & Cú Pháp Linh Kiện `sky130A` (Cực Kỳ Quan Trọng)
Trong `models_global.spice`, PDK khai báo sẵn:
```spice
.option scale=1.0u
```
- **Quy tắc sống còn:** Khi gọi subcircuit `sky130_fd_pr__*`, luôn truyền `w` và `l` bằng **con số trần tính theo micromet ($\mu\text{m}$)** (ví dụ `w=2.0 l=0.5`, **KHÔNG** viết `w=2u l=0.5u` vì nhân với `scale=1u` sẽ biến thành picomet!).
- **Cú pháp truy xuất tham số điểm làm việc BSIM4 trong Ngspice:**
  - Với transistor `XM1 ... sky130_fd_pr__nfet_01v8`:
    `@m.xm1.msky130_fd_pr__nfet_01v8[id]`, `[gm]`, `[gds]`, `[vth]`, `[vgs]`, `[vds]`, `[vdsat]`, `[cgg]`, `[cgd]`, `[cgs]`.
  - Với tụ MIM `XC1 ... sky130_fd_pr__cap_mim_m3_1`:
    `@c.xc1.c1[capacitance]`.

---

## 3. Thông Số Vật Lý BSIM4 Thực Tế Đã Đo Ở Góc `tt` ($27^\circ\text{C}, V_{DD}=1.8\text{ V}$)

### 3.1 Transistor `01v8` (`nfet_01v8` & `pfet_01v8`)
| Hạng mục | `sky130_fd_pr__nfet_01v8` | `sky130_fd_pr__pfet_01v8` | Hệ quả Thiết kế Mạch Thực tế |
| :--- | :--- | :--- | :--- |
| $t_{oxe}$ (BSIM4 model) | $4.148\text{ nm}$ | $4.230\text{ nm}$ | $C_{ox,n} \approx 8.33\text{ fF}/\mu\text{m}^2$, $C_{ox,p} \approx 8.16\text{ fF}/\mu\text{m}^2$ |
| $L_{\min}$ công nghệ | $0.15\ \mu\text{m}$ | $0.15\ \mu\text{m}$ | Dùng $L = 0.15\ \mu\text{m}$ cho khóa `TG` & cổng logic `clk`; dùng $L \in [0.5, 1.0]\ \mu\text{m}$ cho `5T-OTA` để tăng $r_o$ và đạt $A_{OL} > 40\text{ dB}$ |
| Điện áp ngưỡng thực tế ($V_{TH}$ ở $L=0.5\ \mu\text{m}, V_{DS}=0.9\text{ V}$) | $V_{TH,n} \approx 0.633\text{ V}$ | $|V_{TH,p}| \approx 0.976\text{ V}$ | **Lưu ý Vàng:** `pfet_01v8` chuẩn của Sky130A có $|V_{TH,p}|$ khá cao ($\sim 0.95\text{–}0.98\text{ V}$)! |
| Nội trở đơn ở $V_{CM}=0.9\text{ V}$ ($L=0.15\ \mu\text{m}$) | $W_n=2\ \mu\text{m} \Rightarrow R_{n}\approx 4.87\text{ k}\Omega$ | $W_p=6\ \mu\text{m} \Rightarrow R_{p}\approx 15.95\text{ k}\Omega$ | Tại $V_{\text{in}}=0.9\text{ V}$, $R_{\text{on,TG}}(2\mu/6\mu) \approx 3.73\text{ k}\Omega < 5\text{ k}\Omega$. Chọn $W_n \approx 2\text{–}3\ \mu\text{m}, W_p \approx 6\text{–}9\ \mu\text{m}$ cho đường cong $R_{\text{on}}$ phẳng và thấp trên toàn dải. |
| Quỹ áp (Headroom) 5T-OTA hồi tiếp đơn vị ($V_{CM}=0.9\text{ V}$) | $V_{GS1} \approx 0.68\text{–}0.72\text{ V} \Rightarrow V_{\text{tail}} \approx 0.18\text{–}0.22\text{ V}$ | $V_{SG3} \approx 1.05\text{–}1.12\text{ V} \Rightarrow V_{D1}=V_{D3} \approx 0.68\text{–}0.75\text{ V}$ | Tại $V_{\text{in}}=V_{\text{out}}=0.9\text{ V}$: $V_{DS1} \approx 0.50\text{ V} \gg V_{DS,\text{sat}1}$ ($\sim 85\text{ mV}$) và $V_{DS5} \approx 0.20\text{ V} > V_{DS,\text{sat}5}$ ($\sim 110\text{ mV}$). Cần giữ $V_{ov5} \le 130\text{–}150\text{ mV}$ để `M5` bão hòa vững chắc! |

### 3.2 Công thức Tụ MIM `sky130_fd_pr__cap_mim_m3_1` Chính Xác 100%
Theo `continuous/models_capacitors.spice` & `parameters_cap_nom.spice`:
- $C_A = \text{sw\_cap\_mim\_ca} = 2.0\text{ fF}/\mu\text{m}^2$, độ bù biên $\Delta w = \text{sw\_cap\_mim\_dw} = 0.15\ \mu\text{m}$:
  $$C_{\text{mim}}(W, L, \text{mult}) = \text{mult} \times 2.0\text{ fF}/\mu\text{m}^2 \times (W + 0.15) \times (L + 0.15)$$
- **Kích thước Ô Đơn Vị Chuẩn (Golden Unit Cell $C_{\text{unit}} = 100.000\text{ fF}$ chẵn lưới Magic $0.05\ \mu\text{m}$):**
  - Chọn **$W = 4.85\ \mu\text{m}, L = 9.85\ \mu\text{m}$** $\implies W_{\text{eff}} = 5.00\ \mu\text{m}, L_{\text{eff}} = 10.00\ \mu\text{m} \implies C_{\text{unit}} = 2.0 \times 50.00 = \mathbf{100.000\text{ fF}}$!
  - Hoặc ô vuông gần đúng: $W = 6.92\ \mu\text{m}, L = 6.92\ \mu\text{m} \implies C_{\text{unit}} = 99.970\text{ fF}$ (đã kiểm chứng Ngspice: `9.996980e-14 F`).
  - Lõi `sc_core`:
    - $C_1$: `w=4.85 l=9.85 mult=1` ($100.00\text{ fF}$)
    - $C_2$: `w=4.85 l=9.85 mult=8` ($800.00\text{ fF}$, ghép song song 8 ô đơn vị đồng nhất đảm bảo tỷ số $C_2/C_1 = 8.000$ bất chấp sai số khắc biên $\Delta w$!).
