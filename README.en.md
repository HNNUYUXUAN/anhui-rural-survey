[简体中文](README.md) · **English**

# Cultivating the Land, Sustaining Livelihoods

### A study of sustained grain cultivation among farming households in Anhui

Once land contracts are stable, what else do farming households need to keep cultivating their land? This project examines household labor, land and contractual arrangements, agricultural services, and income and risk to understand farming conditions in Anhui and the practical questions that county-level governance can address.

**Huainan Normal University · Qingsui Jianghuai Research Team (青穗江淮调研团)**

[Project homepage · Research library](https://hnnuyuxuan.github.io/anhui-rural-survey/) · [Read the report](https://hnnuyuxuan.github.io/anhui-rural-survey/report/) · [Read the Notebook](https://hnnuyuxuan.github.io/anhui-rural-survey/notebook/) · [Find data and figures](data/README.md) · [Cite this project](CITATION.md)

The report provides chapter navigation, equations, and figures. The Notebook retains complete computation outputs and supports expanding code and downloading the source for reproduction. [Report source](report/report.md) · [Notebook source](notebooks/analysis.ipynb) · [Survey instruments](surveys/README.md)

The linked report, Notebook commentary, research figures, and supporting guides are primarily in Chinese. This English README provides navigation and explains the study's scope and evidence.

![Stable land contracts connect to sustained grain cultivation through operating expectations, contractual and land arrangements, agricultural services, income, and risk](figures/diagrams/fig1-1_grain_continuity_mechanism.png)

*Research framework: from stable land contracts to sustained farm operation. Arrows represent the proposed research mechanisms; see the report for the statistical evidence.*

## Three sources of evidence, one research question

| Year | Respondents | Sample | Research focus | Data entry point |
|:---:|:---|---:|:---|:---:|
| 2025 | Farming households | 2,079 households | Associations between operating conditions and land left uncultivated | [Main empirical evidence](data/README.md) |
| 2026 | Farming households | 570 households | Policy, contracts, and entrusted agricultural services | [Household indicators](data/results/households-2026.csv) |
| 2026 | Villages | 38 villages | Contracts, services, and infrastructure | [Village indicators](data/results/villages-2026.csv) |

The 2025 data provide the main empirical evidence. The 2026 household and village data provide parallel observations. Each survey item uses its own valid denominator. See the [report](report/report.md) and [data notes](DATA.md) for sampling design, model assumptions, and research limitations. Household and village evidence should not be interpreted as individually matched observations.

## Start with the results

Among valid responses in 2025, **8.23%** reported land left uncultivated. The main Logit model uses **2,055 households** with complete records. After controlling for household and operating conditions, disaster exposure is associated with an odds ratio of **1.940** for land being left uncultivated, with a 95% bootstrap interval of **1.381–2.656**. These estimates describe conditional associations. See the [model results table](data/results/fallow-model-2025.csv) for variables, denominators, and estimation methods.

![Odds ratios and confidence intervals for the 2025 model of land left uncultivated](figures/stats/fig4-3_logit_or.png)

*Figure 4-3. Odds ratios from the 2025 model. The accompanying [plotting data](data/charts/fig4-3_logit_or.csv) and [sensitivity checks](data/results/sensitivity-2025.csv) support further verification.*

The study then examines contractual standards, services at critical points in the farming calendar, and recovery after disasters: how can stable land rights translate into stable household farming operations? The [full report](report/report.md) develops the background, methods, main empirical analysis, household profiles, 2026 evidence, and county-level governance implications chapter by chapter.

## Choose your entry point

| Your purpose | Start here | What you will find |
|:---|:---|:---|
| Understand the questions and conclusions | [Report guide](report/README.md) | Eight chapters, the research framework, and conclusions |
| Check numbers and proportions | [Reproduction guide](docs/usage.md) | The Notebook, 24 data files, and verification methods |
| Find data and figures | [Figure index](figures/README.md) | 11 statistical figure groups, 5 conceptual diagrams, and plotting data |
| Design a similar survey | [Survey instruments](surveys/README.md) | Household and village-cadre questionnaires in DOCX and TXT |
| Trace sources and cite the work | [References](references/README.md) · [Citation](CITATION.md) | Source records, citation formats, and author information |
| Retrieve materials or continue work with an agent | [Agent guide](docs/agent-guide.md) · [llms.txt](llms.txt) | Machine-readable navigation, evidence locations, and maintenance procedures |

## Get started locally

```bash
git clone https://github.com/HNNUYUXUAN/anhui-rural-survey.git
cd anhui-rural-survey
python scripts/verify_release.py
python scripts/build_discovery.py --check
```

These checks require only the standard library in Python 3.11 or a compatible version. To execute the Notebook again:

```bash
conda env create -f environment.yml
conda run -n anhuirural-survey python scripts/build_analysis_notebook.py --execute
```

The Notebook reads aggregate statistics, model outputs, and plotting data to verify proportions, redraw the main results, and check consistency across files. See [DATA.md](DATA.md) for the data conditions required to re-estimate individual-level models. The [usage guide](docs/usage.md) covers pip installation, working directories, and outputs. The public package does not include respondent-level records or all inputs needed to reconstruct every model independently.

## Repository collaboration

[He Yiting (Monica)](https://gitee.com/monica-423) is a collaborator on the Gitee repository and studies Rail Transit Signaling and Control at Huainan Normal University. Future repository collaboration will focus on research-material navigation, the readability of figure explanations, and user feedback, helping readers connect questions, data, and conclusions. For authorship of the fieldwork and research results, see the team and citation information below.

## Team, citation, and contributions

This project was completed by the Qingsui Jianghuai Research Team at Huainan Normal University. [Project background](ABOUT.md) describes the research topic and activity context; [author information](AUTHORS.md) lists team members and faculty advisers.

The research-material release is **v1.0.0 (2026-09-14)**. Cite the work using [CITATION.md](CITATION.md) or [CITATION.cff](CITATION.cff), and record the commit and file checksums used. Repository maintenance is documented in [CHANGELOG.md](CHANGELOG.md).

Software scripts are licensed under **AGPL-3.0-only**. Original research content and public data are licensed under **CC BY-SA 4.0**; see [LICENSE](LICENSE) for the applicable scope. Questions and corrections are welcome through [Issues](https://github.com/HNNUYUXUAN/anhui-rural-survey/issues). Read the [contribution guide](CONTRIBUTING.md) before submitting changes.
