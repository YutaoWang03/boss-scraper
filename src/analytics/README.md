# `src/analytics/` 数据分析

离线分析爬虫导出的职位数据（CSV / JSON）或内存中的 `list[dict]`，生成 **Markdown 报告** 与 **PNG 图表**，对应 [docs/PRD.md](../../docs/PRD.md) 第 2.2、第 5 节。

## 模块一览

| 文件 | 说明 |
|------|------|
| `load.py` | `load_jobs(path \| list \| DataFrame)` → DataFrame |
| `features.py` | `enrich_jobs(df)`：解析月薪、`经验学历` 拆桶、描述内规模启发式、`text_for_skills` |
| `salary.py` | 薪资直方分箱、按经验/学历聚合 |
| `skills.py` | 关键词表 + 在描述/标签中计数 |
| `company.py` | 规模与薪资散点用数据子集与覆盖率 |
| `chart.py` | Matplotlib 出图：英文标签 + mathtext（`$\mathrm{CNY/mo}$` 等）；不设 CJK 字体。若已安装 LaTeX 且设置环境变量 `BOSS_SCRAPER_PLOT_USETEX=1`，则启用 `text.usetex`。 |
| `report.py` | **`run_analysis(...)`** 唯一对外入口 |

## 依赖

- `pandas`（与 `data/storage` 导出列名一致：中文表头）
- `matplotlib`
- `src/utils/salary.py` 的 `parse_salary`（与爬虫解密逻辑一致）

不依赖 `api/`、`core/`，避免与浏览器爬虫循环引用。

## 使用示例

```python
from src.analytics.report import run_analysis

run_analysis("output/关键词_城市_20260101_120000.csv")
run_analysis("output/data.json", report_dir="output/reports", basename="my_batch")
```

命令行（项目根目录）：

```bash
python main.py --analyze output/your_export.csv
python main.py --analyze output/your_export.json --report-dir ./output/reports
```

交互向导中选择 **「数据分析（离线）」** 或 **「抓取并分析」** 亦可触发同一管线。

## 输出

默认目录：`output/reports/<basename>/`

- `report.md`：说明、表格与插图引用
- `salary_histogram.png`、`skills_bar.png`、`salary_by_experience.png`、`salary_by_education.png`、`size_salary_scatter.png`（数据不足时对应章节会说明并可能跳过图）

## 限制（与 PRD 一致）

- 月薪来自「薪资范围」文本解析，解密/格式异常时可能缺失。
- 公司规模未在列表页结构化采集，仅从「职位描述」中常见表述推断，覆盖率因数据而异。

更多架构说明见 [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md)。
