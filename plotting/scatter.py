"""Scatter Plot - 散点图（含回归线和相关系数）。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats as sp_stats
from .utils import SEQUENTIAL_COLORS, BIO_PALETTE, style_axis, add_watermark


def plot_scatter(
    data: pd.DataFrame,
    x_col: str = None,
    y_col: str = None,
    group_col: str = None,
    color_col: str = None,
    show_reg: bool = True,
    show_corr: bool = True,
    title: str = "基因表达散点图",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (10, 8),
):
    df = data.copy()
    if x_col is None or y_col is None:
        nc = df.select_dtypes(include=[np.number]).columns
        x_col = x_col or nc[0]
        y_col = y_col or (nc[1] if len(nc) > 1 else nc[0])

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if group_col and group_col in df.columns:
        for i, g in enumerate(df[group_col].unique()):
            m = df[group_col] == g
            ax.scatter(df.loc[m, x_col], df.loc[m, y_col],
                       c=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                       s=40, alpha=0.6, label=g, edgecolors="white", linewidth=0.3)
        ax.legend(title="分组")
    elif color_col and color_col in df.columns:
        sc = ax.scatter(df[x_col], df[y_col], c=df[color_col], cmap="viridis",
                        s=40, alpha=0.7, edgecolors="white", linewidth=0.3)
        plt.colorbar(sc, ax=ax, label=color_col, shrink=0.8)
    else:
        ax.scatter(df[x_col], df[y_col], c=BIO_PALETTE["primary"],
                   s=40, alpha=0.6, edgecolors="white", linewidth=0.3)

    r, p = sp_stats.pearsonr(df[x_col].dropna(), df[y_col].dropna())
    stats_info = {"Pearson r": f"{r:.4f}", "P-value": f"{p:.2e}", "样本数": len(df)}

    if show_reg:
        z = np.polyfit(df[x_col], df[y_col], 1)
        xline = np.linspace(df[x_col].min(), df[x_col].max(), 100)
        ax.plot(xline, np.polyval(z, xline), color=BIO_PALETTE["up"],
                linewidth=2, linestyle="--", alpha=0.8)

    if show_corr:
        p_text = f"p = {p:.2e}" if p < 0.001 else f"p = {p:.4f}"
        ax.text(0.05, 0.95, f"R = {r:.3f}\n{p_text}",
                transform=ax.transAxes, fontsize=11, va="top",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor="gray", alpha=0.8))

    style_axis(ax, title=title, xlabel=xlabel or x_col, ylabel=ylabel or y_col)
    add_watermark(fig)
    fig.tight_layout()
    return fig, stats_info
