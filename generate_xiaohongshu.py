"""Generate Xiaohongshu (小红书) promotional images for BioPlotAgent."""

import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "xiaohongshu")
SHOWCASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "showcase")
os.makedirs(OUT, exist_ok=True)

# 小红书推荐尺寸 3:4 (1080x1440) 或 1:1 (1080x1080)
W, H = 1080, 1440

try:
    font_title = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 58)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
    font_body = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
    font_small = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 22)
    font_tag = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 24)
    font_big = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 72)
except:
    font_title = ImageFont.load_default()
    font_subtitle = font_title
    font_body = font_title
    font_small = font_title
    font_tag = font_title
    font_big = font_title


def draw_rounded_rect(draw, xy, radius, fill, outline=None, width=0):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_tag(draw, x, y, text, bg_color, text_color="white"):
    bbox = draw.textbbox((0, 0), text, font=font_tag)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    padding = 12
    draw_rounded_rect(draw, [x, y, x + tw + padding * 2, y + th + padding * 2 - 4], radius=15, fill=bg_color)
    draw.text((x + padding, y + padding - 2), text, fill=text_color, font=font_tag)
    return tw + padding * 2 + 8


def add_plot_thumbnail(canvas, img_path, x, y, w, h, shadow=True):
    if not os.path.exists(img_path):
        return
    img = Image.open(img_path).convert("RGBA")
    img.thumbnail((w - 8, h - 8), Image.LANCZOS)
    if shadow:
        shadow_layer = Image.new("RGBA", (img.width + 10, img.height + 10), (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow_layer)
        shadow_draw.rounded_rectangle([5, 5, img.width + 5, img.height + 5], radius=8, fill=(0, 0, 0, 60))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(4))
        paste_x = x + (w - shadow_layer.width) // 2
        paste_y = y + (h - shadow_layer.height) // 2
        canvas.paste(shadow_layer, (paste_x, paste_y), shadow_layer)
    paste_x = x + (w - img.width) // 2
    paste_y = y + (h - img.height) // 2
    canvas.paste(img, (paste_x, paste_y))


# ═══════════════════════════════════════════════
# Card 1: 封面图 — 9宫格展示
# ═══════════════════════════════════════════════
print("[1/5] 生成封面图...")
c1 = Image.new("RGB", (W, H), "#FFFFFF")
d1 = ImageDraw.Draw(c1)

# Header gradient bar
for i in range(200):
    ratio = i / 200
    r = int(44 + (52 - 44) * ratio)
    g = int(62 + (152 - 62) * ratio)
    b = int(80 + (219 - 80) * ratio)
    d1.line([(0, i), (W, i)], fill=(r, g, b))

