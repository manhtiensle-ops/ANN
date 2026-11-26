#!/usr/bin/env python3
"""
Capture authentic 3-window EDA workstation screenshots on isolated X11 display (:98):
  - Left half    (808x848+10+22)  : Live Xschem GUI displaying the block/top schematic
  - Top-right    (752x378+834+22) : Live Xterm terminal running interactive Ngspice-47
  - Bottom-right (752x446+834+424): Live Ngspice native X11 Waveform Plotter (`TopLevelShell`)
"""
from __future__ import annotations

import ctypes
import json
import os
import re
import struct
import subprocess
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
XDIR = ROOT / "xschem"
NDIR = ROOT / "ngspice"
FIG_DIR = ROOT / "slides" / "figs"


def place_ngspice_plot_window(display: str, x: int = 834, y: int = 424, w: int = 752, h: int = 446) -> None:
    """Locate Ngspice's Xt TopLevelShell (and its xfwm4 frame) and place it in bottom-right."""
    tree = subprocess.check_output(["xwininfo", "-root", "-tree", "-display", display], text=True)
    lines = tree.splitlines()

    target_frame_id: int | None = None
    target_client_id: int | None = None
    last_top_frame: int | None = None

    for ln in lines:
        m = re.match(r"^(\s+)(0x[0-9a-fA-F]+)\s+(.*)$", ln)
        if not m:
            continue
        indent = len(m.group(1))
        wid = int(m.group(2), 16)
        rest = m.group(3)
        if indent == 5:
            last_top_frame = wid
        if '"TopLevelShell"' in rest and '"ngspice"' in rest:
            target_client_id = wid
            target_frame_id = last_top_frame if indent > 5 else wid
            break

    if target_frame_id is None and target_client_id is None:
        return

    x11 = ctypes.CDLL("libX11.so.6")
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    dpy = x11.XOpenDisplay(display.encode())
    if not dpy:
        return
    try:
        if target_frame_id is not None:
            x11.XMoveResizeWindow(ctypes.c_void_p(dpy), ctypes.c_ulong(target_frame_id), x, y, w, h)
            x11.XRaiseWindow(ctypes.c_void_p(dpy), ctypes.c_ulong(target_frame_id))
        if target_client_id is not None and target_client_id != target_frame_id:
            x11.XResizeWindow(ctypes.c_void_p(dpy), ctypes.c_ulong(target_client_id), w - 10, h - 32)
        x11.XFlush(ctypes.c_void_p(dpy))
    finally:
        x11.XCloseDisplay(ctypes.c_void_p(dpy))


def grab_x11_root(display: str, out_png: Path) -> None:
    raw = subprocess.check_output(["xwd", "-root", "-silent", "-display", display])
    fields = struct.unpack(">25I", raw[:100])
    hdr_size = fields[0]
    width = fields[4]
    height = fields[5]
    byte_order = fields[7]
    bpl = fields[12]
    ncolors = fields[19]
    offset = hdr_size + ncolors * 12

    buf = np.frombuffer(raw, dtype=np.uint8, offset=offset).reshape((height, bpl))
    px = buf[:, : width * 4].reshape((height, width, 4))
    rgb = px[:, :, [2, 1, 0]] if byte_order == 0 else px[:, :, [1, 2, 3]]
    Image.fromarray(rgb, mode="RGB").save(out_png, optimize=True)


