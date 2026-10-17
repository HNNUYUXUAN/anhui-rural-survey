# 阅读、核对与复现

## 阅读路线

先读[研究报告摘要与目录](../report/report.md)，再按研究问题进入第四章的家庭经营分析、第五章的农户画像，或第六章的政策、合同和服务证据。[图表索引](../figures/README.md)把统计图与 CSV 配成对，便于边读边核对。

## 核对一个结果

以“受灾与撂荒的关联”为例：

1. 阅读报告第四章，确认样本、变量定义与条件关联的解释。
2. 打开[2025 年撂荒模型结果](../data/results/fallow-model-2025.csv)，找到“受灾（是/否）”行，核对优势比、区间、样本量和 bootstrap 次数。
3. 对照[图 4-3 制图数据](../data/charts/fig4-3_logit_or.csv)和[统计图](../figures/stats/fig4-3_logit_or.png)。
4. 阅读[敏感性检验](../data/results/sensitivity-2025.csv)，比较不同质量规则与面积定义下的结果。
5. 引用时记录报告章节、文件路径、研究版本、Git 提交与文件 SHA-256。

2026 年比例需要同时核对题项的有效分母。[数据说明](../DATA.md)列出三套资料的证据定位；CSV 的行数表示指标、模型项或情景数量。

## 环境与执行

推荐 Python 3.11。以下命令在仓库根目录执行：

```bash
python scripts/verify_release.py
python scripts/build_discovery.py --check
```

前一条检查文件集合、大小、哈希、材料范围和本地链接，后一条检查机器目录及 LLM 导览与当前材料是否同步。二者只依赖标准库。

完整计算环境可使用 Conda：

```bash
conda env create -f environment.yml
conda run -n anhuirural-survey python scripts/build_analysis_notebook.py --execute
```

也可用 pip。将虚拟环境放在仓库同级，避免把本地环境纳入材料清单。

Windows PowerShell：

```powershell
python -m venv ../anhui-survey-venv
& ../anhui-survey-venv/Scripts/python.exe -m pip install -r requirements-notebook.txt
& ../anhui-survey-venv/Scripts/python.exe scripts/build_analysis_notebook.py --execute
```

Linux / macOS：

```bash
python3 -m venv ../anhui-survey-venv
../anhui-survey-venv/bin/python -m pip install -r requirements-notebook.txt
../anhui-survey-venv/bin/python scripts/build_analysis_notebook.py --execute
```

正式绘图要求系统已安装 **SimSun（宋体）**和 **Times New Roman**；构建器会检查这两个字体，缺少时明确报错。西文与数字优先使用 Times New Roman，中文使用宋体；数学字体、灰度、线型、纹理及图下题注由 `scripts/plot_style.py` 统一配置。发布的 SVG 使用字形轮廓，在线图表不依赖访问者安装字体。字体文件由系统提供。

在 Linux CI 中，可使用 Noto Serif CJK 与 Liberation Serif 做独立数值复核，结果保存在临时文件中：

```bash
python scripts/build_analysis_notebook.py --check-execution --font-mode portable
```

正式阅读页使用仓库内以宋体和 Times New Roman 生成的已执行输出。

## 输出与核验

构建器会重新生成并覆盖 `notebooks/analysis.ipynb`，在当前 Python 环境启动临时内核，保存执行结果。重跑前可用 `git status` 检查已有修改。

Notebook 读取 24 个研究 CSV/JSON，核对主要比例与跨文件一致性并重绘核心图表。个体层模型的重新估计需要原始分析输入；现有聚合结果支持的工作范围见 [DATA.md](../DATA.md)。

执行后可检查所有代码单元已完成、无错误输出，再查看 `git diff --stat`。环境版本和图像渲染变化可能改变 Notebook 字节，因此重跑后的哈希变化需要人工审阅；提交新输出时按[维护指南](maintenance.md)更新清单。

## 查找材料

```bash
python scripts/build_discovery.py --query 合同
python scripts/build_discovery.py --query logit
```

命令按标题、路径与关键词返回资源。完整目录见 [resource-catalog.json](resource-catalog.json)，Agent 阅读顺序见 [agent-guide.md](agent-guide.md)。

## 在线阅读与站点构建

[研究文库](https://hnnuyuxuan.github.io/anhui-rural-survey/)提供[报告](https://hnnuyuxuan.github.io/anhui-rural-survey/report/)和[Notebook](https://hnnuyuxuan.github.io/anhui-rural-survey/notebook/)的直接阅读入口。浏览器中可按目录跳转、展开计算代码、浏览输出并下载数据。正文优先使用系统宋体与 Times New Roman，其余设备按宋体类衬线字体回退。

```bash
python -m pip install -r requirements-site.txt
python scripts/build_site.py --output ../site-preview
python scripts/verify_site.py ../site-preview
python -m http.server 8000 --directory ../site-preview
```

报告与 Notebook 的源文件是维护入口；HTML 由工作流构建。公式渲染资源随站点托管。路径迁移对应关系见 [path-map.json](path-map.json)，部署说明见 [maintenance.md](maintenance.md)。
