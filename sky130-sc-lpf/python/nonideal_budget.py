#!/usr/bin/env python3
"""
Task 2.2 — Non-Ideal Error Budget & Transistor Specification Lock (sky130-sc-lpf).

Sweeps and quantifies three transistor-level non-idealities to lock Week 3 SPICE specs:
  1. CMOS Switch On-Resistance R_on sweep (300 Ohm -> 120 kOhm):
     - Static incomplete-settling charge error in t_on = 47 ns (50 ns - 3 ns dead-time).
     - Dynamic track-and-hold harmonic distortion (THD) when R_on(V) varies across a
       continuously slewing input sine wave (Razavi Ch. 12 nonlinear tracking lag).
     -> Proves R_on < 5 kOhm guarantees settling > 94 tau and track-mode THD < -74 dB.
  2. 5T-OTA Open-Loop Gain A_OL sweep (10 dB -> 70 dB):
     - Unity-gain buffer DC gain error 1/(1 + A_OL) and SC pole-shift sensitivity.
     -> Proves A_OL >= 40 dB (100 V/V) keeps DC gain drop < 0.086 dB (< 1%) and |Delta f_c| < 1%.
  3. Charge Injection & Clock Feedthrough vs. TG Switch Area (W_n * L):
     - Evaluates R_on,max vs. pedestal voltage error on V_out with and without W/2 dummy switch.
     -> Locks optimal TG sizing sweet spot W_n = 4 um, W_p = 12 um (L = 0.15 um).

Outputs:
  - python/nonideal_budget.json
  - slides/figs/week2_nonideal_budgets.png (300 DPI, 3-panel collision-free IEEE layout)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal.windows import hann

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "slides" / "figs"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))
from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style  # noqa: E402

F_CLK = 10.0e6
T_CLK = 1.0 / F_CLK
T_NOV = 3.0e-9
T_ON = 0.5 * T_CLK - T_NOV   # 47 ns active conduction window
C1 = 100.0e-15
C2 = 800.0e-15
ALPHA = C1 / (C1 + C2)
VCM = 0.9
VDD = 1.8

# Verified sky130A BSIM4 TT constants (from python/week1_numbers.json)
COX_N = 8.3246e-3   # F/m^2 (8.325 fF/um^2)
COX_P = 8.1633e-3   # F/m^2 (8.163 fF/um^2)
CGDO_N_PER_UM = 0.49263e-15 / 2.0   # 0.2463 fF/um
CGDO_P_PER_UM = 0.44414e-15 / 6.0   # 0.0740 fF/um
L_SW_UM = 0.15


def simulate_nonlinear_ron_thd(r_on_peak_ohm: float, n_fft: int = 4096, m_sig: int = 73) -> tuple[float, float]:
    """
    Simulate continuous-time Phase-1 tracking & Phase-2 charge sharing when R_on(V)
    exhibits the BSIM4-measured sky130A TG bell curve:
      R_on(V) = R_peak / (1 + 4.8 * ((V - 0.965) / 0.40)^2)
    With m_sig = 73 (f_in = 178.22 kHz near passband edge, A_in = 0.40 V), nonlinear
    RC tracking lag dV_track ~ -R_on(Vin)*C1*(dVin/dt) generates realistic HD2/HD3.
    """
    n_settle = 512
    n_total = n_settle + n_fft
    f_in = (m_sig / n_fft) * F_CLK
    w_in = 2.0 * math.pi * f_in
    a_in = 0.40

    def r_tg(v: float) -> float:
        return r_on_peak_ohm / (1.0 + 4.8 * (((v - 0.965) / 0.40) ** 2))

    n_sub = 24
    dt = T_ON / n_sub
    c_eq = (C1 * C2) / (C1 + C2)

    v_c1 = VCM
    v_c2 = VCM
    v_out = np.empty(n_total, dtype=np.float64)

    for n in range(n_total):
        t0 = n * T_CLK
        # Phase 1: TG1 tracks time-varying Vin(t) from t0 to t0 + T_ON
        for k in range(n_sub):
            t_mid = t0 + (k + 0.5) * dt
            v_src = VCM + a_in * math.sin(w_in * t_mid)
            v_mid = 0.5 * (v_src + v_c1)
            tau1 = r_tg(v_mid) * C1
            v_c1 = v_src + (v_c1 - v_src) * math.exp(-dt / tau1)

        # Phase 2: TG1 open, TG2 redistributes charge between C1 and C2
        v_eq = (C1 * v_c1 + C2 * v_c2) / (C1 + C2)
        for _ in range(n_sub):
            v_mid = 0.5 * (v_c1 + v_c2)
            tau2 = r_tg(v_mid) * c_eq
            decay = math.exp(-dt / tau2)
            v_c1 = v_eq + (v_c1 - v_eq) * decay
            v_c2 = v_eq + (v_c2 - v_eq) * decay
        v_out[n] = v_c2

    y = v_out[n_settle:]
    y = y - np.mean(y)
    win = hann(n_fft, sym=False)
    cg = np.sum(win) / n_fft
    enbw = n_fft * np.sum(win ** 2) / (np.sum(win) ** 2)
    spec = np.fft.rfft(y * win)
    psd = (np.abs(spec) / (n_fft * cg)) ** 2
    psd[1:-1] *= 2.0
    bp = psd / enbw

    p_sig = float(np.sum(bp[m_sig - 2:m_sig + 3]))
    p_harm = 0.0
    for k in range(2, 8):
        b0 = (k * m_sig) % n_fft
        if b0 > n_fft // 2:
            b0 = n_fft - b0
        p_harm += float(np.sum(bp[max(3, b0 - 2):min(n_fft // 2, b0 + 3)]))

    z_inv = np.exp(-1j * w_in * T_CLK)
    v_rms_ideal = (a_in / math.sqrt(2.0)) * abs(ALPHA / (1.0 - (1.0 - ALPHA) * z_inv))
    gain_err_pct = 100.0 * abs(math.sqrt(p_sig) - v_rms_ideal) / v_rms_ideal
    thd_db = 10.0 * math.log10(max(p_harm, 1e-32) / p_sig)
    return gain_err_pct, thd_db


def sweep_ron() -> dict:
    r_grid = np.logspace(2, 5.2, 60)
    static_err_pct = 100.0 * np.exp(-T_ON / (r_grid * C1))
    dyn_r_grid = np.array([300, 600, 1000, 1744, 2264, 3500, 5000, 8000, 12000, 20000, 35000, 60000, 100000], dtype=float)
    dyn_gain_err = []
    dyn_thd_db = []
    for r_pk in dyn_r_grid:
        ge, thd = simulate_nonlinear_ron_thd(r_pk)
        dyn_gain_err.append(ge)
        dyn_thd_db.append(thd)

    r_max_static_0p1pct = T_ON / (math.log(1000.0) * C1)
    _, thd_at_5k = simulate_nonlinear_ron_thd(5000.0)
    _, thd_at_2p26k = simulate_nonlinear_ron_thd(2263.5)

    return {
        "r_grid_ohm": r_grid.tolist(),
        "static_settling_err_pct": static_err_pct.tolist(),
        "dyn_r_peak_ohm": dyn_r_grid.tolist(),
        "dyn_gain_err_pct": dyn_gain_err,
        "dyn_thd_dB": dyn_thd_db,
        "f_test_near_fc_Hz": (73.0 / 4096.0) * F_CLK,
        "R_max_for_0p1pct_static_settling_ohm": r_max_static_0p1pct,
        "R_design_gate_ohm": 5000.0,
        "THD_at_5kOhm_peak_dB": thd_at_5k,
        "THD_at_TG_4_12_2p26kOhm_dB": thd_at_2p26k,
    }


def sweep_aol() -> dict:
    aol_db = np.linspace(10.0, 70.0, 121)
    aol_lin = 10.0 ** (aol_db / 20.0)

    buf_gain = aol_lin / (1.0 + aol_lin)
    buf_gain_err_pct = 100.0 * (1.0 - buf_gain)
    buf_gain_drop_db = -20.0 * np.log10(buf_gain)

    c_gs1 = 90.0e-15
    c_gd1 = 6.0e-15
    c_in_eff = c_gd1 + c_gs1 / (1.0 + aol_lin)
    alpha_buf = C1 / (C1 + C2 + c_in_eff)
    cos_buf = 1.0 - (alpha_buf ** 2) / (2.0 * (1.0 - alpha_buf))
    fc_buf = (F_CLK / (2.0 * math.pi)) * np.arccos(cos_buf)
    fc_ideal = (F_CLK / (2.0 * math.pi)) * math.acos(1.0 - (ALPHA ** 2) / (2.0 * (1.0 - ALPHA)))
    pole_shift_buf_pct = 100.0 * np.abs(fc_buf - fc_ideal) / fc_ideal

    denom_act = (C1 + C2) + (2.0 * C1 + C2) / aol_lin
    p_act = (C2 * (1.0 + 1.0 / aol_lin)) / denom_act
    cos_act = (1.0 + p_act ** 2 - ((1.0 - p_act) ** 2) * 2.0) / (2.0 * p_act)
    fc_act = (F_CLK / (2.0 * math.pi)) * np.arccos(np.clip(cos_act, -1.0, 1.0))
    pole_shift_act_pct = 100.0 * np.abs(fc_act - fc_ideal) / fc_ideal

    idx_35 = int(np.argmin(np.abs(aol_db - 35.0)))
    idx_40 = int(np.argmin(np.abs(aol_db - 40.0)))

    return {
        "aol_dB": aol_db.tolist(),
        "dc_gain_err_pct": buf_gain_err_pct.tolist(),
        "dc_gain_drop_dB": buf_gain_drop_db.tolist(),
        "pole_shift_buffer_pct": pole_shift_buf_pct.tolist(),
        "pole_shift_active_sc_pct": pole_shift_act_pct.tolist(),
        "at_35dB": {
            "A_OL_V_V": float(aol_lin[idx_35]),
            "dc_gain_err_pct": float(buf_gain_err_pct[idx_35]),
            "dc_gain_drop_dB": float(buf_gain_drop_db[idx_35]),
            "pole_shift_active_pct": float(pole_shift_act_pct[idx_35]),
        },
        "at_40dB": {
            "A_OL_V_V": float(aol_lin[idx_40]),
            "dc_gain_err_pct": float(buf_gain_err_pct[idx_40]),
            "dc_gain_drop_dB": float(buf_gain_drop_db[idx_40]),
            "pole_shift_active_pct": float(pole_shift_act_pct[idx_40]),
        },
    }


def sweep_charge_injection() -> dict:
    wn_um = np.linspace(0.8, 16.0, 61)
    wp_um = 3.0 * wn_um
    area_total_um2 = (wn_um + wp_um) * L_SW_UM
    r_on_peak_kohm = 2.2635 * (4.0 / wn_um)

    q_n_0p5 = (wn_um * 1e-6) * (L_SW_UM * 1e-6) * COX_N * 0.50
    q_p_1p3 = (wp_um * 1e-6) * (L_SW_UM * 1e-6) * COX_P * 0.46
    dv_c1_peak_mv = 1e3 * np.maximum(q_n_0p5, q_p_1p3) / (2.0 * C1)
    dv_out_peak_mv = 1e3 * np.maximum(q_n_0p5, q_p_1p3) / (2.0 * (C1 + C2))
    dv_out_with_dummy_mv = 0.20 * dv_out_peak_mv

    cov_n = wn_um * CGDO_N_PER_UM
    cov_p = wp_um * CGDO_P_PER_UM
    dv_cf_out_mv = 1e3 * VDD * np.abs(cov_n - cov_p) / (C1 + C2)

    idx_4 = int(np.argmin(np.abs(wn_um - 4.0)))
    return {
        "Wn_um": wn_um.tolist(),
        "Wp_um": wp_um.tolist(),
        "total_gate_area_um2": area_total_um2.tolist(),
        "Ron_peak_kOhm": r_on_peak_kohm.tolist(),
        "dV_CI_on_C1_mV": dv_c1_peak_mv.tolist(),
        "dV_CI_on_Vout_no_dummy_mV": dv_out_peak_mv.tolist(),
        "dV_CI_on_Vout_with_dummy_mV": dv_out_with_dummy_mv.tolist(),
        "dV_CF_net_on_Vout_mV": dv_cf_out_mv.tolist(),
        "sweet_spot_Wn4_Wp12": {
            "Wn_um": 4.0,
            "Wp_um": 12.0,
            "L_um": L_SW_UM,
            "total_gate_area_um2": float(area_total_um2[idx_4]),
            "Ron_peak_kOhm": float(r_on_peak_kohm[idx_4]),
            "dV_CI_on_C1_peak_mV": float(dv_c1_peak_mv[idx_4]),
            "dV_CI_on_Vout_no_dummy_mV": float(dv_out_peak_mv[idx_4]),
            "dV_CI_on_Vout_with_dummy_mV": float(dv_out_with_dummy_mv[idx_4]),
            "dV_CF_net_on_Vout_mV": float(dv_cf_out_mv[idx_4]),
        },
    }


def plot_budgets(ron_res: dict, aol_res: dict, ci_res: dict, path: Path) -> None:
    apply_ieee_style()
    fig, axes = plt.subplots(1, 3, figsize=(13.4, 4.2))

    # Panel 1: Ron Sweep vs. Track-Mode Nonlinear THD
    ax = axes[0]
    r_k = np.array(ron_res["dyn_r_peak_ohm"]) / 1e3
    thd = np.array(ron_res["dyn_thd_dB"])
    ax.semilogx(r_k, thd, "o-", color=C["cobalt"], lw=2.0, ms=4.5, label="Nonlinear $R_{on}(V)$ THD ($f_{in}$=178 kHz)")
    ax.axvline(5.0, color=C["crimson"], ls="--", lw=1.3, label="Gate Limit: $R_{on} < 5$ kΩ")
    ax.axvline(2.264, color=C["teal"], ls=":", lw=1.5, label="Chosen TG 4/12 (2.26 kΩ)")
    ax.axhline(-60.0, color=C["amber"], ls="-.", lw=1.0)
    ax.text(0.34, -57.5, "−60 dB THD ceiling", fontsize=8.3, color=C["amber"], fontweight="bold")
    ax.set_xlabel("Peak Switch $R_{on}$ (kΩ)")
    ax.set_ylabel("Track-and-Hold THD (dB)")
    ax.set_title("(a) $R_{on}$ vs. Nonlinear Tracking THD")
    ax.set_xlim(0.28, 115.0)
    ax.set_ylim(-102, -32)
    ax.legend(loc="lower right", fontsize=7.9)

    # Panel 2: 5T-OTA A_OL Sweep
    ax = axes[1]
    aol = np.array(aol_res["aol_dB"])
    ax.semilogy(aol, aol_res["dc_gain_err_pct"], color=C["cobalt"], lw=2.1, label="DC Gain Error $1/(1+A_{OL})$ (%)")
    ax.semilogy(aol, aol_res["pole_shift_active_sc_pct"], color=C["amber"], ls="--", lw=1.8, label="SC Pole Shift $|\\Delta f_c / f_c|$ (%)")
    ax.axvline(40.0, color=C["teal"], ls="--", lw=1.4, label="Target Gate: $A_{OL} \\geq 40$ dB")
    ax.axhline(1.0, color=C["crimson"], ls=":", lw=1.0)
    ax.text(12.0, 1.22, "1.0% error ceiling", fontsize=8.3, color=C["crimson"], fontweight="bold")
    ax.set_xlabel("5T-OTA Open-Loop Gain $A_{OL}$ (dB)")
    ax.set_ylabel("Magnitude / Cutoff Error (%)")
    ax.set_title("(b) Finite $A_{OL}$ Error Budget")
    ax.set_xlim(10, 70)
    ax.set_ylim(0.02, 40)
    ax.legend(loc="upper right", fontsize=8.0)

    # Panel 3: Switch Width Trade-off (Collision-free annotations!)
    ax = axes[2]
    wn = np.array(ci_res["Wn_um"])
    l1 = ax.plot(wn, ci_res["Ron_peak_kOhm"], color=C["cobalt"], lw=2.0, label="Peak $R_{on}$ (kΩ, left)")
    ax.axhline(5.0, color=C["crimson"], ls=":", lw=1.0)
    ax.set_xlabel("NMOS Width $W_n$ (µm)  [$W_p = 3 W_n, L = 0.15$ µm]")
    ax.set_ylabel("Peak $R_{on}$ (kΩ)", color=C["cobalt"])
    ax.set_ylim(0, 15.5)
    ax.set_xlim(0.8, 16.0)

    ax_r = ax.twinx()
    ax_r.grid(False)
    ax_r.spines["top"].set_visible(False)
    l2 = ax_r.plot(wn, ci_res["dV_CI_on_Vout_no_dummy_mV"], color=C["amber"], lw=1.9, ls="--", label="$\\Delta V_{CI}$ on $V_{out}$ (no dummy)")
    l3 = ax_r.plot(wn, ci_res["dV_CI_on_Vout_with_dummy_mV"], color=C["teal"], lw=1.9, label="$\\Delta V_{CI}$ on $V_{out}$ (+ W/2 dummy)")
    ax_r.axvline(4.0, color=C["navy"], ls="-.", lw=1.2)
    ax_r.annotate(
        "Sweet Spot\n$W_n$=4, $W_p$=12 µm",
        xy=(4.0, 3.76),
        xytext=(6.6, 6.2),
        fontsize=8.2,
        color=C["navy"],
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.25", fc="#F8FAFC", ec=C["navy"], lw=0.8),
        arrowprops=dict(arrowstyle="->", color=C["navy"], lw=1.0),
    )
    ax_r.set_ylabel("Peak $\\Delta V_{CI}$ on $V_{out}$ (mV)", color=C["amber"])
    ax_r.set_ylim(0, 15.5)

    lines = l1 + l2 + l3
    labels = [ln.get_label() for ln in lines]
    ax.legend(lines, labels, loc="upper left", fontsize=7.8)
    ax.set_title("(c) TG Area Trade-off: $R_{on}$ vs. $\\Delta V_{CI}$")

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    ron_res = sweep_ron()
    aol_res = sweep_aol()
    ci_res = sweep_charge_injection()

    plot_budgets(ron_res, aol_res, ci_res, FIG_DIR / "week2_nonideal_budgets.png")

    payload = {
        "ron_budget": ron_res,
        "aol_budget": aol_res,
        "charge_injection_budget": ci_res,
        "locked_transistor_requirements": {
            "TG_Ron_max_ohm": 5000.0,
            "TG_recommended_Wn_um": 4.0,
            "TG_recommended_Wp_um": 12.0,
            "TG_recommended_L_um": 0.15,
            "OTA_AOL_min_dB": 40.0,
            "OTA_GBW_min_Hz": 10.0e6,
            "OTA_PM_min_deg": 60.0,
            "CLK_t_nov_range_ns": [2.0, 5.0],
        },
    }
    out = ROOT / "python" / "nonideal_budget.json"
    out.write_text(json.dumps(payload, indent=2))

    print("=== NON-IDEAL BUDGET SUMMARY ===")
    print(f"R_on static <0.1% limit = {ron_res['R_max_for_0p1pct_static_settling_ohm']/1e3:.1f} kOhm | "
          f"Track THD @ 5 kOhm = {ron_res['THD_at_5kOhm_peak_dB']:.1f} dB | Track THD @ TG 4/12 (2.26 kOhm) = {ron_res['THD_at_TG_4_12_2p26kOhm_dB']:.1f} dB")
    print(f"A_OL = 40 dB -> DC gain error = {aol_res['at_40dB']['dc_gain_err_pct']:.2f}% ({aol_res['at_40dB']['dc_gain_drop_dB']:.3f} dB), "
          f"active pole shift = {aol_res['at_40dB']['pole_shift_active_pct']:.2f}%")
    sw = ci_res["sweet_spot_Wn4_Wp12"]
    print(f"TG Sweet Spot 4/12 um -> Ron_peak = {sw['Ron_peak_kOhm']:.2f} kOhm, "
          f"dV_CI(Vout) = {sw['dV_CI_on_Vout_no_dummy_mV']:.2f} mV (no dummy) / {sw['dV_CI_on_Vout_with_dummy_mV']:.2f} mV (+W/2 dummy)")
    print(f"[OK] Saved {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
