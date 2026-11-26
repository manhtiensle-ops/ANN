#!/usr/bin/env python3
"""
Task 2.1 — Ideal Switched-Capacitor Low-Pass Filter Golden Model (sky130-sc-lpf).

Implements:
  1. Exact 2-phase discrete-time charge-conservation difference equation:
       (C1 + C2) * Vout[n] - C2 * Vout[n-1] = C1 * Vin[n]
     and Z-domain transfer function:
       H(z) = alpha / (1 - (1 - alpha) * z^-1),   alpha = C1 / (C1 + C2) = 1/9.
  2. Bode Magnitude & Phase comparison: exact discrete H(e^{jwT}) vs. continuous
     first-order RC approximation H_RC(jw) = 1 / (1 + j * f / fc_RC), quantifying
     the -5.664% cutoff frequency shift (187.675 kHz vs. 198.944 kHz).
  3. Multi-tone step-and-hold (zero-order-hold staircase) transient simulation:
     passband tone (50 kHz) + high-frequency interferer (2 MHz) around VCM = 0.9 V.
  4. Coherent FFT spectral baseline (N = 16384, prime bin M_sig = 83, Hann window):
     extracts ideal numerical floor AND physical kT/C thermal-noise-limited baseline
     (SFDR, SNR, SNDR, THD, ENOB) to serve as the Week 3/4 Verification Gate reference.

Outputs:
  - python/metrics_golden.json
  - slides/figs/week2_bode_sc_vs_rc.png       (300 DPI)
  - slides/figs/week2_multitone_transient.png (300 DPI)
  - slides/figs/week2_coherent_fft.png        (300 DPI)
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter
from scipy.signal.windows import hann

ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "slides" / "figs"
sys.path.insert(0, str(ROOT / ".agents" / "skills" / "ieee-slide-engine" / "resources"))
from ieee_plot_style import IEEE_COLORS as C, apply_ieee_style  # noqa: E402

# ---------------------------------------------------------------------------
# Locked Single-Source-of-Truth Specifications
# ---------------------------------------------------------------------------
VDD = 1.8
VCM = 0.9
F_CLK = 10.0e6
T_CLK = 1.0 / F_CLK          # 100 ns
C1 = 100.0e-15               # 100 fF
C2 = 800.0e-15               # 800 fF
ALPHA = C1 / (C1 + C2)       # 1/9
R_EQ = 1.0 / (F_CLK * C1)    # 1.0 MOhm
FC_RC = 1.0 / (2.0 * math.pi * R_EQ * C2)
COS_WCT = 1.0 - (ALPHA ** 2) / (2.0 * (1.0 - ALPHA))  # 143/144
FC_SC = (F_CLK / (2.0 * math.pi)) * math.acos(COS_WCT)
KB = 1.380649e-23
TEMP_K = 300.0


def sc_difference_filter(v_in_samples: np.ndarray, v_init: float = VCM) -> np.ndarray:
    """Solve (C1 + C2)*Vout[n] - C2*Vout[n-1] = C1*Vin[n] with exact initial state."""
    x = v_in_samples - v_init
    b = np.array([ALPHA], dtype=np.float64)
    a = np.array([1.0, -(1.0 - ALPHA)], dtype=np.float64)
    y = lfilter(b, a, x)
    return y + v_init


def freq_response_sc(freqs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return magnitude (dB) and phase (deg) of H(e^{j 2 pi f T_clk})."""
    z_inv = np.exp(-1j * 2.0 * np.pi * freqs * T_CLK)
    h = ALPHA / (1.0 - (1.0 - ALPHA) * z_inv)
    mag_db = 20.0 * np.log10(np.abs(h))
    phase_deg = np.degrees(np.angle(h))
    return mag_db, phase_deg


