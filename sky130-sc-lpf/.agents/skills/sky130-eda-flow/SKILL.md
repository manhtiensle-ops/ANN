---
name: sky130-eda-flow
description: >-
  Use this skill when creating Xschem schematics, running Ngspice Pre-Layout or
  Post-Layout simulations (.op, .dc, .ac, .tran), designing Magic VLSI analog
  layouts (Common-Centroid ABBA, unit MIM capacitor arrays, guard rings), or
  running DRC, Netgen LVS, and PEX extraction on SkyWater 130nm (sky130A) in
  iic-osic-tools (Weeks 1, 3, and 4).
---

# Sky130A Analog EDA & Physical Verification Runbook

Follow this runbook for `/tuan 1` (Task 1.3), `/tuan 3`, `/tuan 4`, `/code [spice_tb]`, and `/review` of transistor/layout results.

## References
- Exact `sky130A` device syntax, BSIM4 TT parameters & MIM cap formula: [sky130a_pdk_reference.md](../../../docs/knowledge/sky130a_pdk_reference.md)
- Environment verification script: [check_env.sh](./scripts/check_env.sh)

---

## Step 0: Mandatory PDK Environment Switch
Every shell session in `iic-osic-tools` defaults to `ihp-sg13g2`. **Always prefix EDA shell commands with:**
```bash
source /headless/ANN/sky130-sc-lpf/env_sky130.sh
```
Verify `.spiceinit` (`set ngbehavior=hsa` and `set ng_nomodcheck`) exists in the working directory before invoking `ngspice -b`.

---

## Step 1: Sky130A SPICE Instantiation Rules
- **Library include:**
  ```spice
  .lib "/foss/pdks/sky130A/libs.tech/combined/sky130.lib.spice" tt
  ```
- **Dimension units:** `.option scale=1.0u` is active inside `sky130.lib.spice`! Pass `w` and `l` as **plain numbers in micrometers** (e.g., `w=4.0 l=0.5 nf=2`, **NEVER** `w=4u` which would become $4 \times 10^{-12}\text{ m}$!).
- **Approved devices:**
  - `XM1 d g s b sky130_fd_pr__nfet_01v8 w=4.0 l=0.5 nf=2 mult=1`
  - `XM3 d g s b sky130_fd_pr__pfet_01v8 w=8.0 l=0.5 nf=2 mult=1`
  - `XC1 top bot sky130_fd_pr__cap_mim_m3_1 w=4.85 l=9.85 mult=1` ($C_1 = 100.00\text{ fF}$)
  - `XC2 top bot sky130_fd_pr__cap_mim_m3_1 w=4.85 l=9.85 mult=8` ($C_2 = 800.00\text{ fF}$)

---

## Step 2: Week 3 Pre-Layout Verification Gates
1. **`non_overlap_clk` (`ngspice/tb_clk.spice`):**
   - Run `.tran 10p 300n` at $f_{\text{clk}} = 10\text{ MHz}$ ($t_r = t_f = 0.5\text{ ns}$).
   - Measure $t_{\text{nov},12}$ and $t_{\text{nov},21}$ at $50\%$ crossing ($0.9\text{ V}$): **PASS** if $t_{\text{nov}} \in [2\text{ ns}, 5\text{ ns}]$ and $\max(V_{\Phi_1} \cdot V_{\Phi_2}) < 0.05\text{ V}^2$ during transitions.
2. **`tg_switch` (`ngspice/tb_tg.spice`):**
   - Sweep $V_{\text{in}} \in [0\text{ V}, 1.8\text{ V}]$ with small test $\Delta V = 1\text{ mV}$, compute $R_{\text{on}}(V_{\text{in}}) = \Delta V / I_{\text{test}}$.
   - **PASS** if $R_{\text{on}} < 5\text{ k}\Omega$ across full signal swing around $0.9\text{ V}$.
