"""
从原始导出列派生分析用特征（薪资数值、经验桶、学历序数、规模启发式等）。
"""

from __future__ import annotations

import re
from typing import Optional, Tuple

import numpy as np
import pandas as pd

from src.utils.salary import parse_salary

# 经验桶顺序（用于排序与折线图 X 轴）
YEAR_BUCKET_ORDER = [
    "在校/应届",
    "1年以内",
    "1-3年",
    "3-5年",
    "5-10年",
    "10年以上",
    "经验不限",
    "未知",
]

# 学历 -> 序数（越高表示学历越高）
EDU_ORDER = {
    "学历不限": 0,
    "初中": 1,
    "高中": 2,
    "中专": 3,
    "大专": 4,
    "本科": 5,
    "硕士": 6,
    "博士": 7,
    "未知": -1,
}

# 职位描述中常见「公司规模」写法 -> 代表人数（取区间中点或下限）
_SIZE_PATTERNS = [
    (re.compile(r"0[-–]20人"), 10),
    (re.compile(r"20[-–]99人"), 60),
    (re.compile(r"100[-–]499人"), 300),
    (re.compile(r"500[-–]999人"), 750),
    (re.compile(r"1000[-–]9999人"), 5500),
    (re.compile(r"10000人以上"), 15000),
    (re.compile(r"少于15人"), 8),
    (re.compile(r"15[-–]50人"), 32),
    (re.compile(r"50[-–]150人"), 100),
    (re.compile(r"150[-–]500人"), 325),
    (re.compile(r"500[-–]2000人"), 1250),
    (re.compile(r"2000人以上"), 3000),
]


def _normalize_text(val) -> str:
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return ""
    return str(val).replace("\r\n", "\n").replace("\r", "\n").strip()


def _salary_avg_from_cell(salary_str: str) -> Optional[float]:
    text = _normalize_text(salary_str)
    if not text:
        return None
    low, high, avg, _months = parse_salary(text)
    if avg and avg > 0:
        return float(avg)
    return None


def _parse_exp_edu(combined: str) -> Tuple[str, str]:
    """从「经验学历」合并字段拆出经验桶标签与学历标签。"""
    text = _normalize_text(combined)
    if not text:
        return "未知", "未知"

    exp_label = "未知"
    edu_label = "未知"

    # 经验
    if "在校" in text or "应届" in text:
        exp_label = "在校/应届"
    elif "1年以内" in text or "1年内" in text:
        exp_label = "1年以内"
    elif re.search(r"1[-–]3年", text):
        exp_label = "1-3年"
    elif re.search(r"3[-–]5年", text):
        exp_label = "3-5年"
    elif re.search(r"5[-–]10年", text):
        exp_label = "5-10年"
    elif "10年以上" in text or "10年+" in text:
        exp_label = "10年以上"
    elif "经验不限" in text:
        exp_label = "经验不限"

    # 学历（取长匹配优先）
    for key in ("博士", "硕士", "本科", "大专", "中专", "高中", "初中"):
        if key in text:
            edu_label = key
            break
    if "学历不限" in text and edu_label == "未知":
        edu_label = "学历不限"

    return exp_label, edu_label


def _company_size_from_description(desc: str) -> Optional[float]:
    text = _normalize_text(desc)
    if not text:
        return None
    for pattern, midpoint in _SIZE_PATTERNS:
        if pattern.search(text):
            return float(midpoint)
    return None


def enrich_jobs(df: pd.DataFrame) -> pd.DataFrame:
    """
    原地式复制并增加分析列：salary_avg, years_bucket, years_order, edu_level, edu_label, sizenum, text_for_skills。
    """
    out = df.copy()

    sal_col = "薪资范围" if "薪资范围" in out.columns else None
    if sal_col:
        out["salary_avg"] = out[sal_col].map(_salary_avg_from_cell)
    else:
        out["salary_avg"] = np.nan

    exp_col = "经验学历" if "经验学历" in out.columns else None
    buckets = []
    edus = []
    year_orders = []
    if exp_col:
        for v in out[exp_col]:
            b, e = _parse_exp_edu(v)
            buckets.append(b)
            edus.append(e)
            try:
                year_orders.append(YEAR_BUCKET_ORDER.index(b))
            except ValueError:
                year_orders.append(len(YEAR_BUCKET_ORDER) - 1)
    else:
        buckets = ["未知"] * len(out)
        edus = ["未知"] * len(out)
        year_orders = [len(YEAR_BUCKET_ORDER) - 1] * len(out)

    out["years_bucket"] = buckets
    out["edu_label"] = edus
    out["edu_level"] = [EDU_ORDER.get(x, -1) for x in edus]
    out["years_order"] = year_orders

    desc_col = "职位描述" if "职位描述" in out.columns else None
    if desc_col:
        out["sizenum"] = out[desc_col].map(_company_size_from_description)
    else:
        out["sizenum"] = np.nan

    # 技能词频用：描述 + 职位标签（若存在）
    tag_col = "职位标签" if "职位标签" in out.columns else None
    parts = []
    if desc_col:
        parts.append(out[desc_col].fillna("").map(_normalize_text))
    else:
        parts.append(pd.Series([""] * len(out)))
    if tag_col:
        parts.append(out[tag_col].fillna("").map(_normalize_text))
    out["text_for_skills"] = parts[0] if len(parts) == 1 else (parts[0] + "\n" + parts[1])

    return out
