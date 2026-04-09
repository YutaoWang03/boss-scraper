"""
串联加载、特征、聚合与图表，生成 Markdown 报告。
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from typing import List, Optional, Union

import pandas as pd

from src.analytics.chart import (
    chart_company_size_scatter,
    chart_salary_by_education,
    chart_salary_by_experience,
    chart_salary_histogram,
    chart_skills_bar,
)
from src.analytics.company import scatter_company_size_salary
from src.analytics.features import enrich_jobs
from src.analytics.load import load_jobs
from src.analytics import salary as salary_mod
from src.analytics import skills as skills_mod

DEFAULT_REPORT_ROOT = "output/reports"


def _slug(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text.strip())[:80]
    return s.strip("_") or "report"


def run_analysis(
    jobs_or_path: Union[str, List[dict], pd.DataFrame],
    report_dir: Optional[str] = None,
    basename: Optional[str] = None,
    max_rows: Optional[int] = None,
) -> str:
    """
    对职位数据运行完整分析并写入 report.md 与图表。

    Args:
        jobs_or_path: CSV/JSON 路径、dict 列表或 DataFrame。
        report_dir: 报告根目录，默认 ./output/reports。
        basename: 子目录名；默认从文件名或时间戳生成。
        max_rows: 可选，随机截断行数（大数据时）。

    Returns:
        生成的 report.md 绝对路径。

    Raises:
        FileNotFoundError, ValueError: 见 load_jobs / 空数据。
    """
    df = load_jobs(jobs_or_path)
    if max_rows is not None and len(df) > max_rows:
        df = df.sample(n=max_rows, random_state=42).reset_index(drop=True)

    if isinstance(jobs_or_path, str) and basename is None:
        basename = _slug(os.path.splitext(os.path.basename(jobs_or_path))[0])
    if not basename:
        basename = datetime.now().strftime("analysis_%Y%m%d_%H%M%S")

    root = os.path.abspath(report_dir or DEFAULT_REPORT_ROOT)
    out_dir = os.path.join(root, basename)
    os.makedirs(out_dir, exist_ok=True)

    df = enrich_jobs(df)
    n = len(df)
    sal_stats = salary_mod.summary_stats(df)
    labels, counts = salary_mod.salary_histogram_counts(df)
    skill_rank = skills_mod.aggregate_skill_frequency(df)
    sub_size, size_stats = scatter_company_size_salary(df)

    # 图表
    fig_dir = out_dir
    flags = {
        "salary_hist": chart_salary_histogram(df, os.path.join(fig_dir, "salary_histogram.png")),
        "skills": chart_skills_bar(df, os.path.join(fig_dir, "skills_bar.png")),
        "exp_line": chart_salary_by_experience(df, os.path.join(fig_dir, "salary_by_experience.png")),
        "edu_bar": chart_salary_by_education(df, os.path.join(fig_dir, "salary_by_education.png")),
        "size_scatter": chart_company_size_scatter(df, os.path.join(fig_dir, "size_salary_scatter.png")),
    }

    # Markdown
    lines: List[str] = []
    lines.append(f"# 职位数据分析报告\n")
    lines.append(f"- 样本数: **{n}**\n")
    lines.append(f"- 有效薪资样本: **{int(sal_stats['count'])}**（`parse_salary` 可解析为月薪估算）\n")
    if sal_stats["count"]:
        lines.append(
            f"- 薪资均值: **{sal_stats['mean']:.0f}** 元/月；中位数: **{sal_stats['median']:.0f}** 元/月\n"
        )
    lines.append("\n> 薪资来自「薪资范围」字段解析，规模来自「职位描述」中的常见人数表述启发式提取，仅供参考（见 PRD 风险说明）。\n")

    lines.append("\n## 1. 薪资区间分布（PRD 5.1）\n")
    lines.append("*了解市场行情区间分布。*\n")
    if flags["salary_hist"]:
        lines.append("![薪资分布](salary_histogram.png)\n")
    else:
        lines.append("*（无可解析薪资，跳过图表）*\n")
    if labels and counts:
        lines.append("\n| 区间 | 职位数 |\n|------|--------|\n")
        for lb, c in zip(labels, counts):
            lines.append(f"| {lb} | {c} |\n")

    lines.append("\n## 2. 技能关键词排行（PRD 5.2）\n")
    lines.append("*从职位描述与标签文本中按关键词表计数。*\n")
    if flags["skills"]:
        lines.append("![技能排行](skills_bar.png)\n")
    else:
        lines.append("*（无命中关键词）*\n")
    if skill_rank:
        lines.append("\n| 技能 | 职位数 |\n|------|--------|\n")
        for name, c in skill_rank[:20]:
            lines.append(f"| {name} | {c} |\n")

    lines.append("\n## 3. 经验与薪资（PRD 5.3）\n")
    lines.append("*我的经验值多少钱？（按经验桶聚合）*\n")
    if flags["exp_line"]:
        lines.append("![经验薪资](salary_by_experience.png)\n")
    else:
        lines.append("*（数据不足或无可解析薪资）*\n")

    lines.append("\n## 4. 学历与薪资（PRD 5.4）\n")
    lines.append("*学历溢价粗看：各学历平均薪资。*\n")
    if flags["edu_bar"]:
        lines.append("![学历薪资](salary_by_education.png)\n")
    else:
        lines.append("*（数据不足）*\n")

    lines.append("\n## 5. 公司规模与薪资（PRD 5.5）\n")
    lines.append(
        f"*大公司是否给得更多：描述中推断规模 vs 薪资。"
        f" 覆盖率约 **{size_stats['coverage_pct']:.1f}%**（{int(size_stats['rows_with_size_and_salary'])}/{int(size_stats['rows_total'])} 条同时有规模与薪资）。*\n"
    )
    if flags["size_scatter"]:
        lines.append("![规模薪资散点](size_salary_scatter.png)\n")
    else:
        lines.append("*（描述中未识别到规模信息或无可解析薪资）*\n")

    report_path = os.path.join(out_dir, "report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"\n📑 分析报告已生成: {report_path}")
    return report_path
