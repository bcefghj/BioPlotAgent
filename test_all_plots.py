"""Test all 25 plot types."""
import sys, os, matplotlib
matplotlib.use("Agg")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from plotting import *

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "examples")
passed, failed = [], []

def test(name, func):
    try:
        fig, stats = func()
        plt.close(fig)
        passed.append(name)
        print(f"  ✓ {name}: {stats}")
    except Exception as e:
        failed.append((name, str(e)))
        print(f"  ✗ {name}: {e}")

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

print("\n=== Testing 25 plot types ===\n")

test("1. Volcano", lambda: plot_volcano(df_deg, gene_col="gene"))
test("2. Heatmap", lambda: plot_heatmap(df_expr, top_n_genes=30))
test("3. PCA", lambda: (lambda d: plot_pca(d, group_col="group", sample_col="sample"))(
    df_expr.T.assign(sample=df_expr.columns, group=df_meta["group"].values).reset_index(drop=True)))
test("4. Survival", lambda: plot_survival(df_surv))
test("5. GO Bar", lambda: plot_go_enrichment(df_go, category_col="Category"))
test("6. Bar", lambda: plot_bar(df_bar, x_col="gene", y_col="expression", group_col="group"))
test("7. Box", lambda: plot_box(df_bar, value_col="expression", group_col="group"))
test("8. Venn", lambda: plot_venn({c: set(df_venn[c].dropna()) for c in df_venn.columns}))
test("9. MA", lambda: plot_ma(df_deg))
test("10. Dot", lambda: plot_dot(df_go, y_col="Term", x_col="FoldEnrichment", size_col="Count", color_col="PValue"))
test("11. Violin", lambda: plot_violin(df_bar, value_col="expression", group_col="group", gene_col="gene"))
test("12. Scatter", lambda: plot_scatter(df_scatter, x_col="GeneA_expression", y_col="GeneB_expression", group_col="group"))
test("13. CorrHeatmap", lambda: plot_correlation_heatmap(df_expr.T))
test("14. Forest", lambda: plot_forest(df_forest, pvalue_col="pvalue"))
test("15. ROC", lambda: plot_roc(df_roc))
test("16. Sankey", lambda: plot_sankey(df_sankey))
test("17. Waterfall", lambda: plot_waterfall(df_waterfall, label_col="sample", group_col="group"))
test("18. Lollipop", lambda: plot_lollipop(df_go, label_col="Term", value_col="Count"))
test("19. Ridge", lambda: plot_ridge(df_bar, value_col="expression", group_col="gene"))
test("20. UpSet", lambda: plot_upset({c: set(df_venn[c].dropna()) for c in df_venn.columns}))
test("21. Pie", lambda: plot_pie(df_go, label_col="Term", value_col="Count"))
test("22. Density", lambda: plot_density(df_bar, value_col="expression", group_col="group"))
test("23. Manhattan", lambda: plot_manhattan(df_manhattan, gene_col="snp"))
test("24. Radar", lambda: plot_radar(df_radar, label_col="sample"))
test("25. StackedBar", lambda: plot_stacked_bar(df_stacked, x_col="sample"))

print(f"\n=== Results: {len(passed)}/25 passed, {len(failed)} failed ===")
for name, err in failed:
    print(f"  FAILED: {name} -> {err}")
