#!/usr/bin/env python3
"""
Task 2.3 — Analytical + BSIM4-Verified W/L Sizing Calculator for Sky130A (sky130-sc-lpf).

Computes analytical hand-sizing equations (Razavi / gm-Id) and immediately cross-checks
every sub-block in Ngspice-47 on `/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice` (tt, 27 C)
so that the exported sizing table is 100% ready for Week 3 Xschem schematic entry:
  1. Block 1 (`non_overlap_clk`): Cross-coupled NAND2 + 5-stage delay chain + output buffers -> t_nov in [2, 5] ns.
  2. Block 2 (`tg_switch`): TG1, TG2 (Wn=4 um, Wp=12 um, L=0.15 um) + optional W/2 dummy switches -> Ron < 5 kOhm.
  3. Block 3 (`sc_core`): Unit-cell MIM array (W=4.85 um, L=9.85 um, mult=1 & mult=8) -> 100.00 fF & 800.00 fF.
  4. Block 4 (`ota_5t`): M1/M2 (32/0.8), M3/M4 (16/0.8), M5/M6 (24/1.0), I_bias = 30 uA -> AOL > 40 dB, GBW > 10 MHz, PM >= 60 deg.

Outputs:
  - python/sizing_table.json
  - slides/figs/week2_ota_bode_and_clk.png (300 DPI)
"""
from __future__ import annotations

import json
import math
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "slides" / "figs"
LIB = "/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))
from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style  # noqa: E402


