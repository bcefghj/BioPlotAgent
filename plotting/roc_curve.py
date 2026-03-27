"""ROC Curve - 受试者工作特征曲线：诊断/分类模型评估。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_roc(
    data: pd.DataFrame,
    true_col: str = "true_label",
    score_cols: list = None,
    title: str = "ROC 曲线",
    figsize: tuple = (8, 8),
):
    df = data.copy()
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    if score_cols is None:
        score_cols = [c for c in df.select_dtypes(include=[np.number]).columns if c != true_col]

    results = {}
    for i, col in enumerate(score_cols):
        fpr, tpr, _ = roc_curve(df[true_col], df[col])
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, color=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
                linewidth=2, label=f"{col} (AUC = {roc_auc:.3f})")
        results[col] = roc_auc

    ax.plot([0, 1], [0, 1], color="grey", linestyle="--", linewidth=1, alpha=0.5)
    ax.fill_between([0, 1], [0, 1], alpha=0.05, color="grey")

    style_axis(ax, title=title, xlabel="假阳性率 (1 - 特异度)", ylabel="真阳性率 (灵敏度)")
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.set_aspect("equal")
    ax.legend(loc="lower right", framealpha=0.9, fontsize=10)
    add_watermark(fig)
    fig.tight_layout()

    stats = {f"{col} AUC": f"{v:.3f}" for col, v in results.items()}
    stats["模型数"] = len(score_cols)
    return fig, stats