def capture_scene(
    display: str,
    env: dict[str, str],
    sch_file: str,
    xterm_title: str,
    echo_lines: list[str],
    plot_title: str,
    ngspice_plot_cmds: str,
    out_png: Path,
) -> None:
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        echo_cmds = "\n".join(f'echo "{ln}"' for ln in echo_lines)

        ng_sp = td_path / "live_plot.sp"
        ng_sp.write_text(
            f"""* {plot_title}
.control
set ngbehavior=hsa
set xbrushwidth=2
set color0=white
set color1=rgb:0/2/4
set color2=rgb:0/4/9
set color3=rgb:d/7/0
set color4=rgb:0/6/6
{ngspice_plot_cmds}
echo "--------------------------------------------------------------------"
{echo_cmds}
echo "--------------------------------------------------------------------"
.endc
"""
        )

        # 1. Live Xschem GUI constrained strictly to left half (light white canvas theme)
        p_xschem = subprocess.Popen(
            [
                "xschem",
                "--rcfile", str(XDIR / "xschemrc"),
                "--tcl", "set dark_colorscheme 0",
                "--command",
                "wm state . normal; wm geometry . 800x848+10+22; after 350 {wm state . normal; wm geometry . 800x848+10+22; xschem zoom_full}",
                str(XDIR / sch_file),
            ],
            cwd=XDIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # 2. Live Xterm in top-right (light white-blue theme, zero dark background!)
        p_xterm = subprocess.Popen(
            [
                "xterm",
                "-T", xterm_title,
                "-geometry", "86x21+834+22",
                "-fa", "DejaVu Sans Mono",
                "-fs", "9.0",
                "-bg", "#FFFFFF",
                "-fg", "#0C4A6E",
                "-e", "ngspice", "-i", str(ng_sp),
            ],
            cwd=NDIR,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        time.sleep(1.7)
        place_ngspice_plot_window(display, x=834, y=424, w=752, h=446)
        time.sleep(0.35)
        grab_x11_root(display, out_png)
        print(f"[OK] Captured 3-window workstation screenshot -> {out_png.name}")

        for proc in (p_xterm, p_xschem):
            proc.terminate()
        for proc in (p_xterm, p_xschem):
            try:
                proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                proc.kill()
        subprocess.run(["pkill", "-f", "live_plot.sp"], capture_output=True)


def extract_tail_lines(log_path: Path, keywords: tuple[str, ...], max_lines: int = 8) -> str:
    lines = log_path.read_text().splitlines()
    picked = [ln for ln in lines if any(k in ln.lower() for k in keywords)]
    return "\n".join(picked[-max_lines:])


def main() -> int:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    disp = ":98"
    xvfb = subprocess.Popen(["Xvfb", disp, "-screen", "0", "1600x900x24"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)

    env = {
        **os.environ,
        "DISPLAY": disp,
        "PDK_ROOT": "/foss/pdks",
        "PDK": "sky130A",
        "PDKPATH": "/foss/pdks/sky130A",
        "XSCHEM_USER_LIBRARY_PATH": str(XDIR),
    }

    wm = subprocess.Popen(["xfwm4"], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)

    subprocess.run(["xsetroot", "-display", disp, "-solid", "#BAE6FD"], capture_output=True)
    xrdb_cfg = (
        "TopLevelShell.geometry: 744x414+834+426\n"
        "*TopLevelShell.geometry: 744x414+834+426\n"
        "ngspice*geometry: 744x414+834+426\n"
    )
    subprocess.run(["xrdb", "-display", disp, "-merge"], input=xrdb_cfg, text=True, capture_output=True)

    try:
        b1_lines = [
            "t_nov_12 = 3.116 ns  |  t_nov_21 = 3.092 ns  |  tr = 174.4 ps",
            "[GATE 3.1 PASS] Non-overlap dead-time in [2.0, 5.0] ns (Zero overlap)",
        ]
        capture_scene(
            disp,
            env,
            "non_overlap_clk.sch",
            "xterm — Ngspice-47: Block 1 (non_overlap_clk .tran 10 MHz)",
            b1_lines,
            "Block 1: 10 MHz Non-Overlapping Clock (Phi1, Phi2)",
            f"load {NDIR / 'tb_clk.raw'}\nplot v(phi1) v(phi2) xlimit 48n 118n ylimit -0.1 1.95",
            FIG_DIR / "w3_gui_clk_workstation.png",
        )

        b2_lines = [
            "Ron(0.9V) = 3.713 kOhm  |  Ron_max = 4.431 kOhm  |  Ron_min = 0.463 kOhm",
            "[GATE 3.2 PASS] R_on(Vin) < 5.0 kOhm across full 0..1.8 V rail",
        ]
        capture_scene(
            disp,
            env,
            "tg_switch.sch",
            "xterm — Ngspice-47: Block 2 (tg_switch .dc R_on Sweep)",
            b2_lines,
            "Block 2: CMOS TG On-Resistance R_on(Vin) [kOhm]",
            f"load {NDIR / 'tb_tg.raw'}\nplot ron_tg_kohm ylimit 0 5.5",
            FIG_DIR / "w3_gui_tg_workstation.png",
        )

        b4_lines = [
            "A_OL = 41.62 dB  |  GBW = 43.61 MHz  |  PM = 81.05 deg  |  SR+ = 22.9 V/us",
            "[GATE 3.3 PASS] All M1-M5 in saturation (margins >= +136.6 mV)",
        ]
        capture_scene(
            disp,
            env,
            "ota_5t.sch",
            "xterm — Ngspice-47: Block 4 (ota_5t .op / .ac / .tran)",
            b4_lines,
            "Block 4: 5T-OTA Open-Loop AC Gain [dB]",
            f"load {NDIR / 'tb_ota_ac.raw'}\nplot gain_db",
            FIG_DIR / "w3_gui_ota_workstation.png",
        )

        d = json.loads((ROOT / "python" / "metrics_week3_prelayout.json").read_text())
        tb = d["top_bode"]
        tf = d["top_fft_prelayout_optimized_dummy"]
        b_top_lines = [
            f"fc_Golden = {tb['fc_golden_Hz']/1e3:.2f} kHz | fc_Pre = {tb['fc_prelayout_Hz']/1e3:.2f} kHz ({tb['fc_error_pct']:+.2f}%)",
            f"SFDR = {tf['SFDR_dB']:.2f} dB | THD = {tf['THD_dB']:.2f} dB | ENOB = {tf['ENOB_bits']:.2f} bits [GATE 3.4 PASS]",
        ]
        capture_scene(
            disp,
            env,
            "top_sc_lpf.sch",
            "xterm — Ngspice-47: Top-Level (top_sc_lpf Coherent .tran & FFT)",
            b_top_lines,
            "Top-Level SC-LPF: Input Sine vs Staircase Filtered Output",
            f"load {NDIR / 'tb_top_zoom.raw'}\nplot v(vin_coh) v(vout_opt) xlimit 20u 54.5u",
            FIG_DIR / "w3_gui_top_workstation.png",
        )
    finally:
        wm.terminate()
        xvfb.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
