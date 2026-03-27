"""GO Enrichment Plot - GO富集分析图。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import BIO_PALETTE, SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_go_enrichment(
    data: pd.DataFrame,
    term_col: str = "Term",
    pvalue_col: str = "PValue",
    count_col: str = "Count",
    category_col: str = None,
    top_n: int = 20,
    plot_style: str = "bar",
    title: str = "GO 富集分析",
    figsize: tuple = (12, 8),
):
    """
    绘制GO富集分析图。

    Parameters
    ----------
    data : pd.DataFrame
        GO富集分析结果
    term_col : str
        GO术语列名
    pvalue_col : str
        P-value列名
    count_col : str
        基因数目列名
    category_col : str, optional
        GO类别列名（BP/MF/CC）
    top_n : int
        展示前N条通路
    plot_style : str
        图表样式：'bar' 或 'dot'
    title : str
        标题
    figsize : tuple
        图表尺寸
    """
    df = data.copy()
    df["-log10(pvalue)"] = -np.log10(df[pvalue_col].clip(lower=1e-300))
    df = df.nsmallest(top_n, pvalue_col)
    df = df.sort_values("-log10(pvalue)")

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if plot_style == "dot":
        if category_col and category_col in df.columns:
            categories = df[category_col].unique()
            for i, cat in enumerate(categories):
                mask = df[category_col] == cat
                ax.scatter(
                    df.loc[mask, "-log10(pvalue)"],
                    df.loc[mask, term_col],
                    s=df.loc[mask, count_col] * 10,
                    c=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                    alpha=0.7,
                    label=cat,
                    edgecolors="white",
                    linewidth=0.5,
                )
        else:
            scatter = ax.scatter(
                df["-log10(pvalue)"],
                df[term_col],
                s=df[count_col] * 10,
                c=df["-log10(pvalue)"],
                cmap="RdYlBu_r",
                alpha=0.7,
                edgecolors="white",
                linewidth=0.5,
            )
            plt.colorbar(scatter, ax=ax, label="-log₁₀(P-value)", shrink=0.8)

        style_axis(ax, title=title, xlabel="-log₁₀(P-value)", ylabel="")

    else:
        if category_col and category_col in df.columns:
            cat_colors = {
                cat: SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)]
                for i, cat in enumerate(df[category_col].unique())
            }
            colors = df[category_col].map(cat_colors)
            bars = ax.barh(df[term_col], df["-log10(pvalue)"], color=colors, height=0.7)

            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor=c, label=cat) for cat, c in cat_colors.items()]
            ax.legend(handles=legend_elements, title="GO 类别", loc="lower right")
        else:
            colors = plt.cm.RdYlBu_r(df["-log10(pvalue)"] / df["-log10(pvalue)"].max())
            ax.barh(df[term_col], df["-log10(pvalue)"], color=colors, height=0.7)

        for i, (val, count) in enumerate(zip(df["-log10(pvalue)"], df[count_col])):
            ax.text(val + 0.1, i, f"n={count}", va="center", fontsize=8)

        style_axis(ax, title=title, xlabel="-log₁₀(P-value)", ylabel="")

    ax.tick_params(axis="y", labelsize=9)
    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "展示通路数": len(df),
        "最显著通路": df.iloc[-1][term_col],
        "最低P值": f"{df[pvalue_col].min():.2e}",
    }
    if category_col and category_col in df.columns:
        stats["GO类别分布"] = df[category_col].value_counts().to_dict()

    return fig, stats
