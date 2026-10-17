# Agent 检索与接手指南

## 入口与阅读顺序

1. [llms.txt](../llms.txt)：项目主题、核心入口和证据定位。
2. [resource-catalog.json](resource-catalog.json)：逐资源的路径、类型、关键词、CSV 字段和记录数。
3. [数据说明](../DATA.md)：样本、有效分母、粒度和可复现范围。
4. [研究报告](../01_调研报告/README.md)：研究问题、方法、结果及局限。
5. [使用指南](usage.md)：安装、执行和单个结果的核对示例。

[llm.txt](../llm.txt)提供兼容入口，[llms-full.txt](../llms-full.txt)提供展开的材料导览。它们由脚本生成；这些文件为机器阅读提供导航，检索收录取决于使用方。

## 检索与回答

```bash
python scripts/build_discovery.py --query 撂荒
python scripts/build_discovery.py --query household
```

机器目录的 `path` 相对仓库根目录，`url` 指向 GitHub 文件；`columns` 和 `record_count` 描述 CSV 结构。`record_count` 是结果表行数，受访者样本量应读取具体字段或报告。中文与英文关键词用于主题检索。

回答研究问题时，先定位报告章节，再核对结果表、制图数据与 Notebook。每个数字连同年份、样本范围、题项分母、单位和必要的方法条件一起引用。Logit 的优势比按条件关联解释；2026 年户村指标按并列证据解释。

数据为空、分母不明或材料之间存在冲突时，记录具体文件和字段，并保留待核状态。引用参考文献时以正文编号和来源登记定位，区分题录与实际核读的全文。

## 接手维护

先运行 `git status --short --branch`，再执行发布核验和索引同步检查。按 [AGENTS.md](../AGENTS.md) 维护文案、数据与计算，按[维护指南](maintenance.md)完成清单刷新、检查与推送。

交付记录应包含变更内容、验证命令及结果、提交号和直接 review 链接。材料的研究版本与仓库维护提交分别记录，版本信息以 [CITATION.cff](../CITATION.cff) 为准。
