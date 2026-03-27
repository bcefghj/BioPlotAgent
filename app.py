"""
BioPlotAgent - 生物信息学智能绘图助手
让零基础用户也能绘制专业的生物信息学图表！
"""

import sys
import os
import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SUPPORTED_PLOTS, PLOT_ICONS, PLOT_CATEGORIES, MINIMAX_API_KEY
from plotting import (
    plot_volcano, plot_heatmap, plot_pca, plot_survival,
    plot_go_enrichment, plot_bar, plot_box, plot_venn,
    plot_ma, plot_dot, plot_violin, plot_scatter,
    plot_correlation_heatmap, plot_forest, plot_roc,
    plot_sankey, plot_waterfall, plot_lollipop, plot_ridge,
    plot_upset, plot_pie, plot_density, plot_manhattan,
    plot_radar, plot_stacked_bar,
    save_figure, get_example_data_path,
)
from tutorials import TUTORIALS, get_tutorial

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="BioPlotAgent - 生物信息学绘图助手",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    .main-header h1 {
        background: linear-gradient(120deg, #2C3E50, #3498DB, #1ABC9C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
    }
    .plot-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3498DB;
    }
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        margin: 0.3rem 0;
    }
    .tutorial-box {
        background: #FFF3CD;
        border-radius: 10px;
        padding: 1rem;
        border-left: 4px solid #FFC107;
        margin: 0.5rem 0;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session state
# ──────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_fig" not in st.session_state:
    st.session_state.current_fig = None


# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧬 BioPlotAgent")
    st.markdown("*生物信息学智能绘图助手*")
    st.divider()

    mode = st.radio(
        "选择模式",
        ["🎨 快速绘图", "🤖 AI 助手", "📚 学习中心"],
        help="快速绘图：选择图表类型直接画图\nAI助手：用自然语言描述需求\n学习中心：学习生物信息学图表知识",
    )

    st.divider()

    if mode == "🤖 AI 助手":
        api_key = st.text_input(
            "MiniMax API Key",
            value=MINIMAX_API_KEY,
            type="password",
            help="在 https://platform.minimax.io/ 获取 API Key",
        )
        if api_key:
            st.success("API Key 已配置 ✓")
        else:
            st.warning("请输入 API Key 以使用 AI 助手功能")

    st.divider()
    st.markdown("""
    ### 💡 快速上手

    1. **零基础？** 先去 📚 学习中心了解各种图表
    2. **有数据？** 选择 🎨 快速绘图上传数据
    3. **不确定？** 试试 🤖 AI助手描述你的需求

    ---
    *Powered by MiniMax M2.7*
    """)


# ──────────────────────────────────────────────
# Helper functions
# ──────────────────────────────────────────────
def load_data(uploaded_file):
    """Load uploaded data file."""
    if uploaded_file is None:
        return None
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)
        elif name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        elif name.endswith(".tsv") or name.endswith(".txt"):
            return pd.read_csv(uploaded_file, sep="\t")
        else:
            st.error("不支持的文件格式，请上传 CSV、TSV、XLSX 文件")
            return None
    except Exception as e:
        st.error(f"读取文件出错: {e}")
        return None


