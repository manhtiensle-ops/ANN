#!/usr/bin/env python3
"""
Generate publication-grade, ERC-clean hierarchical Xschem (.sch & .sym) schematics
for sky130-sc-lpf and netlist them via `xschem -n -s -q` into `ngspice/`.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
XDIR = ROOT / "xschem"
NDIR = ROOT / "ngspice"

HEADER = """v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
"""


class SchBuilder:
    """Helper that stores wires & instances and automatically splits T-junctions at endpoints/pins."""

    def __init__(self) -> None:
        self.items: list[str] = [HEADER]
        self.wires: list[tuple[float, float, float, float, str]] = []
        self.points: set[tuple[float, float]] = set()

    def frame(self, x1: float, y1: float, x2: float, y2: float) -> None:
        """Subtle outer border frame so titles never touch PDF edge headers."""
        self.items.append(f"L 4 {x1:g} {y1:g} {x2:g} {y1:g} {{dash=3}}\n")
        self.items.append(f"L 4 {x2:g} {y1:g} {x2:g} {y2:g} {{dash=3}}\n")
        self.items.append(f"L 4 {x2:g} {y2:g} {x1:g} {y2:g} {{dash=3}}\n")
        self.items.append(f"L 4 {x1:g} {y2:g} {x1:g} {y1:g} {{dash=3}}\n")

    def title(self, txt: str, x: float, y: float, size: float = 0.36) -> None:
        self.items.append(f"T {{{txt}}} {x:g} {y:g} 0 0 {size} {size} {{font=Sans style=bold}}\n")

    def note(self, txt: str, x: float, y: float, size: float = 0.24) -> None:
        self.items.append(f"T {{{txt}}} {x:g} {y:g} 0 0 {size} {size} {{layer=4}}\n")

    def wire(self, x1: float, y1: float, x2: float, y2: float, lab: str = "") -> None:
        if (x1, y1) == (x2, y2):
            return
        self.wires.append((x1, y1, x2, y2, lab))
        self.points.add((x1, y1))
        self.points.add((x2, y2))

    def pin_point(self, x: float, y: float) -> None:
        self.points.add((x, y))

    def inst(self, sym: str, x: float, y: float, rot: int, flip: int, props: str, pins: list[tuple[float, float]] | None = None) -> None:
        self.items.append(f"C {{{sym}}} {x:g} {y:g} {rot} {flip} {{{props}}}\n")
        for px, py in (pins or [(x, y)]):
            self.points.add((px, py))

    def render(self) -> str:
        out = list(self.items)
        for x1, y1, x2, y2, lab in self.wires:
            prop = f"{{lab={lab}}}" if lab else "{}"
            if x1 == x2:
                ya, yb = (y1, y2) if y1 < y2 else (y2, y1)
                cuts = sorted({ya, yb} | {py for (px, py) in self.points if px == x1 and ya < py < yb})
                for k in range(len(cuts) - 1):
                    p = prop if k == 0 else "{}"
                    out.append(f"N {x1:g} {cuts[k]:g} {x2:g} {cuts[k+1]:g} {p}\n")
            elif y1 == y2:
                xa, xb = (x1, x2) if x1 < x2 else (x2, x1)
                cuts = sorted({xa, xb} | {px for (px, py) in self.points if py == y1 and xa < px < xb})
                for k in range(len(cuts) - 1):
                    p = prop if k == 0 else "{}"
                    out.append(f"N {cuts[k]:g} {y1:g} {cuts[k+1]:g} {y2:g} {p}\n")
            else:
                out.append(f"N {x1:g} {y1:g} {x2:g} {y2:g} {prop}\n")
        return "".join(out)


def make_inv_symbol() -> str:
    """Standard IEEE/ANSI NOT (Inverter) symbol preserving exact pin coordinates."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@A @@Y @@VDD @@VSS @symname WN=@WN WP=@WP LCH=@LCH"\ntemplate="name=X1 WN=1.0 WP=2.5 LCH=0.15"\n}\n',
        "V {}\nS {}\nE {}\n",
        # Triangle body: (-34, -30) -> (-34, 30) -> (22, 0) -> (-34, -30)
        "L 4 -34 -30 -34 30 {}\n",
        "L 4 -34 30 22 0 {}\n",
        "L 4 22 0 -34 -30 {}\n",
        # Output inversion bubble at (28, 0), r = 6
        "A 4 28 0 6 0 360 {}\n",
        # Pins & stubs (exact coordinates: A=(-68,0), Y=(68,0), VDD=(0,-64), VSS=(0,64))
        "L 4 -68 0 -34 0 {}\n",
        "B 5 -70.5 -2.5 -65.5 2.5 {name=A dir=in}\n",
        "L 4 34 0 68 0 {}\n",
        "B 5 65.5 -2.5 70.5 2.5 {name=Y dir=out}\n",
        "L 4 0 -64 0 -11.8 {}\n",
        "B 5 -2.5 -66.5 2.5 -61.5 {name=VDD dir=inout}\n",
        "L 4 0 11.8 0 64 {}\n",
        "B 5 -2.5 61.5 2.5 66.5 {name=VSS dir=inout}\n",
        # Clean labels avoiding wires
        "T {@name} 14 -34 0 0 0.17 0.17 {}\n",
        "T {NOT} -16 0 0 0 0.16 0.16 {hcenter=true vcenter=true layer=7}\n",
        "T {W=@WN / @WP} 14 20 0 0 0.12 0.12 {layer=13}\n",
        "T {L=@LCH} 14 34 0 0 0.12 0.12 {layer=13}\n",
        "T {VDD} -5 -52 0 1 0.13 0.13 {}\n",
        "T {VSS} -5 44 0 1 0.13 0.13 {}\n",
    ]
    return "".join(lines)


def _d_gate_arc_lines(cx: float, cy: float, r: float, n_seg: int = 24) -> list[str]:
    """Generate smooth semicircular right-hand D-body segments from top to bottom."""
    import math

    segs = []
    for i in range(n_seg):
        t0 = -math.pi / 2 + (math.pi * i) / n_seg
        t1 = -math.pi / 2 + (math.pi * (i + 1)) / n_seg
        x0, y0 = cx + r * math.cos(t0), cy + r * math.sin(t0)
        x1, y1 = cx + r * math.cos(t1), cy + r * math.sin(t1)
        segs.append(f"L 4 {x0:.2f} {y0:.2f} {x1:.2f} {y1:.2f} {{}}\n")
    return segs


def make_nand2_symbol() -> str:
    """Standard IEEE/ANSI 2-input NAND gate symbol preserving exact pin coordinates."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@A @@B @@Y @@VDD @@VSS @symname"\ntemplate="name=X1"\n}\n',
        "V {}\nS {}\nE {}\n",
        # D-shaped body: left x=-46, straight top/bottom to x=-6, arc r=36 centered (-6,0) -> apex (30,0)
        "L 4 -46 -36 -46 36 {}\n",
        "L 4 -46 -36 -6 -36 {}\n",
        "L 4 -46 36 -6 36 {}\n",
        *_d_gate_arc_lines(-6.0, 0.0, 36.0, n_seg=24),
        # Output inversion bubble at (36, 0), r = 6
        "A 4 36 0 6 0 360 {}\n",
        # Input pins A=(-75,-20), B=(-75,20)
        "L 4 -75 -20 -46 -20 {}\n",
        "B 5 -77.5 -22.5 -72.5 -17.5 {name=A dir=in}\n",
        "T {A} -40 -25 0 0 0.15 0.15 {}\n",
        "L 4 -75 20 -46 20 {}\n",
        "B 5 -77.5 17.5 -72.5 22.5 {name=B dir=in}\n",
        "T {B} -40 14 0 0 0.15 0.15 {}\n",
        # Output pin Y=(75,0)
        "L 4 42 0 75 0 {}\n",
        "B 5 72.5 -2.5 77.5 2.5 {name=Y dir=out}\n",
        # Power pins VDD=(0,-68), VSS=(0,68) touching D-arc at y = +/-35.5
        "L 4 0 -68 0 -35.5 {}\n",
        "B 5 -2.5 -70.5 2.5 -65.5 {name=VDD dir=inout}\n",
        "T {VDD} 5 -54 0 0 0.13 0.13 {}\n",
        "L 4 0 35.5 0 68 {}\n",
        "B 5 -2.5 65.5 2.5 70.5 {name=VSS dir=inout}\n",
        "T {VSS} 5 44 0 0 0.13 0.13 {}\n",
        # Designator & label
        "T {@name} 24 -46 0 0 0.18 0.18 {}\n",
        "T {NAND2} -12 0 0 0 0.17 0.17 {hcenter=true vcenter=true layer=7}\n",
    ]
    return "".join(lines)


def make_and2_symbol() -> str:
    """Standard IEEE/ANSI 2-input AND gate symbol."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@A @@B @@Y @@VDD @@VSS @symname"\ntemplate="name=X1"\n}\n',
        "V {}\nS {}\nE {}\n",
        "L 4 -46 -36 -46 36 {}\n",
        "L 4 -46 -36 -6 -36 {}\n",
        "L 4 -46 36 -6 36 {}\n",
        *_d_gate_arc_lines(-6.0, 0.0, 36.0, n_seg=24),
        "L 4 -75 -20 -46 -20 {}\n",
        "B 5 -77.5 -22.5 -72.5 -17.5 {name=A dir=in}\n",
        "T {A} -40 -25 0 0 0.15 0.15 {}\n",
        "L 4 -75 20 -46 20 {}\n",
        "B 5 -77.5 17.5 -72.5 22.5 {name=B dir=in}\n",
        "T {B} -40 14 0 0 0.15 0.15 {}\n",
        "L 4 30 0 75 0 {}\n",
        "B 5 72.5 -2.5 77.5 2.5 {name=Y dir=out}\n",
        "L 4 0 -68 0 -35.5 {}\n",
        "B 5 -2.5 -70.5 2.5 -65.5 {name=VDD dir=inout}\n",
        "T {VDD} 5 -54 0 0 0.13 0.13 {}\n",
        "L 4 0 35.5 0 68 {}\n",
        "B 5 -2.5 65.5 2.5 70.5 {name=VSS dir=inout}\n",
        "T {VSS} 5 44 0 0 0.13 0.13 {}\n",
        "T {@name} 24 -46 0 0 0.18 0.18 {}\n",
        "T {AND2} -12 0 0 0 0.18 0.18 {hcenter=true vcenter=true layer=7}\n",
    ]
    return "".join(lines)


