"""Academic plotting style with explicit publication font verification."""
from __future__ import annotations

import os
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
import seaborn as sns


def configure() -> dict:
    mode = os.environ.get("SURVEY_FONT_MODE", "publication")
    families = ["Times New Roman", "SimSun"]
    if mode == "portable":
        families = ["Liberation Serif", "Noto Serif CJK JP"]
    elif mode != "publication":
        raise ValueError("Unknown SURVEY_FONT_MODE")
    resolved = {}
    for name in families:
        try:
            filename = font_manager.findfont(name, fallback_to_default=False)
        except ValueError as exc:
            raise RuntimeError(f"Required font missing: {name}. Install it before rendering.") from exc
        resolved[name] = Path(filename).name
    sns.set_theme(style="ticks", context="paper", palette=["#252525", "#777777", "#aaaaaa", "#dddddd"])
    mpl.rcParams.update({
        "font.family": families, "font.size": 11,
        "axes.labelsize": 11, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "legend.fontsize": 10, "figure.facecolor": "white", "axes.facecolor": "white",
        "axes.edgecolor": "black", "axes.linewidth": .8, "axes.grid": False,
        "grid.color": "#dddddd", "grid.linewidth": .5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.unicode_minus": False, "lines.linewidth": 1.2,
        "lines.markerfacecolor": "white", "patch.edgecolor": "black",
        "patch.linewidth": .7, "svg.fonttype": "path", "svg.hashsalt": "anhui-survey",
        "savefig.dpi": 180, "mathtext.fontset": "custom",
        "mathtext.rm": families[0], "mathtext.it": families[0] + ":italic",
        "mathtext.bf": families[0] + ":bold",
    })
    return {"mode": mode, "families": families, "font_files": resolved}


def finish_figure(fig) -> None:
    """Place panel captions below axes and retain monochrome distinctions."""
    axes = fig.axes
    captions = []
    for i, ax in enumerate(axes):
        title = ax.get_title()
        ax.set_title("")
        captions.append((ax, title))
        ax.grid(axis="x" if len(ax.get_yticklabels()) > 8 else "y", color="#dddddd", linewidth=.5)
        for container_index, container in enumerate(ax.containers):
            if isinstance(container, mpl.container.BarContainer):
                for patch in container.patches:
                    patch.set_edgecolor("#333333")
                    patch.set_linewidth(.6)
                    patch.set_hatch(["", "///", "..", "xx"][container_index % 4])
        if ax.get_legend() is not None:
            ax.get_legend().set_frame_on(False)
    fig.tight_layout(rect=(0, .13, 1, 1), w_pad=3)
    for i, (ax, caption) in enumerate(captions):
        box = ax.get_position()
        prefix = f"（{chr(97+i)}）" if len(axes) > 1 else ""
        fig.text((box.x0 + box.x1)/2, .025, prefix + caption,
                 ha="center", va="bottom", fontsize=11)
    plt.show()
