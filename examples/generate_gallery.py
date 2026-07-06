#!/usr/bin/env python3
"""
generate_gallery.py — a COMPREHENSIVE gallery of publication-quality scientific figures.

~110 distinct chart types & variants across 9 categories, each from SYNTHETIC (seeded)
data and built to the data-strength-elevator publication-ready rules: one colorblind-safe
palette (Okabe-Ito), sans-serif typography, points shown on bars, exact stats, sequential
(never jet) colormaps, clean de-spined axes, vector + raster export.

Run:  python3 generate_gallery.py
Outputs PNG (300 dpi) + PDF (vector) per figure to ./png and ./pdf, grouped by category
prefix, and prints a manifest + a category count. One figure failing never aborts the batch.

Dependencies: matplotlib, numpy, scipy, seaborn, networkx, statsmodels, pandas (no LaTeX).
"""
import os, warnings
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch
import seaborn as sns
import networkx as nx
from scipy import stats
from scipy.optimize import curve_fit
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "png"); PDF = os.path.join(HERE, "pdf")
for d in (PNG, PDF):
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(d):  # clean stale outputs so the gallery is exactly this run
        os.remove(os.path.join(d, f))
RNG = np.random.default_rng(20260706)

OI = {"orange": "#E69F00", "blue": "#0072B2", "green": "#009E73", "purple": "#CC79A7",
      "vermillion": "#D55E00", "sky": "#56B4E9", "yellow": "#F0E442", "grey": "#999999",
      "black": "#000000"}
CYCLE = [OI["orange"], OI["blue"], OI["green"], OI["purple"], OI["vermillion"], OI["sky"], OI["yellow"]]
SEQ = "viridis"; DIV = "RdBu_r"

MANIFEST = []


def set_style():
    mpl.rcParams.update({
        "figure.dpi": 110, "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
        "font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8.5, "axes.titleweight": "regular",
        "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
        "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=CYCLE), "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.width": 0.8, "ytick.major.width": 0.8, "lines.linewidth": 1.5,
        "lines.markersize": 4.5, "legend.frameon": False, "axes.axisbelow": True,
        "mathtext.default": "regular", "figure.facecolor": "white",
    })


def save(fig, name, note, cat):
    fig.savefig(os.path.join(PNG, name + ".png"))
    fig.savefig(os.path.join(PDF, name + ".pdf"))
    plt.close(fig)
    MANIFEST.append((cat, name, note))


def title(ax, s):
    ax.set_title(s, loc="left", fontsize=8.5)


def squarify(sizes, x, y, dx, dy):
    """Minimal treemap layout (normalized sizes -> rectangles)."""
    sizes = np.asarray(sizes, float); sizes = sizes / sizes.sum() * (dx * dy)
    rects = []; i = 0
    while i < len(sizes):
        # simple slice-and-dice
        if dx >= dy:
            w = sizes[i] / dy; rects.append((x, y, w, dy)); x += w; dx -= w
        else:
            h = sizes[i] / dx; rects.append((x, y, dx, h)); y += h; dy -= h
        i += 1
    return rects


# ============================================================ A. DISTRIBUTIONS
def dist_histogram_basic():
    d = RNG.normal(50, 12, 500)
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.hist(d, bins=25, color=OI["blue"], edgecolor="white", linewidth=0.4)
    ax.set_xlabel("Particle size (nm)"); ax.set_ylabel("Count"); title(ax, "Histogram")
    save(fig, "A01_histogram", "single distribution", "Distributions")

def dist_histogram_multiple():
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    for m, c, lab in [(45, OI["blue"], "Batch A"), (58, OI["orange"], "Batch B")]:
        ax.hist(RNG.normal(m, 9, 400), bins=22, alpha=0.55, color=c, label=lab, edgecolor="white", linewidth=0.3)
    ax.set_xlabel("Size (nm)"); ax.set_ylabel("Count"); ax.legend(); title(ax, "Overlaid histograms")
    save(fig, "A02_histogram_multiple", "compare two distributions", "Distributions")

def dist_histogram_kde():
    d = RNG.gamma(4, 6, 500)
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    ax.hist(d, bins=25, density=True, color=OI["sky"], edgecolor="white", linewidth=0.4, alpha=0.8)
    sns.kdeplot(d, color=OI["black"], lw=1.5, ax=ax)
    ax.set_xlabel("Response"); ax.set_ylabel("Density"); title(ax, "Histogram + KDE")
    save(fig, "A03_histogram_kde", "density overlay", "Distributions")

def dist_hist2d():
    x = RNG.normal(0, 1, 4000); y = x * 0.6 + RNG.normal(0, 0.8, 4000)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    h = ax.hist2d(x, y, bins=40, cmap=SEQ)
    fig.colorbar(h[3], ax=ax, fraction=0.046, pad=0.04, label="Count")
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "2D histogram")
    save(fig, "A04_hist2d", "joint density (binned)", "Distributions")

def dist_hexbin():
    x = RNG.normal(0, 1, 5000); y = x * 0.5 + RNG.normal(0, 0.7, 5000)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    hb = ax.hexbin(x, y, gridsize=28, cmap=SEQ, mincnt=1)
    fig.colorbar(hb, ax=ax, fraction=0.046, pad=0.04, label="Count")
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Hexbin density")
    save(fig, "A05_hexbin", "joint density (hex)", "Distributions")

def dist_kde_basic():
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    sns.kdeplot(RNG.normal(0, 1, 800), fill=True, color=OI["green"], ax=ax, lw=1.2)
    ax.set_xlabel("Value"); ax.set_ylabel("Density"); title(ax, "Kernel density (KDE)")
    save(fig, "A06_kde", "smooth density", "Distributions")

def dist_kde_multiple():
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    for m, c, lab in [(-1, OI["blue"], "Control"), (0.5, OI["orange"], "Treated"), (2, OI["green"], "High")]:
        sns.kdeplot(RNG.normal(m, 1, 600), color=c, fill=True, alpha=0.25, ax=ax, label=lab, lw=1.2)
    ax.legend(); ax.set_xlabel("Value"); ax.set_ylabel("Density"); title(ax, "Multiple KDEs")
    save(fig, "A07_kde_multiple", "compare densities", "Distributions")

def dist_ridgeline():
    groups = [f"Day {d}" for d in range(1, 9)]
    fig, axes = plt.subplots(len(groups), 1, figsize=(3.6, 3.4), sharex=True)
    cmap = mpl.colormaps[SEQ]
    for i, (g, ax) in enumerate(zip(groups, axes)):
        d = RNG.normal(2 + i * 0.6, 1, 400)
        sns.kdeplot(d, ax=ax, fill=True, color=cmap(i / 7), alpha=0.8, lw=0.8)
        ax.set_ylabel(""); ax.set_yticks([]); ax.set_facecolor("none")
        ax.tick_params(left=False)
        for s in ["left", "right", "top"]:
            ax.spines[s].set_visible(False)
        ax.text(-0.02, 0.12, g, transform=ax.transAxes, ha="right", va="center", fontsize=6.5)
        if i < len(groups) - 1:
            ax.set_xlabel("")
    axes[-1].set_xlabel("Marker intensity")
    fig.suptitle("Ridgeline (joyplot)", x=0.12, y=0.94, ha="left", fontsize=8.5)
    fig.subplots_adjust(hspace=-0.3)
    save(fig, "A08_ridgeline", "distribution over an ordered factor", "Distributions")

def dist_box_grouped():
    data = [RNG.normal(m, s, 40) for m, s in [(20, 5), (28, 6), (35, 5), (42, 7)]]
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    bp = ax.boxplot(data, patch_artist=True, widths=0.6, showfliers=False,
                    medianprops=dict(color="k"))
    for i, box in enumerate(bp["boxes"]):
        box.set(facecolor=CYCLE[i], alpha=0.6, edgecolor="k", linewidth=0.7)
    for i, d in enumerate(data):
        ax.scatter(RNG.normal(i + 1, 0.05, len(d)), d, s=6, color="k", alpha=0.4, zorder=3)
    ax.set_xticklabels(["Q1", "Q2", "Q3", "Q4"]); ax.set_ylabel("Yield (%)")
    title(ax, "Box + points")
    save(fig, "A09_box_grouped", "distribution summary + raw", "Distributions")

def dist_box_notched():
    data = [RNG.normal(m, 6, 50) for m in (30, 45, 38)]
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    bp = ax.boxplot(data, notch=True, patch_artist=True, widths=0.55, medianprops=dict(color="k"))
    for i, box in enumerate(bp["boxes"]):
        box.set(facecolor=CYCLE[i], alpha=0.5)
    ax.set_xticklabels(["A", "B", "C"]); ax.set_ylabel("Score"); title(ax, "Notched box (median CI)")
    save(fig, "A10_box_notched", "median confidence via notch", "Distributions")

def dist_violin():
    data = [RNG.normal(m, s, 200) for m, s in [(20, 5), (35, 7), (55, 9)]]
    fig, ax = plt.subplots(figsize=(3.4, 2.8))
    parts = ax.violinplot(data, showmeans=True)
    for i, b in enumerate(parts["bodies"]):
        b.set_facecolor(CYCLE[i]); b.set_alpha(0.6)
    ax.set_xticks([1, 2, 3]); ax.set_xticklabels(["Low", "Mid", "High"]); ax.set_ylabel("Response")
    title(ax, "Violin (n large)")
    save(fig, "A11_violin", "distribution shape at large n", "Distributions")

def dist_violin_split():
    df = []
    for grp in ["A", "B"]:
        for sex, m in [("M", 30), ("F", 36)]:
            for v in RNG.normal(m + (5 if grp == "B" else 0), 6, 150):
                df.append((grp, sex, v))
    import pandas as pd
    df = pd.DataFrame(df, columns=["group", "sex", "val"])
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    sns.violinplot(data=df, x="group", y="val", hue="sex", split=True, ax=ax,
                   palette=[OI["blue"], OI["orange"]], inner="quart", linewidth=0.8)
    ax.set_ylabel("Value"); ax.set_xlabel("Group"); title(ax, "Split violin")
    save(fig, "A12_violin_split", "distribution by two factors", "Distributions")

