v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -220 -240 220 -240 {dash=3}
L 4 220 -240 220 200 {dash=3}
L 4 220 200 -220 200 {dash=3}
L 4 -220 200 -220 -240 {dash=3}
T {Parameterized CMOS Inverter (inv_cell)} -195 -215 0 0 0.3 0.3 {font=Sans style=bold}
C {sky130_fd_pr/pfet_01v8.sym} 0 -70 0 0 {name=MP model=pfet_01v8 W='WP' L='LCH' nf=1 mult=1 ad='WP*0.29' as='WP*0.29' pd='2*(WP+0.29)' ps='2*(WP+0.29)' nrd='0.29/WP' nrs='0.29/WP'}
C {sky130_fd_pr/nfet_01v8.sym} 0 70 0 0 {name=MN model=nfet_01v8 W='WN' L='LCH' nf=1 mult=1 ad='WN*0.29' as='WN*0.29' pd='2*(WN+0.29)' ps='2*(WN+0.29)' nrd='0.29/WN' nrs='0.29/WN'}
C {devices/ipin.sym} -100 0 0 0 {name=p1 lab=A}
C {devices/opin.sym} 130 0 0 0 {name=p2 lab=Y}
C {devices/iopin.sym} 20 -140 0 1 {name=p3 lab=VDD}
C {devices/iopin.sym} 20 140 0 1 {name=p4 lab=VSS}
N -20 -70 -20 0 {}
N -20 0 -20 70 {}
N -100 0 -20 0 {}
N 20 -40 20 0 {}
N 20 0 20 40 {}
N 20 0 130 0 {}
N 20 -140 20 -100 {}
N 20 -70 50 -70 {}
N 50 -140 50 -70 {}
N 20 -140 50 -140 {}
N 20 100 20 140 {}
N 20 70 50 70 {}
N 50 70 50 140 {}
N 20 140 50 140 {}
