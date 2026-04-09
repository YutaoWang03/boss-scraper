"""
从 CSV / JSON 或内存列表加载职位数据为 DataFrame。
"""

from __future__ import annotations

import json
import os
from typing import Any, List, Union

import pandas as pd


def load_jobs(source: Union[str, List[dict], pd.DataFrame]) -> pd.DataFrame:
    """
    加载职位数据。

    Args:
        source: 文件路径（.csv / .json）、dict 列表，或已有 DataFrame。

    Returns:
        非空 DataFrame（列名保持导出时的中文）。

    Raises:
        FileNotFoundError: 路径不存在。
        ValueError: 空数据或无法解析。
    """
    if isinstance(source, pd.DataFrame):
        df = source.copy()
    elif isinstance(source, list):
        if not source:
            raise ValueError("职位列表为空")
        df = pd.DataFrame(source)
    elif isinstance(source, str):
        path = os.path.abspath(source)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"文件不存在: {path}")
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(path, encoding="utf-8-sig")
        elif ext == ".json":
            with open(path, encoding="utf-8") as f:
                raw: Any = json.load(f)
            if isinstance(raw, dict) and "jobs" in raw:
                raw = raw["jobs"]
            if not isinstance(raw, list):
                raise ValueError("JSON 应为职位对象数组，或含 jobs 键的对象")
            df = pd.DataFrame(raw)
        else:
            raise ValueError(f"不支持的文件类型: {ext}，请使用 .csv 或 .json")
    else:
        raise TypeError(f"不支持的 source 类型: {type(source)}")

    if df.empty:
        raise ValueError("加载结果为空表，无可用职位行")
    return df