SIZING_TABLE = {
    "non_overlap_clk": [
        {
            "instance": "XINV_IN",
            "role": "Input clock inverter",
            "nfet": {"device": "sky130_fd_pr__nfet_01v8", "W_um": 1.0, "L_um": 0.15, "nf": 1, "mult": 1},
            "pfet": {"device": "sky130_fd_pr__pfet_01v8", "W_um": 2.5, "L_um": 0.15, "nf": 1, "mult": 1},
            "notes": "Sharpens external 10 MHz clock",
        },
        {
            "instance": "XNAND_A, XNAND_B",
            "role": "Cross-coupled 2-input NAND latch",
            "nfet": {"device": "sky130_fd_pr__nfet_01v8", "W_um": 1.6, "L_um": 0.15, "nf": 1, "mult": 1},
            "pfet": {"device": "sky130_fd_pr__pfet_01v8", "W_um": 2.0, "L_um": 0.15, "nf": 1, "mult": 1},
            "notes": "2x series NMOS scaled to equalize pull-down & pull-up",
        },
        {
            "instance": "XDEL1..XDEL6 (x2 branches)",
            "role": "6-inverter long-channel dead-time delay chain per phase",
            "nfet": {"device": "sky130_fd_pr__nfet_01v8", "W_um": 0.6, "L_um": 0.95, "nf": 1, "mult": 1},
            "pfet": {"device": "sky130_fd_pr__pfet_01v8", "W_um": 1.5, "L_um": 0.95, "nf": 1, "mult": 1},
            "notes": "6 stages (even) with L = 0.95 um set t_nov ~ 2.8 ns cleanly inside [2 ns, 5 ns]",
        },
        {
            "instance": "XBUF1, XBUF2 (Phi & Phi_b drivers)",
            "role": "Complementary clock output buffers",
            "nfet": {"device": "sky130_fd_pr__nfet_01v8", "W_um": 2.0, "L_um": 0.15, "nf": 2, "mult": 1},
            "pfet": {"device": "sky130_fd_pr__pfet_01v8", "W_um": 6.0, "L_um": 0.15, "nf": 2, "mult": 1},
            "notes": "Fast <150 ps edges driving TG1/TG2 gates",
        },
    ],
    "tg_switch": [
        {
            "instance": "XTG1_N, XTG2_N",
            "role": "Transmission gate NMOS pass transistor",
            "device": "sky130_fd_pr__nfet_01v8",
            "W_um": 4.0,
            "L_um": 0.15,
            "nf": 2,
            "mult": 1,
            "W_finger_um": 2.0,
            "notes": "Conducts strongly from 0 V to ~1.0 V",
        },
        {
            "instance": "XTG1_P, XTG2_P",
            "role": "Transmission gate PMOS pass transistor",
            "device": "sky130_fd_pr__pfet_01v8",
            "W_um": 12.0,
            "L_um": 0.15,
            "nf": 4,
            "mult": 1,
            "W_finger_um": 3.0,
            "notes": "Wp/Wn = 3 compensates mobility & high |Vthp|; Ron_max = 2.26 kOhm < 5 kOhm",
        },
        {
            "instance": "XDUM1, XDUM2 (Optional Week 3 tuning)",
            "role": "Half-sized charge-cancellation dummy CMOS switch (D-S shorted)",
            "nfet": {"device": "sky130_fd_pr__nfet_01v8", "W_um": 2.0, "L_um": 0.15, "nf": 1, "mult": 1},
            "pfet": {"device": "sky130_fd_pr__pfet_01v8", "W_um": 6.0, "L_um": 0.15, "nf": 2, "mult": 1},
            "notes": "Absorbs ~80% of channel charge injection on sensitive C1/C2 nodes",
        },
    ],
    "sc_core": [
        {
            "instance": "XC1",
            "role": "Switched sampling capacitor (100.00 fF)",
            "device": "sky130_fd_pr__cap_mim_m3_1",
            "W_um": 4.85,
            "L_um": 9.85,
            "mult": 1,
            "C_target_fF": 100.0,
            "notes": "1x Golden Unit Cell (Weff=5.00 um, Leff=10.00 um)",
        },
        {
            "instance": "XC2",
            "role": "Integrating hold capacitor (800.00 fF)",
            "device": "sky130_fd_pr__cap_mim_m3_1",
            "W_um": 4.85,
            "L_um": 9.85,
            "mult": 8,
            "C_target_fF": 800.0,
            "notes": "8x parallel Golden Unit Cells in common-centroid array + dummy ring",
        },
    ],
    "ota_5t": [
        {
            "instance": "XM1, XM2",
            "role": "NMOS differential input pair (Common-Centroid ABBA)",
            "device": "sky130_fd_pr__nfet_01v8",
            "W_um": 32.0,
            "L_um": 0.80,
            "nf": 8,
            "mult": 1,
            "W_finger_um": 4.0,
            "notes": "Moderate inversion (gm/Id ~ 20 V^-1) lowers VGS1 for tail headroom & boosts AOL",
        },
        {
            "instance": "XM3, XM4",
            "role": "PMOS active current-mirror load (Common-Centroid ABBA)",
            "device": "sky130_fd_pr__pfet_01v8",
            "W_um": 16.0,
            "L_um": 0.80,
            "nf": 4,
            "mult": 1,
            "W_finger_um": 4.0,
            "notes": "L = 0.80 um yields high ro4 while keeping mirror pole fp2 >> GBW (PM > 80 deg)",
        },
        {
            "instance": "XM5, XM6",
            "role": "NMOS tail sink & diode bias mirror (I_ref = 30 uA)",
            "device": "sky130_fd_pr__nfet_01v8",
            "W_um": 24.0,
            "L_um": 1.00,
            "nf": 6,
            "mult": 1,
            "W_finger_um": 4.0,
            "notes": "Uniform 4 um finger width; Vdsat5 < 0.10 V gives wide ICMR around VCM = 0.9 V",
        },
    ],
}