def make_tg_symbol() -> str:
    """Standard IEEE CMOS Transmission Gate bow-tie symbol preserving exact pin coordinates."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@VIN @@VOUT @@PHI @@PHI_B @@VDD @@VSS @symname"\ntemplate="name=X1"\n}\n',
        "V {}\nS {}\nE {}\n",
        # Bow-tie: left triangle (-40,-24)->(-40,24)->(0,0), right triangle (40,-24)->(40,24)->(0,0)
        "L 4 -40 -24 -40 24 {}\n",
        "L 4 -40 24 0 0 {}\n",
        "L 4 0 0 -40 -24 {}\n",
        "L 4 40 -24 40 24 {}\n",
        "L 4 40 24 0 0 {}\n",
        "L 4 0 0 40 -24 {}\n",
        # Top PMOS control gate bar + inversion bubble at (0, -22)
        "L 4 -18 -16 18 -16 {}\n",
        "A 4 0 -22 6 0 360 {}\n",
        # Bottom NMOS control gate bar
        "L 4 -18 16 18 16 {}\n",
        # VIN=(-88,0), VOUT=(88,0)
        "L 4 -88 0 -40 0 {}\n",
        "B 5 -90.5 -2.5 -85.5 2.5 {name=VIN dir=inout}\n",
        "L 4 40 0 88 0 {}\n",
        "B 5 85.5 -2.5 90.5 2.5 {name=VOUT dir=inout}\n",
        # PHI_B=(-32,-68) -> (-32,-36) -> (0,-36) -> (0,-28)
        "L 4 -32 -68 -32 -36 {}\n",
        "L 4 -32 -36 0 -36 {}\n",
        "L 4 0 -36 0 -28 {}\n",
        "B 5 -34.5 -70.5 -29.5 -65.5 {name=PHI_B dir=in}\n",
        # PHI=(-32,68) -> (-32,36) -> (0,36) -> (0,16)
        "L 4 -32 68 -32 36 {}\n",
        "L 4 -32 36 0 36 {}\n",
        "L 4 0 36 0 16 {}\n",
        "B 5 -34.5 65.5 -29.5 70.5 {name=PHI dir=in}\n",
        # VDD=(32,-68) -> (32,-19.2), VSS=(32,68) -> (32,19.2)
        "L 4 32 -68 32 -19.2 {}\n",
        "B 5 29.5 -70.5 34.5 -65.5 {name=VDD dir=inout}\n",
        "L 4 32 19.2 32 68 {}\n",
        "B 5 29.5 65.5 34.5 70.5 {name=VSS dir=inout}\n",
        # Clean labels
        "T {@name} 46 -40 0 0 0.18 0.18 {}\n",
        "T {TG 2/6} 46 -22 0 0 0.15 0.15 {layer=7}\n",
    ]
    return "".join(lines)


def make_tg_dummy_symbol() -> str:
    """Standard IEEE Half-Sized Dummy CMOS Switch symbol (D=S shorted) preserving pins."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@VNODE @@G_N @@G_P @@VDD @@VSS @symname"\ntemplate="name=X1"\n}\n',
        "V {}\nS {}\nE {}\n",
        # Compact bow-tie [-32, +32] x [-20, +20]
        "L 4 -32 -20 -32 20 {}\n",
        "L 4 -32 20 0 0 {}\n",
        "L 4 0 0 -32 -20 {}\n",
        "L 4 32 -20 32 20 {}\n",
        "L 4 32 20 0 0 {}\n",
        "L 4 0 0 32 -20 {}\n",
        # Top PMOS gate + bubble, Bottom NMOS gate
        "L 4 -14 -14 14 -14 {}\n",
        "A 4 0 -19 5 0 360 {}\n",
        "L 4 -14 14 14 14 {}\n",
        # D=S shorting strap around bottom-right back to VNODE junction at (-48, 0)
        "L 4 -85 0 -32 0 {}\n",
        "L 4 32 0 46 0 {}\n",
        "L 4 46 0 46 -42 {}\n",
        "L 4 46 -42 -48 -42 {}\n",
        "L 4 -48 -42 -48 0 {}\n",
        "P 4 4 -50 -2 -46 -2 -46 2 -50 2 {fill=true}\n",
        "B 5 -87.5 -2.5 -82.5 2.5 {name=VNODE dir=inout}\n",
        # G_P=(-30,-64), VDD=(30,-64), G_N=(-30,64), VSS=(30,64)
        "L 4 -30 -64 -30 -32 {}\n",
        "L 4 -30 -32 0 -32 {}\n",
        "L 4 0 -32 0 -24 {}\n",
        "B 5 -32.5 -66.5 -27.5 -61.5 {name=G_P dir=in}\n",
        "L 4 30 -64 30 -18.8 {}\n",
        "B 5 27.5 -66.5 32.5 -61.5 {name=VDD dir=inout}\n",
        "L 4 -30 64 -30 32 {}\n",
        "L 4 -30 32 0 32 {}\n",
        "L 4 0 32 0 14 {}\n",
        "B 5 -32.5 61.5 -27.5 66.5 {name=G_N dir=in}\n",
        "L 4 30 18.8 30 64 {}\n",
        "B 5 27.5 61.5 32.5 66.5 {name=VSS dir=inout}\n",
        "T {@name} 52 -34 0 0 0.17 0.17 {}\n",
        "T {DUM W/2} 52 -16 0 0 0.14 0.14 {layer=7}\n",
        "T {D=S} 52 0 0 0 0.13 0.13 {layer=13}\n",
    ]
    return "".join(lines)


def make_ota_symbol() -> str:
    """Standard IEEE Operational Amplifier / OTA Triangle symbol preserving exact pin coordinates."""
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        'K {type=subcircuit\nformat="@name @@INP @@INN @@IBIAS @@VOUT @@VDD @@VSS @symname"\ntemplate="name=X1"\n}\n',
        "V {}\nS {}\nE {}\n",
        # Triangle: (-75, -70) -> (-75, 50) -> (75, -10) -> (-75, -70)
        "L 4 -75 -70 -75 50 {}\n",
        "L 4 -75 50 75 -10 {}\n",
        "L 4 75 -10 -75 -70 {}\n",
        # Plus (+) sign at (-62, -30) and Minus (-) sign at (-62, 10)
        "L 4 -67 -30 -57 -30 {}\n",
        "L 4 -62 -35 -62 -25 {}\n",
        "L 4 -67 10 -57 10 {}\n",
        # Input/Output/Bias horizontal stubs
        "L 4 -115 -30 -75 -30 {}\n",
        "B 5 -117.5 -32.5 -112.5 -27.5 {name=INP dir=in}\n",
        "L 4 -115 10 -75 10 {}\n",
        "B 5 -117.5 7.5 -112.5 12.5 {name=INN dir=in}\n",
        "L 4 -115 45 -75 45 {}\n",
        "B 5 -117.5 42.5 -112.5 47.5 {name=IBIAS dir=in}\n",
        "T {IB} -67 37 0 0 0.13 0.13 {}\n",
        "L 4 75 -10 115 -10 {}\n",
        "B 5 112.5 -12.5 117.5 -7.5 {name=VOUT dir=out}\n",
        # VDD=(0,-100) touches top edge at y=-40; VSS=(0,100) touches bottom edge at y=20
        "L 4 0 -100 0 -40 {}\n",
        "B 5 -2.5 -102.5 2.5 -97.5 {name=VDD dir=inout}\n",
        "T {VDD} 6 -82 0 0 0.14 0.14 {}\n",
        "L 4 0 20 0 100 {}\n",
        "B 5 -2.5 97.5 2.5 102.5 {name=VSS dir=inout}\n",
        "T {VSS} 6 66 0 0 0.14 0.14 {}\n",
        "T {@name} 38 -52 0 0 0.20 0.20 {}\n",
        "T {5T-OTA} -18 -14 0 0 0.19 0.19 {hcenter=true vcenter=true layer=7}\n",
        "T {BUFFER} -18 4 0 0 0.15 0.15 {hcenter=true vcenter=true layer=13}\n",
    ]
    return "".join(lines)


