"""Ridge Plot / Joy Plot - 山脊图：多组分布对比。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_ridge(
    data: pd.DataFrame,
    value_col: str = None,
    group_col: str = None,
    overlap: float = 0.6,
    title: str = "山脊图 (Ridge Plot)",
    xlabel: str = "",
    figsize: tuple = (10, 8),
):
    df = data.copy()
    if value_col is None:
        value_col = df.select_dtypes(include=[np.number]).columns[0]
    if group_col is None:
        group_col = df.select_dtypes(exclude=[np.number]).columns[0]

    groups = df[group_col].unique()
    n = len(groups)

    fig, axes = plt.subplots(n, 1, figsize=figsize, facecolor="white", sharex=True)
    if n == 1:
        axes = [axes]

    x_min = df[value_col].min() - df[value_col].std()
    x_max = df[value_col].max() + df[value_col].std()
    x_range = np.linspace(x_min, x_max, 300)

    for i, (group, ax) in enumerate(zip(groups, axes)):
        vals = df.loc[df[group_col] == group, value_col].dropna()
        if len(vals) < 2:
            continue
        kde = gaussian_kde(vals)
        density = kde(x_range)
        color = SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]

        ax.fill_between(x_range, density, alpha=0.6, color=color)
        ax.plot(x_range, density, color=color, linewidth=1.5)
        ax.axhline(y=0, color="black", linewidth=0.3)

        ax.set_ylabel("")
        ax.text(-0.01, 0.5, str(group), transform=ax.transAxes, ha="right", va="center",
                fontsize=10, fontweight="bold")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.set_yticks([])

        if i < n - 1:
            ax.spines["bottom"].set_visible(False)
            ax.set_xticks([])

    axes[-1].set_xlabel(xlabel or value_col, fontsize=12)
    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.02)
    add_watermark(fig)
    fig.tight_layout()

    stats = {"分组数": n}
    for g in groups:
        vals = df.loc[df[group_col] == g, value_col]
        stats[f"{g} 均值"] = f"{vals.mean():.2f}"
    return fig, stats
