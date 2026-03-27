"""Waterfall Plot - 瀑布图：展示突变景观或排序后的变化量。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import BIO_PALETTE, style_axis, add_watermark


def plot_waterfall(
    data: pd.DataFrame,
    value_col: str = "value",
    label_col: str = None,
    group_col: str = None,
    sort: bool = True,
    title: str = "瀑布图 (Waterfall Plot)",
    ylabel: str = "变化量",
    figsize: tuple = (14, 6),
):
    df = data.copy()
    if sort:
        df = df.sort_values(value_col, ascending=False).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    colors = []
    if group_col and group_col in df.columns:
        unique_groups = df[group_col].unique()
        cmap = {g: plt.cm.Set2(i / len(unique_groups)) for i, g in enumerate(unique_groups)}
        colors = [cmap[g] for g in df[group_col]]
    else:
        colors = [BIO_PALETTE["up"] if v >= 0 else BIO_PALETTE["down"] for v in df[value_col]]

    ax.bar(range(len(df)), df[value_col], color=colors, width=1.0, edgecolor="none")
    ax.axhline(y=0, color="black", linewidth=0.8)

    if label_col and label_col in df.columns and len(df) <= 50:
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels(df[label_col], rotation=90, fontsize=7)
    else:
        ax.set_xlabel("样本", fontsize=12)

    if group_col and group_col in df.columns:
        handles = [plt.Rectangle((0, 0), 1, 1, color=cmap[g]) for g in unique_groups]
        ax.legend(handles, unique_groups, title="分组", loc="upper right")

    style_axis(ax, title=title, ylabel=ylabel)
    add_watermark(fig)
    fig.tight_layout()

    n_pos = (df[value_col] >= 0).sum()
    n_neg = (df[value_col] < 0).sum()
    stats = {"总样本": len(df), "正值": n_pos, "负值": n_neg,
             "最大值": f"{df[value_col].max():.2f}", "最小值": f"{df[value_col].min():.2f}"}
    return fig, stats
