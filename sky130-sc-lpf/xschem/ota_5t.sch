v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -390 -280 380 -280 {dash=3}
L 4 380 -280 380 260 {dash=3}
L 4 380 260 -390 260 {dash=3}
L 4 -390 260 -390 -280 {dash=3}
T {Block 4: 5T-OTA Operational Transconductance Amplifier (ota_5t)} -365 -248 0 0 0.34 0.34 {font=Sans style=bold}
T {A_OL = 41.62 dB | GBW = 43.91 MHz | PM = 81.27 deg (CL = 1 pF, I_ref = 30 uA)} -365 -214 0 0 0.23 0.23 {layer=4}
C {sky130_fd_pr/pfet_01v8.sym} -110 -110 0 1 {name=M3 model=pfet_01v8 W=16.0 L=0.80 nf=4 mult=1}
C {sky130_fd_pr/pfet_01v8.sym} 110 -110 0 0 {name=M4 model=pfet_01v8 W=16.0 L=0.80 nf=4 mult=1}
C {devices/iopin.sym} 0 -175 0 0 {name=p_vdd lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} -150 10 0 0 {name=M1 model=nfet_01v8 W=32.0 L=0.80 nf=8 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} 150 10 0 1 {name=M2 model=nfet_01v8 W=32.0 L=0.80 nf=8 mult=1}
C {devices/opin.sym} 290 -50 0 0 {name=p_vout lab=VOUT}
C {devices/ipin.sym} -250 10 0 0 {name=p_inp lab=INP}
C {devices/ipin.sym} 250 10 0 1 {name=p_inn lab=INN}
C {devices/lab_pin.sym} 0 -30 0 0 {name=l_b12 lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} -20 150 0 0 {name=M5 model=nfet_01v8 W=24.0 L=1.00 nf=6 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} -260 150 0 1 {name=M6 model=nfet_01v8 W=24.0 L=1.00 nf=6 mult=1}
C {devices/ipin.sym} -280 65 0 0 {name=p_ib lab=IBIAS}
C {devices/iopin.sym} 0 220 0 0 {name=p_vss lab=VSS}
N -185 -175 -130 -175 {}
N -130 -175 0 -175 {}
N 0 -175 130 -175 {}
N 130 -175 185 -175 {}
N -130 -175 -130 -140 {}
N 130 -175 130 -140 {}
N -185 -175 -185 -110 {}
N -185 -110 -130 -110 {}
N 185 -175 185 -110 {}
N 130 -110 185 -110 {}
N -90 -110 -60 -110 {}
N -60 -110 90 -110 {}
N -60 -110 -60 -60 {}
N -130 -60 -60 -60 {}
N -130 -80 -130 -60 {lab=VD1}
N -130 -60 -130 -20 {}
N 130 -80 130 -50 {}
N 130 -50 130 -20 {}
N 130 -50 290 -50 {}
N -250 10 -170 10 {}
N 170 10 250 10 {}
N -130 10 0 10 {}
N 0 10 130 10 {}
N 0 -30 0 10 {}
N -130 40 -130 85 {}
N 130 40 130 85 {}
N -130 85 0 85 {lab=VTAIL}
N 0 85 130 85 {}
N 0 85 0 120 {}
N -280 65 -280 100 {}
N -280 100 -280 120 {}
N -280 100 -210 100 {}
N -210 100 -210 150 {}
N -240 150 -210 150 {lab=VBIAS}
N -210 150 -40 150 {}
N -330 220 -280 220 {}
N -280 220 0 220 {}
N 0 220 75 220 {}
N -280 180 -280 220 {}
N 0 180 0 220 {}
N -330 150 -280 150 {}
N -330 150 -330 220 {}
N 0 150 75 150 {}
N 75 150 75 220 {}
