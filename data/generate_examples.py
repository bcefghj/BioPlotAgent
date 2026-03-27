"""Generate realistic example datasets for BioPlotAgent demos."""

import numpy as np
import pandas as pd
import os

np.random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
os.makedirs(OUT_DIR, exist_ok=True)


def generate_deg_data():
    """差异表达基因数据 (DESeq2-like output)."""
    n_genes = 5000
    gene_names = [f"Gene_{i:04d}" for i in range(n_genes)]

    log2fc = np.random.normal(0, 1.5, n_genes)
    base_mean = np.abs(np.random.lognormal(5, 2, n_genes))
    pvalues = np.random.beta(0.3, 5, n_genes)

    n_sig_up = 200
    n_sig_down = 150
    idx_up = np.random.choice(n_genes, n_sig_up, replace=False)
    remaining = list(set(range(n_genes)) - set(idx_up))
    idx_down = np.random.choice(remaining, n_sig_down, replace=False)

    log2fc[idx_up] = np.random.uniform(1.5, 5, n_sig_up)
    pvalues[idx_up] = np.random.uniform(1e-20, 0.01, n_sig_up)

    log2fc[idx_down] = np.random.uniform(-5, -1.5, n_sig_down)
    pvalues[idx_down] = np.random.uniform(1e-15, 0.01, n_sig_down)

    known_genes = [
        "TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN", "RB1", "APC",
        "VEGFA", "HIF1A", "CDH1", "NOTCH1", "WNT1", "STAT3", "JAK2",
    ]
    for i, g in enumerate(known_genes):
        if i < len(idx_up):
            gene_names[idx_up[i]] = g
        elif i - len(idx_up) < len(idx_down):
            gene_names[idx_down[i - n_sig_up]] = g

    padj = np.minimum(pvalues * n_genes / np.arange(1, n_genes + 1), 1.0)

    df = pd.DataFrame({
        "gene": gene_names,
        "baseMean": np.round(base_mean, 2),
        "log2FoldChange": np.round(log2fc, 4),
        "lfcSE": np.round(np.abs(np.random.normal(0.3, 0.1, n_genes)), 4),
        "pvalue": pvalues,
        "padj": padj,
    })
    df.to_csv(os.path.join(OUT_DIR, "deg_example.csv"), index=False)
    print(f"DEG data: {len(df)} genes, {n_sig_up} up, {n_sig_down} down")


def generate_expression_matrix():
    """基因表达矩阵数据。"""
    n_genes = 200
    n_samples = 12
    groups = ["Control"] * 6 + ["Treatment"] * 6
    sample_names = [f"{g}_{i+1}" for i, g in enumerate(groups)]

    known_genes = [
        "TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN", "BCL2", "BAX",
        "GAPDH", "ACTB", "VEGFA", "HIF1A", "CDH1", "CDH2", "VIM",
        "SNAI1", "TWIST1", "ZEB1", "MMP2", "MMP9",
    ]
    other_genes = [f"Gene_{i:04d}" for i in range(n_genes - len(known_genes))]
    gene_names = known_genes + other_genes

    expr = np.random.lognormal(3, 1.5, (n_genes, n_samples))

    for i in range(20):
        if i % 2 == 0:
            expr[i, 6:] *= np.random.uniform(2, 4)
        else:
            expr[i, 6:] *= np.random.uniform(0.2, 0.5)

    expr = np.round(expr, 2)
    df = pd.DataFrame(expr, columns=sample_names, index=gene_names)
    df.index.name = "gene"
    df.to_csv(os.path.join(OUT_DIR, "expression_matrix.csv"))
    print(f"Expression matrix: {n_genes} genes x {n_samples} samples")

    meta = pd.DataFrame({
        "sample": sample_names,
        "group": groups,
        "batch": ["Batch1"] * 3 + ["Batch2"] * 3 + ["Batch1"] * 3 + ["Batch2"] * 3,
    })
    meta.to_csv(os.path.join(OUT_DIR, "sample_metadata.csv"), index=False)


