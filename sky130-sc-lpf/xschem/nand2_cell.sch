v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -260 -260 260 -260 {dash=3}
L 4 260 -260 260 230 {dash=3}
L 4 260 230 -260 230 {dash=3}
L 4 -260 230 -260 -260 {dash=3}
T {2-Input CMOS NAND Gate (nand2_cell)} -235 -235 0 0 0.3 0.3 {font=Sans style=bold}
C {sky130_fd_pr/pfet_01v8.sym} -80 -110 0 0 {name=MPA model=pfet_01v8 W=2.0 L=0.15 nf=1 mult=1}
C {sky130_fd_pr/pfet_01v8.sym} 60 -110 0 0 {name=MPB model=pfet_01v8 W=2.0 L=0.15 nf=1 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} 60 20 0 0 {name=MNA model=nfet_01v8 W=1.6 L=0.15 nf=1 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} 60 120 0 0 {name=MNB model=nfet_01v8 W=1.6 L=0.15 nf=1 mult=1}
C {devices/iopin.sym} -60 -180 0 1 {name=p3 lab=VDD}
C {devices/opin.sym} 180 -50 0 0 {name=p5 lab=Y}
C {devices/iopin.sym} 80 190 0 1 {name=p4 lab=VSS}
C {devices/ipin.sym} -180 20 0 0 {name=p1 lab=A}
C {devices/ipin.sym} -180 120 0 0 {name=p2 lab=B}
N -60 -180 -30 -180 {}
N -30 -180 80 -180 {}
N 80 -180 120 -180 {}
N -60 -180 -60 -140 {}
N 80 -180 80 -140 {}
N -60 -110 -30 -110 {}
N -30 -180 -30 -110 {}
N 80 -110 120 -110 {}
N 120 -180 120 -110 {}
N -60 -80 -60 -50 {}
N 80 -80 80 -50 {}
N 80 -50 80 -10 {}
N -60 -50 80 -50 {}
N 80 -50 180 -50 {}
N 80 50 80 90 {}
N 80 150 80 190 {}
N 80 20 130 20 {}
N 80 120 130 120 {}
N 130 20 130 120 {}
N 130 120 130 190 {}
N 80 190 130 190 {}
N -180 20 -140 20 {}
N -140 20 40 20 {}
N -140 -110 -100 -110 {}
N -140 -110 -140 20 {}
N -180 120 10 120 {}
N 10 120 40 120 {}
N 10 -110 40 -110 {}
N 10 -110 10 120 {}
