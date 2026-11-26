v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -260 -230 260 -230 {dash=3}
L 4 260 -230 260 190 {dash=3}
L 4 260 190 -260 190 {dash=3}
L 4 -260 190 -260 -230 {dash=3}
T {Half-Sized CMOS Dummy Switch (tg_dummy: 1.0 / 3.0 um)} -235 -205 0 0 0.28 0.28 {font=Sans style=bold}
C {sky130_fd_pr/pfet_01v8.sym} 0 -65 0 0 {name=MPD model=pfet_01v8 W=3.0 L=0.15 nf=1 mult=1}
C {sky130_fd_pr/nfet_01v8.sym} 0 65 0 0 {name=MND model=nfet_01v8 W=1.0 L=0.15 nf=1 mult=1}
C {devices/iopin.sym} 160 0 0 0 {name=p_vn lab=VNODE}
C {devices/ipin.sym} -140 -65 0 0 {name=p_gp lab=G_P}
C {devices/ipin.sym} -140 65 0 0 {name=p_gn lab=G_N}
C {devices/iopin.sym} 125 -135 0 0 {name=p_vdd lab=VDD}
C {devices/iopin.sym} 125 135 0 0 {name=p_vss lab=VSS}
N 20 -95 70 -95 {}
N 20 -35 70 -35 {}
N 20 35 70 35 {}
N 20 95 70 95 {}
N 70 -95 70 -35 {}
N 70 -35 70 0 {}
N 70 0 70 35 {}
N 70 35 70 95 {}
N 70 0 160 0 {}
N -140 -65 -20 -65 {}
N -140 65 -20 65 {}
N 20 -65 125 -65 {}
N 125 -135 125 -65 {}
N 20 65 125 65 {}
N 125 65 125 135 {}