def make_box_symbol(
    title: str,
    left_pins: list[tuple[str, float, str]],
    right_pins: list[tuple[str, float, str]],
    top_pins: list[tuple[str, float, str]] | None = None,
    bot_pins: list[tuple[str, float, str]] | None = None,
    pin_order: list[str] | None = None,
    extra_params: str = "",
    w_half: float = 95,
    h_half: float = 80,
    stub_tb: float = 30,
) -> str:
    top_pins = top_pins or []
    bot_pins = bot_pins or []
    if pin_order is None:
        pin_order = [p[0] for p in left_pins + right_pins + top_pins + bot_pins]

    pinlist_fmt = " ".join(f"@@{p}" for p in pin_order)
    param_fmt = (" " + " ".join(f"{k}=@{k}" for k in [kv.split("=")[0] for kv in extra_params.split()])) if extra_params else ""
    tmpl = "name=X1" + (f" {extra_params}" if extra_params else "")

    title_y = -6 if extra_params else 0
    lines = [
        "v {xschem version=3.4.6 file_version=1.2}\n",
        "G {}\n",
        f'K {{type=subcircuit\nformat="@name {pinlist_fmt} @symname{param_fmt}"\ntemplate="{tmpl}"\n}}\n',
        "V {}\nS {}\nE {}\n",
        f"L 4 {-w_half:g} {-h_half:g} {w_half:g} {-h_half:g} {{}}\n",
        f"L 4 {w_half:g} {-h_half:g} {w_half:g} {h_half:g} {{}}\n",
        f"L 4 {w_half:g} {h_half:g} {-w_half:g} {h_half:g} {{}}\n",
        f"L 4 {-w_half:g} {h_half:g} {-w_half:g} {-h_half:g} {{}}\n",
        # Place @name cleanly at top-right of box so it never collides with top VDD pin
        f"T {{@name}} {w_half:g} {-h_half - 16:g} 0 1 0.20 0.20 {{}}\n",
        f"T {{{title}}} 0 {title_y:g} 0 0 0.21 0.21 {{hcenter=true vcenter=true layer=7}}\n",
    ]
    if extra_params:
        p_disp = " ".join(f"{kv.split('=')[0]}=@{kv.split('=')[0]}" for kv in extra_params.split())
        lines.append(f"T {{{p_disp}}} 0 {title_y + 16:g} 0 0 0.14 0.14 {{hcenter=true vcenter=true layer=13}}\n")

    stub_lr = 20
    for pname, py, pdir in left_pins:
        px = -w_half - stub_lr
        lines.append(f"L 4 {px:g} {py:g} {-w_half:g} {py:g} {{}}\n")
        lines.append(f"B 5 {px - 2.5:g} {py - 2.5:g} {px + 2.5:g} {py + 2.5:g} {{name={pname} dir={pdir}}}\n")
        lines.append(f"T {{{pname}}} {-w_half + 6:g} {py - 5:g} 0 0 0.17 0.17 {{}}\n")

    for pname, py, pdir in right_pins:
        px = w_half + stub_lr
        lines.append(f"L 4 {w_half:g} {py:g} {px:g} {py:g} {{}}\n")
        lines.append(f"B 5 {px - 2.5:g} {py - 2.5:g} {px + 2.5:g} {py + 2.5:g} {{name={pname} dir={pdir}}}\n")
        lines.append(f"T {{{pname}}} {w_half - 6:g} {py - 5:g} 0 1 0.17 0.17 {{}}\n")

    for pname, px, pdir in top_pins:
        py = -h_half - stub_tb
        lines.append(f"L 4 {px:g} {py:g} {px:g} {-h_half:g} {{}}\n")
        lines.append(f"B 5 {px - 2.5:g} {py - 2.5:g} {px + 2.5:g} {py + 2.5:g} {{name={pname} dir={pdir}}}\n")
        lines.append(f"T {{{pname}}} {px:g} {-h_half + 6:g} 0 0 0.15 0.15 {{hcenter=true}}\n")

    for pname, px, pdir in bot_pins:
        py = h_half + stub_tb
        lines.append(f"L 4 {px:g} {h_half:g} {px:g} {py:g} {{}}\n")
        lines.append(f"B 5 {px - 2.5:g} {py - 2.5:g} {px + 2.5:g} {py + 2.5:g} {{name={pname} dir={pdir}}}\n")
        lines.append(f"T {{{pname}}} {px:g} {h_half - 16:g} 0 0 0.15 0.15 {{hcenter=true}}\n")

    return "".join(lines)


def fet_pins(x: float, y: float, flip: int = 0) -> list[tuple[float, float]]:
    s = -1 if flip else 1
    return [(x + s * 20, y - 30), (x - s * 20, y), (x + s * 20, y + 30), (x + s * 20, y)]


# ---------------------------------------------------------------------------
# 1. inv_cell
# ---------------------------------------------------------------------------
def build_inv_cell() -> None:
    b = SchBuilder()
    b.frame(-220, -240, 220, 200)
    b.title("Parameterized CMOS Inverter (inv_cell)", -195, -215, 0.30)
    b.inst(
        "sky130_fd_pr/pfet_01v8.sym", 0, -70, 0, 0,
        "name=MP model=pfet_01v8 W='WP' L='LCH' nf=1 mult=1 ad='WP*0.29' as='WP*0.29' pd='2*(WP+0.29)' ps='2*(WP+0.29)' nrd='0.29/WP' nrs='0.29/WP'",
        fet_pins(0, -70),
    )
    b.inst(
        "sky130_fd_pr/nfet_01v8.sym", 0, 70, 0, 0,
        "name=MN model=nfet_01v8 W='WN' L='LCH' nf=1 mult=1 ad='WN*0.29' as='WN*0.29' pd='2*(WN+0.29)' ps='2*(WN+0.29)' nrd='0.29/WN' nrs='0.29/WN'",
        fet_pins(0, 70),
    )
    b.wire(-20, -70, -20, 70)
    b.wire(-100, 0, -20, 0)
    b.inst("devices/ipin.sym", -100, 0, 0, 0, "name=p1 lab=A")
    b.wire(20, -40, 20, 40)
    b.wire(20, 0, 130, 0)
    b.inst("devices/opin.sym", 130, 0, 0, 0, "name=p2 lab=Y")
    b.wire(20, -140, 20, -100)
    b.wire(20, -70, 50, -70)
    b.wire(50, -140, 50, -70)
    b.wire(20, -140, 50, -140)
    b.inst("devices/iopin.sym", 20, -140, 0, 1, "name=p3 lab=VDD")
    b.wire(20, 100, 20, 140)
    b.wire(20, 70, 50, 70)
    b.wire(50, 70, 50, 140)
    b.wire(20, 140, 50, 140)
    b.inst("devices/iopin.sym", 20, 140, 0, 1, "name=p4 lab=VSS")

    (XDIR / "inv_cell.sch").write_text(b.render())
    (XDIR / "inv_cell.sym").write_text(make_inv_symbol())


# ---------------------------------------------------------------------------
# 2. nand2_cell
# ---------------------------------------------------------------------------
def build_nand2_cell() -> None:
    b = SchBuilder()
    b.frame(-260, -260, 260, 230)
    b.title("2-Input CMOS NAND Gate (nand2_cell)", -235, -235, 0.30)
    b.inst("sky130_fd_pr/pfet_01v8.sym", -80, -110, 0, 0, "name=MPA model=pfet_01v8 W=2.0 L=0.15 nf=1 mult=1", fet_pins(-80, -110))
    b.inst("sky130_fd_pr/pfet_01v8.sym", 60, -110, 0, 0, "name=MPB model=pfet_01v8 W=2.0 L=0.15 nf=1 mult=1", fet_pins(60, -110))
    b.inst("sky130_fd_pr/nfet_01v8.sym", 60, 20, 0, 0, "name=MNA model=nfet_01v8 W=1.6 L=0.15 nf=1 mult=1", fet_pins(60, 20))
    b.inst("sky130_fd_pr/nfet_01v8.sym", 60, 120, 0, 0, "name=MNB model=nfet_01v8 W=1.6 L=0.15 nf=1 mult=1", fet_pins(60, 120))

    b.wire(-60, -180, 120, -180)
    b.wire(-60, -180, -60, -140)
    b.wire(80, -180, 80, -140)
    b.wire(-60, -110, -30, -110)
    b.wire(-30, -180, -30, -110)
    b.wire(80, -110, 120, -110)
    b.wire(120, -180, 120, -110)
    b.inst("devices/iopin.sym", -60, -180, 0, 1, "name=p3 lab=VDD")

    b.pin_point(80, -50)
    b.wire(-60, -80, -60, -50)
    b.wire(80, -80, 80, -50)
    b.wire(80, -50, 80, -10)
    b.wire(-60, -50, 180, -50)
    b.inst("devices/opin.sym", 180, -50, 0, 0, "name=p5 lab=Y")

    b.wire(80, 50, 80, 90)

    b.wire(80, 150, 80, 190)
    b.wire(80, 20, 130, 20)
    b.wire(80, 120, 130, 120)
    b.wire(130, 20, 130, 190)
    b.wire(80, 190, 130, 190)
    b.inst("devices/iopin.sym", 80, 190, 0, 1, "name=p4 lab=VSS")

    b.wire(-180, 20, 40, 20)
    b.wire(-140, -110, -100, -110)
    b.wire(-140, -110, -140, 20)
    b.inst("devices/ipin.sym", -180, 20, 0, 0, "name=p1 lab=A")
    b.wire(-180, 120, 40, 120)
    b.wire(10, -110, 40, -110)
    b.wire(10, -110, 10, 120)
    b.inst("devices/ipin.sym", -180, 120, 0, 0, "name=p2 lab=B")

    (XDIR / "nand2_cell.sch").write_text(b.render())
    (XDIR / "nand2_cell.sym").write_text(make_nand2_symbol())


