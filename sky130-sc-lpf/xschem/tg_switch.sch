v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -290 -255 310 -255 {dash=3}
L 4 310 -255 310 205 {dash=3}
L 4 310 205 -290 205 {dash=3}
L 4 -290 205 -290 -255 {dash=3}
T {Block 2: CMOS Transmission Gate Switch (tg_switch)} -265 -225 0 0 0.32 0.32 {font=Sans style=bold}
T {Optimized Wn = 2.0 um (nf=1), Wp = 6.0 um (nf=2), L = 0.15 um -> Ron < 4.7 kOhm, Low C_par} -265 -192 0 0 0.21 0.21 {layer=4}
C {sky130_fd_pr/pfet_01v8.sym} 0 -75 0 0 {name=MP model=pfet_01v8 W=6.0 L=0.15 nf=2 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} 0 75 0 0 {name=MN model=nfet_01v8 W=2.0 L=0.15 nf=1 mult=1}
C {devices/iopin.sym} -180 0 0 1 {name=p_vin lab=VIN}
C {devices/iopin.sym} 210 0 0 0 {name=p_vout lab=VOUT}
C {devices/ipin.sym} -180 -75 0 0 {name=p_phib lab=PHI_B}
C {devices/ipin.sym} -180 75 0 0 {name=p_phi lab=PHI}
C {devices/iopin.sym} 145 -145 0 0 {name=p_vdd lab=VDD}
C {devices/iopin.sym} 145 155 0 0 {name=p_vss lab=VSS}
N -180 0 -100 0 {}
N -100 -130 -100 0 {}
N -100 0 -100 130 {}
N -100 -130 20 -130 {}
N 20 -130 20 -105 {}
N -100 130 20 130 {}
N 20 105 20 130 {}
N 20 -45 20 0 {}
N 20 0 20 45 {}
N 20 0 210 0 {}
N -180 -75 -20 -75 {}
N -180 75 -20 75 {}
N 20 -75 145 -75 {}
N 145 -145 145 -75 {}
N 20 75 145 75 {}
N 145 75 145 155 {}
