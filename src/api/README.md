# `src/api/` API 层

## 职责

在 [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) 中，本层负责**整合各模块**、提供统一爬虫接口，并协调浏览器连接、风控检测、解析、缓存与落盘之间的数据流（参见文档「数据流」图示）。

## 模块

- **`scraper.py`**：`BossScraper` 类  
  - 组装 `BrowserManager`、`RiskDetector`、`JobParser`、`DataStorage`、`DataCache`  
  - 实现按关键词、城市、页数拉列表与详情、随机延迟与滚动等行为  
  - 与 PRD 中「职位搜索」「风控检测」「数据缓存」等 P0/P1 能力对应  

## 使用方式

通常由项目根目录的 `main.py` 构造配置字典并实例化 `BossScraper`，无需在业务代码中重复编排上述组件。

## 相关文档

- 需求范围：[docs/PRD.md](../../docs/PRD.md) 第 2 节  
- 分层与依赖：[docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) 第 2～3 节、模块依赖图  
