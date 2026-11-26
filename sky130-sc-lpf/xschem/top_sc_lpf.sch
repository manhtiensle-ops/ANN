v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -580 -260 660 -260 {dash=3}
L 4 660 -260 660 220 {dash=3}
L 4 660 220 -580 220 {dash=3}
L 4 -580 220 -580 -260 {dash=3}
T {Top-Level Switched-Capacitor Low-Pass Filter (top_sc_lpf -- SkyWater 130nm)} -550 -228 0 0 0.38 0.38 {font=Sans style=bold}
T {f_clk = 10 MHz | C1 = 100 fF, C2 = 800 fF | fc_Golden = 187.675 kHz | VDD = 1.8 V, VCM = 0.9 V} -550 -190 0 0 0.25 0.25 {layer=4}
C {devices/iopin.sym} -500 -130 0 1 {name=p_vdd lab=VDD}
C {devices/iopin.sym} -500 -90 0 1 {name=p_vss lab=VSS}
C {devices/ipin.sym} -530 35 0 0 {name=p_clk lab=CLK}
C {non_overlap_clk.sym} -360 35 0 0 {name=XCLK}
C {devices/lab_pin.sym} -360 -70 0 0 {name=l_clk_vdd lab=VDD}
C {devices/lab_pin.sym} -360 140 0 0 {name=l_clk_vss lab=VSS}
C {devices/ipin.sym} -200 -95 0 0 {name=p_vin lab=VIN}
C {sc_core.sym} 10 20 0 0 {name=XSC}
C {devices/lab_pin.sym} 10 -95 0 0 {name=l_sc_vdd lab=VDD}
C {devices/lab_pin.sym} 10 135 0 0 {name=l_sc_vss lab=VSS}
C {ota_5t.sym} 390 15 0 0 {name=XOTA}
C {devices/lab_pin.sym} 390 -85 0 0 {name=l_ota_vdd lab=VDD}
C {devices/lab_pin.sym} 390 115 0 0 {name=l_ota_vss lab=VSS}
C {devices/ipin.sym} 195 105 0 0 {name=p_ib lab=IBIAS}
C {devices/opin.sym} 600 5 0 0 {name=p_vout lab=VOUT}
N -530 35 -495 35 {}
N -200 -95 -145 -95 {}
N -145 -95 -145 -15 {}
N -145 -15 -115 -15 {}
N -225 -10 -170 -10 {lab=PHI1}
N -170 -10 -170 15 {}
N -170 15 -115 15 {}
N -225 20 -185 20 {lab=PHI1_B}
N -185 20 -185 38 {}
N -185 38 -115 38 {}
N -225 50 -185 50 {lab=PHI2}
N -185 50 -185 61 {}
N -185 61 -115 61 {}
N -225 80 -170 80 {lab=PHI2_B}
N -170 80 -170 84 {}
N -170 84 -115 84 {}
N 135 -15 275 -15 {lab=VX}
N 195 105 258 105 {}
N 258 60 258 105 {}
N 258 60 275 60 {}
N 505 5 545 5 {lab=VOUT}
N 545 5 600 5 {}
N 545 5 545 165 {}
N 235 165 545 165 {}
N 235 25 235 165 {}
N 235 25 275 25 {}
