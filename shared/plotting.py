"""shared.plotting — one style, colourblind-safe palette, and the handful of plot helpers notebooks reuse."""
from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import ListedColormap

# Wong (2011) colourblind-safe palette + two extras
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#999999", "#000000", "#882255"]
CMAP = ListedColormap(PALETTE)
CLINICAL = {"normal": "#009E73", "warning": "#E69F00", "critical": "#D55E00", "neutral": "#999999"}


def set_style():
    plt.style.use("seaborn-v0_8-whitegrid")
    mpl.rcParams.update({
        "figure.figsize": (12, 6), "figure.dpi": 100, "savefig.dpi": 150, "savefig.bbox": "tight",
        "font.size": 12, "axes.titlesize": 14, "axes.labelsize": 12, "legend.fontsize": 10,
        "axes.prop_cycle": mpl.cycler(color=PALETTE), "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.alpha": 0.3, "legend.framealpha": 0.9,
    })
    sns.set_palette(PALETTE)


def grid(n, ncols=3, panel=(6, 5)):
    """fig, axes(flat) for n panels; unused axes hidden."""
    nrows = int(np.ceil(n / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(panel[0] * ncols, panel[1] * nrows), squeeze=False)
    flat = axes.ravel()
    for ax in flat[n:]:
        ax.set_visible(False)
    return fig, flat[:n]


def decision_boundary(model, X, y, ax=None, res=200, alpha=0.3, title=""):
    if ax is None:
        _, ax = plt.subplots(figsize=(8, 6))
    x0, x1 = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y0, y1 = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    xx, yy = np.meshgrid(np.linspace(x0, x1, res), np.linspace(y0, y1, res))
    Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)
    k = len(np.unique(y))
    ax.contourf(xx, yy, Z, alpha=alpha, cmap=ListedColormap(PALETTE[:k]))
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=ListedColormap(PALETTE[:k]), edgecolors="k", lw=0.4, s=35)
    ax.set(xlim=(x0, x1), ylim=(y0, y1), xlabel="feature 1", ylabel="feature 2", title=title)
    return ax


def sweep(param_values, train, test, param_name, metric="score", log=False, ax=None):
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 6))
    ax.plot(param_values, train, "o-", label="train", lw=2)
    ax.plot(param_values, test, "s-", label="test", lw=2)
    b = int(np.argmax(test))
    ax.axvline(param_values[b], ls="--", color=PALETTE[2], alpha=0.7, label=f"best {param_name}={param_values[b]}")
    if log:
        ax.set_xscale("log")
    ax.set(xlabel=param_name, ylabel=metric, title=f"{metric} vs {param_name}")
    ax.legend()
    return ax


def curves(history: dict, title="Training"):
    metrics = [k[6:] for k in history if k.startswith("train_")]
    fig, axes = grid(len(metrics), ncols=len(metrics), panel=(7, 5))
    for ax, m in zip(axes, metrics):
        ax.plot(history[f"train_{m}"], label="train", lw=2)
        if f"val_{m}" in history:
            ax.plot(history[f"val_{m}"], label="val", lw=2)
        ax.set(xlabel="epoch", ylabel=m, title=m); ax.legend()
    fig.suptitle(title, fontweight="bold")
    return fig


def patches(X, y=None, n=12, title="Lesion patches"):
    """Show image patches from datasets.load_imaging."""
    fig, axes = grid(n, ncols=6, panel=(2.2, 2.4))
    for i, ax in enumerate(axes):
        ax.imshow(X[i], cmap="gray", vmin=0, vmax=1); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
        if y is not None:
            ax.set_title("lesion" if y[i] else "clear", fontsize=9, color=CLINICAL["critical" if y[i] else "normal"])
    fig.suptitle(title, fontweight="bold")
    return fig
