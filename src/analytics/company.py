"""
公司规模与薪资散点数据准备（PRD 5.5）；规模来自职位描述启发式解析。
"""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd


def scatter_company_size_salary(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    返回同时有 sizenum 与 salary_avg 的行，以及覆盖率统计。
    """
    sub = df.dropna(subset=["salary_avg", "sizenum"])
    n_all = len(df)
    n_both = len(sub)
    coverage = (n_both / n_all * 100.0) if n_all else 0.0
    stats = {
        "rows_total": float(n_all),
        "rows_with_size_and_salary": float(n_both),
        "coverage_pct": coverage,
    }
    return sub, stats
