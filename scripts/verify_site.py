"""Verify published local routes, assets, anchors, notebook output and mathematics."""
from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path",type=Path)
    root=parser.parse_args().path.resolve()
    problems=[]
    links=0
    for page in root.rglob('*.html'):
        soup=BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser')
        if not soup.find('main') or not soup.find('title'):problems.append(f'empty_page:{page.name}')
        for node in soup.select('[href], [src]'):
            value=node.get('href',node.get('src',''))
            parsed=urlsplit(value)
            if parsed.scheme or parsed.netloc:continue
            links+=1
            target=(page.parent/unquote(parsed.path)).resolve() if parsed.path else page
            if target.is_dir():target=target/'index.html'
            if not target.is_relative_to(root) or not target.is_file():
                problems.append(f'broken_link:{page.relative_to(root)}:{value}')
            elif parsed.fragment and target.suffix=='.html':
                other=BeautifulSoup(target.read_text(encoding='utf-8'),'html.parser')
                if other.find(id=unquote(parsed.fragment)) is None:
                    problems.append(f'broken_anchor:{page.relative_to(root)}:{value}')
    report=BeautifulSoup((root/'report/index.html').read_text(encoding='utf-8'),'html.parser')
    notebook=BeautifulSoup((root/'notebook/index.html').read_text(encoding='utf-8'),'html.parser')
    if len(report.select('.math.block')) != 5:problems.append('report_equation_count')
    if len(report.select('main img')) != 16:problems.append('report_figure_count')
    for name, document, count in [('report', report, 7), ('notebook', notebook, 13)]:
        tables = document.select('main table')
        if len(tables) != count:problems.append(f'{name}_table_count')
        for index, table in enumerate(tables, 1):
            if not table.caption or not table.caption.get_text(strip=True):
                problems.append(f'{name}_table_title_missing:{index}')
            elif table.find(recursive=False).name != 'caption':
                problems.append(f'{name}_table_title_position:{index}')
    for index, figure in enumerate(report.select('main figure'), 1):
        if not figure.figcaption or figure.find_all(recursive=False)[-1].name != 'figcaption':
            problems.append(f'report_figure_caption_position:{index}')
    if len(notebook.select('.code-cell')) != 12:problems.append('notebook_code_count')
    if len(list((root/'assets/notebook').glob('*.svg'))) != 8:problems.append('notebook_vector_count')
    for svg in (root/'assets/notebook').glob('*.svg'):
        text=svg.read_text(encoding='utf-8')
        if 'SimSun' not in text or 'TimesNewRoman' not in text:
            problems.append(f'font_glyphs_missing:{svg.name}')
    if problems:
        print('site=FAIL\n'+'\n'.join(problems))
        return 1
    print(f'site=PASS\nlocal_links={links}\nreport_equations=5\nreport_figures=16\nnotebook_figures=8\nnotebook_code_cells=12')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
