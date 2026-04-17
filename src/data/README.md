# `src/data/` 数据层

## 职责

承载**领域模型**、**缓存读写**与**多格式导出**，对应架构文档数据层，支撑 PRD 中的「数据导出」「数据缓存」及第 4 节数据需求。

## 模块

| 文件 | 职责 |
|------|------|
| `models.py` | 职位等数据结构定义（与导出列、下游分析字段对齐） |
| `cache.py` | `DataCache`：缓存命中、读写，减少重复抓取 |
| `storage.py` | `DataStorage`：按 xlsx / csv / md / json 等写入输出目录 |

## 与仓库目录的关系

- 包内逻辑操作的路径通常来自配置中的 `data_dir`（缓存）与 `output_dir`（导出）。  
- 仓库下顶层 [`data/`](../../data/README.md)、[`output/`](../../output/README.md) 目录说明见各自 README。

## 相关文档

- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — 数据流、数据层表格  
- [docs/PRD.md](../../docs/PRD.md) — 场景二（缓存）、输出与字段说明  