def dist_raincloud():
    conds = ["Control", "Low", "High"]; data = [RNG.normal(m, s, 60) for m, s in [(20, 5), (35, 7), (55, 9)]]
    fig, ax = plt.subplots(figsize=(3.6, 2.9))
    for i, d in enumerate(data):
        c = CYCLE[i]
        parts = ax.violinplot(d, positions=[i], widths=0.7, showextrema=False)
        for b in parts["bodies"]:
            b.set_facecolor(c); b.set_alpha(0.35)
            m = np.mean(b.get_paths()[0].vertices[:, 0])
            b.get_paths()[0].vertices[:, 0] = np.clip(b.get_paths()[0].vertices[:, 0], -np.inf, m)
        ax.scatter(RNG.normal(i + 0.2, 0.03, len(d)), d, s=6, color=c, alpha=0.6)
    ax.set_xticks(range(3)); ax.set_xticklabels(conds); ax.set_ylabel("Response")
    title(ax, "Raincloud")
    save(fig, "A13_raincloud", "half-violin + strip", "Distributions")

def dist_strip():
    data = [RNG.normal(m, 4, 12) for m in (20, 26, 33)]
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    for i, d in enumerate(data):
        ax.scatter(RNG.normal(i, 0.06, len(d)), d, s=22, color=CYCLE[i], edgecolor="k", linewidth=0.4)
        ax.hlines(d.mean(), i - 0.2, i + 0.2, color="k", lw=1.5)
    ax.set_xticks(range(3)); ax.set_xticklabels(["A", "B", "C"]); ax.set_ylabel("Value")
    title(ax, "Strip / jitter (small n)")
    save(fig, "A14_strip", "every point at small n", "Distributions")

def dist_ecdf():
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    for m, c, lab in [(0, OI["blue"], "Ref"), (1, OI["orange"], "Test")]:
        ax.ecdf(RNG.normal(m, 1, 300), color=c, label=lab, lw=1.5)
    ax.legend(); ax.set_xlabel("Value"); ax.set_ylabel("Cumulative probability")
    title(ax, "Empirical CDF")
    save(fig, "A15_ecdf", "cumulative distribution", "Distributions")

def dist_qq():
    d = RNG.standard_t(5, 200)
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    stats.probplot(d, dist="norm", plot=ax)
    ax.get_lines()[0].set(marker="o", markersize=3, markerfacecolor=OI["blue"], markeredgecolor="k", markeredgewidth=0.3, ls="")
    ax.get_lines()[1].set(color=OI["orange"], lw=1.2)
    ax.set_title(""); title(ax, "Q–Q plot (normality)")
    save(fig, "A16_qq", "distributional check", "Distributions")


# ============================================================ B. CORRELATION / RELATIONSHIP
def corr_scatter():
    x = RNG.uniform(0, 10, 80); y = 2 * x + RNG.normal(0, 3, 80)
    fig, ax = plt.subplots(figsize=(3.3, 2.9))
    ax.scatter(x, y, s=20, color=OI["blue"], alpha=0.8, edgecolor="k", linewidth=0.3)
    ax.set_xlabel("Concentration"); ax.set_ylabel("Signal"); title(ax, "Scatter")
    save(fig, "B01_scatter", "two continuous variables", "Correlation")

def corr_scatter_groups():
    fig, ax = plt.subplots(figsize=(3.5, 2.9))
    for i, (m, lab) in enumerate([(2, "Type I"), (5, "Type II"), (8, "Type III")]):
        x = RNG.normal(m, 1, 40); y = x + RNG.normal(0, 0.8, 40)
        ax.scatter(x, y, s=20, color=CYCLE[i], label=lab, alpha=0.8, edgecolor="k", linewidth=0.3)
    ax.legend(); ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Scatter by group")
    save(fig, "B02_scatter_groups", "grouped scatter", "Correlation")

def corr_bubble():
    x = RNG.uniform(0, 10, 40); y = RNG.uniform(0, 10, 40); s = RNG.uniform(20, 400, 40)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    sc = ax.scatter(x, y, s=s, c=s, cmap=SEQ, alpha=0.7, edgecolor="k", linewidth=0.3)
    fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, label="Magnitude")
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Bubble chart")
    save(fig, "B03_bubble", "third variable via size", "Correlation")

def corr_regression():
    x = RNG.uniform(0, 10, 60); y = 1.5 * x + 3 + RNG.normal(0, 2.5, 60)
    sl, ic, r, p, se = stats.linregress(x, y)
    xx = np.linspace(0, 10, 100); yy = sl * xx + ic
    resid = y - (sl * x + ic); s_err = np.sqrt(np.sum(resid**2) / (len(x) - 2))
    ci = 1.96 * s_err * np.sqrt(1 / len(x) + (xx - x.mean())**2 / np.sum((x - x.mean())**2))
    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    ax.scatter(x, y, s=18, color=OI["blue"], alpha=0.75, edgecolor="k", linewidth=0.3)
    ax.plot(xx, yy, color=OI["orange"], lw=1.6)
    ax.fill_between(xx, yy - ci, yy + ci, color=OI["orange"], alpha=0.18, linewidth=0)
    ax.text(0.05, 0.9, f"r = {r:.2f}\nP = {p:.1e}", transform=ax.transAxes, fontsize=7)
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Regression + 95% CI")
    save(fig, "B04_regression", "linear fit with confidence band", "Correlation")

def corr_marginal():
    x = RNG.normal(0, 1, 300); y = 0.7 * x + RNG.normal(0, 0.7, 300)
    g = sns.JointGrid(x=x, y=y, height=3.4)
    g.plot_joint(sns.scatterplot, s=14, color=OI["blue"], alpha=0.6, edgecolor="k", linewidth=0.2)
    g.plot_marginals(sns.histplot, color=OI["blue"], edgecolor="white")
    g.set_axis_labels("x", "y")
    g.figure.suptitle("Scatter + marginals", x=0.35, y=1.0, fontsize=8.5)
    save(g.figure, "B05_marginal", "joint + marginal distributions", "Correlation")

def corr_connected():
    t = np.linspace(0, 2 * np.pi, 30); x = np.cos(t) + RNG.normal(0, 0.03, 30); y = np.sin(2 * t)
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    ax.plot(x, y, "-o", color=OI["purple"], markersize=3, lw=1)
    ax.scatter(x[0], y[0], color=OI["green"], s=30, zorder=3, label="start")
    ax.legend(); ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Connected scatter")
    save(fig, "B06_connected_scatter", "ordered trajectory in 2D", "Correlation")

def corr_heatmap():
    import pandas as pd
    data = RNG.normal(0, 1, (200, 8)); data[:, 1] += data[:, 0]; data[:, 3] -= data[:, 2]
    C = np.corrcoef(data, rowvar=False)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    im = ax.imshow(C, cmap=DIV, vmin=-1, vmax=1)
    for i in range(8):
        for j in range(8):
            ax.text(j, i, f"{C[i,j]:.1f}", ha="center", va="center", fontsize=5.5,
                    color="white" if abs(C[i, j]) > 0.6 else "k")
    ax.set_xticks(range(8)); ax.set_yticks(range(8))
    ax.set_xticklabels([f"V{i}" for i in range(8)], fontsize=6); ax.set_yticklabels([f"V{i}" for i in range(8)], fontsize=6)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Pearson r")
    title(ax, "Correlation matrix")
    save(fig, "B07_corr_heatmap", "pairwise correlations", "Correlation")

def corr_clustermap():
    data = RNG.normal(0, 1, (14, 10)); data[:5] += 1.6; data[9:] -= 1.6
    g = sns.clustermap(data, cmap=DIV, center=0, figsize=(3.8, 3.6),
                       cbar_pos=(0.02, 0.8, 0.03, 0.15), dendrogram_ratio=0.16,
                       xticklabels=False, yticklabels=False, linewidths=0.2)
    g.figure.suptitle("Clustered heatmap", x=0.55, y=1.0, fontsize=8.5)
    save(g.figure, "B08_clustermap", "reordered heatmap + dendrograms", "Correlation")

def corr_density2d():
    x = RNG.normal(0, 1, 500); y = 0.6 * x + RNG.normal(0, 0.7, 500)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    sns.kdeplot(x=x, y=y, fill=True, cmap=SEQ, levels=12, ax=ax, thresh=0.05)
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "2D density (contour)")
    save(fig, "B09_density2d", "smooth joint density", "Correlation")

def corr_pairplot():
    import pandas as pd
    n = 120
    df = pd.DataFrame({"size": RNG.normal(100, 20, n), "zeta": RNG.normal(-25, 8, n),
                       "PDI": RNG.uniform(0.1, 0.3, n)})
    df["EE"] = 40 + 0.3 * df["size"] + RNG.normal(0, 6, n)
    df["group"] = RNG.choice(["A", "B"], n)
    g = sns.pairplot(df, hue="group", height=1.05, palette=[OI["blue"], OI["orange"]],
                     plot_kws=dict(s=10, edgecolor="k", linewidth=0.2), corner=True)
    g.figure.suptitle("Pair plot (scatter matrix)", x=0.5, y=1.02, fontsize=8.5)
    save(g.figure, "B10_pairplot", "all pairwise relationships", "Correlation")

def corr_parity():
    obs = RNG.uniform(5, 95, 45); pred = obs + RNG.normal(0, 6, 45)
    r2 = 1 - np.sum((obs - pred)**2) / np.sum((obs - obs.mean())**2)
    fig, ax = plt.subplots(figsize=(3.1, 3.1))
    ax.plot([0, 100], [0, 100], "--", color="k", lw=1)
    ax.scatter(pred, obs, s=18, color=OI["blue"], alpha=0.8, edgecolor="k", linewidth=0.3)
    ax.set_aspect("equal"); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(5, 88, f"R² = {r2:.3f}", fontsize=7.5)
    ax.set_xlabel("Predicted"); ax.set_ylabel("Observed"); title(ax, "Parity (y = x)")
    save(fig, "B11_parity", "model calibration", "Correlation")

def corr_bland_altman():
    m1 = RNG.uniform(20, 80, 45); m2 = m1 + RNG.normal(2, 5, 45)
    mean = (m1 + m2) / 2; diff = m1 - m2; md, sd = diff.mean(), diff.std(ddof=1)
    fig, ax = plt.subplots(figsize=(3.5, 2.9))
    ax.scatter(mean, diff, s=16, color=OI["purple"], alpha=0.8, edgecolor="k", linewidth=0.3)
    for yv, ls in [(md, "--"), (md + 1.96 * sd, ":"), (md - 1.96 * sd, ":")]:
        ax.axhline(yv, ls=ls, lw=0.9, color="k")
    ax.set_xlabel("Mean"); ax.set_ylabel("Difference"); title(ax, "Bland–Altman")
    save(fig, "B12_bland_altman", "method agreement + LoA", "Correlation")