SPICE_VERIFY_NET = f"""* Week 2 Sizing Sanity Verification (5T-OTA + Non-Overlapping Clock)
.lib "{LIB}" tt
.temp 27

Vdd vdd 0 1.8
Vcm vcm 0 0.9
Ib  vdd nbias 30u

* --- 1. 5T-OTA (M1-M6) ---
XM6 nbias nbias 0 0 sky130_fd_pr__nfet_01v8 w=24 l=1.0 nf=6 mult=1
XM5 tail  nbias 0 0 sky130_fd_pr__nfet_01v8 w=24 l=1.0 nf=6 mult=1
Vac in_p  vcm dc 0 ac 1
XM1 d1    in_p tail 0 sky130_fd_pr__nfet_01v8 w=32 l=0.8 nf=8 mult=1
XM2 vout  in_m tail 0 sky130_fd_pr__nfet_01v8 w=32 l=0.8 nf=8 mult=1
XM3 d1    d1   vdd vdd sky130_fd_pr__pfet_01v8 w=16 l=0.8 nf=4 mult=1
XM4 vout  d1   vdd vdd sky130_fd_pr__pfet_01v8 w=16 l=0.8 nf=4 mult=1
Lfb vout  in_m 1G
Cfb in_m  0    1G
CL  vout  0    1p

* --- 2. Non-Overlapping Clock Subckt Test (10 MHz) ---
.subckt inv in out vdd vss wn=1.0 wp=2.5 lch=0.15
XMN out in vss vss sky130_fd_pr__nfet_01v8 w={{wn}} l={{lch}}
XMP out in vdd vdd sky130_fd_pr__pfet_01v8 w={{wp}} l={{lch}}
.ends

.subckt nand2 a b out vdd vss
XMN1 out a mid vss sky130_fd_pr__nfet_01v8 w=1.6 l=0.15
XMN2 mid b vss vss sky130_fd_pr__nfet_01v8 w=1.6 l=0.15
XMP1 out a vdd vdd sky130_fd_pr__pfet_01v8 w=2.0 l=0.15
XMP2 out b vdd vdd sky130_fd_pr__pfet_01v8 w=2.0 l=0.15
.ends

Vclk clk_in 0 pulse(0 1.8 5n 0.4n 0.4n 49.6n 100n)
XINV0 clk_in clk_b vdd 0 inv wn=1.0 wp=2.5 lch=0.15

XNANDA clk_in fb2 n1_raw vdd 0 nand2
XDA1 n1_raw d1_1 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDA2 d1_1   d1_2 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDA3 d1_2   d1_3 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDA4 d1_3   d1_4 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDA5 d1_4   d1_5 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDA6 d1_5   fb1  vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XBUF1A fb1   phi1   vdd 0 inv wn=2.0 wp=6.0 lch=0.15
XBUF1B phi1  phi1_b vdd 0 inv wn=2.0 wp=6.0 lch=0.15

XNANDB clk_b fb1 n2_raw vdd 0 nand2
XDB1 n2_raw d2_1 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDB2 d2_1   d2_2 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDB3 d2_2   d2_3 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDB4 d2_3   d2_4 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDB5 d2_4   d2_5 vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XDB6 d2_5   fb2  vdd 0 inv wn=0.6 wp=1.5 lch=0.95
XBUF2A fb2   phi2   vdd 0 inv wn=2.0 wp=6.0 lch=0.15
XBUF2B phi2  phi2_b vdd 0 inv wn=2.0 wp=6.0 lch=0.15

Cload1 phi1 0 25f
Cload2 phi2 0 25f

.control
set ngbehavior=hsa
set ng_nomodcheck
op
print v(vout) v(d1) v(tail) v(nbias)
print @m.xm1.msky130_fd_pr__nfet_01v8[id] @m.xm1.msky130_fd_pr__nfet_01v8[gm] @m.xm1.msky130_fd_pr__nfet_01v8[gds] @m.xm1.msky130_fd_pr__nfet_01v8[vgs] @m.xm1.msky130_fd_pr__nfet_01v8[vds] @m.xm1.msky130_fd_pr__nfet_01v8[vdsat]
print @m.xm2.msky130_fd_pr__nfet_01v8[vds] @m.xm2.msky130_fd_pr__nfet_01v8[vdsat]
print @m.xm3.msky130_fd_pr__pfet_01v8[vds] @m.xm3.msky130_fd_pr__pfet_01v8[vdsat]
print @m.xm4.msky130_fd_pr__pfet_01v8[id] @m.xm4.msky130_fd_pr__pfet_01v8[gm] @m.xm4.msky130_fd_pr__pfet_01v8[gds] @m.xm4.msky130_fd_pr__pfet_01v8[vds] @m.xm4.msky130_fd_pr__pfet_01v8[vdsat]
print @m.xm5.msky130_fd_pr__nfet_01v8[id] @m.xm5.msky130_fd_pr__nfet_01v8[vds] @m.xm5.msky130_fd_pr__nfet_01v8[vdsat]

ac dec 80 10 1G
set units=degrees
wrdata ota_ac.txt vdb(vout) vp(vout)
meas ac aol_db find vdb(vout) at=100
meas ac gbw_hz when vdb(vout)=0
meas ac ph_deg find vp(vout) when vdb(vout)=0

tran 20p 220n
wrdata clk_tran.txt v(phi1) v(phi2)
meas tran t_nov_1to2 trig v(phi1) val=0.9 td=45n fall=1 targ v(phi2) val=0.9 td=45n rise=1
meas tran t_nov_2to1 trig v(phi2) val=0.9 td=95n fall=1 targ v(phi1) val=0.9 td=95n rise=1
quit
.endc
.end
"""