def generate_survival_data():
    """生存分析数据。"""
    n_patients = 200
    np.random.seed(42)

    groups = np.random.choice(["高表达组", "低表达组"], n_patients, p=[0.45, 0.55])

    time = np.zeros(n_patients)
    event = np.zeros(n_patients, dtype=int)

    for i in range(n_patients):
        if groups[i] == "高表达组":
            time[i] = np.random.exponential(36)
            event[i] = 1 if np.random.random() < 0.6 else 0
        else:
            time[i] = np.random.exponential(60)
            event[i] = 1 if np.random.random() < 0.4 else 0

    time = np.clip(time, 1, 120).round(1)

    df = pd.DataFrame({
        "patient_id": [f"P{i:03d}" for i in range(n_patients)],
        "time": time,
        "event": event,
        "group": groups,
        "age": np.random.randint(30, 80, n_patients),
        "stage": np.random.choice(["I", "II", "III", "IV"], n_patients, p=[0.2, 0.3, 0.3, 0.2]),
    })
    df.to_csv(os.path.join(OUT_DIR, "survival_data.csv"), index=False)
    print(f"Survival data: {n_patients} patients")


def generate_go_enrichment_data():
    """GO富集分析数据。"""
    go_terms = {
        "BP": [
            "细胞周期调控", "DNA损伤修复", "细胞凋亡", "免疫应答",
            "血管生成", "细胞增殖", "转录调控", "蛋白质磷酸化",
            "信号转导", "细胞分化", "炎症反应", "氧化应激响应",
        ],
        "MF": [
            "蛋白激酶活性", "DNA结合", "转录因子活性", "GTP酶活性",
            "受体结合", "ATP结合", "蛋白结合", "酶活性调节",
        ],
        "CC": [
            "细胞核", "细胞质", "线粒体", "内质网",
            "细胞膜", "高尔基体", "溶酶体", "细胞外基质",
        ],
    }

    rows = []
    for cat, terms in go_terms.items():
        for term in terms:
            rows.append({
                "Category": cat,
                "Term": term,
                "Count": np.random.randint(5, 80),
                "PValue": 10 ** np.random.uniform(-10, -1),
                "FoldEnrichment": np.round(np.random.uniform(1.5, 5.0), 2),
                "GeneRatio": f"{np.random.randint(5, 50)}/{np.random.randint(100, 500)}",
            })

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "go_enrichment.csv"), index=False)
    print(f"GO enrichment: {len(df)} terms")


def generate_venn_data():
    """韦恩图数据。"""
    all_genes = [f"Gene_{i:04d}" for i in range(500)]
    known = ["TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN", "RB1", "APC",
             "VEGFA", "HIF1A", "CDH1", "NOTCH1", "BCL2", "BAX", "GAPDH"]
    all_genes[:15] = known

    set_a = set(np.random.choice(all_genes, 120, replace=False))
    set_b = set(np.random.choice(all_genes, 100, replace=False))
    set_c = set(np.random.choice(all_genes, 80, replace=False))

    common = set(np.random.choice(all_genes[:50], 20, replace=False))
    set_a |= common
    set_b |= common

    df = pd.DataFrame({
        "DEG分析": pd.Series(list(set_a)),
        "蛋白组学": pd.Series(list(set_b)),
        "文献报道": pd.Series(list(set_c)),
    })
    df.to_csv(os.path.join(OUT_DIR, "venn_data.csv"), index=False)
    print(f"Venn data: {len(set_a)}, {len(set_b)}, {len(set_c)} genes")


def generate_bar_data():
    """柱状图示例数据。"""
    genes = ["TP53", "BRCA1", "EGFR", "MYC", "KRAS", "PTEN", "VEGFA", "HIF1A"]
    rows = []
    for gene in genes:
        ctrl = np.random.lognormal(3, 0.5)
        treat = ctrl * np.random.uniform(0.3, 3)
        rows.append({"gene": gene, "group": "Control", "expression": round(ctrl, 2),
                      "se": round(ctrl * 0.15, 2)})
        rows.append({"gene": gene, "group": "Treatment", "expression": round(treat, 2),
                      "se": round(treat * 0.15, 2)})

    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT_DIR, "bar_data.csv"), index=False)
    print(f"Bar data: {len(genes)} genes x 2 groups")


if __name__ == "__main__":
    generate_deg_data()
    generate_expression_matrix()
    generate_survival_data()
    generate_go_enrichment_data()
    generate_venn_data()
    generate_bar_data()
    print("\nAll example datasets generated!")
