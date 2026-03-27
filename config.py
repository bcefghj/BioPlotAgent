import os
from dotenv import load_dotenv

load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.io/v1"
MINIMAX_MODEL = "MiniMax-M2.7"

SUPPORTED_PLOTS = {
    # ── 差异表达分析 ──
    "volcano": "火山图 (Volcano Plot)",
    "ma_plot": "MA Plot",
    "heatmap": "热图 (Heatmap)",
    # ── 降维与聚类 ──
    "pca": "PCA 主成分分析图",
    "correlation_heatmap": "相关性热图",
    # ── 临床与生存分析 ──
    "survival": "生存分析曲线 (KM Plot)",
    "forest": "森林图 (Forest Plot)",
    "roc": "ROC 曲线",
    # ── 富集分析 ──
    "go_enrichment": "GO 富集分析图",
    "dot": "气泡图 (Dot Plot)",
    # ── 基础统计图表 ──
    "bar": "柱状图 (Bar Plot)",
    "box": "箱线图 (Box Plot)",
    "violin": "小提琴图 (Violin Plot)",
    "scatter": "散点图 (Scatter Plot)",
    "density": "密度图 (Density Plot)",
    "ridge": "山脊图 (Ridge Plot)",
    "pie": "饼图/环形图 (Pie/Donut)",
    "stacked_bar": "堆叠柱状图 (Stacked Bar)",
    "lollipop": "棒棒糖图 (Lollipop Chart)",
    # ── 集合分析 ──
    "venn": "韦恩图 (Venn Diagram)",
    "upset": "UpSet Plot (多组集合)",
    # ── 基因组与GWAS ──
    "manhattan": "曼哈顿图 (Manhattan Plot)",
    # ── 关系与流程 ──
    "sankey": "桑基图 (Sankey Diagram)",
    "waterfall": "瀑布图 (Waterfall Plot)",
    "radar": "雷达图 (Radar Chart)",
}

PLOT_ICONS = {
    "volcano": "🌋", "ma_plot": "📉", "heatmap": "🔥",
    "pca": "📊", "correlation_heatmap": "🔗",
    "survival": "📈", "forest": "🌲", "roc": "🎯",
    "go_enrichment": "🧬", "dot": "🫧",
    "bar": "📊", "box": "📦", "violin": "🎻",
    "scatter": "⚡", "density": "🌊", "ridge": "⛰️",
    "pie": "🥧", "stacked_bar": "📚", "lollipop": "🍭",
    "venn": "⭕", "upset": "🔀",
    "manhattan": "🏙️",
    "sankey": "🔄", "waterfall": "🌊", "radar": "🕸️",
}

PLOT_CATEGORIES = {
    "差异表达分析": ["volcano", "ma_plot", "heatmap"],
    "降维与聚类": ["pca", "correlation_heatmap"],
    "临床与生存分析": ["survival", "forest", "roc"],
    "富集分析": ["go_enrichment", "dot"],
    "基础统计图表": ["bar", "box", "violin", "scatter", "density", "ridge", "pie", "stacked_bar", "lollipop"],
    "集合分析": ["venn", "upset"],
    "基因组与GWAS": ["manhattan"],
    "关系与流程": ["sankey", "waterfall", "radar"],
}