# ---------------------------------------------------------------------------
# 2b. and2_cell (NAND2 + NOT -> IEEE AND2)
# ---------------------------------------------------------------------------
def build_and2_cell() -> None:
    b = SchBuilder()
    b.frame(-300, -180, 300, 150)
    b.title("2-Input CMOS AND Gate (and2_cell = NAND2 + NOT)", -275, -155, 0.28)
    b.inst("devices/iopin.sym", -240, -100, 0, 1, "name=p_vdd lab=VDD")
    b.inst("devices/iopin.sym", -240, -65, 0, 1, "name=p_vss lab=VSS")

    b.inst("devices/ipin.sym", -240, -20, 0, 0, "name=p1 lab=A")
    b.wire(-240, -20, -155, -20)
    b.inst("devices/ipin.sym", -240, 20, 0, 0, "name=p2 lab=B")
    b.wire(-240, 20, -155, 20)

    b.inst("nand2_cell.sym", -80, 0, 0, 0, "name=XNAND", [(-155, -20), (-155, 20), (-5, 0), (-80, -68), (-80, 68)])
    b.inst("devices/lab_pin.sym", -80, -68, 0, 0, "name=lv_n lab=VDD")
    b.inst("devices/lab_pin.sym", -80, 68, 0, 0, "name=lg_n lab=VSS")

    b.wire(-5, 0, 42, 0, "Y_B")
    b.inst("inv_cell.sym", 110, 0, 0, 0, "name=XINV WN=1.0 WP=2.5 LCH=0.15", [(42, 0), (178, 0), (110, -64), (110, 64)])
    b.inst("devices/lab_pin.sym", 110, -64, 0, 0, "name=lv_i lab=VDD")
    b.inst("devices/lab_pin.sym", 110, 64, 0, 0, "name=lg_i lab=VSS")

    b.wire(178, 0, 240, 0)
    b.inst("devices/opin.sym", 240, 0, 0, 0, "name=p3 lab=Y")

    (XDIR / "and2_cell.sch").write_text(b.render())
    (XDIR / "and2_cell.sym").write_text(make_and2_symbol())


# ---------------------------------------------------------------------------
# 3. Block 1 — non_overlap_clk
# ---------------------------------------------------------------------------
def build_non_overlap_clk() -> None:
    b = SchBuilder()
    b.frame(-620, -340, 1280, 280)
    b.title("Block 1: 10 MHz Non-Overlapping Clock Generator (non_overlap_clk)", -580, -305, 0.42)
    b.note("Cross-coupled NAND2 + 6-stage L=0.95 um delay chain -> t_nov = 2.92 ns (Gate: 2-5 ns)", -580, -262, 0.28)
    b.inst("devices/iopin.sym", -530, -195, 0, 1, "name=p_vdd lab=VDD")
    b.inst("devices/iopin.sym", -530, -155, 0, 1, "name=p_vss lab=VSS")

    # Input CLK & XINV0 at (-400, 100): A=(-468,100), Y=(-332,100), VDD=(-400,36), VSS=(-400,164)
    b.inst("devices/ipin.sym", -540, 100, 0, 0, "name=p_clk lab=CLK")
    b.wire(-540, 100, -468, 100)
    b.inst("inv_cell.sym", -400, 100, 0, 0, "name=XINV0 WN=1.0 WP=2.5 LCH=0.15", [(-468, 100), (-332, 100), (-400, 36), (-400, 164)])
    b.inst("devices/lab_pin.sym", -400, 36, 0, 0, "name=l_vdd0 lab=VDD")
    b.inst("devices/lab_pin.sym", -400, 164, 0, 0, "name=l_vss0 lab=VSS")
    b.wire(-332, 100, -300, 100)

    b.wire(-500, -150, -500, 100)
    b.wire(-500, -150, -285, -150)
    b.wire(-300, 100, -300, 150)
    b.wire(-300, 150, -285, 150)

    # XNAND_A at (-210, -130): A=(-285,-150), B=(-285,-110), Y=(-135,-130), VDD=(-210,-198), VSS=(-210,-62)
    b.inst("nand2_cell.sym", -210, -130, 0, 0, "name=XNAND_A", [(-285, -150), (-285, -110), (-135, -130), (-210, -198), (-210, -62)])
    b.inst("devices/lab_pin.sym", -210, -198, 0, 0, "name=lv_na lab=VDD")
    b.inst("devices/lab_pin.sym", -210, -62, 0, 0, "name=lg_na lab=VSS")

    # XNAND_B at (-210, 130): A=(-285,110), B=(-285,150), Y=(-135,130), VDD=(-210,62), VSS=(-210,198)
    b.inst("nand2_cell.sym", -210, 130, 0, 0, "name=XNAND_B", [(-285, 110), (-285, 150), (-135, 130), (-210, 62), (-210, 198)])
    b.inst("devices/lab_pin.sym", -210, 62, 0, 0, "name=lv_nb lab=VDD")
    b.inst("devices/lab_pin.sym", -210, 198, 0, 0, "name=lg_nb lab=VSS")

    # 6 delay inverters spaced by 150 units: inv_cell has w_half=48 + stub=20 = 68, h_half=38 + stub=26 = 64
    xs_del = [-50, 100, 250, 400, 550, 700]
    b.wire(-135, -130, -118, -130)
    b.wire(-135, 130, -118, 130)
    for i, cx in enumerate(xs_del, start=1):
        b.inst("inv_cell.sym", cx, -130, 0, 0, f"name=XDA{i} WN=0.6 WP=1.5 LCH=0.95", [(cx - 68, -130), (cx + 68, -130), (cx, -194), (cx, -66)])
        b.inst("devices/lab_pin.sym", cx, -194, 0, 0, f"name=lv_da{i} lab=VDD")
        b.inst("devices/lab_pin.sym", cx, -66, 0, 0, f"name=lg_da{i} lab=VSS")
        b.inst("inv_cell.sym", cx, 130, 0, 0, f"name=XDB{i} WN=0.6 WP=1.5 LCH=0.95", [(cx - 68, 130), (cx + 68, 130), (cx, 66), (cx, 194)])
        b.inst("devices/lab_pin.sym", cx, 66, 0, 0, f"name=lv_db{i} lab=VDD")
        b.inst("devices/lab_pin.sym", cx, 194, 0, 0, f"name=lg_db{i} lab=VSS")
        if i < len(xs_del):
            b.wire(cx + 68, -130, xs_del[i] - 68, -130)
            b.wire(cx + 68, 130, xs_del[i] - 68, 130)

    # Cross-coupled feedbacks FB1 and FB2
    b.wire(768, -130, 822, -130, "FB1")
    b.wire(795, -130, 795, -20)
    b.wire(-265, -20, 795, -20)
    b.wire(-265, -20, -265, 110)
    b.wire(-285, 110, -265, 110)

    b.wire(768, 130, 822, 130, "FB2")
    b.wire(795, 20, 795, 130)
    b.wire(-245, 20, 795, 20)
    b.wire(-245, -110, -245, 20)
    b.wire(-285, -110, -245, -110)

    # Output buffers XBUF1A (890,-130), XBUF1B (1080,-130)
    b.inst("inv_cell.sym", 890, -130, 0, 0, "name=XBUF1A WN=2.0 WP=6.0 LCH=0.15", [(822, -130), (958, -130), (890, -194), (890, -66)])
    b.inst("devices/lab_pin.sym", 890, -194, 0, 0, "name=lv_b1a lab=VDD")
    b.inst("devices/lab_pin.sym", 890, -66, 0, 0, "name=lg_b1a lab=VSS")
    b.wire(958, -130, 1012, -130)
    b.wire(985, -215, 985, -130)
    b.wire(985, -215, 1190, -215, "PHI1")
    b.inst("devices/opin.sym", 1190, -215, 0, 0, "name=p_phi1 lab=PHI1")

    b.inst("inv_cell.sym", 1080, -130, 0, 0, "name=XBUF1B WN=2.0 WP=6.0 LCH=0.15", [(1012, -130), (1148, -130), (1080, -194), (1080, -66)])
    b.inst("devices/lab_pin.sym", 1080, -194, 0, 0, "name=lv_b1b lab=VDD")
    b.inst("devices/lab_pin.sym", 1080, -66, 0, 0, "name=lg_b1b lab=VSS")
    b.wire(1148, -130, 1190, -130, "PHI1_B")
    b.inst("devices/opin.sym", 1190, -130, 0, 0, "name=p_phi1b lab=PHI1_B")

    b.inst("inv_cell.sym", 890, 130, 0, 0, "name=XBUF2A WN=2.0 WP=6.0 LCH=0.15", [(822, 130), (958, 130), (890, 66), (890, 194)])
    b.inst("devices/lab_pin.sym", 890, 66, 0, 0, "name=lv_b2a lab=VDD")
    b.inst("devices/lab_pin.sym", 890, 194, 0, 0, "name=lg_b2a lab=VSS")
    b.wire(958, 130, 1012, 130)
    b.wire(985, 130, 985, 215)
    b.wire(985, 215, 1190, 215, "PHI2")
    b.inst("devices/opin.sym", 1190, 215, 0, 0, "name=p_phi2 lab=PHI2")

    b.inst("inv_cell.sym", 1080, 130, 0, 0, "name=XBUF2B WN=2.0 WP=6.0 LCH=0.15", [(1012, 130), (1148, 130), (1080, 66), (1080, 194)])
    b.inst("devices/lab_pin.sym", 1080, 66, 0, 0, "name=lv_b2b lab=VDD")
    b.inst("devices/lab_pin.sym", 1080, 194, 0, 0, "name=lg_b2b lab=VSS")
    b.wire(1148, 130, 1190, 130, "PHI2_B")
    b.inst("devices/opin.sym", 1190, 130, 0, 0, "name=p_phi2b lab=PHI2_B")

    (XDIR / "non_overlap_clk.sch").write_text(b.render())
    (XDIR / "non_overlap_clk.sym").write_text(
        make_box_symbol(
            "NON-OVERLAP CLK",
            left_pins=[("CLK", 0, "in")],
            right_pins=[("PHI1", -45, "out"), ("PHI1_B", -15, "out"), ("PHI2", 15, "out"), ("PHI2_B", 45, "out")],
            top_pins=[("VDD", 0, "inout")],
            bot_pins=[("VSS", 0, "inout")],
            pin_order=["CLK", "PHI1", "PHI1_B", "PHI2", "PHI2_B", "VDD", "VSS"],
            w_half=115,
            h_half=75,
            stub_tb=30,
        )
    )


