"""Readable notebook tables; presentation never mutates source frames."""
from __future__ import annotations

from IPython.display import display
from pandas.api.types import is_bool_dtype, is_numeric_dtype


LABELS = {
    "state": "土地状态", "group": "劳动力组", "n": "有效 n", "percent": "比例",
    "term": "变量", "odds_ratio": "OR", "ci_low_or": "95%下限", "ci_high_or": "95%上限",
    "bootstrap_sign_p": "符号检验 p", "scenario": "分析口径", "fallow_percent": "撂荒比例",
    "labor_or": "劳动力 OR", "area_or": "面积 OR", "disaster_or": "受灾 OR", "status": "状态",
    "profile": "经营画像", "share_percent": "占比（%）", "labor": "劳动力（人）",
    "operated_area": "经营面积（亩）", "grain_area": "粮食面积（亩）",
    "managed_percent": "托管（%）", "transfer_out_percent": "转出（%）", "transfer_in_percent": "转入（%）",
    "label": "指标", "success": "肯定回答数", "denominator_rule": "有效分母规则",
    "sensitivity_n": "排短时 n", "sensitivity_success": "排短时肯定数", "sensitivity_percent": "排短时比例",
    "theme": "主题", "household_label": "农户指标", "household_percent": "农户比例",
    "household_n": "农户 n", "village_label": "村级指标", "village_percent": "村级比例", "village_n": "村级 n",
}


def show_table(frame, title: str, formats: dict | None = None) -> None:
    """Caption above; prose left aligned; numeric values right aligned."""
    labels = {column: LABELS.get(column, column) for column in frame.columns}
    shown = frame.rename(columns=labels)
    numeric = [labels[c] for c in frame if is_numeric_dtype(frame[c]) and not is_bool_dtype(frame[c])]
    formatted = {labels[c]: value for c, value in (formats or {}).items()}
    styled = (shown.style.set_uuid(title.split('　')[0]).hide(axis="index")
              .format(formatted, na_rep="—", escape="html")
              .set_caption(title)
              .set_properties(**{"text-align": "left", "vertical-align": "top"})
              .set_table_styles([
                  {"selector": "caption", "props": "caption-side:top;text-align:center;font-weight:bold;padding:0.8em 0;"},
                  {"selector": "th", "props": "text-align:left;white-space:nowrap;padding:0.6em 0.8em;border-bottom:1px solid #777;"},
                  {"selector": "td", "props": "padding:0.6em 0.8em;line-height:1.6;"},
              ]))
    if numeric:
        styled = styled.set_properties(subset=numeric, **{"text-align": "right", "white-space": "nowrap"})
    display(styled)
