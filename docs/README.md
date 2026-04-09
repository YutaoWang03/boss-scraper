# Boss 直聘爬虫 — 文档与使用说明

## 设计文档索引

| 文档 | 内容 |
|------|------|
| [PRD.md](./PRD.md) | 产品定位、功能优先级、用户故事、数据字段、非功能需求与规划 |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 分层架构、各层职责、数据流、模块依赖、扩展设计（含 analytics） |

项目根目录另有 [README.md](../README.md) 作为入口；各源码与数据目录下的 `README.md` 与上述架构、PRD 交叉引用。

---

一个模块化的 Boss 直聘职位信息爬虫，支持数据爬取和数据分析。

## 功能特点

- 🔍 多城市职位搜索
- 📊 多格式数据导出（Excel、CSV、Markdown、JSON）
- 🛡️ 内置风控检测
- 💾 数据缓存管理
- 🎯 支持交互式和命令行模式
- 📈 可扩展的数据分析功能（规划中）

## 环境要求

- Python 3.8+
- Chrome 浏览器

## 安装

```bash
# 克隆项目
cd boss-scraper

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

## 使用前提

需要先启动 Chrome 浏览器（带调试端口）：

```bash
# Mac
open -a "Google Chrome" --args --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

## 使用方法

### 交互式模式

```bash
python main.py -i
```

### 命令行模式

```bash
# 基本用法
python main.py -k "AI产品经理" -p 3

# 指定城市
python main.py -k "AI产品" -p 3 -c 北京

# 指定输出格式（可多选）
python main.py -k "AI产品" -p 3 --format xlsx,csv,md

# 强制重新抓取（忽略缓存）
python main.py -k "AI产品" -p 3 --force

# 离线分析已导出的 CSV/JSON（无需 Chrome）
python main.py --analyze output/关键词_城市_20260101_120000.csv
python main.py --analyze output/data.json --report-dir ./output/reports
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| -k, --keyword | 搜索关键词 | 必填 |
| -p, --pages | 爬取页数 | 1 |
| -c, --city | 城市 | 杭州 |
| --format | 输出格式(xlsx,csv,md,json) | xlsx |
| -o, --output | 输出目录 | ./output |
| --force | 强制重新抓取 | False |
| -i, --interactive | 交互式模式 | False |
| --analyze | 仅分析指定 CSV/JSON 路径 | - |
| --report-dir | 分析报告根目录 | output/reports |

## 数据输出

### 输出字段

| 字段 | 说明 |
|------|------|
| 岗位名称 | 职位名称 |
| 薪资范围 | 薪资范围文本 |
| 工作城市 | 城市 |
| 具体地址 | 详细地址 |
| 公司名称 | 公司名 |
| 经验学历 | 经验/学历要求 |
| 职位链接 | BOSS直聘链接 |
| 职位描述 | 详细职位描述 |

### 输出格式

- **xlsx**: Excel 格式
- **csv**: CSV 格式
- **md**: Markdown 格式
- **json**: JSON 格式

## 风控提示

⚠️ 使用本爬虫时请注意：

- 请使用**独立账号**爬取，避免主账号被封
- 建议每天爬取不超过 **200-300 条**
- 适当休息，避免 24 小时连续爬取
- 间歇性爬取更安全（爬 1 小时休息 30 分钟）

## 项目结构

```
boss-scraper/
├── src/
│   ├── core/          # 核心层
│   │   ├── browser.py
│   │   ├── detector.py
│   │   └── parser.py
│   ├── utils/         # 工具层
│   │   ├── salary.py
│   │   └── delay.py
│   ├── data/          # 数据层
│   │   ├── storage.py
│   │   ├── cache.py
│   │   └── models.py
│   ├── api/           # 调用层
│   │   └── scraper.py
│   ├── analytics/     # 数据分析与报告
│   │   ├── load.py, features.py, report.py, …
│   └── config.py
├── data/               # 数据缓存
├── output/             # 输出目录
├── main.py
└── requirements.txt
```

## 数据分析

已实现离线分析（`--analyze` 或交互式「数据分析 / 抓取并分析」），生成 `output/reports/<basename>/report.md` 与图表。详见 [PRD.md](./PRD.md) 第 2.2、第 5 节与 [src/analytics/README.md](../src/analytics/README.md)。

## 许可证

仅供学习交流使用，请勿用于商业目的。
