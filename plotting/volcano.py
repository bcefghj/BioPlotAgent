"""Volcano Plot - 火山图：展示差异表达基因分析结果。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import BIO_PALETTE, style_axis, add_watermark


def plot_volcano(
    data: pd.DataFrame,
    log2fc_col: str = "log2FoldChange",
    pvalue_col: str = "pvalue",
    gene_col: str = None,
    fc_threshold: float = 1.0,
    pvalue_threshold: float = 0.05,
    title: str = "差异表达基因火山图",
    top_n_labels: int = 10,
    figsize: tuple = (10, 8),
):
    """
    绘制火山图。

    Parameters
    ----------
    data : pd.DataFrame
        差异表达分析结果，需包含 log2FC 和 p-value 列
    log2fc_col : str
        log2 fold change 列名
    pvalue_col : str
        p-value 列名
    gene_col : str, optional
        基因名称列名，用于标注
    fc_threshold : float
        fold change 阈值（绝对值）
    pvalue_threshold : float
        p-value 阈值
    title : str
        图表标题
    top_n_labels : int
        标注前N个显著基因
    figsize : tuple
        图表尺寸
    """
    df = data.copy()
    df["-log10(pvalue)"] = -np.log10(df[pvalue_col].clip(lower=1e-300))

    conditions = [
        (df[log2fc_col] >= fc_threshold) & (df[pvalue_col] < pvalue_threshold),
        (df[log2fc_col] <= -fc_threshold) & (df[pvalue_col] < pvalue_threshold),
    ]
    choices = ["上调 (Up)", "下调 (Down)"]
    df["group"] = np.select(conditions, choices, default="无显著变化 (NS)")

    color_map = {
        "上调 (Up)": BIO_PALETTE["up"],
        "下调 (Down)": BIO_PALETTE["down"],
        "无显著变化 (NS)": BIO_PALETTE["neutral"],
    }

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    for group, color in color_map.items():
        mask = df["group"] == group
        ax.scatter(
            df.loc[mask, log2fc_col],
            df.loc[mask, "-log10(pvalue)"],
            c=color,
            s=15,
            alpha=0.6,
            label=f"{group} ({mask.sum()})",
            edgecolors="none",
        )

    ax.axhline(y=-np.log10(pvalue_threshold), color="grey", linestyle="--", linewidth=0.8)
    ax.axvline(x=fc_threshold, color="grey", linestyle="--", linewidth=0.8)
    ax.axvline(x=-fc_threshold, color="grey", linestyle="--", linewidth=0.8)

    if gene_col and gene_col in df.columns:
        sig_genes = df[df["group"] != "无显著变化 (NS)"].nlargest(top_n_labels, "-log10(pvalue)")
        try:
            from adjustText import adjust_text

            texts = []
            for _, row in sig_genes.iterrows():
                texts.append(
                    ax.annotate(
                        row[gene_col],
                        (row[log2fc_col], row["-log10(pvalue)"]),
                        fontsize=7,
                        alpha=0.8,
                    )
                )
            adjust_text(texts, arrowprops=dict(arrowstyle="-", color="grey", lw=0.5))
        except ImportError:
            for _, row in sig_genes.iterrows():
                ax.annotate(
                    row[gene_col],
                    (row[log2fc_col], row["-log10(pvalue)"]),
                    fontsize=7,
                    alpha=0.8,
                    xytext=(5, 5),
                    textcoords="offset points",
                )

    style_axis(ax, title=title, xlabel="log₂(Fold Change)", ylabel="-log₁₀(P-value)")
    ax.legend(loc="upper right", framealpha=0.9, fontsize=10)
    add_watermark(fig)
    fig.tight_layout()

    up_count = (df["group"] == "上调 (Up)").sum()
    down_count = (df["group"] == "下调 (Down)").sum()
    stats = {
        "上调基因数": up_count,
        "下调基因数": down_count,
        "总显著基因数": up_count + down_count,
        "总基因数": len(df),
    }

    return fig, stats