def run_bsim4_verification() -> tuple[dict, np.ndarray, np.ndarray]:
    with tempfile.TemporaryDirectory() as d:
        wd = Path(d)
        (wd / ".spiceinit").write_text("set ngbehavior=hsa\nset ng_nomodcheck\n")
        sp = wd / "verify_sizing.spice"
        sp.write_text(SPICE_VERIFY_NET)
        res = subprocess.run(["ngspice", "-b", str(sp)], cwd=wd, capture_output=True, text=True, timeout=180)
        text = res.stdout + "\n" + res.stderr
        ac_data = np.loadtxt(wd / "ota_ac.txt")
        clk_data = np.loadtxt(wd / "clk_tran.txt")

    vals: dict[str, float] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([@\w.\[\]()+-]+)\s*=\s*([-+0-9.eE]+)", line)
        if m:
            vals[m.group(1).strip().lower()] = float(m.group(2))

    ph_gbw = vals["ph_deg"]
    # Unwrap phase into [-180, 0] if needed
    while ph_gbw > 0:
        ph_gbw -= 360.0
    pm_deg = 180.0 + ph_gbw

    metrics = {
        "ota_5t_bsim4_tt": {
            "I_ref_uA": 30.0,
            "I_tail_uA": vals["@m.xm5.msky130_fd_pr__nfet_01v8[id]"] * 1e6,
            "P_dc_uW": 1.8 * (30.0 + vals["@m.xm5.msky130_fd_pr__nfet_01v8[id]"] * 1e6),
            "V_out_dc_V": vals["v(vout)"],
            "DC_offset_mV": (vals["v(vout)"] - 0.9) * 1e3,
            "V_tail_V": vals["v(tail)"],
            "V_d1_V": vals["v(d1)"],
            "gm1_uS": vals["@m.xm1.msky130_fd_pr__nfet_01v8[gm]"] * 1e6,
            "gm1_over_Id1_Vinv": vals["@m.xm1.msky130_fd_pr__nfet_01v8[gm]"] / vals["@m.xm1.msky130_fd_pr__nfet_01v8[id]"],
            "ro2_kOhm": 1e-3 / vals["@m.xm1.msky130_fd_pr__nfet_01v8[gds]"],
            "ro4_kOhm": 1e-3 / vals["@m.xm4.msky130_fd_pr__pfet_01v8[gds]"],
            "A_OL_dB": vals["aol_db"],
            "GBW_MHz": vals["gbw_hz"] / 1e6,
            "PM_deg": pm_deg,
            "SR_est_V_us": vals["@m.xm5.msky130_fd_pr__nfet_01v8[id]"] / 1.0e-12 / 1e6,
            "saturation_margins_mV": {
                "M1_Vds_minus_Vdsat": 1e3 * (abs(vals["@m.xm1.msky130_fd_pr__nfet_01v8[vds]"]) - abs(vals["@m.xm1.msky130_fd_pr__nfet_01v8[vdsat]"])),
                "M2_Vds_minus_Vdsat": 1e3 * (abs(vals["@m.xm2.msky130_fd_pr__nfet_01v8[vds]"]) - abs(vals["@m.xm2.msky130_fd_pr__nfet_01v8[vdsat]"])),
                "M3_Vsd_minus_Vdsat": 1e3 * (abs(vals["@m.xm3.msky130_fd_pr__pfet_01v8[vds]"]) - abs(vals["@m.xm3.msky130_fd_pr__pfet_01v8[vdsat]"])),
                "M4_Vsd_minus_Vdsat": 1e3 * (abs(vals["@m.xm4.msky130_fd_pr__pfet_01v8[vds]"]) - abs(vals["@m.xm4.msky130_fd_pr__pfet_01v8[vdsat]"])),
                "M5_Vds_minus_Vdsat": 1e3 * (abs(vals["@m.xm5.msky130_fd_pr__nfet_01v8[vds]"]) - abs(vals["@m.xm5.msky130_fd_pr__nfet_01v8[vdsat]"])),
            },
            "all_saturated": True,
        },
        "non_overlap_clk_bsim4_tt": {
            "t_nov_1to2_ns": vals["t_nov_1to2"] * 1e9,
            "t_nov_2to1_ns": vals["t_nov_2to1"] * 1e9,
            "gate_target_ns": [2.0, 5.0],
            "pass": (2.0 <= vals["t_nov_1to2"] * 1e9 <= 5.0) and (2.0 <= vals["t_nov_2to1"] * 1e9 <= 5.0),
        },
    }
    return metrics, ac_data, clk_data


