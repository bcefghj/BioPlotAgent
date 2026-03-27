"""Density Plot - 密度图：展示数据分布概率密度。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_density(
    data: pd.DataFrame,
    value_col: str = None,
    group_col: str = None,
    fill: bool = True,
    title: str = "密度分布图",
    xlabel: str = "",
    figsize: tuple = (10, 7),
):
    df = data.copy()
    if value_col is None:
        value_col = df.select_dtypes(include=[np.number]).columns[0]

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if group_col and group_col in df.columns:
        for i, g in enumerate(df[group_col].unique()):
            vals = df.loc[df[group_col] == g, value_col].dropna()
            if len(vals) < 2:
                continue
            kde = gaussian_kde(vals)
            x = np.linspace(vals.min() - vals.std(), vals.max() + vals.std(), 300)
            y = kde(x)
            color = SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
            ax.plot(x, y, color=color, linewidth=2, label=g)
            if fill:
                ax.fill_between(x, y, alpha=0.3, color=color)
    else:
        vals = df[value_col].dropna()
        kde = gaussian_kde(vals)
        x = np.linspace(vals.min() - vals.std(), vals.max() + vals.std(), 300)
        y = kde(x)
        ax.plot(x, y, color=SEQUENTIAL_COLORS[0], linewidth=2)
        if fill:
            ax.fill_between(x, y, alpha=0.3, color=SEQUENTIAL_COLORS[0])

    if group_col:
        ax.legend(title="分组", framealpha=0.9)

    style_axis(ax, title=title, xlabel=xlabel or value_col, ylabel="密度")
    add_watermark(fig)
    fig.tight_layout()

    stats = {"样本数": len(df), f"{value_col} 均值": f"{df[value_col].mean():.2f}",
             f"{value_col} 标准差": f"{df[value_col].std():.2f}"}
    return fig, stats
