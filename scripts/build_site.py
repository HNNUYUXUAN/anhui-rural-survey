"""Build a self-contained academic reading site from the reviewed sources."""
from __future__ import annotations

import argparse
import base64
import html
import json
import posixpath
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://hnnuyuxuan.github.io/anhui-rural-survey/"
REPO = "https://github.com/HNNUYUXUAN/anhui-rural-survey"
MD = MarkdownIt("commonmark", {"html": True}).enable("table").use(dollarmath_plugin)
ROUTES = {"README.md": "index.html", "report/report.md": "report/index.html",
          "report/README.md": "report/guide.html", "notebooks/README.md": "notebook/index.html"}


def render_markdown(text: str) -> str:
    # GitHub's code-delimited inline math also renders in the reading pages.
    text = re.sub(r"\$`([^`\n]+)`\$", lambda match: "$" + match[1] + "$", text)
    return MD.render(text)


def route(path: str) -> str:
    if path in ROUTES:
        return ROUTES[path]
    if path.endswith("/README.md"):
        return path.removesuffix("README.md") + "index.html"
    return str(Path(path).with_suffix(".html")).replace("\\", "/")


def relative(current: str, target: str) -> str:
    return quote(posixpath.relpath(target, posixpath.dirname(current) or "."), safe="/#")


def enhance(body: str, source: str, destination: str) -> tuple[str, str]:
    soup = BeautifulSoup(body, "html.parser")
    for node in soup.select("a[href], img[src]"):
        attr = "src" if node.name == "img" else "href"
        value = node[attr]
        parsed = urlsplit(value)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        target = posixpath.normpath(posixpath.join(posixpath.dirname(source), unquote(parsed.path)))
        if target.startswith("../"):
            raise ValueError(f"Link escapes repository: {source}: {value}")
        if target.endswith(".md"):
            target = route(target)
        node[attr] = relative(destination, target) + ("#" + parsed.fragment if parsed.fragment else "")
    headings = []
    for index, heading in enumerate(soup.select("h2"), 1):
        previous = heading.find_previous_sibling()
        anchor = previous.get("id") if previous and previous.name == "a" else None
        identifier = anchor or f"section-{index}"
        heading["id"] = heading.get("id", identifier if not anchor else identifier+"-title")
        headings.append((identifier, heading.get_text(" ", strip=True)))
    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div", attrs={"class": "table-scroll", "tabindex": "0", "role": "region", "aria-label": "数据表，可横向浏览"})
        table.wrap(wrapper)
    for paragraph in list(soup.find_all("p")):
        if paragraph.find("img") is None:
            continue
        if paragraph.get_text(strip=True):
            continue
        paragraph.name = "figure"
        next_paragraph = paragraph.find_next_sibling("p")
        if next_paragraph and next_paragraph.find("em") and next_paragraph.get_text(strip=True).startswith(("图", "研究框架")):
            next_paragraph.name = "figcaption"
            paragraph.append(next_paragraph.extract())
    toc = "<ol>" + "".join(f'<li><a href="#{key}">{html.escape(label)}</a></li>' for key,label in headings) + "</ol>"
    return str(soup), toc


