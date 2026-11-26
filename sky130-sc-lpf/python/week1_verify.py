#!/usr/bin/env python3
"""
Week 1 verification script for sky130-sc-lpf.

Gate 1 evidence:
  (A) Automatic dimensional analysis of every Week-1 formula (SI base units).
  (B) Exact numeric values of the locked specs (Req, fc_RC, fc_SC, OSR, kT/C, ...).
  (C) sky130A BSIM4 / passive-device facts measured with ngspice (no guessing):
      Vth (with/without body effect), k' = uCox, TG Ron(Vin), resistor sheet
      values + PVT spread, MIM capacitance + PVT spread.

Outputs:
  python/week1_numbers.json
  slides/figs/week1_tg_ron.png     (300 DPI)
  slides/figs/week1_rc_vs_sc_pvt.png (300 DPI)

Run:  source env_sky130.sh && python3 python/week1_verify.py
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
LIB = "/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice"
FIG_DIR = ROOT / "slides" / "figs"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))

# ---------------------------------------------------------------------------
# (A) Minimal dimensional-analysis engine: exponents of (kg, m, s, A, K)
# ---------------------------------------------------------------------------
class Dim:
    __slots__ = ("e",)

    def __init__(self, kg=0, m=0, s=0, A=0, K=0):
        self.e = tuple(Fraction(x) for x in (kg, m, s, A, K))

    def __mul__(self, o):
        return Dim(*(a + b for a, b in zip(self.e, o.e)))

    def __truediv__(self, o):
        return Dim(*(a - b for a, b in zip(self.e, o.e)))

    def __pow__(self, p):
        return Dim(*(a * Fraction(p) for a in self.e))

    def __eq__(self, o):
        return self.e == o.e

    def __repr__(self):
        names = ("kg", "m", "s", "A", "K")
        parts = [f"{n}^{x}" if x != 1 else n for n, x in zip(names, self.e) if x != 0]
        return "·".join(parts) if parts else "1"


ONE = Dim()
SEC = Dim(s=1)
METER = Dim(m=1)
AMP = Dim(A=1)
KELVIN = Dim(K=1)
HZ = ONE / SEC
JOULE = Dim(kg=1, m=2, s=-2)
VOLT = JOULE / (AMP * SEC)
OHM = VOLT / AMP
FARAD = (AMP * SEC) / VOLT
SIEMENS = ONE / OHM
COULOMB = AMP * SEC
MOBILITY = METER**2 / (VOLT * SEC)          # m^2/(V s)
COX = FARAD / METER**2                      # F/m^2
KB = JOULE / KELVIN                         # Boltzmann constant


def dimension_checks() -> list[dict]:
    """Each entry: formula, derived dimension, expected dimension, pass flag."""
    checks = [
        ("R_eq = 1/(f_clk·C1)", ONE / (HZ * FARAD), OHM, "Ω"),
        ("τ = R·C", OHM * FARAD, SEC, "s"),
        ("f_c,RC = 1/(2π·R_eq·C2)", ONE / (OHM * FARAD), HZ, "Hz"),
        ("f_c,RC = f_clk·C1/(2π·C2)", HZ * FARAD / FARAD, HZ, "Hz"),
        ("α = C1/(C1+C2)", FARAD / FARAD, ONE, "1"),
        ("Q = C·V  (charge conservation)", FARAD * VOLT, COULOMB, "C"),
        ("ω_c·T_clk  (argument of cos)", HZ * SEC, ONE, "rad (1)"),
        ("OSR = f_clk/(2 f_c)", HZ / HZ, ONE, "1"),
        ("v_n² = k_B·T/C", KB * KELVIN / FARAD, VOLT**2, "V²"),
        ("I_D = ½·µCox·(W/L)·V_ov²", MOBILITY * COX * VOLT**2, AMP, "A"),
        ("g_m = µCox·(W/L)·V_ov", MOBILITY * COX * VOLT, SIEMENS, "S"),
        ("g_m = 2·I_D/V_ov", AMP / VOLT, SIEMENS, "S"),
        ("R_on = 1/[µCox·(W/L)·(V_GS−V_TH)]", ONE / (MOBILITY * COX * VOLT), OHM, "Ω"),
        ("r_o = 1/(λ·I_D)", ONE / ((ONE / VOLT) * AMP), OHM, "Ω"),
        ("A_OL = g_m·(r_o2 ∥ r_o4)", SIEMENS * OHM, ONE, "V/V"),
        ("GBW = g_m/(2π·C_L)", SIEMENS / FARAD, HZ, "Hz"),
        ("f_p2 = g_m3/(2π·C_X)", SIEMENS / FARAD, HZ, "Hz"),
        ("SR = I_tail/C_L", AMP / FARAD, VOLT / SEC, "V/s"),
        ("ΔV_CI = W·L·Cox·V_ov/(2·C_H)", METER**2 * COX * VOLT / FARAD, VOLT, "V"),
        ("ΔV_CF = V_clk·W·C_ov/(W·C_ov + C_H)", VOLT * (METER * (FARAD / METER)) / FARAD, VOLT, "V"),
        ("C_mim = C_A·(W+dw)·(L+dw)", (FARAD / METER**2) * METER * METER, FARAD, "F"),
        ("ε_settle = exp(−t/(R_on·C1))", SEC / (OHM * FARAD), ONE, "1 (exponent)"),
    ]
    out = []
    for name, got, exp, unit in checks:
        out.append({"formula": name, "derived_SI": repr(got), "expected": unit, "pass": got == exp})
    return out


# ---------------------------------------------------------------------------
# (B) Locked spec numbers
# ---------------------------------------------------------------------------
def spec_numbers() -> dict:
    f_clk = 10e6
    C1, C2 = 100e-15, 800e-15
    T = 300.0
    kB = 1.380649e-23
    alpha = C1 / (C1 + C2)
    R_eq = 1 / (f_clk * C1)
    fc_rc = 1 / (2 * math.pi * R_eq * C2)
    cos_wT = 1 - alpha**2 / (2 * (1 - alpha))
    fc_sc = f_clk / (2 * math.pi) * math.acos(cos_wT)
    # Exact discrete equivalent of a true RC (impulse invariance): pole e^{-T/(R C2)}
    p_rc = math.exp(-C1 / C2)
    p_sc = 1 - alpha
    # Backward-Euler mapping s=(1-z^-1)/T of 1/(1+s·τ), τ=T·C2/C1 -> pole C2/(C1+C2)
    p_be = (C2 / C1) / (1 + C2 / C1)
    return {
        "f_clk_Hz": f_clk,
        "T_clk_s": 1 / f_clk,
        "C1_F": C1,
        "C2_F": C2,
        "alpha": alpha,
        "alpha_fraction": "1/9",
        "R_eq_ohm": R_eq,
        "fc_RC_Hz": fc_rc,
        "cos_wcT": cos_wT,
        "cos_wcT_fraction": str(Fraction(1) - Fraction(1, 81) / (2 * Fraction(8, 9))),
        "fc_SC_Hz": fc_sc,
        "fc_SC_vs_RC_percent": 100 * (fc_sc - fc_rc) / fc_rc,
        "pole_SC": p_sc,
        "pole_RC_impulse_invariant": p_rc,
        "pole_backward_euler": p_be,
        "OSR_vs_fcSC": f_clk / (2 * fc_sc),
        "OSR_vs_fcRC": f_clk / (2 * fc_rc),
        "first_alias_band_Hz": f_clk - fc_sc,
        "H_at_alias_dB": None,  # filled below
        "kTC_C1_Vrms": math.sqrt(kB * T / C1),
        "kTC_C2_Vrms": math.sqrt(kB * T / C2),
        "T_K": T,
        "settle_tau_max_for_0p1pct_in_47ns_s": 47e-9 / math.log(1000),
        "Ron_max_for_0p1pct_in_47ns_ohm": 47e-9 / math.log(1000) / C1,
        "Ron_design_limit_ohm": 5e3,
        "settle_tau_at_5k_s": 5e3 * C1,
        "settle_n_tau_at_5k_in_47ns": 47e-9 / (5e3 * C1),
        "GBW_target_Hz": 10e6,
        "tau_OTA_at_GBW_s": 1 / (2 * math.pi * 10e6),
        "buffer_gain_error_40dB_percent": 100 * (1 - 100 / 101),
        "buffer_gain_error_35dB_percent": 100 * (1 - 10**(35 / 20) / (1 + 10**(35 / 20))),
    }


def h_mag_db(f, alpha, f_clk):
    z = np.exp(1j * 2 * np.pi * f / f_clk)
    return 20 * np.log10(np.abs(alpha / (1 - (1 - alpha) / z)))


# ---------------------------------------------------------------------------
# (C) ngspice characterization
# ---------------------------------------------------------------------------
NET_OP = """* week1 op characterization
.lib "{lib}" {corner}
.temp {temp}
Vdd vdd 0 1.8
Vcm vcm 0 0.9
Vg09 g09 0 0.9
Vgn85 gn85 0 0.85
Vgp12 gp12 0 0.6
Vs02 s02 0 0.2
Vd07 d07 0 0.7
Vr r 0 0.1

