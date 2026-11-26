#!/usr/bin/env python3
"""
Generate pedagogical 300-DPI IEEE figures for Week 1 storytelling slides
using the verified Single Source of Truth (python/week1_numbers.json).

Outputs:
  slides/figs/week1_io_expected.png         (Time-domain Multi-tone I/O + Z-domain Bode/Alias)
  slides/figs/week1_rc_vs_sc_pvt.png        (Enhanced PVT bar chart with explicit SC 0.0% markers)
  slides/figs/week1_ss_spec_window.png      (S&S Cutoff Window & Integer Ratio K=C2/C1 + f_clk OSR trade-off)
  slides/figs/week1_ss_ota_noise_bridge.png (kT/C Thermal Noise SNR vs C2 + 2nd-Order Step vs Phase Margin)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "slides" / "figs"
NUMBERS_PATH = ROOT / "python" / "week1_numbers.json"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))

from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style  # noqa: E402


def plot_io_expected(spec: dict, path: Path) -> None:
    apply_ieee_style()
    f_clk = spec["f_clk_Hz"]
    T_clk = spec["T_clk_s"]
    alpha = spec["alpha"]
    fc_sc = spec["fc_SC_Hz"]
    fc_rc = spec["fc_RC_Hz"]

    v_cm = 0.9
    f_sig, a_sig = 50e3, 0.30
    f_int, a_int = 2.0e6, 0.12

    n_warmup = 600
    n_show = 400
    n_tot = n_warmup + n_show
    n = np.arange(n_tot)
    t = n * T_clk

    v_in = v_cm + a_sig * np.sin(2 * np.pi * f_sig * t) + a_int * np.sin(2 * np.pi * f_int * t)
    v_out = np.empty_like(v_in)
    y = v_cm
    for k in range(n_tot):
        y = (1.0 - alpha) * y + alpha * v_in[k]
        v_out[k] = y

    t_us = (t[n_warmup:] - t[n_warmup]) * 1e6
    vin_show = v_in[n_warmup:]
    vout_show = v_out[n_warmup:]

    freqs = np.logspace(np.log10(10e3), np.log10(10.5e6), 2400)
    z = np.exp(1j * 2 * np.pi * freqs / f_clk)
    h_sc_db = 20 * np.log10(np.abs(alpha / (1.0 - (1.0 - alpha) / z)))
    h_rc_db = 20 * np.log10(1.0 / np.sqrt(1.0 + (freqs / fc_rc) ** 2))

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(6.8, 5.2), gridspec_kw={"height_ratios": [1.0, 1.15], "hspace": 0.44}
    )

    ax1.plot(t_us, vin_show, color=C["amber"], lw=1.0, alpha=0.82,
             label="INPUT: 50 kHz (0.30 Vp) + 2 MHz nhiễu (0.12 Vp)")
    ax1.step(t_us, vout_show, where="post", color=C["teal"], lw=2.0,
             label="OUTPUT dự kiến H(z): Giữ 50 kHz, nén 2 MHz (−20 dB)")
    ax1.axhline(v_cm, color=C["slate"], lw=0.8, ls=":", alpha=0.7)
    ax1.set_xlim(0, 40)
    ax1.set_ylim(0.42, 1.62)
    ax1.set_yticks([0.5, 0.75, 1.0, 1.25, 1.5])
    ax1.set_xlabel("Thời gian (µs)")
    ax1.set_ylabel("Điện áp (V)")
    ax1.set_title("Mô phỏng lý thuyết I/O: Lọc nhiễu cao tần 2 MHz khỏi tín hiệu 50 kHz")
    ax1.legend(loc="upper center", ncol=1, fontsize=8.0, framealpha=0.96)
    ax1.annotate(
        "Nhiễu 2 MHz giảm 10×\n(120 mVp → 12 mVp)",
        xy=(15.0, vout_show[150]),
        xytext=(21.2, 0.48),
        fontsize=8.0,
        fontweight="bold",
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.28", fc="#F0FDFA", ec=C["teal"], lw=0.9),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.1, connectionstyle="arc3,rad=-0.12"),
    )

    ax2.semilogx(freqs / 1e3, h_rc_db, color=C["slate"], lw=1.3, ls="--",
                 label=f"Xấp xỉ RC liên tục (fc = {fc_rc/1e3:.2f} kHz)")
    ax2.semilogx(freqs / 1e3, h_sc_db, color=C["cobalt"], lw=2.1,
                 label=f"SC-LPF chính xác H(z) (fc = {fc_sc/1e3:.2f} kHz)")

    ax2.axvspan(10, fc_sc / 1e3, color=C["teal"], alpha=0.09)
    ax2.axvspan(5000, 10500, color=C["amber"], alpha=0.09)
    ax2.axhline(-3.01, color=C["crimson"], lw=0.9, ls=":", alpha=0.8)
    ax2.axvline(5000, color=C["amber"], lw=1.0, ls="--", alpha=0.85)

    pts = [
        (50.0, spec["H_at_50kHz_dB"], C["teal"]),
        (fc_sc / 1e3, -3.01, C["crimson"]),
        (2000.0, spec["H_at_2MHz_dB"], C["cobalt"]),
    ]
    for fx, gy, col in pts:
        ax2.plot(fx, gy, "o", color=col, ms=5.5, zorder=5)

    ax2.text(28, -14.2, "Dải thông\n(Passband)", ha="center", fontsize=8.0,
             fontweight="bold", color=C["teal"])
    ax2.annotate(
        "Ảnh Aliasing\n(9.81 MHz)",
        xy=(9600.0, -3.0),
        xytext=(1500, -6.5),
        ha="center",
        fontsize=7.8,
        fontweight="bold",
        color=C["amber"],
        bbox=dict(boxstyle="round,pad=0.22", fc="#FFFBEB", ec=C["amber"], lw=0.8),
        arrowprops=dict(arrowstyle="->", color=C["amber"], lw=1.0),
    )
    ax2.annotate(
        "50 kHz: −0.30 dB",
        xy=(50.0, spec["H_at_50kHz_dB"]),
        xytext=(15.5, -8.5),
        fontsize=7.8,
        fontweight="bold",
        color=C["teal"],
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.0),
    )
    ax2.annotate(
        "fc,SC = 187.7 kHz (−3 dB)",
        xy=(fc_sc / 1e3, -3.01),
        xytext=(310, 0.2),
        fontsize=7.8,
        fontweight="bold",
        color=C["crimson"],
        va="bottom",
        arrowprops=dict(arrowstyle="->", color=C["crimson"], lw=1.0),
    )
    ax2.annotate(
        "2 MHz: −20.0 dB",
        xy=(2000.0, spec["H_at_2MHz_dB"]),
        xytext=(420, -21.5),
        fontsize=7.8,
        fontweight="bold",
        color=C["cobalt"],
        arrowprops=dict(arrowstyle="->", color=C["cobalt"], lw=1.0),
    )
    ax2.text(4650, -14.5, "Nyquist\n5 MHz", ha="right", fontsize=7.5, color=C["amber"], fontweight="bold")

    ax2.set_xlim(10, 10500)
    ax2.set_ylim(-29, 4.5)
    ax2.set_xlabel("Tần số (kHz) — Thang log")
    ax2.set_ylabel("|H(f)| (dB)")
    ax2.set_title("Đáp ứng biên độ H(z): Dải thông, suy giảm nhiễu & khoảng cách ảnh Aliasing")
    ax2.legend(loc="lower left", fontsize=7.8, framealpha=0.96)

    fig.savefig(path)
    plt.close(fig)


def plot_pvt_enhanced(pvt: dict, path: Path) -> None:
    apply_ieee_style()
    labels = list(pvt.keys())
    rc = [pvt[k]["fc_RC_onchip_dev_pct"] for k in labels]
    sc = [pvt[k]["fc_SC_dev_pct"] for k in labels]
    x = np.arange(len(labels))

    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.bar(x - 0.18, rc, 0.36, color=C["amber"], alpha=0.92,
           label="RC trên chip (res_xhigh_po × cap_mim)")
    ax.plot(x + 0.18, sc, color=C["teal"], lw=2.2, marker="o", ms=6.0, zorder=5,
            label="Tụ chuyển mạch SC (f_clk · C₁/C₂ = 0.0%)")

    for xi, v in zip(x, rc):
        if abs(v) > 0.5:
            ax.text(xi - 0.18, v + (1.5 if v > 0 else -1.8), f"{v:+.1f}%",
                    ha="center", va="bottom" if v > 0 else "top",
                    fontsize=8.2, fontweight="bold", color=C["amber"])
        else:
            ax.text(xi - 0.18, 2.2, "0.0%", ha="center", va="bottom",
                    fontsize=7.8, color=C["slate"])

    ax.annotate(
        "SC-LPF: Δfc = 0.0% (7 góc PVT)\nPhụ thuộc duy nhất tỷ số C₁/C₂",
        xy=(3.18, -1.0),
        xytext=(3.0, -32.0),
        ha="center",
        fontsize=7.8,
        fontweight="bold",
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.30", fc="#F0FDFA", ec=C["teal"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.2),
    )

    ax.axhline(0, color="#334155", lw=0.85)
    ax.set_xticks(x, labels, fontsize=8.6)
    ax.set_ylabel("Độ trôi Δfc so với góc chuẩn (%)")
    ax.set_title("Độ trôi tần số cắt qua 7 góc PVT (Sky130A Ngspice-47)", pad=28)
    ax.set_ylim(-43, 46)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=2, fontsize=7.6, framealpha=0.96)
    fig.savefig(path)
    plt.close(fig)


def plot_ss_spec_window(path: Path) -> None:
    """
    2-panel figure showing HOW Signals & Systems specs dictate:
      (Left) Valid cutoff window [143.1, 201.0] kHz and why integer ratio K = C2/C1 = 8 is unique optimal.
      (Right) Sampling clock f_clk trade-off: Aliasing band distance vs required unit capacitor count (1+K).
    """
    apply_ieee_style()
    f_clk = 10e6

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.8, 4.05), gridspec_kw={"wspace": 0.36}
    )

    # --- Left Panel: Stopband Attenuation @ 2 MHz vs Integer Ratio K = C2/C1 ---
    k_cont = np.linspace(5.0, 12.0, 400)
    a_cont = 1.0 / (1.0 + k_cont)
    z_2m = np.exp(1j * 2 * np.pi * 2.0e6 / f_clk)
    z_50k = np.exp(1j * 2 * np.pi * 50.0e3 / f_clk)

    att_2m = -20 * np.log10(np.abs(a_cont / (1.0 - (1.0 - a_cont) / z_2m)))
    loss_50k = -20 * np.log10(np.abs(a_cont / (1.0 - (1.0 - a_cont) / z_50k)))

    valid_mask = (att_2m >= 20.0) & (loss_50k <= 0.5)
    k_valid = k_cont[valid_mask]

    ax1.axvspan(k_valid.min(), k_valid.max(), color=C["teal"], alpha=0.11,
                label="Vùng đạt chuẩn S&S (50k ≤0.5 dB & 2M ≥20 dB)")
    ax1.plot(k_cont, att_2m, color=C["cobalt"], lw=2.1, label="Độ nén nhiễu tại 2 MHz (dB)")
    ax1.axhline(20.0, color=C["crimson"], lw=1.1, ls="--", label="Ngưỡng yêu cầu ≥ 20 dB tại 2 MHz")

    for k_int in range(6, 12):
        al = 1.0 / (1.0 + k_int)
        at = float(-20 * np.log10(np.abs(al / (1.0 - (1.0 - al) / z_2m))))
        ls50 = float(-20 * np.log10(np.abs(al / (1.0 - (1.0 - al) / z_50k))))
        ok = (at >= 20.0) and (ls50 <= 0.5)
        col = C["teal"] if k_int == 8 else (C["crimson"] if not ok else C["navy"])
        ms = 8.5 if k_int == 8 else 5.8
        ax1.plot(k_int, at, "o", color=col, ms=ms, zorder=6)
        if k_int == 7:
            ax1.text(7.15, at - 1.45, f"K=7: {at:.1f} dB\n(Trượt <20 dB)", ha="center",
                     fontsize=7.3, fontweight="bold", color=col)
        elif k_int == 8:
            ax1.text(8.0, at + 0.55, f"K=8\n({at:.1f} dB)", ha="center",
                     fontsize=7.8, fontweight="bold", color=col)
        elif k_int == 11:
            ax1.text(10.85, at - 1.55, "K=11: Trượt\n(>0.5 dB @50k)", ha="center",
                     fontsize=7.2, fontweight="bold", color=col)

    ax1.annotate(
        "CHỐT K = C₂/C₁ = 8\n• fc,SC = 187.7 kHz\n• Nén 2 MHz: 20.02 dB (ĐẠT)\n• Mảng 1+8 = 9 ô (vuông 3×3)",
        xy=(8.0, 20.02),
        xytext=(8.40, 16.25),
        fontsize=7.6,
        fontweight="bold",
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.28", fc="#F0FDFA", ec=C["teal"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.2),
    )

    ax1.set_xlim(5.3, 11.9)
    ax1.set_ylim(15.5, 25.2)
    ax1.set_xlabel("Tỷ số tụ nguyên K = C₂ / C₁ (tại f_clk = 10 MHz)")
    ax1.set_ylabel("Độ nén nhiễu tại 2 MHz (dB)")
    ax1.set_title("1. Ràng buộc phổ khóa chặt K = C₂/C₁ = 8", fontsize=10.8)
    ax1.legend(loc="upper left", fontsize=7.2, framealpha=0.96)

    # --- Right Panel: Why f_clk = 10 MHz? (OSR / Alias vs Unit Cap Area) ---
    f_clks_mhz = np.array([2.0, 5.0, 10.0, 20.0, 40.0])
    fc_target = 198.94e3
    k_needed = f_clks_mhz * 1e6 / (2 * np.pi * fc_target)
    total_units = 1.0 + np.round(k_needed)
    f_alias_mhz = f_clks_mhz - 0.188

    ax2_r = ax2.twinx()
    ax2_r.spines["top"].set_visible(False)
    ax2_r.grid(False)

    l1 = ax2.plot(f_clks_mhz, f_alias_mhz, "-o", color=C["cobalt"], lw=2.1, ms=6.0,
                  label="Tần số ảnh Aliasing đầu tiên (MHz)")
    l2 = ax2_r.plot(f_clks_mhz, total_units, "--s", color=C["amber"], lw=2.0, ms=6.0,
                    label="Tổng số ô tụ đơn vị (1 + K) cần dùng")

    ax2.axvline(10.0, color=C["teal"], lw=1.4, ls=":")
    ax2.plot(10.0, 9.81, "o", color=C["teal"], ms=9.5, zorder=6)
    ax2.annotate(
        "ĐIỂM NGỌT f_clk = 10 MHz\n• OSR = 26.6 (Ảnh xa 9.81 MHz)\n• Gọn 9 ô MIM (450 µm²)\n• Bán chu kỳ 50 ns nhẹ tải OTA",
        xy=(10.0, 9.81),
        xytext=(16.5, 3.2),
        fontsize=7.6,
        fontweight="bold",
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.28", fc="#F0FDFA", ec=C["teal"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.2),
    )

    ax2.set_xlim(0, 43)
    ax2.set_ylim(0, 46)
    ax2_r.set_ylim(0, 54)
    ax2.set_xlabel("Tần số xung nhịp lấy mẫu f_clk (MHz)")
    ax2.set_ylabel("Tần số dải ảnh Aliasing (MHz)", color=C["cobalt"])
    ax2_r.set_ylabel("Số ô tụ đơn vị MIM (1 + K)", color=C["amber"])
    ax2.set_title("2. Đánh đổi Nyquist OSR vs. Diện tích tụ", fontsize=10.8)

    lines = l1 + l2
    labels = [ln.get_label() for ln in lines]
    ax2.legend(lines, labels, loc="upper left", fontsize=7.2, framealpha=0.96)

    fig.savefig(path)
    plt.close(fig)


def plot_ss_ota_noise_bridge(path: Path) -> None:
    """
    2-panel figure showing HOW Signals & Systems dictates:
      (Left) Absolute capacitor sizing C1=100 fF, C2=800 fF from kT/C SNR ceiling & parasitic error.
      (Right) OTA Phase Margin PM >= 60 deg from 2nd-order closed-loop step settling inside 50 ns.
    """
    apply_ieee_style()
    kB, T = 1.380649e-23, 300.0
    v_sig_rms = 0.40 / math.sqrt(2.0)

    fig, (ax1, ax2) = plt.subplots(
        1, 2, figsize=(10.8, 4.05), gridspec_kw={"wspace": 0.44}
    )

    # --- Left Panel: SNR_kT/C and Parasitic Ratio Error vs C1 (with C2 = 8*C1) ---
    c1_ff = np.logspace(1, 2.7, 300)
    c2_f = 8.0 * c1_ff * 1e-15
    vn_rms = np.sqrt(kB * T / c2_f)
    snr_db = 20 * np.log10(v_sig_rms / vn_rms)
    cp_err_pct = 100.0 * (1.5 / c1_ff)

    ax1_r = ax1.twinx()
    ax1_r.spines["top"].set_visible(False)
    ax1_r.grid(False)

    l1 = ax1.semilogx(c1_ff, snr_db, color=C["cobalt"], lw=2.1,
                      label="Trần SNR nhiễu nhiệt kT/C (dB, Vp=0.4V)")
    l2 = ax1_r.semilogx(c1_ff, cp_err_pct, "--", color=C["crimson"], lw=1.9,
                        label="Sai số do tụ ký sinh dây ~1.5 fF (%)")

    ax1.axhline(70.0, color=C["slate"], lw=0.9, ls=":")
    ax1.axvline(100.0, color=C["teal"], lw=1.4, ls=":")
    snr_100 = float(20 * np.log10(v_sig_rms / math.sqrt(kB * T / 800e-15)))
    ax1.plot(100.0, snr_100, "o", color=C["teal"], ms=9.0, zorder=6)

    ax1.annotate(
        "CHỐT C₁=100 fF, C₂=800 fF\n• SNR_kT/C = 71.9 dB (~11.6 bit)\n• Tụ ký sinh < 1.5% C₁\n• Tải OTA nhẹ (≤ 1 pF)",
        xy=(100.0, snr_100),
        xytext=(255.0, 61.2),
        ha="center",
        fontsize=7.3,
        fontweight="bold",
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.26", fc="#F0FDFA", ec=C["teal"], lw=1.0),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.2),
    )

    ax1.set_xlim(10, 750)
    ax1.set_ylim(56, 83)
    ax1_r.set_ylim(0, 18)
    ax1.set_xlabel("Tụ lấy mẫu C₁ (fF) — với C₂ = 8·C₁")
    ax1.set_ylabel("Trần SNR nhiễu nhiệt (dB)", color=C["cobalt"])
    ax1_r.set_ylabel("Tỷ lệ ký sinh Cp / C₁ (%)", color=C["crimson"])
    ax1.set_title("1. Phổ nhiễu kT/C quyết định cỡ tụ tuyệt đối", fontsize=10.8)

    lines = l1 + l2
    ax1.legend(lines, [ln.get_label() for ln in lines], loc="upper left", fontsize=7.2, framealpha=0.96)

    # --- Right Panel: 2nd-Order Closed-Loop Step Response vs Phase Margin ---
    t_ns = np.linspace(0, 50, 500)
    t_s = t_ns * 1e-9
    gbw_demo = 20e6
    wu = 2 * np.pi * gbw_demo

    cases = [
        (32, C["crimson"], "--", "PM = 32° (Rung mạnh, vọt lố 38%)"),
        (45, C["amber"], "-.", "PM = 45° (Vọt lố 23%, chậm êm)"),
        (60, C["teal"], "-", "PM = 60° (Chuẩn thiết kế: êm tại 47 ns)"),
        (76, C["cobalt"], "-", "PM = 76° (Tắt dần quá tới hạn, 0% rung)"),
    ]

    for pm_deg, col, ls, lbl in cases:
        zs = np.linspace(0.15, 1.2, 4000)
        pms = np.degrees(np.arctan(2 * zs / np.sqrt(np.sqrt(1 + 4 * zs**4) - 2 * zs**2)))
        zeta = float(zs[np.argmin(np.abs(pms - pm_deg))])
        wp2 = (2 * zeta) ** 2 * wu
        wn = math.sqrt(wu * wp2)
        if zeta < 1.0:
            wd = wn * math.sqrt(1.0 - zeta**2)
            phi = math.acos(zeta)
            y = 1.0 - (np.exp(-zeta * wn * t_s) / math.sqrt(1.0 - zeta**2)) * np.sin(wd * t_s + phi)
        else:
            r1 = -wn * (zeta - math.sqrt(zeta**2 - 1.0))
            r2 = -wn * (zeta + math.sqrt(zeta**2 - 1.0))
            y = 1.0 - (r2 * np.exp(r1 * t_s) - r1 * np.exp(r2 * t_s)) / (r2 - r1)
        lw = 2.3 if pm_deg == 60 else 1.5
        ax2.plot(t_ns, y, color=col, ls=ls, lw=lw, label=lbl)

    ax2.axhline(1.0, color=C["slate"], lw=0.8, ls=":")
    ax2.axvline(47.0, color=C["navy"], lw=1.1, ls=":")
    ax2.text(46.0, 0.16, "Cuối pha Φ₂\n(47 ns)", ha="right", fontsize=7.6,
             fontweight="bold", color=C["navy"])

    ax2.set_xlim(0, 50)
    ax2.set_ylim(0, 1.78)
    ax2.set_yticks([0.0, 0.4, 0.8, 1.0, 1.4])
    ax2.set_xlabel("Thời gian trong bán chu kỳ xung nhịp (ns)")
    ax2.set_ylabel("Đáp ứng bước nhảy chuẩn hóa V_out(t)")
    ax2.set_title("2. Đáp ứng bậc 2 vòng kín lý giải PM ≥ 60°", fontsize=10.8)
    ax2.legend(loc="upper right", fontsize=7.1, framealpha=0.96)

    fig.savefig(path)
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    data = json.loads(NUMBERS_PATH.read_text(encoding="utf-8"))
    plot_io_expected(data["spec"], FIG_DIR / "week1_io_expected.png")
    plot_pvt_enhanced(data["pvt_rc_vs_sc"], FIG_DIR / "week1_rc_vs_sc_pvt.png")
    plot_ss_spec_window(FIG_DIR / "week1_ss_spec_window.png")
    plot_ss_ota_noise_bridge(FIG_DIR / "week1_ss_ota_noise_bridge.png")
    print("[OK] Generated all 4 Week 1 storytelling figures in slides/figs/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