d1.text((W // 2, 50), "BioPlotAgent", fill="white", font=font_big, anchor="mt")
d1.text((W // 2, 135), "零基础也能画出发表级图表", fill="#E8E8E8", font=font_subtitle, anchor="mt")

# Tags
tag_y = 175
tags = ["AI驱动", "10种图表", "一键出图", "完全免费"]
tag_colors = ["#E74C3C", "#3498DB", "#2ECC71", "#9B59B6"]
tag_x = 130
for text, color in zip(tags, tag_colors):
    tag_x += draw_tag(d1, tag_x, tag_y, text, color)

# Plot grid (3x3)
plots = [
    "01_volcano_plot.png", "02_heatmap.png", "03_pca_plot.png",
    "04_survival_curve.png", "05_go_enrichment_bar.png", "06_go_enrichment_dot.png",
    "07_bar_plot.png", "08_box_plot.png", "09_venn_diagram.png",
]
labels = [
    "火山图", "热图", "PCA分析",
    "生存曲线", "GO富集(柱状)", "GO富集(气泡)",
    "柱状图", "箱线图", "韦恩图",
]
GRID_TOP = 230
CELL_W = (W - 80) // 3
CELL_H = (H - GRID_TOP - 200) // 3

for idx, (pfile, label) in enumerate(zip(plots, labels)):
    row, col = divmod(idx, 3)
    cx = 40 + col * CELL_W
    cy = GRID_TOP + row * CELL_H

    d1.rounded_rectangle([cx + 2, cy + 2, cx + CELL_W - 2, cy + CELL_H - 2], radius=8, fill="#F8F9FA", outline="#E0E0E0")
    add_plot_thumbnail(c1, os.path.join(SHOWCASE, pfile), cx + 6, cy + 6, CELL_W - 12, CELL_H - 40, shadow=False)
    d1.text((cx + CELL_W // 2, cy + CELL_H - 22), label, fill="#2C3E50", font=font_small, anchor="mm")

# Footer
footer_y = H - 150
d1.line([(40, footer_y), (W - 40, footer_y)], fill="#E0E0E0", width=1)
d1.text((W // 2, footer_y + 20), "生物信息学智能绘图助手", fill="#2C3E50", font=font_subtitle, anchor="mt")
d1.text((W // 2, footer_y + 65), "上传数据 → AI分析 → 一键出图 → 下载高清图", fill="#7F8C8D", font=font_small, anchor="mt")
d1.text((W // 2, footer_y + 100), "github.com/bcefghj/BioPlotAgent", fill="#3498DB", font=font_small, anchor="mt")

c1.save(os.path.join(OUT, "01_cover.png"), dpi=(200, 200))
print("  ✓ 01_cover.png")


# ═══════════════════════════════════════════════
# Card 2: 火山图特写
# ═══════════════════════════════════════════════
print("[2/5] 火山图特写...")
c2 = Image.new("RGB", (W, H), "#FFFFFF")
d2 = ImageDraw.Draw(c2)

for i in range(120):
    ratio = i / 120
    r = int(231 + (255 - 231) * ratio)
    g = int(76 + (255 - 76) * ratio)
    b = int(60 + (255 - 60) * ratio)
    d2.line([(0, i), (W, i)], fill=(r, g, b))

d2.text((W // 2, 30), "差异表达基因 · 火山图", fill="white", font=font_title, anchor="mt")
d2.text((W // 2, 95), "RNA-seq分析必备 | 一图看懂哪些基因变了", fill="#FFE0DC", font=font_body, anchor="mt")

add_plot_thumbnail(c2, os.path.join(SHOWCASE, "01_volcano_plot.png"), 30, 140, W - 60, 650)

# Explanation
info_y = 820
d2.rounded_rectangle([40, info_y, W - 40, info_y + 350], radius=15, fill="#FFF3E0", outline="#F39C12", width=2)
info_lines = [
    ("💡 怎么看这张图？", font_subtitle, "#E67E22"),
    ("", font_small, "#333"),
    ("🔴 红色点 = 上调基因（实验组表达升高）", font_body, "#E74C3C"),
    ("🔵 蓝色点 = 下调基因（实验组表达降低）", font_body, "#3498DB"),
    ("⚪ 灰色点 = 无显著变化", font_body, "#95A5A6"),
    ("", font_small, "#333"),
    ("越靠上 = 越显著 | 越靠两侧 = 变化越大", font_body, "#2C3E50"),
]
for i, (text, font, color) in enumerate(info_lines):
    if text:
        d2.text((70, info_y + 18 + i * 44), text, fill=color, font=font)

# Stats
stats_y = info_y + 370
d2.text((W // 2, stats_y), "本图统计：上调 980 个 | 下调 918 个 | 共 5000 个基因", fill="#7F8C8D", font=font_small, anchor="mt")

# Bottom
d2.text((W // 2, H - 80), "BioPlotAgent · 零基础一键生成", fill="#CCCCCC", font=font_small, anchor="mt")
d2.text((W // 2, H - 45), "github.com/bcefghj/BioPlotAgent", fill="#3498DB", font=font_small, anchor="mt")

c2.save(os.path.join(OUT, "02_volcano_detail.png"), dpi=(200, 200))
print("  ✓ 02_volcano_detail.png")


# ═══════════════════════════════════════════════
# Card 3: 生存分析特写
# ═══════════════════════════════════════════════
print("[3/5] 生存分析特写...")
c3 = Image.new("RGB", (W, H), "#FFFFFF")
d3 = ImageDraw.Draw(c3)

for i in range(120):
    ratio = i / 120
    r = int(52 + (255 - 52) * ratio)
    g = int(152 + (255 - 152) * ratio)
    b = int(219 + (255 - 219) * ratio)
    d3.line([(0, i), (W, i)], fill=(r, g, b))

d3.text((W // 2, 30), "Kaplan-Meier 生存分析", fill="white", font=font_title, anchor="mt")
d3.text((W // 2, 95), "TCGA数据分析必备 | 评估基因预后价值", fill="#DCE9F5", font=font_body, anchor="mt")

add_plot_thumbnail(c3, os.path.join(SHOWCASE, "04_survival_curve.png"), 30, 140, W - 60, 650)

info_y = 820
d3.rounded_rectangle([40, info_y, W - 40, info_y + 350], radius=15, fill="#E8F8F5", outline="#1ABC9C", width=2)
info_lines = [
    ("💡 怎么看生存曲线？", font_subtitle, "#1ABC9C"),
    ("", font_small, "#333"),
    ("📈 蓝色线（低表达组）下降更慢 = 存活更久", font_body, "#3498DB"),
    ("📉 红色线（高表达组）下降更快 = 预后更差", font_body, "#E74C3C"),
    ("", font_small, "#333"),
    ("p = 0.0014 < 0.05 → 两组差异显著！", font_body, "#2C3E50"),
    ("说明这个基因的表达水平与患者预后相关", font_body, "#7F8C8D"),
]
for i, (text, font, color) in enumerate(info_lines):
    if text:
        d3.text((70, info_y + 18 + i * 44), text, fill=color, font=font)

stats_y = info_y + 370
d3.text((W // 2, stats_y), "200名患者 | 高表达组 vs 低表达组 | Log-rank检验", fill="#7F8C8D", font=font_small, anchor="mt")

d3.text((W // 2, H - 80), "BioPlotAgent · 零基础一键生成", fill="#CCCCCC", font=font_small, anchor="mt")
d3.text((W // 2, H - 45), "github.com/bcefghj/BioPlotAgent", fill="#3498DB", font=font_small, anchor="mt")

c3.save(os.path.join(OUT, "03_survival_detail.png"), dpi=(200, 200))
print("  ✓ 03_survival_detail.png")


# ═══════════════════════════════════════════════
# Card 4: 功能亮点展示
# ═══════════════════════════════════════════════
print("[4/5] 功能亮点...")
c4 = Image.new("RGB", (W, H), "#FFFFFF")
d4 = ImageDraw.Draw(c4)

for i in range(160):
    ratio = i / 160
    r = int(155 + (255 - 155) * ratio)
    g = int(89 + (255 - 89) * ratio)
    b = int(182 + (255 - 182) * ratio)
    d4.line([(0, i), (W, i)], fill=(r, g, b))

d4.text((W // 2, 30), "为什么选择 BioPlotAgent？", fill="white", font=font_title, anchor="mt")
d4.text((W // 2, 100), "专为生信小白打造的绘图神器", fill="#F0E0F8", font=font_body, anchor="mt")

features = [
    ("🎨", "三种模式随心切换", "快速绘图 · AI助手 · 学习中心\n不会？AI教你！要图？一键生成！"),
    ("📊", "10种专业图表", "火山图/热图/PCA/生存分析/GO富集\n柱状图/箱线图/韦恩图/MA Plot/气泡图"),
    ("🧠", "AI 智能分析", "基于 MiniMax M2.7 大模型\n上传数据→自动推荐图表→解释结果"),
    ("📚", "边学边用", "每种图表配详细教程\n用生活比喻解释专业概念，看得懂！"),
    ("💾", "高清导出", "支持 PNG（300dpi）和 PDF 矢量图\n直接用于论文发表，不用再P图"),
    ("🆓", "完全免费开源", "MIT 协议，随便用\n代码全部公开，欢迎 Star ⭐"),
]

card_y = 180
for i, (icon, title, desc) in enumerate(features):
    y = card_y + i * 195
    d4.rounded_rectangle([50, y, W - 50, y + 180], radius=12, fill="#F8F9FA", outline="#E0E0E0")
    d4.text((90, y + 20), icon, font=font_title)
    d4.text((160, y + 25), title, fill="#2C3E50", font=font_subtitle)
    lines = desc.split("\n")
    for j, line in enumerate(lines):
        d4.text((160, y + 75 + j * 34), line, fill="#7F8C8D", font=font_small)

d4.text((W // 2, H - 45), "github.com/bcefghj/BioPlotAgent", fill="#3498DB", font=font_small, anchor="mt")

c4.save(os.path.join(OUT, "04_features.png"), dpi=(200, 200))
print("  ✓ 04_features.png")


# ═══════════════════════════════════════════════
# Card 5: 使用教程/快速开始
# ═══════════════════════════════════════════════
print("[5/5] 快速开始教程...")
c5 = Image.new("RGB", (W, H), "#FFFFFF")
d5 = ImageDraw.Draw(c5)

for i in range(120):
    ratio = i / 120
    r = int(46 + (255 - 46) * ratio)
    g = int(204 + (255 - 204) * ratio)
    b = int(113 + (255 - 113) * ratio)
    d5.line([(0, i), (W, i)], fill=(r, g, b))

d5.text((W // 2, 30), "3步上手 BioPlotAgent", fill="white", font=font_title, anchor="mt")
d5.text((W // 2, 95), "从安装到出图，5分钟搞定！", fill="#D5F5E3", font=font_body, anchor="mt")

steps = [
    ("Step 1", "安装", "pip install -r requirements.txt", "复制粘贴一行命令即可"),
    ("Step 2", "启动", "streamlit run app.py", "浏览器自动打开，无需配置"),
    ("Step 3", "绘图", "选择图表 → 上传数据 → 点击生成", "就是这么简单！"),
]

step_y = 150
for i, (step, title, cmd, note) in enumerate(steps):
    y = step_y + i * 240
    d5.rounded_rectangle([50, y, W - 50, y + 220], radius=15, fill="#F0FFF4", outline="#2ECC71", width=2)

    d5.ellipse([70, y + 15, 140, y + 85], fill="#2ECC71")
    d5.text((105, y + 50), str(i + 1), fill="white", font=font_title, anchor="mm")

    d5.text((160, y + 25), f"{step}: {title}", fill="#2C3E50", font=font_subtitle)

    d5.rounded_rectangle([70, y + 85, W - 70, y + 135], radius=8, fill="#1A1A2E")
    d5.text((90, y + 95), f"$ {cmd}", fill="#2ECC71", font=font_body)

    d5.text((70, y + 155), f"💡 {note}", fill="#7F8C8D", font=font_small)

# Tips
tips_y = step_y + 3 * 240 + 20
d5.rounded_rectangle([50, tips_y, W - 50, tips_y + 250], radius=15, fill="#FFF3CD", outline="#F39C12", width=2)
d5.text((W // 2, tips_y + 20), "💡 小贴士", fill="#E67E22", font=font_subtitle, anchor="mt")
tips = [
    "• 快速绘图和学习中心不需要API Key，可以直接用！",
    "• AI助手需要 MiniMax API Key（免费注册即可获取）",
    "• 支持 CSV、TSV、XLSX 格式的数据文件",
    "• 图片支持高清 PNG（适合PPT）和 PDF（适合论文）",
]
for i, tip in enumerate(tips):
    d5.text((80, tips_y + 65 + i * 36), tip, fill="#856404", font=font_small)

d5.text((W // 2, H - 45), "github.com/bcefghj/BioPlotAgent", fill="#3498DB", font=font_small, anchor="mt")

c5.save(os.path.join(OUT, "05_quickstart.png"), dpi=(200, 200))
print("  ✓ 05_quickstart.png")


print(f"\n✅ All 5 xiaohongshu cards generated!")
print(f"📁 Output: {OUT}")
for f in sorted(os.listdir(OUT)):
    sz = os.path.getsize(os.path.join(OUT, f)) // 1024
    print(f"  - {f} ({sz}KB)")