# ---------------------------------------------------------------------------
# 4. Block 2 — tg_switch & tg_dummy
# ---------------------------------------------------------------------------
def build_tg_switch() -> None:
    b = SchBuilder()
    b.frame(-290, -255, 310, 205)
    b.title("Block 2: CMOS Transmission Gate Switch (tg_switch)", -265, -225, 0.32)
    b.note("Optimized Wn = 2.0 um (nf=1), Wp = 6.0 um (nf=2), L = 0.15 um -> Ron < 4.7 kOhm, Low C_par", -265, -192, 0.21)

    b.inst("sky130_fd_pr/pfet_01v8.sym", 0, -75, 0, 0, "name=MP model=pfet_01v8 W=6.0 L=0.15 nf=2 mult=1", fet_pins(0, -75))
    b.inst("sky130_fd_pr/nfet_01v8.sym", 0, 75, 0, 0, "name=MN model=nfet_01v8 W=2.0 L=0.15 nf=1 mult=1", fet_pins(0, 75))

    # Left iopin with flip=1 so label VIN sits cleanly to the LEFT of the pin!
    b.inst("devices/iopin.sym", -180, 0, 0, 1, "name=p_vin lab=VIN")
    b.wire(-180, 0, -100, 0)
    b.wire(-100, -130, -100, 130)
    b.wire(-100, -130, 20, -130)
    b.wire(20, -130, 20, -105)
    b.wire(-100, 130, 20, 130)
    b.wire(20, 105, 20, 130)

    b.wire(20, -45, 20, 45)
    b.wire(20, 0, 210, 0)
    b.inst("devices/iopin.sym", 210, 0, 0, 0, "name=p_vout lab=VOUT")

    b.wire(-180, -75, -20, -75)
    b.inst("devices/ipin.sym", -180, -75, 0, 0, "name=p_phib lab=PHI_B")
    b.wire(-180, 75, -20, 75)
    b.inst("devices/ipin.sym", -180, 75, 0, 0, "name=p_phi lab=PHI")

    b.wire(20, -75, 145, -75)
    b.wire(145, -145, 145, -75)
    b.inst("devices/iopin.sym", 145, -145, 0, 0, "name=p_vdd lab=VDD")
    b.wire(20, 75, 145, 75)
    b.wire(145, 75, 145, 155)
    b.inst("devices/iopin.sym", 145, 155, 0, 0, "name=p_vss lab=VSS")

    (XDIR / "tg_switch.sch").write_text(b.render())
    (XDIR / "tg_switch.sym").write_text(make_tg_symbol())

    d = SchBuilder()
    d.frame(-260, -230, 260, 190)
    d.title("Half-Sized CMOS Dummy Switch (tg_dummy: 1.0 / 3.0 um)", -235, -205, 0.28)
    d.inst("sky130_fd_pr/pfet_01v8.sym", 0, -65, 0, 0, "name=MPD model=pfet_01v8 W=3.0 L=0.15 nf=1 mult=1", fet_pins(0, -65))
    d.inst("sky130_fd_pr/nfet_01v8.sym", 0, 65, 0, 0, "name=MND model=nfet_01v8 W=1.0 L=0.15 nf=1 mult=1", fet_pins(0, 65))
    d.wire(20, -95, 70, -95)
    d.wire(20, -35, 70, -35)
    d.wire(20, 35, 70, 35)
    d.wire(20, 95, 70, 95)
    d.wire(70, -95, 70, 95)
    d.wire(70, 0, 160, 0)
    d.inst("devices/iopin.sym", 160, 0, 0, 0, "name=p_vn lab=VNODE")
    d.wire(-140, -65, -20, -65)
    d.inst("devices/ipin.sym", -140, -65, 0, 0, "name=p_gp lab=G_P")
    d.wire(-140, 65, -20, 65)
    d.inst("devices/ipin.sym", -140, 65, 0, 0, "name=p_gn lab=G_N")
    d.wire(20, -65, 125, -65)
    d.wire(125, -135, 125, -65)
    d.inst("devices/iopin.sym", 125, -135, 0, 0, "name=p_vdd lab=VDD")
    d.wire(20, 65, 125, 65)
    d.wire(125, 65, 125, 135)
    d.inst("devices/iopin.sym", 125, 135, 0, 0, "name=p_vss lab=VSS")

    (XDIR / "tg_dummy.sch").write_text(d.render())
    (XDIR / "tg_dummy.sym").write_text(make_tg_dummy_symbol())


# ---------------------------------------------------------------------------
# 5. Block 3 — sc_core
# ---------------------------------------------------------------------------
def build_sc_core() -> None:
    b = SchBuilder()
    b.frame(-520, -300, 560, 250)
    b.title("Block 3: Switched-Capacitor MIM Filter Core (sc_core)", -490, -268, 0.38)
    b.note("C1 = 100 fF (1x 4.85x9.85 um MIM) | C2 = 800 fF (8x unit MIM) | W/2 Dummy Charge Cancellation", -490, -230, 0.25)

    # Supply & clock port bank on far left
    b.inst("devices/iopin.sym", -430, -165, 0, 1, "name=p_vdd lab=VDD")
    b.inst("devices/iopin.sym", -430, -125, 0, 1, "name=p_vss lab=VSS")
    for idx, (pname, py) in enumerate([("PHI1", 75), ("PHI1_B", 115), ("PHI2", 155), ("PHI2_B", 195)]):
        b.inst("devices/ipin.sym", -430, py, 0, 0, f"name=p_clk{idx} lab={pname}")
        b.wire(-430, py, -385, py, pname)

    # XTG1 at (-210, -10): w_half=68+20=88, h_half=40+28=68 -> VIN=(-298,-10), VOUT=(-122,-10), top=(-242/-178, -78), bot=(-242/-178, 58)
    b.inst("devices/ipin.sym", -380, -10, 0, 0, "name=p_vin lab=VIN")
    b.wire(-380, -10, -298, -10)
    b.inst("tg_switch.sym", -210, -10, 0, 0, "name=XTG1", [(-298, -10), (-122, -10), (-242, -78), (-178, -78), (-242, 58), (-178, 58)])
    b.inst("devices/lab_pin.sym", -242, -78, 0, 0, "name=l_tg1_pb lab=PHI1_B")
    b.inst("devices/lab_pin.sym", -178, -78, 0, 1, "name=l_tg1_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", -242, 58, 0, 0, "name=l_tg1_p lab=PHI1")
    b.inst("devices/lab_pin.sym", -178, 58, 0, 1, "name=l_tg1_vss lab=VSS")

    # Node V1 -> XC1 at (-20, 115) (NO dummy on V1 to preserve exact C1 = 100 fF!)
    b.wire(-122, -10, 82, -10, "V1")
    b.wire(-20, -10, -20, 85)
    b.inst("sky130_fd_pr/cap_mim_m3_1.sym", -20, 115, 0, 0, "name=C1 model=cap_mim_m3_1 W=4.85 L=9.85 MF=1", [(-20, 85), (-20, 145)])
    b.wire(-20, 145, -20, 195)
    b.inst("devices/lab_pin.sym", -20, 195, 0, 0, "name=l_c1_vss lab=VSS")

    # XTG2 at (170, -10): VIN=(82,-10), VOUT=(258,-10), top=(138/202, -78), bot=(138/202, 58)
    b.inst("tg_switch.sym", 170, -10, 0, 0, "name=XTG2", [(82, -10), (258, -10), (138, -78), (202, -78), (138, 58), (202, 58)])
    b.inst("devices/lab_pin.sym", 138, -78, 0, 0, "name=l_tg2_pb lab=PHI2_B")
    b.inst("devices/lab_pin.sym", 202, -78, 0, 1, "name=l_tg2_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", 138, 58, 0, 0, "name=l_tg2_p lab=PHI2")
    b.inst("devices/lab_pin.sym", 202, 58, 0, 1, "name=l_tg2_vss lab=VSS")

    # Node VX -> XC2 at (320, 115) & XDUM2 at (380, -130): VNODE=(295,-130), top=(350/410,-194), bot=(350/410,-66)
    b.wire(258, -10, 490, -10, "VX")
    b.wire(320, -10, 320, 85)
    b.inst("sky130_fd_pr/cap_mim_m3_1.sym", 320, 115, 0, 0, "name=C2 model=cap_mim_m3_1 W=4.85 L=9.85 MF=8", [(320, 85), (320, 145)])
    b.wire(320, 145, 320, 195)
    b.inst("devices/lab_pin.sym", 320, 195, 0, 0, "name=l_c2_vss lab=VSS")

    b.wire(280, -130, 280, -10)
    b.wire(280, -130, 295, -130)
    b.inst("tg_dummy.sym", 380, -130, 0, 0, "name=XDUM2", [(295, -130), (350, -194), (410, -194), (350, -66), (410, -66)])
    b.inst("devices/lab_pin.sym", 350, -194, 0, 0, "name=l_d2_gp lab=PHI2")
    b.inst("devices/lab_pin.sym", 410, -194, 0, 1, "name=l_d2_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", 350, -66, 0, 0, "name=l_d2_gn lab=PHI2_B")
    b.inst("devices/lab_pin.sym", 410, -66, 0, 1, "name=l_d2_vss lab=VSS")

    b.inst("devices/opin.sym", 490, -10, 0, 0, "name=p_vx lab=VX")

    (XDIR / "sc_core.sch").write_text(b.render())
    (XDIR / "sc_core.sym").write_text(
        make_box_symbol(
            "SC MIM CORE (1:8)",
            left_pins=[("VIN", -35, "in"), ("PHI1", -5, "in"), ("PHI1_B", 18, "in"), ("PHI2", 41, "in"), ("PHI2_B", 64, "in")],
            right_pins=[("VX", -35, "out")],
            top_pins=[("VDD", 0, "inout")],
            bot_pins=[("VSS", 0, "inout")],
            pin_order=["VIN", "VX", "PHI1", "PHI1_B", "PHI2", "PHI2_B", "VDD", "VSS"],
            w_half=105,
            h_half=85,
            stub_tb=30,
        )
    )