def load_example_data(filename):
    """Load an example dataset."""
    path = get_example_data_path(filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None


def display_stats(stats: dict):
    """Display statistics in a nice format."""
    if not stats:
        return
    cols = st.columns(min(len(stats), 4))
    for i, (key, value) in enumerate(stats.items()):
        with cols[i % len(cols)]:
            st.metric(label=key, value=str(value))


def download_button(fig, filename="bioplot"):
    """Create download buttons for figure."""
    col1, col2 = st.columns(2)
    with col1:
        buf_png = save_figure(fig, format="png")
        st.download_button(
            "📥 下载 PNG (高清)",
            data=buf_png,
            file_name=f"{filename}.png",
            mime="image/png",
        )
    with col2:
        buf_pdf = save_figure(fig, format="pdf")
        st.download_button(
            "📥 下载 PDF (矢量图)",
            data=buf_pdf,
            file_name=f"{filename}.pdf",
            mime="application/pdf",
        )


# ──────────────────────────────────────────────
# Mode: Quick Plotting
# ──────────────────────────────────────────────
def render_quick_plot():
    st.markdown('<div class="main-header"><h1>🎨 快速绘图</h1></div>', unsafe_allow_html=True)
    st.markdown("选择图表类型，上传数据或使用示例数据，一键生成专业图表！**支持 25 种图表！**")

    cat = st.selectbox("选择类别", list(PLOT_CATEGORIES.keys()))
    plot_type = st.selectbox(
        "选择图表类型",
        PLOT_CATEGORIES[cat],
        format_func=lambda x: f"{PLOT_ICONS.get(x, '')} {SUPPORTED_PLOTS[x]}",
    )

    tutorial = get_tutorial(plot_type)
    if tutorial:
        with st.expander("📖 了解这种图表", expanded=False):
            st.markdown(tutorial.get("what", ""))
            if "data_format" in tutorial:
                st.markdown(tutorial["data_format"])

    st.divider()

    col_data, col_params = st.columns([1, 1])

    with col_data:
        st.subheader("📂 数据")
        data_source = st.radio(
            "数据来源",
            ["📤 上传自己的数据", "📋 使用示例数据"],
            horizontal=True,
        )

        data = None
        if data_source == "📤 上传自己的数据":
            uploaded = st.file_uploader(
                "上传数据文件",
                type=["csv", "tsv", "xlsx", "txt"],
                help="支持 CSV、TSV、XLSX 格式",
            )
            data = load_data(uploaded)
        else:
            example_map = {
                "volcano": "deg_example.csv",
                "heatmap": "expression_matrix.csv",
                "pca": "expression_matrix.csv",
                "survival": "survival_data.csv",
                "go_enrichment": "go_enrichment.csv",
                "bar": "bar_data.csv",
                "box": "bar_data.csv",
                "venn": "venn_data.csv",
                "ma_plot": "deg_example.csv",
                "dot": "go_enrichment.csv",
                "violin": "bar_data.csv",
                "scatter": "scatter_data.csv",
                "correlation_heatmap": "expression_matrix.csv",
                "forest": "forest_data.csv",
                "roc": "roc_data.csv",
                "sankey": "sankey_data.csv",
                "waterfall": "waterfall_data.csv",
                "lollipop": "go_enrichment.csv",
                "ridge": "bar_data.csv",
                "upset": "venn_data.csv",
                "pie": "go_enrichment.csv",
                "density": "bar_data.csv",
                "manhattan": "manhattan_data.csv",
                "radar": "radar_data.csv",
                "stacked_bar": "stacked_bar_data.csv",
            }
            data = load_example_data(example_map.get(plot_type, ""))
            if data is not None:
                st.success(f"已加载示例数据 ({len(data)} 行 × {len(data.columns)} 列)")

        if data is not None:
            with st.expander("👀 预览数据", expanded=False):
                st.dataframe(data.head(20), use_container_width=True)

    with col_params:
        st.subheader("⚙️ 参数设置")
        params = get_plot_params(plot_type, data)

    st.divider()

    if data is not None and st.button("🚀 生成图表", type="primary", use_container_width=True):
        with st.spinner("正在绘制图表..."):
            try:
                fig, stats = generate_plot(plot_type, data, params)
                st.session_state.current_fig = fig

                st.subheader("📊 结果")
                display_stats(stats)
                st.pyplot(fig, use_container_width=True)
                download_button(fig, filename=f"bioplot_{plot_type}")

                if tutorial:
                    with st.expander("🎓 如何解读这张图？", expanded=True):
                        st.markdown(tutorial.get("how", ""))

                plt.close(fig)

            except Exception as e:
                st.error(f"绘图出错: {str(e)}")
                st.info("💡 请检查数据格式是否正确，或尝试调整参数设置。")


def get_plot_params(plot_type, data):
    """Get user-configurable parameters for each plot type."""
    params = {}

    if data is None:
        st.info("请先选择数据")
        return params

    cols = data.columns.tolist()
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()

    if plot_type == "volcano":
        params["log2fc_col"] = st.selectbox("log2FC 列", cols, index=cols.index("log2FoldChange") if "log2FoldChange" in cols else 0)
        params["pvalue_col"] = st.selectbox("P-value 列", cols, index=cols.index("pvalue") if "pvalue" in cols else 0)
        params["gene_col"] = st.selectbox("基因名列（可选）", ["无"] + cols, index=cols.index("gene") + 1 if "gene" in cols else 0)
        if params["gene_col"] == "无":
            params["gene_col"] = None
        params["fc_threshold"] = st.slider("|log₂FC| 阈值", 0.5, 3.0, 1.0, 0.1)
        params["pvalue_threshold"] = st.select_slider("P-value 阈值", options=[0.001, 0.01, 0.05, 0.1], value=0.05)
        params["top_n_labels"] = st.slider("标注前N个基因", 0, 30, 10)
        params["title"] = st.text_input("标题", "差异表达基因火山图")

    elif plot_type == "heatmap":
        params["gene_col"] = st.selectbox("基因名列", ["无"] + cols, index=0)
        if params["gene_col"] == "无":
            params["gene_col"] = None
        params["normalize"] = st.checkbox("Z-score 标准化", value=True)
        params["cluster_rows"] = st.checkbox("行聚类", value=True)
        params["cluster_cols"] = st.checkbox("列聚类", value=True)
        params["top_n_genes"] = st.slider("展示前N个高变基因", 10, 100, 50)
        params["cmap"] = st.selectbox("配色方案", ["RdBu_r", "viridis", "coolwarm", "YlOrRd"], index=0)
        params["title"] = st.text_input("标题", "基因表达热图")

    elif plot_type == "pca":
        params["group_col"] = st.selectbox("分组列（可选）", ["无"] + cols, index=0)
        if params["group_col"] == "无":
            params["group_col"] = None
        params["sample_col"] = st.selectbox("样本名列（可选）", ["无"] + cols, index=0)
        if params["sample_col"] == "无":
            params["sample_col"] = None
        params["show_labels"] = st.checkbox("显示样本标签", value=True)
        params["title"] = st.text_input("标题", "PCA 主成分分析图")

    elif plot_type == "survival":
        params["time_col"] = st.selectbox("时间列", cols, index=cols.index("time") if "time" in cols else 0)
        params["event_col"] = st.selectbox("事件列", cols, index=cols.index("event") if "event" in cols else 0)
        params["group_col"] = st.selectbox("分组列", cols, index=cols.index("group") if "group" in cols else 0)
        params["ci_show"] = st.checkbox("显示置信区间", value=True)
        params["at_risk"] = st.checkbox("显示风险人数表", value=True)
        params["title"] = st.text_input("标题", "Kaplan-Meier 生存分析曲线")

    elif plot_type == "go_enrichment":
        params["term_col"] = st.selectbox("术语列", cols, index=cols.index("Term") if "Term" in cols else 0)
        params["pvalue_col"] = st.selectbox("P-value 列", cols, index=cols.index("PValue") if "PValue" in cols else 0)
        params["count_col"] = st.selectbox("基因数列", cols, index=cols.index("Count") if "Count" in cols else 0)
        params["category_col"] = st.selectbox("类别列（可选）", ["无"] + cols, index=cols.index("Category") + 1 if "Category" in cols else 0)
        if params["category_col"] == "无":
            params["category_col"] = None
        params["top_n"] = st.slider("展示前N条", 5, 30, 20)
        params["plot_style"] = st.radio("样式", ["bar", "dot"], format_func=lambda x: "柱状图" if x == "bar" else "气泡图", horizontal=True)
        params["title"] = st.text_input("标题", "GO 富集分析")

    elif plot_type == "bar":
        params["x_col"] = st.selectbox("X轴（如基因名）", cols, index=0)
        y_default = numeric_cols.index("expression") if "expression" in numeric_cols else 0
        params["y_col"] = st.selectbox("Y轴（如表达量）", numeric_cols, index=y_default)
        params["group_col"] = st.selectbox("分组列（可选）", ["无"] + cols, index=cols.index("group") + 1 if "group" in cols else 0)
        if params["group_col"] == "无":
            params["group_col"] = None
        err_options = ["无"] + numeric_cols
        params["error_col"] = st.selectbox("误差棒列（可选）", err_options, index=err_options.index("se") if "se" in err_options else 0)
        if params["error_col"] == "无":
            params["error_col"] = None
        params["horizontal"] = st.checkbox("水平显示", value=False)
        params["title"] = st.text_input("标题", "基因表达柱状图")

    elif plot_type == "box":
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=numeric_cols.index("expression") if "expression" in numeric_cols else 0)
        params["group_col"] = st.selectbox("分组列", cols, index=cols.index("group") if "group" in cols else 0)
        gene_options = ["无"] + cols
        params["gene_col"] = st.selectbox("基因列（可选，多基因对比）", gene_options, index=gene_options.index("gene") if "gene" in gene_options else 0)
        if params["gene_col"] == "无":
            params["gene_col"] = None
        params["show_points"] = st.checkbox("显示数据点", value=True)
        params["title"] = st.text_input("标题", "基因表达箱线图")

    elif plot_type == "venn":
        st.info("韦恩图使用特殊数据格式：每列为一个集合")
        params["title"] = st.text_input("标题", "基因集合韦恩图")

    elif plot_type == "ma_plot":
        params["log2fc_col"] = st.selectbox("log2FC 列", cols, index=cols.index("log2FoldChange") if "log2FoldChange" in cols else 0)
        params["basemean_col"] = st.selectbox("baseMean 列", cols, index=cols.index("baseMean") if "baseMean" in cols else 0)
        params["pvalue_col"] = st.selectbox("P-value 列", cols, index=cols.index("pvalue") if "pvalue" in cols else 0)
        params["fc_threshold"] = st.slider("|log₂FC| 阈值", 0.5, 3.0, 1.0, 0.1)
        params["title"] = st.text_input("标题", "MA Plot")

    elif plot_type == "dot":
        non_numeric_cols = data.select_dtypes(exclude=[np.number]).columns.tolist()
        params["y_col"] = st.selectbox("Y轴（类别）", non_numeric_cols if non_numeric_cols else cols, index=0)
        params["x_col"] = st.selectbox("X轴（数值）", numeric_cols, index=0)
        params["size_col"] = st.selectbox("气泡大小", numeric_cols, index=min(1, len(numeric_cols) - 1))
        params["color_col"] = st.selectbox("气泡颜色", numeric_cols, index=min(2, len(numeric_cols) - 1))
        params["title"] = st.text_input("标题", "富集分析气泡图")

    elif plot_type == "violin":
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        params["group_col"] = st.selectbox("分组列", cols, index=cols.index("group") if "group" in cols else 0)
        gene_opts = ["无"] + cols
        params["gene_col"] = st.selectbox("基因列（可选）", gene_opts, index=gene_opts.index("gene") if "gene" in gene_opts else 0)
        if params["gene_col"] == "无":
            params["gene_col"] = None
        params["inner"] = st.selectbox("内部样式", ["box", "quartile", "point", "stick"], index=0)
        params["title"] = st.text_input("标题", "基因表达小提琴图")

    elif plot_type == "scatter":
        params["x_col"] = st.selectbox("X轴", numeric_cols, index=0)
        params["y_col"] = st.selectbox("Y轴", numeric_cols, index=min(1, len(numeric_cols) - 1))
        grp_opts = ["无"] + cols
        params["group_col"] = st.selectbox("分组列（可选）", grp_opts, index=grp_opts.index("group") if "group" in grp_opts else 0)
        if params["group_col"] == "无":
            params["group_col"] = None
        params["show_reg"] = st.checkbox("显示回归线", value=True)
        params["show_corr"] = st.checkbox("显示相关系数", value=True)
        params["title"] = st.text_input("标题", "基因表达散点图")

    elif plot_type == "correlation_heatmap":
        params["method"] = st.selectbox("相关性方法", ["pearson", "spearman", "kendall"])
        params["annot"] = st.checkbox("显示数值", value=len(data.select_dtypes(include=[np.number]).columns) <= 20)
        params["mask_upper"] = st.checkbox("隐藏上三角", value=True)
        params["title"] = st.text_input("标题", "相关性热图")

    elif plot_type == "forest":
        params["label_col"] = st.selectbox("变量名列", cols, index=0)
        params["estimate_col"] = st.selectbox("效应值列 (HR/OR)", numeric_cols, index=0)
        params["lower_col"] = st.selectbox("CI下限列", numeric_cols, index=min(1, len(numeric_cols) - 1))
        params["upper_col"] = st.selectbox("CI上限列", numeric_cols, index=min(2, len(numeric_cols) - 1))
        pv_opts = ["无"] + cols
        params["pvalue_col"] = st.selectbox("P-value列（可选）", pv_opts, index=pv_opts.index("pvalue") if "pvalue" in pv_opts else 0)
        if params["pvalue_col"] == "无":
            params["pvalue_col"] = None
        params["log_scale"] = st.checkbox("对数坐标", value=True)
        params["title"] = st.text_input("标题", "森林图 (Forest Plot)")

    elif plot_type == "roc":
        params["true_col"] = st.selectbox("真实标签列", cols, index=cols.index("true_label") if "true_label" in cols else 0)
        all_nc = [c for c in numeric_cols if c != params["true_col"]]
        params["score_cols"] = st.multiselect("评分列（可多选）", all_nc, default=all_nc[:3])
        params["title"] = st.text_input("标题", "ROC 曲线")

    elif plot_type == "sankey":
        params["source_col"] = st.selectbox("源节点列", cols, index=0)
        params["target_col"] = st.selectbox("目标节点列", cols, index=min(1, len(cols) - 1))
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        params["title"] = st.text_input("标题", "桑基图")

    elif plot_type == "waterfall":
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        lbl_opts = ["无"] + cols
        params["label_col"] = st.selectbox("标签列（可选）", lbl_opts, index=0)
        if params["label_col"] == "无":
            params["label_col"] = None
        grp_opts2 = ["无"] + cols
        params["group_col"] = st.selectbox("分组列（可选）", grp_opts2, index=grp_opts2.index("group") if "group" in grp_opts2 else 0)
        if params["group_col"] == "无":
            params["group_col"] = None
        params["sort"] = st.checkbox("按值排序", value=True)
        params["title"] = st.text_input("标题", "瀑布图")

    elif plot_type == "lollipop":
        non_nc = data.select_dtypes(exclude=[np.number]).columns.tolist()
        params["label_col"] = st.selectbox("标签列", non_nc if non_nc else cols, index=0)
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        params["horizontal"] = st.checkbox("水平显示", value=True)
        params["sort"] = st.checkbox("排序", value=True)
        params["title"] = st.text_input("标题", "棒棒糖图")

    elif plot_type == "ridge":
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        non_nc = data.select_dtypes(exclude=[np.number]).columns.tolist()
        params["group_col"] = st.selectbox("分组列", non_nc if non_nc else cols, index=0)
        params["title"] = st.text_input("标题", "山脊图")

    elif plot_type == "upset":
        st.info("UpSet Plot 使用与韦恩图相同的数据格式：每列为一个集合")
        params["title"] = st.text_input("标题", "UpSet Plot")

    elif plot_type == "pie":
        non_nc = data.select_dtypes(exclude=[np.number]).columns.tolist()
        params["label_col"] = st.selectbox("标签列", non_nc if non_nc else cols, index=0)
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        params["donut"] = st.checkbox("环形图样式", value=False)
        params["top_n"] = st.slider("展示前N项", 5, 20, 10)
        params["title"] = st.text_input("标题", "比例分布图")

    elif plot_type == "density":
        params["value_col"] = st.selectbox("数值列", numeric_cols, index=0)
        grp_opts = ["无"] + cols
        params["group_col"] = st.selectbox("分组列（可选）", grp_opts, index=grp_opts.index("group") if "group" in grp_opts else 0)
        if params["group_col"] == "无":
            params["group_col"] = None
        params["fill"] = st.checkbox("填充颜色", value=True)
        params["title"] = st.text_input("标题", "密度分布图")

    elif plot_type == "manhattan":
        params["chr_col"] = st.selectbox("染色体列", cols, index=cols.index("chr") if "chr" in cols else 0)
        params["pos_col"] = st.selectbox("位置列", cols, index=cols.index("pos") if "pos" in cols else 0)
        params["pvalue_col"] = st.selectbox("P-value列", cols, index=cols.index("pvalue") if "pvalue" in cols else 0)
        gene_opts = ["无"] + cols
        params["gene_col"] = st.selectbox("基因/SNP标签列", gene_opts, index=gene_opts.index("snp") if "snp" in gene_opts else 0)
        if params["gene_col"] == "无":
            params["gene_col"] = None
        params["title"] = st.text_input("标题", "曼哈顿图")

    elif plot_type == "radar":
        params["label_col"] = st.selectbox("标签列", cols, index=0)
        params["value_cols"] = st.multiselect("数值列（多选）", numeric_cols, default=numeric_cols[:6])
        params["fill"] = st.checkbox("填充", value=True)
        params["title"] = st.text_input("标题", "雷达图")

    elif plot_type == "stacked_bar":
        non_nc = data.select_dtypes(exclude=[np.number]).columns.tolist()
        params["x_col"] = st.selectbox("X轴（样本/类别）", non_nc if non_nc else cols, index=0)
        params["value_cols"] = st.multiselect("数值列（多选）", numeric_cols, default=numeric_cols[:6])
        params["normalize"] = st.checkbox("百分比标准化", value=False)
        params["horizontal"] = st.checkbox("水平显示", value=False)
        params["title"] = st.text_input("标题", "堆叠柱状图")

    return params