def freq_response_rc(freqs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return magnitude (dB) and phase (deg) of continuous RC filter 1/(1 + j f/fc_RC)."""
    h = 1.0 / (1.0 + 1j * (freqs / FC_RC))
    mag_db = 20.0 * np.log10(np.abs(h))
    phase_deg = np.degrees(np.angle(h))
    return mag_db, phase_deg


def coherent_spectral_metrics(
    v_out: np.ndarray,
    m_sig: int,
    n_harmonics: int = 7,
) -> tuple[np.ndarray, np.ndarray, dict]:
    """
    Compute coherent Hann-windowed FFT metrics on N steady-state samples.

    Hann window main lobe spans m +/- 1 bins; DC spans bins 0..2.
    """
    n_fft = len(v_out)
    assert math.gcd(m_sig, n_fft) == 1, "m_sig and N must be coprime for coherent sampling"

    v_ac = v_out - np.mean(v_out)
    win = hann(n_fft, sym=False)
    # Coherent amplitude & power normalization
    coherent_gain = np.sum(win) / n_fft
    enbw_bins = n_fft * np.sum(win ** 2) / (np.sum(win) ** 2)  # 1.5 for periodic Hann

    spec = np.fft.rfft(v_ac * win)
    # Single-sided power spectrum (V^2 rms per bin, corrected for window coherent gain)
    psd = (np.abs(spec) / (n_fft * coherent_gain)) ** 2
    psd[1:-1] *= 2.0  # fold negative frequencies (except DC and Nyquist)
    # Divide bin-summed power by ENBW so sinusoidal lobe integration equals exact V_rms^2
    bin_power = psd / enbw_bins

    freqs = np.fft.rfftfreq(n_fft, d=T_CLK)

    def lobe_bins(center_bin: int) -> set[int]:
        return {b for b in range(center_bin - 2, center_bin + 3) if 0 <= b <= n_fft // 2}

    dc_bins = {0, 1, 2}
    sig_bins = lobe_bins(m_sig)
    p_sig = float(np.sum([bin_power[b] for b in sig_bins]))

    harm_powers = {}
    all_harm_bins: set[int] = set()
    for k in range(2, n_harmonics + 1):
        # Account for aliasing into [0, N/2]
        raw = (k * m_sig) % n_fft
        folded = raw if raw <= n_fft // 2 else n_fft - raw
        hb = lobe_bins(folded) - sig_bins - dc_bins
        pk = float(np.sum([bin_power[b] for b in hb]))
        harm_powers[f"H{k}_dBc"] = float(10.0 * np.log10(max(pk, 1e-36) / p_sig))
        all_harm_bins |= hb

    p_harm_total = 0.0
    for b in all_harm_bins:
        p_harm_total += float(bin_power[b])

    noise_bins = [
        b for b in range(3, n_fft // 2)
        if b not in sig_bins and b not in all_harm_bins
    ]
    p_noise = float(np.sum(bin_power[noise_bins]))
    p_nd = p_noise + p_harm_total

    # Highest non-signal spur across entire Nyquist band (excluding DC and fundamental lobe)
    spur_candidates = [
        b for b in range(3, n_fft // 2 + 1)
        if b not in sig_bins
    ]
    max_spur_bin = max(spur_candidates, key=lambda b: psd[b])
    # Integrate 3-bin lobe around max spur for accurate spur tone power
    p_max_spur = float(np.sum([bin_power[b] for b in range(max(3, max_spur_bin - 1), min(n_fft // 2 + 1, max_spur_bin + 2)) if b not in sig_bins]))

    snr_db = 10.0 * np.log10(p_sig / max(p_noise, 1e-36))
    sndr_db = 10.0 * np.log10(p_sig / max(p_nd, 1e-36))
    thd_db = 10.0 * np.log10(max(p_harm_total, 1e-36) / p_sig)
    sfdr_db = 10.0 * np.log10(p_sig / max(p_max_spur, 1e-36))
    enob = (sndr_db - 1.76) / 6.02

    # Spectrum in dBc relative to fundamental peak for clean visualization
    spec_dbc = 10.0 * np.log10(np.maximum(psd, 1e-36) / np.max(psd[list(sig_bins)]))

    metrics = {
        "N_fft": n_fft,
        "M_sig": m_sig,
        "f_in_Hz": m_sig * F_CLK / n_fft,
        "V_out_rms_V": math.sqrt(p_sig),
        "V_out_peak_V": math.sqrt(2.0 * p_sig),
        "SNR_dB": float(snr_db),
        "SNDR_dB": float(sndr_db),
        "SFDR_dB": float(sfdr_db),
        "THD_dB": float(thd_db),
        "THD_percent": float(100.0 * (10.0 ** (thd_db / 20.0))),
        "ENOB_bits": float(enob),
        "max_spur_freq_Hz": float(freqs[max_spur_bin]),
        "harmonics_dBc": harm_powers,
    }
    return freqs, spec_dbc, metrics


def simulate_ktc_sc_filter(
    v_in_samples: np.ndarray,
    seed: int = 42,
) -> np.ndarray:
    """
    Physically accurate discrete-time SC LPF with sampled kT/C thermal noise.

    In Phase 1, TG1 samples Vin onto C1 with variance kB*T/C1.
    In Phase 2, TG2 shares charge between C1 and C2, adding switch noise on C_eq = C1*C2/(C1+C2),
    yielding steady-state output noise variance kB*T/C2 (exact thermodynamic equipartition!).
    """
    rng = np.random.default_rng(seed)
    n = len(v_in_samples)
    sigma_phi1 = math.sqrt(KB * TEMP_K / C1)
    c_eq = (C1 * C2) / (C1 + C2)
    sigma_phi2 = math.sqrt(KB * TEMP_K / c_eq)

    v_n1 = rng.normal(0.0, sigma_phi1, size=n)
    # Charge error on C_eq transfers to V_out scaled by C_eq / (C1 + C2) ... wait:
    # Exact thermodynamic check:
    # Vout[n] = (1-alpha)*Vout[n-1] + alpha*(Vin[n] + v_n1[n]) + v_phi2_out[n]
    # Note Var((1-alpha)*Vout + alpha*(Vin + v_n1)):
    # Var(Vout) * [1 - (1-alpha)^2] = alpha^2 * (kT/C1) + Var(v_phi2_out).
    # In Phase 2, C1 || C2 freeze with relative voltage noise delta_V across C1-C2 loop of variance kT/C_eq;
    # by charge conservation (C1+C2)*v_phi2_out = C1 * delta_V => v_phi2_out = alpha * delta_V!
    # Check total steady-state variance:
    # Var(Vout) = alpha^2 * (kT/C1 + kT*(C1+C2)/(C1*C2)) / (alpha*(2-alpha))
    #           = alpha * (kT/C1) * (1 + (C1+C2)/C2) / (2 - alpha)
    #           = (C1/(C1+C2)) * (kT/C1) * ((C1+2C2)/C2) / ((C1+2C2)/(C1+C2)) = kT / C2 !!
    # Exact analytical identity: Var(Vout) == kB * T / C2!
    v_phi2_out = ALPHA * rng.normal(0.0, sigma_phi2, size=n)

    v_out = np.empty(n, dtype=np.float64)
    prev = VCM
    one_m_a = 1.0 - ALPHA
    for i in range(n):
        prev = one_m_a * prev + ALPHA * (v_in_samples[i] + v_n1[i]) + v_phi2_out[i]
        v_out[i] = prev
    return v_out


# ---------------------------------------------------------------------------
# Plotting (300 DPI, zero-overlap IEEE Modern layout)
# ---------------------------------------------------------------------------
def plot_bode(path: Path) -> None:
    apply_ieee_style()
    freqs = np.logspace(3, np.log10(F_CLK / 2.0), 2000)
    mag_sc, ph_sc = freq_response_sc(freqs)
    mag_rc, ph_rc = freq_response_rc(freqs)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.2), sharex=True, gridspec_kw={"height_ratios": [1.35, 1.0]})

    ax1.semilogx(freqs / 1e3, mag_rc, color=C["amber"], ls="--", lw=1.8, label=f"Continuous RC ($f_{{c,RC}}$ = {FC_RC/1e3:.2f} kHz)")
    ax1.semilogx(freqs / 1e3, mag_sc, color=C["cobalt"], lw=2.2, label=f"Exact Discrete SC $H(z)$ ($f_{{c,SC}}$ = {FC_SC/1e3:.2f} kHz)")
    ax1.axhline(-3.0103, color=C["slate"], ls=":", lw=1.0)
    ax1.axvline(FC_SC / 1e3, color=C["cobalt"], ls=":", lw=1.1)
    ax1.axvline(FC_RC / 1e3, color=C["amber"], ls=":", lw=1.1)

    ax1.annotate(
        f"$f_{{c,SC}}$ = {FC_SC/1e3:.2f} kHz\n($\\Delta f_c$ = −5.66% vs. RC)",
        xy=(FC_SC / 1e3, -3.01),
        xytext=(14.0, -13.5),
        fontsize=9,
        color=C["cobalt"],
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="#EFF6FF", ec=C["cobalt"], lw=0.8),
        arrowprops=dict(arrowstyle="->", color=C["cobalt"], lw=1.0),
    )
    mag_2m, _ = freq_response_sc(np.array([2.0e6]))
    ax1.plot(2000.0, mag_2m[0], "o", color=C["teal"], ms=5)
    ax1.annotate(
        f"2 MHz stopband: {mag_2m[0]:.1f} dB",
        xy=(2000.0, mag_2m[0]),
        xytext=(330.0, -25.5),
        fontsize=9,
        color=C["teal"],
        bbox=dict(boxstyle="round,pad=0.25", fc="#F0FDFA", ec=C["teal"], lw=0.8),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.0),
    )

    ax1.set_ylabel("Magnitude |H(f)| (dB)")
    ax1.set_ylim(-30, 3)
    ax1.set_title("Bode Frequency Response: Exact Z-Domain H(z) vs. Continuous RC")
    ax1.legend(loc="lower left", fontsize=9)

    ax2.semilogx(freqs / 1e3, ph_rc, color=C["amber"], ls="--", lw=1.8, label="Continuous RC Phase")
    ax2.semilogx(freqs / 1e3, ph_sc, color=C["cobalt"], lw=2.2, label="Discrete SC Phase $\\angle H(e^{j\\omega T_{clk}})$")
    ax2.axvline(5000.0, color=C["crimson"], ls="-.", lw=1.1)
    ax2.text(4650.0, -22.0, "Nyquist $f_{clk}/2$ = 5 MHz", ha="right", fontsize=8.8, color=C["crimson"], fontweight="bold")
    ax2.set_xlabel("Frequency (kHz)")
    ax2.set_ylabel("Phase (deg)")
    ax2.set_xlim(1.0, 5000.0)
    ax2.set_ylim(-95, 5)
    ax2.set_yticks([0, -22.5, -45, -67.5, -90])
    ax2.legend(loc="lower left", fontsize=8.8)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def plot_multitone_transient(path: Path) -> dict:
    apply_ieee_style()
    f_sig = 50.0e3     # Passband desired signal
    a_sig = 0.30       # 300 mV peak
    f_int = 2.0e6      # High-frequency stopband interferer
    a_int = 0.12       # 120 mV peak

    n_cycles_clk = 800  # 80 us total (4 full periods of 50 kHz; settle in first ~10 us)
    t_sample = np.arange(n_cycles_clk) * T_CLK
    v_in_s = VCM + a_sig * np.sin(2.0 * np.pi * f_sig * t_sample) + a_int * np.sin(2.0 * np.pi * f_int * t_sample)
    v_clean_s = VCM + a_sig * np.sin(2.0 * np.pi * f_sig * t_sample)
    v_out_s = sc_difference_filter(v_in_s, v_init=VCM)

    # Fine continuous time grid for plotting last 2 periods of 50 kHz (40 us -> 80 us)
    t_fine = np.linspace(40.0e-6, 80.0e-6, 6000)
    v_in_fine = VCM + a_sig * np.sin(2.0 * np.pi * f_sig * t_fine) + a_int * np.sin(2.0 * np.pi * f_int * t_fine)
    v_ideal_pb = VCM + a_sig * (10 ** (freq_response_sc(np.array([f_sig]))[0][0] / 20.0)) * np.sin(
        2.0 * np.pi * f_sig * t_fine + np.radians(freq_response_sc(np.array([f_sig]))[1][0])
    )

    mask = (t_sample >= 40.0e-6) & (t_sample <= 80.0e-6)
    mask_zoom = (t_sample >= 44.0e-6) & (t_sample <= 47.0e-6)
    mask_fine_zoom = (t_fine >= 44.0e-6) & (t_fine <= 47.0e-6)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.4, 5.2), gridspec_kw={"height_ratios": [1.25, 1.0]})

    ax1.plot(t_fine * 1e6, v_in_fine, color="#94A3B8", lw=0.9, alpha=0.85, label="Input: 50 kHz (0.30 V) + 2 MHz interferer (0.12 V)")
    ax1.step(t_sample[mask] * 1e6, v_out_s[mask], where="post", color=C["cobalt"], lw=2.0, label="SC LPF Staircase Output $V_{out}[n]$")
    ax1.axhline(VCM, color=C["slate"], ls=":", lw=0.8)
    ax1.set_xlim(40.0, 80.0)
    ax1.set_ylim(0.38, 1.44)
    ax1.set_ylabel("Voltage (V)")
    ax1.set_title("Multi-Tone Transient Response: 2 MHz Interferer Rejection (−20.0 dB)")
    ax1.legend(loc="upper right", fontsize=8.8)

    ax2.plot(t_fine[mask_fine_zoom] * 1e6, v_in_fine[mask_fine_zoom], color="#94A3B8", lw=1.1, ls="--", label="Corrupted Input $V_{in}(t)$")
    ax2.step(t_sample[mask_zoom] * 1e6, v_out_s[mask_zoom], where="post", color=C["cobalt"], lw=2.2, label="Zero-Order-Hold Step ($T_{clk}$ = 100 ns)")
    ax2.plot(t_fine[mask_fine_zoom] * 1e6, v_ideal_pb[mask_fine_zoom], color=C["teal"], lw=1.5, ls=":", label="Theoretical 50 kHz Envelope")
    ax2.set_xlim(44.0, 47.0)
    ax2.set_xlabel("Time (µs)")
    ax2.set_ylabel("Zoomed V (V)")
    ax2.set_title("Zoomed Staircase Hold Detail (44–47 µs, 30 Clock Cycles)")
    ax2.legend(loc="lower left", fontsize=8.6)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)

    # Measure steady-state ripple attenuation
    _ = v_clean_s
    return {
        "f_sig_Hz": f_sig,
        "A_sig_V": a_sig,
        "f_interferer_Hz": f_int,
        "A_interferer_V": a_int,
        "passband_gain_50kHz_dB": float(freq_response_sc(np.array([f_sig]))[0][0]),
        "stopband_gain_2MHz_dB": float(freq_response_sc(np.array([f_int]))[0][0]),
        "interferer_attenuation_factor": float(10 ** (-freq_response_sc(np.array([f_int]))[0][0] / 20.0)),
    }


def plot_coherent_fft(
    freqs: np.ndarray,
    spec_ideal_dbc: np.ndarray,
    spec_ktc_dbc: np.ndarray,
    m_ideal: dict,
    m_ktc: dict,
    path: Path,
) -> None:
    apply_ieee_style()
    fig, ax = plt.subplots(figsize=(7.4, 4.1))

    # Plot from bin 1 upward on log/linear frequency axis (linear up to 5 MHz or semilogx)
    valid = freqs >= 500.0
    ax.semilogx(freqs[valid] / 1e3, spec_ktc_dbc[valid], color="#94A3B8", lw=0.8, alpha=0.85,
                label=f"Golden + Physical kT/C Noise (SNR = {m_ktc['SNR_dB']:.1f} dB, ENOB = {m_ktc['ENOB_bits']:.2f} bits)")
    ax.semilogx(freqs[valid] / 1e3, spec_ideal_dbc[valid], color=C["cobalt"], lw=1.2, alpha=0.9,
                label=f"Noise-Free Float64 Golden (SFDR = {m_ideal['SFDR_dB']:.1f} dB, THD = {m_ideal['THD_dB']:.1f} dB)")

    f0_khz = m_ideal["f_in_Hz"] / 1e3
    ax.plot(f0_khz, 0.0, "o", color=C["teal"], ms=6)
    ax.annotate(
        f"Fundamental $f_0$ = {f0_khz:.3f} kHz\n($M_{{sig}}$ = {m_ideal['M_sig']}, $N$ = {m_ideal['N_fft']})",
        xy=(f0_khz, 0.0),
        xytext=(2.2, -18.0),
        fontsize=9,
        color=C["teal"],
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="#F0FDFA", ec=C["teal"], lw=0.8),
        arrowprops=dict(arrowstyle="->", color=C["teal"], lw=1.0),
    )

    ax.set_xlim(0.5, 5000.0)
    ax.set_ylim(-175, 10)
    ax.set_xlabel("Frequency (kHz)")
    ax.set_ylabel("Normalized Magnitude (dBc)")
    ax.set_title("Coherent FFT Spectrum (N = 16384, Hann Window, $V_{in,p}$ = 0.40 V)")
    ax.legend(loc="lower left", fontsize=8.6)

    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Bode comparison plot
    plot_bode(FIG_DIR / "week2_bode_sc_vs_rc.png")

    # 2. Multi-tone transient plot
    multitone_info = plot_multitone_transient(FIG_DIR / "week2_multitone_transient.png")

    # 3. Coherent FFT (N = 16384, discard 2048 settling clocks first so transient tail < 1e-100!)
    n_fft = 16384
    n_settle = 2048
    m_sig = 83  # prime, f_in = 50.6591796875 kHz
    a_in = 0.40  # 0.40 V peak around VCM = 0.9 V -> [0.50 V, 1.30 V]

    n_total = n_settle + n_fft
    idx = np.arange(n_total, dtype=np.float64)
    f_in = (m_sig / n_fft) * F_CLK
    v_in = VCM + a_in * np.sin(2.0 * np.pi * f_in * idx * T_CLK)

    v_out_ideal_all = sc_difference_filter(v_in, v_init=VCM)
    v_out_ideal = v_out_ideal_all[n_settle:]

    v_out_ktc_all = simulate_ktc_sc_filter(v_in, seed=2026)
    v_out_ktc = v_out_ktc_all[n_settle:]

    freqs, spec_ideal_dbc, metrics_ideal = coherent_spectral_metrics(v_out_ideal, m_sig=m_sig)
    _, spec_ktc_dbc, metrics_ktc = coherent_spectral_metrics(v_out_ktc, m_sig=m_sig)

    # Theoretical kT/C SNR check
    h_f0_lin = 10.0 ** (freq_response_sc(np.array([f_in]))[0][0] / 20.0)
    v_out_rms_theory = (a_in / math.sqrt(2.0)) * h_f0_lin
    v_ktc_rms_theory = math.sqrt(KB * TEMP_K / C2)
    snr_ktc_theory_db = 20.0 * math.log10(v_out_rms_theory / v_ktc_rms_theory)

    plot_coherent_fft(
        freqs,
        spec_ideal_dbc,
        spec_ktc_dbc,
        metrics_ideal,
        metrics_ktc,
        FIG_DIR / "week2_coherent_fft.png",
    )

    golden_payload = {
        "specs_locked": {
            "VDD_V": VDD,
            "VCM_V": VCM,
            "f_clk_Hz": F_CLK,
            "T_clk_s": T_CLK,
            "C1_F": C1,
            "C2_F": C2,
            "alpha": ALPHA,
            "R_eq_ohm": R_EQ,
            "fc_RC_Hz": FC_RC,
            "fc_SC_Hz": FC_SC,
            "fc_shift_percent": 100.0 * (FC_SC - FC_RC) / FC_RC,
            "OSR": F_CLK / (2.0 * FC_SC),
        },
        "multitone_transient": multitone_info,
        "coherent_fft_ideal_float64": metrics_ideal,
        "coherent_fft_with_kTC_noise": {
            **metrics_ktc,
            "v_n_out_rms_theory_V": v_ktc_rms_theory,
            "SNR_kTC_theory_dB": snr_ktc_theory_db,
        },
        "week3_verification_targets": {
            "fc_target_Hz": FC_SC,
            "fc_tolerance_pct": 5.0,
            "fc_pass_band_Hz": [FC_SC * 0.95, FC_SC * 1.05],
            "SFDR_min_target_dB": 50.0,
            "THD_max_target_dB": -48.0,
            "SNR_kTC_ceiling_dB": snr_ktc_theory_db,
        },
    }

    out_json = ROOT / "python" / "metrics_golden.json"
    out_json.write_text(json.dumps(golden_payload, indent=2))

    print("=== GOLDEN MODEL SUMMARY ===")
    print(f"fc_RC = {FC_RC/1e3:.3f} kHz | fc_SC = {FC_SC/1e3:.3f} kHz ({100*(FC_SC-FC_RC)/FC_RC:+.2f}%)")
    print(f"Ideal Float64 FFT : SFDR = {metrics_ideal['SFDR_dB']:.1f} dB, THD = {metrics_ideal['THD_dB']:.1f} dB, SNR = {metrics_ideal['SNR_dB']:.1f} dB")
    print(f"Physical kT/C FFT : SNR = {metrics_ktc['SNR_dB']:.2f} dB (theory {snr_ktc_theory_db:.2f} dB), SFDR = {metrics_ktc['SFDR_dB']:.2f} dB, ENOB = {metrics_ktc['ENOB_bits']:.2f} bits")
    print(f"[OK] Saved {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
