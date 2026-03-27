"""Stacked Bar Plot - 堆叠柱状图：展示组成比例。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_stacked_bar(
    data: pd.DataFrame,
    x_col: str = None,
    value_cols: list = None,
    normalize: bool = False,
    horizontal: bool = False,
    title: str = "堆叠柱状图",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (12, 7),
):
    df = data.copy()
    if x_col is None:
        x_col = df.columns[0]
    if value_cols is None:
        value_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if normalize:
        row_sums = df[value_cols].sum(axis=1)
        for col in value_cols:
            df[col] = df[col] / row_sums * 100

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    x = np.arange(len(df))
    bottoms = np.zeros(len(df))

    for i, col in enumerate(value_cols):
        color = SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
        if horizontal:
            ax.barh(x, df[col], left=bottoms, color=color, label=col, height=0.7, edgecolor="white", linewidth=0.5)
        else:
            ax.bar(x, df[col], bottom=bottoms, color=color, label=col, width=0.7, edgecolor="white", linewidth=0.5)
        bottoms += df[col].values

    if horizontal:
        ax.set_yticks(x)
        ax.set_yticklabels(df[x_col], fontsize=9)
        style_axis(ax, title=title, xlabel=("百分比 (%)" if normalize else ylabel) or "值")
    else:
        ax.set_xticks(x)
        ax.set_xticklabels(df[x_col], rotation=45, ha="right", fontsize=9)
        style_axis(ax, title=title, ylabel=("百分比 (%)" if normalize else ylabel) or "值")

    ax.legend(title="类别", bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    add_watermark(fig)
    fig.tight_layout()

    stats = {"样本数": len(df), "类别数": len(value_cols), "标准化": "百分比" if normalize else "原始值"}
    return fig, stats
