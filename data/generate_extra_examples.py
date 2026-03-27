"""Generate extra example datasets for the 15 new plot types."""

import numpy as np
import pandas as pd
import os

np.random.seed(2026)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
os.makedirs(OUT, exist_ok=True)


def gen_forest():
    variables = ["TP53 高表达", "年龄 >60", "肿瘤分期 III-IV", "BRCA1 突变",
                 "化疗", "EGFR 高表达", "男性", "吸烟", "BMI >30", "Ki67 >20%"]
    hrs = [1.85, 1.42, 2.31, 1.67, 0.65, 1.53, 1.12, 1.78, 0.89, 1.95]
    df = pd.DataFrame({
        "variable": variables,
        "HR": hrs,
        "lower": [h * np.random.uniform(0.55, 0.8) for h in hrs],
        "upper": [h * np.random.uniform(1.3, 1.8) for h in hrs],
        "pvalue": [0.001, 0.023, 0.0003, 0.008, 0.012, 0.031, 0.45, 0.005, 0.32, 0.0001],
    })
    df.to_csv(os.path.join(OUT, "forest_data.csv"), index=False)
    print("forest_data.csv")


def gen_roc():
    n = 300
    true_label = np.random.binomial(1, 0.4, n)
    score_good = true_label * np.random.uniform(0.5, 1.0, n) + (1 - true_label) * np.random.uniform(0.0, 0.5, n)
    score_good += np.random.normal(0, 0.1, n)
    score_med = true_label * np.random.uniform(0.3, 0.9, n) + (1 - true_label) * np.random.uniform(0.1, 0.7, n)
    score_bad = np.random.uniform(0, 1, n)
    df = pd.DataFrame({
        "true_label": true_label,
        "Model_A": np.clip(score_good, 0, 1).round(4),
        "Model_B": np.clip(score_med, 0, 1).round(4),
        "Random": score_bad.round(4),
    })
    df.to_csv(os.path.join(OUT, "roc_data.csv"), index=False)
    print("roc_data.csv")


def gen_sankey():
    rows = []
    pathways = {"细胞周期": 45, "凋亡": 38, "免疫": 52, "代谢": 30}
    targets = {"上调": 0.55, "下调": 0.30, "无变化": 0.15}
    for src, total in pathways.items():
        for tgt, frac in targets.items():
            rows.append({"source": src, "target": tgt, "value": int(total * frac * np.random.uniform(0.8, 1.2))})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "sankey_data.csv"), index=False)
    print("sankey_data.csv")


def gen_waterfall():
    n = 60
    genes = [f"Sample_{i:02d}" for i in range(n)]
    values = np.concatenate([np.random.uniform(20, 80, 15), np.random.uniform(-5, 15, 20),
                             np.random.uniform(-80, -10, 25)])
    np.random.shuffle(values)
    groups = np.random.choice(["Responder", "Stable", "Progressor"], n, p=[0.3, 0.35, 0.35])
    df = pd.DataFrame({"sample": genes, "value": values.round(1), "group": groups})
    df.to_csv(os.path.join(OUT, "waterfall_data.csv"), index=False)
    print("waterfall_data.csv")


def gen_manhattan():
    rows = []
    for chrom in range(1, 23):
        n_snps = np.random.randint(200, 500)
        positions = np.sort(np.random.randint(1e6, 2.5e8, n_snps))
        pvals = np.random.beta(0.5, 10, n_snps)
        if chrom in [3, 7, 12, 17]:
            hot_idx = np.random.choice(n_snps, np.random.randint(3, 8), replace=False)
            pvals[hot_idx] = 10 ** np.random.uniform(-12, -7, len(hot_idx))
        for j in range(n_snps):
            rows.append({"chr": chrom, "pos": int(positions[j]), "pvalue": pvals[j],
                          "snp": f"rs{np.random.randint(100000, 9999999)}"})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "manhattan_data.csv"), index=False)
    print(f"manhattan_data.csv ({len(df)} SNPs)")


def gen_radar():
    df = pd.DataFrame({
        "sample": ["Control", "Treatment_A", "Treatment_B"],
        "增殖": [65, 40, 30], "凋亡": [20, 55, 70], "迁移": [70, 35, 25],
        "侵袭": [60, 30, 20], "血管生成": [55, 45, 35], "免疫逃逸": [50, 25, 40],
    })
    df.to_csv(os.path.join(OUT, "radar_data.csv"), index=False)
    print("radar_data.csv")


def gen_stacked_bar():
    samples = [f"Sample_{i}" for i in range(1, 13)]
    cell_types = ["T细胞", "B细胞", "NK细胞", "巨噬细胞", "树突细胞", "中性粒细胞"]
    data = {"sample": samples}
    for ct in cell_types:
        data[ct] = np.random.dirichlet(np.ones(len(samples)) * 2).round(3) * 100
    df = pd.DataFrame(data)
    for ct in cell_types:
        df[ct] = np.abs(np.random.normal(np.random.uniform(5, 30), 5, len(samples))).round(1)
    df.to_csv(os.path.join(OUT, "stacked_bar_data.csv"), index=False)
    print("stacked_bar_data.csv")


def gen_scatter_corr():
    n = 100
    gene_a = np.random.lognormal(3, 0.8, n)
    gene_b = gene_a * np.random.uniform(0.5, 1.5, n) + np.random.normal(0, 5, n)
    groups = np.random.choice(["Control", "Treatment"], n)
    df = pd.DataFrame({
        "GeneA_expression": gene_a.round(2),
        "GeneB_expression": gene_b.round(2),
        "group": groups,
    })
    df.to_csv(os.path.join(OUT, "scatter_data.csv"), index=False)
    print("scatter_data.csv")


if __name__ == "__main__":
    gen_forest()
    gen_roc()
    gen_sankey()
    gen_waterfall()
    gen_manhattan()
    gen_radar()
    gen_stacked_bar()
    gen_scatter_corr()
    print("\nAll extra examples generated!")
