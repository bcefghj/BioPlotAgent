"""Box Plot - 箱线图：展示数据分布和组间差异。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_box(
    data: pd.DataFrame,
    value_col: str = None,
    group_col: str = None,
    gene_col: str = None,
    title: str = "基因表达箱线图",
    ylabel: str = "表达量",
    show_points: bool = True,
    figsize: tuple = (10, 7),
):
    """
    绘制箱线图。

    Parameters
    ----------
    data : pd.DataFrame
        数据
    value_col : str
        数值列名
    group_col : str
        分组列名
    gene_col : str, optional
        基因列名（用于多基因对比）
    title : str
        标题
    ylabel : str
        Y轴标签
    show_points : bool
        是否显示数据点
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    palette = {g: SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
               for i, g in enumerate(df[group_col].unique())} if group_col else None

    if gene_col and gene_col in df.columns:
        sns.boxplot(
            data=df, x=gene_col, y=value_col, hue=group_col,
            palette=palette, ax=ax, width=0.6, linewidth=1.2,
        )
        if show_points:
            sns.stripplot(
                data=df, x=gene_col, y=value_col, hue=group_col,
                palette=palette, ax=ax, dodge=True, size=4,
                alpha=0.5, jitter=True, legend=False,
            )
        plt.xticks(rotation=45, ha="right")
    elif group_col:
        if value_col is None:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            value_col = numeric_cols[0]

        sns.boxplot(
            data=df, x=group_col, y=value_col,
            palette=palette, ax=ax, width=0.5, linewidth=1.2,
        )
        if show_points:
            sns.stripplot(
                data=df, x=group_col, y=value_col,
                color="black", ax=ax, size=4, alpha=0.4, jitter=True,
            )
    else:
        numeric_df = df.select_dtypes(include=[np.number])
        sns.boxplot(data=numeric_df, ax=ax, palette=SEQUENTIAL_COLORS[:len(numeric_df.columns)])
        plt.xticks(rotation=45, ha="right")

    style_axis(ax, title=title, ylabel=ylabel)
    add_watermark(fig)
    fig.tight_layout()

    stats = {}
    if value_col and group_col:
        for group in df[group_col].unique():
            vals = df.loc[df[group_col] == group, value_col]
            stats[f"{group} 中位数"] = f"{vals.median():.2f}"
            stats[f"{group} 均值"] = f"{vals.mean():.2f}"

    return fig, stats
