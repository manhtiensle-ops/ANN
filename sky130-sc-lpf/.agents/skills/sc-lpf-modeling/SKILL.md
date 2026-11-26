---
name: sc-lpf-modeling
description: >-
  Use this skill when building, running, or reviewing Python behavioral models,
  Z-domain/RC frequency response comparisons, coherent FFT spectral analysis
  (SFDR, SNR, SNDR, THD), non-ideal error budgets (Ron, AOL, charge injection,
  kT/C), transistor W/L sizing scripts, or Golden-vs-Ngspice waveform/FFT
  overlays for sky130-sc-lpf (Weeks 2, 3, and 4).
---

# SC-LPF Python Modeling & Sizing Runbook

Follow this procedure whenever executing `/tuan 2`, `/code golden_model`, `/code nonideal_budget`, `/code sizing_calc`, `/code ngspice_vs_golden`, or `/review` with spectral/sizing metrics.

## References
- Exact mathematical derivations & formulas: [specs_and_math.md](../../../docs/knowledge/specs_and_math.md)
- Verified `sky130A` BSIM4 TT device parameters: [sky130a_pdk_reference.md](../../../docs/knowledge/sky130a_pdk_reference.md)
- 300-DPI IEEE Matplotlib style helper: [ieee_plot_style.py](../ieee-slide-engine/resources/ieee_plot_style.py)

---

## Procedure 1: Ideal Golden Model (`python/golden_model.py`)
1. **Discrete-Time Difference Equation (Exact 2-Phase Charge Conservation):**
   - $\alpha = \frac{C_1}{C_1 + C_2} = \frac{100\text{ fF}}{900\text{ fF}} = \frac{1}{9}$
   - $V_{\text{out}}[n] = (1 - \alpha) V_{\text{out}}[n-1] + \alpha V_{\text{in}}[n]$ around $V_{CM} = 0.9\text{ V}$.
   - Transfer function: $H(z) = \frac{\alpha}{1 - (1 - \alpha)z^{-1}}$.
2. **Bode Magnitude & Phase Overlay ($H(e^{j\omega T_{\text{clk}}})$ vs. Continuous $H_{\text{RC}}(j\omega)$):**
   - Continuous approximation: $f_{c,\text{RC}} = \frac{f_{\text{clk}} C_1}{2\pi C_2} \approx 198.94\text{ kHz}$.
   - Exact discrete $-3\text{ dB}$ frequency: $f_{c,\text{SC}} = \frac{f_{\text{clk}}}{2\pi}\arccos\left(1 - \frac{\alpha^2}{2(1-\alpha)}\right) \approx 187.67\text{ kHz}$ ($\Delta f_c = -5.66\%$).
   - Annotate both $f_{c,\text{SC}}$ and $f_{c,\text{RC}}$ plus Nyquist $f_{\text{clk}}/2 = 5\text{ MHz}$ without label overlap.
3. **Multi-Tone Step-Hold Transient:**
   - Simulate $v_{\text{in}}(t) = V_{CM} + A_{\text{sig}}\sin(2\pi f_{\text{sig}} t) + A_{\text{int}}\sin(2\pi f_{\text{int}} t)$ with $f_{\text{sig}} = 50\text{ kHz}$ (passband) and $f_{\text{int}} = 2\text{ MHz}$ (stopband interferer), rendering zero-order-hold staircase output at $T_{\text{clk}} = 100\text{ ns}$.
4. **Coherent FFT Baseline ($N = 16384$):**
   - Enforce prime coherent bin $M_{\text{sig}}$ (`gcd(M_sig, N) == 1`): $f_{\text{in}} = \frac{M_{\text{sig}}}{N} f_{\text{clk}}$ (e.g., $M_{\text{sig}} = 83 \Rightarrow f_{\text{in}} = 50.65918\text{ kHz}$).
   - Remove DC ($V_{CM}$) mean, apply exact Hann window (`scipy.signal.windows.hann(N, sym=False)`), integrate $\pm 1$ bins around fundamental & harmonics ($2f_0 \dots 7f_0$) to account for Hann main-lobe width, and export **SFDR, SNR, SNDR, THD, ENOB** to `python/metrics_golden.json`.

