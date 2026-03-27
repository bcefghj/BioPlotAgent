"""Radar / Spider Chart - 雷达图：多维度对比。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import SEQUENTIAL_COLORS, add_watermark


def plot_radar(
    data: pd.DataFrame,
    label_col: str = None,
    value_cols: list = None,
    title: str = "雷达图 (Radar Chart)",
    fill: bool = True,
    figsize: tuple = (9, 9),
):
    df = data.copy()
    if label_col is None:
        label_col = df.columns[0]
    if value_cols is None:
        value_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    categories = value_cols
    n_cats = len(categories)
    angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True), facecolor="white")

    for i, (_, row) in enumerate(df.iterrows()):
        values = row[value_cols].values.tolist()
        values += values[:1]
        color = SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
        ax.plot(angles, values, "o-", linewidth=2, color=color, label=str(row[label_col]), markersize=5)
        if fill:
            ax.fill(angles, values, alpha=0.15, color=color)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=30)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), framealpha=0.9)
    add_watermark(fig)

    stats = {"组数": len(df), "维度数": n_cats}
    return fig, stats