def corr_residual():
    x = RNG.uniform(0, 10, 80); y = 2 * x + RNG.normal(0, 1 + 0.15 * x, 80)  # heteroscedastic
    sl, ic, *_ = stats.linregress(x, y); resid = y - (sl * x + ic)
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.scatter(sl * x + ic, resid, s=16, color=OI["vermillion"], alpha=0.8, edgecolor="k", linewidth=0.3)
    ax.axhline(0, color="k", lw=0.9, ls="--")
    ax.set_xlabel("Fitted value"); ax.set_ylabel("Residual"); title(ax, "Residual plot")
    save(fig, "B13_residual", "diagnostic for a fit", "Correlation")

def _lowess(x, y, frac=0.3):
    """Pure-numpy LOWESS (tricube-weighted local linear fit)."""
    n = len(x); r = max(3, int(np.ceil(frac * n))); yhat = np.zeros(n)
    for i in range(n):
        d = np.abs(x - x[i]); idx = np.argsort(d)[:r]; dm = d[idx].max() or 1.0
        w = (1 - (d[idx] / dm) ** 3) ** 3
        X = np.vstack([np.ones(r), x[idx]]).T; Wd = w[:, None]
        beta, *_ = np.linalg.lstsq(X * Wd, y[idx] * w, rcond=None)
        yhat[i] = beta[0] + beta[1] * x[i]
    return yhat

def corr_loess():
    x = np.sort(RNG.uniform(0, 10, 120)); y = np.sin(x) + RNG.normal(0, 0.3, 120)
    fig, ax = plt.subplots(figsize=(3.4, 2.7))
    ax.scatter(x, y, s=12, color=OI["grey"], alpha=0.7)
    ax.plot(x, _lowess(x, y, 0.3), color=OI["orange"], lw=2)
    ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "LOESS smoother")
    save(fig, "B14_loess", "nonparametric trend", "Correlation")


# ============================================================ C. COMPARISON / RANKING
def comp_bar():
    cats = ["A", "B", "C", "D"]; vals = [23, 45, 31, 38]
    fig, ax = plt.subplots(figsize=(3.2, 2.7))
    ax.bar(cats, vals, color=OI["blue"], edgecolor="k", linewidth=0.6)
    ax.set_ylabel("Value"); title(ax, "Bar chart")
    save(fig, "C01_bar", "categorical magnitude (zero-based)", "Comparison")

def comp_bar_horizontal():
    cats = [f"Gene {i}" for i in range(8)]; vals = np.sort(RNG.uniform(1, 10, 8))
    fig, ax = plt.subplots(figsize=(3.3, 2.9))
    ax.barh(cats, vals, color=OI["green"], edgecolor="k", linewidth=0.5)
    ax.set_xlabel("Fold enrichment"); title(ax, "Horizontal bar")
    save(fig, "C02_bar_horizontal", "ranked categories", "Comparison")

def comp_grouped_bar():
    x = np.arange(3); w = 0.26
    means = np.array([[18, 42, 78], [15, 38, 71], [20, 45, 83]], float)
    err = means * 0.08
    fig, ax = plt.subplots(figsize=(4.0, 2.9))
    for j, lab in enumerate(["Vehicle", "Free", "NP"]):
        ax.bar(x + (j - 1) * w, means[:, j], w, yerr=err[:, j], color=CYCLE[j], edgecolor="k",
               linewidth=0.5, label=lab, error_kw=dict(elinewidth=0.7, capsize=2))
    ax.set_xticks(x); ax.set_xticklabels(["HeLa", "A549", "HepG2"]); ax.legend(); ax.set_ylabel("Uptake (%)")
    title(ax, "Grouped bar")
    save(fig, "C03_grouped_bar", "two-factor comparison", "Comparison")

def comp_stacked_bar():
    cats = ["S1", "S2", "S3", "S4"]; a = RNG.uniform(20, 40, 4); b = RNG.uniform(20, 40, 4); c = RNG.uniform(20, 40, 4)
    fig, ax = plt.subplots(figsize=(3.3, 2.8))
    ax.bar(cats, a, color=OI["blue"], label="Phase I", edgecolor="w", linewidth=0.3)
    ax.bar(cats, b, bottom=a, color=OI["orange"], label="Phase II", edgecolor="w", linewidth=0.3)
    ax.bar(cats, c, bottom=a + b, color=OI["green"], label="Phase III", edgecolor="w", linewidth=0.3)
    ax.legend(ncol=3, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, 1.18)); ax.set_ylabel("Amount")
    title(ax, "Stacked bar")
    save(fig, "C04_stacked_bar", "composition per category", "Comparison")

def comp_percent_stacked():
    cats = ["S1", "S2", "S3", "S4"]; M = RNG.uniform(1, 5, (3, 4)); M = M / M.sum(0) * 100
    fig, ax = plt.subplots(figsize=(3.3, 2.8))
    bottom = np.zeros(4)
    for j, (lab, c) in enumerate([("A", OI["blue"]), ("B", OI["orange"]), ("C", OI["green"])]):
        ax.bar(cats, M[j], bottom=bottom, color=c, label=lab, edgecolor="w", linewidth=0.3); bottom += M[j]
    ax.legend(ncol=3, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, 1.16)); ax.set_ylabel("Percent (%)"); ax.set_ylim(0, 100)
    title(ax, "100% stacked bar")
    save(fig, "C05_percent_stacked", "proportion per category", "Comparison")

def comp_diverging_bar():
    cats = [f"M{i}" for i in range(10)]; vals = np.sort(RNG.uniform(-1, 1, 10) * 3)
    cols = [OI["blue"] if v < 0 else OI["orange"] for v in vals]
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    ax.barh(cats, vals, color=cols, edgecolor="k", linewidth=0.4)
    ax.axvline(0, color="k", lw=0.8); ax.set_xlabel("log₂ fold-change"); title(ax, "Diverging bar")
    save(fig, "C06_diverging_bar", "signed values around zero", "Comparison")

def comp_dot_on_bar():
    groups = ["Reference", "F1", "F7"]; cols = [OI["grey"], OI["blue"], OI["orange"]]
    data = [RNG.normal(m, s, 8) for m, s in [(51, 4.5), (58, 5), (82, 3.2)]]
    means = [d.mean() for d in data]; sds = [d.std(ddof=1) for d in data]
    fig, ax = plt.subplots(figsize=(3.2, 2.9))
    ax.bar(range(3), means, 0.6, yerr=sds, color=cols, edgecolor="k", linewidth=0.6,
           error_kw=dict(elinewidth=0.8, capsize=3))
    for i, d in enumerate(data):
        ax.scatter(RNG.normal(i, 0.05, len(d)), d, s=14, facecolor="white", edgecolor="k", linewidth=0.5, zorder=3)
    t, p = stats.ttest_ind(data[2], data[0])
    ax.plot([0, 0, 2, 2], [92, 95, 95, 92], lw=0.8, c="k")
    ax.text(1, 96, f"P = {p:.1e}", ha="center", fontsize=6.5)
    ax.set_xticks(range(3)); ax.set_xticklabels(groups); ax.set_ylabel("Release (%)"); ax.set_ylim(0, 105)
    title(ax, "Dot-on-bar")
    save(fig, "C07_dot_on_bar", "bars never hide the sample (AP1)", "Comparison")

def comp_lollipop():
    cats = [f"Item {i}" for i in range(9)]; vals = np.sort(RNG.uniform(1, 10, 9))
    fig, ax = plt.subplots(figsize=(3.2, 3.0)); y = np.arange(9)
    ax.hlines(y, 0, vals, color=OI["grey"], lw=1.2)
    ax.scatter(vals, y, color=OI["orange"], s=40, zorder=3, edgecolor="k", linewidth=0.4)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=6.5); ax.set_xlabel("Value"); title(ax, "Lollipop")
    save(fig, "C08_lollipop", "ranked values, low ink", "Comparison")

def comp_cleveland():
    cats = [f"Assay {i}" for i in range(8)]; before = RNG.uniform(2, 5, 8); after = before + RNG.uniform(1, 4, 8)
    fig, ax = plt.subplots(figsize=(3.4, 3.0)); y = np.arange(8)
    ax.hlines(y, before, after, color=OI["grey"], lw=1.2, zorder=1)
    ax.scatter(before, y, color=OI["blue"], s=30, label="Before", zorder=3)
    ax.scatter(after, y, color=OI["orange"], s=30, label="After", zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(cats, fontsize=6.5); ax.legend(); ax.set_xlabel("Value")
    title(ax, "Cleveland dot / dumbbell")
    save(fig, "C09_cleveland_dumbbell", "paired change per category", "Comparison")

def comp_radar():
    labels = ["Potency", "Selectivity", "Solubility", "Stability", "Safety", "PK"]
    vals = [0.8, 0.65, 0.5, 0.9, 0.7, 0.6]; vals2 = [0.6, 0.8, 0.7, 0.5, 0.85, 0.75]
    ang = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist(); ang += ang[:1]
    fig, ax = plt.subplots(figsize=(3.2, 3.2), subplot_kw=dict(polar=True))
    for v, c, lab in [(vals, OI["blue"], "Lead"), (vals2, OI["orange"], "Backup")]:
        vv = v + v[:1]
        ax.plot(ang, vv, color=c, lw=1.5, label=lab); ax.fill(ang, vv, color=c, alpha=0.15)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(labels, fontsize=6.5); ax.set_yticklabels([])
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1)); title(ax, "Radar / spider")
    save(fig, "C10_radar", "multivariate profile", "Comparison")

def comp_parallel():
    import pandas as pd
    n = 60; df = pd.DataFrame({"A": RNG.normal(0, 1, n), "B": RNG.normal(0, 1, n),
                               "C": RNG.normal(0, 1, n), "D": RNG.normal(0, 1, n)})
    df["grp"] = RNG.choice([0, 1, 2], n)
    fig, ax = plt.subplots(figsize=(3.8, 2.8)); cols = ["A", "B", "C", "D"]
    for _, row in df.iterrows():
        ax.plot(range(4), [row[c] for c in cols], color=CYCLE[int(row["grp"])], alpha=0.35, lw=0.8)
    ax.set_xticks(range(4)); ax.set_xticklabels(cols); ax.set_ylabel("Standardized value")
    title(ax, "Parallel coordinates")
    save(fig, "C11_parallel_coords", "high-dim comparison", "Comparison")

