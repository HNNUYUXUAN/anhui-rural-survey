# Repository guidance

## Read first

- Read `README.md`, `DATA.md`, `docs/agent-guide.md`, and `docs/maintenance.md` before changing this repository.
- Inspect Git status and preserve existing user changes.
- Use `docs/resource-catalog.json` and `python scripts/build_discovery.py --query <term>` to locate research materials.

## Research and presentation

- Write reader-facing Chinese prose around the research question and the reader's task. Use direct links and existing research figures in navigation.
- Keep implementation and maintenance details in technical guides. Keep scientific qualifications beside the result they qualify.
- Preserve source data, authorship, research version, and license scope unless the requested change explicitly covers them.
- Cite exact tables and report sections. Keep years, effective denominators, units, and model assumptions explicit. Distinguish conditional associations from causal conclusions and household/village parallel evidence from matched observations.
- Use standard LaTeX for mathematics. For new figures, prefer an academic white background, legible Chinese and Latin fonts, clear units, captions below figures and titles above tables. Inspect overlap and clipping.
- Use SimSun for Chinese and Times New Roman for Latin text and numbers in publication charts. Preserve SVG glyph outlines for web display. Portable CI fonts may only be used in isolated execution checks.
- Use short English directory and file names; keep prose and research labels in their source language. Maintain `docs/path-map.json` for path migrations.
- Follow the approved public-data list in `scripts/verify_release.py`; source records and third-party full texts require separate publication review.

## Validation and handoff

- Run `python scripts/verify_release.py` and `python scripts/build_discovery.py --check`.
- Run `python scripts/build_analysis_notebook.py --execute` when changing computation or research data; inspect real outputs.
- Regenerate discovery files with `python scripts/build_discovery.py`. Stage reviewed new files before `python scripts/update_release_manifest.py`, then rerun verification and stage the manifests.
- Keep local environments and QA artifacts outside the repository. Inspect `git diff --check` and the staged diff before committing.
- Report the concrete change, checks, commit, and review URL after pushing.
- Build Pages outside the repository with `python scripts/build_site.py --output ../site`, then run `python scripts/verify_site.py ../site` and inspect desktop and narrow-screen behavior. Publish only reviewed, executed notebook outputs.

## Browser runtime

Use the installed Playwright CLI with Chromium. Windows uses `C:/ProgramData/PlaywrightRuntime` and `C:/ProgramData/ms-playwright`; WSL uses `/opt/playwright-runtime` and `/opt/ms-playwright`. Keep automatic browser downloads disabled. Report a missing or incompatible runtime instead of installing a browser.
