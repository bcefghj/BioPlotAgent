"""Generate all showcase images for BioPlotAgent demos & marketing."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

from plotting import (
    plot_volcano, plot_heatmap, plot_pca, plot_survival,
    plot_go_enrichment, plot_bar, plot_box, plot_venn,
    plot_ma, plot_dot,
)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "showcase")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "examples")
os.makedirs(OUT, exist_ok=True)

DPI = 200


def save(fig, name):
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {name}.png saved ({os.path.getsize(path) // 1024}KB)")


# ═══════════════════════════════════════════════
# 1. Volcano Plot
# ═══════════════════════════════════════════════
print("\n[1/10] 🌋 Volcano Plot")
df_deg = pd.read_csv(os.path.join(DATA, "deg_example.csv"))
fig, stats = plot_volcano(
    df_deg,
    gene_col="gene",
    fc_threshold=1.0,
    pvalue_threshold=0.05,
    top_n_labels=15,
    title="差异表达基因火山图\nDifferentially Expressed Genes",
    figsize=(11, 9),
)
print(f"  Stats: {stats}")
save(fig, "01_volcano_plot")

# ═══════════════════════════════════════════════
# 2. Heatmap
# ═══════════════════════════════════════════════
print("\n[2/10] 🔥 Heatmap")
df_expr = pd.read_csv(os.path.join(DATA, "expression_matrix.csv"), index_col=0)
fig, stats = plot_heatmap(
    df_expr,
    normalize=True,
    cluster_rows=True,
    cluster_cols=True,
    top_n_genes=40,
    cmap="RdBu_r",
    title="基因表达热图 (Top 40 高变基因)",
    figsize=(13, 11),
)
print(f"  Stats: {stats}")
save(fig, "02_heatmap")

# ═══════════════════════════════════════════════
# 3. PCA Plot
# ═══════════════════════════════════════════════
print("\n[3/10] 📊 PCA Plot")
df_meta = pd.read_csv(os.path.join(DATA, "sample_metadata.csv"))
df_pca_input = df_expr.T.copy()  # 12 samples x 200 genes
df_pca_input.insert(0, "sample", df_pca_input.index)
df_pca_input["group"] = df_meta["group"].values
df_pca_input = df_pca_input.reset_index(drop=True)
fig, stats = plot_pca(
    df_pca_input,
    group_col="group",
    sample_col="sample",
    show_labels=True,
    title="PCA 主成分分析图\n样本聚类与分组验证",
    figsize=(10, 8),
)
print(f"  Stats: {stats}")
save(fig, "03_pca_plot")

# ═══════════════════════════════════════════════
# 4. Survival Analysis
# ═══════════════════════════════════════════════
print("\n[4/10] 📈 Survival Curve")
df_surv = pd.read_csv(os.path.join(DATA, "survival_data.csv"))
fig, stats = plot_survival(
    df_surv,
    time_col="time",
    event_col="event",
    group_col="group",
    ci_show=True,
    at_risk=True,
    title="Kaplan-Meier 生存分析曲线\nTP53 高表达 vs 低表达",
    figsize=(11, 8),
)
print(f"  Stats: {stats}")
save(fig, "04_survival_curve")

# ═══════════════════════════════════════════════
# 5. GO Enrichment - Bar
# ═══════════════════════════════════════════════
print("\n[5/10] 🧬 GO Enrichment (Bar)")
df_go = pd.read_csv(os.path.join(DATA, "go_enrichment.csv"))
fig, stats = plot_go_enrichment(
    df_go,
    term_col="Term",
    pvalue_col="PValue",
    count_col="Count",
    category_col="Category",
    top_n=20,
    plot_style="bar",
    title="GO 富集分析 (柱状图)\nGene Ontology Enrichment Analysis",
    figsize=(13, 9),
)
print(f"  Stats: {stats}")
save(fig, "05_go_enrichment_bar")

# ═══════════════════════════════════════════════
# 6. GO Enrichment - Dot
# ═══════════════════════════════════════════════
print("\n[6/10] 🫧 GO Enrichment (Dot)")
fig, stats = plot_go_enrichment(
    df_go,
    term_col="Term",
    pvalue_col="PValue",
    count_col="Count",
    category_col="Category",
    top_n=20,
    plot_style="dot",
    title="GO 富集分析 (气泡图)\nGene Ontology Enrichment Analysis",
    figsize=(13, 9),
)
save(fig, "06_go_enrichment_dot")

# ═══════════════════════════════════════════════
# 7. Bar Plot
# ═══════════════════════════════════════════════
print("\n[7/10] 📊 Bar Plot")
df_bar = pd.read_csv(os.path.join(DATA, "bar_data.csv"))
fig, stats = plot_bar(
    df_bar,
    x_col="gene",
    y_col="expression",
    group_col="group",
    error_col="se",
    title="关键基因表达量对比\nControl vs Treatment",
    ylabel="相对表达量 (FPKM)",
    figsize=(12, 7),
)
print(f"  Stats: {stats}")
save(fig, "07_bar_plot")

# ═══════════════════════════════════════════════
# 8. Box Plot
# ═══════════════════════════════════════════════
print("\n[8/10] 📦 Box Plot")
fig, stats = plot_box(
    df_bar,
    value_col="expression",
    group_col="group",
    gene_col="gene",
    show_points=True,
    title="基因表达箱线图\n组间差异分析",
    ylabel="相对表达量 (FPKM)",
    figsize=(13, 7),
)
print(f"  Stats: {stats}")
save(fig, "08_box_plot")

# ═══════════════════════════════════════════════
# 9. Venn Diagram
# ═══════════════════════════════════════════════
print("\n[9/10] ⭕ Venn Diagram")
df_venn = pd.read_csv(os.path.join(DATA, "venn_data.csv"))
sets = {col: set(df_venn[col].dropna().astype(str)) for col in df_venn.columns}
fig, stats = plot_venn(
    sets,
    title="多组学交叉分析韦恩图\nDEG ∩ 蛋白组学 ∩ 文献报道",
    figsize=(9, 9),
)
print(f"  Stats: {stats}")
save(fig, "09_venn_diagram")

# ═══════════════════════════════════════════════
# 10. MA Plot
# ═══════════════════════════════════════════════
print("\n[10/10] 📉 MA Plot")
fig, stats = plot_ma(
    df_deg,
    fc_threshold=1.0,
    pvalue_threshold=0.05,
    title="MA Plot\n差异表达与平均表达量关系",
    figsize=(11, 8),
)
print(f"  Stats: {stats}")
save(fig, "10_ma_plot")


# ═══════════════════════════════════════════════
# COMBO: 组合大图 — 小红书封面 (PIL 拼接)
# ═══════════════════════════════════════════════
print("\n\n🎨 Generating combo showcase image (stitching from individual plots)...")

from PIL import Image, ImageDraw, ImageFont

images_info = [
    ("01_volcano_plot.png", "火山图"),
    ("02_heatmap.png", "热图"),
    ("03_pca_plot.png", "PCA分析"),
    ("04_survival_curve.png", "生存分析"),
    ("05_go_enrichment_bar.png", "GO富集"),
    ("07_bar_plot.png", "柱状图"),
    ("08_box_plot.png", "箱线图"),
    ("09_venn_diagram.png", "韦恩图"),
    ("10_ma_plot.png", "MA Plot"),
]

THUMB_W, THUMB_H = 640, 520
COLS, ROWS = 3, 3
PADDING = 30
HEADER_H = 180
FOOTER_H = 160

canvas_w = COLS * THUMB_W + (COLS + 1) * PADDING
canvas_h = HEADER_H + ROWS * THUMB_H + (ROWS + 1) * PADDING + FOOTER_H

canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
draw = ImageDraw.Draw(canvas)

try:
    title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 52)
    sub_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 26)
    footer_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
except:
    title_font = ImageFont.load_default()
    sub_font = title_font
    footer_font = title_font

draw.text(
    (canvas_w // 2, 40),
    "BioPlotAgent",
    fill="#2C3E50", font=title_font, anchor="mt",
)
draw.text(
    (canvas_w // 2, 110),
    "生物信息学智能绘图助手 · 零基础一键出图 · AI驱动 · 10种图表",
    fill="#7F8C8D", font=sub_font, anchor="mt",
)
draw.line([(PADDING, HEADER_H - 10), (canvas_w - PADDING, HEADER_H - 10)], fill="#3498DB", width=3)

for idx, (fname, label) in enumerate(images_info):
    row, col = divmod(idx, COLS)
    x = PADDING + col * (THUMB_W + PADDING)
    y = HEADER_H + PADDING + row * (THUMB_H + PADDING)

    img_path = os.path.join(OUT, fname)
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img.thumbnail((THUMB_W, THUMB_H), Image.LANCZOS)
        paste_x = x + (THUMB_W - img.width) // 2
        paste_y = y + (THUMB_H - img.height) // 2
        canvas.paste(img, (paste_x, paste_y))
    else:
        draw.rectangle([x, y, x + THUMB_W, y + THUMB_H], outline="#CCCCCC")
        draw.text((x + THUMB_W // 2, y + THUMB_H // 2), label, fill="#999", font=sub_font, anchor="mm")

footer_y = canvas_h - FOOTER_H + 20
draw.rectangle([(0, footer_y - 20), (canvas_w, canvas_h)], fill="#EBF5FB")
lines = [
    "✅ 10种生物信息学图表    ✅ AI智能助手    ✅ 零基础友好",
    "✅ 高清PNG/PDF导出    ✅ 边学边练    ✅ 完全开源免费",
    "GitHub: github.com/bcefghj/BioPlotAgent",
]
for i, line in enumerate(lines):
    draw.text((canvas_w // 2, footer_y + i * 38), line, fill="#2C3E50", font=footer_font, anchor="mt")

combo_path = os.path.join(OUT, "combo_showcase.png")
canvas.save(combo_path, dpi=(200, 200))
print(f"  ✓ combo_showcase.png saved ({os.path.getsize(combo_path) // 1024}KB)")
print("\n✅ All showcase images generated!")
print(f"📁 Output directory: {OUT}")
print(f"📊 Total files: {len(os.listdir(OUT))}")
