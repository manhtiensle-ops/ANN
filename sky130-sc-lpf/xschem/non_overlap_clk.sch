v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
L 4 -620 -340 1280 -340 {dash=3}
L 4 1280 -340 1280 280 {dash=3}
L 4 1280 280 -620 280 {dash=3}
L 4 -620 280 -620 -340 {dash=3}
T {Block 1: 10 MHz Non-Overlapping Clock Generator (non_overlap_clk)} -580 -305 0 0 0.42 0.42 {font=Sans style=bold}
T {Cross-coupled NAND2 + 6-stage L=0.95 um delay chain -> t_nov = 2.92 ns (Gate: 2-5 ns)} -580 -262 0 0 0.28 0.28 {layer=4}
C {devices/iopin.sym} -530 -195 0 1 {name=p_vdd lab=VDD}
C {devices/iopin.sym} -530 -155 0 1 {name=p_vss lab=VSS}
C {devices/ipin.sym} -540 100 0 0 {name=p_clk lab=CLK}
C {inv_cell.sym} -400 100 0 0 {name=XINV0 WN=1.0 WP=2.5 LCH=0.15}
C {devices/lab_pin.sym} -400 36 0 0 {name=l_vdd0 lab=VDD}
C {devices/lab_pin.sym} -400 164 0 0 {name=l_vss0 lab=VSS}
C {nand2_cell.sym} -210 -130 0 0 {name=XNAND_A}
C {devices/lab_pin.sym} -210 -198 0 0 {name=lv_na lab=VDD}
C {devices/lab_pin.sym} -210 -62 0 0 {name=lg_na lab=VSS}
C {nand2_cell.sym} -210 130 0 0 {name=XNAND_B}
C {devices/lab_pin.sym} -210 62 0 0 {name=lv_nb lab=VDD}
C {devices/lab_pin.sym} -210 198 0 0 {name=lg_nb lab=VSS}
C {inv_cell.sym} -50 -130 0 0 {name=XDA1 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} -50 -194 0 0 {name=lv_da1 lab=VDD}
C {devices/lab_pin.sym} -50 -66 0 0 {name=lg_da1 lab=VSS}
C {inv_cell.sym} -50 130 0 0 {name=XDB1 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} -50 66 0 0 {name=lv_db1 lab=VDD}
C {devices/lab_pin.sym} -50 194 0 0 {name=lg_db1 lab=VSS}
C {inv_cell.sym} 100 -130 0 0 {name=XDA2 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 100 -194 0 0 {name=lv_da2 lab=VDD}
C {devices/lab_pin.sym} 100 -66 0 0 {name=lg_da2 lab=VSS}
C {inv_cell.sym} 100 130 0 0 {name=XDB2 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 100 66 0 0 {name=lv_db2 lab=VDD}
C {devices/lab_pin.sym} 100 194 0 0 {name=lg_db2 lab=VSS}
C {inv_cell.sym} 250 -130 0 0 {name=XDA3 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 250 -194 0 0 {name=lv_da3 lab=VDD}
C {devices/lab_pin.sym} 250 -66 0 0 {name=lg_da3 lab=VSS}
C {inv_cell.sym} 250 130 0 0 {name=XDB3 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 250 66 0 0 {name=lv_db3 lab=VDD}
C {devices/lab_pin.sym} 250 194 0 0 {name=lg_db3 lab=VSS}
C {inv_cell.sym} 400 -130 0 0 {name=XDA4 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 400 -194 0 0 {name=lv_da4 lab=VDD}
C {devices/lab_pin.sym} 400 -66 0 0 {name=lg_da4 lab=VSS}
C {inv_cell.sym} 400 130 0 0 {name=XDB4 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 400 66 0 0 {name=lv_db4 lab=VDD}
C {devices/lab_pin.sym} 400 194 0 0 {name=lg_db4 lab=VSS}
C {inv_cell.sym} 550 -130 0 0 {name=XDA5 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 550 -194 0 0 {name=lv_da5 lab=VDD}
C {devices/lab_pin.sym} 550 -66 0 0 {name=lg_da5 lab=VSS}
C {inv_cell.sym} 550 130 0 0 {name=XDB5 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 550 66 0 0 {name=lv_db5 lab=VDD}
C {devices/lab_pin.sym} 550 194 0 0 {name=lg_db5 lab=VSS}
C {inv_cell.sym} 700 -130 0 0 {name=XDA6 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 700 -194 0 0 {name=lv_da6 lab=VDD}
C {devices/lab_pin.sym} 700 -66 0 0 {name=lg_da6 lab=VSS}
C {inv_cell.sym} 700 130 0 0 {name=XDB6 WN=0.6 WP=1.5 LCH=0.95}
C {devices/lab_pin.sym} 700 66 0 0 {name=lv_db6 lab=VDD}
C {devices/lab_pin.sym} 700 194 0 0 {name=lg_db6 lab=VSS}
C {inv_cell.sym} 890 -130 0 0 {name=XBUF1A WN=2.0 WP=6.0 LCH=0.15}
C {devices/lab_pin.sym} 890 -194 0 0 {name=lv_b1a lab=VDD}
C {devices/lab_pin.sym} 890 -66 0 0 {name=lg_b1a lab=VSS}
C {devices/opin.sym} 1190 -215 0 0 {name=p_phi1 lab=PHI1}
C {inv_cell.sym} 1080 -130 0 0 {name=XBUF1B WN=2.0 WP=6.0 LCH=0.15}
C {devices/lab_pin.sym} 1080 -194 0 0 {name=lv_b1b lab=VDD}
C {devices/lab_pin.sym} 1080 -66 0 0 {name=lg_b1b lab=VSS}
C {devices/opin.sym} 1190 -130 0 0 {name=p_phi1b lab=PHI1_B}
C {inv_cell.sym} 890 130 0 0 {name=XBUF2A WN=2.0 WP=6.0 LCH=0.15}
C {devices/lab_pin.sym} 890 66 0 0 {name=lv_b2a lab=VDD}
C {devices/lab_pin.sym} 890 194 0 0 {name=lg_b2a lab=VSS}
C {devices/opin.sym} 1190 215 0 0 {name=p_phi2 lab=PHI2}
C {inv_cell.sym} 1080 130 0 0 {name=XBUF2B WN=2.0 WP=6.0 LCH=0.15}
C {devices/lab_pin.sym} 1080 66 0 0 {name=lv_b2b lab=VDD}
C {devices/lab_pin.sym} 1080 194 0 0 {name=lg_b2b lab=VSS}
C {devices/opin.sym} 1190 130 0 0 {name=p_phi2b lab=PHI2_B}
N -540 100 -500 100 {}
N -500 100 -468 100 {}
N -332 100 -300 100 {}
N -500 -150 -500 100 {}
N -500 -150 -285 -150 {}
N -300 100 -300 150 {}
N -300 150 -285 150 {}
N -135 -130 -118 -130 {}
N -135 130 -118 130 {}
N 18 -130 32 -130 {}
N 18 130 32 130 {}
N 168 -130 182 -130 {}
N 168 130 182 130 {}
N 318 -130 332 -130 {}
N 318 130 332 130 {}
N 468 -130 482 -130 {}
N 468 130 482 130 {}
N 618 -130 632 -130 {}
N 618 130 632 130 {}
N 768 -130 795 -130 {lab=FB1}
N 795 -130 822 -130 {}
N 795 -130 795 -20 {}
N -265 -20 795 -20 {}
N -265 -20 -265 110 {}
N -285 110 -265 110 {}
N 768 130 795 130 {lab=FB2}
N 795 130 822 130 {}
N 795 20 795 130 {}
N -245 20 795 20 {}
N -245 -110 -245 20 {}
N -285 -110 -245 -110 {}
N 958 -130 985 -130 {}
N 985 -130 1012 -130 {}
N 985 -215 985 -130 {}
N 985 -215 1190 -215 {lab=PHI1}
N 1148 -130 1190 -130 {lab=PHI1_B}
N 958 130 985 130 {}
N 985 130 1012 130 {}
N 985 130 985 215 {}
N 985 215 1190 215 {lab=PHI2}
N 1148 130 1190 130 {lab=PHI2_B}
