"""Sankey / Alluvial Plot - 桑基图/冲积图：流量和分类关系可视化。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from .utils import SEQUENTIAL_COLORS, add_watermark


def plot_sankey(
    data: pd.DataFrame,
    source_col: str = "source",
    target_col: str = "target",
    value_col: str = "value",
    title: str = "桑基图 (Sankey Diagram)",
    figsize: tuple = (12, 8),
):
    """Simplified alluvial/sankey using matplotlib."""
    df = data.copy()
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    sources = df[source_col].unique()
    targets = df[target_col].unique()
    all_nodes = list(sources) + [t for t in targets if t not in sources]

    src_totals = df.groupby(source_col)[value_col].sum()
    tgt_totals = df.groupby(target_col)[value_col].sum()

    left_y, right_y = {}, {}
    gap = 0.02
    total_left = src_totals.sum()
    y = 0
    for s in sources:
        h = src_totals[s] / total_left
        left_y[s] = (y, y + h)
        y += h + gap

    total_right = tgt_totals.sum()
    y = 0
    for t in targets:
        h = tgt_totals[t] / total_right
        right_y[t] = (y, y + h)
        y += h + gap

    left_cursor = {s: left_y[s][0] for s in sources}
    right_cursor = {t: right_y[t][0] for t in targets}

    for i, (_, row) in enumerate(df.iterrows()):
        s, t, v = row[source_col], row[target_col], row[value_col]
        lh = (v / total_left)
        rh = (v / total_right)
        ly0, ry0 = left_cursor[s], right_cursor[t]
        color = SEQUENTIAL_COLORS[list(sources).index(s) % len(SEQUENTIAL_COLORS)]

        from matplotlib.path import Path
        verts = [
            (0.15, ly0), (0.4, ly0), (0.6, ry0), (0.85, ry0),
            (0.85, ry0 + rh), (0.6, ry0 + rh), (0.4, ly0 + lh), (0.15, ly0 + lh),
            (0.15, ly0),
        ]
        codes = [Path.MOVETO] + [Path.CURVE4] * 3 + [Path.LINETO] + [Path.CURVE4] * 3 + [Path.CLOSEPOLY]
        path = Path(verts, codes)
        patch = mpatches.PathPatch(path, facecolor=color, alpha=0.4, edgecolor="none")
        ax.add_patch(patch)

        left_cursor[s] += lh
        right_cursor[t] += rh

    bar_w = 0.04
    for s in sources:
        y0, y1 = left_y[s]
        color = SEQUENTIAL_COLORS[list(sources).index(s) % len(SEQUENTIAL_COLORS)]
        ax.barh(y0, bar_w, height=y1 - y0, left=0.15 - bar_w, color=color, edgecolor="white", linewidth=0.5)
        ax.text(0.15 - bar_w - 0.01, (y0 + y1) / 2, s, ha="right", va="center", fontsize=10)

    for j, t in enumerate(targets):
        y0, y1 = right_y[t]
        color = SEQUENTIAL_COLORS[(len(sources) + j) % len(SEQUENTIAL_COLORS)]
        ax.barh(y0, bar_w, height=y1 - y0, left=0.85, color=color, edgecolor="white", linewidth=0.5)
        ax.text(0.85 + bar_w + 0.01, (y0 + y1) / 2, t, ha="left", va="center", fontsize=10)

    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.05, max(y, 1.1))
    ax.axis("off")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    add_watermark(fig)
    fig.tight_layout()

    stats = {"源节点数": len(sources), "目标节点数": len(targets), "连接数": len(df)}
    return fig, stats