# ---------------------------------------------------------------------------
# 6. Block 4 — ota_5t
# ---------------------------------------------------------------------------
def build_ota_5t() -> None:
    b = SchBuilder()
    b.frame(-390, -280, 380, 260)
    b.title("Block 4: 5T-OTA Operational Transconductance Amplifier (ota_5t)", -365, -248, 0.34)
    b.note("A_OL = 41.62 dB | GBW = 43.91 MHz | PM = 81.27 deg (CL = 1 pF, I_ref = 30 uA)", -365, -214, 0.23)

    b.inst("sky130_fd_pr/pfet_01v8.sym", -110, -110, 0, 1, "name=M3 model=pfet_01v8 W=16.0 L=0.80 nf=4 mult=1", fet_pins(-110, -110, flip=1))
    b.inst("sky130_fd_pr/pfet_01v8.sym", 110, -110, 0, 0, "name=M4 model=pfet_01v8 W=16.0 L=0.80 nf=4 mult=1", fet_pins(110, -110, flip=0))
    b.wire(-185, -175, 185, -175)
    b.wire(-130, -175, -130, -140)
    b.wire(130, -175, 130, -140)
    b.wire(-185, -175, -185, -110)
    b.wire(-185, -110, -130, -110)
    b.wire(185, -175, 185, -110)
    b.wire(130, -110, 185, -110)
    b.inst("devices/iopin.sym", 0, -175, 0, 0, "name=p_vdd lab=VDD")

    b.wire(-90, -110, 90, -110)
    b.wire(-60, -110, -60, -60)
    b.wire(-130, -60, -60, -60)

    # M1 at (-150, 10) -> D=(-130,-20), G=(-170,10), S=(-130,40), B=(-130,10)
    # M2 at (150, 10, flip=1) -> D=(130,-20), G=(170,10), S=(130,40), B=(130,10)
    b.inst("sky130_fd_pr/nfet_01v8.sym", -150, 10, 0, 0, "name=M1 model=nfet_01v8 W=32.0 L=0.80 nf=8 mult=1", fet_pins(-150, 10, flip=0))
    b.inst("sky130_fd_pr/nfet_01v8.sym", 150, 10, 0, 1, "name=M2 model=nfet_01v8 W=32.0 L=0.80 nf=8 mult=1", fet_pins(150, 10, flip=1))
    b.wire(-130, -80, -130, -20, "VD1")
    b.wire(130, -80, 130, -20)
    b.wire(130, -50, 290, -50)
    b.inst("devices/opin.sym", 290, -50, 0, 0, "name=p_vout lab=VOUT")

    b.wire(-250, 10, -170, 10)
    b.inst("devices/ipin.sym", -250, 10, 0, 0, "name=p_inp lab=INP")
    b.wire(170, 10, 250, 10)
    b.inst("devices/ipin.sym", 250, 10, 0, 1, "name=p_inn lab=INN")

    # Join M1.B (-130,10) and M2.B (130,10) at center (0, -25) with a single clean VSS label in open space!
    b.wire(-130, 10, 130, 10)
    b.wire(0, -30, 0, 10)
    b.inst("devices/lab_pin.sym", 0, -30, 0, 0, "name=l_b12 lab=VSS")

    # Common Tail Node VTAIL at y = 85 & Tail Sink M5 + Bias Mirror M6
    b.wire(-130, 40, -130, 85)
    b.wire(130, 40, 130, 85)
    b.wire(-130, 85, 130, 85, "VTAIL")
    b.wire(0, 85, 0, 120)

    b.inst("sky130_fd_pr/nfet_01v8.sym", -20, 150, 0, 0, "name=M5 model=nfet_01v8 W=24.0 L=1.00 nf=6 mult=1", fet_pins(-20, 150, flip=0))
    b.inst("sky130_fd_pr/nfet_01v8.sym", -260, 150, 0, 1, "name=M6 model=nfet_01v8 W=24.0 L=1.00 nf=6 mult=1", fet_pins(-260, 150, flip=1))

    b.inst("devices/ipin.sym", -280, 65, 0, 0, "name=p_ib lab=IBIAS")
    b.wire(-280, 65, -280, 120)
    b.wire(-280, 100, -210, 100)
    b.wire(-210, 100, -210, 150)
    b.wire(-240, 150, -40, 150, "VBIAS")

    b.wire(-330, 220, 75, 220)
    b.wire(-280, 180, -280, 220)
    b.wire(0, 180, 0, 220)
    b.wire(-330, 150, -280, 150)
    b.wire(-330, 150, -330, 220)
    b.wire(0, 150, 75, 150)
    b.wire(75, 150, 75, 220)
    b.inst("devices/iopin.sym", 0, 220, 0, 0, "name=p_vss lab=VSS")

    (XDIR / "ota_5t.sch").write_text(b.render())
    (XDIR / "ota_5t.sym").write_text(make_ota_symbol())


# ---------------------------------------------------------------------------
# 7. Top-Level Circuit — top_sc_lpf
# ---------------------------------------------------------------------------
def build_top_sc_lpf() -> None:
    b = SchBuilder()
    b.frame(-580, -260, 660, 220)
    b.title("Top-Level Switched-Capacitor Low-Pass Filter (top_sc_lpf -- SkyWater 130nm)", -550, -228, 0.38)
    b.note("f_clk = 10 MHz | C1 = 100 fF, C2 = 800 fF | fc_Golden = 187.675 kHz | VDD = 1.8 V, VCM = 0.9 V", -550, -190, 0.25)

    b.inst("devices/iopin.sym", -500, -130, 0, 1, "name=p_vdd lab=VDD")
    b.inst("devices/iopin.sym", -500, -90, 0, 1, "name=p_vss lab=VSS")

    # 1. XCLK at (-360, 35): w_half=115+20=135, h_half=75+30=105
    # CLK=(-495,35), PHI1=(-225,-10), PHI1_B=(-225,20), PHI2=(-225,50), PHI2_B=(-225,80), VDD=(-360,-70), VSS=(-360,140)
    b.inst("devices/ipin.sym", -530, 35, 0, 0, "name=p_clk lab=CLK")
    b.wire(-530, 35, -495, 35)
    b.inst("non_overlap_clk.sym", -360, 35, 0, 0, "name=XCLK",
           [(-495, 35), (-225, -10), (-225, 20), (-225, 50), (-225, 80), (-360, -70), (-360, 140)])
    b.inst("devices/lab_pin.sym", -360, -70, 0, 0, "name=l_clk_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", -360, 140, 0, 0, "name=l_clk_vss lab=VSS")

    # 2. XSC at (10, 20): w_half=105+20=125, h_half=85+30=115
    # VIN=(-115,-15), PHI1=(-115,15), PHI1_B=(-115,38), PHI2=(-115,61), PHI2_B=(-115,84), VX=(135,-15), VDD=(10,-95), VSS=(10,135)
    b.inst("devices/ipin.sym", -200, -95, 0, 0, "name=p_vin lab=VIN")
    b.wire(-200, -95, -145, -95)
    b.wire(-145, -95, -145, -15)
    b.wire(-145, -15, -115, -15)

    b.wire(-225, -10, -170, -10, "PHI1")
    b.wire(-170, -10, -170, 15)
    b.wire(-170, 15, -115, 15)

    b.wire(-225, 20, -185, 20, "PHI1_B")
    b.wire(-185, 20, -185, 38)
    b.wire(-185, 38, -115, 38)

    b.wire(-225, 50, -185, 50, "PHI2")
    b.wire(-185, 50, -185, 61)
    b.wire(-185, 61, -115, 61)

    b.wire(-225, 80, -170, 80, "PHI2_B")
    b.wire(-170, 80, -170, 84)
    b.wire(-170, 84, -115, 84)

    b.inst("sc_core.sym", 10, 20, 0, 0, "name=XSC",
           [(-115, -15), (135, -15), (-115, 15), (-115, 38), (-115, 61), (-115, 84), (10, -95), (10, 135)])
    b.inst("devices/lab_pin.sym", 10, -95, 0, 0, "name=l_sc_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", 10, 135, 0, 0, "name=l_sc_vss lab=VSS")

    # 3. XOTA at (390, 15): w_half=95+20=115, h_half=70+30=100
    # INP=(275,-15), INN=(275,25), IBIAS=(275,60), VOUT=(505,5), VDD=(390,-85), VSS=(390,115)
    b.wire(135, -15, 275, -15, "VX")
    b.inst("ota_5t.sym", 390, 15, 0, 0, "name=XOTA",
           [(275, -15), (275, 25), (275, 60), (505, 5), (390, -85), (390, 115)])
    b.inst("devices/lab_pin.sym", 390, -85, 0, 0, "name=l_ota_vdd lab=VDD")
    b.inst("devices/lab_pin.sym", 390, 115, 0, 0, "name=l_ota_vss lab=VSS")

    # External IBIAS pin placed cleanly at x=195, y=105 -> routed at x=258 (zero wire crossings!)
    b.inst("devices/ipin.sym", 195, 105, 0, 0, "name=p_ib lab=IBIAS")
    b.wire(195, 105, 258, 105)
    b.wire(258, 60, 258, 105)
    b.wire(258, 60, 275, 60)

    # Unity-gain negative feedback loop (vertical drop at x=235, zero crossing with IBIAS)
    b.wire(505, 5, 600, 5, "VOUT")
    b.wire(545, 5, 545, 165)
    b.wire(235, 165, 545, 165)
    b.wire(235, 25, 235, 165)
    b.wire(235, 25, 275, 25)
    b.inst("devices/opin.sym", 600, 5, 0, 0, "name=p_vout lab=VOUT")

    (XDIR / "top_sc_lpf.sch").write_text(b.render())
    (XDIR / "top_sc_lpf.sym").write_text(
        make_box_symbol(
            "SKY130 SC-LPF",
            left_pins=[("VIN", -25, "in"), ("CLK", 5, "in"), ("IBIAS", 35, "in")],
            right_pins=[("VOUT", 0, "out")],
            top_pins=[("VDD", 0, "inout")],
            bot_pins=[("VSS", 0, "inout")],
            pin_order=["VIN", "CLK", "IBIAS", "VOUT", "VDD", "VSS"],
            w_half=95,
            h_half=65,
            stub_tb=28,
        )
    )


