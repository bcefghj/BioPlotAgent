"""MA Plot - 展示差异表达与平均表达量的关系。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import BIO_PALETTE, style_axis, add_watermark


def plot_ma(
    data: pd.DataFrame,
    log2fc_col: str = "log2FoldChange",
    basemean_col: str = "baseMean",
    pvalue_col: str = "pvalue",
    fc_threshold: float = 1.0,
    pvalue_threshold: float = 0.05,
    title: str = "MA Plot",
    figsize: tuple = (10, 8),
):
    """
    绘制MA Plot。

    Parameters
    ----------
    data : pd.DataFrame
        差异表达结果数据
    log2fc_col : str
        log2 fold change 列名
    basemean_col : str
        平均表达量列名
    pvalue_col : str
        p-value 列名
    fc_threshold : float
        FC阈值
    pvalue_threshold : float
        p-value 阈值
    title : str
        标题
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    sig_up = (df[log2fc_col] >= fc_threshold) & (df[pvalue_col] < pvalue_threshold)
    sig_down = (df[log2fc_col] <= -fc_threshold) & (df[pvalue_col] < pvalue_threshold)
    ns = ~sig_up & ~sig_down

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    ax.scatter(
        np.log10(df.loc[ns, basemean_col].clip(lower=1e-10)),
        df.loc[ns, log2fc_col],
        c=BIO_PALETTE["neutral"], s=10, alpha=0.4,
        label=f"无显著变化 ({ns.sum()})",
    )
    ax.scatter(
        np.log10(df.loc[sig_up, basemean_col].clip(lower=1e-10)),
        df.loc[sig_up, log2fc_col],
        c=BIO_PALETTE["up"], s=15, alpha=0.6,
        label=f"上调 ({sig_up.sum()})",
    )
    ax.scatter(
        np.log10(df.loc[sig_down, basemean_col].clip(lower=1e-10)),
        df.loc[sig_down, log2fc_col],
        c=BIO_PALETTE["down"], s=15, alpha=0.6,
        label=f"下调 ({sig_down.sum()})",
    )

    ax.axhline(y=0, color="black", linewidth=0.8)
    ax.axhline(y=fc_threshold, color="grey", linestyle="--", linewidth=0.6)
    ax.axhline(y=-fc_threshold, color="grey", linestyle="--", linewidth=0.6)

    style_axis(ax, title=title, xlabel="log₁₀(平均表达量)", ylabel="log₂(Fold Change)")
    ax.legend(loc="upper right", framealpha=0.9)
    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "上调基因": int(sig_up.sum()),
        "下调基因": int(sig_down.sum()),
        "总基因数": len(df),
    }

    return fig, stats
