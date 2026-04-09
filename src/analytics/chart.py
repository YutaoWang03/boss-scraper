"""
Matplotlib charts (PRD section 5). English labels + optional LaTeX (matplotlib mathtext or system TeX).
No CJK fonts: category axes are mapped to English for display.
"""

from __future__ import annotations

import os
import shutil
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.analytics import salary as salary_mod
from src.analytics import skills as skills_mod
from src.analytics.company import scatter_company_size_salary

_STYLE_DONE = False

# Experience bucket labels (data are Chinese; plot in English)
_EXPERIENCE_EN = {
    "在校/应届": "Campus / new grad",
    "1年以内": "≤1 yr",
    "1-3年": "1–3 yr",
    "3-5年": "3–5 yr",
    "5-10年": "5–10 yr",
    "10年以上": "10+ yr",
    "经验不限": "Any exp.",
    "未知": "Unknown",
}

_EDU_EN = {
    "学历不限": "Any",
    "初中": "Junior high",
    "高中": "High school",
    "中专": "Vocational",
    "大专": "Associate",
    "本科": "Bachelor",
    "硕士": "Master",
    "博士": "PhD",
    "未知": "Unknown",
}

_SKILL_EN = {
    "机器学习": "Machine learning",
    "深度学习": "Deep learning",
    "大模型": "LLM / GenAI",
    "产品经理": "Product manager",
    "数据分析": "Data analysis",
    "敏捷": "Agile / Scrum",
}


def _en_experience(s: str) -> str:
    return _EXPERIENCE_EN.get(str(s).strip(), str(s))


def _en_edu(s: str) -> str:
    return _EDU_EN.get(str(s).strip(), str(s))


def _en_skill(s: str) -> str:
    return _SKILL_EN.get(str(s).strip(), str(s))


def _setup_matplotlib():
    global _STYLE_DONE
    if _STYLE_DONE:
        return
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Helvetica", "Arial", "sans-serif"]
    # Matplotlib mathtext (no external LaTeX); use $...$ in labels when needed
    plt.rcParams["mathtext.default"] = "regular"
    plt.rcParams["mathtext.fontset"] = "dejavusans"

    if os.environ.get("BOSS_SCRAPER_PLOT_USETEX", "").lower() in ("1", "true", "yes"):
        if shutil.which("latex"):
            plt.rcParams["text.usetex"] = True
            plt.rcParams["font.family"] = "serif"
        else:
            import warnings

            warnings.warn(
                "BOSS_SCRAPER_PLOT_USETEX is set but `latex` was not found; using default (no usetex).",
                UserWarning,
                stacklevel=2,
            )

    _STYLE_DONE = True


def _save(fig, path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    fig.tight_layout()
    fig.savefig(path, dpi=120, bbox_inches="tight")
    plt.close(fig)


def chart_salary_histogram(df: pd.DataFrame, out_path: str) -> bool:
    _setup_matplotlib()
    labels, counts = salary_mod.salary_histogram_counts(df)
    if not counts or sum(counts) == 0:
        return False
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(labels))
    ax.bar(x, counts, color="steelblue", edgecolor="white")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("Job count")
    ax.set_xlabel(r"Monthly salary bin ($\mathrm{CNY/mo}$, est.)")
    ax.set_title("Salary distribution (PRD 5.1)")
    _save(fig, out_path)
    return True


def chart_skills_bar(df: pd.DataFrame, out_path: str, top_n: int = 15) -> bool:
    _setup_matplotlib()
    ranked = skills_mod.aggregate_skill_frequency(df)
    if not ranked:
        return False
    ranked = ranked[:top_n]
    labels = [_en_skill(x[0]) for x in ranked]
    vals = [x[1] for x in ranked]
    fig, ax = plt.subplots(figsize=(8, max(4, top_n * 0.35)))
    y = np.arange(len(labels))
    ax.barh(y, vals, color="teal", edgecolor="white")
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Jobs with keyword hit")
    ax.set_title("Skill keyword ranking (PRD 5.2)")
    _save(fig, out_path)
    return True


def chart_salary_by_experience(df: pd.DataFrame, out_path: str) -> bool:
    _setup_matplotlib()
    g = salary_mod.salary_by_years_bucket(df)
    if g.empty:
        return False
    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(g))
    ax.plot(x, g["mean_salary"].values, marker="o", label="Mean", color="coral")
    ax.plot(x, g["median_salary"].values, marker="s", label="Median", color="seagreen")
    ax.set_xticks(x)
    xlabels = [_en_experience(str(v)) for v in g["years_bucket"].tolist()]
    ax.set_xticklabels(xlabels, rotation=30, ha="right")
    ax.set_ylabel(r"$\mathrm{CNY/mo}$ (estimated)")
    ax.set_title("Salary by experience bucket (PRD 5.3)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    _save(fig, out_path)
    return True


def chart_salary_by_education(df: pd.DataFrame, out_path: str) -> bool:
    _setup_matplotlib()
    g = salary_mod.salary_by_education(df)
    if g.empty:
        return False
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(g))
    ax.bar(x, g["mean_salary"].values, color="mediumpurple", edgecolor="white")
    ax.set_xticks(x)
    xlabels = [_en_edu(str(v)) for v in g["edu_label"].tolist()]
    ax.set_xticklabels(xlabels, rotation=25, ha="right")
    ax.set_ylabel(r"Mean monthly salary ($\mathrm{CNY}$, est.)")
    ax.set_title("Mean salary by education (PRD 5.4)")
    ax.grid(True, axis="y", alpha=0.3)
    _save(fig, out_path)
    return True


def chart_company_size_scatter(df: pd.DataFrame, out_path: str) -> bool:
    _setup_matplotlib()
    sub, _ = scatter_company_size_salary(df)
    if sub.empty:
        return False
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(sub["sizenum"], sub["salary_avg"], alpha=0.5, c="darkblue", edgecolors="none", s=40)
    ax.set_xscale("log")
    ax.set_xlabel("Company size (headcount, heuristic; log scale)")
    ax.set_ylabel(r"Monthly salary ($\mathrm{CNY/mo}$, est.)")
    ax.set_title("Company size vs salary (PRD 5.5, heuristic)")
    ax.grid(True, alpha=0.3)
    _save(fig, out_path)
    return True