def page(title: str, body: str, toc: str, dest: str, active: str = "") -> str:
    def url(target): return relative(dest,target)
    navigation = "".join(f'<a href="{url(target)}"'+(' aria-current="page"' if label==active else '')+f'>{label}</a>'
                         for label,target in [("首页","index.html"),("报告","report/index.html"),("Notebook","notebook/index.html"),("数据","data/index.html")])
    content = f'<div class="layout"><aside class="toc"><details open><summary>本页目录</summary>{toc}</details></aside><main id="content">{body}</main></div>' if toc else f'<main class="home" id="content">{body}</main>'
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · 安徽农户持续种粮调研</title>
<meta name="description" content="安徽农户持续种粮调研：研究报告、公开数据与可复核 Notebook。淮南师范学院青穗江淮调研团。">
<link rel="canonical" href="{BASE+dest.removesuffix('index.html')}"><link rel="icon" href="data:,">
<link rel="stylesheet" href="{url('assets/style.css')}"><link rel="stylesheet" href="{url('assets/katex/katex.min.css')}">
<script defer src="{url('assets/katex/katex.min.js')}"></script><script defer src="{url('assets/site.js')}"></script></head>
<body id="top"><a class="skip" href="#content">跳转正文</a><header><div class="bar"><a class="brand" href="{url('index.html')}">青穗江淮 · 调研文库</a><nav aria-label="主导航">{navigation}</nav></div></header>
{content}<footer>淮南师范学院 · 青穗江淮调研团 · <a href="{REPO}">GitHub</a> · <a href="{url('CITATION.html')}">引用</a> · <a href="{REPO}/blob/main/LICENSE">许可</a><br>原创研究内容 CC BY-SA 4.0 · 软件 AGPL-3.0-only</footer></body></html>'''


def notebook_body(output: Path) -> str:
    notebook = json.loads((ROOT / "notebooks/analysis.ipynb").read_text(encoding="utf-8"))
    if notebook.get("metadata", {}).get("plot_style", {}).get("mode") != "publication":
        raise ValueError("Publish only the reviewed notebook rendered with publication fonts")
    parts = ['<p class="eyebrow">研究计算 · 已执行输出</p>',
             '<div class="actions"><a href="../notebooks/analysis.ipynb" download>下载 Notebook</a><a href="../docs/usage.html">运行指南</a></div>',
             '<div class="toolbar"><button data-code="show">展开全部代码</button><button data-code="hide">收起全部代码</button><button data-print>打印阅读页</button><span class="meta" id="code-status" role="status"></span></div>']
    image_index = 0
    for cell in notebook["cells"]:
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            parts.append(render_markdown(source))
            continue
        if cell["cell_type"] != "code": continue
        if cell.get("execution_count") is None:
            raise ValueError("Notebook contains an unexecuted cell")
        parts.append(f'<section class="notebook-cell"><details class="code-cell"><summary>代码 [{cell["execution_count"]}] · 展开查看</summary><pre><code>{html.escape(source)}</code></pre></details>')
        for result in cell.get("outputs", []):
            if result.get("output_type") == "error": raise ValueError("Notebook contains an error")
            data = result.get("data", {})
            if "image/svg+xml" in data or "image/png" in data:
                image_index += 1
                svg = "image/svg+xml" in data
                suffix = "svg" if svg else "png"
                filename = f"assets/notebook/figure-{image_index:02d}.{suffix}"
                target = output/filename
                target.parent.mkdir(parents=True,exist_ok=True)
                value = data["image/svg+xml" if svg else "image/png"]
                value = "".join(value) if isinstance(value,list) else value
                target.write_bytes(value.encode("utf-8") if svg else base64.b64decode(value))
                captions = ["土地经营状态与劳动力分组", "撂荒模型优势比与置信区间", "经营面积与灾害预测情景", "敏感性口径比较", "经营画像的占比与特征", "农户端指标", "村级指标", "农户与村级并列指标"]
                parts.append(f'<figure class="output"><img src="../{filename}" alt="{captions[image_index-1]}"></figure>')
            elif "text/html" in data:
                parts.append('<div class="output">'+"".join(data["text/html"])+"</div>")
            elif "text" in result:
                parts.append('<div class="output"><pre>'+html.escape("".join(result["text"]))+'</pre></div>')
            elif "text/plain" in data:
                parts.append('<div class="output"><pre>'+html.escape("".join(data["text/plain"]))+'</pre></div>')
        parts.append('</section>')
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output == ROOT or output in ROOT.parents or ROOT in output.parents:
        parser.error("Output must be a dedicated directory outside the source repository")
    output.mkdir(parents=True,exist_ok=True)
    (output/"assets").mkdir(exist_ok=True)
    for name in ("style.css", "site.js"):
        shutil.copy2(ROOT/"web"/name, output/"assets"/name)
    shutil.copytree(ROOT/"web/vendor/katex", output/"assets/katex", dirs_exist_ok=True)
    for folder in ("data","figures","references","surveys","notebooks","docs","LICENSES"):
        for source in (ROOT/folder).rglob("*"):
            if source.is_file() and source.suffix != ".md":
                target = output/source.relative_to(ROOT)
                target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(source,target)
    for source in ROOT.rglob("*.md"):
        relative_source=source.relative_to(ROOT).as_posix()
        if any(part.startswith(".") for part in source.relative_to(ROOT).parts):continue
        if relative_source in {"README.md", "notebooks/README.md"}:continue
        if relative_source.startswith("web/"):continue
        destination=route(relative_source)
        text=source.read_text(encoding="utf-8-sig")
        body,toc=enhance(render_markdown(text),relative_source,destination)
        title=next((line.lstrip('# ').strip() for line in text.splitlines() if line.startswith('# ')),source.stem)
        target=output/destination
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(page(title,body,toc,destination,"报告" if relative_source=="report/report.md" else ""),encoding="utf-8",newline="\n")
    # Notebook output paths already refer to the destination, not source Markdown.
    body,toc=enhance(notebook_body(output),"notebook/index.md","notebook/index.html")
    (output/'notebook').mkdir(exist_ok=True)
    (output/'notebook/index.html').write_text(page("公开数据分析与结果复核",body,toc,"notebook/index.html","Notebook"),encoding='utf-8')
    home='''<p class="eyebrow">安徽农户持续种粮调研 · 研究文库</p><h1>把地种好，把日子过稳</h1>
<p class="lead">稳定承包如何转化为持续经营？从家庭劳动力、土地与合同、社会化服务和收益风险出发，理解安徽农户的经营处境。</p>
<p class="meta">淮南师范学院 · 青穗江淮调研团<br>2025 年 2,079 户主实证 · 2026 年 570 户与 38 村并列证据</p>
<figure><img src="figures/diagrams/fig1-1_grain_continuity_mechanism.png" alt="持续种粮主机制链"><figcaption>研究框架：从稳定承包到持续经营。</figcaption></figure>
<a class="entry" href="report/"><strong>01　阅读研究报告 →</strong><span>八章正文、方法公式、16 张图与调查附录。按章节连续阅读。</span></a>
<a class="entry" href="notebook/"><strong>02　核对数据与计算 →</strong><span>已执行 Notebook：数据表、复算代码、学术图表与一致性检查。</span></a>
<a class="entry" href="data/"><strong>03　查找研究材料 →</strong><span>24 个聚合结果与制图数据文件，按用途进入。</span></a>
<div class="actions"><a href="figures/">图表索引</a><a href="surveys/">调查工具</a><a href="references/">参考文献</a><a href="docs/usage.html">复现指南</a></div>'''
    (output/'index.html').write_text(page("把地种好，把日子过稳",home,"","index.html","首页"),encoding='utf-8')
    for name in ("llms.txt","llm.txt","llms-full.txt","CITATION.cff","LICENSE"):
        shutil.copy2(ROOT/name, output/name)
    (output/'report/report.md').write_bytes((ROOT/'report/report.md').read_bytes())
    (output/'.nojekyll').write_text('',encoding='utf-8')
    print(f"site=BUILT\nhtml_pages={len(list(output.rglob('*.html')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