def generate_plot(plot_type, data, params):
    """Call the appropriate plotting function."""
    dispatch = {
        "volcano": lambda: plot_volcano(data, **params),
        "heatmap": lambda: plot_heatmap(data, **params),
        "pca": lambda: plot_pca(data, **params),
        "survival": lambda: plot_survival(data, **params),
        "go_enrichment": lambda: plot_go_enrichment(data, **params),
        "bar": lambda: plot_bar(data, **params),
        "box": lambda: plot_box(data, **params),
        "ma_plot": lambda: plot_ma(data, **params),
        "dot": lambda: plot_dot(data, **params),
        "violin": lambda: plot_violin(data, **params),
        "scatter": lambda: plot_scatter(data, **params),
        "correlation_heatmap": lambda: plot_correlation_heatmap(data, **params),
        "forest": lambda: plot_forest(data, **params),
        "roc": lambda: plot_roc(data, **params),
        "sankey": lambda: plot_sankey(data, **params),
        "waterfall": lambda: plot_waterfall(data, **params),
        "lollipop": lambda: plot_lollipop(data, **params),
        "ridge": lambda: plot_ridge(data, **params),
        "density": lambda: plot_density(data, **params),
        "pie": lambda: plot_pie(data, **params),
        "manhattan": lambda: plot_manhattan(data, **params),
        "radar": lambda: plot_radar(data, **params),
        "stacked_bar": lambda: plot_stacked_bar(data, **params),
    }

    if plot_type == "venn":
        sets = {col: set(data[col].dropna().astype(str)) for col in data.columns}
        return plot_venn(sets, title=params.get("title", "韦恩图"))
    elif plot_type == "upset":
        sets = {col: set(data[col].dropna().astype(str)) for col in data.columns}
        return plot_upset(sets, title=params.get("title", "UpSet Plot"))
    elif plot_type in dispatch:
        return dispatch[plot_type]()
    else:
        raise ValueError(f"未知图表类型: {plot_type}")


