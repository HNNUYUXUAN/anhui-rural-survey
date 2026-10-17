"""Build deterministic research navigation; no third-party dependencies."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "https://github.com/HNNUYUXUAN/anhui-rural-survey"
GROUPS = {
    "report": "研究报告",
    "data": "研究数据",
    "figures": "图表",
    "references": "参考文献",
    "surveys": "调查工具",
    "notebooks": "分析 Notebook",
}
TOPICS = (
    (("撂荒", "fallow", "logit", "敏感性"), ["撂荒", "fallow", "logit", "敏感性", "sensitivity"]),
    (("画像", "profile", "聚类"), ["农户画像", "profile", "cluster"]),
    (("合同", "contract", "constraints"), ["合同", "contract", "托管", "service"]),
    (("政策", "policy", "future"), ["政策认知", "policy", "未来安排", "future"]),
    (("村", "village", "governance"), ["村级", "village", "治理", "governance"]),
    (("农户", "household"), ["农户", "household"]),
    (("土地", "land"), ["土地", "land", "承包", "tenure"]),
    (("收入", "income"), ["收入", "income"]),
    (("受灾", "disaster", "risk", "recovery"), ["灾害", "disaster", "风险", "risk"]),
    (("问卷",), ["问卷", "questionnaire", "survey"]),
)


def resources() -> list[dict]:
    result = []
    migration = json.loads((ROOT / "docs/path-map.json").read_text(encoding="utf-8"))
    titles = {new: Path(old).stem for old, new in migration.items()}
    for directory, kind in GROUPS.items():
        for path in sorted((ROOT / directory).rglob("*")):
            if not path.is_file() or path.name == "README.md":
                continue
            relative = path.relative_to(ROOT).as_posix()
            keywords = sorted({word for triggers, words in TOPICS
                               if any(t in relative.casefold() for t in triggers)
                               for word in words})
            item = {"title": titles.get(relative, path.stem), "kind": kind, "path": relative,
                    "url": REPOSITORY + "/blob/main/" + quote(relative),
                    "format": path.suffix.lstrip("."), "keywords": keywords}
            if path.suffix == ".csv":
                with path.open(encoding="utf-8-sig", newline="") as stream:
                    rows = list(csv.reader(stream))
                item["columns"] = rows[0] if rows else []
                item["record_count"] = max(0, len(rows) - 1)
                # Indicator names carry topics that generic filenames omit.
                labels = " ".join(row[0] for row in rows[1:] if row).casefold()
                item["keywords"] = sorted(set(keywords) | {
                    word for triggers, words in TOPICS
                    if any(t in labels for t in triggers) for word in words
                })
            result.append(item)
    return result


def outputs() -> dict[str, str]:
    items = resources()
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    version = re.search(r'^version: "([^"]+)"', citation, re.M).group(1)
    date = re.search(r'^date-released: "([^"]+)"', citation, re.M).group(1)
    catalog = {"schema_version": 1, "title": "安徽农户持续种粮调研项目",
               "repository": REPOSITORY, "research_version": version,
               "date_released": date,
               "record_count_definition": "CSV 数据行数；样本量与有效分母见具体字段及报告。",
               "resources": items}
    intro = (
        "# 安徽农户持续种粮调研项目\n\n"
        "> 把地种好，把日子过稳：稳定承包背景下安徽农户持续种粮的约束结构。\n\n"
        "淮南师范学院青穗江淮调研团。2025 年 2079 户为主实证，2026 年 570 户与 38 村为并列证据。\n"
        f"研究材料版本：v{version}（{date}）。\n\n"
        "## 阅读入口\n\n"
    )
    links = [("项目首页", "README.md"), ("研究报告", "report/README.md"),
             ("研究数据", "data/README.md"), ("图表与制图数据", "figures/README.md"),
             ("参考文献", "references/README.md"), ("调查工具", "surveys/README.md"),
             ("Notebook", "notebooks/README.md"), ("数据口径", "DATA.md"),
             ("复现指南", "docs/usage.md"), ("Agent 接手指南", "docs/agent-guide.md"),
             ("机器资源目录", "docs/resource-catalog.json"), ("引用", "CITATION.cff"),
             ("许可证", "LICENSE")]
    brief = intro + "".join(f"- [{label}]({REPOSITORY}/blob/main/{quote(path)})\n" for label, path in links)
    brief += "\n## 在线阅读\n\n- [完整报告](https://hnnuyuxuan.github.io/anhui-rural-survey/report/)\n- [已执行 Notebook](https://hnnuyuxuan.github.io/anhui-rural-survey/notebook/)\n"
    brief += (
        "\n## 证据与计算\n\n"
        "公开输入为聚合统计、模型输出与制图数据。Notebook 可复核比例、图表及文件间一致性；"
        "个体层模型重估需要原始分析输入。各题项采用各自有效分母，Logit 结果按条件关联解释，"
        "户级与村级资料按并列观察解释。引用数字时附报告章节、结果文件、年份、单位与分母。\n\n"
        "核验：`python scripts/verify_release.py`；索引检查：`python scripts/build_discovery.py --check`。\n"
        "检索：`python scripts/build_discovery.py --query 合同`。\n"
        "执行：`python scripts/build_analysis_notebook.py --execute`，依赖见 `requirements-notebook.txt`。\n"
    )
    full = brief + "\n## 完整材料导览\n"
    for kind in GROUPS.values():
        full += f"\n### {kind}\n\n"
        for item in items:
            if item["kind"] != kind:
                continue
            full += f'- [{item["title"]}]({item["url"]}) · {item["format"]}\n'
            if "columns" in item:
                full += f'  字段：{"、".join(item["columns"])}；数据行：{item["record_count"]}。\n'
    return {"docs/resource-catalog.json": json.dumps(catalog, ensure_ascii=False, indent=2) + "\n",
            "llms.txt": brief, "llm.txt": brief, "llms-full.txt": full}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="Check generated files without writing.")
    group.add_argument("--query", help="Search resource titles, paths, and bilingual keywords.")
    args = parser.parse_args()
    if args.query is not None:
        query = args.query.strip().casefold()
        if not query:
            parser.error("query must contain text")
        matches = [r for r in resources() if query in
                   " ".join([r["title"], r["path"], *r["keywords"]]).casefold()]
        for item in matches:
            print(f'{item["kind"]}\t{item["path"]}')
        print(f"matches={len(matches)}")
        return 0
    stale = []
    for relative, content in outputs().items():
        target = ROOT / relative
        if args.check:
            if not target.is_file() or target.read_bytes() != content.encode("utf-8"):
                stale.append(relative)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")
    if stale:
        print("discovery=FAIL\n" + "\n".join(stale))
        return 1
    print("discovery=PASS" if args.check else "discovery=UPDATED")
    print(f"resources={len(resources())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
