"""Dot Plot / Bubble Chart - 气泡图：多维数据可视化。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import style_axis, add_watermark


def plot_dot(
    data: pd.DataFrame,
    x_col: str = None,
    y_col: str = None,
    size_col: str = None,
    color_col: str = None,
    title: str = "富集分析气泡图",
    xlabel: str = "",
    ylabel: str = "",
    cmap: str = "RdYlBu_r",
    figsize: tuple = (10, 8),
):
    """
    绘制气泡图。

    Parameters
    ----------
    data : pd.DataFrame
        数据
    x_col : str
        X轴列名（如 Rich Factor）
    y_col : str
        Y轴列名（如 Pathway）
    size_col : str
        气泡大小列名（如 Count）
    color_col : str
        气泡颜色列名（如 -log10(pvalue)）
    title : str
        标题
    xlabel, ylabel : str
        轴标签
    cmap : str
        颜色映射
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    cols = df.columns.tolist()
    if x_col is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        x_col = numeric_cols[0] if len(numeric_cols) > 0 else cols[1]
    if y_col is None:
        non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
        y_col = non_numeric_cols[0] if len(non_numeric_cols) > 0 else cols[0]
    if size_col is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        size_col = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
    if color_col is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        color_col = numeric_cols[-1] if len(numeric_cols) > 0 else None

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    sizes = df[size_col]
    size_scale = (sizes - sizes.min()) / (sizes.max() - sizes.min() + 1e-10) * 300 + 50

    if color_col:
        scatter = ax.scatter(
            df[x_col], df[y_col],
            s=size_scale, c=df[color_col],
            cmap=cmap, alpha=0.7,
            edgecolors="white", linewidth=0.5,
        )
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
        cbar.set_label(color_col, fontsize=10)
    else:
        ax.scatter(
            df[x_col], df[y_col],
            s=size_scale, c="#3498DB",
            alpha=0.7, edgecolors="white", linewidth=0.5,
        )

    size_legend_values = [sizes.min(), sizes.median(), sizes.max()]
    size_legend_scaled = [(v - sizes.min()) / (sizes.max() - sizes.min() + 1e-10) * 300 + 50
                          for v in size_legend_values]
    for val, s in zip(size_legend_values, size_legend_scaled):
        ax.scatter([], [], s=s, c="grey", alpha=0.5, label=f"{size_col}={val:.0f}")
    ax.legend(title="大小图例", loc="lower right", framealpha=0.9, fontsize=9)

    style_axis(ax, title=title, xlabel=xlabel or x_col, ylabel=ylabel or "")
    ax.tick_params(axis="y", labelsize=9)
    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "数据条数": len(df),
        f"{x_col} 范围": f"{df[x_col].min():.2f} ~ {df[x_col].max():.2f}",
    }

    return fig, stats
