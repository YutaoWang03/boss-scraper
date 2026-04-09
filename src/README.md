# `src/` 源代码包

本目录为 Python 包根，实现 [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) 中的分层结构：`main.py` 通过 `api` 层调度 `core`、`data`、`utils`，配置集中在 `config.py`。

## 子目录

| 目录 | 角色（架构文档中的层） |
|------|------------------------|
| [api/](api/README.md) | API 层：对外爬虫入口，编排流程 |
| [core/](core/README.md) | 核心层：浏览器、风控检测、页面解析 |
| [data/](data/README.md) | 数据层：模型、缓存、多格式存储 |
| [utils/](utils/README.md) | 工具层：薪资处理、随机延迟等 |
| [analytics/](analytics/README.md) | 数据分析（规划中，见 PRD 第二期） |

## 根文件

- **`config.py`**：城市代码、支持格式、延迟与 Chrome 端口等默认配置（架构文档中的「配置层」）。

## 依赖方向（约定）

上层可依赖下层，避免 `core` 直接依赖 `api`。具体依赖图见 [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)「模块依赖关系」。
