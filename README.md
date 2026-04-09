# Boss 直聘爬虫（boss-scraper）

面向求职场景的职位信息采集工具，采用分层模块化设计。产品目标、功能范围与非功能要求见 [docs/PRD.md](docs/PRD.md)；分层职责、数据流与依赖关系见 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)。

## 快速开始

```bash
cd boss-scraper
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

先以远程调试端口启动 Chrome（默认 `9222`），再执行：

```bash
python main.py -i
# 或
python main.py -k "关键词" -p 3 -c 杭州
# 离线分析已导出数据（无需 Chrome）
python main.py --analyze output/关键词_城市_时间戳.csv
```

完整参数、输出字段与风控说明见 [docs/README.md](docs/README.md)；分析模块见 [src/analytics/README.md](src/analytics/README.md)。

## 目录说明

| 目录 | 说明 |
|------|------|
| [docs/](docs/README.md) | PRD、架构设计与使用文档 |
| [src/](src/README.md) | 源代码包（api / core / data / utils / analytics） |
| [data/](data/README.md) | 运行期缓存与中间数据（勿提交敏感内容） |
| [output/](output/README.md) | 导出结果（xlsx / csv / md / json） |
| `main.py` | CLI 与交互式向导入口 |

## 架构概要（摘自架构文档）

```
main.py → api/scraper.py (BossScraper) → core/ + data/ + utils/
         ↑
    config.py（城市码、格式、延迟等）
```

各子包职责见对应目录下的 `README.md`。

## 许可与风险

仅供个人学习交流；请控制抓取频率并遵守平台规则。详见 PRD「风险与限制」与 docs 中的风控提示。
