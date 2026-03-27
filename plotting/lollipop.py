"""Lollipop Chart - 棒棒糖图：柱状图的优雅替代品。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import SEQUENTIAL_COLORS, BIO_PALETTE, style_axis, add_watermark


def plot_lollipop(
    data: pd.DataFrame,
    label_col: str = None,
    value_col: str = None,
    group_col: str = None,
    horizontal: bool = True,
    sort: bool = True,
    title: str = "棒棒糖图 (Lollipop Chart)",
    xlabel: str = "",
    ylabel: str = "",
    figsize: tuple = (10, 8),
):
    df = data.copy()
    if label_col is None:
        label_col = df.columns[0]
    if value_col is None:
        value_col = df.select_dtypes(include=[np.number]).columns[0]
    if sort:
        df = df.sort_values(value_col).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if group_col and group_col in df.columns:
        groups = df[group_col].unique()
        cmap = {g: SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)] for i, g in enumerate(groups)}
        colors = [cmap[g] for g in df[group_col]]
    else:
        norm = plt.Normalize(df[value_col].min(), df[value_col].max())
        colors = plt.cm.RdYlBu_r(norm(df[value_col]))

    positions = range(len(df))
    if horizontal:
        ax.hlines(y=positions, xmin=0, xmax=df[value_col], color=colors, linewidth=1.5, alpha=0.7)
        ax.scatter(df[value_col], positions, color=colors, s=60, zorder=5, edgecolors="white", linewidth=0.5)
        ax.set_yticks(positions)
        ax.set_yticklabels(df[label_col], fontsize=9)
        ax.axvline(x=0, color="grey", linewidth=0.5)
        style_axis(ax, title=title, xlabel=xlabel or value_col)
    else:
        ax.vlines(x=positions, ymin=0, ymax=df[value_col], color=colors, linewidth=1.5, alpha=0.7)
        ax.scatter(positions, df[value_col], color=colors, s=60, zorder=5, edgecolors="white", linewidth=0.5)
        ax.set_xticks(positions)
        ax.set_xticklabels(df[label_col], rotation=45, ha="right", fontsize=9)
        style_axis(ax, title=title, ylabel=ylabel or value_col)

    add_watermark(fig)
    fig.tight_layout()
    stats = {"数据条数": len(df), "最大值": f"{df[value_col].max():.2f}", "最小值": f"{df[value_col].min():.2f}"}
    return fig, stats
