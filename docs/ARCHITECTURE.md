# 架构设计文档

## 整体架构

采用分层架构设计，将爬虫项目分为以下层次：

```
┌─────────────────────────────────────────┐
│            CLI 入口层 (main.py)          │
│     爬虫流程 | --analyze 离线分析入口      │
├─────────────────────────────────────────┤
│              API 层 (api/)               │
│              爬虫入口 (scraper.py)        │
├─────────────────────────────────────────┤
│           分析层 (analytics/)            │
│  load | features | salary/skills/company │
│       chart | report (run_analysis)      │
├─────────────────────────────────────────┤
│              核心层 (core/)               │
│    browser.py | detector.py | parser.py  │
├─────────────────────────────────────────┤
│              工具层 (utils/)             │
│        salary.py | delay.py             │
├─────────────────────────────────────────┤
│              数据层 (data/)               │
│   storage.py | cache.py | models.py     │
├─────────────────────────────────────────┤
│            配置层 (config.py)             │
└─────────────────────────────────────────┘
```

## 各层职责

### 1. CLI 入口层 (main.py)

- 解析命令行参数（含 `--analyze` / `--report-dir`）
- 交互式输入处理（数据抓取、离线分析、抓取并分析）
- 流程控制：爬虫路径或分析路径互斥优先

### 2. API 层 (api/scraper.py)

- 整合各模块
- 提供统一的爬虫接口
- 协调数据流

### 3. 核心层 (core/)

| 模块 | 职责 |
|------|------|
| browser.py | 浏览器连接管理 |
| detector.py | 风控检测（登录页、验证码等）|
| parser.py | 页面元素解析，提取职位信息 |

### 4. 工具层 (utils/)

| 模块 | 职责 |
|------|------|
| salary.py | 薪资解密（字体映射） |
| delay.py | 随机延迟（模拟人类行为） |

### 5. 数据层 (data/)

| 模块 | 职责 |
|------|------|
| storage.py | 多格式数据存储 |
| cache.py | 缓存数据管理 |
| models.py | 数据模型定义 |

### 6. 配置层 (config.py)

- 城市代码映射
- 默认配置
- 支持的输出格式

### 7. 分析层 (analytics/)

| 模块 | 职责 |
|------|------|
| load.py | 从 CSV / JSON / 内存列表加载为 DataFrame |
| features.py | 派生 salary_avg、经验桶、学历序数、描述内公司规模启发式等 |
| salary.py | 薪资分布与按经验/学历聚合 |
| skills.py | 职位描述/标签关键词词频 |
| company.py | 规模与薪资散点数据准备 |
| chart.py | Matplotlib 出图（英文轴标签 + mathtext；可选 `BOSS_SCRAPER_PLOT_USETEX`） |
| report.py | `run_analysis()` 串联并生成 `report.md` |

分析层仅依赖 `pandas`、`matplotlib` 与 `utils/salary.py`，不依赖 `api`/`core`，避免循环依赖。

## 数据流

```
用户输入
    ↓
检查缓存 ←→ 爬虫执行
    ↓              ↓
保存缓存     数据解析
    ↓              ↓
数据存储 ←← 返回数据
    ↓
输出文件
```

离线分析数据流（与爬虫解耦）：

```
导出 CSV/JSON 或内存 jobs 列表
    ↓
analytics/load → features → salary | skills | company
    ↓
chart → report.md + PNG（默认 output/reports/<basename>/）
```

## 模块依赖关系

```
main.py
  ├── BossScraper (api/scraper.py)
  │     ├── BrowserManager (core/browser.py)
  │     ├── RiskDetector (core/detector.py)
  │     ├── JobParser (core/parser.py)
  │     ├── DataStorage (data/storage.py)
  │     ├── DataCache (data/cache.py)
  │     └── config 模块 (get_city_code 等)
  └── run_analysis (analytics/report.py)
        ├── load / features / salary / skills / company / chart
        └── utils/salary.py（parse_salary，与 parser 共用解密逻辑）

utils/salary.py  (被 parser.py、analytics/features 引用)
utils/delay.py   (被 scraper.py 引用)
```

## 扩展设计

### 数据分析模块（已实现基线）

```
src/analytics/
├── load.py      # 数据加载
├── features.py  # 特征派生
├── salary.py    # 薪资分析
├── skills.py    # 技能分析
├── company.py   # 公司规模（描述启发式）
├── chart.py     # 可视化图表
└── report.py    # 报告生成（对外入口 run_analysis）
```

### 分析数据流

```
原始数据 → 数据清洗 → 特征提取 → 分析计算 → 可视化 → 报告
```

后续可增强：jieba 分词、Web 展示、多批次趋势（见 PRD 第三期）。

## 配置管理

通过 Config 类统一管理配置：

```python
config = Config(
    keyword="AI产品",
    pages=3,
    city="杭州",
    output_format=["xlsx", "csv"],
    chrome_port=9222,
    # ...
)
```

## 错误处理

- 风控检测：自动检测并停止
- 网络异常：重试机制
- 数据异常：跳过并记录
- 缓存管理：自动检查和加载

## 安全考虑

- 随机延迟降低风控风险
- 验证码检测
- 登录态检测
- 数据备份到本地缓存
