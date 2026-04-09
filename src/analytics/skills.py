"""
技能词频（PRD 5.2）：关键词表 + 在职位描述/标签文本中计数。
"""

from __future__ import annotations

import re
from collections import Counter
from typing import List, Tuple

import pandas as pd

# 可维护的技术与产品向关键词（小写匹配时对英文；中文直接子串）
SKILL_KEYWORDS: List[Tuple[str, str]] = [
    # (显示名, 匹配用正则或短语) — 使用正则时需忽略大小写对英文
    ("Python", r"Python|python"),
    ("Java", r"\bJava\b|java(?!script)"),
    ("JavaScript", r"JavaScript|javascript|JS\b|js\b"),
    ("TypeScript", r"TypeScript|typescript|TS\b"),
    ("Go", r"\bGo\b|Golang|golang"),
    ("C++", r"C\+\+|\bcpp\b"),
    ("Rust", r"\bRust\b"),
    ("SQL", r"\bSQL\b|MySQL|PostgreSQL|数据库"),
    ("Spark", r"\bSpark\b"),
    ("Hadoop", r"Hadoop|Hive"),
    ("机器学习", r"机器学习|machine learning|\bML\b"),
    ("深度学习", r"深度学习|deep learning"),
    ("NLP", r"\bNLP\b|自然语言"),
    ("CV", r"计算机视觉|图像识别|视觉算法"),
    ("大模型", r"大模型|LLM|GPT|AIGC"),
    ("PyTorch", r"PyTorch|pytorch"),
    ("TensorFlow", r"TensorFlow|tensorflow"),
    ("Kubernetes", r"Kubernetes|K8s|k8s"),
    ("Docker", r"Docker|docker|容器"),
    ("AWS", r"\bAWS\b|亚马逊云"),
    ("Linux", r"Linux|linux"),
    ("React", r"React|react"),
    ("Vue", r"Vue\.?js|\bVue\b"),
    ("Node", r"Node\.?js|\bNode\b"),
    ("产品经理", r"产品经理|产品策划"),
    ("数据分析", r"数据分析|数据分析师"),
    ("Tableau", r"Tableau|Power\s*BI|FineBI"),
    ("Figma", r"Figma|figma|Sketch"),
    ("敏捷", r"敏捷|Scrum|迭代"),
]

# 预编译
_COMPILED = [(label, re.compile(pattern, re.IGNORECASE)) for label, pattern in SKILL_KEYWORDS]


def count_skills_in_text(text: str) -> Counter:
    c: Counter = Counter()
    if not text or not str(text).strip():
        return c
    for label, rx in _COMPILED:
        if rx.search(str(text)):
            c[label] += 1
    return c


def aggregate_skill_frequency(df: pd.DataFrame, text_col: str = "text_for_skills") -> List[Tuple[str, int]]:
    """全表合并计数，返回 (技能, 出现职位数) 降序列表。"""
    total = Counter()
    if text_col not in df.columns:
        return []
    for text in df[text_col]:
        total.update(count_skills_in_text(text))
    ranked = total.most_common()
    return ranked
