"""Heatmap - 热图：展示基因表达模式。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .utils import style_axis, add_watermark


def plot_heatmap(
    data: pd.DataFrame,
    gene_col: str = None,
    sample_cols: list = None,
    normalize: bool = True,
    cluster_rows: bool = True,
    cluster_cols: bool = True,
    cmap: str = "RdBu_r",
    title: str = "基因表达热图",
    top_n_genes: int = 50,
    figsize: tuple = (12, 10),
):
    """
    绘制基因表达热图。

    Parameters
    ----------
    data : pd.DataFrame
        表达矩阵数据
    gene_col : str, optional
        基因名称列名，设为index
    sample_cols : list, optional
        样本列名列表，默认使用所有数值列
    normalize : bool
        是否进行Z-score标准化
    cluster_rows : bool
        是否对行（基因）聚类
    cluster_cols : bool
        是否对列（样本）聚类
    cmap : str
        颜色映射
    title : str
        标题
    top_n_genes : int
        展示方差最大的前N个基因
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    if gene_col and gene_col in df.columns:
        df = df.set_index(gene_col)

    if sample_cols:
        df = df[sample_cols]
    else:
        df = df.select_dtypes(include=[np.number])

    if len(df) > top_n_genes:
        variances = df.var(axis=1)
        df = df.loc[variances.nlargest(top_n_genes).index]

    if normalize:
        df = df.apply(lambda x: (x - x.mean()) / x.std(), axis=1)
        df = df.fillna(0)

    g = sns.clustermap(
        df,
        cmap=cmap,
        figsize=figsize,
        row_cluster=cluster_rows,
        col_cluster=cluster_cols,
        xticklabels=True,
        yticklabels=True if len(df) <= 50 else False,
        linewidths=0.5,
        linecolor="white",
        dendrogram_ratio=(0.1, 0.1),
        cbar_kws={"label": "Z-score" if normalize else "表达量"},
    )

    g.fig.suptitle(title, fontsize=14, fontweight="bold", y=1.02)
    add_watermark(g.fig)

    plt.setp(g.ax_heatmap.get_xticklabels(), rotation=45, ha="right", fontsize=9)
    plt.setp(g.ax_heatmap.get_yticklabels(), fontsize=8)

    stats = {
        "展示基因数": len(df),
        "样本数": len(df.columns),
        "标准化": "Z-score" if normalize else "原始值",
    }

    return g.fig, stats
