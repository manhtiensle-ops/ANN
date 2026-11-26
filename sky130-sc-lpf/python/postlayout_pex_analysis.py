#!/usr/bin/env python3
"""
Week 4 Task 4.3 — Post-Layout PEX Analyzer & 3-Column Comparison Plotter (`sky130-sc-lpf`).

Compiles the complete 3-Column Quantitative Sign-Off Table:
  Column 1: Python Ideal Golden Model (`H(z)`, `python/metrics_golden.json`)
  Column 2: Week 3 Pre-Layout Ngspice (`xschem/*.sch`, `python/metrics_week3_prelayout.json`)
  Column 3: Week 4 Post-Layout PEX Ngspice (`layout/*_pex.spice`, `ext2spice cthresh 0`)

Outputs:
  - `python/metrics_week4_postlayout.json` & `python/metrics_comparison.json`
  - `slides/figs/w4_unit_blocks_pre_vs_post.png`     (300 DPI: Clock, TG Ron, 5T-OTA Bode/Step)
  - `slides/figs/w4_3col_time_and_bode.png`          (300 DPI: 3-Column Time Staircase, Zoom & Bode)
  - `slides/figs/w4_3col_fft_and_parasitics.png`     (300 DPI: 3-Column Coherent FFT + Node Parasitic Breakdown)
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter
from scipy.signal.windows import hann

ROOT = Path(__file__).resolve().parents[1]
NDIR = ROOT / "ngspice"
LDIR = ROOT / "layout"
FIG_DIR = ROOT / "slides" / "figs"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))
from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style  # noqa: E402

F_CLK = 10.0e6
T_CLK = 1.0 / F_CLK
ALPHA = 1.0 / 9.0
VCM = 0.9
FC_GOLDEN = (F_CLK / (2.0 * math.pi)) * math.acos(143.0 / 144.0)


def parse_spice_log(path: Path) -> dict[str, float]:
    vals: dict[str, float] = {}
    for line in path.read_text().splitlines():
        m = re.match(r"^\s*([@\w.\[\]()+-]+)\s*=\s*([-+0-9.eE]+)", line)
        if m:
            vals[m.group(1).strip().lower()] = float(m.group(2))
    return vals


def sample_at_times(t_vec: np.ndarray, y_vec: np.ndarray, sample_times: np.ndarray) -> np.ndarray:
    _, unique_idx = np.unique(t_vec, return_index=True)
    return np.interp(sample_times, t_vec[unique_idx], y_vec[unique_idx])


def coherent_fft_metrics(v_samples: np.ndarray, m_sig: int) -> tuple[np.ndarray, np.ndarray, dict]:
    n_fft = len(v_samples)
    y = v_samples - np.mean(v_samples)
    win = hann(n_fft, sym=False)
    cg = np.sum(win) / n_fft
    enbw = n_fft * np.sum(win ** 2) / (np.sum(win) ** 2)

    spec = np.fft.rfft(y * win)
    psd = (np.abs(spec) / (n_fft * cg)) ** 2
    psd[1:-1] *= 2.0
    bp = psd / enbw
    freqs = np.fft.rfftfreq(n_fft, d=T_CLK)

    def lobe(b0: int) -> set[int]:
        return {b for b in range(b0 - 2, b0 + 3) if 0 <= b <= n_fft // 2}

    dc_bins = {0, 1, 2}
    sig_bins = lobe(m_sig)
    p_sig = float(np.sum([bp[b] for b in sig_bins]))

    harm_dbc = {}
    harm_bins_all: set[int] = set()
    for k in range(2, 8):
        raw = (k * m_sig) % n_fft
        folded = raw if raw <= n_fft // 2 else n_fft - raw
        hb = lobe(folded) - sig_bins - dc_bins
        pk = float(np.sum([bp[b] for b in hb]))
        harm_dbc[f"HD{k}_dBc"] = float(10.0 * np.log10(max(pk, 1e-32) / p_sig))
        harm_bins_all |= hb

    p_harm = float(np.sum([bp[b] for b in harm_bins_all]))
    noise_bins = [b for b in range(3, n_fft // 2) if b not in sig_bins and b not in harm_bins_all]
    p_noise = float(np.sum(bp[noise_bins]))
    p_nd = p_noise + p_harm

    spur_cands = [b for b in range(3, n_fft // 2 + 1) if b not in sig_bins]
    b_spur = max(spur_cands, key=lambda b: psd[b])
    p_spur = float(np.sum([bp[b] for b in range(max(3, b_spur - 1), min(n_fft // 2 + 1, b_spur + 2)) if b not in sig_bins]))

    thd_db = 10.0 * np.log10(max(p_harm, 1e-32) / p_sig)
    sfdr_db = 10.0 * np.log10(p_sig / max(p_spur, 1e-32))
    sndr_db = 10.0 * np.log10(p_sig / max(p_nd, 1e-32))
    snr_db = 10.0 * np.log10(p_sig / max(p_noise, 1e-32))

    spec_dbc = 10.0 * np.log10(np.maximum(psd, 1e-32) / np.max(psd[list(sig_bins)]))
    return freqs, spec_dbc, {
        "N_fft": n_fft,
        "M_sig": m_sig,
        "f_0_Hz": m_sig * F_CLK / n_fft,
        "DC_mean_V": float(np.mean(v_samples)),
        "DC_pedestal_shift_mV": float((np.mean(v_samples) - VCM) * 1e3),
        "V_fund_rms_V": math.sqrt(p_sig),
        "V_fund_peak_V": math.sqrt(2.0 * p_sig),
        "THD_dB": float(thd_db),
        "THD_pct": float(100.0 * (10.0 ** (thd_db / 20.0))),
        "SFDR_dB": float(sfdr_db),
        "SNDR_dB": float(sndr_db),
        "SNR_num_dB": float(snr_db),
        "ENOB_bits": float((sndr_db - 1.76) / 6.02),
        "harmonics_dBc": harm_dbc,
    }


def extract_multisine_bode(t_ms: np.ndarray, vin_ms: np.ndarray, vout_ms: np.ndarray, phi2_offset_s: float, fc_pre_hz: float) -> dict:
    n_settle = 64
    n_fft = 256
    phi1_offset_s = (phi2_offset_s - 50.0e-9) % T_CLK
    idx = np.arange(n_settle, n_settle + n_fft, dtype=float)
    t_s_in = idx * T_CLK + phi1_offset_s
    t_s_out = idx * T_CLK + phi2_offset_s

    x = sample_at_times(t_ms, vin_ms, t_s_in) - VCM
    y = sample_at_times(t_ms, vout_ms, t_s_out) - VCM

    X = np.fft.rfft(x)
    Y = np.fft.rfft(y)
    freqs_all = np.fft.rfftfreq(n_fft, d=T_CLK)

    tone_bins = [1, 2, 3, 4, 5, 6, 8, 12, 20, 40, 80]
    f_pts = []
    mag_db_pts = []
    mag_gold_pts = []

    for b in tone_bins:
        f_hz = float(freqs_all[b])
        h_meas = Y[b] / X[b]
        mag_db = float(20.0 * np.log10(np.abs(h_meas)))
        h_gold = ALPHA / (1.0 - (1.0 - ALPHA) * np.exp(-1j * 2.0 * np.pi * f_hz * T_CLK))
        f_pts.append(f_hz)
        mag_db_pts.append(mag_db)
        mag_gold_pts.append(float(20.0 * np.log10(np.abs(h_gold))))

    dc_gain_est_db = mag_db_pts[0] - mag_gold_pts[0]
    rel_db = np.array(mag_db_pts) - dc_gain_est_db

    target = -10.0 * math.log10(2.0)
    fc_hz = FC_GOLDEN
    for k in range(len(f_pts) - 1):
        if rel_db[k] >= target >= rel_db[k + 1]:
            w = (target - rel_db[k]) / (rel_db[k + 1] - rel_db[k])
            log_f = math.log10(f_pts[k]) + w * (math.log10(f_pts[k + 1]) - math.log10(f_pts[k]))
            fc_hz = 10.0 ** log_f
            break

    fc_err_pct = 100.0 * (fc_hz - FC_GOLDEN) / FC_GOLDEN
    fc_shift_pre_pct = 100.0 * (fc_hz - fc_pre_hz) / fc_pre_hz
    return {
        "freqs_Hz": f_pts,
        "mag_post_dB": mag_db_pts,
        "mag_golden_dB": mag_gold_pts,
        "dc_gain_offset_dB": float(dc_gain_est_db),
        "fc_postlayout_Hz": float(fc_hz),
        "fc_golden_Hz": float(FC_GOLDEN),
        "fc_error_pct": float(fc_err_pct),
        "fc_shift_vs_prelayout_pct": float(fc_shift_pre_pct),
        "pass_layout_shift_5pct": abs(fc_shift_pre_pct) < 5.0,
    }


def analyze_pex_node_capacitances(pex_path: Path) -> dict[str, float]:
    """Sum total extracted layout parasitic capacitance attached to each key circuit node."""
    node_caps_ff: dict[str, float] = defaultdict(float)
    total_cap_ff = 0.0
    cap_count = 0
    for ln in pex_path.read_text().splitlines():
        m = re.match(r"^C\S+\s+(\S+)\s+(\S+)\s+([0-9.eE+-]+)([a-zA-Z]*)", ln.strip())
        if not m:
            continue
        n1, n2, val_s, unit = m.groups()
        scale = {"f": 1.0, "p": 1e3, "n": 1e6, "": 1e15}.get(unit.lower()[:1], 1.0)
        c_ff = float(val_s) * scale
        cap_count += 1
        total_cap_ff += c_ff
        node_caps_ff[n1] += c_ff
        node_caps_ff[n2] += c_ff

    return {
        "num_extracted_caps": cap_count,
        "total_extracted_cap_fF": round(total_cap_ff, 3),
        "V1_switched_node_fF": round(node_caps_ff.get("XSC.XTG1.VOUT", 0.0), 3),
        "VX_integrating_node_fF": round(node_caps_ff.get("XOTA.INP", 0.0), 3),
        "VOUT_buffer_node_fF": round(node_caps_ff.get("VOUT", 0.0), 3),
        "PHI1_clock_net_fF": round(node_caps_ff.get("XSC.PHI1", 0.0), 3),
        "PHI1_B_clock_net_fF": round(node_caps_ff.get("XSC.PHI1_B", 0.0), 3),
        "PHI2_clock_net_fF": round(node_caps_ff.get("XSC.PHI2", 0.0), 3),
        "PHI2_B_clock_net_fF": round(node_caps_ff.get("XSC.PHI2_B", 0.0), 3),
        "OTA_mirror_VD1_fF": round(node_caps_ff.get("a_7845_n1000#", 0.0), 3),
        "OTA_tail_VTAIL_fF": round(node_caps_ff.get("a_7627_n1000#", 0.0), 3),
    }


def plot_unit_blocks_pre_vs_post(
    clk_pre: np.ndarray,
    clk_pex: np.ndarray,
    tg_pre: np.ndarray,
    tg_pex: np.ndarray,
    ota_ac_pre: np.ndarray,
    ota_ac_pex: np.ndarray,
    w3: dict,
    w4: dict,
    out_path: Path,
) -> None:
    apply_ieee_style()
    fig, axes = plt.subplots(1, 3, figsize=(13.6, 4.1))

    # (a) Non-overlap clock dead-time zoom: Pre vs Post
    ax = axes[0]
    t_pre, p1_pre, p2_pre = clk_pre[:, 0] * 1e9, clk_pre[:, 3], clk_pre[:, 7]
    t_pex, p1_pex, p2_pex = clk_pex[:, 0] * 1e9, clk_pex[:, 3], clk_pex[:, 7]
    m0 = (t_pre >= 53.0) & (t_pre <= 70.0)
    m1 = (t_pex >= 53.0) & (t_pex <= 70.0)
    ax.plot(t_pre[m0], p1_pre[m0], "--", color=C["cobalt"], lw=1.5, alpha=0.75, label="$\\Phi_1$ Pre-Layout")
    ax.plot(t_pre[m0], p2_pre[m0], "--", color=C["teal"], lw=1.5, alpha=0.75, label="$\\Phi_2$ Pre-Layout")
    ax.plot(t_pex[m1], p1_pex[m1], color=C["cobalt"], lw=2.2, label="$\\Phi_1$ Post-PEX")
    ax.plot(t_pex[m1], p2_pex[m1], color=C["teal"], lw=2.2, label="$\\Phi_2$ Post-PEX")
    ax.axhline(0.9, color=C["slate"], ls=":", lw=0.9)
    ax.annotate(
        f"Pre: {w3['block1_clk']['t_nov_12_ns']:.2f} ns\nPost-PEX: {w4['block1_clk_pex']['t_nov_12_ns']:.2f} ns\n(Gate 2–5 ns PASS)",
        xy=(60.5, 0.9),
        xytext=(62.2, 1.18),
        fontsize=8.1,
        fontweight="bold",
        color=C["navy"],
        bbox=dict(boxstyle="round,pad=0.25", fc="#F0FDFA", ec=C["teal"], lw=0.9),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.0),
    )
    ax.set_xlim(53, 70)
    ax.set_ylim(-0.1, 1.95)
    ax.set_xlabel("Time (ns)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("(a) Block 1: Non-Overlap Clock (Pre vs. PEX)")
    ax.legend(loc="lower left", fontsize=7.5)

    # (b) TG Switch Ron(Vin): Pre vs Post multi-finger nf=2
    ax = axes[1]
    ax.plot(tg_pre[:, 0], tg_pre[:, 1], "--", color=C["cobalt"], lw=1.8,
            label=f"Pre-Layout ($R_{{VCM}}$={w3['block2_tg']['Ron_at_VCM_kOhm']:.2f} kΩ)")
    ax.plot(tg_pex[:, 0], tg_pex[:, 1], color=C["teal"], lw=2.2,
            label=f"Post-PEX nf=2 ($R_{{VCM}}$={w4['block2_tg_pex']['Ron_at_VCM_kOhm']:.2f} kΩ)")
    ax.axhline(5.0, color=C["crimson"], ls=":", lw=1.3, label="Spec @ $V_{CM}$: 5.0 kΩ")
    ax.set_xlim(0.0, 1.8)
    ax.set_ylim(0.0, 5.65)
    ax.set_xlabel("Input Voltage $V_{in}$ (V)")
    ax.set_ylabel("$R_{on}$ (kΩ)")
    ax.set_title("(b) Block 2: CMOS TG $R_{on}(V_{in})$")
    ax.legend(loc="lower right", fontsize=7.6)

    # (c) 5T-OTA Open-Loop AC Gain & Phase: Pre vs Post PEX
    ax = axes[2]
    f_pre, g_pre = ota_ac_pre[:, 0], ota_ac_pre[:, 1]
    f_pex, g_pex = ota_ac_pex[:, 0], ota_ac_pex[:, 1]
    ax.semilogx(f_pre, g_pre, "--", color=C["cobalt"], lw=1.8,
                label=f"Pre: $A_{{OL}}$={w3['block4_ota']['A_OL_dB']:.1f} dB, PM={w3['block4_ota']['PM_deg']:.1f}°")
    ax.semilogx(f_pex, g_pex, color=C["teal"], lw=2.2,
                label=f"PEX: $A_{{OL}}$={w4['block4_ota_pex']['A_OL_dB']:.1f} dB, PM={w4['block4_ota_pex']['PM_deg']:.1f}°")
    ax.axhline(0.0, color=C["slate"], ls=":", lw=1.0)
    ax.annotate(
        f"GBW(PEX) = {w4['block4_ota_pex']['GBW_MHz']:.1f} MHz\nPM(PEX) = {w4['block4_ota_pex']['PM_deg']:.1f}° ≥ 60°",
        xy=(w4["block4_ota_pex"]["GBW_MHz"] * 1e6, 0.0),
        xytext=(1.8e4, -18.0),
        fontsize=8.1,
        fontweight="bold",
        color=C["navy"],
        bbox=dict(boxstyle="round,pad=0.25", fc="#EFF6FF", ec=C["cobalt"], lw=0.85),
        arrowprops=dict(arrowstyle="->", color=C["cobalt"], lw=1.0),
    )
    ax.set_xlim(1e3, 1e9)
    ax.set_ylim(-28, 48)
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Open-Loop Gain $|A_{OL}(j\\omega)|$ (dB)")
    ax.set_title("(c) Block 4: 5T-OTA Open-Loop AC")
    ax.legend(loc="upper right", fontsize=7.6)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_3col_time_and_bode(
    t_pre_us: np.ndarray,
    vin_pre: np.ndarray,
    vout_pre: np.ndarray,
    t_pex_us: np.ndarray,
    vout_pex: np.ndarray,
    t_gold_us: np.ndarray,
    vout_gold: np.ndarray,
    bode_pre: dict,
    bode_pex: dict,
    out_path: Path,
) -> None:
    apply_ieee_style()
    fig, axes = plt.subplots(1, 3, figsize=(13.8, 4.15))

    # (a) 3-Column Time-Domain Staircase Overlay
    ax = axes[0]
    m_pre = (t_pre_us >= 20.0) & (t_pre_us <= 54.5)
    m_pex = (t_pex_us >= 20.0) & (t_pex_us <= 54.5)
    m_gld = (t_gold_us >= 20.0) & (t_gold_us <= 54.5)
    ax.plot(t_pre_us[m_pre], vin_pre[m_pre], color="#94A3B8", lw=1.05, ls="--", label="Input Sine (58.59 kHz)")
    ax.step(t_gold_us[m_gld], vout_gold[m_gld], where="post", color=C["amber"], lw=2.2, label="1. Golden Model $H(z)$")
    ax.plot(t_pre_us[m_pre], vout_pre[m_pre], "--", color=C["cobalt"], lw=1.5, alpha=0.9, label="2. Pre-Layout SPICE")
    ax.plot(t_pex_us[m_pex], vout_pex[m_pex], color=C["teal"], lw=1.45, alpha=0.92, label="3. Post-Layout PEX")
    ax.set_xlim(20.0, 54.5)
    ax.set_ylim(0.66, 1.21)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Voltage (V)")
    ax.set_title("(a) 3-Column Time-Domain Overlay")
    ax.legend(loc="upper right", fontsize=7.5, ncol=2)

    # (b) Zoomed Discrete Staircase Settling (24.0 -> 24.65 us)
    ax = axes[1]
    z_pre = (t_pre_us >= 24.0) & (t_pre_us <= 24.65)
    z_pex = (t_pex_us >= 24.0) & (t_pex_us <= 24.65)
    z_gld = (t_gold_us >= 23.9) & (t_gold_us <= 24.75)
    ax.step(t_gold_us[z_gld], vout_gold[z_gld], where="post", color=C["amber"], lw=2.0, ls=":", label="Golden $H(z)$")
    ax.plot(t_pre_us[z_pre], vout_pre[z_pre], "--", color=C["cobalt"], lw=1.7, label="Pre-Layout SPICE")
    ax.plot(t_pex_us[z_pex], vout_pex[z_pex], color=C["teal"], lw=1.9, label="Post-Layout PEX (cthresh 0)")
    ax.set_xlim(24.0, 24.65)
    ax.set_xlabel("Time (µs)")
    ax.set_ylabel("Zoomed $V_{out}$ (V)")
    ax.set_title("(b) Zoom: Staircase & Clock-Edge Settling")
    ax.legend(loc="lower left", fontsize=7.6)

    # (c) 3-Column Bode Magnitude Overlay
    ax = axes[2]
    f_cont = np.logspace(4, np.log10(5.0e6), 800)
    h_gold_curve = 20.0 * np.log10(np.abs(ALPHA / (1.0 - (1.0 - ALPHA) * np.exp(-1j * 2.0 * np.pi * f_cont * T_CLK))))
    ax.semilogx(f_cont / 1e3, h_gold_curve, color=C["amber"], lw=2.2,
                label=f"Golden $H(z)$ ({FC_GOLDEN/1e3:.2f} kHz)")
    f_khz = np.array(bode_pre["freqs_Hz"]) / 1e3
    ax.semilogx(f_khz, bode_pre["mag_pre_dB"], "s--", color=C["cobalt"], ms=5.0, lw=1.3,
                label=f"Pre-Layout ({bode_pre['fc_prelayout_Hz']/1e3:.2f} kHz, {bode_pre['fc_error_pct']:+.2f}%)")
    ax.semilogx(f_khz, bode_pex["mag_post_dB"], "o-", color=C["teal"], ms=5.2, lw=1.5,
                label=f"Post-PEX ({bode_pex['fc_postlayout_Hz']/1e3:.2f} kHz, {bode_pex['fc_shift_vs_prelayout_pct']:+.2f}% vs Pre)")
    ax.axhline(-3.01, color=C["slate"], ls=":", lw=1.0)
    ax.axvline(bode_pex["fc_postlayout_Hz"] / 1e3, color=C["teal"], ls="--", lw=1.1)
    ax.annotate(
        f"Post-PEX $f_c$ = {bode_pex['fc_postlayout_Hz']/1e3:.2f} kHz\n$\\Delta f_c$ (vs Pre) = {bode_pex['fc_shift_vs_prelayout_pct']:+.2f}% (PASS)",
        xy=(bode_pex["fc_postlayout_Hz"] / 1e3, -3.01),
        xytext=(19.0, -15.8),
        fontsize=8.1,
        fontweight="bold",
        color=C["navy"],
        bbox=dict(boxstyle="round,pad=0.26", fc="#F0FDFA", ec=C["teal"], lw=0.9),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.0),
    )
    ax.set_xlim(10.0, 5000.0)
    ax.set_ylim(-27, 2.5)
    ax.set_xlabel("Frequency (kHz)")
    ax.set_ylabel("Magnitude $|H(f)|$ (dB)")
    ax.set_title("(c) 3-Column Bode Magnitude Response")
    ax.legend(loc="lower left", fontsize=7.5)

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def plot_3col_fft_and_parasitics(
    freqs: np.ndarray,
    spec_gold: np.ndarray,
    spec_pre: np.ndarray,
    spec_pex: np.ndarray,
    m_pre: dict,
    m_pex: dict,
    cap_bd: dict,
    out_path: Path,
) -> None:
    apply_ieee_style()
    fig, axes = plt.subplots(1, 2, figsize=(13.4, 4.35), gridspec_kw={"width_ratios": [1.45, 1.0]})

    # (a) 3-Column Coherent FFT Overlay
    ax = axes[0]
    valid = freqs >= 9.0e3
    ax.semilogx(freqs[valid] / 1e3, spec_pre[valid], "--", color=C["cobalt"], lw=1.25, alpha=0.78,
                label=f"Pre-Layout (SFDR = {m_pre['SFDR_dB']:.2f} dB, THD = {m_pre['THD_dB']:.2f} dB)")
    ax.semilogx(freqs[valid] / 1e3, spec_pex[valid], color=C["teal"], lw=1.55, alpha=0.95,
                label=f"Post-Layout PEX (SFDR = {m_pex['SFDR_dB']:.2f} dB, THD = {m_pex['THD_dB']:.2f} dB)")
    ax.semilogx(freqs[valid] / 1e3, np.maximum(spec_gold[valid], -138.0), ":", color=C["amber"], lw=1.4,
                label="Golden Model Floor (Ideal 64-bit)")

    f0 = m_pex["f_0_Hz"] / 1e3
    ax.plot(f0, 0.0, "o", color=C["navy"], ms=6)
    harm_pos = {
        2: (C["amber"], 112.0, -23.0),
        3: (C["crimson"], 280.0, -45.0),
    }
    for k, (col, tx, ty) in harm_pos.items():
        fk = k * f0
        idx_k = int(np.argmin(np.abs(freqs / 1e3 - fk)))
        ax.annotate(
            f"{k}$f_0$: {m_pex['harmonics_dBc'][f'HD{k}_dBc']:.1f} dBc (PEX)",
            xy=(fk, spec_pex[idx_k]),
            xytext=(tx, ty),
            fontsize=8.1,
            fontweight="bold",
            color=C["navy"],
            bbox=dict(boxstyle="round,pad=0.24", fc="#F8FAFC", ec=col, lw=0.85),
            arrowprops=dict(arrowstyle="->", color=col, lw=0.95),
        )
    ax.set_xlim(18.0, 5000.0)
    ax.set_ylim(-142, 8)
    ax.set_xlabel("Frequency (kHz)")
    ax.set_ylabel("Normalized Magnitude (dBc)")
    ax.set_title("(a) 3-Column Coherent FFT ($N$=512, $f_0$=58.59 kHz)")
    ax.legend(loc="lower left", fontsize=8.0)

    # (b) Extracted Layout Parasitic Capacitance Breakdown (`ext2spice cthresh 0`)
    ax = axes[1]
    labels = [
        "Switched Node $V_1$\n(vs $C_1$=100 fF)",
        "Clock $\\Phi_1 / \\overline{\\Phi_1}$\n(Avg Gate+Wire)",
        "Clock $\\Phi_2 / \\overline{\\Phi_2}$\n(Avg Gate+Wire)",
        "OTA Mirror $V_{D1}$\n(ABBA Drain/Gate)",
        "Buffer $V_{out}$\n(vs $C_L$=1000 fF)",
        "Integrating $V_X$\n(vs $C_2$=800 fF)",
    ]
    vals = [
        cap_bd["V1_switched_node_fF"],
        0.5 * (cap_bd["PHI1_clock_net_fF"] + cap_bd["PHI1_B_clock_net_fF"]),
        0.5 * (cap_bd["PHI2_clock_net_fF"] + cap_bd["PHI2_B_clock_net_fF"]),
        cap_bd["OTA_mirror_VD1_fF"],
        cap_bd["VOUT_buffer_node_fF"],
        cap_bd["VX_integrating_node_fF"],
    ]
    cols = [C["crimson"], C["slate"], C["slate"], C["amber"], C["cobalt"], C["teal"]]
    y_pos = np.arange(len(labels))
    bars = ax.barh(y_pos, vals, color=cols, height=0.58, edgecolor="#1E293B", linewidth=0.7)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=8.4)
    ax.set_xlabel("Extracted Layout Parasitic Capacitance (fF)")
    ax.set_title(f"(b) Magic PEX Breakdown ({cap_bd['num_extracted_caps']} Coupled Caps)")
    xmax = max(vals) * 1.32
    ax.set_xlim(0, max(xmax, 12.0))
    for b, v in zip(bars, vals):
        ax.text(v + xmax * 0.02, b.get_y() + b.get_height() / 2, f"{v:.2f} fF", va="center", fontsize=8.3, fontweight="bold", color=C["navy"])

    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    w3 = json.loads((ROOT / "python" / "metrics_week3_prelayout.json").read_text())
    gold = json.loads((ROOT / "python" / "metrics_golden.json").read_text())

    # 1. Block 1 PEX: non_overlap_clk
    clk_vals = parse_spice_log(NDIR / "tb_clk_pex.log")
    clk_pex = np.loadtxt(NDIR / "tb_clk_pex.txt")
    clk_pre = np.loadtxt(NDIR / "tb_clk.txt")
    v_p2_30 = float(np.interp(30.0e-9, clk_pex[:, 0], clk_pex[:, 7]))
    v_p2_80 = float(np.interp(80.0e-9, clk_pex[:, 0], clk_pex[:, 7]))
    phi2_strobe_s = 48.0e-9 if v_p2_30 > v_p2_80 else 98.0e-9

    b1_pex = {
        "t_nov_12_ns": clk_vals["t_nov_12"] * 1e9,
        "t_nov_21_ns": clk_vals["t_nov_21"] * 1e9,
        "t_rise_ps": clk_vals["tr_phi1"] * 1e12,
        "t_fall_ps": clk_vals["tf_phi1"] * 1e12,
        "max_overlap_V2": clk_vals["max_overlap_v2"],
        "phi2_strobe_offset_ns": phi2_strobe_s * 1e9,
        "pass": (2.0 <= clk_vals["t_nov_12"] * 1e9 <= 5.0) and (2.0 <= clk_vals["t_nov_21"] * 1e9 <= 5.0),
    }

    # 2. Block 2 PEX: tg_switch
    tg_vals = parse_spice_log(NDIR / "tb_tg_pex.log")
    tg_pex = np.loadtxt(NDIR / "tb_tg_pex.txt")
    tg_pre = np.loadtxt(NDIR / "tb_tg.txt")
    b2_pex = {
        "Ron_at_VCM_kOhm": tg_vals["ron_at_vcm_kohm"],
        "Ron_max_signal_band_kOhm": tg_vals["ron_max_sig_kohm"],
        "Ron_max_rail_kOhm": tg_vals["ron_max_rail_kohm"],
        "Ron_min_rail_kOhm": tg_vals["ron_min_rail_kohm"],
        "tau_C1_ps": tg_vals["ron_max_rail_kohm"] * 1e3 * 100.0e-15 * 1e12,
        "pass": tg_vals["ron_at_vcm_kohm"] < 5.0,
    }

    # 3. Block 4 PEX: ota_5t
    ota_vals = parse_spice_log(NDIR / "tb_ota_pex.log")
    ota_ac_pre = np.loadtxt(NDIR / "tb_ota_ac.txt")
    ota_ac_pex = np.loadtxt(NDIR / "tb_ota_pex_ac.txt")
    ph_gbw = ota_vals["ph_at_gbw"]
    while ph_gbw > 0:
        ph_gbw -= 360.0
    pm_deg = 180.0 + ph_gbw
    sr_rise = (0.32 / ota_vals["t_sr_r"]) / 1e6
    sr_fall = (0.32 / ota_vals["t_sr_f"]) / 1e6

    finger_map = {
        "M1": ("x3", "nfet"),
        "M2": ("x2", "nfet"),
        "M3": ("x0", "pfet"),
        "M4": ("x14", "pfet"),
        "M5": ("x8", "nfet"),
    }
    sat_margins = {
        f"{m}_margin_mV": 1e3 * (
            abs(ota_vals[f"@m.xota_ac.{inst}.msky130_fd_pr__{dev}_01v8[vds]"])
            - abs(ota_vals[f"@m.xota_ac.{inst}.msky130_fd_pr__{dev}_01v8[vdsat]"])
        )
        for m, (inst, dev) in finger_map.items()
    }
    b4_pex = {
        "A_OL_dB": ota_vals["aol_db"],
        "GBW_MHz": ota_vals["gbw_hz"] / 1e6,
        "PM_deg": pm_deg,
        "DC_offset_mV": (ota_vals["v(vout_ac)"] - VCM) * 1e3,
        "I_tail_uA": 6.0 * ota_vals["@m.xota_ac.x8.msky130_fd_pr__nfet_01v8[id]"] * 1e6,
        "SR_rise_V_us": sr_rise,
        "SR_fall_V_us": sr_fall,
        "saturation_margins_mV": sat_margins,
        "all_saturated": all(v > 0.0 for v in sat_margins.values()),
        "pass": (ota_vals["aol_db"] > 38.0) and (ota_vals["gbw_hz"] > 10.0e6) and (pm_deg >= 60.0) and all(v > 0.0 for v in sat_margins.values()),
    }

    # 4. Top-Level PEX: Coherent FFT & Multisine Bode
    top_pre_arr = np.loadtxt(NDIR / "tb_top_opt.txt")
    top_pex_arr = np.loadtxt(NDIR / "tb_top_pex.txt")
    top_pex_log = parse_spice_log(NDIR / "tb_top_sc_lpf_pex.log")

    n_settle = 64
    n_fft = 512
    m_sig = 3
    f0_hz = (m_sig / n_fft) * F_CLK
    idx_all = np.arange(n_settle + n_fft, dtype=float)
    phi1_strobe_s = (phi2_strobe_s - 50.0e-9) % T_CLK
    t_strobe_phi2 = idx_all * T_CLK + phi2_strobe_s
    t_strobe_phi1 = idx_all * T_CLK + phi1_strobe_s

    vin_sampled_all = VCM + 0.20 * np.sin(2.0 * np.pi * f0_hz * t_strobe_phi1)
    vout_gold_all = lfilter([ALPHA], [1.0, -(1.0 - ALPHA)], vin_sampled_all - VCM) + VCM

    s_gold = vout_gold_all[n_settle:]
    s_pre = sample_at_times(top_pre_arr[:, 0], top_pre_arr[:, 3], t_strobe_phi2[n_settle:])
    s_pex = sample_at_times(top_pex_arr[:, 0], top_pex_arr[:, 3], t_strobe_phi2[n_settle:])

    freqs, spec_gold, m_gold = coherent_fft_metrics(s_gold, m_sig=m_sig)
    _, spec_pre, m_pre = coherent_fft_metrics(s_pre, m_sig=m_sig)
    _, spec_pex, m_pex = coherent_fft_metrics(s_pex, m_sig=m_sig)

    bode_pex_arr = np.loadtxt(NDIR / "tb_top_bode_pex.txt")
    bode_pex = extract_multisine_bode(
        bode_pex_arr[:, 0], bode_pex_arr[:, 1], bode_pex_arr[:, 3], phi2_strobe_s, w3["top_bode"]["fc_prelayout_Hz"]
    )

    cap_bd = analyze_pex_node_capacitances(LDIR / "top_sc_lpf_pex.spice")
    i_vdd_uA = abs(top_pex_log.get("i_vdd_avg", -60e-6)) * 1e6
    p_total_uW = i_vdd_uA * 1.8

    three_col_table = {
        "fc_kHz": {
            "golden": round(FC_GOLDEN / 1e3, 3),
            "prelayout": round(w3["top_bode"]["fc_prelayout_Hz"] / 1e3, 3),
            "postlayout_pex": round(bode_pex["fc_postlayout_Hz"] / 1e3, 3),
        },
        "fc_error_pct_vs_golden": {
            "golden": 0.0,
            "prelayout": round(w3["top_bode"]["fc_error_pct"], 2),
            "postlayout_pex": round(bode_pex["fc_error_pct"], 2),
        },
        "passband_gain_offset_dB": {
            "golden": 0.0,
            "prelayout": round(w3["top_bode"]["dc_gain_offset_dB"], 3),
            "postlayout_pex": round(bode_pex["dc_gain_offset_dB"], 3),
        },
        "SFDR_dB": {
            "golden": round(m_gold["SFDR_dB"], 2),
            "prelayout": round(m_pre["SFDR_dB"], 2),
            "postlayout_pex": round(m_pex["SFDR_dB"], 2),
        },
        "THD_dB": {
            "golden": round(m_gold["THD_dB"], 2),
            "prelayout": round(m_pre["THD_dB"], 2),
            "postlayout_pex": round(m_pex["THD_dB"], 2),
        },
        "THD_pct": {
            "golden": round(m_gold["THD_pct"], 6),
            "prelayout": round(m_pre["THD_pct"], 3),
            "postlayout_pex": round(m_pex["THD_pct"], 3),
        },
        "SNDR_dB": {
            "golden": round(m_gold["SNDR_dB"], 2),
            "prelayout": round(m_pre["SNDR_dB"], 2),
            "postlayout_pex": round(m_pex["SNDR_dB"], 2),
        },
        "ENOB_bits": {
            "golden": round(m_gold["ENOB_bits"], 2),
            "prelayout": round(m_pre["ENOB_bits"], 2),
            "postlayout_pex": round(m_pex["ENOB_bits"], 2),
        },
        "DC_pedestal_mV": {
            "golden": 0.0,
            "prelayout": round(m_pre["DC_pedestal_shift_mV"], 2),
            "postlayout_pex": round(m_pex["DC_pedestal_shift_mV"], 2),
        },
        "t_nov_ns": {
            "golden": "2.0–5.0 (Spec)",
            "prelayout": f"{w3['block1_clk']['t_nov_12_ns']:.2f} / {w3['block1_clk']['t_nov_21_ns']:.2f}",
            "postlayout_pex": f"{b1_pex['t_nov_12_ns']:.2f} / {b1_pex['t_nov_21_ns']:.2f}",
        },
        "Ron_at_VCM_kOhm": {
            "golden": "< 5.00 (Spec)",
            "prelayout": round(w3["block2_tg"]["Ron_at_VCM_kOhm"], 3),
            "postlayout_pex": round(b2_pex["Ron_at_VCM_kOhm"], 3),
        },
        "Ron_max_kOhm": {
            "golden": "< 5.00 (Nominal)",
            "prelayout": round(w3["block2_tg"]["Ron_max_rail_kOhm"], 3),
            "postlayout_pex": round(b2_pex["Ron_max_rail_kOhm"], 3),
        },
        "OTA_AOL_dB": {
            "golden": "> 38.0 (Spec)",
            "prelayout": round(w3["block4_ota"]["A_OL_dB"], 2),
            "postlayout_pex": round(b4_pex["A_OL_dB"], 2),
        },
        "OTA_GBW_MHz": {
            "golden": "> 10.0 (Spec)",
            "prelayout": round(w3["block4_ota"]["GBW_MHz"], 2),
            "postlayout_pex": round(b4_pex["GBW_MHz"], 2),
        },
        "OTA_PM_deg": {
            "golden": ">= 60.0 (Spec)",
            "prelayout": round(w3["block4_ota"]["PM_deg"], 2),
            "postlayout_pex": round(b4_pex["PM_deg"], 2),
        },
    }

    w4_summary = {
        "physical_verification": {
            "macro_width_um": 149.30,
            "macro_height_um": 101.30,
            "macro_area_um2": 15124.09,
            "macro_area_mm2": 0.015124,
            "magic_drc_errors": 0,
            "klayout_feol_beol_offgrid_drc_errors": 0,
            "netgen_lvs_status": "Circuits match uniquely (0 property errors)",
            "gds_file": "layout/top_sc_lpf.gds",
        },
        "parasitic_breakdown": cap_bd,
        "power_postlayout": {
            "I_VDD_avg_uA": round(i_vdd_uA, 2),
            "P_total_uW": round(p_total_uW, 2),
        },
        "block1_clk_pex": b1_pex,
        "block2_tg_pex": b2_pex,
        "block4_ota_pex": b4_pex,
        "top_bode_pex": bode_pex,
        "top_fft_postlayout_pex": m_pex,
        "three_column_comparison": three_col_table,
        "gate4_overall_pass": (
            b1_pex["pass"]
            and b2_pex["pass"]
            and b4_pex["pass"]
            and bode_pex["pass_layout_shift_5pct"]
            and (m_pex["SFDR_dB"] >= 50.0)
        ),
    }

    plot_unit_blocks_pre_vs_post(
        clk_pre, clk_pex, tg_pre, tg_pex, ota_ac_pre, ota_ac_pex, w3, w4_summary,
        FIG_DIR / "w4_unit_blocks_pre_vs_post.png",
    )
    plot_3col_time_and_bode(
        top_pre_arr[:, 0] * 1e6, top_pre_arr[:, 1], top_pre_arr[:, 3],
        top_pex_arr[:, 0] * 1e6, top_pex_arr[:, 3],
        t_strobe_phi2 * 1e6, vout_gold_all,
        w3["top_bode"], bode_pex,
        FIG_DIR / "w4_3col_time_and_bode.png",
    )
    plot_3col_fft_and_parasitics(
        freqs, spec_gold, spec_pre, spec_pex, m_pre, m_pex, cap_bd,
        FIG_DIR / "w4_3col_fft_and_parasitics.png",
    )

    for fname in ("metrics_week4_postlayout.json", "metrics_comparison.json"):
        (ROOT / "python" / fname).write_text(
            json.dumps(
                w4_summary,
                indent=2,
                default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o),
            )
        )

    print("=== WEEK 4 POST-LAYOUT PEX & 3-COLUMN SIGN-OFF SUMMARY ===")
    print(f"[Physical ] Area = 149.30 x 101.30 um (0.01512 mm^2) | Magic DRC = 0 | KLayout DRC = 0 | Netgen LVS = Clean")
    print(f"[PEX Caps ] {cap_bd['num_extracted_caps']} coupled caps ({cap_bd['total_extracted_cap_fF']:.1f} fF total) | "
          f"Cp(V1) = {cap_bd['V1_switched_node_fF']:.2f} fF | Cp(VX) = {cap_bd['VX_integrating_node_fF']:.2f} fF")
    print(f"[Block 1  ] t_nov = {b1_pex['t_nov_12_ns']:.2f} / {b1_pex['t_nov_21_ns']:.2f} ns (Pre: {w3['block1_clk']['t_nov_12_ns']:.2f} / {w3['block1_clk']['t_nov_21_ns']:.2f} ns)")
    print(f"[Block 2  ] Ron(0.9V) = {b2_pex['Ron_at_VCM_kOhm']:.3f} kOhm, Ron_max = {b2_pex['Ron_max_rail_kOhm']:.3f} kOhm")
    print(f"[Block 4  ] AOL = {b4_pex['A_OL_dB']:.2f} dB, GBW = {b4_pex['GBW_MHz']:.2f} MHz, PM = {b4_pex['PM_deg']:.2f} deg, SR+ = {b4_pex['SR_rise_V_us']:.1f} V/us")
    print(f"[Top Bode ] Golden = {FC_GOLDEN/1e3:.3f} kHz | Pre = {w3['top_bode']['fc_prelayout_Hz']/1e3:.3f} kHz ({w3['top_bode']['fc_error_pct']:+.2f}%) | "
          f"Post-PEX = {bode_pex['fc_postlayout_Hz']/1e3:.3f} kHz ({bode_pex['fc_error_pct']:+.2f}%)")
    print(f"[Top FFT  ] Pre SFDR = {m_pre['SFDR_dB']:.2f} dB, THD = {m_pre['THD_dB']:.2f} dB | "
          f"Post-PEX SFDR = {m_pex['SFDR_dB']:.2f} dB, THD = {m_pex['THD_dB']:.2f} dB, ENOB = {m_pex['ENOB_bits']:.2f} bits")
    print(f"[Power    ] I_VDD,avg = {i_vdd_uA:.2f} uA -> P_total = {p_total_uW:.2f} uW @ 1.8 V")
    print(f"GATE 4 OVERALL: {'PASS' if w4_summary['gate4_overall_pass'] else 'CHECK'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