def comp_slope():
    items = ["A", "B", "C", "D", "E"]; t1 = RNG.uniform(20, 80, 5); t2 = t1 + RNG.uniform(-15, 25, 5)
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    for i, it in enumerate(items):
        ax.plot([0, 1], [t1[i], t2[i]], "-o", color=CYCLE[i], markersize=4)
        ax.text(-0.05, t1[i], it, ha="right", fontsize=6.5); ax.text(1.05, t2[i], f"{t2[i]:.0f}", ha="left", fontsize=6.5)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["2024", "2025"]); ax.set_xlim(-0.3, 1.3)
    ax.set_ylabel("Metric"); title(ax, "Slope chart")
    save(fig, "C12_slope", "before/after ranking change", "Comparison")

def comp_bump():
    teams = ["A", "B", "C", "D", "E"]; T = 6
    ranks = np.array([RNG.permutation(5) + 1 for _ in range(T)]).T
    fig, ax = plt.subplots(figsize=(3.8, 2.8))
    for i, tm in enumerate(teams):
        ax.plot(range(T), ranks[i], "-o", color=CYCLE[i], markersize=4, label=tm)
    ax.invert_yaxis(); ax.set_yticks(range(1, 6)); ax.set_xlabel("Round"); ax.set_ylabel("Rank")
    ax.legend(ncol=5, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, 1.18)); title(ax, "Bump chart")
    save(fig, "C13_bump", "rank evolution over time", "Comparison")

def comp_error_only():
    cats = ["A", "B", "C", "D", "E"]; means = RNG.uniform(10, 40, 5); err = RNG.uniform(2, 6, 5)
    fig, ax = plt.subplots(figsize=(3.2, 2.7))
    ax.errorbar(range(5), means, yerr=err, fmt="o", color=OI["blue"], capsize=3, markersize=6, elinewidth=1)
    ax.set_xticks(range(5)); ax.set_xticklabels(cats); ax.set_ylabel("Estimate ± 95% CI")
    title(ax, "Point-estimate + CI")
    save(fig, "C14_point_ci", "position-based estimates", "Comparison")


# ============================================================ D. PART OF WHOLE
def pow_stacked_area():
    t = np.arange(20); ys = np.abs(RNG.normal(3, 1, (4, 20))).cumsum(1) * 0.3 + 1
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    ax.stackplot(t, ys, colors=CYCLE[:4], labels=["A", "B", "C", "D"], edgecolor="w", linewidth=0.2)
    ax.legend(ncol=4, fontsize=6, loc="upper left"); ax.set_xlabel("Time"); ax.set_ylabel("Amount")
    title(ax, "Stacked area")
    save(fig, "D01_stacked_area", "composition over time", "Part-of-whole")

def pow_treemap():
    sizes = np.sort(RNG.uniform(1, 10, 8))[::-1]; labels = [f"C{i}" for i in range(8)]
    rects = squarify(sizes, 0, 0, 1, 1)
    fig, ax = plt.subplots(figsize=(3.4, 3.0)); cmap = mpl.colormaps[SEQ]
    for i, (x, y, w, h) in enumerate(rects):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=cmap(i / 8), edgecolor="w", linewidth=1.2))
        ax.text(x + w / 2, y + h / 2, labels[i], ha="center", va="center", fontsize=7, color="w")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); title(ax, "Treemap")
    save(fig, "D02_treemap", "hierarchical proportions", "Part-of-whole")

def pow_sunburst():
    fig, ax = plt.subplots(figsize=(3.2, 3.2), subplot_kw=dict(polar=True))
    inner = [0.4, 0.35, 0.25]; ci = [OI["blue"], OI["orange"], OI["green"]]
    start = 0
    for frac, c in zip(inner, ci):
        ax.bar(np.pi * 2 * (start + frac / 2), 1, width=np.pi * 2 * frac, bottom=1, color=c, edgecolor="w")
        # outer
        for k in range(2):
            ax.bar(np.pi * 2 * (start + frac * (k + 0.5) / 2), 1, width=np.pi * 2 * frac / 2,
                   bottom=2, color=c, alpha=0.6 - 0.2 * k, edgecolor="w")
        start += frac
    ax.set_axis_off(); title(ax, "Sunburst (nested ring)")
    save(fig, "D03_sunburst", "nested hierarchy", "Part-of-whole")

def pow_venn():
    fig, ax = plt.subplots(figsize=(3.2, 2.8))
    ax.add_patch(Circle((0.38, 0.5), 0.28, color=OI["blue"], alpha=0.45))
    ax.add_patch(Circle((0.62, 0.5), 0.28, color=OI["orange"], alpha=0.45))
    ax.text(0.28, 0.5, "142", ha="center", fontsize=8); ax.text(0.72, 0.5, "98", ha="center", fontsize=8)
    ax.text(0.5, 0.5, "57", ha="center", fontsize=8)
    ax.text(0.28, 0.83, "Proteomics", ha="center", fontsize=7); ax.text(0.72, 0.83, "RNA-seq", ha="center", fontsize=7)
    ax.set_xlim(0, 1); ax.set_ylim(0.1, 0.95); ax.axis("off"); title(ax, "Venn diagram")
    save(fig, "D04_venn", "set overlap", "Part-of-whole")

def pow_dendrogram():
    from scipy.cluster.hierarchy import dendrogram, linkage
    data = RNG.normal(0, 1, (12, 6)); data[:6] += 2
    Z = linkage(data, "ward")
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    dendrogram(Z, ax=ax, color_threshold=0, above_threshold_color=OI["grey"], leaf_font_size=6)
    ax.set_ylabel("Distance"); title(ax, "Dendrogram")
    save(fig, "D05_dendrogram", "hierarchical clustering", "Part-of-whole")

def pow_waffle():
    fig, ax = plt.subplots(figsize=(3.2, 2.6))
    props = [55, 30, 15]; cols = [OI["blue"], OI["orange"], OI["green"]]
    grid = np.repeat(range(3), props).astype(int); RNG.shuffle(grid)
    grid = np.pad(grid, (0, 100 - len(grid)))[:100].reshape(10, 10)
    for i in range(10):
        for j in range(10):
            ax.add_patch(Rectangle((j, i), 0.9, 0.9, color=cols[grid[i, j]]))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
    ax.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=c) for c in cols],
              labels=["Approved", "Phase III", "Phase II"], fontsize=6, loc="upper center",
              bbox_to_anchor=(0.5, 1.14), ncol=3)
    title(ax, "Waffle chart")
    save(fig, "D06_waffle", "part-of-whole as unit squares", "Part-of-whole")

def pow_mosaic():
    cols = ["Male", "Female"]; rows = ["Responder", "Non-responder"]
    counts = np.array([[62, 48], [30, 70]], float)  # rows x cols
    coltot = counts.sum(0); widths = coltot / coltot.sum()
    fig, ax = plt.subplots(figsize=(3.4, 2.9)); gap = 0.01; x = 0
    for j, cw in enumerate(widths):
        heights = counts[:, j] / counts[:, j].sum(); y = 0
        for i, hh in enumerate(heights):
            ax.add_patch(Rectangle((x, y), cw - gap, hh - gap, facecolor=CYCLE[i], alpha=0.7, edgecolor="w"))
            if cw > 0.15:
                ax.text(x + cw / 2, y + hh / 2, f"{int(counts[i,j])}", ha="center", va="center", fontsize=7)
            y += hh
        ax.text(x + cw / 2, -0.04, cols[j], ha="center", fontsize=6.5)
        x += cw
    ax.legend(handles=[Rectangle((0, 0), 1, 1, color=CYCLE[i], alpha=0.7) for i in range(2)],
              labels=rows, fontsize=6, loc="upper center", bbox_to_anchor=(0.5, 1.14), ncol=2)
    ax.set_xlim(0, 1); ax.set_ylim(-0.08, 1); ax.axis("off"); title(ax, "Mosaic plot")
    save(fig, "D07_mosaic", "two categorical variables", "Part-of-whole")


# ============================================================ E. FLOW / NETWORK
def flow_sankey():
    from matplotlib.sankey import Sankey
    fig = plt.figure(figsize=(3.8, 2.8)); ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])
    Sankey(ax=ax, flows=[1.0, -0.6, -0.25, -0.15], labels=["Dose", "Absorbed", "First-pass", "Excreted"],
           orientations=[0, 0, 1, -1], trunklength=1.2, facecolor=OI["blue"],
           edgecolor="k").finish()
    for s in ax.spines.values():
        s.set_visible(False)
    title(ax, "Sankey diagram")
    save(fig, "E01_sankey", "mass/flow balance", "Flow-Network")

def flow_network():
    G = nx.karate_club_graph()
    pos = nx.spring_layout(G, seed=7)
    deg = np.array([d for _, d in G.degree()])
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=OI["grey"], width=0.6, alpha=0.6)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=deg * 12, node_color=deg, cmap=SEQ,
                           edgecolors="k", linewidths=0.4)
    ax.axis("off"); title(ax, "Network graph (spring)")
    save(fig, "E02_network", "nodes + edges, degree-scaled", "Flow-Network")

def flow_chord_arc():
    # arc diagram of a small network
    n = 10; G = nx.gnp_random_graph(n, 0.3, seed=3)
    fig, ax = plt.subplots(figsize=(3.8, 2.4))
    xs = np.arange(n)
    for u, v in G.edges():
        c = (xs[u] + xs[v]) / 2; r = abs(xs[u] - xs[v]) / 2
        th = np.linspace(0, np.pi, 40)
        ax.plot(c + r * np.cos(th), r * np.sin(th), color=OI["blue"], alpha=0.5, lw=0.8)
    ax.scatter(xs, np.zeros(n), s=40, color=OI["orange"], zorder=3, edgecolor="k", linewidth=0.4)
    for i in xs:
        ax.text(i, -0.4, f"N{i}", ha="center", fontsize=6)
    ax.set_ylim(-0.8, n / 2); ax.axis("off"); title(ax, "Arc diagram")
    save(fig, "E03_arc", "network on a line", "Flow-Network")

