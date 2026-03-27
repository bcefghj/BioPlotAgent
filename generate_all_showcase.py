"""Generate showcase images for all 25 plot types."""
import sys, os, matplotlib
matplotlib.use("Agg")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotting import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "showcase")
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "examples")
os.makedirs(OUT, exist_ok=True)
DPI = 200

def save(fig, name):
    path = os.path.join(OUT, f"{name}.png")
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white", pad_inches=0.3)
    plt.close(fig)
    print(f"  ✓ {name}.png ({os.path.getsize(path)//1024}KB)")

df_deg = pd.read_csv(f"{DATA}/deg_example.csv")
df_expr = pd.read_csv(f"{DATA}/expression_matrix.csv", index_col=0)
df_meta = pd.read_csv(f"{DATA}/sample_metadata.csv")
df_surv = pd.read_csv(f"{DATA}/survival_data.csv")
df_go = pd.read_csv(f"{DATA}/go_enrichment.csv")
df_bar = pd.read_csv(f"{DATA}/bar_data.csv")
df_venn = pd.read_csv(f"{DATA}/venn_data.csv")
df_forest = pd.read_csv(f"{DATA}/forest_data.csv")
df_roc = pd.read_csv(f"{DATA}/roc_data.csv")
df_sankey = pd.read_csv(f"{DATA}/sankey_data.csv")
df_waterfall = pd.read_csv(f"{DATA}/waterfall_data.csv")
df_manhattan = pd.read_csv(f"{DATA}/manhattan_data.csv")
df_radar = pd.read_csv(f"{DATA}/radar_data.csv")
df_stacked = pd.read_csv(f"{DATA}/stacked_bar_data.csv")
df_scatter = pd.read_csv(f"{DATA}/scatter_data.csv")
sets = {c: set(df_venn[c].dropna()) for c in df_venn.columns}

df_pca = df_expr.T.copy()
df_pca.insert(0, "sample", df_pca.index)
df_pca["group"] = df_meta["group"].values
df_pca = df_pca.reset_index(drop=True)

plots = [
    ("01_volcano", lambda: plot_volcano(df_deg, gene_col="gene", title="差异表达基因火山图\nDifferentially Expressed Genes", figsize=(11,9), top_n_labels=15)),
    ("02_heatmap", lambda: plot_heatmap(df_expr, top_n_genes=40, title="基因表达热图 (Top 40 高变基因)", figsize=(13,11))),
    ("03_pca", lambda: plot_pca(df_pca, group_col="group", sample_col="sample", title="PCA 主成分分析图\n样本聚类与分组验证", figsize=(10,8))),
    ("04_survival", lambda: plot_survival(df_surv, title="Kaplan-Meier 生存分析曲线\nTP53 高表达 vs 低表达", figsize=(11,8))),
    ("05_go_bar", lambda: plot_go_enrichment(df_go, category_col="Category", title="GO 富集分析 (柱状图)", figsize=(13,9))),
    ("06_go_dot", lambda: plot_go_enrichment(df_go, category_col="Category", plot_style="dot", title="GO 富集分析 (气泡图)", figsize=(13,9))),
    ("07_bar", lambda: plot_bar(df_bar, x_col="gene", y_col="expression", group_col="group", error_col="se", title="关键基因表达量对比\nControl vs Treatment", ylabel="相对表达量", figsize=(12,7))),
    ("08_box", lambda: plot_box(df_bar, value_col="expression", group_col="group", gene_col="gene", title="基因表达箱线图\n组间差异分析", figsize=(13,7))),
    ("09_venn", lambda: plot_venn(sets, title="多组学交叉分析韦恩图", figsize=(9,9))),
    ("10_ma", lambda: plot_ma(df_deg, title="MA Plot\n差异表达与平均表达量关系", figsize=(11,8))),
    ("11_violin", lambda: plot_violin(df_bar, value_col="expression", group_col="group", gene_col="gene", title="基因表达小提琴图", figsize=(13,7))),
    ("12_scatter", lambda: plot_scatter(df_scatter, x_col="GeneA_expression", y_col="GeneB_expression", group_col="group", title="基因共表达散点图\nGeneA vs GeneB", figsize=(10,8))),
    ("13_corr_heatmap", lambda: plot_correlation_heatmap(df_expr.T, title="样本间相关性热图", figsize=(10,9))),
    ("14_forest", lambda: plot_forest(df_forest, pvalue_col="pvalue", title="多变量Cox回归森林图", figsize=(12,None))),
    ("15_roc", lambda: plot_roc(df_roc, title="诊断模型ROC曲线对比", figsize=(9,9))),
    ("16_sankey", lambda: plot_sankey(df_sankey, title="通路-基因表达变化桑基图", figsize=(12,8))),
    ("17_waterfall", lambda: plot_waterfall(df_waterfall, label_col="sample", group_col="group", title="肿瘤治疗响应瀑布图", figsize=(14,6))),
    ("18_lollipop", lambda: plot_lollipop(df_go, label_col="Term", value_col="Count", title="GO术语基因数棒棒糖图", figsize=(10,9))),
    ("19_ridge", lambda: plot_ridge(df_bar, value_col="expression", group_col="gene", title="基因表达分布山脊图", figsize=(10,10))),
    ("20_upset", lambda: plot_upset(sets, title="UpSet Plot — 多组学交叉分析", figsize=(14,8))),
    ("21_pie", lambda: plot_pie(df_go, label_col="Term", value_col="Count", donut=True, title="GO术语基因数比例 (环形图)", figsize=(9,9))),
    ("22_density", lambda: plot_density(df_bar, value_col="expression", group_col="group", title="Control vs Treatment 表达密度分布", figsize=(10,7))),
    ("23_manhattan", lambda: plot_manhattan(df_manhattan, gene_col="snp", title="全基因组关联分析曼哈顿图", figsize=(16,6))),
    ("24_radar", lambda: plot_radar(df_radar, label_col="sample", title="肿瘤表型多维雷达图", figsize=(9,9))),
    ("25_stacked_bar", lambda: plot_stacked_bar(df_stacked, x_col="sample", normalize=True, title="免疫细胞组成堆叠柱状图 (百分比)", figsize=(13,7))),
]

print(f"\n=== Generating {len(plots)} showcase images ===\n")
for name, func in plots:
    try:
        fig, stats = func()
        save(fig, name)
    except Exception as e:
        print(f"  ✗ {name}: {e}")

print(f"\n✅ Done! {len(os.listdir(OUT))} files in {OUT}")