# ──────────────────────────────────────────────
# Mode: AI Assistant
# ──────────────────────────────────────────────
def render_ai_assistant():
    st.markdown('<div class="main-header"><h1>🤖 AI 绘图助手</h1></div>', unsafe_allow_html=True)
    st.markdown("用自然语言描述你想要的图表，AI 帮你完成！")

    current_api_key = st.session_state.get("api_key_input", MINIMAX_API_KEY)
    if not current_api_key:
        st.warning("⚠️ 请在左侧侧边栏输入 MiniMax API Key")
        st.markdown("""
        ### 如何获取 API Key？

        1. 访问 [MiniMax 开放平台](https://platform.minimax.io/)
        2. 注册/登录账号
        3. 在控制台获取 API Key
        4. 将 Key 粘贴到左侧侧边栏

        **或者**：在项目目录创建 `.env` 文件，写入：
        ```
        MINIMAX_API_KEY=your_key_here
        ```
        """)
        return

    col_chat, col_upload = st.columns([2, 1])

    with col_upload:
        st.subheader("📂 上传数据（可选）")
        uploaded = st.file_uploader(
            "上传数据文件",
            type=["csv", "tsv", "xlsx"],
            key="ai_upload",
        )
        user_data = load_data(uploaded)
        if user_data is not None:
            st.success(f"数据已加载: {user_data.shape[0]} 行 × {user_data.shape[1]} 列")
            with st.expander("预览数据"):
                st.dataframe(user_data.head(10))

        st.divider()
        st.markdown("""
        ### 💡 试试这些问题

        - "我有一组差异表达数据，应该画什么图？"
        - "帮我解释一下火山图怎么看"
        - "什么是PCA分析？有什么用？"
        - "热图的Z-score标准化是什么意思？"
        - "生存分析的p值小于0.05说明什么？"
        """)

    with col_chat:
        st.subheader("💬 对话")

        chat_container = st.container(height=500)
        with chat_container:
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if prompt := st.chat_input("输入你的问题..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            try:
                from llm.minimax_client import BioPlotLLM

                llm = BioPlotLLM(api_key=current_api_key)

                if user_data is not None:
                    data_desc = f"\n\n[用户数据信息：{user_data.shape[0]}行 × {user_data.shape[1]}列，列名：{', '.join(user_data.columns[:20])}]"
                    full_prompt = prompt + data_desc
                else:
                    full_prompt = prompt

                with st.spinner("AI 思考中..."):
                    history = [
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.chat_history[:-1]
                    ]
                    response = llm.chat(full_prompt, history=history[-10:])

                st.session_state.chat_history.append({"role": "assistant", "content": response})

                with chat_container:
                    with st.chat_message("assistant"):
                        st.markdown(response)

            except Exception as e:
                error_msg = f"调用 AI 时出错: {str(e)}"
                st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                with chat_container:
                    with st.chat_message("assistant"):
                        st.error(error_msg)


# ──────────────────────────────────────────────
# Mode: Learning Center
# ──────────────────────────────────────────────
def render_learning_center():
    st.markdown('<div class="main-header"><h1>📚 生物信息学绘图学习中心</h1></div>', unsafe_allow_html=True)
    st.markdown("从零开始学习生物信息学图表，每种图表都有详细教程和动手实践！")

    tab_overview, tab_detail, tab_practice = st.tabs(["📖 图表总览", "🔍 详细教程", "🧪 动手实践"])

    with tab_overview:
        st.markdown("### 生物信息学常用图表一览")
        st.markdown("")

        grid_cols = st.columns(2)
        for i, (ptype, tutorial) in enumerate(TUTORIALS.items()):
            with grid_cols[i % 2]:
                with st.container(border=True):
                    st.markdown(f"#### {tutorial['title']}")
                    what_text = tutorial.get("what", "")
                    first_para = what_text.strip().split("\n\n")[1] if "\n\n" in what_text else what_text[:150]
                    st.markdown(first_para)
                    st.caption(f"适用场景：{tutorial.get('when', '')[:80]}...")

    with tab_detail:
        selected = st.selectbox(
            "选择要学习的图表",
            list(TUTORIALS.keys()),
            format_func=lambda x: TUTORIALS[x]["title"],
        )

        tutorial = TUTORIALS[selected]

        st.markdown(f"# {tutorial['title']}")

        if "what" in tutorial:
            st.markdown("---")
            st.markdown(tutorial["what"])

        if "when" in tutorial:
            st.markdown("---")
            if isinstance(tutorial["when"], str) and len(tutorial["when"]) < 200:
                st.info(f"**使用场景**：{tutorial['when']}")
            else:
                st.markdown(tutorial["when"])

        if "how" in tutorial:
            st.markdown("---")
            st.markdown(tutorial["how"])

        if "data_format" in tutorial:
            st.markdown("---")
            st.markdown(tutorial["data_format"])

    with tab_practice:
        st.markdown("### 🧪 动手实践")
        st.markdown("用示例数据亲手绘制图表，加深理解！")

        practice_type = st.selectbox(
            "选择练习",
            ["volcano", "heatmap", "survival", "go_enrichment"],
            format_func=lambda x: f"{PLOT_ICONS.get(x, '')} {SUPPORTED_PLOTS[x]}",
            key="practice_select",
        )

        practice_map = {
            "volcano": ("deg_example.csv", {
                "log2fc_col": "log2FoldChange",
                "pvalue_col": "pvalue",
                "gene_col": "gene",
                "fc_threshold": 1.0,
                "pvalue_threshold": 0.05,
                "top_n_labels": 10,
                "title": "练习：差异表达基因火山图",
            }),
            "heatmap": ("expression_matrix.csv", {
                "gene_col": None,
                "normalize": True,
                "cluster_rows": True,
                "cluster_cols": True,
                "top_n_genes": 50,
                "cmap": "RdBu_r",
                "title": "练习：基因表达热图",
            }),
            "survival": ("survival_data.csv", {
                "time_col": "time",
                "event_col": "event",
                "group_col": "group",
                "ci_show": True,
                "at_risk": True,
                "title": "练习：生存分析曲线",
            }),
            "go_enrichment": ("go_enrichment.csv", {
                "term_col": "Term",
                "pvalue_col": "PValue",
                "count_col": "Count",
                "category_col": "Category",
                "top_n": 20,
                "plot_style": "bar",
                "title": "练习：GO富集分析",
            }),
        }

        example_file, default_params = practice_map[practice_type]
        data = load_example_data(example_file)

        if data is not None:
            tutorial = get_tutorial(practice_type)

            st.markdown(f"**第1步：理解数据**")
            with st.expander("查看示例数据", expanded=True):
                st.dataframe(data.head(10), use_container_width=True)
                st.caption(f"数据大小: {data.shape[0]} 行 × {data.shape[1]} 列")

            st.markdown(f"**第2步：调整参数（尝试改变参数看看图表有什么变化！）**")

            practice_params = default_params.copy()
            if practice_type == "volcano":
                practice_params["fc_threshold"] = st.slider(
                    "调整 FC 阈值（看看红蓝点数量如何变化）",
                    0.5, 3.0, 1.0, 0.25, key="practice_fc"
                )
                practice_params["pvalue_threshold"] = st.select_slider(
                    "调整 P-value 阈值",
                    options=[0.001, 0.01, 0.05, 0.1],
                    value=0.05,
                    key="practice_pv",
                )
            elif practice_type == "heatmap":
                practice_params["top_n_genes"] = st.slider(
                    "展示基因数",
                    10, 100, 50, 10, key="practice_topn"
                )
                practice_params["normalize"] = st.checkbox("Z-score标准化", True, key="practice_norm")

            st.markdown(f"**第3步：生成图表！**")
            if st.button("🎯 绘制练习图表", type="primary", key="practice_btn"):
                with st.spinner("绘制中..."):
                    try:
                        fig, stats = generate_plot(practice_type, data, practice_params)

                        display_stats(stats)
                        st.pyplot(fig, use_container_width=True)

                        st.markdown(f"**第4步：学会解读**")
                        if tutorial and "how" in tutorial:
                            st.markdown(tutorial["how"])

                        download_button(fig, filename=f"practice_{practice_type}")
                        plt.close(fig)
                    except Exception as e:
                        st.error(f"绘图出错: {e}")


# ──────────────────────────────────────────────
# Main routing
# ──────────────────────────────────────────────
if mode == "🎨 快速绘图":
    render_quick_plot()
elif mode == "🤖 AI 助手":
    render_ai_assistant()
elif mode == "📚 学习中心":
    render_learning_center()

# Footer
st.divider()
st.markdown(
    '<div style="text-align:center; color:#999; font-size:0.8rem;">'
    'BioPlotAgent v1.0 | 让生物信息学绘图变得简单 | '
    '<a href="https://github.com/bcefghj/BioPlotAgent">GitHub</a>'
    '</div>',
    unsafe_allow_html=True,
)