def flow_bipartite():
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    left = ["Drug A", "Drug B", "Drug C"]; right = ["Target 1", "Target 2", "Target 3", "Target 4"]
    ly = np.linspace(0.2, 0.8, 3); ry = np.linspace(0.15, 0.85, 4)
    edges = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3)]
    for a, b in edges:
        ax.plot([0, 1], [ly[a], ry[b]], color=OI["grey"], lw=1, alpha=0.7)
    ax.scatter([0] * 3, ly, s=120, color=OI["blue"], zorder=3)
    ax.scatter([1] * 4, ry, s=120, color=OI["orange"], zorder=3)
    for i, l in enumerate(left):
        ax.text(-0.05, ly[i], l, ha="right", fontsize=6.5)
    for i, r in enumerate(right):
        ax.text(1.05, ry[i], r, ha="left", fontsize=6.5)
    ax.set_xlim(-0.4, 1.4); ax.axis("off"); title(ax, "Bipartite graph")
    save(fig, "E04_bipartite", "two-set relationships", "Flow-Network")

def flow_adjacency():
    G = nx.gnp_random_graph(14, 0.25, seed=5); A = nx.to_numpy_array(G)
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    ax.imshow(A, cmap="Greys", interpolation="nearest")
    ax.set_xlabel("Node"); ax.set_ylabel("Node"); title(ax, "Adjacency matrix")
    save(fig, "E05_adjacency", "network as a matrix", "Flow-Network")


# ============================================================ F. TIME / EVOLUTION
def time_line():
    t = np.linspace(0, 10, 100)
    fig, ax = plt.subplots(figsize=(3.5, 2.6))
    ax.plot(t, np.sin(t) * np.exp(-0.1 * t), color=OI["blue"])
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Signal"); title(ax, "Line chart")
    save(fig, "F01_line", "single series over time", "Time-series")

def time_multiline():
    t = np.linspace(0, 24, 50)
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    for i, (k, lab) in enumerate([(0.3, "A"), (0.18, "B"), (0.12, "C")]):
        ax.plot(t, 100 * (1 - np.exp(-k * t)), color=CYCLE[i], label=lab)
    ax.legend(); ax.set_xlabel("Time (h)"); ax.set_ylabel("Release (%)"); title(ax, "Multi-series line")
    save(fig, "F02_multiline", "several series", "Time-series")

def time_ci_band():
    t = np.linspace(0, 24, 25)
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    for name, c, k in [("Nanocrystal", OI["orange"], 0.35), ("Suspension", OI["blue"], 0.15)]:
        mu = 100 * (1 - np.exp(-k * t)); sd = 4 + 0.06 * mu
        ax.plot(t, mu, color=c, label=name); ax.fill_between(t, mu - sd, mu + sd, color=c, alpha=0.18, linewidth=0)
    ax.legend(loc="lower right"); ax.set_xlabel("Time (h)"); ax.set_ylabel("Absorbed (%)")
    title(ax, "Line + s.d. ribbon")
    save(fig, "F03_line_ci", "trajectory + uncertainty", "Time-series")

def time_area():
    t = np.arange(30); y = np.abs(RNG.normal(5, 2, 30)).cumsum() * 0.2
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    ax.fill_between(t, y, color=OI["sky"], alpha=0.6); ax.plot(t, y, color=OI["blue"])
    ax.set_xlabel("Day"); ax.set_ylabel("Cumulative"); title(ax, "Area chart")
    save(fig, "F04_area", "magnitude over time", "Time-series")

def time_stream():
    t = np.arange(40); ys = np.abs(RNG.normal(0, 1, (5, 40)))
    ys = np.array([np.convolve(y, np.ones(5) / 5, "same") for y in ys]) + 0.5
    fig, ax = plt.subplots(figsize=(3.7, 2.5))
    ax.stackplot(t, ys, colors=CYCLE[:5], baseline="wiggle", edgecolor="w", linewidth=0.2)
    ax.set_xlabel("Time"); ax.set_yticks([]); title(ax, "Streamgraph")
    save(fig, "F05_streamgraph", "flowing composition", "Time-series")

def time_waterfall():
    t = np.linspace(0, 120, 100)
    fig, ax = plt.subplots(figsize=(3.6, 3.0)); offset = 0; cmap = mpl.colormaps[SEQ]
    for i, k in enumerate(np.linspace(0.02, 0.09, 7)):
        rel = 100 * (1 - np.exp(-k * t)) + offset
        ax.plot(t, rel, color=cmap(i / 6), lw=1.2); ax.fill_between(t, offset, rel, color=cmap(i / 6), alpha=0.1)
        offset += 22
    ax.set_yticks([]); ax.set_xlabel("Time (min)"); ax.set_ylabel("Release (offset per formulation)")
    title(ax, "Waterfall")
    save(fig, "F06_waterfall", "family of profiles", "Time-series")

def time_candlestick():
    n = 30; close = 100 + np.cumsum(RNG.normal(0, 2, n)); openp = close + RNG.normal(0, 1, n)
    high = np.maximum(openp, close) + RNG.uniform(0, 2, n); low = np.minimum(openp, close) - RNG.uniform(0, 2, n)
    fig, ax = plt.subplots(figsize=(3.8, 2.6))
    for i in range(n):
        up = close[i] >= openp[i]; c = OI["green"] if up else OI["vermillion"]
        ax.plot([i, i], [low[i], high[i]], color=c, lw=0.7)
        ax.add_patch(Rectangle((i - 0.3, min(openp[i], close[i])), 0.6, abs(close[i] - openp[i]) + 1e-6,
                               facecolor=c, edgecolor=c))
    ax.set_xlabel("Session"); ax.set_ylabel("Price"); title(ax, "Candlestick (OHLC)")
    save(fig, "F07_candlestick", "financial time-series", "Time-series")

def time_spectrogram():
    fs = 500; t = np.arange(0, 4, 1 / fs)
    sig = np.sin(2 * np.pi * (5 + 20 * t) * t) + 0.3 * RNG.normal(0, 1, len(t))
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    Pxx, freqs, bins, im = ax.specgram(sig, NFFT=128, Fs=fs, noverlap=100, cmap=SEQ)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Power (dB)")
    ax.set_xlabel("Time (s)"); ax.set_ylabel("Frequency (Hz)"); ax.set_ylim(0, 120)
    title(ax, "Spectrogram")
    save(fig, "F08_spectrogram", "time–frequency (chirp)", "Time-series")

def time_decomposition():
    t = np.arange(120); period = 12
    series = 10 + 0.05 * t + 3 * np.sin(2 * np.pi * t / period) + RNG.normal(0, 0.6, 120)
    # centered moving-average trend (pure numpy)
    trend = np.full(120, np.nan); h = period // 2
    for i in range(h, 120 - h):
        trend[i] = series[i - h:i + h + 1].mean()
    detr = series - trend
    seasonal = np.zeros(120)
    for ph in range(period):
        vals = detr[ph::period]; seasonal[ph::period] = np.nanmean(vals)
    seasonal -= np.nanmean(seasonal)
    resid = series - trend - seasonal
    fig, axs = plt.subplots(4, 1, figsize=(3.8, 3.8), sharex=True)
    for ax, comp, lab in zip(axs, [series, trend, seasonal, resid],
                             ["Observed", "Trend", "Seasonal", "Residual"]):
        ax.plot(t, comp, color=OI["blue"], lw=1); ax.set_ylabel(lab, fontsize=6.5)
    axs[-1].set_xlabel("Month"); fig.suptitle("Seasonal decomposition", x=0.13, y=0.95, ha="left", fontsize=8.5)
    save(fig, "F09_decomposition", "trend + seasonal + residual", "Time-series")

def time_step():
    t = np.arange(15); y = np.cumsum(RNG.integers(-2, 3, 15))
    fig, ax = plt.subplots(figsize=(3.4, 2.5))
    ax.step(t, y, where="post", color=OI["purple"]); ax.scatter(t, y, s=12, color=OI["purple"], zorder=3)
    ax.set_xlabel("Event"); ax.set_ylabel("State"); title(ax, "Step function")
    save(fig, "F10_step", "piecewise-constant series", "Time-series")


# ============================================================ G. SCIENTIFIC / BIOMEDICAL
def sci_dose_response():
    def hill(x, b, top, ec, h):
        return b + (top - b) / (1 + (ec / x) ** h)
    dose = np.logspace(-2, 2, 9); y = hill(dose, 2, 98, 1.5, 1.2) + RNG.normal(0, 4, 9)
    p, _ = curve_fit(hill, dose, y, p0=[0, 100, 1, 1], maxfev=10000)
    xx = np.logspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(3.4, 2.8))
    ax.plot(xx, hill(xx, *p), color=OI["orange"]); ax.scatter(dose, y, s=20, facecolor="w", edgecolor=OI["orange"], linewidth=1)
    ax.axvline(p[2], ls="--", lw=0.8, color=OI["grey"]); ax.text(p[2] * 1.2, 8, f"EC₅₀={p[2]:.2f}", fontsize=7)
    ax.set_xscale("log"); ax.set_xlabel("Conc. (µM)"); ax.set_ylabel("Inhibition (%)"); title(ax, "Dose–response (Hill)")
    save(fig, "G01_dose_response", "sigmoidal fit", "Scientific")

def sci_kaplan_meier():
    def km(times, ev):
        t = np.sort(times); e = ev[np.argsort(times)]; s = 1; xs = [0]; ys = [1]
        for ti in np.unique(t):
            d = np.sum((t == ti) & (e == 1)); at = np.sum(t >= ti)
            if at: s *= 1 - d / at
            xs += [ti, ti]; ys += [ys[-1], s]
        return np.array(xs), np.array(ys)
    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    for name, c, sc in [("Vehicle", OI["grey"], 8), ("Free", OI["blue"], 14), ("NP", OI["orange"], 24)]:
        t = RNG.exponential(sc, 30); cen = RNG.uniform(0, 40, 30)
        obs = np.minimum(t, cen); ev = (t <= cen).astype(int)
        xs, ys = km(np.clip(obs, 0, 40), ev); ax.step(xs, ys, where="post", color=c, label=name)
    ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival"); ax.set_ylim(0, 1.02); ax.legend()
    ax.text(0.5, 0.1, "log-rank P < 0.001", transform=ax.transAxes, fontsize=7); title(ax, "Kaplan–Meier")
    save(fig, "G02_kaplan_meier", "time-to-event", "Scientific")