3. **`ota_5t` (`ngspice/tb_ota.spice`):**
   - `.op`: Check `vds > vdsat` and region saturation for `M1–M5`. Watch PMOS headroom (`|Vthp| ≈ 0.98 V` in `pfet_01v8`).
   - `.ac dec 100 1 1G` (open-loop with large $L_{\text{fb}} = 1\text{ GH}, C_{\text{fb}} = 1\text{ GF}$ around $V_{CM} = 0.9\text{ V}$, $C_L = 1\text{ pF}$): **PASS** if $A_{OL} > 35\text{–}40\text{ dB}$, $\text{GBW} > 10\text{ MHz}$, $\text{PM} \ge 60^\circ$.
   - `.tran`: Unity-gain step ($0.7\text{ V} \leftrightarrow 1.1\text{ V}$) for Slew Rate $\text{SR}^+, \text{SR}^-$ and DC offset at $V_{\text{in}} = 0.9\text{ V}$.
4. **`top_sc_lpf` (`ngspice/tb_top_sc_lpf.spice`):**
   - Coherent `.tran` with `maxstep <= 100p`, `reltol=1e-4`, `vntol=1e-6` to preserve charge accuracy on $100\text{ fF}$.
   - Export `wrdata` to CSV, analyze via `python/ngspice_vs_golden.py`. **PASS** if $|\Delta f_c / f_{c,\text{golden}}| < 5\%$.

---

## Step 3: Week 4 Physical Design & PEX Verification Gates
1. **Analog Layout Rules (Magic VLSI `-rcfile /foss/pdks/sky130A/libs.tech/magic/sky130A.magicrc`):**
   - Multi-finger FETs (`nf >= 2`) to minimize drain/source junction capacitance $C_{db}, C_{sb}$.
   - **Common-Centroid (ABBA)** placement for `M1/M2` differential pair and `M3/M4` current mirror.
   - **Unit-Cell MIM Array:** $1\times$ unit cell ($4.85 \times 9.85\ \mu\text{m}$) for $C_1$, $8\times$ parallel unit cells for $C_2$, surrounded by grounded **Dummy MIM Ring** for $1:8$ etching matching; connect sensitive virtual node (`V_minus`) to **top plate (`m4`/`capm`)** to minimize bottom-plate parasitic to substrate!
   - Separate P+ substrate **Guard Rings** (`psubdiff` + `licon` + `li1`) isolating digital `non_overlap_clk` from analog `sc_core` & `ota_5t`, plus N-well tap rings for PMOS wells.
2. **DRC Check (Batch Magic):**
   ```bash
   magic -dnull -noconsole -rcfile $PDKPATH/libs.tech/magic/sky130A.magicrc << 'EOF'
   load layout/top_sc_lpf.mag
   select top cell
   expand
   drc euclidean on
   drc style drc(full)
   drc check
   drc catchup
   drc count total
   quit -noprompt
   EOF
   ```
   **PASS:** `Total DRC errors found: 0`.
3. **LVS Check (Netgen Batch):**
   ```bash
   netgen -batch lvs "layout/top_sc_lpf_lvs.spice top_sc_lpf" "ngspice/top_sc_lpf_sch.spice top_sc_lpf" $PDKPATH/libs.tech/netgen/sky130A_setup.tcl layout/lvs_report.out
   ```
   **PASS:** `Netlists match uniquely` and `Property errors were not found`.
4. **Parasitic Extraction (PEX) & 3-Column Comparison:**
   - Extract full coupled/parasitic capacitances: `extract all`, `ext2sim labels on`, `ext2sim`, `extresist tolerance 10`, `ext2spice lvs`, `ext2spice cthresh 0`, `ext2spice extresist on`, `ext2spice -o layout/top_sc_lpf_pex.spice`.
   - Re-run coherent `.tran` + FFT and compile the 3-column table (**Golden Model vs. Pre-Layout vs. Post-Layout PEX**).
