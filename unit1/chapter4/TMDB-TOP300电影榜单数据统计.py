"""TMDB-TOP300电影榜单数据统计

基于 TMDB_TOP30_Movie_Chart_Analysis.ipynb 整理封装而成，图表样式与原 Notebook 保持一致。

功能：
    需求1：每年电影数量变化折线图
    需求2：不同语言电影数量柱状图
    需求3：不同类型电影数量柱状图
    需求4：不同评分数量占比饼状图

数据：csv_data/movie.csv
输出：csv_data/TMDB-TOP300.png
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

# ==================== 全局配置 ====================
# 展示中文
plt.rcParams['font.sans-serif'] = ['SimHei']
# 解决负号 '-' 显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

# 以脚本所在目录为基准，保证在任意工作目录下运行都能找到数据文件
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / 'csv_data' / 'movie.csv'
SAVE_PATH = BASE_DIR / 'csv_data' / 'TMDB-TOP300.png'

FIG_TITLE = 'TMDB-TOP300电影榜单数据统计'
COLOR = 'green'
SMALL_RATIO = 0.02  # 饼图中占比小于2%的评分合并为"其他"


# ==================== 数据加载 ====================
def load_data(csv_path: Path = CSV_PATH) -> pd.DataFrame:
    """加载数据，并处理年份列的缺失值（用"上映时间"的前4位补齐）。

    本来年份没有缺失值，只是做如果有缺失值该怎么处理的演示。
    """
    data = pd.read_csv(
        csv_path,
        usecols=['电影名', '年份', '上映时间', '类型', '时长', '评分', '语言'],
        dtype={'年份': 'Int64'},  # Int64 允许缺失值，int64 不允许
    )
    # 用"上映时间"的前4位作为年份补齐缺失值（转成数值型，保证列仍为数值类型）
    year_fill = pd.to_numeric(data['上映时间'].str[:4], errors='coerce')
    data['年份'] = data['年份'].fillna(year_fill)
    return data


# ==================== 需求1：每年电影数量变化折线图 ====================
def get_year_count(data: pd.DataFrame) -> tuple[list, list]:
    """按年份分组统计电影数量，并补齐中间没有电影的年份（数量记为0）。"""
    year_count = data.groupby('年份')['年份'].count()

    # x轴数据：从最小年份到最大年份的连续年份列表
    min_year = year_count.index.min()
    max_year = year_count.index.max()
    x = list(range(min_year, max_year + 1))
    # y轴数据：没有电影的年份计为0
    y = [int(year_count.get(i, 0)) for i in x]
    return x, y


def draw_year_line(axes: Axes, x: list, y: list) -> None:
    """绘制每年电影数量变化折线图。"""
    axes.plot(x, y, color=COLOR)
    axes.set_title('每年电影数量变化折线图', fontsize=15)
    axes.set_xlabel('年份', fontsize=12)
    axes.set_ylabel('电影数量', fontsize=12)
    axes.set_xticks(x[::8])
    axes.set_yticks([i for i in range(0, 31, 3)])
    axes.grid(linestyle='--', alpha=0.5)


# ==================== 需求2：不同语言电影数量柱状图 ====================
def get_language_count(data: pd.DataFrame) -> pd.Series:
    """按语言分组统计电影数量，降序排列。"""
    return data.groupby('语言')['语言'].count().sort_values(ascending=False)


def draw_language_bar(axes: Axes, language_count: pd.Series) -> None:
    """绘制不同语言电影数量柱状图。"""
    axes.bar(language_count.index.tolist(), language_count.values.tolist(),
             color=COLOR, width=0.7)
    axes.set_title('不同语言电影数量柱状图', fontsize=15)
    axes.set_xlabel('语言', fontsize=12)
    axes.set_ylabel('电影数量', fontsize=12)
    axes.grid(linestyle='--', alpha=0.5)
    axes.tick_params(axis='x', rotation=90)  # 旋转x轴标签


# ==================== 需求3：不同类型电影数量柱状图 ====================
def get_type_count(data: pd.DataFrame) -> dict:
    """统计不同类型的电影数量（一部电影可能有多个类型，用','分隔）。"""
    type_count = {}
    for types in data['类型'].str.split(','):  # 如: 剧情,犯罪
        for movie_type in types:  # 如: 剧情
            type_count[movie_type] = type_count.get(movie_type, 0) + 1
    return type_count


def draw_type_bar(axes: Axes, type_count: dict) -> None:
    """绘制不同类型电影数量柱状图。"""
    axes.bar(list(type_count.keys()), list(type_count.values()),
             color=COLOR, width=0.7)
    axes.set_title('不同类型电影数量柱状图', fontsize=15)
    axes.set_xlabel('类型', fontsize=12)
    axes.set_ylabel('电影数量', fontsize=12)
    axes.grid(linestyle='--', alpha=0.5)
    axes.tick_params(axis='x', rotation=90)  # 旋转x轴标签


# ==================== 需求4：不同评分数量占比饼状图 ====================
def get_score_count(data: pd.DataFrame, small_ratio: float = SMALL_RATIO) -> pd.Series:
    """统计不同评分的电影数量，占比小于 small_ratio（2%）的合并为"其他"。"""
    score_count = data.groupby('评分')['评分'].count()
    total = score_count.sum()
    large_scores = score_count.loc[score_count >= total * small_ratio]  # 大数据，比例>=2%
    small_scores = score_count.loc[score_count < total * small_ratio]   # 小数据，比例<2%
    if small_scores.shape[0] > 0:
        large_scores = large_scores.copy()  # 显式拷贝，避免修改切片警告
        large_scores['其他'] = small_scores.sum()
    return large_scores


def draw_score_pie(axes: Axes, score_count: pd.Series) -> None:
    """绘制不同评分数量占比饼状图。"""
    scores = score_count.index.tolist()       # 评分列表
    score_values = score_count.values.tolist()  # 数量列表
    axes.pie(score_values, labels=scores, autopct='%1.1f%%', startangle=0)  # startangle 起始角度
    axes.set_title('不同评分数量占比饼状图', fontsize=15)
    axes.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.3))


# ==================== 主流程 ====================
def create_figure() -> tuple:
    """创建画布和2x2子图，返回 (fig, axes1, axes2, axes3, axes4)。"""
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 12), dpi=100)
    # 添加画布标题：x=0.5:X轴位置；y=0.95:y轴位置
    fig.suptitle(FIG_TITLE, fontsize=23, x=0.5, y=0.98)
    # 调整子图间距，hspace:控制垂直间距，wspace:控制水平间距
    fig.subplots_adjust(hspace=0.6, wspace=0.2)
    axes1 = axes[0][0]
    axes2 = axes[0][1]
    axes3 = axes[1][0]
    axes4 = axes[1][1]
    return fig, axes1, axes2, axes3, axes4


def main() -> None:
    """完整分析流程：加载每张子图所需数据 -> 绘图 -> 保存并显示。"""
    _, axes1, axes2, axes3, axes4 = create_figure()
    data = load_data()

    # 需求1：每年电影数量变化折线图
    x, y = get_year_count(data)
    draw_year_line(axes1, x, y)

    # 需求2：不同语言电影数量柱状图
    language_count = get_language_count(data)
    draw_language_bar(axes2, language_count)

    # 需求3：不同类型电影数量柱状图
    type_count = get_type_count(data)
    print(type_count)
    draw_type_bar(axes3, type_count)

    # 需求4：不同评分数量占比饼状图
    score_count = get_score_count(data)
    draw_score_pie(axes4, score_count)

    # 保存并显示画布
    plt.savefig(SAVE_PATH)
    plt.show()


if __name__ == '__main__':
    main()
