"""Publication-ready plotting utilities and theme configuration."""

from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns


def configure_plot_style() -> None:
    """Configure Matplotlib and Seaborn aesthetics for academic presentation."""
    sns.set_theme(
        style="whitegrid",
        font="sans-serif",
        palette="deep",
    )
    plt.rcParams.update(
        {
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "axes.titlesize": 13,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "figure.titlesize": 14,
            "font.family": "sans-serif",
        }
    )