def sci_forest():
    studies = [f"Study {i}" for i in range(1, 8)] + ["Pooled"]
    est = np.r_[RNG.normal(0.7, 0.2, 7), [0.72]]; lo = est - RNG.uniform(0.1, 0.3, 8); hi = est + RNG.uniform(0.1, 0.3, 8)
    fig, ax = plt.subplots(figsize=(3.6, 3.0)); y = np.arange(8)[::-1]
    ax.errorbar(est[:-1], y[:-1], xerr=[est[:-1] - lo[:-1], hi[:-1] - est[:-1]], fmt="s", color=OI["blue"], capsize=2, markersize=5)
    ax.plot([lo[-1], est[-1], hi[-1]], [y[-1]] * 3, "D-", color=OI["orange"], markersize=6)
    ax.axvline(1, ls="--", color=OI["grey"], lw=0.8)
    ax.set_yticks(y); ax.set_yticklabels(studies, fontsize=6.5); ax.set_xlabel("Odds ratio (95% CI)")
    title(ax, "Forest plot (meta-analysis)")
    save(fig, "G03_forest", "effect sizes across studies", "Scientific")

def sci_pk():
    t = np.array([0.25, 0.5, 1, 2, 4, 6, 8, 12, 24])
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    for name, c, (ka, ke) in [("IR ref", OI["grey"], (1.5, 0.25)), ("Nano", OI["orange"], (0.7, 0.12))]:
        conc = 100 * ka / (ka - ke) * (np.exp(-ke * t) - np.exp(-ka * t))
        ax.semilogy(t, conc * np.exp(RNG.normal(0, 0.05, len(t))), "o-", color=c, label=name, markersize=4)
    ax.set_xlabel("Time (h)"); ax.set_ylabel("Conc. (ng/mL)"); ax.legend(); title(ax, "Semi-log PK profile")
    save(fig, "G04_pk_semilog", "geometric mean, log axis", "Scientific")

def sci_dissolution():
    t = np.array([0, 5, 10, 15, 30, 45, 60, 90, 120])
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    for name, c, k in [("RLD", OI["grey"], 0.06), ("Test", OI["orange"], 0.055)]:
        rel = 100 * (1 - np.exp(-k * t)); ax.errorbar(t, rel, yerr=2 + 0.04 * rel, fmt="o-", color=c, label=name, capsize=2, markersize=4)
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Released (%)"); ax.set_ylim(0, 105); ax.legend(loc="lower right")
    ax.text(0.55, 0.2, "f2 = 62", transform=ax.transAxes, fontsize=7.5); title(ax, "Dissolution profile")
    save(fig, "G05_dissolution", "profile + f2", "Scientific")

def sci_roc():
    fig, ax = plt.subplots(figsize=(3.2, 3.1))
    for name, c, sep in [("Model A", OI["orange"], 1.4), ("Model B", OI["blue"], 0.8), ("Model C", OI["green"], 0.4)]:
        lab = RNG.integers(0, 2, 200); sc = RNG.normal(sep * lab, 1)
        order = np.argsort(-sc); l = lab[order]; tpr = np.r_[0, np.cumsum(l) / l.sum()]; fpr = np.r_[0, np.cumsum(1 - l) / (1 - l).sum()]
        ax.plot(fpr, tpr, color=c, label=f"{name} ({np.trapezoid(tpr, fpr):.2f})")
    ax.plot([0, 1], [0, 1], "--", color=OI["grey"], lw=0.8); ax.set_aspect("equal")
    ax.set_xlabel("FPR"); ax.set_ylabel("TPR"); ax.legend(loc="lower right"); title(ax, "ROC curves")
    save(fig, "G06_roc", "classifier discrimination", "Scientific")

def sci_pr():
    fig, ax = plt.subplots(figsize=(3.2, 3.0))
    for name, c, sep in [("Model A", OI["orange"], 1.4), ("Model B", OI["blue"], 0.7)]:
        lab = RNG.integers(0, 2, 300); sc = RNG.normal(sep * lab, 1); order = np.argsort(-sc); l = lab[order]
        tp = np.cumsum(l); prec = tp / np.arange(1, len(l) + 1); rec = tp / l.sum()
        ax.plot(rec, prec, color=c, label=name)
    ax.set_xlabel("Recall"); ax.set_ylabel("Precision"); ax.legend(); title(ax, "Precision–recall")
    save(fig, "G07_pr_curve", "PR for imbalanced classes", "Scientific")

def sci_calibration():
    p = RNG.uniform(0, 1, 500); y = (RNG.uniform(0, 1, 500) < p).astype(int)
    bins = np.linspace(0, 1, 11); idx = np.digitize(p, bins) - 1
    xb = [p[idx == i].mean() if np.any(idx == i) else np.nan for i in range(10)]
    yb = [y[idx == i].mean() if np.any(idx == i) else np.nan for i in range(10)]
    fig, ax = plt.subplots(figsize=(3.1, 3.0))
    ax.plot([0, 1], [0, 1], "--", color=OI["grey"], lw=0.8)
    ax.plot(xb, yb, "o-", color=OI["blue"]); ax.set_aspect("equal")
    ax.set_xlabel("Predicted probability"); ax.set_ylabel("Observed frequency"); title(ax, "Calibration curve")
    save(fig, "G08_calibration", "probability reliability", "Scientific")

def sci_confusion():
    classes = ["Amorphous", "Crystalline", "Mixed"]; C = np.array([[46, 3, 1], [2, 44, 4], [3, 5, 42]])
    Cn = C / C.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    im = ax.imshow(Cn, cmap="Blues", vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{C[i,j]}", ha="center", va="center", fontsize=8, color="white" if Cn[i, j] > 0.5 else "k")
    ax.set_xticks(range(3)); ax.set_xticklabels(classes, fontsize=6.5); ax.set_yticks(range(3)); ax.set_yticklabels(classes, fontsize=6.5)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True"); title(ax, "Confusion matrix")
    save(fig, "G09_confusion", "per-class classifier behaviour", "Scientific")

def sci_volcano():
    n = 2000; lfc = RNG.normal(0, 1.2, n); pval = 10 ** (-np.abs(RNG.normal(0, 1.5, n)) * (1 + np.abs(lfc) / 3))
    sig = (np.abs(lfc) > 1) & (pval < 0.05)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    ax.scatter(lfc[~sig], -np.log10(pval[~sig]), s=5, color=OI["grey"], alpha=0.5)
    up = sig & (lfc > 0); dn = sig & (lfc < 0)
    ax.scatter(lfc[up], -np.log10(pval[up]), s=6, color=OI["orange"], label="Up")
    ax.scatter(lfc[dn], -np.log10(pval[dn]), s=6, color=OI["blue"], label="Down")
    ax.axhline(-np.log10(0.05), ls="--", color="k", lw=0.6); ax.axvline(1, ls="--", color="k", lw=0.6); ax.axvline(-1, ls="--", color="k", lw=0.6)
    ax.set_xlabel("log₂ fold-change"); ax.set_ylabel("−log₁₀ P"); ax.legend(); title(ax, "Volcano plot")
    save(fig, "G10_volcano", "differential expression", "Scientific")

def sci_manhattan():
    chroms = 12; pos = []; pv = []; ch = []
    for c in range(chroms):
        k = 200; pos.append(np.arange(k) + c * 220); ch.append(np.full(k, c))
        base = RNG.uniform(0.1, 1, k);
        if c in (3, 7): base[RNG.integers(0, k, 5)] *= 0.001
        pv.append(base)
    pos = np.concatenate(pos); pv = np.concatenate(pv); ch = np.concatenate(ch)
    fig, ax = plt.subplots(figsize=(4.2, 2.6))
    for c in range(chroms):
        m = ch == c; ax.scatter(pos[m], -np.log10(pv[m]), s=3, color=OI["blue"] if c % 2 else OI["sky"])
    ax.axhline(-np.log10(5e-8 * 1e5), ls="--", color=OI["vermillion"], lw=0.8)
    ax.set_xlabel("Genomic position"); ax.set_ylabel("−log₁₀ P"); ax.set_xticks([]); title(ax, "Manhattan plot")
    save(fig, "G11_manhattan", "GWAS-style genome scan", "Scientific")

def sci_ma():
    n = 1500; A = RNG.uniform(2, 14, n); M = RNG.normal(0, 0.6, n); M[A > 10] += RNG.normal(0, 1.2, np.sum(A > 10))
    fig, ax = plt.subplots(figsize=(3.5, 2.7))
    ax.scatter(A, M, s=5, color=OI["grey"], alpha=0.5); ax.axhline(0, color=OI["orange"], lw=1)
    ax.set_xlabel("A (mean log-intensity)"); ax.set_ylabel("M (log-ratio)"); title(ax, "MA plot")
    save(fig, "G12_ma_plot", "intensity-dependent ratio", "Scientific")

def sci_tornado():
    params = ["Diffusivity", "Porosity", "Partition K", "Tortuosity", "Solubility", "Film"]
    low = np.array([-22, -15, -12, -8, -6, -3]); high = np.array([25, 14, 16, 7, 5, 4])
    o = np.argsort(np.abs(high) + np.abs(low)); params = [params[i] for i in o]; low, high = low[o], high[o]
    fig, ax = plt.subplots(figsize=(3.8, 2.8)); y = np.arange(len(params))
    ax.barh(y, high, color=OI["orange"], edgecolor="k", linewidth=0.4, label="+10%")
    ax.barh(y, low, color=OI["blue"], edgecolor="k", linewidth=0.4, label="−10%")
    ax.axvline(0, color="k", lw=0.8); ax.set_yticks(y); ax.set_yticklabels(params, fontsize=6.5)
    ax.set_xlabel("Δ AUC (%)"); ax.legend(loc="lower right"); title(ax, "Tornado sensitivity")
    save(fig, "G13_tornado", "ranked parameter influence", "Scientific")

def sci_scree_pca():
    X = np.vstack([RNG.normal(0, 1, (40, 10)) * 0.6 + m for m in
                   ([-3, 0] + [0] * 8, [3, 0] + [0] * 8, [0, 4] + [0] * 8)])
    lab = np.repeat([0, 1, 2], 40); Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False); var = S**2 / np.sum(S**2); sc = U * S
    fig, axs = plt.subplots(1, 2, figsize=(6.2, 2.7))
    axs[0].plot(np.arange(1, 11), var * 100, "o-", color="k", markersize=4); axs[0].set_yscale("log")
    axs[0].set_xlabel("Component"); axs[0].set_ylabel("Variance (%)"); title(axs[0], "Scree")
    for k in range(3):
        m = lab == k; axs[1].scatter(sc[m, 0], sc[m, 1], s=16, color=CYCLE[k], label=f"C{k+1}", edgecolor="k", linewidth=0.3)
    axs[1].set_xlabel(f"PC1 ({var[0]*100:.0f}%)"); axs[1].set_ylabel(f"PC2 ({var[1]*100:.0f}%)"); axs[1].legend(); title(axs[1], "PCA scores")
    fig.tight_layout()
    save(fig, "G14_scree_pca", "rank + structure", "Scientific")