* --- NMOS Vth vs L, VGS=VDS=0.9 V, VSB=0
XN015 vcm g09 0 0 sky130_fd_pr__nfet_01v8 w=2 l=0.15
XN050 vcm g09 0 0 sky130_fd_pr__nfet_01v8 w=2 l=0.5
XN100 vcm g09 0 0 sky130_fd_pr__nfet_01v8 w=2 l=1
* --- NMOS as OTA input pair (VSB=0.2 V), L=0.5
XNIN d07 g09 s02 0 sky130_fd_pr__nfet_01v8 w=4 l=0.5
* --- NMOS as TG switch at Vin=VCM (VSB=0.9, VGS=0.9)
XNTG vcm vdd vcm 0 sky130_fd_pr__nfet_01v8 w=2 l=0.15
* --- PMOS Vth vs L, VSG=VSD=0.9 V, VBS=0
XP015 vcm g09 vdd vdd sky130_fd_pr__pfet_01v8 w=4 l=0.15
XP050 vcm g09 vdd vdd sky130_fd_pr__pfet_01v8 w=4 l=0.5
XP100 vcm g09 vdd vdd sky130_fd_pr__pfet_01v8 w=4 l=1
* --- PMOS as TG switch at Vin=VCM (VBS=0.9, VSG=0.9)
XPTG vcm 0 vcm vdd sky130_fd_pr__pfet_01v8 w=6 l=0.15
* --- k' extraction (long channel, saturation)
XNK vcm gn85 0 0 sky130_fd_pr__nfet_01v8 w=5 l=1
XPK 0 gp12 vdd vdd sky130_fd_pr__pfet_01v8 w=5 l=1
* --- Passive devices
XRH r 0 0 sky130_fd_pr__res_high_po w=0.35 l=35
Vrx r rx 0
XRX rx 0 0 sky130_fd_pr__res_xhigh_po w=0.35 l=35
Vrh0 r rh 0
XRH2 rh 0 0 sky130_fd_pr__res_high_po w=0.35 l=35
XC1 vcm 0 sky130_fd_pr__cap_mim_m3_1 w=4.85 l=9.85 mult=1
XC2 vcm 0 sky130_fd_pr__cap_mim_m3_1 w=4.85 l=9.85 mult=8
* --- Provisional 5T-OTA headroom probes (diode-connected, I_tail = 40 uA)
Ib1 vdd ngs 20u
XNVGS ngs ngs s02 0 sky130_fd_pr__nfet_01v8 w=10 l=0.5
Ib5 vdd nt 40u
XNT nt nt 0 0 sky130_fd_pr__nfet_01v8 w=10 l=1
Ip3 pd 0 20u
XP3 pd pd vdd vdd sky130_fd_pr__pfet_01v8 w=10 l=0.5

