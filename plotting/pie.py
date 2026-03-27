"""Pie / Donut Chart - 饼图/环形图：展示比例分布。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import SEQUENTIAL_COLORS, add_watermark


def plot_pie(
    data: pd.DataFrame,
    label_col: str = None,
    value_col: str = None,
    donut: bool = False,
    title: str = "比例分布图",
    top_n: int = 10,
    figsize: tuple = (9, 9),
):
    df = data.copy()
    if label_col is None:
        label_col = df.columns[0]
    if value_col is None:
        value_col = df.select_dtypes(include=[np.number]).columns[0]

    if len(df) > top_n:
        df = df.nlargest(top_n - 1, value_col)
        others = data[~data.index.isin(df.index)][value_col].sum()
        other_row = pd.DataFrame({label_col: ["其他"], value_col: [others]})
        df = pd.concat([df, other_row], ignore_index=True)

    fig, ax = plt.subplots(figsize=figsize, facecolor="white")
    colors = SEQUENTIAL_COLORS[:len(df)]

    wedges, texts, autotexts = ax.pie(
        df[value_col], labels=df[label_col], colors=colors,
        autopct="%1.1f%%", startangle=90, pctdistance=0.75 if donut else 0.6,
        textprops={"fontsize": 10},
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for t in autotexts:
        t.set_fontsize(9)
        t.set_color("white" if not donut else "#333")

    if donut:
        centre_circle = plt.Circle((0, 0), 0.50, fc="white")
        ax.add_artist(centre_circle)
        ax.text(0, 0, f"总计\n{df[value_col].sum():.0f}", ha="center", va="center",
                fontsize=16, fontweight="bold", color="#2C3E50")

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    add_watermark(fig)

    stats = {"类别数": len(df), "总计": f"{df[value_col].sum():.0f}",
             "最大占比": f"{df[value_col].max() / df[value_col].sum() * 100:.1f}%"}
    return fig, stats