def sci_biplot():
    X = RNG.normal(0, 1, (60, 4)); X[:, 1] += X[:, 0]
    Xc = X - X.mean(0); U, S, Vt = np.linalg.svd(Xc, full_matrices=False); sc = U * S; var = S**2 / S.sum()**2
    fig, ax = plt.subplots(figsize=(3.4, 3.1))
    ax.scatter(sc[:, 0], sc[:, 1], s=14, color=OI["grey"], alpha=0.6)
    for i, lab in enumerate(["size", "zeta", "PDI", "EE"]):
        ax.arrow(0, 0, Vt[0, i] * 3, Vt[1, i] * 3, color=OI["orange"], head_width=0.1, lw=1.2)
        ax.text(Vt[0, i] * 3.2, Vt[1, i] * 3.2, lab, fontsize=6.5, color=OI["vermillion"])
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2"); title(ax, "PCA biplot")
    save(fig, "G15_biplot", "scores + loadings", "Scientific")

def sci_embedding():
    cl = [RNG.normal(m, 0.6, (60, 2)) for m in ([0, 0], [4, 3], [-3, 4], [2, -4])]
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    for i, c in enumerate(cl):
        ax.scatter(c[:, 0], c[:, 1], s=12, color=CYCLE[i], alpha=0.75, edgecolor="k", linewidth=0.2, label=f"Type {i+1}")
    ax.set_xlabel("UMAP-1"); ax.set_ylabel("UMAP-2"); ax.legend(fontsize=6, markerscale=0.8); title(ax, "Embedding (UMAP-style)")
    save(fig, "G16_embedding", "nonlinear low-dim embedding", "Scientific")

def sci_stem():
    freqs = np.arange(1, 16); amp = np.abs(RNG.normal(0, 1, 15)); amp[[2, 6, 10]] += 3
    fig, ax = plt.subplots(figsize=(3.5, 2.5))
    ax.stem(freqs, amp, linefmt=OI["blue"], markerfmt="o", basefmt=" ")
    ax.set_xlabel("Mode"); ax.set_ylabel("Coefficient"); title(ax, "Stem (sparse spectrum)")
    save(fig, "G17_stem", "discrete/sparse coefficients", "Scientific")

def sci_bifurcation():
    rs = np.linspace(2.5, 4.0, 800); fig, ax = plt.subplots(figsize=(3.8, 2.8))
    for r in rs:
        x = 0.5
        for _ in range(200):
            x = r * x * (1 - x)
        xs = []
        for _ in range(80):
            x = r * x * (1 - x); xs.append(x)
        ax.plot([r] * 80, xs, ",", color=OI["black"], alpha=0.25, markersize=0.3)
    ax.set_xlabel("r"); ax.set_ylabel("x*"); title(ax, "Bifurcation diagram")
    save(fig, "G18_bifurcation", "route to chaos (logistic map)", "Scientific")

def sci_gci():
    N = np.array([1e3, 4e3, 1.6e4, 6.4e4, 2.56e5]); err = 0.8 * (N ** (-0.5)) * 20
    fig, ax = plt.subplots(figsize=(3.3, 2.7))
    ax.loglog(N, err, "o-", color=OI["blue"]);
    ax.loglog(N, 20 * 0.8 * N ** -0.5, "--", color=OI["grey"], label="slope −1/2")
    ax.set_xlabel("Mesh cells"); ax.set_ylabel("Discretization error"); ax.legend(); title(ax, "Grid convergence (log–log)")
    save(fig, "G19_gci", "mesh-independence / order", "Scientific")

def sci_control_chart():
    n = 40; x = RNG.normal(50, 2, n); mu, sd = 50, 2
    fig, ax = plt.subplots(figsize=(3.8, 2.5))
    ax.plot(x, "o-", color=OI["blue"], markersize=4)
    for k, ls in [(0, "-"), (3, "--"), (-3, "--")]:
        ax.axhline(mu + k * sd, ls=ls, color=OI["vermillion"] if k else "k", lw=0.8)
    out = np.abs(x - mu) > 3 * sd
    ax.scatter(np.where(out)[0], x[out], s=40, facecolor="none", edgecolor=OI["vermillion"], linewidth=1.2)
    ax.set_xlabel("Sample"); ax.set_ylabel("Measurement"); title(ax, "Control chart (SPC)")
    save(fig, "G20_control_chart", "process monitoring ±3σ", "Scientific")


# ============================================================ H. 3D & FIELDS
def field_surface3d():
    x = np.linspace(-3, 3, 60); t = np.linspace(0, 3, 60); X, T = np.meshgrid(x, t)
    U = np.exp(-T * 0.6) * np.sin(2 * X) * np.exp(-0.2 * X**2)
    fig = plt.figure(figsize=(3.8, 3.1)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, T, U, cmap=SEQ, linewidth=0, rcount=60, ccount=60)
    ax.set_xlabel("x"); ax.set_ylabel("t"); ax.set_zlabel("u"); ax.view_init(28, -58); ax.tick_params(labelsize=6)
    title(ax, "3D surface")
    save(fig, "H01_surface3d", "solution field u(x,t)", "3D-Fields")

def field_wireframe():
    x = np.linspace(-3, 3, 30); y = np.linspace(-3, 3, 30); X, Y = np.meshgrid(x, y); Z = np.exp(-(X**2 + Y**2) / 4)
    fig = plt.figure(figsize=(3.6, 3.0)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_wireframe(X, Y, Z, color=OI["blue"], linewidth=0.5); ax.tick_params(labelsize=6)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z"); title(ax, "3D wireframe")
    save(fig, "H02_wireframe", "surface as mesh", "3D-Fields")

def field_scatter3d():
    cl = [RNG.normal(m, 0.7, (40, 3)) for m in ([0, 0, 0], [3, 3, 2], [-2, 2, -3])]
    fig = plt.figure(figsize=(3.6, 3.0)); ax = fig.add_subplot(111, projection="3d")
    for i, c in enumerate(cl):
        ax.scatter(c[:, 0], c[:, 1], c[:, 2], s=12, color=CYCLE[i], edgecolor="k", linewidth=0.2)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z"); ax.tick_params(labelsize=6); title(ax, "3D scatter")
    save(fig, "H03_scatter3d", "three continuous variables", "3D-Fields")

def field_contour():
    x = np.linspace(-3, 3, 100); y = np.linspace(-3, 3, 100); X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y) + 0.3 * (X**2 + Y**2) ** 0.5
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    cs = ax.contour(X, Y, Z, levels=12, cmap=SEQ); ax.clabel(cs, inline=True, fontsize=5)
    ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_aspect("equal"); title(ax, "Contour lines")
    save(fig, "H04_contour", "iso-lines of a field", "3D-Fields")

def field_contourf():
    x = np.linspace(0, 1, 120); y = np.linspace(0, 1, 120); X, Y = np.meshgrid(x, y)
    Z = np.exp(-((X - 0.4)**2 + (Y - 0.6)**2) / 0.03) + 0.6 * np.exp(-((X - 0.7)**2 + (Y - 0.3)**2) / 0.05)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    cf = ax.contourf(X, Y, Z, levels=15, cmap=SEQ)
    fig.colorbar(cf, ax=ax, fraction=0.046, pad=0.04, label="Magnitude")
    ax.set_xlabel("x/L"); ax.set_ylabel("y/L"); ax.set_aspect("equal"); title(ax, "Filled contour")
    save(fig, "H05_contourf", "field with colorbar", "3D-Fields")

def field_heatmap():
    x = np.linspace(0, 1, 120); y = np.linspace(0, 1, 120); X, Y = np.meshgrid(x, y)
    F = np.exp(-((X - 0.35)**2 + (Y - 0.6)**2) / 0.03) + 0.6 * np.exp(-((X - 0.7)**2 + (Y - 0.3)**2) / 0.05)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    im = ax.pcolormesh(X, Y, F, cmap=SEQ, shading="auto")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Velocity (m/s)")
    ax.set_xlabel("x/L"); ax.set_ylabel("y/L"); ax.set_aspect("equal"); title(ax, "Field heatmap")
    save(fig, "H06_field_heatmap", "2D field, viridis (never jet)", "3D-Fields")

def field_quiver():
    x = np.linspace(-2, 2, 16); y = np.linspace(-2, 2, 16); X, Y = np.meshgrid(x, y)
    U = -Y; V = X; M = np.hypot(U, V)
    fig, ax = plt.subplots(figsize=(3.3, 3.0))
    q = ax.quiver(X, Y, U, V, M, cmap=SEQ, scale=40)
    fig.colorbar(q, ax=ax, fraction=0.046, pad=0.04, label="|v|")
    ax.set_aspect("equal"); ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Quiver (vector field)")
    save(fig, "H07_quiver", "vector field arrows", "3D-Fields")

def field_streamplot():
    x = np.linspace(-3, 3, 60); y = np.linspace(-3, 3, 60); X, Y = np.meshgrid(x, y)
    U = -1 - X**2 + Y; V = 1 + X - Y**2; speed = np.hypot(U, V)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    strm = ax.streamplot(X, Y, U, V, color=speed, cmap=SEQ, linewidth=0.8, density=1.1)
    fig.colorbar(strm.lines, ax=ax, fraction=0.046, pad=0.04, label="Speed")
    ax.set_aspect("equal"); ax.set_xlabel("x"); ax.set_ylabel("y"); title(ax, "Streamplot")
    save(fig, "H08_streamplot", "flow streamlines", "3D-Fields")

def field_polar():
    th = np.linspace(0, 2 * np.pi, 200)
    fig, ax = plt.subplots(figsize=(3.2, 3.2), subplot_kw=dict(polar=True))
    for k, c in zip([2, 3, 4], [OI["blue"], OI["orange"], OI["green"]]):
        ax.plot(th, np.abs(np.cos(k * th)), color=c, lw=1.2)
    ax.set_title("Polar plot (rose)", va="bottom", fontsize=8.5)
    save(fig, "H09_polar", "periodic / directional data", "3D-Fields")

