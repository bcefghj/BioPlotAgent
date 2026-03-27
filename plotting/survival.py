"""Survival Analysis - 生存分析曲线（Kaplan-Meier Plot）。"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from .utils import SEQUENTIAL_COLORS, style_axis, add_watermark


def plot_survival(
    data: pd.DataFrame,
    time_col: str = "time",
    event_col: str = "event",
    group_col: str = "group",
    title: str = "Kaplan-Meier 生存分析曲线",
    ci_show: bool = True,
    at_risk: bool = True,
    figsize: tuple = (10, 7),
):
    """
    绘制Kaplan-Meier生存曲线。

    Parameters
    ----------
    data : pd.DataFrame
        生存数据，需包含时间、事件状态和分组列
    time_col : str
        生存时间列名
    event_col : str
        事件状态列名（1=事件发生，0=删失）
    group_col : str
        分组列名
    title : str
        标题
    ci_show : bool
        是否显示置信区间
    at_risk : bool
        是否显示风险人数表
    figsize : tuple
        图表尺寸
    """
    df = data.copy()

    if at_risk:
        fig, axes = plt.subplots(
            2, 1,
            figsize=figsize,
            gridspec_kw={"height_ratios": [3, 1]},
            facecolor="white",
        )
        ax_main = axes[0]
        ax_table = axes[1]
    else:
        fig, ax_main = plt.subplots(figsize=figsize, facecolor="white")

    groups = df[group_col].unique()
    kmf_results = {}

    for i, group in enumerate(groups):
        mask = df[group_col] == group
        kmf = KaplanMeierFitter()
        kmf.fit(
            df.loc[mask, time_col],
            event_observed=df.loc[mask, event_col],
            label=str(group),
        )
        kmf.plot_survival_function(
            ax=ax_main,
            ci_show=ci_show,
            color=SEQUENTIAL_COLORS[i % len(SEQUENTIAL_COLORS)],
            linewidth=2,
        )
        kmf_results[group] = kmf

    p_value = None
    if len(groups) == 2:
        g1, g2 = groups[0], groups[1]
        m1, m2 = df[group_col] == g1, df[group_col] == g2
        result = logrank_test(
            df.loc[m1, time_col], df.loc[m2, time_col],
            event_observed_A=df.loc[m1, event_col],
            event_observed_B=df.loc[m2, event_col],
        )
        p_value = result.p_value
        p_text = f"p = {p_value:.2e}" if p_value < 0.001 else f"p = {p_value:.4f}"
        ax_main.text(
            0.95, 0.95,
            f"Log-rank test\n{p_text}",
            transform=ax_main.transAxes,
            fontsize=10,
            verticalalignment="top",
            horizontalalignment="right",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.8),
        )

    style_axis(ax_main, title=title, xlabel="时间", ylabel="生存概率")
    ax_main.set_ylim(-0.05, 1.05)
    ax_main.legend(title="分组", loc="lower left", framealpha=0.9)

    if at_risk:
        time_points = np.linspace(0, df[time_col].max(), 6).astype(int)
        table_data = []
        for group in groups:
            mask = df[group_col] == group
            row = []
            for t in time_points:
                n_at_risk = ((df.loc[mask, time_col] >= t)).sum()
                row.append(str(n_at_risk))
            table_data.append(row)

        ax_table.axis("off")
        table = ax_table.table(
            cellText=table_data,
            rowLabels=[str(g) for g in groups],
            colLabels=[str(t) for t in time_points],
            loc="center",
            cellLoc="center",
        )
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.5)
        ax_table.set_title("风险人数 (Number at Risk)", fontsize=10, pad=5)

    add_watermark(fig)
    fig.tight_layout()

    stats = {
        "分组数": len(groups),
        "总样本数": len(df),
        "事件数": int(df[event_col].sum()),
    }
    if p_value is not None:
        stats["Log-rank p值"] = f"{p_value:.4e}"

    return fig, stats