def netlist_all() -> None:
    NDIR.mkdir(parents=True, exist_ok=True)
    env = {
        **os.environ,
        "PDK_ROOT": "/foss/pdks",
        "PDK": "sky130A",
        "PDKPATH": "/foss/pdks/sky130A",
        "XSCHEM_USER_LIBRARY_PATH": str(XDIR),
    }
    rcfile = str(XDIR / "xschemrc")
    targets = [
        "inv_cell.sch",
        "nand2_cell.sch",
        "and2_cell.sch",
        "non_overlap_clk.sch",
        "tg_switch.sch",
        "tg_dummy.sch",
        "sc_core.sch",
        "ota_5t.sch",
        "top_sc_lpf.sch",
    ]
    for sch_file in targets:
        out_spice = sch_file.replace(".sch", "_xschem.spice")
        log_file = Path("/tmp") / f"xschem_{sch_file}.log"
        # Use standard SPICE netlisting (includes AD/AS/PD/PS source/drain junction parasitics!)
        # and uncomment top .subckt/.ends if Xschem comments the top wrapper
        cmd = [
            "xschem",
            "--rcfile", rcfile,
            "-x", "-r", "-q", "-n", "-s",
            "-l", str(log_file),
            "--tcl", "set top_subckt 1",
            "-o", str(NDIR),
            "-N", out_spice,
            str(XDIR / sch_file),
        ]
        res = subprocess.run(cmd, cwd=XDIR, env=env, capture_output=True, text=True, timeout=30)
        sp_path = NDIR / out_spice
        log_txt = log_file.read_text() if log_file.exists() else ""
        if res.returncode != 0 or not sp_path.exists() or "Error:" in log_txt:
            raise RuntimeError(f"Failed netlisting {sch_file} (rc={res.returncode}):\n{log_txt}\n{res.stdout}\n{res.stderr}")
        # Clean top-level `**.subckt` / `**.ends` and trailing `.end` so every file is directly `.include`-able!
        raw = sp_path.read_text()
        cleaned_lines = []
        for ln in raw.splitlines():
            if ln.startswith("**.subckt "):
                cleaned_lines.append(ln[2:])
            elif ln.startswith("**.ends"):
                cleaned_lines.append(".ends")
            elif ln.strip() == ".end":
                continue
            else:
                cleaned_lines.append(ln)
        sp_path.write_text("\n".join(cleaned_lines) + "\n")
        print(f"[OK] Netlisted (with S/D junction AD/AS/PD/PS): {sch_file:22s} -> ngspice/{out_spice}")


def _render_sch_to_pil(sch_path: Path, pad: int = 36):
    from PIL import Image, ImageChops

    stem = sch_path.stem
    pdf_p = Path(f"/tmp/{stem}.pdf")
    raw_png = Path(f"/tmp/{stem}_raw.png")
    subprocess.run(
        ["xschem", "-x", "-r", "-q", "-c", "--rcfile", str(XDIR / "xschemrc"),
         "--pdf", "--plotfile", str(pdf_p), str(sch_path)],
        check=True, capture_output=True
    )
    subprocess.run(
        ["gs", "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=png16m", "-r300",
         f"-sOutputFile={raw_png}", str(pdf_p)],
        check=True, capture_output=True
    )
    im = Image.open(raw_png).convert("RGB")
    # Mask out Xschem's full top-left PostScript filename header across top margin
    im.paste((255, 255, 255), (0, 0, im.width, 105))
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        box = (max(0, bbox[0] - pad), max(0, bbox[1] - pad),
               min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad))
        im = im.crop(box)
    return im


