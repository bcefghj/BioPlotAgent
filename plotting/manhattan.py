"""Manhattan Plot - 曼哈顿图：全基因组关联研究(GWAS)结果展示。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import style_axis, add_watermark


CHR_COLORS = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
              "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"]


def plot_manhattan(
    data: pd.DataFrame,
    chr_col: str = "chr",
    pos_col: str = "pos",
    pvalue_col: str = "pvalue",
    gene_col: str = None,
    sig_threshold: float = 5e-8,
    sug_threshold: float = 1e-5,
    title: str = "曼哈顿图 (Manhattan Plot)",
    top_n_labels: int = 5,
    figsize: tuple = (16, 6),
):
    df = data.copy()
    df["-log10p"] = -np.log10(df[pvalue_col].clip(lower=1e-300))

    chr_order = sorted(df[chr_col].unique(), key=lambda x: int(str(x).replace("chr", "")) if str(x).replace("chr", "").isdigit() else 99)
    df[chr_col] = pd.Categorical(df[chr_col], categories=chr_order, ordered=True)
    df = df.sort_values([chr_col, pos_col])

    offset = 0
    x_positions = []
    chr_centers = {}
    for chrom in chr_order:
        mask = df[chr_col] == chrom
        positions = df.loc[mask, pos_col].values
        x_positions.extend(positions + offset)
        chr_centers[chrom] = offset + (positions.max() - positions.min()) / 2 + positions.min()
        offset += positions.max() + 1e6

    df["x_plot"] = x_positions

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    for i, chrom in enumerate(chr_order):
        mask = df[chr_col] == chrom
        color = CHR_COLORS[i % len(CHR_COLORS)]
        ax.scatter(df.loc[mask, "x_plot"], df.loc[mask, "-log10p"],
                   c=color, s=8, alpha=0.6, edgecolors="none")

    ax.axhline(y=-np.log10(sig_threshold), color="red", linestyle="--", linewidth=0.8, label=f"显著 (p={sig_threshold})")
    ax.axhline(y=-np.log10(sug_threshold), color="blue", linestyle="--", linewidth=0.6, alpha=0.5, label=f"建议 (p={sug_threshold})")

    if gene_col and gene_col in df.columns:
        sig = df[df[pvalue_col] < sig_threshold].nsmallest(top_n_labels, pvalue_col)
        for _, row in sig.iterrows():
            ax.annotate(row[gene_col], (row["x_plot"], row["-log10p"]),
                        fontsize=7, xytext=(3, 5), textcoords="offset points")

    ax.set_xticks([chr_centers[c] for c in chr_order])
    ax.set_xticklabels([str(c).replace("chr", "") for c in chr_order], fontsize=8)
    ax.set_xlim(df["x_plot"].min() - 1e6, df["x_plot"].max() + 1e6)

    style_axis(ax, title=title, xlabel="染色体", ylabel="-log₁₀(P-value)")
    ax.legend(loc="upper right", fontsize=9)
    add_watermark(fig)
    fig.tight_layout()

    n_sig = (df[pvalue_col] < sig_threshold).sum()
    stats = {"SNP总数": len(df), "显著SNP": int(n_sig), "染色体数": len(chr_order)}
    return fig, stats