.control
op
{prints}
quit
.endc
.end
"""

NET_RON = """* week1 TG Ron sweep
.lib "{lib}" {corner}
.temp {temp}
Vdd vdd 0 1.8
Vin in 0 0
Vdn dn in 1m
Vdp dp in 1m
Vdt dt in 1m
XN dn vdd in 0 sky130_fd_pr__nfet_01v8 w={wn} l=0.15
XP dp 0 in vdd sky130_fd_pr__pfet_01v8 w={wp} l=0.15
XTN dt vdd in 0 sky130_fd_pr__nfet_01v8 w={wn} l=0.15
XTP dt 0 in vdd sky130_fd_pr__pfet_01v8 w={wp} l=0.15
.control
dc Vin 0 1.799 0.005
wrdata {out} i(Vdn) i(Vdp) i(Vdt)
quit
.endc
.end
"""


def mos(inst: str, kind: str, param: str) -> str:
    model = "nfet_01v8" if kind == "n" else "pfet_01v8"
    return f"@m.{inst}.msky130_fd_pr__{model}[{param}]"


OP_PROBES = {
    "vth_n_L0p15": mos("xn015", "n", "vth"),
    "vth_n_L0p5": mos("xn050", "n", "vth"),
    "vth_n_L1": mos("xn100", "n", "vth"),
    "vth_n_in_vsb0p2": mos("xnin", "n", "vth"),
    "vth_n_tg_vsb0p9": mos("xntg", "n", "vth"),
    "vth_p_L0p15": mos("xp015", "p", "vth"),
    "vth_p_L0p5": mos("xp050", "p", "vth"),
    "vth_p_L1": mos("xp100", "p", "vth"),
    "vth_p_tg_vbs0p9": mos("xptg", "p", "vth"),
    "id_nk": mos("xnk", "n", "id"),
    "vth_nk": mos("xnk", "n", "vth"),
    "id_pk": mos("xpk", "p", "id"),
    "vth_pk": mos("xpk", "p", "vth"),
    "cgdo_n": mos("xntg", "n", "cgdo"),
    "cgdo_p": mos("xptg", "p", "cgdo"),
    "i_res_high_po": "i(Vrh0)",
    "i_res_xhigh_po": "i(Vrx)",
    "c_unit": "@c.xc1.c1[capacitance]",
    "vgs_m1_20uA_W10L0p5_vsb0p2": mos("xnvgs", "n", "vgs"),
    "vth_m1_20uA_W10L0p5_vsb0p2": mos("xnvgs", "n", "vth"),
    "vdsat_m1": mos("xnvgs", "n", "vdsat"),
    "vgs_m5_40uA_W10L1": mos("xnt", "n", "vgs"),
    "vdsat_m5": mos("xnt", "n", "vdsat"),
    "vgs_m3_20uA_W10L0p5": mos("xp3", "p", "vgs"),
    "vth_m3": mos("xp3", "p", "vth"),
    "vdsat_m3": mos("xp3", "p", "vdsat"),
}


def run_ngspice(netlist: str, workdir: Path) -> str:
    (workdir / ".spiceinit").write_text("set ngbehavior=hsa\nset ng_nomodcheck\n")
    sp = workdir / "tb.spice"
    sp.write_text(netlist)
    r = subprocess.run(["ngspice", "-b", str(sp)], cwd=workdir, capture_output=True, text=True, timeout=600)
    return r.stdout + "\n" + r.stderr


def parse_prints(text: str) -> dict:
    vals = {}
    for line in text.splitlines():
        m = re.match(r"^\s*(\S+)\s*=\s*([-+0-9.eE]+)\s*$", line)
        if m:
            vals[m.group(1).lower()] = float(m.group(2))
    return vals


def op_characterize(corner: str, temp: float) -> dict:
    prints = "\n".join(f"print {p}" for p in OP_PROBES.values())
    net = NET_OP.format(lib=LIB, corner=corner, temp=temp, prints=prints)
    with tempfile.TemporaryDirectory() as d:
        out = run_ngspice(net, Path(d))
    raw = parse_prints(out)
    res = {}
    for key, probe in OP_PROBES.items():
        res[key] = raw.get(probe.lower())
    # Derived quantities
    vr = 0.1
    w, nsq = 0.35, 35 / 0.35
    if res["i_res_high_po"]:
        res["R_high_po_ohm"] = vr / abs(res["i_res_high_po"])
        res["Rs_high_po_ohm_sq"] = res["R_high_po_ohm"] / nsq
    if res["i_res_xhigh_po"]:
        res["R_xhigh_po_ohm"] = vr / abs(res["i_res_xhigh_po"])
        res["Rs_xhigh_po_ohm_sq"] = res["R_xhigh_po_ohm"] / nsq
    if res["id_nk"] and res["vth_nk"] is not None:
        vov = 0.85 - res["vth_nk"]
        res["vov_nk"] = vov
        res["kprime_n_A_V2"] = 2 * abs(res["id_nk"]) * 1 / (5 * vov**2)
    if res["id_pk"] and res["vth_pk"] is not None:
        vov = 1.2 - abs(res["vth_pk"])
        res["vov_pk"] = vov
        res["kprime_p_A_V2"] = 2 * abs(res["id_pk"]) * 1 / (5 * vov**2)
    if "missing" in out.lower() and not res["c_unit"]:
        res["_log_tail"] = out[-1500:]
    return res


def ron_sweep(wn: float, wp: float, corner: str = "tt", temp: float = 27) -> dict:
    with tempfile.TemporaryDirectory() as d:
        out_file = Path(d) / "ron.txt"
        run_ngspice(NET_RON.format(lib=LIB, wn=wn, wp=wp, out=out_file, corner=corner, temp=temp), Path(d))
        data = np.loadtxt(out_file)
    vin = data[:, 0]
    i_n, i_p, i_t = (np.abs(data[:, k]) for k in (1, 3, 5))
    eps = 1e-15
    return {
        "vin": vin,
        "ron_n": 1e-3 / np.maximum(i_n, eps),
        "ron_p": 1e-3 / np.maximum(i_p, eps),
        "ron_tg": 1e-3 / np.maximum(i_t, eps),
    }


def ron_summary(sw: dict, lo=0.5, hi=1.3) -> dict:
    v, r = sw["vin"], sw["ron_tg"]
    band = (v >= lo) & (v <= hi)
    full = (v >= 0.0) & (v <= 1.8)
    i_mid = int(np.argmin(np.abs(v - 0.9)))
    return {
        "Ron_tg_at_0p9_ohm": float(r[i_mid]),
        "Ron_n_at_0p9_ohm": float(sw["ron_n"][i_mid]),
        "Ron_p_at_0p9_ohm": float(sw["ron_p"][i_mid]),
        f"Ron_tg_max_{lo}_{hi}V_ohm": float(r[band].max()),
        f"Ron_tg_min_{lo}_{hi}V_ohm": float(r[band].min()),
        f"Vin_at_Ron_max_{lo}_{hi}V": float(v[band][np.argmax(r[band])]),
        "Ron_tg_max_full_rail_ohm": float(r[full].max()),
        "Vin_at_Ron_max_full_rail": float(v[full][np.argmax(r[full])]),
    }


# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
def plot_ron(sweeps: dict, path: Path):
    import matplotlib.pyplot as plt
    from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style

    apply_ieee_style()
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    (wn, wp), sw = list(sweeps.items())[0]
    ax.semilogy(sw["vin"], sw["ron_n"] / 1e3, color=C["cobalt"], lw=1.4, ls="--", label=f"NMOS only (W={wn} µm)")
    ax.semilogy(sw["vin"], sw["ron_p"] / 1e3, color=C["amber"], lw=1.4, ls="--", label=f"PMOS only (W={wp} µm)")
    styles = [C["teal"], C["navy"], C["crimson"]]
    for k, ((wn_, wp_), s) in enumerate(sweeps.items()):
        ax.semilogy(s["vin"], s["ron_tg"] / 1e3, color=styles[k % 3], lw=2.0, label=f"TG {wn_}/{wp_} µm")
    ax.axhline(5, color=C["crimson"], lw=1.0, ls=":")
    ax.text(0.03, 5.6, "Gate: R$_{on}$ < 5 kΩ", color=C["crimson"], fontsize=9)
    ax.axvspan(0.5, 1.3, color=C["cobalt"], alpha=0.06)
    ax.text(0.9, 0.13, "signal band 0.9 ± 0.4 V", ha="center", fontsize=8.5, color=C["slate"])
    ax.set_xlim(0, 1.8)
    ax.set_ylim(0.1, 200)
    ax.set_xlabel("V$_{in}$ (V)")
    ax.set_ylabel("R$_{on}$ (kΩ)")
    ax.set_title("sky130A TG on-resistance, L = 0.15 µm, tt / 27 °C")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), borderaxespad=0)
    fig.savefig(path)
    plt.close(fig)


def plot_pvt(pvt: dict, path: Path):
    import matplotlib.pyplot as plt
    from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style

    apply_ieee_style()
    labels = list(pvt.keys())
    rc = [pvt[k]["fc_RC_onchip_dev_pct"] for k in labels]
    sc = [pvt[k]["fc_SC_dev_pct"] for k in labels]
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.bar(x - 0.19, rc, 0.36, color=C["amber"], label="On-chip RC (xhigh_po R × MIM C)")
    ax.bar(x + 0.19, sc, 0.36, color=C["teal"], label="Switched-cap (f$_{clk}$·C$_1$/C$_2$)")
    for xi, v in zip(x, rc):
        ax.text(xi - 0.19, v + (1.2 if v >= 0 else -1.2), f"{v:+.1f}%", ha="center",
                va="bottom" if v >= 0 else "top", fontsize=8, color=C["amber"])
    ax.axhline(0, color="#334155", lw=0.8)
    ax.set_xticks(x, labels)
    ax.set_ylabel("Δf$_c$ vs. nominal (%)")
    ax.set_title("Cut-off drift across PVT: RC vs. switched-capacitor")
    lim = max(5, max(abs(v) for v in rc) * 1.35)
    ax.set_ylim(-lim, lim)
    ax.legend(loc="lower left", fontsize=8.5)
    fig.savefig(path)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    results = {}

    # (A)
    dims = dimension_checks()
    results["dimension_checks"] = dims
    n_ok = sum(d["pass"] for d in dims)
    print(f"[A] Dimensional analysis: {n_ok}/{len(dims)} formulas consistent")
    for d in dims:
        if not d["pass"]:
            print("    FAIL:", d)

    # (B)
    spec = spec_numbers()
    spec["H_at_alias_dB"] = float(h_mag_db(spec["f_clk_Hz"] - 50e3, spec["alpha"], spec["f_clk_Hz"]))
    spec["H_at_2MHz_dB"] = float(h_mag_db(2e6, spec["alpha"], spec["f_clk_Hz"]))
    spec["H_at_50kHz_dB"] = float(h_mag_db(50e3, spec["alpha"], spec["f_clk_Hz"]))
    spec["H_at_nyquist_dB"] = float(h_mag_db(5e6, spec["alpha"], spec["f_clk_Hz"]))
    results["spec"] = spec
    print(f"[B] fc_RC = {spec['fc_RC_Hz']/1e3:.3f} kHz, fc_SC = {spec['fc_SC_Hz']/1e3:.3f} kHz "
          f"({spec['fc_SC_vs_RC_percent']:+.2f} %), OSR = {spec['OSR_vs_fcSC']:.2f}")

    # (C1) nominal device characterization
    nominal = op_characterize("tt", 27)
    results["device_tt_27C"] = nominal
    print("[C1] tt/27C:", {k: (round(v, 5) if isinstance(v, float) else v) for k, v in nominal.items()})

    # (C2) PVT spread of on-chip RC vs SC ratio
    pvt_cases = [("tt", 27, "tt 27°C"), ("hh", 27, "hh 27°C"), ("ll", 27, "ll 27°C"),
                 ("tt", -40, "tt −40°C"), ("tt", 125, "tt 125°C"),
                 ("hh", 125, "hh 125°C"), ("ll", -40, "ll −40°C")]
    pvt = {}
    ref = None
    for corner, temp, label in pvt_cases:
        r = nominal if (corner, temp) == ("tt", 27) else op_characterize(corner, temp)
        R, Cu = r.get("R_xhigh_po_ohm"), r.get("c_unit")
        entry = {"corner": corner, "temp_C": temp, "R_xhigh_po_ohm": R, "C_unit_F": Cu,
                 "R_high_po_ohm": r.get("R_high_po_ohm")}
        if ref is None:
            ref = entry
        entry["fc_RC_onchip_dev_pct"] = 100 * ((ref["R_xhigh_po_ohm"] * ref["C_unit_F"]) / (R * Cu) - 1)
        # SC: fc ∝ f_clk * C1/C2 ; both are unit-cell multiples -> ratio is exactly 1:8 in the model
        entry["fc_SC_dev_pct"] = 0.0
        entry["C_unit_dev_pct"] = 100 * (Cu / ref["C_unit_F"] - 1)
        entry["R_dev_pct"] = 100 * (R / ref["R_xhigh_po_ohm"] - 1)
        pvt[label] = entry
        print(f"[C2] {label:10s} R_xhigh={R/1e3:8.2f} kΩ  C_unit={Cu*1e15:7.3f} fF  "
              f"ΔfcRC={entry['fc_RC_onchip_dev_pct']:+6.1f}%")
    results["pvt_rc_vs_sc"] = pvt

    # (C3) TG Ron sweeps
    sizes = [(2, 6), (4, 12), (8, 24)]
    sweeps = {s: ron_sweep(*s) for s in sizes}
    results["tg_ron"] = {f"Wn{s[0]}_Wp{s[1]}": ron_summary(sw) for s, sw in sweeps.items()}
    for k, v in results["tg_ron"].items():
        print(f"[C3] {k}: " + ", ".join(f"{a}={b:.0f}" if "ohm" in a else f"{a}={b:.3f}" for a, b in v.items()))

    # (C3b) TG Ron PVT risk for the recommended 4/12 baseline
    pvt_ron = {}
    for corner, temp in (("tt", 27), ("ss", -40), ("ss", 27), ("ss", 125), ("ff", 27), ("tt", 125), ("sf", 27), ("fs", 27)):
        sm = ron_summary(ron_sweep(4, 12, corner, temp))
        pvt_ron[f"{corner}_{temp}C"] = sm
        print(f"[C3b] TG 4/12 {corner:2s} {temp:4d}C: Ron@0.9={sm['Ron_tg_at_0p9_ohm']:.0f} Ω, "
              f"max(0.5-1.3V)={sm['Ron_tg_max_0.5_1.3V_ohm']:.0f} Ω")
    results["tg_ron_pvt_Wn4_Wp12"] = pvt_ron

    # (C3c) 5T-OTA input common-mode range estimate (provisional bias, measured VGS/Vdsat)
    n = nominal
    vin_min = n["vgs_m1_20uA_W10L0p5_vsb0p2"] + n["vdsat_m5"]
    vd1 = 1.8 - abs(n["vgs_m3_20uA_W10L0p5"])
    vin_max = vd1 + n["vth_m1_20uA_W10L0p5_vsb0p2"]
    results["ota_icmr_estimate"] = {
        "assumptions": "I_tail=40uA, M1/M2 W/L=10/0.5, M3/M4 W/L=10/0.5, M5 W/L=10/1 (provisional, Week 2 will size)",
        "VGS1_V": n["vgs_m1_20uA_W10L0p5_vsb0p2"], "Vdsat5_V": n["vdsat_m5"],
        "VSG3_V": abs(n["vgs_m3_20uA_W10L0p5"]), "VD1_V": vd1,
        "Vin_cm_min_V": vin_min, "Vin_cm_max_V": vin_max,
        "max_symmetric_swing_about_0p9_V": max(0.0, min(0.9 - vin_min, vin_max - 0.9)),
    }
    print("[C3c] ICMR estimate:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in results["ota_icmr_estimate"].items()})

    # (C4) Charge injection & clock feedthrough first-order estimates (TG 2/6 at VCM)
    eps0, eps_ox = 8.854e-12, 3.9
    cox_n = eps0 * eps_ox / 4.148e-9
    cox_p = eps0 * eps_ox / 4.23e-9
    vthn_tg = nominal["vth_n_tg_vsb0p9"]
    vthp_tg = abs(nominal["vth_p_tg_vbs0p9"])
    vov_n = max(1.8 - 0.9 - vthn_tg, 0.0)
    vov_p = max(0.9 - vthp_tg, 0.0)
    qn = 2e-6 * 0.15e-6 * cox_n * vov_n
    qp = 6e-6 * 0.15e-6 * cox_p * vov_p
    ci = {
        "Cox_n_F_m2": cox_n, "Cox_p_F_m2": cox_p,
        "Vov_n_tg_at_VCM": vov_n, "Vov_p_tg_at_VCM": vov_p,
        "Qch_n_C": qn, "Qch_p_C": qp,
        "dV_CI_n_on_C1_V": qn / (2 * 100e-15),
        "dV_CI_p_on_C1_V": -qp / (2 * 100e-15),
        "dV_CI_net_on_C1_V": (qn - qp) / (2 * 100e-15),
    }
    for tag, wdt in (("n", 2e-6), ("p", 6e-6)):
        cgdo = nominal.get(f"cgdo_{tag}")
        if cgdo:
            cov = cgdo  # ngspice reports the instance overlap cap (already W-scaled) in F
            ci[f"Cov_{tag}_F"] = cov
            ci[f"dV_CF_{tag}_on_C1_V"] = 1.8 * cov / (cov + 100e-15)
    results["charge_injection_tg2_6"] = ci
    if "dV_CF_n_on_C1_V" in ci and "dV_CF_p_on_C1_V" in ci:
        ci["dV_CF_net_on_C1_V"] = ci["dV_CF_n_on_C1_V"] - ci["dV_CF_p_on_C1_V"]
    print("[C4]", {k: f"{v:.3e}" for k, v in ci.items()})

    # Figures
    plot_ron(sweeps, FIG_DIR / "week1_tg_ron.png")
    plot_pvt(pvt, FIG_DIR / "week1_rc_vs_sc_pvt.png")

    out = ROOT / "python" / "week1_numbers.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"[OK] wrote {out}")
    print(f"[OK] figures in {FIG_DIR}")
    gate = n_ok == len(dims)
    print("GATE-1 DIMENSIONAL CHECK:", "PASS" if gate else "FAIL")
    return 0 if gate else 1


if __name__ == "__main__":
    sys.exit(main())
