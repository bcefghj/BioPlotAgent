"""Correlation Heatmap - 相关性热图：展示基因/样本间的相关系数。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import style_axis, add_watermark


def plot_correlation_heatmap(
    data: pd.DataFrame,
    method: str = "pearson",
    annot: bool = True,
    mask_upper: bool = True,
    cmap: str = "RdBu_r",
    title: str = "基因/样本相关性热图",
    figsize: tuple = (10, 9),
):
    df = data.select_dtypes(include=[np.number]).copy()
    corr = df.corr(method=method)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    mask = None
    if mask_upper:
        mask = np.triu(np.ones_like(corr, dtype=bool), k=1)

    sns.heatmap(
        corr, mask=mask, annot=annot, fmt=".2f",
        cmap=cmap, center=0, vmin=-1, vmax=1,
        square=True, linewidths=0.5, linecolor="white",
        ax=ax, cbar_kws={"shrink": 0.8, "label": f"{method.title()} 相关系数"},
        annot_kws={"size": 8},
    )
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=9)
    plt.setp(ax.get_yticklabels(), fontsize=9)
    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "变量数": len(corr),
        "方法": method,
        "最高相关": f"{corr.where(~np.eye(len(corr), dtype=bool)).max().max():.3f}",
        "最低相关": f"{corr.where(~np.eye(len(corr), dtype=bool)).min().min():.3f}",
    }
    return fig, stats
