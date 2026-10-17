# 公开数据分析与结果复核

[打开已执行 Notebook](安徽农户持续种粮调研_公开数据分析与结果复核.ipynb) · [安装与运行指南](../docs/usage.md)

Notebook 围绕“读取数据 → 核对比例与模型输出 → 重绘图表 → 检查一致性”展开，包含完整说明、代码和已保存的输出。输入来自[研究数据](../02_公开数据/README.md)中的 24 个 CSV/JSON。

## 运行

在仓库根目录执行：

```bash
conda env create -f environment.yml
conda run -n anhuirural-survey python scripts/build_analysis_notebook.py --execute
```

构建命令会覆盖本目录的 Notebook 并保存新输出。使用当前环境的临时内核；pip 安装方式、字体建议与输出检查见[使用指南](../docs/usage.md)。

## 阅读与计算

| 工作 | 输入与输出 |
|---|---|
| 数据清单 | 文件、字段、记录数及数据粒度 |
| 2025 年结果 | 土地状态、模型输出、画像与敏感性比较 |
| 2026 年结果 | 农户、村级指标及题项有效分母 |
| 可视化与一致性 | 主要图表重绘、跨文件数值核对 |

个体层模型重估需要原始分析输入。公开聚合结果支持的复核范围及研究解释见 [DATA.md](../DATA.md)。

[研究报告](../01_调研报告/README.md) · [图表索引](../03_图表/README.md) · [返回首页](../README.md)