def export_logic_and_testbench_composites(out_dir: Path) -> None:
    """Create 300-DPI IEEE symbol showcase + leaf CMOS cell figure and 4-testbench figure."""
    import tempfile
    import matplotlib.pyplot as plt

    # 1. Build temporary symbol-showcase schematic in /tmp so xschem/ stays clean
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        sym_sch = SchBuilder()
        sym_sch.inst("inv_cell.sym", -450, 10, 0, 0, "name=XNOT WN=1.0 WP=2.5 LCH=0.15")
        sym_sch.inst("nand2_cell.sym", -265, 10, 0, 0, "name=XNAND2")
        sym_sch.inst("and2_cell.sym", -80, 10, 0, 0, "name=XAND2")
        sym_sch.inst("tg_switch.sym", 115, 10, 0, 0, "name=XTG")
        sym_sch.inst("tg_dummy.sym", 300, 10, 0, 0, "name=XDUM")
        sym_sch.inst("ota_5t.sym", 495, 20, 0, 0, "name=XOTA")
        sym_file = td_p / "ieee_symbols_showcase.sch"
        sym_file.write_text(sym_sch.render())

        # 2. Build 4 Xschem Testbench schematics in /tmp
        # TB1: Clock testbench
        tb1 = SchBuilder()
        tb1.frame(-420, -185, 390, 175)
        tb1.title("TB1: non_overlap_clk (.tran 10p 250n)", -395, -155, 0.30)
        tb1.inst("devices/vsource.sym", -320, 20, 0, 0, "name=VCLK value=\"10 MHz (0..1.8V)\"")
        tb1.inst("devices/gnd.sym", -320, 50, 0, 0, "name=g1 lab=0")
        tb1.wire(-320, -10, -145, -10, "CLK")
        tb1.inst("non_overlap_clk.sym", -10, -10, 0, 0, "name=XCLK")
        tb1.inst("devices/lab_pin.sym", -10, -115, 0, 0, "name=lv1 lab=VDD")
        tb1.inst("devices/lab_pin.sym", -10, 95, 0, 0, "name=lg1 lab=VSS")
        for idx, (pname, py) in enumerate([("PHI1", -55), ("PHI1_B", -25), ("PHI2", 5), ("PHI2_B", 35)]):
            tb1.wire(125, py, 240, py, pname)
            tb1.inst("devices/lab_pin.sym", 240, py, 0, 1, f"name=lo{idx} lab={pname}")
        tb1.inst("devices/capa.sym", 200, 90, 0, 0, "name=CL1_4 value=25f")
        tb1.wire(200, 35, 200, 60)
        tb1.inst("devices/gnd.sym", 200, 120, 0, 0, "name=g2 lab=0")
        tb1_p = td_p / "tb1_clk.sch"
        tb1_p.write_text(tb1.render())

        # TB2: TG Ron testbench
        tb2 = SchBuilder()
        tb2.frame(-360, -170, 360, 160)
        tb2.title("TB2: tg_switch (.dc Vin 0 1.8 5mV)", -335, -142, 0.30)
        tb2.inst("devices/vsource.sym", -240, 30, 0, 0, "name=VIN value=\"DC 0..1.8V\"")
        tb2.inst("devices/gnd.sym", -240, 60, 0, 0, "name=g3 lab=0")
        tb2.wire(-240, 0, -88, 0, "VIN")
        tb2.inst("tg_switch.sym", 0, 0, 0, 0, "name=XTG")
        tb2.inst("devices/lab_pin.sym", -32, -68, 0, 0, "name=lpb lab=\"PHI_B=0V\"")
        tb2.inst("devices/lab_pin.sym", 32, -68, 0, 1, "name=lv2 lab=VDD")
        tb2.inst("devices/lab_pin.sym", -32, 68, 0, 0, "name=lp lab=\"PHI=1.8V\"")
        tb2.inst("devices/lab_pin.sym", 32, 68, 0, 1, "name=lg2 lab=VSS")
        tb2.wire(88, 0, 210, 0, "VOUT")
        tb2.inst("devices/vsource.sym", 210, 30, 0, 0, "name=VTST value=\"1mV + VIN\"")
        tb2.inst("devices/gnd.sym", 210, 60, 0, 0, "name=g4 lab=0")
        tb2_p = td_p / "tb2_tg.sch"
        tb2_p.write_text(tb2.render())

        # TB3: 5T-OTA Open-Loop AC testbench
        tb3 = SchBuilder()
        tb3.frame(-390, -195, 370, 195)
        tb3.title("TB3: ota_5t Open-Loop .ac (Lfb=1GH, Cfb=1GF)", -365, -168, 0.29)
        tb3.inst("devices/vsource.sym", -295, -5, 0, 0, "name=VAC value=\"DC 0.9 AC 1\"")
        tb3.inst("devices/gnd.sym", -295, 25, 0, 0, "name=g5 lab=0")
        tb3.wire(-295, -35, -115, -35)
        tb3.wire(-115, -35, -115, -40)
        tb3.inst("devices/isource.sym", -235, 65, 0, 0, "name=IBIAS value=30u")
        tb3.inst("devices/gnd.sym", -235, 95, 0, 0, "name=g6 lab=0")
        tb3.wire(-235, 35, -115, 35)
        tb3.inst("ota_5t.sym", 0, -10, 0, 0, "name=XOTA")
        tb3.inst("devices/lab_pin.sym", 0, -110, 0, 0, "name=lv3 lab=VDD")
        tb3.inst("devices/lab_pin.sym", 0, 90, 0, 0, "name=lg3 lab=VSS")
        tb3.wire(115, -20, 240, -20, "VOUT")
        tb3.inst("devices/capa.sym", 240, 20, 0, 0, "name=CL value=1p")
        tb3.wire(240, -20, 240, -10)
        tb3.inst("devices/gnd.sym", 240, 50, 0, 0, "name=g7 lab=0")
        tb3.wire(175, -20, 175, 130)
        tb3.wire(45, 130, 175, 130)
        tb3.inst("devices/ind.sym", 15, 130, 1, 0, "name=Lfb value=1G")
        tb3.wire(-145, 130, -15, 130)
        tb3.wire(-145, 0, -145, 130)
        tb3.wire(-145, 0, -115, 0)
        tb3.inst("devices/capa.sym", -145, 160, 0, 0, "name=Cfb value=1G")
        tb3.inst("devices/gnd.sym", -145, 190, 0, 0, "name=g8 lab=0")
        tb3_p = td_p / "tb3_ota.sch"
        tb3_p.write_text(tb3.render())

        # TB4: Top-Level SC-LPF Coherent .tran & Multisine testbench
        tb4 = SchBuilder()
        tb4.frame(-435, -180, 360, 170)
        tb4.title("TB4: top_sc_lpf Coherent .tran / Multisine Bode", -410, -152, 0.29)
        tb4.inst("devices/vsource.sym", -345, -55, 0, 0, "name=VIN value=\"0.9 + 0.2sin(2pi f0 t)\"")
        tb4.inst("devices/gnd.sym", -345, -25, 0, 0, "name=g9 lab=0")
        tb4.wire(-345, -85, -165, -85)
        tb4.wire(-165, -85, -165, -25)
        tb4.wire(-165, -25, -115, -25)
        tb4.inst("devices/vsource.sym", -345, 45, 0, 0, "name=VCLK value=\"10 MHz\"")
        tb4.inst("devices/gnd.sym", -345, 75, 0, 0, "name=g10 lab=0")
        tb4.wire(-345, 15, -165, 15)
        tb4.wire(-165, 15, -165, 5)
        tb4.wire(-165, 5, -115, 5)
        tb4.inst("devices/isource.sym", -225, 110, 0, 0, "name=IB value=30u")
        tb4.inst("devices/gnd.sym", -225, 140, 0, 0, "name=g11 lab=0")
        tb4.wire(-225, 80, -145, 80)
        tb4.wire(-145, 35, -145, 80)
        tb4.wire(-145, 35, -115, 35)
        tb4.inst("top_sc_lpf.sym", 0, 0, 0, 0, "name=XDUT")
        tb4.inst("devices/lab_pin.sym", 0, -93, 0, 0, "name=lv4 lab=VDD")
        tb4.inst("devices/lab_pin.sym", 0, 93, 0, 0, "name=lg4 lab=VSS")
        tb4.wire(115, 0, 230, 0, "VOUT")
        tb4.inst("devices/capa.sym", 230, 40, 0, 0, "name=CL_1pF value=1p")
        tb4.wire(230, 0, 230, 10)
        tb4.inst("devices/gnd.sym", 230, 70, 0, 0, "name=g12 lab=0")
        tb4_p = td_p / "tb4_top.sch"
        tb4_p.write_text(tb4.render())

        # Render Logic Showcase + 4 Leaf Cells -> w3_sch_logic_and_cells.png
        im_syms = _render_sch_to_pil(sym_file, pad=24)
        im_inv = _render_sch_to_pil(XDIR / "inv_cell.sch")
        im_nand = _render_sch_to_pil(XDIR / "nand2_cell.sch")
        im_and = _render_sch_to_pil(XDIR / "and2_cell.sch")
        im_dum = _render_sch_to_pil(XDIR / "tg_dummy.sch")

        fig = plt.figure(figsize=(13.6, 8.2), dpi=300, facecolor="#FFFFFF")
        gs = fig.add_gridspec(2, 4, height_ratios=[0.95, 1.35], hspace=0.22, wspace=0.14)
        ax_top = fig.add_subplot(gs[0, :])
        ax_top.imshow(im_syms)
        ax_top.set_title("(a) Standard IEEE / ANSI Symbols Created in Xschem (NOT, NAND2, AND2, CMOS TG, Dummy W/2, 5T-OTA)",
                         fontsize=11, fontweight="bold", color="#0369A1", pad=6)
        ax_top.axis("off")

        cells = [
            (im_inv, "(b) inv_cell.sch (NOT)"),
            (im_nand, "(c) nand2_cell.sch (NAND2)"),
            (im_and, "(d) and2_cell.sch (NAND2+NOT)"),
            (im_dum, "(e) tg_dummy.sch (Dummy W/2)"),
        ]
        for idx, (im_c, title_c) in enumerate(cells):
            ax = fig.add_subplot(gs[1, idx])
            ax.imshow(im_c)
            ax.set_title(title_c, fontsize=10, fontweight="bold", color="#0C4A6E", pad=5)
            for sp in ax.spines.values():
                sp.set_edgecolor("#BAE6FD")
                sp.set_linewidth(1.0)
            ax.set_xticks([])
            ax.set_yticks([])

        fig.savefig(out_dir / "w3_sch_logic_and_cells.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
        plt.close(fig)
        print("[OK] Rendered crisp 300-DPI composite: w3_sch_logic_and_cells.png")

        # Render 4 Testbenches -> w3_sch_testbenches.png
        im_tb1 = _render_sch_to_pil(tb1_p)
        im_tb2 = _render_sch_to_pil(tb2_p)
        im_tb3 = _render_sch_to_pil(tb3_p)
        im_tb4 = _render_sch_to_pil(tb4_p)

        fig2, axes2 = plt.subplots(2, 2, figsize=(13.6, 8.0), dpi=300, facecolor="#FFFFFF")
        tbs = [
            (im_tb1, "(a) TB1: non_overlap_clk (.tran 10p 250n, CL=25fF)"),
            (im_tb2, "(b) TB2: tg_switch (.dc Vin 0..1.8V, dVds=1mV)"),
            (im_tb3, "(c) TB3: ota_5t (.op / Open-Loop .ac via Lfb=1GH, Cfb=1GF)"),
            (im_tb4, "(d) TB4: top_sc_lpf (Coherent .tran & 11-Tone Bode, CL=1pF)"),
        ]
        for ax, (im_t, title_t) in zip(axes2.flat, tbs):
            ax.imshow(im_t)
            ax.set_title(title_t, fontsize=10.5, fontweight="bold", color="#0369A1", pad=5)
            for sp in ax.spines.values():
                sp.set_edgecolor("#BAE6FD")
                sp.set_linewidth(1.0)
            ax.set_xticks([])
            ax.set_yticks([])
        fig2.tight_layout()
        fig2.savefig(out_dir / "w3_sch_testbenches.png", dpi=300, bbox_inches="tight", facecolor="#FFFFFF")
        plt.close(fig2)
        print("[OK] Rendered crisp 300-DPI composite: w3_sch_testbenches.png")


def export_schematic_pngs() -> None:
    out_dir = ROOT / "slides" / "figs"
    out_dir.mkdir(parents=True, exist_ok=True)
    for name in ["non_overlap_clk", "tg_switch", "sc_core", "ota_5t", "top_sc_lpf"]:
        final_png = out_dir / f"w3_sch_{name}.png"
        im = _render_sch_to_pil(XDIR / f"{name}.sch", pad=36)
        im.save(final_png, dpi=(300, 300))
        print(f"[OK] Rendered crisp 300-DPI schematic: {final_png.name} ({im.size[0]}x{im.size[1]})")
    export_logic_and_testbench_composites(out_dir)


def main() -> int:
    XDIR.mkdir(parents=True, exist_ok=True)
    build_inv_cell()
    build_nand2_cell()
    build_and2_cell()
    build_non_overlap_clk()
    build_tg_switch()
    build_sc_core()
    build_ota_5t()
    build_top_sc_lpf()
    netlist_all()
    export_schematic_pngs()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
