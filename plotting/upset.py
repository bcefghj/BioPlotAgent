"""UpSet Plot - 集合交叉可视化（Venn图替代方案，支持多组）。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from .utils import BIO_PALETTE, SEQUENTIAL_COLORS, add_watermark


def plot_upset(
    sets: dict,
    min_size: int = 1,
    title: str = "UpSet Plot (集合交叉分析)",
    figsize: tuple = (14, 8),
):
    set_names = list(sets.keys())
    n_sets = len(set_names)
    all_elements = set()
    for s in sets.values():
        all_elements |= s

    membership = {}
    for elem in all_elements:
        key = tuple(1 if elem in sets[name] else 0 for name in set_names)
        membership.setdefault(key, set()).add(elem)

    combos = [(k, len(v)) for k, v in membership.items() if len(v) >= min_size]
    combos.sort(key=lambda x: x[1], reverse=True)
    if len(combos) > 30:
        combos = combos[:30]

    fig = plt.figure(figsize=figsize, facecolor="white")
    gs = fig.add_gridspec(2, 2, height_ratios=[3, 1.2], width_ratios=[0.2, 1],
                          hspace=0.05, wspace=0.05)

    ax_bar = fig.add_subplot(gs[0, 1])
    ax_matrix = fig.add_subplot(gs[1, 1], sharex=ax_bar)
    ax_sets = fig.add_subplot(gs[1, 0], sharey=ax_matrix)

    x = np.arange(len(combos))
    sizes = [c[1] for c in combos]
    bar_colors = [BIO_PALETTE["primary"] if sum(c[0]) > 1 else BIO_PALETTE["neutral"] for c in combos]
    ax_bar.bar(x, sizes, color=bar_colors, width=0.6, edgecolor="white")
    for i, s in enumerate(sizes):
        ax_bar.text(i, s + max(sizes) * 0.02, str(s), ha="center", va="bottom", fontsize=8)
    ax_bar.set_ylabel("交叉大小", fontsize=11)
    ax_bar.spines["top"].set_visible(False)
    ax_bar.spines["right"].set_visible(False)
    ax_bar.set_xticks([])

    for i, (combo, _) in enumerate(combos):
        for j in range(n_sets):
            if combo[j]:
                ax_matrix.scatter(i, j, s=80, c=BIO_PALETTE["primary"], zorder=5, edgecolors="white")
            else:
                ax_matrix.scatter(i, j, s=30, c="#E0E0E0", zorder=5)
        active = [j for j in range(n_sets) if combo[j]]
        if len(active) > 1:
            ax_matrix.plot([i, i], [min(active), max(active)],
                           color=BIO_PALETTE["primary"], linewidth=1.5, zorder=3)

    ax_matrix.set_yticks(range(n_sets))
    ax_matrix.set_yticklabels([])
    ax_matrix.set_xticks([])
    ax_matrix.spines["top"].set_visible(False)
    ax_matrix.spines["right"].set_visible(False)
    ax_matrix.spines["bottom"].set_visible(False)
    ax_matrix.set_ylim(-0.5, n_sets - 0.5)
    for spine in ax_matrix.spines.values():
        spine.set_visible(False)
    ax_matrix.grid(axis="y", alpha=0.15)

    set_sizes = [len(sets[name]) for name in set_names]
    ax_sets.barh(range(n_sets), set_sizes, color=SEQUENTIAL_COLORS[:n_sets], height=0.6, edgecolor="white")
    ax_sets.set_yticks(range(n_sets))
    ax_sets.set_yticklabels(set_names, fontsize=10)
    ax_sets.invert_xaxis()
    ax_sets.set_xlabel("集合大小", fontsize=10)
    ax_sets.spines["top"].set_visible(False)
    ax_sets.spines["right"].set_visible(False)

    fig.suptitle(title, fontsize=14, fontweight="bold")
    add_watermark(fig)

    stats = {"集合数": n_sets, "交叉组合数": len(combos), "总元素数": len(all_elements)}
    return fig, stats
