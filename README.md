# 安徽农户持续种粮调研项目

本仓库汇集《把地种好，把日子过稳——稳定承包背景下安徽农户持续种粮的约束结构》的公开版报告、聚合分析结果、制图数据、统计图、逻辑图、参考文献记录、调查工具和可执行分析 Notebook。

报告以 2025 年 2079 份农户问卷为主实证，以 2026 年 570 份农户问卷和 38 份村级问卷作为并列证据，分析稳定承包背景下家庭禀赋、合同、社会化服务、收益风险与持续种粮之间的约束结构。各结论的样本、有效分母、模型和局限以报告正文为准。

项目缘起、活动相关页面、材料来源和公开边界见 [ABOUT.md](ABOUT.md)。

## 仓库结构

- `01_调研报告/`：移除可识别个人实拍图片的 Markdown 公开版报告。
- `02_公开数据/聚合分析结果/`：模型结果、分组统计、画像汇总和 2026 年汇总指标。
- `02_公开数据/图表数据/`：统计图对应的制图数据。
- `03_图表/`：统计图 PNG/SVG 与逻辑图 PNG。
- `04_参考文献/`：正文引用清单和不含本地全文路径的来源登记。
- `05_调查工具/`：农户端和村干部端问卷的 DOCX/TXT 版本。
- `notebooks/`：已经完整执行并保存输出的公开数据分析与结果复核 Notebook。
- `ABOUT.md`：项目背景、活动相关页面、材料关系与证据边界。
- `AUTHORS.md`、`CITATION.cff`：作者、团队、机构与机器可读引用信息。
- `LICENSE`、`LICENSES/`：软件与研究内容的强互惠双许可证。
- `MANIFEST.csv`、`SHA256SUMS.txt`：公开包文件集合、大小和 SHA-256。

## 数据说明

公开包只提供聚合统计、模型输出和图表数据，不提供逐行答卷或可回溯到单个答卷的派生记录。详细边界见 [DATA.md](DATA.md)。

## 核验

使用 Python 3.11 或兼容版本执行：

```powershell
python .\scripts\verify_release.py
```

核验脚本检查清单覆盖、文件大小、SHA-256、目录边界、Markdown 本地链接和问卷 DOCX 核心元数据。

## 运行 Notebook

创建环境后，可从仓库根目录重新执行完整版 Notebook：

```powershell
conda env create -f environment.yml
conda run -n anhuirural-survey python scripts/build_analysis_notebook.py --execute
```

也可使用最小化的 pip 环境：

```powershell
python -m pip install -r requirements-notebook.txt
python scripts/build_analysis_notebook.py --execute
```

构建器使用当前 Python 创建临时内核，不依赖机器上既有的 Jupyter kernelspec。Notebook 读取全部 24 个公开研究数据文件，复核主要统计口径、重绘核心结果并执行数据一致性检查。公开仓库不含微观数据，因此 Notebook 不重新估计个体层模型或重新执行聚类分配。

## 作者与项目链接

项目由淮南师范学院青穗江淮调研团完成，作者和指导教师信息见 [AUTHORS.md](AUTHORS.md)。活动相关页面为[《百校江淮大调研｜第三届安徽省“百校千镇万村”大学生乡村振兴大调研立项名单揭晓!》](https://mp.weixin.qq.com/s/X2sH0Tu2Dmlcer4riqexJA)。该链接用于记录活动背景，不替代团队申报材料，也不作为报告统计结论的证据。

## 许可证

- `scripts/`：GNU Affero General Public License v3.0 only（AGPL-3.0-only）。
- 原创报告、说明文档、问卷、图表、聚合结果与图表数据：Creative Commons Attribution-ShareAlike 4.0 International（CC BY-SA 4.0）。

两者均要求衍生成果继续按相同或兼容的开放许可证共享；AGPL 还覆盖修改后软件通过网络向用户提供服务的情形。具体范围、例外和完整条款见 [LICENSE](LICENSE)。

## 引用

建议引用格式见 [CITATION.md](CITATION.md)，机器可读信息见 [CITATION.cff](CITATION.cff)。当前公开版本为 **v1.0.0（2026-09-14）**；如后续取得 DOI，将同步更新引用信息。
