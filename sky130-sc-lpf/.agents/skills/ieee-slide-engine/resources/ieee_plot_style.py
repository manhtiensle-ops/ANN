"""Reusable 300-DPI IEEE/ISSCC Matplotlib styling for sky130-sc-lpf."""
import matplotlib as mpl
import matplotlib.pyplot as plt

IEEE_COLORS = {
    "navy": "#0F172A",
    "cobalt": "#2563EB",
    "cyan": "#0284C7",
    "teal": "#0D9488",
    "amber": "#D97706",
    "crimson": "#DC2626",
    "slate": "#475569",
    "grid": "#CBD5E1",
    "bg": "#FFFFFF",
}


def apply_ieee_style() -> None:
    """Configure Matplotlib rcParams for crisp 300-DPI conference figures."""
    mpl.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08,
        "figure.facecolor": IEEE_COLORS["bg"],
        "axes.facecolor": IEEE_COLORS["bg"],
        "axes.edgecolor": "#334155",
        "axes.linewidth": 1.0,
        "axes.grid": True,
        "grid.color": IEEE_COLORS["grid"],
        "grid.linestyle": "--",
        "grid.linewidth": 0.6,
        "grid.alpha": 0.65,
        "font.family": "sans-serif",
        "font.size": 10.5,
        "axes.titlesize": 12,
        "axes.titleweight": "bold",
        "axes.labelsize": 10.5,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9.5,
        "legend.frameon": True,
        "legend.facecolor": "#F8FAFC",
        "legend.edgecolor": "#CBD5E1",
        "lines.linewidth": 1.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })
