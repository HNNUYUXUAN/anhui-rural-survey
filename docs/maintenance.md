# 仓库维护指南

## 修改与验证

1. 检查 `git status --short --branch` 和远端更新，保留工作区已有修改。
2. 修改对应文档、脚本或研究材料，核对引用及本地链接。
3. 若改动 Notebook 构建器或研究数据，完整执行 Notebook 并检查数值、图表与输出。
4. 更新机器目录与导览：`python scripts/build_discovery.py`。
5. 使用明确路径暂存本次文件，并审阅 `git diff --cached` 与 `git status --short`。
6. 刷新清单：`python scripts/update_release_manifest.py`。脚本按 Git 已跟踪文件建立清单，新增材料需要先暂存。
7. 运行 `python scripts/verify_release.py`、`python scripts/build_discovery.py --check` 与 `git diff --check`。
8. 暂存 `MANIFEST.csv`、`SHA256SUMS.txt`，再次检查差异后提交并推送；核对远端提交和 GitHub Actions 结果。

每次修改后重新生成受影响的索引与清单。日志、浏览器截图和虚拟环境保存在仓库外，避免进入研究材料包。

## 在线文库与图表

`report/report.md` 和 `notebooks/analysis.ipynb` 是在线报告与计算阅读页的来源。`web/` 保存共用样式、交互脚本与公式渲染资源，`scripts/build_site.py` 构建 HTML。工作流通过文件核验、索引核验、独立 Notebook 执行、图表语义测试和站点链接检查后，从 `main` 部署到 GitHub Pages。

正式 Notebook 用宋体与 Times New Roman 执行，保存矢量输出。CI 用可安装的衬线字体在临时文件中复核数值，站点始终从已经审阅的正式 Notebook 构建。新增图表需检查独立点、误差棒、线型和图题位置；运行 `python scripts/test_plot_style.py` 可检查通用样式的关键行为。

仓库路径使用短英文名称。迁移关系见 [path-map.json](path-map.json)。插图只裁切外边距，裁切框与前后哈希见 [figure-crops.json](figure-crops.json)。更新插图后，检查每个坐标标签与图中文字是否完整。

站点构建与核验命令见[使用指南](usage.md)；运行资源及许可见[第三方资源说明](third-party.md)。

## 审阅重点

首页和目录围绕读者任务组织，配图使用实际研究材料，图题置于图下。科学数字以结果文件为依据，图文在 GitHub 实际页面检查；公式保留标准 LaTeX。新增统计图时检查字体、单位、图例和文字遮挡。

公开研究数据的文件集合由 `scripts/verify_release.py` 中的明确列表约束。扩充数据范围时，需同时审阅数据粒度、字段、权利与引用信息，再更新该列表。个人记录和第三方全文的处理遵循 [DATA.md](../DATA.md) 与 [LICENSE](../LICENSE)。

## 版本

[CITATION.cff](../CITATION.cff)记录研究材料版本。导航、说明与维护工具的变化写入 [CHANGELOG.md](../CHANGELOG.md)，通过提交号定位。正式发布新的研究版本时，再统一更新引用信息、版本号与发布说明。