---

## Procedure 2: Non-Ideal Error Budget (`python/nonideal_budget.py`)
1. **Switch Resistance $R_{\text{on}}$ Sweep ($100\ \Omega \to 50\text{ k}\Omega$):**
   - Incomplete charge settling in $T_{\text{clk}}/2 = 50\text{ ns}$: $\epsilon_{\text{set}} = e^{-T_{\text{clk}} / (2 \cdot 2 R_{\text{on}} C_1)}$ (accounting for $TG_1$ or $TG_2$ path).
   - Verify budget threshold: $R_{\text{on}} < 5\text{ k}\Omega \Rightarrow \tau = R_{\text{on}} C_1 < 0.5\text{ ns} \ll 50\text{ ns}$ ($> 50\tau$, dynamic nonlinear $R_{\text{on}}(V)$ THD budget requires $R_{\text{on}} < 5\text{ k}\Omega$).
2. **Finite 5T-OTA Gain $A_{OL}$ Sweep ($10\text{ dB} \to 70\text{ dB}$):**
   - Modified charge equation with finite $A_{OL}$:
     $$H_{A}(z) = \frac{\alpha / \left(1 + \frac{1}{A_{OL}(1-\alpha)}\right)}{1 - \frac{1-\alpha + 1/A_{OL}}{1 + \frac{1}{A_{OL}} \cdot \frac{C_1+C_2}{C_2}\dots} z^{-1}}$$
     (Use exact charge conservation at virtual node $V_- = V_{CM} - \frac{v_{\text{out}}}{A_{OL}}$ from `specs_and_math.md`).
   - Prove DC gain error $< 1.5\%$ and pole shift $< 1.5\%$ when $A_{OL} \ge 38\text{–}40\text{ dB}$ ($A_{OL} \ge 80\text{–}100\text{ V/V}$).
3. **Charge Injection & $kT/C$ Thermal Noise:**
   - Compute $\Delta V_{\text{CI}} \approx \frac{W L C_{ox} (V_{GS} - V_{TH})}{2 C_{\text{hold}}}$ vs. switch area $W \times L$ and CMOS TG complementary cancellation + dummy switch ($W/2$).
   - Verify total sampled noise $v_{n,\text{rms}} = \sqrt{\frac{kT}{C_2}\dots} \approx 72\ \mu\text{V}_{\text{rms}}$ ($\text{SNR}_{\text{max}} > 75\text{ dB}$ for $V_{p} = 0.4\text{ V}$).

---

## Procedure 3: Sky130A Sizing Calculator (`python/sizing_calc.py`)
1. Use verified BSIM4 `sky130A` TT constants from `sky130a_pdk_reference.md` (notably $V_{TH,n} \approx 0.63\text{ V}$ and $|V_{TH,p}| \approx 0.98\text{ V}$ for `01v8` devices!).
2. Size all 4 sub-blocks (`non_overlap_clk`, `tg_switch`, `sc_core` unit MIM cap $4.85\ \mu\text{m} \times 9.85\ \mu\text{m}$, `ota_5t` `M1–M5` + bias mirror `M6`) with explicit `W`, `L`, `nf`, `mult` on $0.05\ \mu\text{m}$ layout grid.
3. Export machine-readable `python/sizing_table.json` and Markdown summary table.

---

## Procedure 4: Golden vs. Pre-Layout / Post-Layout Overlay (`python/ngspice_vs_golden.py`)
1. Sample Ngspice `.tran` output strictly at the end of phase $\Phi_2$ (just before $\Phi_2$ falling edge, e.g., $t_n = n T_{\text{clk}} + 95\text{ ns}$) to avoid continuous-time slewing transients when computing discrete-time SC FFT.
2. Export 300-DPI overlay plots (Time-Domain Staircase, Swept/Multitone Bode Magnitude, Coherent FFT Spectrum) and update `metrics_comparison.json` against Verification Gates.
