# `src/core/` 核心层

## 职责

贴近浏览器与 DOM 的实现，对应架构文档中的 **核心层**：连接管理、风控判断、职位卡片解析。与 PRD 中「风控检测（登录页、验证码等）」及原始/处理后字段的提取直接相关。

## 模块

| 文件 | 职责（见 ARCHITECTURE） |
|------|-------------------------|
| `browser.py` | `BrowserManager`：连接已启动的 Chrome（远程调试端口） |
| `detector.py` | `RiskDetector`：识别登录页、验证码等风险并返回是否中断 |
| `parser.py` | `JobParser`：从列表页元素解析岗位名称、薪资、公司、链接等 |

## 依赖说明

- `parser` 可能使用 `utils/salary` 等工具处理 Boss 薪资展示（加密字体等），详见代码引用。  
- 本层不应依赖 `api`，由 `BossScraper` 调用本层组件。

## 相关文档

- [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md) — 核心层表格、数据流  
- [docs/PRD.md](../../docs/PRD.md) — 第 4 节数据字段、第 6.3 节安全与风控  
