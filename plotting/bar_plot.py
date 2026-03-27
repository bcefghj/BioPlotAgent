"""Bar Plot - 柱状图：展示基因表达量或统计数据。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_bar(
    data: pd.DataFrame,
    x_col: str = None,
    y_col: str = None,
    group_col: str = None,
    error_col: str = None,
    title: str = "基因表达柱状图",
    xlabel: str = "",
    ylabel: str = "表达量",
    horizontal: bool = False,
    figsize: tuple = (10, 7),
):
    """
    绘制柱状图。

    Parameters
    ----------
    data : pd.DataFrame
        数据
    x_col : str
        X轴列名（如基因名）
    y_col : str
        Y轴列名（如表达量）
    group_col : str, optional
        分组列名
    error_col : str, optional
        误差棒列名
    title : str
        标题
    xlabel : str
        X轴标签
    ylabel : str
        Y轴标签
    horizontal : bool
        是否水平绘制
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    if x_col is None:
        x_col = df.columns[0]
    if y_col is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        y_col = numeric_cols[0] if len(numeric_cols) > 0 else df.columns[1]

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if group_col and group_col in df.columns:
        groups = df[group_col].unique()
        x_vals = df[x_col].unique()
        width = 0.8 / len(groups)

        for i, group in enumerate(groups):
            mask = df[group_col] == group
            positions = np.arange(len(x_vals)) + i * width - (len(groups) - 1) * width / 2

            yerr = df.loc[mask, error_col].values if error_col and error_col in df.columns else None

            if horizontal:
                ax.barh(
                    positions, df.loc[mask, y_col], height=width * 0.9,
                    color=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                    xerr=yerr, capsize=3, label=str(group), alpha=0.85,
                )
            else:
                ax.bar(
                    positions, df.loc[mask, y_col], width=width * 0.9,
                    color=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                    yerr=yerr, capsize=3, label=str(group), alpha=0.85,
                )

        if horizontal:
            ax.set_yticks(range(len(x_vals)))
            ax.set_yticklabels(x_vals)
        else:
            ax.set_xticks(range(len(x_vals)))
            ax.set_xticklabels(x_vals, rotation=45, ha="right")

        ax.legend(title="分组")
    else:
        yerr = df[error_col].values if error_col and error_col in df.columns else None

        if horizontal:
            ax.barh(
                df[x_col], df[y_col],
                color=SEQUENTIAL_COLORS[:len(df)],
                xerr=yerr, capsize=3, alpha=0.85,
            )
        else:
            ax.bar(
                df[x_col], df[y_col],
                color=SEQUENTIAL_COLORS[:len(df)],
                yerr=yerr, capsize=3, alpha=0.85,
            )
            plt.xticks(rotation=45, ha="right")

    style_axis(
        ax, title=title,
        xlabel=ylabel if horizontal else xlabel,
        ylabel=xlabel if horizontal else ylabel,
    )
    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "数据条数": len(df),
        "最大值": f"{df[y_col].max():.2f}",
        "最小值": f"{df[y_col].min():.2f}",
        "平均值": f"{df[y_col].mean():.2f}",
    }

    return fig, stats
