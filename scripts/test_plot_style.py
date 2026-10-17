"""Regression checks for chart semantics and caption placement."""
import unittest
from unittest.mock import patch

import matplotlib.pyplot as plt

from plot_style import configure, finish_figure


class PlotStyleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        configure()

    def tearDown(self):
        plt.close("all")

    def test_forest_points_and_caps_remain_unconnected(self):
        fig, ax = plt.subplots()
        bars = ax.errorbar([1, 2, 3, 4], range(4), xerr=.2, fmt="o", capsize=4)
        lines = [bars.lines[0], *bars.lines[1]]
        before = [line.get_linestyle() for line in lines]
        with patch("matplotlib.pyplot.show"):
            finish_figure(fig)
        self.assertEqual([line.get_linestyle() for line in lines], before)
        self.assertTrue(all(style == "None" for style in before))

    def test_caption_is_below_axes_and_hatches_distinguish_series(self):
        fig, ax = plt.subplots()
        first = ax.bar([0, 1], [2, 3])
        second = ax.bar([.3, 1.3], [4, 5])
        ax.set_title("经营状态")
        with patch("matplotlib.pyplot.show"):
            finish_figure(fig)
        self.assertEqual(ax.get_title(), "")
        self.assertEqual(fig.texts[0].get_text(), "经营状态")
        self.assertLess(fig.texts[0].get_position()[1], ax.get_position().y0)
        self.assertNotEqual(first.patches[0].get_hatch(), second.patches[0].get_hatch())


if __name__ == "__main__":
    unittest.main()
