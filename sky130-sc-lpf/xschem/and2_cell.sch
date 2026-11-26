v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -300 -180 300 -180 {dash=3}
L 4 300 -180 300 150 {dash=3}
L 4 300 150 -300 150 {dash=3}
L 4 -300 150 -300 -180 {dash=3}
T {2-Input CMOS AND Gate (and2_cell = NAND2 + NOT)} -275 -155 0 0 0.28 0.28 {font=Sans style=bold}
C {devices/iopin.sym} -240 -100 0 1 {name=p_vdd lab=VDD}
C {devices/iopin.sym} -240 -65 0 1 {name=p_vss lab=VSS}
C {devices/ipin.sym} -240 -20 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -240 20 0 0 {name=p2 lab=B}
C {nand2_cell.sym} -80 0 0 0 {name=XNAND}
C {devices/lab_pin.sym} -80 -68 0 0 {name=lv_n lab=VDD}
C {devices/lab_pin.sym} -80 68 0 0 {name=lg_n lab=VSS}
C {inv_cell.sym} 110 0 0 0 {name=XINV WN=1.0 WP=2.5 LCH=0.15}
C {devices/lab_pin.sym} 110 -64 0 0 {name=lv_i lab=VDD}
C {devices/lab_pin.sym} 110 64 0 0 {name=lg_i lab=VSS}
C {devices/opin.sym} 240 0 0 0 {name=p3 lab=Y}
N -240 -20 -155 -20 {}
N -240 20 -155 20 {}
N -5 0 42 0 {lab=Y_B}
N 178 0 240 0 {}