def field_ternary():
    # simple ternary scatter via barycentric transform
    pts = RNG.dirichlet([2, 2, 2], 80)
    def to_xy(p):
        return p[:, 1] + p[:, 2] / 2, p[:, 2] * np.sqrt(3) / 2
    x, y = to_xy(pts)
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    tri = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3) / 2], [0, 0]])
    ax.plot(tri[:, 0], tri[:, 1], color="k", lw=0.8)
    sc = ax.scatter(x, y, s=18, c=pts[:, 0], cmap=SEQ, edgecolor="k", linewidth=0.2)
    ax.text(-0.03, -0.03, "A", fontsize=8); ax.text(1.0, -0.03, "B", fontsize=8); ax.text(0.5, 0.9, "C", fontsize=8)
    ax.set_aspect("equal"); ax.axis("off"); title(ax, "Ternary plot")
    save(fig, "H10_ternary", "3-component composition", "3D-Fields")


# ============================================================ I. SPECIALIZED / MULTI-PANEL
def spec_multipanel():
    fig, axs = plt.subplots(2, 2, figsize=(5.2, 4.0))
    t = np.linspace(0, 10, 100)
    axs[0, 0].plot(t, np.sin(t), color=OI["blue"]); title(axs[0, 0], "")
    d = [RNG.normal(m, 4, 8) for m in (20, 35)]
    axs[0, 1].bar([0, 1], [np.mean(x) for x in d], yerr=[np.std(x) for x in d], color=[OI["grey"], OI["orange"]], edgecolor="k", linewidth=0.5)
    for i, x in enumerate(d):
        axs[0, 1].scatter(RNG.normal(i, 0.05, 8), x, s=10, color="k", zorder=3)
    axs[0, 1].set_xticks([0, 1]); axs[0, 1].set_xticklabels(["Ctrl", "Tx"])
    xx = RNG.uniform(0, 10, 50); axs[1, 0].scatter(xx, 2 * xx + RNG.normal(0, 3, 50), s=12, color=OI["green"], alpha=0.7)
    M = RNG.normal(0, 1, (6, 6)); im = axs[1, 1].imshow(M, cmap=DIV, vmin=-2, vmax=2)
    for ax, lab in zip(axs.ravel(), "abcd"):
        ax.text(-0.18, 1.08, lab, transform=ax.transAxes, fontsize=11, fontweight="bold")
    fig.tight_layout()
    save(fig, "I01_multipanel_abc", "composed figure with a/b/c labels", "Specialized")

def spec_small_multiples():
    fig, axs = plt.subplots(2, 4, figsize=(6.4, 3.0), sharex=True, sharey=True)
    t = np.linspace(0, 24, 30)
    for i, ax in enumerate(axs.ravel()):
        k = 0.05 + i * 0.02; ax.plot(t, 100 * (1 - np.exp(-k * t)), color=CYCLE[i % len(CYCLE)])
        ax.set_title(f"F{i+1}", fontsize=7, loc="left")
    fig.supxlabel("Time (h)", fontsize=8); fig.supylabel("Release (%)", fontsize=8)
    fig.suptitle("Small multiples (shared axes)", x=0.13, ha="left", fontsize=8.5); fig.tight_layout()
    save(fig, "I02_small_multiples", "one grammar, many panels", "Specialized")

def spec_annotated_heatmap():
    M = RNG.uniform(0, 100, (6, 6))
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    im = ax.imshow(M, cmap=SEQ)
    for i in range(6):
        for j in range(6):
            ax.text(j, i, f"{M[i,j]:.0f}", ha="center", va="center", fontsize=6, color="white" if M[i, j] < 50 else "k")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Value")
    ax.set_xticks(range(6)); ax.set_yticks(range(6)); title(ax, "Annotated heatmap")
    save(fig, "I03_annotated_heatmap", "matrix with cell values", "Specialized")

def spec_horizon():
    t = np.arange(120); y = np.cumsum(RNG.normal(0, 1, 120))
    fig, ax = plt.subplots(figsize=(4.0, 1.6))
    bands = [OI["blue"], OI["sky"], OI["orange"], OI["vermillion"]]
    base = 0; step = (y.max() - y.min()) / 4
    for i in range(4):
        ax.fill_between(t, np.clip(y - (y.min() + i * step), 0, step), color=bands[i], alpha=0.8)
    ax.set_yticks([]); ax.set_xlabel("Time"); title(ax, "Horizon chart")
    save(fig, "I04_horizon", "dense time-series in little height", "Specialized")

def spec_upset():
    # simplified UpSet: intersection sizes as bars + a dot matrix below
    sets = ["A", "B", "C"]; combos = [("A",), ("B",), ("C",), ("A", "B"), ("A", "C"), ("B", "C"), ("A", "B", "C")]
    sizes = [120, 90, 70, 45, 38, 30, 22]
    fig, (axb, axm) = plt.subplots(2, 1, figsize=(3.8, 3.0), gridspec_kw=dict(height_ratios=[2, 1], hspace=0.05), sharex=True)
    axb.bar(range(len(combos)), sizes, color=OI["blue"], edgecolor="k", linewidth=0.4)
    axb.set_ylabel("Intersection size"); axb.set_title("UpSet-style intersections", loc="left", fontsize=8.5)
    for i, combo in enumerate(combos):
        for j, s in enumerate(sets):
            on = s in combo
            axm.scatter(i, j, s=40, color=OI["black"] if on else "#dddddd", zorder=3)
        onj = [j for j, s in enumerate(sets) if s in combo]
        if len(onj) > 1:
            axm.plot([i, i], [min(onj), max(onj)], color=OI["black"], lw=1.2)
    axm.set_yticks(range(3)); axm.set_yticklabels(sets); axm.set_xticks([]); axm.set_ylim(-0.5, 2.5)
    for s in ["top", "right", "left", "bottom"]:
        axm.spines[s].set_visible(False)
    save(fig, "I05_upset", "many-set intersections", "Specialized")

def spec_colormap_demo():
    x = np.linspace(0, 1, 256).reshape(1, -1)
    fig, axs = plt.subplots(4, 1, figsize=(3.6, 2.2))
    for ax, cm, lab in zip(axs, ["viridis", "cividis", "Greys", "jet"],
                           ["viridis (use)", "cividis (use)", "greyscale (use)", "jet (AVOID)"]):
        ax.imshow(x, aspect="auto", cmap=cm); ax.set_yticks([]); ax.set_xticks([])
        ax.set_ylabel(lab, rotation=0, ha="right", va="center", fontsize=7)
    fig.suptitle("Colormap choice (AP12)", x=0.35, y=0.98, fontsize=8.5); fig.tight_layout()
    save(fig, "I06_colormap_demo", "perceptual uniformity, not rainbow", "Specialized")

def spec_error_band_compare():
    t = np.linspace(0, 10, 50)
    fig, ax = plt.subplots(figsize=(3.6, 2.7))
    for i, (a, c, lab) in enumerate([(1, OI["blue"], "Model"), (0.8, OI["orange"], "Data")]):
        y = a * np.sin(t) + i * 0.1; sd = 0.2 + 0.05 * np.abs(y)
        ax.plot(t, y, color=c, label=lab); ax.fill_between(t, y - sd, y + sd, color=c, alpha=0.18, linewidth=0)
    ax.legend(); ax.set_xlabel("Time"); ax.set_ylabel("Value"); title(ax, "Model vs data (bands)")
    save(fig, "I07_model_vs_data", "overlay with uncertainty", "Specialized")


REGISTRY = [
    dist_histogram_basic, dist_histogram_multiple, dist_histogram_kde, dist_hist2d, dist_hexbin,
    dist_kde_basic, dist_kde_multiple, dist_ridgeline, dist_box_grouped, dist_box_notched,
    dist_violin, dist_violin_split, dist_raincloud, dist_strip, dist_ecdf, dist_qq,
    corr_scatter, corr_scatter_groups, corr_bubble, corr_regression, corr_marginal, corr_connected,
    corr_heatmap, corr_clustermap, corr_density2d, corr_pairplot, corr_parity, corr_bland_altman,
    corr_residual, corr_loess,
    comp_bar, comp_bar_horizontal, comp_grouped_bar, comp_stacked_bar, comp_percent_stacked,
    comp_diverging_bar, comp_dot_on_bar, comp_lollipop, comp_cleveland, comp_radar, comp_parallel,
    comp_slope, comp_bump, comp_error_only,
    pow_stacked_area, pow_treemap, pow_sunburst, pow_venn, pow_dendrogram, pow_waffle, pow_mosaic,
    flow_sankey, flow_network, flow_chord_arc, flow_bipartite, flow_adjacency,
    time_line, time_multiline, time_ci_band, time_area, time_stream, time_waterfall, time_candlestick,
    time_spectrogram, time_decomposition, time_step,
    sci_dose_response, sci_kaplan_meier, sci_forest, sci_pk, sci_dissolution, sci_roc, sci_pr,
    sci_calibration, sci_confusion, sci_volcano, sci_manhattan, sci_ma, sci_tornado, sci_scree_pca,
    sci_biplot, sci_embedding, sci_stem, sci_bifurcation, sci_gci, sci_control_chart,
    field_surface3d, field_wireframe, field_scatter3d, field_contour, field_contourf, field_heatmap,
    field_quiver, field_streamplot, field_polar, field_ternary,
    spec_multipanel, spec_small_multiples, spec_annotated_heatmap, spec_horizon, spec_upset,
    spec_colormap_demo, spec_error_band_compare,
]


def main():
    set_style()
    print(f"Generating comprehensive gallery ({len(REGISTRY)} figures, synthetic seeded data)\n")
    ok, fail = 0, []
    for fn in REGISTRY:
        try:
            fn(); ok += 1
        except Exception as e:
            fail.append((fn.__name__, repr(e)))
    from collections import Counter
    cats = Counter(c for c, _, _ in MANIFEST)
    print(f"OK: {ok}/{len(REGISTRY)}   ->  {PNG} (PNG) + {PDF} (PDF)")
    for c, n in cats.items():
        print(f"  {c:16s} {n}")
    if fail:
        print("\nFAILURES:")
        for name, err in fail:
            print(f"  ✗ {name}: {err}")
    # write manifest for the README builder
    import json
    json.dump(MANIFEST, open(os.path.join(HERE, "manifest.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
