"""
薪资分布、按经验/学历分组的聚合（对应 PRD 5.1、5.3、5.4）。
"""

from __future__ import annotations

from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from src.analytics.features import YEAR_BUCKET_ORDER

# 每组至少多少条才参与图表（避免单点噪声）
MIN_GROUP_SIZE = 2

# 薪资直方图默认分箱（单位：元/月）
DEFAULT_SALARY_BINS = [0, 15000, 25000, 35000, 45000, 60000, 80000, 100000, 150000, 10**9]
DEFAULT_SALARY_BIN_LABELS = [
    "<15k",
    "15-25k",
    "25-35k",
    "35-45k",
    "45-60k",
    "60-80k",
    "80-100k",
    "100-150k",
    ">150k",
]


def salary_histogram_counts(df: pd.DataFrame) -> Tuple[List[str], List[int]]:
    """有效 salary_avg 的区间计数，用于直方图与报告表格。"""
    s = df["salary_avg"].dropna()
    if s.empty:
        return [], []

    counts, _ = np.histogram(s, bins=DEFAULT_SALARY_BINS)
    labels = list(DEFAULT_SALARY_BIN_LABELS)
    # 长度应与 counts 一致
    return labels[: len(counts)], [int(x) for x in counts]


def salary_by_years_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """每个经验桶的薪资均值与中位数（过滤样本不足的桶）。"""
    sub = df.dropna(subset=["salary_avg"])
    if sub.empty:
        return pd.DataFrame(columns=["years_bucket", "mean_salary", "median_salary", "count"])

    g = sub.groupby("years_bucket", observed=False)["salary_avg"].agg(["mean", "median", "count"])
    g = g.reset_index()
    g.columns = ["years_bucket", "mean_salary", "median_salary", "count"]
    g = g[g["count"] >= MIN_GROUP_SIZE]
    # 按既定顺序排序
    order_map = {b: i for i, b in enumerate(YEAR_BUCKET_ORDER)}
    g["_ord"] = g["years_bucket"].map(lambda x: order_map.get(x, 999))
    g = g.sort_values("_ord").drop(columns=["_ord"])
    return g


def salary_by_education(df: pd.DataFrame) -> pd.DataFrame:
    """每个学历标签的薪资均值（过滤未知/不限且样本过少时可仍显示但标注）。"""
    sub = df.dropna(subset=["salary_avg"])
    if sub.empty:
        return pd.DataFrame(columns=["edu_label", "mean_salary", "median_salary", "count"])

    g = sub.groupby("edu_label", observed=False)["salary_avg"].agg(["mean", "median", "count"])
    g = g.reset_index()
    g.columns = ["edu_label", "mean_salary", "median_salary", "count"]
    g = g[g["count"] >= MIN_GROUP_SIZE]
    g = g.sort_values("mean_salary", ascending=False)
    return g


def summary_stats(df: pd.DataFrame) -> Dict[str, float]:
    """整体薪资摘要。"""
    s = df["salary_avg"].dropna()
    if s.empty:
        return {"count": 0, "mean": float("nan"), "median": float("nan")}
    return {
        "count": float(len(s)),
        "mean": float(s.mean()),
        "median": float(s.median()),
    }
