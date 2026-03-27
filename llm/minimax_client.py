"""MiniMax LLM client for BioPlotAgent using OpenAI-compatible API."""

from openai import OpenAI
from config import MINIMAX_API_KEY, MINIMAX_BASE_URL, MINIMAX_MODEL

SYSTEM_PROMPT = """你是 BioPlotAgent —— 一个专业的生物信息学绘图助手，专为零基础用户设计。

你的核心能力：
1. 根据用户的自然语言描述，推荐合适的生物信息学图表类型
2. 解释每种图表的生物学含义和使用场景
3. 帮助用户理解数据格式要求
4. 生成可执行的 Python 绘图代码
5. 用通俗易懂的语言解释分析结果

支持的图表类型：
- 火山图 (Volcano Plot): 展示差异表达基因，X轴为log2FC，Y轴为-log10(p-value)
- 热图 (Heatmap): 展示基因表达模式，颜色深浅代表表达量高低
- PCA图: 主成分分析，展示样本间的整体差异
- 生存分析曲线 (KM Plot): 展示不同组别的生存时间差异
- GO富集分析图: 展示基因本体富集结果
- 柱状图 (Bar Plot): 展示基因表达量或统计数据
- 箱线图 (Box Plot): 展示数据分布和组间差异
- 韦恩图 (Venn Diagram): 展示基因集合间的重叠关系
- MA Plot: 展示表达差异与平均表达量的关系
- 气泡图 (Dot Plot): 多维数据展示

回复规则：
- 始终使用中文回复
- 用类比和生活化的例子解释专业概念
- 如果用户描述不明确，主动询问关键信息
- 每次回复都附上简短的知识点
- 推荐合适的图表时说明原因"""


class BioPlotLLM:
    def __init__(self, api_key: str = None):
        self.client = OpenAI(
            api_key=api_key or MINIMAX_API_KEY,
            base_url=MINIMAX_BASE_URL,
        )
        self.model = MINIMAX_MODEL

    def chat(self, user_message: str, history: list = None) -> str:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=2000,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"调用AI时出错: {str(e)}\n\n请检查API Key是否正确配置。"

    def analyze_data_and_suggest(self, data_description: str) -> str:
        prompt = f"""用户上传了以下数据：
{data_description}

请分析这个数据适合绘制哪些生物信息学图表，并给出推荐理由。
对每种推荐的图表，简要说明：
1. 为什么适合这个数据
2. 能揭示什么生物学信息
3. 数据是否需要预处理"""
        return self.chat(prompt)

    def explain_plot(self, plot_type: str, data_summary: str = "") -> str:
        prompt = f"""请用通俗易懂的语言解释"{plot_type}"：

1. 这种图是什么？用一个生活化的比喻来解释
2. 在生物信息学中常用于什么场景？
3. 怎么解读这种图？（横轴、纵轴、颜色等分别代表什么）
4. 一个好的{plot_type}应该是什么样的？
{f"5. 根据以下数据特征，解读结果：{data_summary}" if data_summary else ""}

请确保零基础的同学也能理解。"""
        return self.chat(prompt)

    def generate_custom_code(self, request: str, data_columns: list = None) -> str:
        col_info = f"\n数据包含以下列：{', '.join(data_columns)}" if data_columns else ""
        prompt = f"""用户需求：{request}{col_info}

请生成完整的Python绘图代码，要求：
1. 使用 matplotlib/seaborn/plotly
2. 代码中包含详细的中文注释，解释每一步在做什么
3. 图表标签使用中文
4. 使用美观的配色方案
5. 代码可以直接运行

只输出Python代码，用```python```包裹。"""
        return self.chat(prompt)
