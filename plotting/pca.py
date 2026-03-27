"""PCA Plot - 主成分分析图：展示样本整体差异。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_pca(
    data: pd.DataFrame,
    group_col: str = None,
    sample_col: str = None,
    n_components: int = 2,
    title: str = "PCA 主成分分析图",
    show_labels: bool = True,
    figsize: tuple = (10, 8),
):
    """
    绘制PCA分析图。

    Parameters
    ----------
    data : pd.DataFrame
        表达矩阵（行=样本，列=基因/特征）或（行=基因，列=样本）
    group_col : str, optional
        分组列名
    sample_col : str, optional
        样本名列名
    n_components : int
        主成分数量
    title : str
        标题
    show_labels : bool
        是否显示样本标签
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    group_info = None
    sample_names = None

    if group_col and group_col in df.columns:
        group_info = df[group_col].values
        df = df.drop(columns=[group_col])
    if sample_col and sample_col in df.columns:
        sample_names = df[sample_col].values
        df = df.drop(columns=[sample_col])

    numeric_df = df.select_dtypes(include=[np.number])

    if numeric_df.shape[0] < numeric_df.shape[1]:
        numeric_df = numeric_df.T
        if sample_names is None:
            sample_names = data.columns[df.columns.isin(numeric_df.index) | True]

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(numeric_df)

    pca = PCA(n_components=min(n_components, min(scaled_data.shape)))
    pca_result = pca.fit_transform(scaled_data)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if group_info is not None and len(group_info) == len(pca_result):
        groups = pd.Series(group_info)
        unique_groups = groups.unique()
        for i, group in enumerate(unique_groups):
            mask = groups == group
            ax.scatter(
                pca_result[mask, 0],
                pca_result[mask, 1],
                c=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                s=80,
                alpha=0.7,
                label=group,
                edgecolors="white",
                linewidth=0.5,
            )
    else:
        ax.scatter(
            pca_result[:, 0],
            pca_result[:, 1],
            c=SEQUENTIAL_COLORS[0],
            s=80,
            alpha=0.7,
            edgecolors="white",
            linewidth=0.5,
        )

    if show_labels and sample_names is not None and len(sample_names) == len(pca_result):
        for i, name in enumerate(sample_names):
            ax.annotate(
                str(name),
                (pca_result[i, 0], pca_result[i, 1]),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
                alpha=0.8,
            )

    var_explained = pca.explained_variance_ratio_ * 100
    style_axis(
        ax,
        title=title,
        xlabel=f"PC1 ({var_explained[0]:.1f}%)",
        ylabel=f"PC2 ({var_explained[1]:.1f}%)" if len(var_explained) > 1 else "PC2",
    )

    if group_info is not None:
        ax.legend(title="分组", loc="best", framealpha=0.9)

    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "PC1 解释方差": f"{var_explained[0]:.1f}%",
        "PC2 解释方差": f"{var_explained[1]:.1f}%" if len(var_explained) > 1 else "N/A",
        "样本数": len(pca_result),
        "特征数": numeric_df.shape[1],
    }

    return fig, stats
