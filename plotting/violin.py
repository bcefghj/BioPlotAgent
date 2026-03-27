"""Violin Plot - 小提琴图：展示数据分布形态和组间差异。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_violin(
    data: pd.DataFrame,
    value_col: str = None,
    group_col: str = None,
    gene_col: str = None,
    split: bool = False,
    inner: str = "box",
    title: str = "基因表达小提琴图",
    ylabel: str = "表达量",
    figsize: tuple = (11, 7),
):
    df = data.copy()
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    palette = {g: SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
               for i, g in enumerate(df[group_col].unique())} if group_col else None

    if gene_col and gene_col in df.columns:
        sns.violinplot(
            data=df, x=gene_col, y=value_col, hue=group_col,
            palette=palette, ax=ax, inner=inner, split=split,
            linewidth=1, saturation=0.85,
        )
        sns.stripplot(
            data=df, x=gene_col, y=value_col, hue=group_col,
            palette=palette, ax=ax, dodge=True, size=2.5,
            alpha=0.3, jitter=True, legend=False,
        )
        plt.xticks(rotation=45, ha="right")
    elif group_col:
        if value_col is None:
            value_col = df.select_dtypes(include=[np.number]).columns[0]
        sns.violinplot(
            data=df, x=group_col, y=value_col,
            palette=palette, ax=ax, inner=inner, linewidth=1,
        )
        sns.stripplot(
            data=df, x=group_col, y=value_col,
            color="black", ax=ax, size=2.5, alpha=0.3, jitter=True,
        )

    style_axis(ax, title=title, ylabel=ylabel)
    add_watermark(fig)
    fig.tight_layout()

    stats = {"数据条数": len(df)}
    if value_col and group_col:
        for g in df[group_col].unique():
            vals = df.loc[df[group_col] == g, value_col]
            stats[f"{g} 中位数"] = f"{vals.median():.2f}"
    return fig, stats
