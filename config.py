import os
from dotenv import load_dotenv

load_dotenv()

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.io/v1"
MINIMAX_MODEL = "MiniMax-M2.7"

SUPPORTED_PLOTS = {
    "volcano": "火山图 (Volcano Plot)",
    "heatmap": "热图 (Heatmap)",
    "pca": "PCA主成分分析图",
    "survival": "生存分析曲线 (KM Plot)",
    "go_enrichment": "GO富集分析图",
    "bar": "柱状图 (Bar Plot)",
    "box": "箱线图 (Box Plot)",
    "venn": "韦恩图 (Venn Diagram)",
    "ma_plot": "MA Plot",
    "dot": "气泡图 (Dot Plot)",
}

PLOT_ICONS = {
    "volcano": "🌋",
    "heatmap": "🔥",
    "pca": "📊",
    "survival": "📈",
    "go_enrichment": "🧬",
    "bar": "📊",
    "box": "📦",
    "venn": "⭕",
    "ma_plot": "📉",
    "dot": "🫧",
}
