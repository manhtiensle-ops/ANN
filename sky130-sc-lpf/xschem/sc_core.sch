v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -520 -300 560 -300 {dash=3}
L 4 560 -300 560 250 {dash=3}
L 4 560 250 -520 250 {dash=3}
L 4 -520 250 -520 -300 {dash=3}
T {Block 3: Switched-Capacitor MIM Filter Core (sc_core)} -490 -268 0 0 0.38 0.38 {font=Sans style=bold}
T {C1 = 100 fF (1x 4.85x9.85 um MIM) | C2 = 800 fF (8x unit MIM) | W/2 Dummy Charge Cancellation} -490 -230 0 0 0.25 0.25 {layer=4}
C {devices/iopin.sym} -430 -165 0 1 {name=p_vdd lab=VDD}
C {devices/iopin.sym} -430 -125 0 1 {name=p_vss lab=VSS}
C {devices/ipin.sym} -430 75 0 0 {name=p_clk0 lab=PHI1}
C {devices/ipin.sym} -430 115 0 0 {name=p_clk1 lab=PHI1_B}
C {devices/ipin.sym} -430 155 0 0 {name=p_clk2 lab=PHI2}
C {devices/ipin.sym} -430 195 0 0 {name=p_clk3 lab=PHI2_B}
C {devices/ipin.sym} -380 -10 0 0 {name=p_vin lab=VIN}
C {tg_switch.sym} -210 -10 0 0 {name=XTG1}
C {devices/lab_pin.sym} -242 -78 0 0 {name=l_tg1_pb lab=PHI1_B}
C {devices/lab_pin.sym} -178 -78 0 1 {name=l_tg1_vdd lab=VDD}
C {devices/lab_pin.sym} -242 58 0 0 {name=l_tg1_p lab=PHI1}
C {devices/lab_pin.sym} -178 58 0 1 {name=l_tg1_vss lab=VSS}
C {sky130_fd_pr/cap_mim_m3_1.sym} -20 115 0 0 {name=C1 model=cap_mim_m3_1 W=4.85 L=9.85 MF=1}
C {devices/lab_pin.sym} -20 195 0 0 {name=l_c1_vss lab=VSS}
C {tg_switch.sym} 170 -10 0 0 {name=XTG2}
C {devices/lab_pin.sym} 138 -78 0 0 {name=l_tg2_pb lab=PHI2_B}
C {devices/lab_pin.sym} 202 -78 0 1 {name=l_tg2_vdd lab=VDD}
C {devices/lab_pin.sym} 138 58 0 0 {name=l_tg2_p lab=PHI2}
C {devices/lab_pin.sym} 202 58 0 1 {name=l_tg2_vss lab=VSS}
C {sky130_fd_pr/cap_mim_m3_1.sym} 320 115 0 0 {name=C2 model=cap_mim_m3_1 W=4.85 L=9.85 MF=8}
C {devices/lab_pin.sym} 320 195 0 0 {name=l_c2_vss lab=VSS}
C {tg_dummy.sym} 380 -130 0 0 {name=XDUM2}
C {devices/lab_pin.sym} 350 -194 0 0 {name=l_d2_gp lab=PHI2}
C {devices/lab_pin.sym} 410 -194 0 1 {name=l_d2_vdd lab=VDD}
C {devices/lab_pin.sym} 350 -66 0 0 {name=l_d2_gn lab=PHI2_B}
C {devices/lab_pin.sym} 410 -66 0 1 {name=l_d2_vss lab=VSS}
C {devices/opin.sym} 490 -10 0 0 {name=p_vx lab=VX}
N -430 75 -385 75 {lab=PHI1}
N -430 115 -385 115 {lab=PHI1_B}
N -430 155 -385 155 {lab=PHI2}
N -430 195 -385 195 {lab=PHI2_B}
N -380 -10 -298 -10 {}
N -122 -10 -20 -10 {lab=V1}
N -20 -10 82 -10 {}
N -20 -10 -20 85 {}
N -20 145 -20 195 {}
N 258 -10 280 -10 {lab=VX}
N 280 -10 320 -10 {}
N 320 -10 490 -10 {}
N 320 -10 320 85 {}
N 320 145 320 195 {}
N 280 -130 280 -10 {}
N 280 -130 295 -130 {}