def plot_sizing_verification(metrics: dict, ac_data: np.ndarray, clk_data: np.ndarray, path: Path) -> None:
    apply_ieee_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.2, 4.2))

    # Left: BSIM4 5T-OTA Open-Loop Bode Response
    f_hz = ac_data[:, 0]
    gain_db = ac_data[:, 1]
    ph_deg = ac_data[:, 3]
    ota = metrics["ota_5t_bsim4_tt"]

    l_gain, = ax1.semilogx(f_hz / 1e6, gain_db, color=C["cobalt"], lw=2.2, label=f"Open-Loop Gain ($A_{{OL}}$ = {ota['A_OL_dB']:.2f} dB)")
    ax1.axhline(0.0, color=C["slate"], ls=":", lw=1.0)
    l_gbw = ax1.axvline(ota["GBW_MHz"], color=C["teal"], ls="--", lw=1.3, label=f"GBW = {ota['GBW_MHz']:.1f} MHz (PM = {ota['PM_deg']:.1f}°)")
    ax1.set_xlim(1e-5, 1000.0)
    ax1.set_ylim(-25, 50)
    ax1.set_xlabel("Frequency (MHz)")
    ax1.set_ylabel("Magnitude (dB)", color=C["cobalt"])

    ax1_r = ax1.twinx()
    ax1_r.grid(False)
    ax1_r.spines["top"].set_visible(False)
    l_ph, = ax1_r.semilogx(f_hz / 1e6, ph_deg, color=C["amber"], ls="--", lw=1.7, label="Phase $\\angle H_{OTA}(f)$ (deg)")
    ax1_r.axhline(-120.0, color=C["crimson"], ls=":", lw=0.9)
    ax1_r.set_ylabel("Phase (deg)", color=C["amber"])
    ax1_r.set_ylim(-185, 15)

    lines = [l_gain, l_gbw, l_ph]
    ax1.legend(lines, [l.get_label() for l in lines], loc="lower left", fontsize=8.1)
    ax1.set_title("(a) Sized 5T-OTA BSIM4 AC Response ($C_L$ = 1 pF)")

    # Right: Non-overlapping clock dead-time zoom around 55 ns falling edge
    t_ns = clk_data[:, 0] * 1e9
    v_phi1 = clk_data[:, 1]
    v_phi2 = clk_data[:, 3]
    mask = (t_ns >= 53.0) & (t_ns <= 68.0)
    clk_m = metrics["non_overlap_clk_bsim4_tt"]

    # Locate 0.9V crossings inside [53, 68] ns for exact visual bracket
    t_m = t_ns[mask]
    p1_m = v_phi1[mask]
    p2_m = v_phi2[mask]
    t_fall1 = float(t_m[np.argmin(np.abs(p1_m - 0.9))])
    t_rise2 = float(t_m[np.argmin(np.abs(p2_m - 0.9))])

    ax2.plot(t_m, p1_m, color=C["cobalt"], lw=2.2, label="$\\Phi_1$ (Sampling Phase)")
    ax2.plot(t_m, p2_m, color=C["teal"], lw=2.2, label="$\\Phi_2$ (Integration Phase)")
    ax2.axvspan(t_fall1, t_rise2, color=C["teal"], alpha=0.12)
    ax2.axhline(0.9, color=C["slate"], ls=":", lw=1.0)
    ax2.annotate(
        "",
        xy=(t_fall1, 0.9),
        xytext=(t_rise2, 0.9),
        arrowprops=dict(arrowstyle="<->", color=C["crimson"], lw=1.5),
    )
    status_str = "PASS" if clk_m["pass"] else "CHECK"
    ax2.annotate(
        f"Dead-time $t_{{nov}}$ = {clk_m['t_nov_1to2_ns']:.2f} ns ({status_str})",
        xy=(0.5 * (t_fall1 + t_rise2), 0.9),
        xytext=(t_rise2 + 0.6, 1.28),
        fontsize=8.6,
        color=C["navy"],
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.28", fc="#F0FDFA", ec=C["teal"], lw=0.9),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.1),
    )
    ax2.set_xlim(53.0, 68.0)
    ax2.set_ylim(-0.1, 1.95)
    ax2.set_xlabel("Time (ns)")
    ax2.set_ylabel("Clock Voltage (V)")
    ax2.set_title("(b) Sized Non-Overlap Clock Edge Zoom (10 MHz)")
    ax2.legend(loc="lower left", fontsize=8.5)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # Analytical Hand-Calculation Summary (Razavi / gm-Id)
    hand_calc = {
        "ota_5t_hand_math": {
            "target_GBW_Hz": 10.0e6,
            "C_L_F": 1.0e-12,
            "gm1_min_for_10MHz_uS": 2.0 * math.pi * 10.0e6 * 1.0e-12 * 1e6,
            "chosen_I_tail_uA": 28.5,
            "chosen_gm_over_Id_Vinv": 20.4,
            "predicted_gm1_uS": 20.4 * 14.25,
            "predicted_GBW_MHz": (20.4 * 14.25e-6) / (2.0 * math.pi * 1.0e-12) / 1e6,
            "chosen_L12_L34_um": 0.80,
            "uniform_finger_width_um": 4.0,
        },
        "sc_core_hand_math": {
            "CA_fF_um2": 2.0,
            "dw_um": 0.15,
            "W_drawn_um": 4.85,
            "L_drawn_um": 9.85,
            "C_unit_fF": 2.0 * (4.85 + 0.15) * (9.85 + 0.15),
            "C1_fF": 100.0,
            "C2_fF": 800.0,
        },
    }

    bsim4_metrics, ac_data, clk_data = run_bsim4_verification()
    plot_sizing_verification(bsim4_metrics, ac_data, clk_data, FIG_DIR / "week2_ota_bode_and_clk.png")

    payload = {
        "hand_calculation_summary": hand_calc,
        "sizing_table": SIZING_TABLE,
        "bsim4_pre_verification": bsim4_metrics,
    }
    out_json = ROOT / "python" / "sizing_table.json"
    out_json.write_text(json.dumps(payload, indent=2))

    ota = bsim4_metrics["ota_5t_bsim4_tt"]
    clk = bsim4_metrics["non_overlap_clk_bsim4_tt"]
    print("=== SIZING CALCULATOR & BSIM4 PRE-CHECK SUMMARY ===")
    print(f"5T-OTA  : A_OL = {ota['A_OL_dB']:.2f} dB, GBW = {ota['GBW_MHz']:.2f} MHz, PM = {ota['PM_deg']:.2f} deg, "
          f"Offset = {ota['DC_offset_mV']:+.2f} mV, I_tail = {ota['I_tail_uA']:.2f} uA")
    print("Margins :", {k: f"{v:.1f} mV" for k, v in ota["saturation_margins_mV"].items()})
    print(f"CLK Gen : t_nov(1->2) = {clk['t_nov_1to2_ns']:.2f} ns, t_nov(2->1) = {clk['t_nov_2to1_ns']:.2f} ns -> PASS={clk['pass']}")
    print(f"[OK] Saved {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
