"""Venn Diagram - 韦恩图：展示基因集合重叠关系。"""

import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from .utils import BIO_PALETTE, add_watermark


def plot_venn(
    sets: dict,
    title: str = "基因集合韦恩图",
    figsize: tuple = (8, 8),
):
    """
    绘制韦恩图。

    Parameters
    ----------
    sets : dict
        集合字典，如 {"Group A": {"gene1", "gene2"}, "Group B": {"gene2", "gene3"}}
        支持2或3组
    title : str
        标题
    figsize : tuple
        图表尺寸
    """
    fig, ax = plt.subplots(figsize=figsize, facecolor="white")

    names = list(sets.keys())
    set_values = [sets[name] for name in names]

    colors_2 = (BIO_PALETTE["up"], BIO_PALETTE["down"])
    colors_3 = (BIO_PALETTE["up"], BIO_PALETTE["down"], BIO_PALETTE["accent"])

    if len(set_values) == 2:
        v = venn2(set_values, set_labels=names, ax=ax)
        for i, patch_id in enumerate(["10", "01", "11"]):
            patch = v.get_patch_by_id(patch_id)
            if patch:
                color_idx = 0 if patch_id[0] == "1" else 1
                if patch_id == "11":
                    patch.set_color(BIO_PALETTE["highlight"])
                else:
                    patch.set_color(colors_2[color_idx])
                patch.set_alpha(0.5)

    elif len(set_values) == 3:
        v = venn3(set_values, set_labels=names, ax=ax)
        for patch_id in ["100", "010", "001", "110", "101", "011", "111"]:
            patch = v.get_patch_by_id(patch_id)
            if patch:
                patch.set_alpha(0.5)
    else:
        ax.text(0.5, 0.5, "韦恩图仅支持2组或3组数据", transform=ax.transAxes,
                ha="center", va="center", fontsize=14)
        return fig, {}

    ax.set_title(title, fontsize=14, fontweight="bold", pad=20)
    add_watermark(fig)

    stats = {}
    for name, s in sets.items():
        stats[f"{name} 总数"] = len(s)

    if len(set_values) == 2:
        common = set_values[0] & set_values[1]
        stats["共有元素数"] = len(common)
        stats[f"仅 {names[0]}"] = len(set_values[0] - set_values[1])
        stats[f"仅 {names[1]}"] = len(set_values[1] - set_values[0])
    elif len(set_values) == 3:
        common_all = set_values[0] & set_values[1] & set_values[2]
        stats["三组共有"] = len(common_all)

    return fig, stats
