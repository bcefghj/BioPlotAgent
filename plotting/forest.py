"""Forest Plot - 森林图：荟萃分析/多变量分析结果展示。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import BIO_PALETTE, style_axis, add_watermark


def plot_forest(
    data: pd.DataFrame,
    label_col: str = "variable",
    estimate_col: str = "HR",
    lower_col: str = "lower",
    upper_col: str = "upper",
    pvalue_col: str = None,
    null_value: float = 1.0,
    log_scale: bool = True,
    title: str = "森林图 (Forest Plot)",
    xlabel: str = "Hazard Ratio (95% CI)",
    figsize: tuple = (10, None),
):
    df = data.copy()
    n = len(df)
    if figsize[1] is None:
        figsize = (figsize[0], max(4, n * 0.5 + 2))

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    y_pos = np.arange(n)[::-1]
    colors = [BIO_PALETTE["up"] if row[estimate_col] > null_value else BIO_PALETTE["down"]
              for _, row in df.iterrows()]

    for i, (_, row) in enumerate(df.iterrows()):
        est = row[estimate_col]
        lo, hi = row[lower_col], row[upper_col]
        ax.plot([lo, hi], [y_pos[i], y_pos[i]], color=colors[i], linewidth=2, solid_capstyle="round")
        ax.scatter(est, y_pos[i], color=colors[i], s=80, zorder=5, edgecolors="white", linewidth=0.5)

    ax.axvline(x=null_value, color="black", linestyle="--", linewidth=0.8, alpha=0.6)

    labels = []
    for _, row in df.iterrows():
        lbl = f"{row[label_col]}  {row[estimate_col]:.2f} ({row[lower_col]:.2f}-{row[upper_col]:.2f})"
        if pvalue_col and pvalue_col in df.columns:
            p = row[pvalue_col]
            lbl += f"  p={'<0.001' if p < 0.001 else f'{p:.3f}'}"
        labels.append(lbl)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)

    if log_scale:
        ax.set_xscale("log")

    style_axis(ax, title=title, xlabel=xlabel)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    add_watermark(fig)
    fig.tight_layout()

    n_risk = (df[estimate_col] > null_value).sum()
    n_protect = (df[estimate_col] <= null_value).sum()
    stats = {"变量数": n, "风险因素": n_risk, "保护因素": n_protect}
    return fig, stats
