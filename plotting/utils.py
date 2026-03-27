"""Shared plotting utilities."""

import os
import io
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

BIO_PALETTE = {
    "up": "#E74C3C",
    "down": "#3498DB",
    "neutral": "#95A5A6",
    "highlight": "#E67E22",
    "primary": "#2C3E50",
    "secondary": "#7F8C8D",
    "accent": "#1ABC9C",
    "bg": "#FAFAFA",
}

SEQUENTIAL_COLORS = [
    "#E74C3C", "#3498DB", "#2ECC71", "#F39C12",
    "#9B59B6", "#1ABC9C", "#E67E22", "#34495E",
    "#16A085", "#C0392B", "#2980B9", "#27AE60",
]


def save_figure(fig, format="png", dpi=300):
    buf = io.BytesIO()
    fig.savefig(buf, format=format, dpi=dpi, bbox_inches="tight", facecolor="white")
    buf.seek(0)
    return buf


def get_example_data_path(filename: str) -> str:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", "examples", filename)


def style_axis(ax, title="", xlabel="", ylabel="", fontsize=12):
    ax.set_title(title, fontsize=fontsize + 2, fontweight="bold", pad=15)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(labelsize=fontsize - 1)


def add_watermark(fig, text="BioPlotAgent"):
    fig.text(
        0.98, 0.02, text,
        fontsize=8, color="#CCCCCC",
        ha="right", va="bottom",
        alpha=0.5,
    )
