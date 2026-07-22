#!/usr/bin/env python3
"""
generate_gallery.py — a COMPREHENSIVE gallery of publication-quality scientific figures.

~138 distinct chart types & variants across 10 categories, each from SYNTHETIC (seeded)
data and built to the data-strength-elevator publication-ready rules: one colorblind-safe
palette (Okabe-Ito), sans-serif typography, points shown on bars, exact stats, sequential
(never jet) colormaps, clean de-spined axes, vector + raster export.

Run:  python3 scripts/generate_gallery.py          (from the skill root)
Outputs PNG (300 dpi) + PDF (vector) per figure to ../examples/png and ../examples/pdf, grouped by category
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

HERE = os.path.dirname(os.path.abspath(__file__))                       # scripts/ — the build code
OUT = os.path.normpath(os.path.join(HERE, "..", "examples"))            # examples/ — the rendered gallery
PNG = os.path.join(OUT, "png"); PDF = os.path.join(OUT, "pdf")
for d in (PNG, PDF):
    os.makedirs(d, exist_ok=True)


def clean_outputs():
    """Remove stale figures so a FULL build is exactly this run.

    Only called for a full build — a filtered (`--category`) run must not delete the categories it is
    not rendering. Files only: any sub-directory is preserved, and
    os.remove() raises on a directory, which previously crashed the build mid-wipe.
    """
    for d in (PNG, PDF):
        for f in os.listdir(d):
            p = os.path.join(d, f)
            if os.path.isfile(p):
                os.remove(p)
RNG = np.random.default_rng(20260706)

OI = {"orange": "#E69F00", "blue": "#0072B2", "green": "#009E73", "purple": "#CC79A7",
      "vermillion": "#D55E00", "sky": "#56B4E9", "yellow": "#F0E442", "grey": "#999999",
      "black": "#000000"}
CYCLE = [OI["orange"], OI["blue"], OI["green"], OI["purple"], OI["vermillion"], OI["sky"], OI["yellow"]]
SEQ = "viridis"; DIV = "RdBu_r"
# The seven categorical series slots above are the only "colours" a user usually wants to swap. SEQ
# (sequential) and DIV (diverging) are perceptual colormaps — change them here if you need to, but keep
# them perceptually-uniform (never jet). Swap the categorical palette without editing code via
# `--palette` (see apply_palette / --list-palettes).

_CB_SAFE_PALETTES = {"okabe_ito", "prism_colorblind_safe"}  # per graph_catalog.json palette notes
_SERIES_SLOTS = ["orange", "blue", "green", "purple", "vermillion", "sky", "yellow"]


def _load_palettes():
    """Named categorical palettes, read from graph_catalog.json so there is one source of truth."""
    import json
    try:
        with open(os.path.join(HERE, "graph_catalog.json"), encoding="utf-8") as f:
            raw = json.load(f).get("palettes", {})
    except Exception:
        raw = {}
    out = {}
    for k, v in raw.items():
        hexes = v if isinstance(v, list) else (v.get("cycle") or v.get("hex"))
        if hexes:
            out[k] = list(hexes)
    out.setdefault("okabe_ito", CYCLE + [OI["grey"], OI["black"]])
    return out


def apply_palette(name):
    """Recolour the whole gallery to a named palette (edit-free colour choice).

    The seven categorical series slots (orange, blue, green, purple, vermillion, sky, yellow) take the
    palette's colours in order — cycled if the palette is short — so every `OI["blue"]`-style reference
    and the axes prop-cycle recolour together. grey/black stay neutral structural colours, and SEQ/DIV
    are untouched. Prints a colorblind-safety warning for any non-Okabe palette, matching the library's
    own rule that a colour cycle should stay colorblind-safe unless you deliberately opt out.
    """
    global CYCLE
    pals = _load_palettes()
    if name not in pals:
        raise SystemExit(f"Unknown palette '{name}'. Choices: {', '.join(sorted(pals))}")
    hexes = pals[name]
    for i, slot in enumerate(_SERIES_SLOTS):
        OI[slot] = hexes[i % len(hexes)]
    CYCLE = [OI[s] for s in _SERIES_SLOTS]
    set_style()
    if name not in _CB_SAFE_PALETTES:
        print(f"⚠ palette '{name}' is not verified colorblind-safe (see graph_catalog.json). "
              f"okabe_ito and prism_colorblind_safe are the safe choices.\n")

MANIFEST = []
OVERLAPS = []  # (figure_name, [(labelA, labelB), ...]) — populated by the F16 text-overlap audit

try:  # the F16 publication-ready gate (references/publication-ready-figures.md R1)
    from _figure_qc import audit_overlaps_detailed
except Exception:  # pragma: no cover - QC is advisory; never block the gallery build
    audit_overlaps_detailed = None


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
    if audit_overlaps_detailed is not None:
        try:
            hits = [h for h in audit_overlaps_detailed(fig) if h["actionable"]]
            if hits:
                OVERLAPS.append((name, hits))
        except Exception:
            pass  # a QC failure must never lose a figure
    fig.savefig(os.path.join(PNG, name + ".png"), metadata={"Software": None})
    # metadata={"CreationDate": None} strips the wall-clock timestamp matplotlib otherwise embeds in
    # every PDF, so a rebuild that changed nothing visual produces a byte-identical file (no diff churn).
    fig.savefig(os.path.join(PDF, name + ".pdf"), metadata={"CreationDate": None})
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
    ax.legend(ncol=3, fontsize=6, loc="upper right", bbox_to_anchor=(1.02, 1.20)); ax.set_ylabel("Percent (%)"); ax.set_ylim(0, 100)
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
              labels=["Approved", "Phase III", "Phase II"], fontsize=6, loc="upper right",
              bbox_to_anchor=(1.02, 1.18), ncol=3)
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
              labels=rows, fontsize=6, loc="upper right", bbox_to_anchor=(1.02, 1.18), ncol=2)
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
    ax.set_title("Polar plot (rose)", va="bottom", fontsize=8.5, y=1.10)
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
    fig.tight_layout(w_pad=3.0, h_pad=2.0)  # room for the panel letters in the gutters
    for ax, lab in zip(axs.ravel(), "abcd"):
        ax.text(-0.22, 1.10, lab, transform=ax.transAxes, fontsize=11, fontweight="bold")
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


# ============================================================ A. DISTRIBUTIONS (Ex1 additions)

def dist_sina():
    """Sina plot: every raw cell sits ON the violin, jittered by local density, so shape and n are both auditable."""
    conds = ["Vehicle", "Plain LNP", "PEG-LNP", "Ab-LNP"]
    n = 50
    data = [RNG.lognormal(np.log(m), s, n) for m, s in
            [(35, 0.42), (120, 0.38), (190, 0.34), (330, 0.30)]]
    fig, ax = plt.subplots(figsize=(3.7, 3.0))
    hw = 0.36
    hues = [OI["sky"], OI["blue"], OI["green"], OI["purple"]]   # no orange: vermillion median must pop
    for i, (v, c) in enumerate(zip(data, hues)):
        kde = stats.gaussian_kde(v)
        grid = np.linspace(v.min(), v.max(), 240)
        dg = kde(grid); peak = dg.max()
        ax.fill_betweenx(grid, i - dg / peak * hw, i + dg / peak * hw, facecolor=c,
                         alpha=0.30, edgecolor=c, linewidth=0.9, zorder=1)
        off = (RNG.random(n) * 2 - 1) * (kde(v) / peak) * hw * 0.88   # density-proportional jitter
        ax.scatter(i + off, v, s=5, facecolor=c, edgecolor="k", linewidth=0.25, alpha=0.9, zorder=3)
        q1, med, q3 = np.percentile(v, [25, 50, 75])
        ax.hlines(med, i - hw * 0.95, i + hw * 0.95, color=OI["vermillion"], lw=1.6, zorder=4)
        ax.hlines([q1, q3], i - hw * 0.7, i + hw * 0.7, color="k", lw=0.8, ls=(0, (2.2, 1.6)), zorder=4)
    u, p = stats.mannwhitneyu(data[3], data[2])
    fold = np.median(data[3]) / np.median(data[2])
    top = max(v.max() for v in data)
    ax.plot([2, 2, 3, 3], [top * 1.05, top * 1.12, top * 1.12, top * 1.05], lw=0.8, c="k")
    ptxt = "P < 0.0001" if p < 1e-4 else f"P = {p:.4f}"
    ax.text(2.5, top * 1.145, f"{ptxt}  ({fold:.1f}× median)", ha="center", fontsize=6.5)
    ax.set_xticks(range(4)); ax.set_xticklabels(conds)
    ax.set_xlim(-0.62, 3.62); ax.set_ylim(0, top * 1.22)
    ax.set_ylabel("Single-cell uptake (FI, a.u.)")
    ax.set_xlabel("Formulation (n = 50 cells per group)")
    title(ax, "Sina — violin + every point")
    save(fig, "A17_sina", "violin + every raw point", "Distributions")

def dist_paired_prepost():
    """Paired crossover design: each subject is one line, so the within-subject change is the visible quantity."""
    n = 34
    ref = RNG.lognormal(np.log(48), 0.26, n)                       # reference (IR) Cmax
    test = ref * RNG.lognormal(np.log(0.78), 0.28, n)              # test (MR) Cmax, same subjects
    up = test > ref
    fig, ax = plt.subplots(figsize=(3.5, 3.0))
    for a, b, u in zip(ref, test, up):
        c = OI["vermillion"] if u else OI["blue"]
        ax.plot([0, 1], [a, b], color=c, lw=0.7, alpha=0.5, zorder=2)
    bp = ax.boxplot([ref, test], positions=[0, 1], widths=0.34, patch_artist=True,
                    showfliers=False, medianprops=dict(color="k", lw=1.2),
                    boxprops=dict(linewidth=0.7), whiskerprops=dict(linewidth=0.7),
                    capprops=dict(linewidth=0.7), zorder=4)
    for box in bp["boxes"]:                       # boxes stay neutral: colour encodes direction only
        box.set(facecolor=OI["grey"], alpha=0.45, edgecolor="k")
    for el in ("boxes", "whiskers", "caps", "medians"):
        for a in bp[el]:
            a.set_zorder(4)
    w, p = stats.wilcoxon(ref, test)
    top = max(ref.max(), test.max())
    ax.plot([0, 0, 1, 1], [top * 1.05, top * 1.11, top * 1.11, top * 1.05], lw=0.8, c="k")
    ptxt = "P < 0.0001" if p < 1e-4 else f"P = {p:.4f}"
    ax.text(0.5, top * 1.135, f"Wilcoxon {ptxt}, n = {n} subjects", ha="center", fontsize=6.5)
    ax.plot([], [], color=OI["blue"], lw=1.2, label=f"Decrease (n = {int((~up).sum())})")
    ax.plot([], [], color=OI["vermillion"], lw=1.2, label=f"Increase (n = {int(up.sum())})")
    ax.legend(loc="upper right", fontsize=6, handlelength=1.4, borderpad=0.2, labelspacing=0.3)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Reference (IR)", "Test (MR)"])
    ax.set_xlim(-0.45, 1.45); ax.set_ylim(0, top * 1.42)
    ax.set_ylabel("Cmax (ng/mL)"); ax.set_xlabel("Crossover period")
    title(ax, "Paired before/after")
    save(fig, "A18_paired_prepost", "paired before/after with subject lines", "Distributions")

def dist_broken_axis():
    """Broken-axis DOT plot: the long tail is compressed without crushing the low groups, and position (not length) encodes value."""
    conds = ["Unfiltered", "5.0 µm", "1.2 µm", "0.45 µm"]
    n = 40
    data = [RNG.poisson(RNG.lognormal(np.log(lam), s, n)).astype(float)
            for lam, s in [(38, 0.95), (6.0, 1.05), (1.6, 1.15), (0.5, 1.35)]]
    xj = []
    for i, v in enumerate(data):                      # density-aware jitter -> stacked columns
        uq, ct = np.unique(v, return_counts=True)
        wide = dict(zip(uq, np.minimum(ct / 8.0, 1.0)))
        xj.append(i + (RNG.random(n) * 2 - 1) * np.array([wide[x] for x in v]) * 0.34)
    fig, (axh, axl) = plt.subplots(2, 1, sharex=True, figsize=(3.8, 3.2),
                                   gridspec_kw=dict(height_ratios=[1, 2.1], hspace=0.10))
    for ax, keep in ((axh, lambda v: v >= 15), (axl, lambda v: v <= 14)):   # split, never double-plot
        for x, v in zip(xj, data):
            m = keep(v)
            ax.scatter(x[m], v[m], s=13, facecolor=OI["grey"], edgecolor="k", linewidth=0.35,
                       alpha=0.85, zorder=2, clip_on=(ax is axl))
        for i, v in enumerate(data):
            m = v.mean(); ci = 1.96 * v.std(ddof=1) / np.sqrt(n)
            ax.errorbar(i, m, yerr=ci, fmt="_", color=OI["vermillion"], markersize=10,
                        elinewidth=1.1, capsize=2.5, markeredgewidth=1.4, zorder=4)
    axh.set_yscale("log"); axh.set_ylim(14.5, 1200)             # compressed tail segment
    axh.set_yticks([20, 50, 150, 400]); axh.set_yticklabels(["20", "50", "150", "400"])
    axh.minorticks_off()
    axl.set_ylim(-0.9, 14.5); axl.set_yticks([0, 5, 10])
    axh.spines["bottom"].set_visible(False); axh.tick_params(bottom=False, labelbottom=False)
    axl.spines["top"].set_visible(False)
    d = 0.6
    kw = dict(marker=[(-1, -d), (1, d)], markersize=5, linestyle="none",
              color="k", mec="k", mew=0.9, clip_on=False)
    axh.plot([0], [0], transform=axh.transAxes, **kw)
    axl.plot([0], [1], transform=axl.transAxes, **kw)
    u, p = stats.mannwhitneyu(data[0], np.concatenate(data[1:]))
    axh.plot([0, 0, 3, 3], [350, 520, 520, 350], lw=0.8, c="k")
    ptxt = "P < 0.0001" if p < 1e-4 else f"P = {p:.4f}"
    axh.text(1.5, 560, f"Mann-Whitney {ptxt}", ha="center", fontsize=6.5)
    axl.text(3.42, 13.8, "Upper segment compressed (log)\nDots, not bars: position encodes value (AP9)",
             ha="right", va="top", fontsize=6, color=OI["grey"], linespacing=1.35)
    axl.set_xticks(range(4)); axl.set_xticklabels(conds); axl.set_xlim(-0.62, 3.62)
    axl.set_xlabel("Filtration step (n = 40 containers)")
    fig.supylabel("Particles ≥10 µm per container", fontsize=8.5, x=0.005)
    title(axh, "Broken axis (dot plot)")
    save(fig, "A19_broken_axis", "long tail without crushing the low group", "Distributions")



# ============================================================ B. CORRELATION / RELATIONSHIP (Ex1 additions)

def corr_triangle():
    """Every signed pairwise correlation shown exactly once, with significance marked."""
    names = ["Polymer MW", "Drug load", "D50", "Span", "Porosity",
             "Zeta", "Burst 24 h", "t50 in vitro", "Cmax", "AUC 0-28 d"]
    n = 40
    # 3 latent drivers of a PLGA long-acting-injectable batch record:
    # F1 erosion propensity, F2 polymer chain length, F3 particle size
    load = np.array([
        [0.05,  0.95,  0.05],   # Polymer MW
        [0.55,  0.05,  0.35],   # Drug load
        [-0.10, 0.10,  0.92],   # D50
        [0.05, -0.05,  0.55],   # Span
        [0.90, -0.25, -0.20],   # Porosity
        [-0.45, 0.15, -0.30],   # Zeta
        [0.85, -0.35, -0.45],   # Burst 24 h
        [-0.70, 0.60,  0.55],   # t50 in vitro
        [0.80, -0.30, -0.35],   # Cmax
        [0.15,  0.55,  0.35],   # AUC 0-28 d
    ])
    z = RNG.normal(size=(n, 3))
    x = z @ load.T + 0.45 * RNG.normal(size=(n, len(names)))

    k = len(names)
    rmat = np.ones((k, k)); pmat = np.zeros((k, k))
    for i in range(k):
        for j in range(i + 1, k):
            r, p = stats.pearsonr(x[:, i], x[:, j])
            rmat[i, j] = rmat[j, i] = r
            pmat[i, j] = pmat[j, i] = p
    # strict lower triangle, re-indexed so no empty row/column is drawn
    sub_r, sub_p = rmat[1:, :-1], pmat[1:, :-1]
    mask = np.triu(np.ones_like(sub_r, bool), k=1)          # keep col <= row
    show = np.ma.masked_array(sub_r, mask)

    fig, ax = plt.subplots(figsize=(3.9, 3.15))
    cmap = plt.get_cmap(DIV).copy()
    mesh = ax.pcolormesh(show, cmap=cmap, vmin=-1, vmax=1,
                         edgecolors="white", linewidth=0.4)
    ax.set_aspect("equal"); ax.invert_yaxis()
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    ax.set_xticks(np.arange(k - 1) + 0.5); ax.set_yticks(np.arange(k - 1) + 0.5)
    ax.set_xticklabels(names[:-1], rotation=90, fontsize=6)
    ax.set_yticklabels(names[1:], fontsize=6)

    def stars(p):
        return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 5e-2 else ""

    for a in range(k - 1):
        for b in range(a + 1):
            s = stars(sub_p[a, b])
            if not s:
                continue
            shade = cmap((sub_r[a, b] + 1) / 2)
            lum = 0.299 * shade[0] + 0.587 * shade[1] + 0.114 * shade[2]
            ax.text(b + 0.5, a + 0.62, s, ha="center", va="center", fontsize=6.0,
                    color="white" if lum < 0.55 else "0.15")

    cb = fig.colorbar(mesh, ax=ax, fraction=0.046, pad=0.04, label="Pearson r")
    cb.set_ticks([-1, -0.5, 0, 0.5, 1]); cb.ax.tick_params(labelsize=6.5)
    cb.outline.set_linewidth(0.6)

    def callout(a, b, tx, ty, ha):
        r, p = sub_r[a, b], sub_p[a, b]
        ptxt = "p < 0.001" if p < 1e-3 else f"p = {p:.3f}"
        ax.annotate(f"{names[a + 1]} / {names[b]}\nr = {r:+.2f}, {ptxt}",
                    xy=(b + 0.5, a + 0.5), xytext=(tx, ty), ha=ha, va="center",
                    fontsize=6.0, color="0.15",
                    bbox=dict(boxstyle="square,pad=0.34", fc="white", ec="0.35",
                              ls="--", lw=0.6),
                    arrowprops=dict(arrowstyle="-", ls="--", lw=0.6, color="0.35",
                                    shrinkA=1, shrinkB=1))

    tri = np.where(~mask)
    vals = sub_r[tri]
    hi = int(np.argmax(vals)); lo = int(np.argmin(vals))
    callout(tri[0][hi], tri[1][hi], 4.5, 1.15, "left")
    callout(tri[0][lo], tri[1][lo], 8.9, 3.6, "right")
    ax.text(8.9, 5.5, "* p < 0.05\n** p < 0.01\n*** p < 0.001",
            ha="right", va="top", fontsize=6.0, color="0.3", linespacing=1.35)

    title(ax, "Batch-descriptor correlogram (n = 40 batches)")
    fig.tight_layout()
    save(fig, "B15_corr_triangle", "lower-triangle correlogram + significance", "Correlation")

def corr_parity_xy_err():
    """Parity with x and y error bars: agreement is quantified, divergent lots are named."""
    n_test, n_qc, n_hit = 40, 8, 6
    obs_t = RNG.uniform(90, 830, n_test)
    pred_t = obs_t * np.exp(RNG.normal(0, 0.155, n_test))
    obs_q = RNG.normal(410, 16, n_qc)
    pred_q = obs_q * np.exp(RNG.normal(0, 0.035, n_qc))
    obs_h = np.linspace(360, 860, n_hit) + RNG.normal(0, 10, n_hit)
    pred_h = obs_h * RNG.uniform(0.22, 0.42, n_hit)          # model misses these lots

    obs = np.concatenate([obs_t, obs_h]); pred = np.concatenate([pred_t, pred_h])
    xe = np.concatenate([obs_t, obs_h]) * RNG.uniform(0.06, 0.14, n_test + n_hit)
    ye = np.concatenate([pred_t, pred_h]) * RNG.uniform(0.07, 0.13, n_test + n_hit)
    xe_q = obs_q * 0.035; ye_q = pred_q * 0.03

    # agreement metrics — all computed from the plotted points, against the identity line
    def ident_r2(o, p):
        return float(1 - np.sum((p - o) ** 2) / np.sum((o - o.mean()) ** 2))

    r2_all = ident_r2(obs, pred); r2_keep = ident_r2(obs_t, pred_t)
    rmse = float(np.sqrt(np.mean((pred - obs) ** 2)))
    mdape = float(np.median(np.abs((pred - obs) / obs * 100.0)))
    fold = pred / obs
    within2 = float(np.mean((fold >= 0.5) & (fold <= 2.0)) * 100)

    fig, ax = plt.subplots(figsize=(3.6, 3.45))
    lim = (0, 1000)
    ax.plot(lim, lim, ls="--", lw=1.0, color="0.15", zorder=1, label="Identity (y = x)")
    ax.plot([0, 500], [0, 1000], ls=":", lw=0.8, color="0.55", zorder=1, label="2-fold envelope")
    ax.plot([0, 1000], [0, 500], ls=":", lw=0.8, color="0.55", zorder=1)

    ax.errorbar(obs_t, pred_t, xerr=xe[:n_test], yerr=ye[:n_test], fmt="none",
                ecolor="0.72", elinewidth=0.55, capsize=0, zorder=2)
    ax.errorbar(obs_q, pred_q, xerr=xe_q, yerr=ye_q, fmt="none",
                ecolor=OI["orange"], elinewidth=0.55, alpha=0.7, capsize=0, zorder=2)
    ax.errorbar(obs_h, pred_h, xerr=xe[n_test:], yerr=ye[n_test:], fmt="none",
                ecolor="0.55", elinewidth=0.55, capsize=0, zorder=2)
    ax.scatter(obs_t, pred_t, s=17, facecolors="none", edgecolors=OI["grey"],
               linewidths=0.8, zorder=3, label=f"Test lots (n = {n_test})")
    ax.scatter(obs_q, pred_q, s=17, facecolors="none", edgecolors=OI["orange"],
               linewidths=0.9, zorder=4, label=f"QC standard (n = {n_qc})")
    n_beyond = int(np.sum((pred_h / obs_h < 0.5) | (pred_h / obs_h > 2.0)))
    ax.scatter(obs_h, pred_h, s=20, color=OI["vermillion"], zorder=5,
               label=f"Flagged, >2-fold (n = {n_beyond})")

    # lot IDs on a clear row beneath the flagged points, plus one named callout
    lot_ids = ["L-07", "L-19", "L-22", "L-31", "L-44", "L-58"]
    lot_kind = {"L-07": "nanocrystal", "L-19": "SNEDDS", "L-22": "amorphous SD",
                "L-31": "co-crystal", "L-44": "lipid SMEDDS", "L-58": "mesoporous"}
    order = list(np.argsort(obs_h))
    for rank, idx in enumerate(order):
        ax.annotate(lot_ids[rank], xy=(obs_h[idx], pred_h[idx]),
                    xytext=(obs_h[idx], 42), fontsize=6.0, color=OI["vermillion"],
                    ha="center", va="center",
                    arrowprops=dict(arrowstyle="-", lw=0.55, color=OI["vermillion"],
                                    shrinkA=2, shrinkB=3))
    worst = int(np.argmin(pred_h / obs_h))
    wid = lot_ids[order.index(worst)]
    ax.annotate(f"{wid}: {lot_kind[wid]}\n{obs_h[worst] / pred_h[worst]:.1f}-fold under-predicted",
                xy=(obs_h[worst], pred_h[worst]), xytext=(800, 452),
                fontsize=6.0, color=OI["vermillion"], ha="center", va="center",
                linespacing=1.4,
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="none", alpha=0.9),
                arrowprops=dict(arrowstyle="-", lw=0.55, color=OI["vermillion"],
                                shrinkA=4, shrinkB=3))

    ax.text(0.035, 0.725,
            f"R$^2$ = {r2_all:.2f} vs identity\n"
            f"median abs. %PE = {mdape:.1f}%\n"
            f"{within2:.0f}% of lots within 2-fold\n"
            f"R$^2$ = {r2_keep:.2f} excluding flagged",
            transform=ax.transAxes, ha="left", va="top", fontsize=6, color="0.2",
            linespacing=1.5)

    ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect("equal")
    ax.set_xticks(np.arange(0, 1001, 250)); ax.set_yticks(np.arange(0, 1001, 250))
    ax.set_xlabel("Observed C$_{max}$ (ng mL$^{-1}$)")
    ax.set_ylabel("PBPK-predicted C$_{max}$ (ng mL$^{-1}$)")
    ax.legend(loc="upper left", fontsize=6.0, handletextpad=0.5, labelspacing=0.32,
              borderaxespad=0.2)
    title(ax, "Model validation: predicted vs observed")
    fig.tight_layout()
    save(fig, "B16_parity_xy_err", "parity with x/y error + flagged outliers", "Correlation")

def corr_grouped_regression():
    """Pooled fit and within-group fits point opposite ways — a Simpson's-paradox check."""
    # group centres ASCEND with x while every within-group slope is negative:
    # the confounder (lipid series) reverses the sign of the pooled trend
    groups = [("Series A12", 10, 0.55, -0.35, CYCLE[3]),
              ("Series A2",   9, 0.95, 1.05, CYCLE[2]),
              ("Series A3",  15, 1.45, 2.55, CYCLE[0])]
    slope_w = -1.85                                  # within-series: PEG shields uptake
    xs, ys, gid = [], [], []
    for i, (_, n, xc, yc, _) in enumerate(groups):
        xi = xc + RNG.normal(0, 0.17, n)
        yi = yc + slope_w * (xi - xc) + RNG.normal(0, 0.26, n)
        xs.append(xi); ys.append(yi); gid.append(np.full(n, i))
    x = np.concatenate(xs); y = np.concatenate(ys); g = np.concatenate(gid)
    xerr = RNG.uniform(0.025, 0.06, x.size)

    pooled = stats.linregress(x, y)
    fits = [stats.linregress(xs[i], ys[i]) for i in range(3)]

    fig, ax = plt.subplots(figsize=(5.1, 2.85))
    fig.subplots_adjust(left=0.115, right=0.605, top=0.86, bottom=0.185)
    ax.errorbar(x, y, xerr=xerr, fmt="none", ecolor="0.6", elinewidth=0.55, capsize=1.4,
                zorder=2)
    for i, (lab, _, _, _, col) in enumerate(groups):
        m = g == i
        ax.scatter(x[m], y[m], s=26, color=col, edgecolors="0.25", linewidths=0.5,
                   zorder=3)
        gx = np.linspace(xs[i].min() - 0.05, xs[i].max() + 0.05, 50)
        ax.plot(gx, fits[i].intercept + fits[i].slope * gx, color=col, ls="--", lw=1.1,
                zorder=4)
    px = np.linspace(x.min() - 0.05, x.max() + 0.05, 50)
    ax.plot(px, pooled.intercept + pooled.slope * px, color=OI["vermillion"], lw=1.7,
            zorder=5)

    ax.set_xlabel("Mean PEG surface density (chains per 100 nm$^2$)")
    ax.set_ylabel("Normalized luciferase\nexpression in HeLa (a.u.)")
    # explicit ticks INSIDE the view: matplotlib's out-of-view tick labels are never
    # drawn but still carry bboxes, and stack up in the corner under the audit
    ax.set_xlim(0.15, 1.90); ax.set_xticks(np.arange(0.25, 1.90, 0.25))
    ax.set_ylim(-1.65, 3.65); ax.set_yticks(np.arange(-1, 4, 1))
    title(ax, "Pooled vs within-series trend (n = 34 LNPs)")

    def pblock(p):
        return "p < 0.001" if p < 1e-3 else f"p = {p:.4f}"

    rows = [("Overall (n = 34)", pooled.rvalue, pooled.pvalue, pooled.slope,
             OI["vermillion"], True)]
    for i, (lab, n, _, _, col) in enumerate(groups):
        rows.append((f"{lab} (n = {n})", fits[i].rvalue, fits[i].pvalue, fits[i].slope,
                     col, False))
    ytop = [0.99, 0.735, 0.485, 0.235]
    for (lab, rv, pv, sl, col, is_pool), yy in zip(rows, ytop):
        if is_pool:
            ax.plot([1.055, 1.115], [yy - 0.028] * 2, color=col, lw=2.0,
                    transform=ax.transAxes, clip_on=False)
        else:
            ax.plot([1.085], [yy - 0.028], marker="o", ms=5.5, color=col, mec="0.25",
                    mew=0.5, transform=ax.transAxes, clip_on=False)
        ax.text(1.145, yy, f"{lab}\nr = {rv:+.3f}   {pblock(pv)}\nslope = {sl:+.2f}",
                transform=ax.transAxes, ha="left", va="top", fontsize=6,
                color=col if is_pool else "0.25", linespacing=1.4)
    # note text is DERIVED from the fitted signs, so it cannot disagree with the lines
    n_neg = int(sum(f.slope < 0 for f in fits))
    dirn = "positive" if pooled.slope > 0 else "negative"
    ax.text(0.985, 0.03,
            f"Pooled slope {pooled.slope:+.2f} is {dirn}, yet\n"
            f"{n_neg} of {len(fits)} within-series slopes are negative.",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=6.0,
            color="0.35", linespacing=1.35)
    save(fig, "B17_grouped_regression", "pooled fit + per-group r (Simpson check)", "Correlation")



# ============================================================ C. COMPARISON / RANKING (Ex1 additions)

def comp_grouped_dot_on_bar():
    """Two-factor grouped bars that still show every replicate — the AP1 fix for a plain grouped bar."""
    lines = ["MCF-7", "A549", "HepG2"]; treats = ["Free drug", "Plain NP", "Targeted NP"]
    mu = np.array([[12, 34, 68], [10, 29, 57], [14, 38, 74]], float)
    n = 6; w = 0.26
    reps = np.stack([[RNG.normal(mu[i, j], mu[i, j] * 0.11, n) for j in range(3)] for i in range(3)])
    fig, ax = plt.subplots(figsize=(4.6, 2.9))
    x = np.arange(3)
    for j, (lab, c) in enumerate(zip(treats, CYCLE)):
        pos = x + (j - 1) * 0.28
        m = reps[:, j].mean(1); sd = reps[:, j].std(1, ddof=1)
        ax.bar(pos, m, w, yerr=sd, color=c, edgecolor="k", linewidth=0.5, label=lab,
               error_kw=dict(elinewidth=0.8, capsize=2.2, ecolor="k"), zorder=2)
        for i in range(3):
            ax.scatter(RNG.normal(pos[i], 0.035, n), reps[i, j], s=6, color="k", zorder=4)
    t, p = stats.ttest_ind(reps[0, 2], reps[0, 0])
    ptxt = "P < 0.0001" if p < 1e-4 else f"P = {p:.4f}"
    ax.plot([-0.28, -0.28, 0.28, 0.28], [88, 92, 92, 88], lw=0.8, c="k")
    ax.text(0.0, 93.5, f"{ptxt}", ha="center", fontsize=6.5)
    ax.set_xticks(x); ax.set_xticklabels(lines)
    ax.set_ylim(0, 102); ax.set_xlim(-0.62, 2.62)
    ax.set_ylabel("Cellular uptake (% of dose)")
    ax.set_xlabel("Cell line (n = 6 wells per bar)")
    ax.legend(ncol=3, fontsize=6, loc="lower right", bbox_to_anchor=(1.0, 1.0),
              handlelength=1.2, columnspacing=1.0, handletextpad=0.5)
    title(ax, "Grouped dot-on-bar")
    save(fig, "C15_grouped_dot_on_bar", "two-factor bars that still show replicates", "Comparison")

def comp_dot_reference_zones():
    """One estimate per subject read against banded interpretation thresholds, so zone-crossing is direct."""
    tro = np.concatenate([RNG.lognormal(np.log(11), 0.30, 8), RNG.lognormal(np.log(22), 0.22, 4)])
    imp = np.array([False] * 8 + [True] * 4)
    ids = np.array([f"P{i:02d}" for i in range(1, 13)])
    o = np.argsort(tro); tro, imp, ids = tro[o], imp[o], ids[o]
    lo, hi = 10.0, 20.0
    xmax = max(28.0, tro.max() * 1.15)
    fig, ax = plt.subplots(figsize=(3.8, 3.1))
    y = np.arange(len(tro)); ytop = len(tro) + 0.9
    for x0, x1, fc, al in [(0, lo, "0.55", 0.18), (lo, hi, OI["green"], 0.14), (hi, xmax, "0.25", 0.20)]:
        ax.axvspan(x0, x1, color=fc, alpha=al, lw=0, zorder=0)
    ax.axvline(lo, color="k", ls=(0, (3, 2)), lw=0.8, zorder=1)
    ax.axvline(hi, color=OI["vermillion"], ls=(0, (1.2, 1.4)), lw=1.0, zorder=1)
    for lab, xc in [("Sub-\ntherapeutic", lo / 2), ("Target\nwindow", (lo + hi) / 2), ("Supra-\ntherapeutic", (hi + xmax) / 2)]:
        ax.text(xc, ytop - 0.15, lab, ha="center", va="top", fontsize=6, color="0.25", linespacing=1.3)
    for flag, c, lab in [(False, OI["blue"], "CrCl ≥ 60 mL/min"), (True, OI["vermillion"], "CrCl < 60 mL/min")]:
        s = imp == flag
        ax.scatter(tro[s], y[s], s=32, color=c, edgecolor="k", linewidth=0.4, label=lab, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(ids, fontsize=6.5)
    ax.set_ylim(-0.9, ytop); ax.set_xlim(0, xmax)
    ax.set_xlabel("Steady-state trough (mg/L)"); ax.set_ylabel("Subject (sorted by trough)")
    ax.legend(loc="lower right", fontsize=6, handletextpad=0.3, borderpad=0.4, labelspacing=0.35,
              frameon=True, facecolor="white", edgecolor="none", framealpha=0.82)
    title(ax, "Dot plot with reference zones")
    save(fig, "C16_dot_reference_zones", "estimates against banded thresholds", "Comparison")



# ============================================================ E. FLOW / NETWORK (Ex1 additions)

def flow_alluvial():
    """A 1000-unit dose stays mass-balanced while it splits through four disposition stages."""
    TOT = 1000
    stages = ["Dose", "Absorption", "First pass", "Elimination"]
    nodes = [
        [("Dose", 1000, OI["black"])],
        [("Absorbed", 640, OI["blue"]), ("Unabsorbed", 360, OI["grey"])],
        [("Systemic", 455, OI["blue"]), ("Pre-systemic", 185, OI["orange"]),
         ("Unabsorbed", 360, OI["grey"])],
        [("Renal", 250, OI["sky"]), ("Hepatic", 205, OI["green"]),
         ("Metabolite", 185, OI["orange"]), ("Faecal", 360, OI["grey"])],
    ]
    # (stage, source index, destination index, value)
    links = [(0, 0, 0, 640), (0, 0, 1, 360),
             (1, 0, 0, 455), (1, 0, 1, 185), (1, 1, 2, 360),
             (2, 0, 0, 250), (2, 0, 1, 205), (2, 1, 2, 185), (2, 2, 3, 360)]

    # --- mass-balance verification (the analytical point of the chart) ---
    for s, col in enumerate(nodes):
        assert sum(v for _, v, _ in col) == TOT, f"stage {s} mass != {TOT}"
    for s in range(len(nodes) - 1):
        assert sum(v for st, _, _, v in links if st == s) == TOT, f"link layer {s} mass != {TOT}"
        for i, (_, v, _) in enumerate(nodes[s]):
            assert sum(w for st, si, _, w in links if st == s and si == i) == v
        for j, (_, v, _) in enumerate(nodes[s + 1]):
            assert sum(w for st, _, di, w in links if st == s and di == j) == v

    MASS, GAP, SLAB = 0.75, 0.045, 0.055
    ys = []                                   # ys[stage][i] = (top, bottom)
    for col in nodes:
        top = 0.5 + (MASS + (len(col) - 1) * GAP) / 2
        row = []
        for _, v, _ in col:
            h = v / TOT * MASS
            row.append((top, top - h)); top -= h + GAP
        ys.append(row)

    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    t = np.linspace(0, 1, 90)
    smooth = 0.5 * (1 - np.cos(np.pi * t))     # C1-continuous sigmoid between stage y-positions
    out_off = [[0.0] * len(c) for c in nodes]
    in_off = [[0.0] * len(c) for c in nodes]
    for st, si, di, v in links:
        h = v / TOT * MASS
        a_t = ys[st][si][0] - out_off[st][si]; a_b = a_t - h
        b_t = ys[st + 1][di][0] - in_off[st + 1][di]; b_b = b_t - h
        out_off[st][si] += h; in_off[st + 1][di] += h
        xs = (st + SLAB / 2) + ((st + 1 - SLAB / 2) - (st + SLAB / 2)) * t
        ax.fill_between(xs, a_b + (b_b - a_b) * smooth, a_t + (b_t - a_t) * smooth,
                        color=nodes[st + 1][di][2], alpha=0.40, linewidth=0, zorder=1)
    for s, col in enumerate(nodes):
        for i, (nm, v, c) in enumerate(col):
            top, bot = ys[s][i]
            ax.add_patch(Rectangle((s - SLAB / 2, bot), SLAB, top - bot, facecolor=c,
                                   edgecolor="none", zorder=3))
            ax.text(s, (top + bot) / 2, f"{nm} {v}", ha="center", va="center", fontsize=6,
                    color="white", zorder=4,
                    bbox=dict(boxstyle="round,pad=0.25", facecolor=c, edgecolor="none"))
    ax.text(-0.42, 1.03, f"mass conserved: {TOT} units at every stage", fontsize=6, color=OI["grey"])
    ax.set_xlim(-0.45, 3.45); ax.set_ylim(-0.01, 1.10)
    ax.set_xticks(range(4)); ax.set_xticklabels(stages); ax.set_yticks([])
    ax.tick_params(axis="x", length=0)
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    title(ax, "Alluvial flow (mass balance of an oral dose)")
    save(fig, "E06_alluvial", "multi-stage cohort flow with ribbons", "Flow-Network")

def flow_radial_dendrogram():
    """Kinase-panel selectivity: a radial clustering tree whose tip area encodes residual activity."""
    from scipy.cluster.hierarchy import linkage, dendrogram
    fams = [("TK", 18), ("TKL", 13), ("STE", 14), ("CAMK", 13), ("CMGC", 14)]
    cents = RNG.normal(0, 1, (len(fams), 6)) * 4.5
    X = np.vstack([cents[g] + RNG.normal(0, 0.7, (n, 6)) for g, (_, n) in enumerate(fams)])
    grp = np.concatenate([[g] * n for g, (_, n) in enumerate(fams)])
    n = len(X)

    pct = RNG.uniform(55, 99, n)                       # % of DMSO control (high = no binding)
    hits = np.concatenate([np.where(grp == 0)[0][:6], np.where(grp == 3)[0][:3]])
    pct[hits] = RNG.uniform(0.3, 12, len(hits))
    def sz(p):
        return 5.0 + 130.0 * ((100.0 - p) / 100.0) ** 3

    Z = linkage(X, method="ward")
    dd = dendrogram(Z, no_plot=True)
    order = np.array(dd["leaves"])
    pos = np.empty(n, int); pos[order] = np.arange(n)  # leaf -> angular slot

    members, hgrp = {i: {i} for i in range(n)}, {}
    for k, row in enumerate(Z):
        m = members[int(row[0])] | members[int(row[1])]
        members[n + k] = m
        gs = set(grp[list(m)])
        hgrp[float(row[2])] = gs.pop() if len(gs) == 1 else -1

    R_TIP, R_ROOT, R_LAB = 1.0, 0.20, 1.22
    hmax = Z[:, 2].max()
    th = lambda x: 2 * np.pi * x / (10.0 * n)
    rr = lambda h: R_TIP - (h / hmax) * (R_TIP - R_ROOT)

    fig, ax = plt.subplots(figsize=(4.2, 3.0), subplot_kw=dict(projection="polar"))
    fig.subplots_adjust(left=0.02, right=0.70, top=0.90, bottom=0.04)
    ax.set_theta_zero_location("N"); ax.set_theta_direction(-1)

    for g, (nm, _) in enumerate(fams):                 # pale sector tint + rim label
        p = pos[grp == g]
        lo, hi = th(5 + 10 * p.min()) - np.pi / n, th(5 + 10 * p.max()) + np.pi / n
        aa = np.linspace(lo, hi, 40)
        ax.fill_between(aa, 0, R_LAB + 0.03, color=CYCLE[g], alpha=0.09, linewidth=0, zorder=0)
        ax.text((lo + hi) / 2, R_LAB, nm, ha="center", va="center", fontsize=6,
                color=CYCLE[g], fontweight="bold")
    for xs4, ys4 in zip(dd["icoord"], dd["dcoord"]):   # radial segments + constant-radius arcs
        g = hgrp.get(float(ys4[1]), -1)
        c = CYCLE[g] if g >= 0 else OI["grey"]
        ax.plot([th(xs4[0])] * 2, [rr(ys4[0]), rr(ys4[1])], color=c, lw=0.7, zorder=2)
        ax.plot([th(xs4[3])] * 2, [rr(ys4[3]), rr(ys4[2])], color=c, lw=0.7, zorder=2)
        aa = np.linspace(th(xs4[0]), th(xs4[3]), 30)
        ax.plot(aa, np.full_like(aa, rr(ys4[1])), color=c, lw=0.7, zorder=2)
    ax.scatter(th(5 + 10 * pos), np.full(n, R_TIP), s=sz(pct), c=[CYCLE[g] for g in grp],
               edgecolor="k", linewidth=0.25, zorder=4)

    leg_p = [1, 10, 30, 70]
    hs = [ax.scatter([], [], s=sz(p), facecolor=OI["grey"], edgecolor="k", linewidth=0.25) for p in leg_p]
    ax.legend(hs, [f"{p}%" for p in leg_p], title="% of control", loc="center left",
              bbox_to_anchor=(1.04, 0.42), fontsize=6, title_fontsize=6,
              labelspacing=1.0, handletextpad=0.9, borderpad=0.2)
    ax.set_ylim(0, R_LAB + 0.16); ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False); ax.spines["polar"].set_visible(False)
    title(ax, "Radial dendrogram (kinase selectivity)")
    save(fig, "E07_radial_dendrogram", "radial tree with value-scaled tips", "Flow-Network")

def flow_network_communities():
    """Detected modules, degree-scaled nodes and named hubs make a trafficking interactome readable."""
    sizes = [15, 13, 11, 9]
    lab = np.concatenate([[i] * s for i, s in enumerate(sizes)])
    n = len(lab)
    P = np.where(lab[:, None] == lab[None, :], 0.45, 0.03)
    M = np.triu(RNG.random((n, n)) < P, 1)
    stem = ["RAB", "VPS", "CHMP", "STX", "VAMP", "SNAP", "ATG", "LAMP"]
    name = {i: f"{stem[i % 8]}{1 + i // 8}" for i in range(n)}
    G = nx.Graph(); G.add_nodes_from(range(n))
    for i, j in zip(*np.where(M)):
        G.add_edge(int(i), int(j), weight=float(RNG.uniform(0.3, 1.0)))
    blocks = np.split(np.arange(n), np.cumsum(sizes)[:-1])
    for blk in blocks:                                  # no orphan nodes, one link between blocks
        for v in blk:
            if G.degree(int(v)) == 0:
                G.add_edge(int(v), int(blk[0] if v != blk[0] else blk[1]), weight=0.5)
    for a, b in zip(blocks[:-1], blocks[1:]):
        G.add_edge(int(a[0]), int(b[0]), weight=0.35)
    while not nx.is_connected(G):                       # deterministic bridge repair
        comp = sorted((sorted(c) for c in nx.connected_components(G)), key=len, reverse=True)
        G.add_edge(comp[0][0], comp[1][0], weight=0.3)

    comms = [sorted(c) for c in nx.community.greedy_modularity_communities(G, weight="weight")]
    comms.sort(key=len, reverse=True)
    Q = nx.community.modularity(G, [set(c) for c in comms], weight="weight")
    cof = {v: k for k, c in enumerate(comms) for v in c}
    deg = dict(G.degree())
    pos = nx.spring_layout(G, weight="weight", seed=7, iterations=200)
    xy = np.array([pos[i] for i in range(n)]); ctr = xy.mean(axis=0)

    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=OI["grey"], alpha=0.45,
                           width=[2.0 * G[u][v]["weight"] ** 2 for u, v in G.edges()])
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=[10 + 11 * deg[i] for i in range(n)],
                           node_color=[CYCLE[cof[i]] for i in range(n)],
                           edgecolors="k", linewidths=0.35)
    hubs = [max(c, key=lambda i: deg[i]) for c in comms]  # label ONE top hub per community only
    nx.draw_networkx_nodes(G, pos, nodelist=hubs, ax=ax, node_size=[10 + 11 * deg[i] for i in hubs],
                           node_color=[CYCLE[cof[i]] for i in hubs], edgecolors="k", linewidths=1.4)
    for h in hubs:                                      # leader line = unambiguous attribution
        d = pos[h] - ctr; d = d / (np.hypot(*d) + 1e-9)
        ax.annotate(name[h], xy=pos[h], xytext=(pos[h][0] + 0.32 * d[0], pos[h][1] + 0.27 * d[1]),
                    fontsize=6, ha="center", va="center", color="k", zorder=6,
                    arrowprops=dict(arrowstyle="-", lw=0.5, color=OI["black"], shrinkA=0, shrinkB=4),
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.85))
    ax.legend(handles=[Circle((0, 0), 1, facecolor=CYCLE[k], edgecolor="k", linewidth=0.35)
                       for k in range(len(comms))],
              labels=[f"M{k+1} (n={len(c)})" for k, c in enumerate(comms)],
              loc="lower center", bbox_to_anchor=(0.5, -0.04), ncol=4, fontsize=6,
              handletextpad=0.4, columnspacing=0.8, handlelength=1.0)
    ax.text(0.0, 1.0, f"Q = {Q:.2f}\nsize $\\propto$ degree, width $\\propto$ weight",
            transform=ax.transAxes, fontsize=6, color=OI["grey"], ha="left", va="top")
    ax.set_xlim(xy[:, 0].min() - 0.42, xy[:, 0].max() + 0.42)
    ax.set_ylim(xy[:, 1].min() - 0.30, xy[:, 1].max() + 0.42); ax.axis("off")
    title(ax, "Network with detected communities")
    save(fig, "E08_network_communities", "communities + hub labels", "Flow-Network")



# ============================================================ F. TIME / EVOLUTION (Ex1 additions)

def time_offset_traces():
    """Nine ROI traces on offset baselines: propagation order is read off directly."""
    fs, dur = 10.0, 70.0
    t = np.arange(0, dur, 1 / fs)
    rois = [("Soma 1", OI["blue"], 22.0, 0.62), ("Primary 2", OI["orange"], 22.9, 0.44),
            ("Primary 3", OI["orange"], 23.5, 0.40), ("Secondary 4", OI["green"], 24.6, 0.30),
            ("Secondary 5", OI["green"], 25.3, 0.27), ("Secondary 6", OI["green"], 26.2, 0.25),
            ("Secondary 7", OI["green"], 27.1, 0.22), ("Secondary 8", OI["green"], 28.3, 0.21),
            ("Secondary 9", OI["green"], 29.6, 0.18)]
    off = 0.85

    def transient(t0, amp, tau_r=0.35, tau_d=3.2):
        d = t - t0
        return np.where(d >= 0, amp * (1 - np.exp(-d / tau_r)) * np.exp(-d / tau_d), 0.0)

    fig, ax = plt.subplots(figsize=(4.3, 3.3))
    ax.axvspan(20.0, 21.5, color=OI["sky"], alpha=0.22, lw=0, zorder=0)
    peaks = []
    for i, (lab, col, t0, amp) in enumerate(rois):
        base = -i * off
        drift = 0.035 * np.sin(2 * np.pi * t / 47 + i)
        prev = transient(t0, amp) + transient(t0 + 0.4, 0.25 * amp, 0.5, 6.0)
        y1 = base + prev + drift + RNG.normal(0, 0.017, t.size)
        y2 = (base + 0.9 * transient(t0 + RNG.normal(0, 0.25), 0.88 * amp)
              + drift + RNG.normal(0, 0.017, t.size))
        ax.plot(t, y2, color=col, lw=0.7, alpha=0.32, zorder=2)
        ax.plot(t, y1, color=col, lw=0.9, zorder=3)
        w = (t > 21) & (t < 40)
        tp = float(t[w][np.argmax(y1[w])]); peaks.append(tp)
        ax.plot([tp], [base + amp + 0.14], marker="v", ms=3.0, color=col,
                mec="none", zorder=4)
        ax.text(-0.012, base + 0.06, lab, transform=ax.get_yaxis_transform(),
                ha="right", va="center", fontsize=6.2, color=col)

    ax.axvline(peaks[0], color="0.35", ls="--", lw=0.6, zorder=1)
    ax.axvline(peaks[-1], color="0.35", ls="--", lw=0.6, zorder=1)
    ax.annotate(f"wave transit {peaks[-1] - peaks[0]:.1f} s",
                xy=(peaks[-1], 0.92), xytext=(peaks[-1] + 3.5, 1.02),
                ha="left", va="center", fontsize=6, color="0.35",
                arrowprops=dict(arrowstyle="-", lw=0.55, color="0.5", shrinkB=1))
    ax.text(20.75, -8.05, "stimulus", ha="center", va="top", fontsize=6, color="0.35")

    # scale bar: lengths are the printed values, in data units
    sx, sy = 61.0, -7.55
    ax.plot([sx, sx], [sy, sy + 0.5], color="0.15", lw=1.3, solid_capstyle="butt")
    ax.plot([sx - 10, sx], [sy, sy], color="0.15", lw=1.3, solid_capstyle="butt")
    ax.text(sx - 0.9, sy + 0.25, "0.5 $\\Delta$F/F$_0$", ha="right", va="center",
            fontsize=6, color="0.15")
    ax.text(sx - 5, sy - 0.12, "10 s", ha="center", va="top", fontsize=6, color="0.15")

    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_ylim(-8.6, 1.5); ax.set_xlim(0, dur)
    ax.set_xlabel("Time (s)")
    title(ax, "Calcium wave across 9 ROIs ($\\Delta$F/F$_0$)")
    fig.tight_layout()
    save(fig, "F11_offset_traces", "many traces via offset + scale bar", "Time-series")



# ============================================================ H. 3D & FIELDS (Ex1 additions)

def field_annotated_profile():
    """A wall-shear profile and the velocity field that produces it, on one x axis."""
    import matplotlib.patheffects as pe
    r0, sten, z0, wid = 2.0, 0.55, 8.0, 1.6
    u0, mu = 200.0, 3.5e-3                       # mm/s ; Pa.s
    z = np.linspace(0, 22, 460); r = np.linspace(-r0, r0, 300)
    Z, R = np.meshgrid(z, r)
    rw = r0 * (1 - sten * np.exp(-((z - z0) / wid) ** 2))
    RW = r0 * (1 - sten * np.exp(-((Z - z0) / wid) ** 2))
    u_par = 1.5 * u0 * (r0 / RW) * np.clip(1 - (R / RW) ** 2, 0, None)
    rt = r0 * (1 - sten)
    u_jet = 1.5 * u0 * (r0 / rt) * np.clip(1 - (R / rt) ** 2, 0, None)
    wj = np.where(Z > z0, np.exp(-((Z - z0) / 5.0) ** 2), 0.0)
    u = (1 - wj) * u_par + wj * u_jet
    u -= 88.0 * np.exp(-((Z - (z0 + 2.6)) / 1.9) ** 2) * \
        np.exp(-((np.abs(R) - 0.80 * r0) / 0.48) ** 2)
    u = np.where(np.abs(R) <= RW, u, np.nan)

    dudr = np.gradient(np.nan_to_num(u), r, axis=0)
    tau = np.array([np.interp(-0.94 * rw[j], r, dudr[:, j]) for j in range(z.size)]) * mu
    jmax = int(np.argmax(tau)); tmax = tau[jmax]
    rev = tau < 0
    z_rev = (z[rev].min(), z[rev].max()) if rev.any() else None

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4.1, 3.7), sharex=True,
                                   gridspec_kw={"height_ratios": [1.0, 1.85],
                                                "hspace": 0.24})
    fig.subplots_adjust(left=0.145, right=0.815, top=0.905, bottom=0.115)
    ax1.axhline(0, color="0.6", lw=0.6, ls=":")
    ax1.plot(z, tau, color=OI["blue"], lw=1.3)
    if z_rev:
        ax1.axvspan(*z_rev, color=OI["vermillion"], alpha=0.16, lw=0)
    ax1.plot([z[jmax]], [tmax], marker="o", ms=3.5, color=OI["blue"])
    ax1.annotate(f"$\\tau_w$ peak {tmax:.1f} Pa", xy=(z[jmax], tmax),
                 xytext=(z[jmax] - 1.0, tmax * 1.02), ha="right", va="top", fontsize=6,
                 color=OI["blue"],
                 arrowprops=dict(arrowstyle="-", lw=0.55, color=OI["blue"], shrinkB=2))
    if z_rev:
        ax1.text((z_rev[0] + z_rev[1]) / 2, tmax * 0.30,
                 f"reversal\n{z_rev[1] - z_rev[0]:.1f} mm", ha="center", va="center",
                 fontsize=6.0, color=OI["vermillion"], linespacing=1.3)
    ax1.set_ylabel("$\\tau_w$ (Pa)")
    ax1.set_ylim(min(-0.9, tau.min() * 1.5), tmax * 1.30)
    ax1.yaxis.set_major_locator(mpl.ticker.MaxNLocator(4, prune="lower"))
    ax1.tick_params(labelsize=6.5)

    im = ax2.pcolormesh(Z, R, np.abs(u), cmap=SEQ, shading="auto", rasterized=True)
    ax2.contour(Z, R, np.nan_to_num(u, nan=1.0), levels=[0], colors="white",
                linewidths=0.7, linestyles="--")
    ax2.fill_between(z, rw, r0, color="0.86", lw=0)        # vessel wall / surrounding tissue
    ax2.fill_between(z, -r0, -rw, color="0.86", lw=0)
    ax2.plot(z, rw, color="0.3", lw=0.9); ax2.plot(z, -rw, color="0.3", lw=0.9)
    halo = [pe.withStroke(linewidth=1.7, foreground="black")]
    ax1.axvline(z0, color="0.3", ls="--", lw=0.8, zorder=6)
    ax2.axvline(z0, color="0.2", ls="--", lw=0.8, zorder=6)
    ax2.annotate("jet core", xy=(z0 + 3.5, 0.0), xytext=(z0 + 7.0, 1.45),
                 fontsize=6.2, color="white", ha="center", va="center",
                 arrowprops=dict(arrowstyle="->", lw=0.8, color="white"),
                 path_effects=halo)
    ax2.annotate("flow reversal", xy=(z0 + 3.4, -1.55), xytext=(z0 + 8.8, -1.55),
                 fontsize=6.2, color="white", ha="center", va="center",
                 arrowprops=dict(arrowstyle="->", lw=0.8, color="white"),
                 path_effects=halo)
    ax2.annotate("throat", xy=(z0, 0.62), xytext=(z0 - 2.6, 1.45),
                 fontsize=6.2, color="white", ha="center", va="center",
                 arrowprops=dict(arrowstyle="->", lw=0.8, color="white"),
                 path_effects=halo)
    ax2.set_xlabel("Axial position z (mm)"); ax2.set_ylabel("Radial position r (mm)")
    ax2.set_xlim(0, 22); ax2.set_ylim(-r0, r0)
    ax2.set_xticks(np.arange(0, 22.1, 5)); ax2.set_yticks(np.arange(-2, 2.1, 1))
    ax2.tick_params(labelsize=6.5)
    # colorbar scoped to the field panel only; same 0.046 width / 0.04 pad as the
    # house form, but sized off ax2 so both panels keep identical widths
    p2 = ax2.get_position()
    cax = fig.add_axes([p2.x1 + 0.027, p2.y0, 0.031, p2.height])
    cb = fig.colorbar(im, cax=cax, label="Velocity magnitude (mm s$^{-1}$)")
    cb.ax.tick_params(labelsize=6.5); cb.outline.set_linewidth(0.6)
    title(ax1, "Stenosis: wall shear profile over its velocity field")
    save(fig, "H11_annotated_field_profile", "field + companion profile, annotated", "3D-Fields")



# ============================================================ I. SPECIALIZED / MULTI-PANEL (Ex1 additions)

def spec_study_design():
    """Panel-a orientation: who got what, when, and where the readouts land on the study clock."""
    load = [d for w in range(5) for d in (7 * w, 7 * w + 2, 7 * w + 4)]
    groups = [("i.v. siControl", [7, 21], OI["grey"]),
              ("i.v. siMMP13", [7, 21], OI["vermillion"]),
              ("i.a. depot (single)", [7], OI["purple"]),
              ("i.p. inhibitor 1$\\times$/2 wk", [7, 21], OI["green"]),
              ("i.p. inhibitor 3$\\times$/wk", [d for d in load if d >= 7], OI["blue"])]
    rows = [4.35, 3.30, 2.60, 1.90, 1.20, 0.50]

    fig, ax = plt.subplots(figsize=(6.4, 3.0))
    for x0, x1, c in [(-9, 0, OI["grey"]), (0, 35, OI["sky"])]:   # treatment windows as spans
        ax.add_patch(Rectangle((x0, -0.1), x1 - x0, 5.70, facecolor=c, alpha=0.10,
                               edgecolor="none", zorder=0))
    ax.add_patch(Rectangle((-9, 6.45), 44, 0.95, facecolor=OI["grey"], alpha=0.16,
                           edgecolor="none", zorder=1))
    ax.text(17.5, 6.92, "Mouse OA model, both knees\n"
                        "mechanical loading 3$\\times$/wk (9 N, 250 cycles)",
            ha="center", va="center", fontsize=7, zorder=2)
    for x0, x1, lb, c in [(-9, 0, "acclimatisation", OI["grey"]), (0, 35, "loading + treatment", OI["sky"])]:
        ax.add_patch(Rectangle((x0, 5.80), x1 - x0, 0.30, facecolor=c, alpha=0.55,
                               edgecolor="none", zorder=1))
        ax.text((x0 + x1) / 2, 5.95, lb, ha="center", va="center", fontsize=6, zorder=2)
    for d, lb, ha in [(0, "randomisation", "left"), (21, "interim readout", "center"),
                      (35, "endpoint (tissue)", "right")]:
        ax.vlines(d, 0.15, 4.95, color=OI["black"], lw=0.7, ls=(0, (2, 2)), zorder=1)
        ax.text(d, 5.15, lb, ha=ha, va="bottom", fontsize=6.5, zorder=2)
    ax.scatter(load, [rows[0]] * len(load), marker="v", s=16, color=OI["black"], zorder=3)
    ax.scatter([35], [rows[0]], marker="v", s=30, color=OI["vermillion"], zorder=4)
    for k, (nm, days, c) in enumerate(groups):
        y = rows[k + 1]
        ax.plot([0, 35], [y, y], ls=":", lw=0.7, color=OI["grey"], zorder=1)
        ax.scatter(days, [y] * len(days), marker="^", s=24, color=c, edgecolor="k",
                   linewidth=0.3, zorder=3)
    ax.set_xlim(-9.5, 36.5); ax.set_ylim(-0.1, 7.5)
    ax.set_xticks([0, 7, 14, 21, 28, 35]); ax.set_xlabel("Study day")
    ax.set_xticks(np.arange(-7, 36, 1), minor=True)
    ax.set_yticks(rows)
    ax.set_yticklabels(["mechanical loading"] + [g[0] for g in groups], fontsize=6.5)
    ax.tick_params(axis="y", length=0)
    ax.spines["left"].set_visible(False)
    title(ax, "Study design and dosing schedule")
    save(fig, "I08_study_design", "study-design / dosing timeline", "Specialized")

def spec_pipeline_schematic():
    """A branch-and-merge block diagram of the in vitro to in vivo prediction pipeline."""
    def lt(c, k=0.28):
        return tuple(1 - (1 - ch) * k for ch in mpl.colors.to_rgb(c))
    KIND = {"data": OI["sky"], "proc": OI["grey"], "model": OI["orange"], "out": OI["green"]}
    boxes = {
        "diss":  (0.95, 2.55, "Dissolution\nprofiles (f2)", "data"),
        "pk":    (0.95, 0.75, "Reference PK\n(in vivo Cp)", "data"),
        "qc":    (3.05, 2.55, "QC, outlier\n+ deconvolution", "proc"),
        "pbpk":  (5.35, 3.45, "PBPK\n(mechanistic)", "model"),
        "ivivc": (5.35, 1.55, "IVIVC level A\n(empirical)", "model"),
        "avg":   (7.60, 2.55, "Model\naveraging", "proc"),
        "cp":    (9.55, 3.35, "Predicted\nCp(t)", "out"),
        "pe":    (9.55, 1.65, "%PE vs\nobserved", "out"),
    }
    arrows = [("diss", "qc"), ("qc", "pbpk"), ("qc", "ivivc"), ("pk", "ivivc"),
              ("pbpk", "avg"), ("ivivc", "avg"), ("avg", "cp"), ("avg", "pe"), ("pk", "pe")]

    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.set_xlim(-0.1, 10.9); ax.set_ylim(-0.50, 4.05)
    txt = {k: ax.text(x, y, lb, ha="center", va="center", fontsize=6.5, zorder=3,
                      bbox=dict(boxstyle="round,pad=0.42", facecolor=lt(KIND[kd]),
                                edgecolor=KIND[kd], linewidth=0.8))
           for k, (x, y, lb, kd) in boxes.items()}
    fig.canvas.draw()                       # measure the drawn boxes so arrows stop at their edges
    rend = fig.canvas.get_renderer()
    def edge(k, ang):                       # centre-to-border distance of box k, in points
        bb = txt[k].get_bbox_patch().get_window_extent(rend)
        ca, sa = abs(np.cos(ang)), abs(np.sin(ang))
        d = min(bb.width / 2 / ca if ca > 1e-6 else np.inf,
                bb.height / 2 / sa if sa > 1e-6 else np.inf)
        return d * 72.0 / fig.dpi
    for a, b in arrows:
        xa, ya, _, _ = boxes[a]; xb, yb, _, _ = boxes[b]
        (pax, pay), (pbx, pby) = ax.transData.transform([(xa, ya), (xb, yb)])
        ang = np.arctan2(pby - pay, pbx - pax)
        rad = 0.0 if abs(ya - yb) < 1e-9 else (0.14 if yb > ya else -0.14)
        ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=7,
                                     shrinkA=edge(a, ang) + 1.5, shrinkB=edge(b, ang) + 3.5,
                                     lw=0.8, color=OI["grey"],
                                     connectionstyle=f"arc3,rad={rad}", zorder=1))
    ax.legend(handles=[Rectangle((0, 0), 1, 1, facecolor=lt(c), edgecolor=c, linewidth=0.8)
                       for c in KIND.values()],
              labels=["input data", "processing", "model", "output"], loc="lower center",
              bbox_to_anchor=(0.5, -0.03), ncol=4, fontsize=6, handlelength=1.1,
              handletextpad=0.4, columnspacing=1.2)
    ax.axis("off")
    title(ax, "Analysis pipeline (branch and merge)")
    save(fig, "I09_pipeline_schematic", "analysis / model pipeline diagram", "Specialized")

def spec_pie_vs_bar():
    """The same six close shares: unrankable as angle or arc, trivial as length."""
    org = ["Liver", "Spleen", "Kidney", "Lung", "Tumour", "Heart"]
    pct = np.array([21.5, 19.8, 18.4, 16.2, 13.7, 10.4])
    assert abs(pct.sum() - 100.0) < 1e-9, "shares must be a whole"
    cols = CYCLE[:6]
    fig, axs = plt.subplots(1, 3, figsize=(6.4, 2.6), gridspec_kw=dict(width_ratios=[1, 1, 1.45]))
    wp = dict(edgecolor="white", linewidth=0.6)
    axs[0].pie(pct, colors=cols, startangle=90, counterclock=False, wedgeprops=wp)
    axs[1].pie(pct, colors=cols, startangle=90, counterclock=False,
               wedgeprops=dict(width=0.42, **wp))
    for a in axs[:2]:
        a.set_aspect("equal"); a.set_anchor("N")           # keep panel titles on one baseline
    title(axs[0], "pie (AVOID — AP10)"); title(axs[1], "donut (AVOID — AP11)")
    o = np.argsort(pct)                                    # ascending -> largest on top
    axs[2].barh(np.arange(6), pct[o], color=[cols[i] for i in o], edgecolor="k", linewidth=0.4)
    for k, i in enumerate(o):
        axs[2].text(pct[i] + 0.6, k, f"{pct[i]:.1f}%", va="center", fontsize=6.5)
    axs[2].set_yticks(np.arange(6)); axs[2].set_yticklabels([org[i] for i in o], fontsize=7)
    axs[2].set_xlim(0, 27); axs[2].set_xlabel("Injected dose recovered (%)")
    title(axs[2], "bar (use)")
    axs[0].legend(handles=[Rectangle((0, 0), 1, 1, facecolor=c) for c in cols], labels=org,
                  loc="upper center", bbox_to_anchor=(1.08, -0.02), ncol=3, fontsize=6,
                  handlelength=1.0, handletextpad=0.4, columnspacing=1.0)
    fig.text(0.5, -0.10, "a and b force a colour lookup, then an angle/arc comparison; "
                         "c is read off one common baseline.", ha="center", fontsize=6,
             color=OI["grey"])
    fig.tight_layout()
    save(fig, "I10_pie_vs_bar", "AP10/AP11: why pie loses to a bar", "Specialized")



# ============================================================ J. OMICS / SINGLE-CELL / CYTOMETRY

def omics_embedding_feature_pair():
    """One embedding read two ways: cluster identity, then the same coordinates re-coloured by one gene."""
    import matplotlib.patheffects as pe
    names = ["T cells", "B cells", "Macrophages", "Endothelial",
             "Fibroblasts", "Mast cells", "pDCs"]
    ctr = np.array([[-4.5, 6.0], [-6.5, -4.0], [2.0, 0.5], [9.0, 8.0],
                    [10.0, -4.5], [-1.0, -9.0], [3.0, 12.5]]) * 1.24
    nper = [1800, 900, 2400, 1300, 1500, 700, 400]
    XY, lab = [], []
    for k, (c, n) in enumerate(zip(ctr, nper)):
        ang = RNG.uniform(0, 2 * np.pi, n)                       # lobed, sharp-edged, area-filled
        wob = (1 + 0.22 * np.sin(3 * ang + RNG.uniform(0, 6.3))  # island — not a Gaussian ellipse
                 + 0.13 * np.sin(5 * ang + RNG.uniform(0, 6.3)))
        rad = np.sqrt(RNG.random(n)) * wob
        th = RNG.uniform(0, np.pi)
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        s = 0.62 * np.sqrt(n / 1000.0) * np.array([RNG.uniform(2.2, 2.9), RNG.uniform(3.0, 3.8)])
        XY.append((np.c_[rad * np.cos(ang), rad * np.sin(ang)] * s) @ R + c)
        lab.append(np.full(n, k))
    XY = np.vstack(XY); lab = np.concatenate(lab)
    XY[:, 0] += 1.1 * np.sin(XY[:, 1] / 4.5)                     # smooth warp -> organic UMAP islands
    XY[:, 1] += 1.1 * np.cos(XY[:, 0] / 5.0)

    # one continuous feature: CD68 is myeloid-restricted (macrophages, weakly pDCs)
    expr = np.abs(RNG.normal(0, 0.11, XY.shape[0]))
    expr[lab == 2] += RNG.gamma(4.0, 0.34, int((lab == 2).sum()))
    expr[lab == 6] += RNG.gamma(2.0, 0.20, int((lab == 6).sum()))
    expr = np.clip(expr, 0, 2.6)

    fig, axs = plt.subplots(1, 2, figsize=(6.4, 3.0))
    for k in range(len(names)):                                  # (a) categorical clusters
        m = lab == k
        axs[0].scatter(XY[m, 0], XY[m, 1], s=1.1, color=CYCLE[k], alpha=0.75, linewidths=0)
        axs[0].text(np.median(XY[m, 0]), np.median(XY[m, 1]), names[k], fontsize=6.3,
                    ha="center", va="center", color="k", zorder=5,
                    path_effects=[pe.withStroke(linewidth=1.8, foreground="white")])
    o = np.argsort(expr)                                         # (b) same coords, one feature
    sc = axs[1].scatter(XY[o, 0], XY[o, 1], s=1.1, c=expr[o], cmap=SEQ, vmin=0, vmax=2.6, linewidths=0)
    fig.colorbar(sc, ax=axs[1], fraction=0.046, pad=0.04, label="CD68 (log-norm. counts)")

    for ax in axs:
        ax.set_xlabel("UMAP 1"); ax.set_ylabel("UMAP 2")
        ax.set_xticks([-10, -5, 0, 5, 10]); ax.set_yticks([-10, 0, 10])
    title(axs[0], f"Clusters (n = {XY.shape[0]:,} cells)")
    title(axs[1], "Same embedding: CD68")
    fig.tight_layout()
    save(fig, "J01_embedding_feature_pair", "clusters + same embedding by feature", "Omics-Cytometry")

def omics_dotplot_matrix():
    """Each dot carries two statistics at once: how many cells express a marker (size) and how strongly (colour)."""
    genes = ["PTPRC", "CD3E", "MS4A1", "LYZ", "CD68", "PECAM1", "COL1A1", "TPSAB1", "KRT18", "MKI67"]
    groups = ["T cells", "B cells", "Macrophages", "Endothelial", "Fibroblasts", "Mast cells"]
    n_cell = 220
    p_on = np.full((len(genes), len(groups)), 0.06)              # P(cell expresses gene)
    lvl = np.full((len(genes), len(groups)), 0.35)               # mean level when expressed

    def setg(g, cols, p, l):
        i = genes.index(g)
        for c in cols:
            p_on[i, c] = p; lvl[i, c] = l
    setg("PTPRC", [0, 1, 2, 5], 0.93, 2.1); setg("PTPRC", [3, 4], 0.10, 0.5)
    setg("CD3E", [0], 0.88, 1.9); setg("MS4A1", [1], 0.85, 2.0)
    setg("LYZ", [2], 0.90, 2.4); setg("LYZ", [5], 0.34, 0.9)
    setg("CD68", [2], 0.82, 1.8); setg("PECAM1", [3], 0.87, 2.0)
    setg("COL1A1", [4], 0.91, 2.5); setg("TPSAB1", [5], 0.80, 2.2)
    setg("KRT18", [3, 4], 0.22, 0.7); setg("MKI67", [0, 2, 4], 0.16, 0.6)

    pct = np.zeros_like(p_on); mean_ = np.zeros_like(p_on)       # BOTH stats from the same cells
    for i in range(len(genes)):
        for j in range(len(groups)):
            on = RNG.random(n_cell) < p_on[i, j]
            x = np.where(on, RNG.gamma(3.0, lvl[i, j] / 3.0, n_cell), 0.0)
            pct[i, j] = 100.0 * on.mean(); mean_[i, j] = x.mean()
    scaled = mean_ / mean_.max()                                 # ONE scale for the whole matrix,
    # so a gene that is low everywhere stays dark instead of being rescaled up to the top colour.

    X, Y = np.meshgrid(np.arange(len(groups)), np.arange(len(genes)))
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    sc = ax.scatter(X.ravel(), Y.ravel(), s=4 + (pct.ravel() / 100.0) * 118, c=scaled.ravel(),
                    cmap=SEQ, vmin=0, vmax=1, edgecolor="0.35", linewidth=0.3, zorder=3)
    ax.set_xticks(range(len(groups))); ax.set_xticklabels(groups, rotation=30, ha="right", fontsize=6.5)
    ax.set_yticks(range(len(genes))); ax.set_yticklabels(genes, fontsize=6.5, style="italic")
    ax.set_xlim(-0.65, len(groups) - 0.35); ax.set_ylim(len(genes) - 0.35, -0.65)
    ax.grid(True, lw=0.3, color="0.86"); ax.tick_params(length=2)
    ax.set_xlabel("Cell type")
    fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, label="Mean expression (scaled to matrix max)")
    hs = [ax.scatter([], [], s=4 + (v / 100.0) * 118, color="0.55", edgecolor="0.35", linewidth=0.3)
          for v in (0, 25, 50, 75, 100)]
    ax.legend(hs, ["0", "25", "50", "75", "100"], title="Percent expressed", loc="center left",
              bbox_to_anchor=(1.24, 0.5), labelspacing=1.05, fontsize=6.5, title_fontsize=7,
              handletextpad=0.9, borderpad=0.3)
    title(ax, f"Marker dot plot (n = {n_cell} cells per cell type)")
    fig.tight_layout()
    save(fig, "J02_dotplot_matrix", "two statistics at once (size + colour)", "Omics-Cytometry")

def omics_stacked_violin():
    """One row per gene, one violin per dose: the whole distribution stays visible instead of a group mean."""
    genes = ["EGFR", "MYC", "CDKN1A", "AURKB", "TP53", "CD274"]
    doses = ["Vehicle", "0.1 µM", "1 µM", "10 µM", "Combo"]
    base = {"EGFR": 1.90, "MYC": 2.20, "CDKN1A": 0.50, "AURKB": 1.70, "TP53": 1.10, "CD274": 0.35}
    slope = {"EGFR": -0.32, "MYC": -0.40, "CDKN1A": 0.46, "AURKB": -0.34, "TP53": 0.06, "CD274": 0.12}
    n = 180                                                      # well above the n~20 violin floor (AP2)

    fig, axs = plt.subplots(len(genes), 1, figsize=(4.3, 4.1), sharex=True)
    for g, ax in zip(genes, axs):
        rows = []
        for j in range(len(doses)):
            mu = max(base[g] + slope[g] * j, 0.08)
            v = RNG.gamma(9.0, mu / 9.0, n)
            if g == "CD274" and j >= 3:                          # induced sub-population -> bimodal
                f = n // 3 if j == len(doses) - 1 else n // 6    # (a mean would hide this entirely)
                v[:f] = RNG.gamma(16.0, 2.40 / 16.0, f)
            rows.append(v)
        parts = ax.violinplot(rows, positions=np.arange(len(doses)), widths=0.82,
                              showextrema=False, showmedians=True)
        for j, b in enumerate(parts["bodies"]):
            b.set_facecolor(CYCLE[j]); b.set_alpha(0.72); b.set_edgecolor("0.25"); b.set_linewidth(0.4)
        parts["cmedians"].set_color("0.15"); parts["cmedians"].set_linewidth(0.7)
        allv = np.concatenate(rows)                              # row scaled to its own working range
        lo, hi = np.percentile(allv, 0.5), np.percentile(allv, 99.5)
        pad = 0.10 * (hi - lo)
        ax.set_ylim(lo - pad, hi + pad); ax.set_yticks([lo, hi])
        ax.set_yticklabels([f"{lo:.1f}", f"{hi:.1f}"], fontsize=5.5)
        ax.set_ylabel(g, rotation=0, ha="right", va="center", fontsize=6.5, style="italic", labelpad=4)
        ax.tick_params(axis="y", length=2)
    axs[-1].set_xticks(range(len(doses)))
    axs[-1].set_xticklabels(doses, rotation=30, ha="right", fontsize=6.5)
    axs[-1].set_xlabel("Gefitinib, 24 h", fontsize=8)
    axs[-1].tick_params(axis="x", length=2)
    title(axs[0], "Log-normalised expression, scaled per gene")
    fig.tight_layout(h_pad=0.35)
    save(fig, "J03_stacked_violin", "per-gene distributions across groups", "Omics-Cytometry")

def omics_enrichment_dotplot():
    """One panel carries three enrichment quantities: hit fraction, set size and significance."""
    from matplotlib.lines import Line2D

    def bh(p):                                     # Benjamini-Hochberg, no statsmodels needed
        p = np.asarray(p, float); m = p.size; o = np.argsort(p)
        q = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
        out = np.empty(m); out[o] = np.clip(q, 0, 1); return out

    names = ["Efferocytosis", "Apoptotic cell clearance", "Tissue remodelling",
             "Arginine and proline metabolism", "Antigen processing and presentation",
             "TNF signalling pathway", "NF-kappa B signalling pathway",
             "Humoral immune response", "JAK-STAT signalling pathway",
             "Adaptive immune response"]
    N, n_de, n_bg = 18000, 312, 55                 # background genes, DE list, untested pathways
    size = RNG.integers(48, 300, len(names))       # pathway sizes (genes annotated)
    fold = RNG.uniform(2.6, 7.4, len(names))       # enrichment over the null expectation
    hits = np.maximum(np.round(n_de * size / N * fold).astype(int), 4)
    bg_size = RNG.integers(40, 400, n_bg)
    bg_hits = RNG.binomial(bg_size, n_de / N)      # null-behaving pathways, for an honest BH
    p_all = stats.hypergeom.sf(np.r_[hits, bg_hits] - 1, N, np.r_[size, bg_size], n_de)
    padj = bh(p_all)[:len(names)]                  # adjusted across every pathway tested

    o = np.argsort(padj)[::-1]                     # least significant first -> plots at bottom
    names = [names[i] for i in o]; hits, size, padj = hits[o], size[o], padj[o]
    ratio = hits / size                            # gene ratio = hits / pathway size
    sig = -np.log10(padj)
    s_of = lambda c: 10.0 + 3.2 * c                # marker area, linear in gene count

    fig, ax = plt.subplots(figsize=(4.9, 2.9))
    y = np.arange(len(names))
    ax.grid(axis="both", lw=0.4, color=OI["grey"], alpha=0.45)
    sc = ax.scatter(ratio, y, s=s_of(hits), c=sig, cmap=SEQ, edgecolor="k", linewidth=0.4, zorder=3)
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=6.5)
    ax.set_ylim(-0.8, len(names) - 0.2)
    ax.set_xlim(ratio.min() - 0.013, ratio.max() + 0.013)   # a ratio is not a bar -> no zero-base
    ax.set_xlabel("gene ratio (hits / pathway size)")
    ax.tick_params(axis="x", labelsize=7)
    fig.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, label="-log10 adjusted p (BH)")

    counts = np.unique(np.round(np.linspace(hits.min(), hits.max(), 4)).astype(int))
    handles = [Line2D([], [], marker="o", linestyle="none", markersize=np.sqrt(s_of(c)),
                      markerfacecolor=OI["grey"], markeredgecolor="k", markeredgewidth=0.4,
                      label=str(c)) for c in counts]
    ax.legend(handles=handles, title="gene count", loc="upper left", bbox_to_anchor=(0.0, -0.24),
              ncol=len(counts), fontsize=6, title_fontsize=6.5, handletextpad=0.35,
              columnspacing=1.1, borderpad=0.0)
    title(ax, "Pathway enrichment (dot plot)")
    save(fig, "J04_enrichment_dotplot", "ratio, count and FDR in one panel", "Omics-Cytometry")

def omics_gsea_running():
    """The running score shows WHERE a gene set sits in the ranking, not just that it is enriched."""
    def bh(p):
        p = np.asarray(p, float); m = p.size; o = np.argsort(p)
        q = np.minimum.accumulate((p[o] * m / np.arange(1, m + 1))[::-1])[::-1]
        out = np.empty(m); out[o] = np.clip(q, 0, 1); return out

    n, k, nperm = 1200, 90, 1000
    metric = np.sort(RNG.normal(0, 1.6, n))[::-1]          # ranked signal-to-noise, descending
    absm = np.abs(metric)

    def es_curves(idx2d):                                   # weighted running Kolmogorov-Smirnov
        m = idx2d.shape[0]
        inc = np.zeros((m, n)); r = absm[idx2d]
        np.put_along_axis(inc, idx2d, r / r.sum(axis=1, keepdims=True), axis=1)
        miss = np.full((m, n), 1.0 / (n - k))
        np.put_along_axis(miss, idx2d, 0.0, axis=1)
        cur = np.cumsum(inc - miss, axis=1)
        j = np.argmax(np.abs(cur), axis=1)
        return cur, j, cur[np.arange(m), j]

    decay = [170.0, 430.0, 900.0, 1e7, 1e7, 1e7, 1e7, 1e7]  # family of 8 sets -> a real FDR
    members = np.array([np.sort(RNG.choice(n, k, replace=False,
                                           p=(np.exp(-np.arange(n) / d) + 0.05) /
                                             (np.exp(-np.arange(n) / d) + 0.05).sum()))
                        for d in decay])
    cur, jpk, es = es_curves(members)
    _, _, null = es_curves(np.sort(np.argsort(RNG.random((nperm, n)), axis=1)[:, :k], axis=1))
    pos, neg = null[null > 0].mean(), -null[null < 0].mean()
    nes = np.where(es > 0, es / pos, es / neg)
    nes_null = np.where(null > 0, null / pos, null / neg)
    pval = np.array([(1 + (nes_null >= v).sum()) / (nperm + 1) if v > 0 else
                     (1 + (nes_null <= v).sum()) / (nperm + 1) for v in nes])
    q = bh(pval)

    i = 0                                                   # the strongly top-enriched set
    hit, curve, pk, ES = members[i], cur[i], int(jpk[i]), es[i]
    x = np.arange(1, n + 1)

    fig, (a1, a2, a3) = plt.subplots(3, 1, figsize=(3.8, 3.2), sharex=True,
                                     gridspec_kw=dict(height_ratios=[3.0, 0.5, 1.35], hspace=0.0))
    a1.axhline(0, color=OI["grey"], lw=0.7)
    a1.axvline(x[pk], color=OI["grey"], ls="--", lw=0.7)
    a1.plot(x, curve, color=OI["green"], lw=1.3)
    a1.plot(x[pk], ES, "o", ms=4.5, mfc="white", mec=OI["green"], mew=1.2, zorder=4)
    a1.set_ylim(-0.10, ES + 0.30)
    a1.set_yticks([0.0, 0.2, 0.4, 0.6])
    a1.set_ylabel("running ES")
    a1.text(0.985, 0.97, f"ES = {ES:.2f}\nNES = {nes[i]:.2f}\nFDR q = {q[i]:.4f}",
            transform=a1.transAxes, ha="right", va="top", fontsize=6.5, linespacing=1.35)

    a2.vlines(x[hit], 0, 1, color="k", lw=0.5)
    a2.set_ylim(0, 1); a2.set_yticks([])
    a2.set_ylabel("hits", fontsize=6)
    for sp in ("left", "bottom"):
        a2.spines[sp].set_visible(False)
    a2.tick_params(axis="y", length=0)

    a3.axhline(0, color=OI["grey"], lw=0.7)
    a3.fill_between(x, metric, 0, where=metric >= 0, color=OI["vermillion"], lw=0, interpolate=True)
    a3.fill_between(x, metric, 0, where=metric < 0, color=OI["blue"], lw=0, interpolate=True)
    a3.set_yticks([-4, 0, 4])
    a3.set_ylabel("metric")
    a3.set_xlabel("gene rank in ordered list")
    a3.set_xlim(1, n)

    title(a1, "GSEA: Hallmark oxidative phosphorylation")
    save(fig, "J05_gsea_running", "running enrichment + rank ticks", "Omics-Cytometry")

def omics_heatmap_tracks():
    """Annotation tracks prove the expression blocks follow treatment, not processing batch."""
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch

    genes = ["Il6", "Tnf", "Nfkb1", "Ccl2", "Cxcl10", "Hmox1", "Nqo1",
             "Gclc", "Sod2", "Casp3", "Bax", "Bcl2", "Mki67", "Ccnd1"]
    groups = ["Vehicle", "LNP-low", "LNP-high", "Free drug"]
    per, ng = 6, len(genes)
    gidx = np.repeat(np.arange(4), per)                      # samples ordered by treatment
    bidx = np.tile(np.repeat(np.arange(3), 2), 4)            # batch balanced inside every group
    ns = gidx.size

    X = RNG.normal(0, 0.55, (ng, ns))
    dose = np.array([0.0, 1.0, 2.0, 1.4])[gidx]              # treatment effect, gene-specific sign
    load = np.r_[np.linspace(1.0, 0.45, 9), np.linspace(-0.9, -0.35, 5)]
    X += load[:, None] * dose[None, :]
    X += RNG.normal(0, 0.30, (ng, 1)) * (bidx - 1)[None, :]  # small nuisance batch effect
    Z = (X - X.mean(1, keepdims=True)) / X.std(1, ddof=1, keepdims=True)
    v = np.ceil(np.abs(Z).max() * 2) / 2

    gcols = [OI["orange"], OI["blue"], OI["green"], OI["purple"]]
    bcols = ["#DCDCDC", "#9A9A9A", "#4D4D4D"]

    fig = plt.figure(figsize=(5.6, 3.3))
    gs = fig.add_gridspec(3, 1, height_ratios=[0.30, 0.13, 2.0], hspace=0.13)
    axg, axb, axm = (fig.add_subplot(gs[i]) for i in range(3))

    axg.imshow(gidx[None, :], aspect="auto", cmap=ListedColormap(gcols), vmin=-0.5, vmax=3.5)
    for j, g in enumerate(groups):
        axg.text(j * per + (per - 1) / 2, 0, g, ha="center", va="center", fontsize=6.5,
                 color="k" if g == "Vehicle" else "white")
    axb.imshow(bidx[None, :], aspect="auto", cmap=ListedColormap(bcols), vmin=-0.5, vmax=2.5)
    for a, lab in ((axg, "treatment"), (axb, "batch")):
        a.set_xticks([]); a.set_yticks([])
        a.set_ylabel(lab, rotation=0, ha="right", va="center", fontsize=6.5, labelpad=4)
        for sp in a.spines.values():
            sp.set_visible(False)

    im = axm.imshow(Z, aspect="auto", cmap=DIV, vmin=-v, vmax=v, interpolation="nearest")
    axm.set_yticks(np.arange(ng)); axm.set_yticklabels(genes, fontsize=6)
    axm.set_xticks([])
    axm.set_xlabel("samples (n = 24), ordered by treatment group", labelpad=2)
    for j in range(1, 4):                                    # thin dividers between groups
        axm.axvline(j * per - 0.5, color="white", lw=1.0)
    cb = fig.colorbar(im, ax=[axg, axb, axm], fraction=0.046, pad=0.04, shrink=0.76,
                      anchor=(0.0, 0.0), label="row z-score (log2 CPM)")
    cb.set_ticks([-v, -v / 2, 0, v / 2, v]); cb.ax.tick_params(labelsize=6.5)

    axm.legend(handles=[Patch(facecolor=c, edgecolor="k", linewidth=0.3, label=f"run {i + 1}")
                        for i, c in enumerate(bcols)],
               title="batch", loc="upper left", bbox_to_anchor=(0.0, -0.13), ncol=3,
               fontsize=6, title_fontsize=6.5, handlelength=1.1, handleheight=0.9,
               handletextpad=0.4, columnspacing=1.2, borderpad=0.0)
    title(axg, "Expression heatmap with sample annotation tracks")
    save(fig, "J06_heatmap_tracks", "matrix + categorical sample tracks", "Omics-Cytometry")

def omics_flow_gating():
    """Each panel plots only what the previous gate kept, so the whole % chain is auditable."""
    from matplotlib.path import Path
    n = 9000
    kind = RNG.choice([0, 1, 2], n, p=[0.80, 0.13, 0.07])        # 0 cell, 1 debris, 2 doublet
    fsc_a = np.where(kind == 0, RNG.normal(2.10, 0.42, n),
                     np.where(kind == 1, RNG.normal(0.45, 0.22, n), RNG.normal(3.60, 0.50, n)))
    fsc_a = np.clip(fsc_a, 0.02, 5.0)
    ssc_a = np.where(kind == 0, RNG.normal(120, 38, n),
                     np.where(kind == 1, RNG.normal(45, 42, n), RNG.normal(190, 55, n)))
    ssc_a = np.clip(ssc_a, 1, 320)
    fsc_h = np.where(kind == 2, 0.62 * fsc_a, 0.93 * fsc_a) + RNG.normal(0, 0.09, n)
    dead = RNG.random(n) < 0.11
    viab = np.where(dead, RNG.normal(4.30, 0.35, n), RNG.normal(2.20, 0.30, n))
    sub = RNG.choice([0, 1, 2], n, p=[0.44, 0.30, 0.26])         # CD4+, CD8+, double-negative
    cd4 = np.where(sub == 0, RNG.normal(4.40, 0.30, n), RNG.normal(2.30, 0.32, n))
    cd8 = np.where(sub == 1, RNG.normal(4.50, 0.30, n), RNG.normal(2.30, 0.32, n))

    # gate 1 removes debris but deliberately KEEPS doublets — gate 2 is what removes those
    g1 = [(0.90, 12), (0.90, 215), (2.20, 278), (4.55, 278), (4.80, 120), (3.60, 15)]
    g2 = [(0.75, 0.50), (4.90, 4.36), (4.90, 4.78), (0.75, 0.92)]
    THR_V, THR_Q = 3.20, 3.20
    idx = np.arange(n)
    in1 = Path(g1).contains_points(np.c_[fsc_a, ssc_a]); i1 = idx[in1]; p1 = 100 * in1.mean()
    in2 = Path(g2).contains_points(np.c_[fsc_a[i1], fsc_h[i1]]); i2 = i1[in2]; p2 = 100 * in2.mean()
    in3 = viab[i2] < THR_V; i3 = i2[in3]; p3 = 100 * in3.mean()
    q4 = (cd4[i3] > THR_Q) & (cd8[i3] < THR_Q); q8 = (cd8[i3] > THR_Q) & (cd4[i3] < THR_Q)
    p4, p8 = 100 * q4.mean(), 100 * q8.mean()

    def dens(x, y, bins=44):                                     # local event density -> point colour
        H, xe, ye = np.histogram2d(x, y, bins=bins)
        ix = np.clip(np.digitize(x, xe) - 1, 0, bins - 1)
        iy = np.clip(np.digitize(y, ye) - 1, 0, bins - 1)
        return H[ix, iy]

    def cloud(ax, x, y):
        d = dens(x, y); o = np.argsort(d)
        ax.scatter(x[o], y[o], c=d[o], cmap=SEQ, s=1.3, linewidths=0, rasterized=True)

    def gate_label(ax, s, corner):                               # always into an emptied corner
        x, ha = (0.03, "left") if corner[1] == "l" else (0.97, "right")
        y, va = (0.97, "top") if corner[0] == "t" else (0.03, "bottom")
        ax.text(x, y, s, transform=ax.transAxes, ha=ha, va=va, fontsize=6, color=OI["vermillion"])

    fig, axs = plt.subplots(1, 4, figsize=(6.4, 2.35))
    cloud(axs[0], fsc_a, ssc_a)
    axs[0].plot(*np.array(g1 + [g1[0]]).T, color=OI["vermillion"], lw=0.9)
    axs[0].set_xlabel("FSC-A ($10^6$)", fontsize=7); axs[0].set_ylabel("SSC-A ($10^3$)", fontsize=7)
    axs[0].set_xticks([0, 2, 4]); axs[0].set_yticks([0, 150, 300])
    axs[0].set_ylim(0, 430); gate_label(axs[0], f"Cells\n{p1:.1f}%", "tl")

    cloud(axs[1], fsc_a[i1], fsc_h[i1])
    axs[1].plot(*np.array(g2 + [g2[0]]).T, color=OI["vermillion"], lw=0.9)
    axs[1].set_xlabel("FSC-A ($10^6$)", fontsize=7); axs[1].set_ylabel("FSC-H ($10^6$)", fontsize=7)
    axs[1].set_xticks([1, 2, 3, 4]); axs[1].set_yticks([1, 2, 3, 4])
    axs[1].set_ylim(0.1, 6.6); gate_label(axs[1], f"Singlets\n{p2:.1f}%", "tl")

    cloud(axs[2], viab[i2], ssc_a[i2])
    axs[2].plot([1.30, THR_V, THR_V, 1.30, 1.30], [10, 10, 265, 265, 10], color=OI["vermillion"], lw=0.9)
    axs[2].set_xlabel("Viability dye", fontsize=7); axs[2].set_ylabel("SSC-A ($10^3$)", fontsize=7)
    axs[2].set_xticks([2, 3, 4]); axs[2].set_xticklabels(["$10^2$", "$10^3$", "$10^4$"])
    axs[2].set_yticks([0, 150, 300]); axs[2].set_ylim(0, 430)
    gate_label(axs[2], f"Live\n{p3:.1f}%", "tl")

    cloud(axs[3], cd4[i3], cd8[i3])
    axs[3].axvline(THR_Q, color=OI["vermillion"], lw=0.9); axs[3].axhline(THR_Q, color=OI["vermillion"], lw=0.9)
    axs[3].set_xlabel("CD4-BUV395", fontsize=7); axs[3].set_ylabel("CD8-BV711", fontsize=7)
    axs[3].set_xticks([2, 3, 4, 5]); axs[3].set_xticklabels(["$10^2$", "$10^3$", "$10^4$", "$10^5$"])
    axs[3].set_yticks([2, 3, 4, 5]); axs[3].set_yticklabels(["$10^2$", "$10^3$", "$10^4$", "$10^5$"])
    # limits opened by the data itself, so both quadrant labels land in provably event-free margins
    xl, xr = cd4[i3].min() - 0.4, cd4[i3].max() + 1.8
    yb, yt = cd8[i3].min() - 0.4, cd8[i3].max() + 1.5
    axs[3].set_xlim(xl, xr); axs[3].set_ylim(yb, yt)
    axs[3].text(xl + 0.03 * (xr - xl), yt - 0.03 * (yt - yb), f"CD8+\n{p8:.1f}%", ha="left",
                va="top", fontsize=6, color=OI["vermillion"])    # band above every event
    axs[3].text(xr - 0.02 * (xr - xl), 0.5 * (yb + THR_Q), f"CD4+\n{p4:.1f}%", ha="right",
                va="center", fontsize=6, color=OI["vermillion"])  # band right of every event

    for ax in axs:
        ax.tick_params(labelsize=5.8, length=2)
    fig.suptitle("Sequential gating strategy (% of parent kept)", x=0.012, y=0.995, ha="left", fontsize=8.5)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.subplots_adjust(wspace=0.66)
    fig.canvas.draw()                                            # tight bboxes include tick labels
    r = fig.canvas.get_renderer(); inv = fig.transFigure.inverted()
    for a, b in zip(axs[:-1], axs[1:]):                          # parent -> child arrows, clear of labels
        xa = inv.transform(a.get_tightbbox(r).p1)[0]
        xb = inv.transform(b.get_tightbbox(r).p0)[0]
        pa = a.get_position(); mid = 0.5 * (xa + xb)
        half = max(0.006, min(0.017, 0.36 * (xb - xa)))
        fig.add_artist(FancyArrowPatch((mid - half, 0.5 * (pa.y0 + pa.y1)),
                                       (mid + half, 0.5 * (pa.y0 + pa.y1)),
                                       transform=fig.transFigure, arrowstyle="-|>",
                                       mutation_scale=7, lw=0.9, color="k"))
    save(fig, "J07_flow_gating", "sequential gating strategy with % kept", "Omics-Cytometry")


# ============================================================ A. DISTRIBUTIONS (reference-corpus additions)

def dist_psd_percentiles():
    """A volume-weighted size distribution whose D10/D50/D90 and span are read off its own cumulative curve."""
    # --- synthetic laser-diffraction measurement of a nanoparticle prep --------------
    sigma = 0.358                                     # log-normal shape (breadth of the prep)
    target = 120.0                                    # nm, intended volume-median diameter
    mu = np.log(target) - 3 * sigma ** 2              # number-median chosen so the VOLUME median lands on target
    d = np.exp(RNG.normal(mu, sigma, 2_500_000))      # particle population, number-weighted
    edges = np.logspace(np.log10(20), np.log10(1000), 81)
    vol, _ = np.histogram(d, bins=edges, weights=d ** 3)      # q3 = volume weighting
    frac = 100.0 * vol / vol.sum()                            # % of total volume in each bin
    Q3 = np.concatenate([[0.0], np.cumsum(frac)])             # cumulative undersize, at bin EDGES
    ctr = np.sqrt(edges[:-1] * edges[1:])                     # geometric bin centres
    q3 = frac / np.diff(np.log10(edges))                      # density dQ3/dlog d

    # --- percentiles INVERTED FROM THE PLOTTED CUMULATIVE CURVE (never typed in) -----
    d10, d50, d90 = np.interp([10.0, 50.0, 90.0], Q3, edges)
    span = (d90 - d10) / d50

    fig, ax = plt.subplots(figsize=(3.8, 2.9))
    ax.set_xscale("log")
    ax.fill_between(ctr, q3, color=OI["blue"], alpha=0.16, linewidth=0)
    ax.plot(ctr, q3, color=OI["blue"], lw=1.5)
    ax.set_xlim(30, 500); ax.set_ylim(0, q3.max() * 1.30)
    ax.set_xlabel("Particle diameter (nm)")
    ax.set_ylabel("Volume density d$Q_3$/dlog d (%)", color=OI["blue"])
    ax.tick_params(axis="y", colors=OI["blue"])
    ax.spines["left"].set_color(OI["blue"])
    ax.set_xticks([30, 50, 100, 200, 500])
    ax.set_xticklabels(["30", "50", "100", "200", "500"])
    ax.set_xticks([], minor=True)

    ax2 = ax.twinx()                                          # the real idiom: cumulative undersize alongside
    ax2.plot(edges, Q3, color=OI["orange"], lw=1.4, zorder=3)
    # headroom above the 100% plateau: the percentile tags live there, clear of BOTH curves
    ax2.set_ylim(0, 126); ax2.set_yticks([0, 10, 50, 90, 100])
    ax2.set_ylabel("Cumulative undersize $Q_3$ (%)", color=OI["orange"])
    ax2.tick_params(axis="y", colors=OI["orange"])
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(True); ax2.spines["right"].set_color(OI["orange"])
    for t in ax2.get_xticklabels():      # twinx hides its x-axis but leaves the label artists flagged
        t.set_visible(False)             # visible; only ax draws the shared x ticks

    # droplines, each tagged above the plateau: three distinct x, so no two tags can collide
    for dv, pct in [(d10, 10), (d50, 50), (d90, 90)]:
        ax2.vlines(dv, 0, 107, color=OI["grey"], lw=0.7, ls=(0, (2.5, 2)), zorder=2)
        ax2.plot([dv], [pct], marker="o", ms=3.6, color=OI["orange"],
                 mec="white", mew=0.7, zorder=4)
        ax2.text(dv, 116, f"$D_{{{pct}}}$\n{dv:.0f} nm", ha="center", va="center",
                 fontsize=6.5, linespacing=1.35, zorder=5)
    ax2.text(0.985, 0.32, f"span = ($D_{{90}}$-$D_{{10}}$)/$D_{{50}}$\n= {span:.2f}",
             transform=ax2.transAxes, ha="right", va="bottom", fontsize=6, linespacing=1.5)
    title(ax, "Size distribution with percentile readout")
    save(fig, "A20_psd_percentiles", "size distribution with D10/D50/D90", "Distributions")



# ============================================================ B. CORRELATION (reference-corpus additions)

def corr_distribution_overlap():
    """How much two biomarker distributions actually coincide, integrated from the plotted curves."""
    # ---- synthetic exposure cohort: day-14 trough concentration, responders vs non-responders
    n_nr, n_r = 64, 72
    s_nr = RNG.normal(62.0, 12.0, n_nr)
    s_r = RNG.normal(78.0, 14.0, n_r)
    m1, sd1 = s_nr.mean(), s_nr.std(ddof=1)
    m2, sd2 = s_r.mean(), s_r.std(ddof=1)

    lo = min(m1 - 4.6 * sd1, m2 - 4.6 * sd2)
    hi = max(m1 + 4.6 * sd1, m2 + 4.6 * sd2)
    xg = np.linspace(lo, hi, 4001)
    f1 = stats.norm.pdf(xg, m1, sd1)
    f2 = stats.norm.pdf(xg, m2, sd2)
    fmin = np.minimum(f1, f2)

    # ---- every number printed below is a numerical integral over the PLOTTED curves
    ovl = np.trapezoid(fmin, xg)                                    # overlap coefficient, in [0, 1]
    mu1 = np.trapezoid(xg * f1, xg); v1 = np.trapezoid((xg - mu1) ** 2 * f1, xg)
    mu2 = np.trapezoid(xg * f2, xg); v2 = np.trapezoid((xg - mu2) ** 2 * f2, xg)
    d = (mu2 - mu1) / np.sqrt((v1 + v2) / 2)                        # Cohen's d
    F1 = np.concatenate(([0.0], np.cumsum((f1[:-1] + f1[1:]) / 2 * np.diff(xg))))
    auc = np.trapezoid(f2 * F1, xg)                                 # P(responder > non-responder)

    # ---- decision threshold: where the two plotted densities cross, between the two modes
    g = f2 - f1
    cross = [i for i in np.where(np.diff(np.sign(g)))[0] if min(m1, m2) < xg[i] < max(m1, m2)]
    i0 = cross[0]
    xstar = xg[i0] + (xg[i0 + 1] - xg[i0]) * (-g[i0]) / (g[i0 + 1] - g[i0])
    ystar = np.interp(xstar, xg, f1)

    fig, ax = plt.subplots(figsize=(3.8, 2.9))
    ax.fill_between(xg, fmin, color=OI["grey"], alpha=0.45, linewidth=0,
                    label=f"overlap $\\int$min($f_1$,$f_2$)d$x$ = {ovl:.2f}")
    ax.plot(xg, f1, color=OI["blue"], lw=1.4, label=f"Non-responders (n = {n_nr})")
    ax.plot(xg, f2, color=OI["orange"], lw=1.4, label=f"Responders (n = {n_r})")
    top = max(f1.max(), f2.max()) * 1.62
    ax.plot(s_nr, np.full(n_nr, -0.030 * top), "|", ms=3.2, mew=0.6, color=OI["blue"])
    ax.plot(s_r, np.full(n_r, -0.062 * top), "|", ms=3.2, mew=0.6, color=OI["orange"])
    ax.axvline(xstar, color="0.35", ls="--", lw=0.8, zorder=0)
    ax.plot([xstar], [ystar], marker="o", ms=3.2, color="0.2", zorder=5)
    ax.text(xstar + 0.010 * (hi - lo), ystar + 0.035 * top, "$x^*$",
            ha="left", va="bottom", fontsize=6.5, color="0.25")
    ax.text(0.985, 0.97, f"AUC = {auc:.2f}\nCohen's $d$ = {d:.2f}\n"
                         f"$x^*$ = {xstar:.0f} ng mL$^{{-1}}$", transform=ax.transAxes,
            ha="right", va="top", fontsize=6.5, linespacing=1.5)
    ax.legend(loc="upper left", fontsize=6.2, handlelength=1.5, borderaxespad=0.2,
              labelspacing=0.35)
    ax.set_ylim(-0.085 * top, top)
    ax.set_xlim(lo, hi)
    ax.set_yticks(np.arange(0, f1.max() * 1.2, 0.01))
    ax.set_xlabel("Day-14 trough concentration (ng mL$^{-1}$)")
    ax.set_ylabel("Probability density (mL ng$^{-1}$)")
    title(ax, "Distribution overlap, quantified")
    save(fig, "B18_distribution_overlap", "quantified overlap of two distributions", "Correlation")



# ============================================================ G. SCIENTIFIC (reference-corpus additions)

def sci_annotated_spectrum():
    """A spectrum whose band labels are placed at peaks located in the array, not at typed constants."""
    from scipy.signal import find_peaks
    # ---- synthetic FTIR trace of a drug-loaded PLGA nanoparticle, 1000-1800 cm-1 at 1 cm-1
    wn = np.arange(1000.0, 1801.0, 1.0)
    bands = [(1748.0, 0.85, 11.0), (1652.0, 0.56, 17.0),
             (1541.0, 0.36, 15.0), (1088.0, 0.48, 22.0)]
    absorb = 0.028 + 2.4e-5 * (wn - 1000.0)                         # positive, gently sloping baseline
    for c, a, s in bands:
        absorb = absorb + a * np.exp(-0.5 * ((wn - c) / s) ** 2)
    absorb = absorb + RNG.normal(0, 0.0035, wn.size)

    # ---- peak positions come from the array; only the chemistry of the assignment is prior knowledge
    idx, props = find_peaks(absorb, prominence=0.05, distance=25)
    order = np.argsort(props["prominences"])[::-1][:4]
    idx = np.sort(idx[order])
    assign = {1748: "ester C=O (PLGA)", 1652: "amide I (C=O)",
              1541: "amide II (N–H)", 1088: "C–O–C stretch"}
    ytxt = {1748: 1.42, 1652: 1.22, 1541: 1.02, 1088: 0.80}

    fig, ax = plt.subplots(figsize=(3.8, 3.0))
    ax.plot(wn, absorb, color=OI["blue"], lw=1.0)
    for i in idx:
        px, py = wn[i], absorb[i]
        key = min(assign, key=lambda k: abs(k - px))                # nearest assignment in the table
        side = "right" if px < 1200 else "left"
        ax.plot([px], [py], marker="o", ms=3.0, mfc="none", mec="0.2", mew=0.7, zorder=4)
        ax.annotate(f"{px:.0f} cm$^{{-1}}$  {assign[key]}", xy=(px, py + 0.035),
                    xytext=(px, ytxt[key]), ha=side, va="center", fontsize=6, color="0.15",
                    arrowprops=dict(arrowstyle="-", lw=0.5, color="0.45", shrinkA=1.5, shrinkB=1.5))
    ax.set_xlim(1800, 1000)                                         # FTIR convention: wavenumber decreasing
    ax.set_ylim(0, 1.55)
    ax.set_xticks(np.arange(1000, 1801, 200))
    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Absorbance (a.u.)")
    title(ax, "FTIR of drug-loaded PLGA NP: assigned bands")
    save(fig, "G21_annotated_spectrum", "spectrum with assigned bands", "Scientific")



# ============================================================ I. SPECIALIZED (reference-corpus additions)

def spec_biodistribution_route():
    """Where an i.v. dose actually goes: route, circulation, then organs each carrying its share of the dose."""
    from matplotlib.lines import Line2D

    ROLE = {"mps": OI["vermillion"], "target": OI["green"], "other": OI["sky"]}
    ROLE_LAB = {"mps": "mononuclear phagocyte system", "target": "tumour (target)",
                "other": "other tissue / carcass"}
    blood = 18.4                                              # %ID still circulating at 24 h
    organs = [("Liver", 27.6, "mps"), ("Carcass + other", 25.5, "other"), ("Spleen", 12.3, "mps"),
              ("Tumour", 6.8, "target"), ("Kidney", 4.5, "other"), ("Lung", 3.2, "other"),
              ("Heart", 1.7, "other")]
    assert abs(blood + sum(o[1] for o in organs) - 100.0) < 1e-9, "recovered dose must close on 100 %ID"

    X0, SCALE = 6.50, 0.0851                                  # bar origin (zero-based) and %ID -> data units
    rows = list(range(len(organs) - 1, -1, -1))               # y = 6 (Liver) down to 0 (Heart)

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.set_xlim(0, 10.0); ax.set_ylim(-1.15, 7.35); ax.axis("off")

    def node(x, y, s):
        return ax.text(x, y, s, ha="center", va="center", fontsize=6.5, zorder=4,
                       bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                                 edgecolor=OI["grey"], linewidth=0.8))

    node(0.80, 3.0, "i.v. bolus")
    ax.text(0.80, 2.30, "5 mg/kg, tail vein", ha="center", va="center", fontsize=6, color=OI["grey"])
    node(3.45, 3.0, "systemic\ncirculation")
    ax.text(3.10, 2.15, f"blood pool {blood} %ID", ha="center", va="center", fontsize=6, color=OI["grey"])

    # nanoparticle glyphs ride the injection route -- a band that carries NO text.
    # point-sized markers, not Circle patches: they stay round on a free-aspect axes.
    ax.plot([1.62, 1.80, 1.98, 2.16], [3.0] * 4, marker="o", ms=3.2, ls="none",
            color=OI["blue"], zorder=3)
    ax.add_patch(FancyArrowPatch((2.34, 3.0), (2.62, 3.0), arrowstyle="-|>", mutation_scale=7,
                                 lw=0.9, color=OI["blue"], zorder=3))
    names = []
    for y, (nm, pct, role) in zip(rows, organs):              # label | bar | value -> three disjoint x-bands
        names.append(ax.text(6.30, y, nm, ha="right", va="center", fontsize=6.5))
        ax.add_patch(Rectangle((X0, y - 0.21), pct * SCALE, 0.42, facecolor=ROLE[role],
                               edgecolor="none", zorder=2))
        ax.text(X0 + pct * SCALE + 0.12, y, f"{pct:.1f}", ha="left", va="center", fontsize=6.5)
    ax.text(X0, 6.85, "bar length = % of injected dose (24 h)", ha="left", va="center", fontsize=6,
            color=OI["grey"])

    # distribution bus: a trunk plus purely horizontal stubs. A diagonal fan would have to sweep
    # across neighbouring rows; a horizontal stub can only ever reach its OWN row's label.
    TRUNK = 4.40
    ax.plot([4.10, TRUNK], [3.0, 3.0], color=OI["grey"], lw=0.7, zorder=1)
    ax.plot([TRUNK, TRUNK], [min(rows), max(rows)], color=OI["grey"], lw=0.7, zorder=1)
    fig.canvas.draw()                                         # measure each name so its arrow stops just short of it
    rend = fig.canvas.get_renderer(); inv = ax.transData.inverted()
    for y, t in zip(rows, names):
        xl = float(inv.transform((t.get_window_extent(rend).x0, 0.0))[0])
        ax.add_patch(FancyArrowPatch((TRUNK, y), (xl - 0.18, y), arrowstyle="-|>", mutation_scale=6,
                                     lw=0.7, color=OI["grey"], zorder=1))

    ax.legend(handles=[Line2D([], [], marker="s", ls="none", ms=4.5, color=ROLE[k]) for k in ROLE],
              labels=[ROLE_LAB[k] for k in ROLE], loc="lower left", fontsize=6,
              handlelength=1.0, handletextpad=0.5, labelspacing=0.45, borderpad=0.0)
    title(ax, "Route of administration and organ fate")
    save(fig, "I11_biodistribution_route", "route of administration and organ fate", "Specialized")

def spec_mechanism_cartoon():
    """Panel-a orientation cartoon: a ligand seated on its receptor, then the four steps that follow it inside."""
    from matplotlib.lines import Line2D
    from matplotlib.patches import Arc

    MEM, LIG, CARGO = OI["grey"], OI["orange"], OI["vermillion"]
    Y0, DEPTH, WID, T = 2.62, 0.76, 0.78, 0.13                # membrane level, pit depth/width, bilayer thickness
    XP, R, LG = 4.55, 0.34, 0.055                             # pit centre, particle radius, ligand stub length

    def mem(x):                                               # bilayer centreline, dimpled at the pit
        return Y0 - DEPTH * np.exp(-((np.asarray(x, float) - XP) / WID) ** 2)

    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    ax.set_xlim(0, 12.8); ax.set_ylim(0, 5.0); ax.axis("off")
    ax.set_aspect("equal")                                    # spheres must render as circles, not ellipses

    xm = np.linspace(0, 12.8, 1100); ym = mem(xm)
    ax.fill_between(xm, ym - T / 2, ym + T / 2, facecolor=MEM, alpha=0.30, linewidth=0, zorder=1)
    for off in (-T / 2, T / 2):                               # two leaflets -> reads as a bilayer, not an axis rule
        ax.plot(xm, ym + off, color=MEM, lw=1.0, zorder=2)
    ax.text(0.12, 4.82, "Extracellular", ha="left", va="center", fontsize=6.5, color=OI["grey"])
    ax.text(0.12, 0.30, "Cytosol", ha="left", va="center", fontsize=6.5, color=OI["grey"])

    def particle(cx, cy, rad, ligand_angles, z=5):
        for a in ligand_angles:                               # ligand stubs, drawn from the particle surface out
            t = np.deg2rad(a)
            ax.plot([cx + rad * np.cos(t), cx + (rad + LG) * np.cos(t)],
                    [cy + rad * np.sin(t), cy + (rad + LG) * np.sin(t)],
                    color=LIG, lw=1.0, solid_capstyle="round", zorder=z)
        ax.add_patch(Circle((cx, cy), rad, facecolor=OI["blue"], edgecolor="white",
                            linewidth=0.7, zorder=z + 1))

    # ---- 1 BIND: receptor arms terminate EXACTLY on the ligand tips (contact by construction)
    CX1, CY1, YOKE = 1.85, 3.61, 3.05
    th = np.deg2rad([235.0, 305.0])
    tips = np.column_stack([CX1 + (R + LG) * np.cos(th), CY1 + (R + LG) * np.sin(th)])
    ax.plot([CX1, CX1], [mem(CX1) + T / 2, YOKE], color=OI["orange"], lw=1.8,
            solid_capstyle="round", zorder=3)
    for tx, ty in tips:
        ax.plot([CX1, tx], [YOKE, ty], color=OI["orange"], lw=1.8, solid_capstyle="round", zorder=3)
    particle(CX1, CY1, R, [235, 305, 20, 70, 120, 165])

    # ---- 2 INTERNALISE: particle seated on the upper leaflet inside the invagination
    CY2 = mem(XP) + T / 2 + R
    particle(XP, CY2, R, [200, 250, 290, 340, 40, 140])

    # ---- 3 TRAFFIC and 4 RELEASE: closed endosome, then one whose wall has opened
    V3, V4 = (7.30, 1.42, 0.46), (9.90, 1.05, 0.44)
    for cx, cy, rad in (V3, V4):
        ax.add_patch(Circle((cx, cy), rad, facecolor="white", edgecolor="none", zorder=4))
    ax.add_patch(Circle(V3[:2], V3[2], facecolor="none", edgecolor=MEM, lw=1.6, zorder=5))
    ax.add_patch(Circle(V3[:2], 0.27, facecolor=OI["blue"], edgecolor="white", lw=0.6, zorder=6))
    ax.add_patch(Arc(V4[:2], 2 * V4[2], 2 * V4[2], theta1=58, theta2=372,   # gap in the wall -> it has opened
                     edgecolor=MEM, lw=1.6, zorder=5))
    ax.add_patch(Circle(V4[:2], 0.25, facecolor=OI["blue"], edgecolor="white", lw=0.6, alpha=0.45, zorder=6))
    for k, rr in enumerate([0.58, 0.76, 0.96, 1.18]):         # cargo escaping through the opening
        a = np.deg2rad(25 + 4 * k)
        ax.add_patch(Circle((V4[0] + rr * np.cos(a), V4[1] + rr * np.sin(a)), 0.070 - 0.010 * k,
                            facecolor=CARGO, edgecolor="none", zorder=6))

    for (xa, ya), (xb, yb), rad in [((2.42, 3.88), (4.15, 2.72), 0.20),
                                    ((5.10, 1.70), (6.78, 1.52), -0.18),
                                    ((7.84, 1.16), (9.40, 1.18), -0.15)]:
        ax.add_patch(FancyArrowPatch((xa, ya), (xb, yb), arrowstyle="-|>", mutation_scale=8,
                                     lw=1.0, color=OI["black"], zorder=7,
                                     connectionstyle=f"arc3,rad={rad}"))

    for n, (bx, by, word) in enumerate([(1.25, 4.22, "bind"), (5.25, 2.98, "internalise"),
                                        (6.75, 0.62, "traffic"), (9.30, 0.26, "release")], start=1):
        ax.text(bx, by, str(n), ha="center", va="center", fontsize=6, color="white", zorder=9,
                bbox=dict(boxstyle="circle,pad=0.30", facecolor=OI["black"], edgecolor="none"))
        ax.text(bx + 0.26, by, word, ha="left", va="center", fontsize=6.5, zorder=9)

    ax.legend(handles=[Line2D([], [], marker="o", ls="none", ms=5, color=OI["blue"]),
                       Line2D([], [], marker="_", ls="none", ms=7, mew=1.8, color=OI["orange"]),
                       Line2D([], [], marker="_", ls="none", ms=7, mew=1.8, color=MEM),
                       Line2D([], [], marker="o", ls="none", ms=4, color=CARGO)],
              labels=["nanoparticle", "ligand / receptor", "lipid bilayer", "released cargo"],
              loc="upper right", fontsize=6, handlelength=1.0, handletextpad=0.5,
              labelspacing=0.4, borderpad=0.0)
    title(ax, "Receptor binding and uptake pathway")
    save(fig, "I12_mechanism_cartoon", "receptor binding and uptake pathway", "Specialized")



# ============================================================ J. OMICS (reference-corpus additions)

def omics_pca_ellipses():
    """A real SVD of 60 x 30 metabolite data, with each group's 95% ellipse built from its own covariance."""
    from matplotlib.patches import Ellipse
    n_per, p = 20, 30
    groups = ["Vehicle", "Low dose", "High dose"]
    lab = np.repeat(np.arange(3), n_per)
    n = lab.size
    # two latent programmes drive group structure; the remaining features are noise
    dose = np.array([-1.05, 0.10, 1.00])[lab] + RNG.normal(0, 0.30, n)
    stress = np.array([-0.45, 0.95, -0.35])[lab] + RNG.normal(0, 0.30, n)
    # random loading DIRECTIONS, fixed loading STRENGTH, so the variance split does not
    # drift with the shared RNG's position in the gallery build
    w1 = np.zeros(p); w1[:11] = RNG.normal(0, 1.0, 11); w1 *= 2.9 / np.linalg.norm(w1)
    w2 = np.zeros(p); w2[8:20] = RNG.normal(0, 1.0, 12); w2 *= 2.6 / np.linalg.norm(w2)
    X = np.outer(dose, w1) + np.outer(stress, w2) + RNG.normal(0, 0.75, (n, p))

    # ---- autoscale, then an actual decomposition; the axis percentages come from S
    Z = (X - X.mean(0)) / X.std(0, ddof=1)
    U, S, Vt = np.linalg.svd(Z, full_matrices=False)
    scores = U * S
    var = S ** 2 / np.sum(S ** 2)
    k95 = stats.chi2.ppf(0.95, 2)

    fig, ax = plt.subplots(figsize=(3.7, 3.1))
    xs, ys = [], []
    for k, gname in enumerate(groups):
        pts = scores[lab == k][:, :2]
        ctr = pts.mean(0)
        cov = np.cov(pts.T)
        ev, evec = np.linalg.eigh(cov)
        o = np.argsort(ev)[::-1]; ev, evec = ev[o], evec[:, o]
        ang = np.degrees(np.arctan2(evec[1, 0], evec[0, 0]))
        w, h = 2 * np.sqrt(k95 * ev)
        ax.add_patch(Ellipse(tuple(ctr), w, h, angle=ang, facecolor=CYCLE[k], alpha=0.10,
                             edgecolor=CYCLE[k], lw=0.9, ls="--", zorder=1))
        ax.scatter(pts[:, 0], pts[:, 1], s=17, color=CYCLE[k], edgecolor="k", linewidth=0.3,
                   alpha=0.9, label=gname, zorder=3)
        ax.plot([ctr[0]], [ctr[1]], marker="+", ms=5.5, mew=1.1, color="k", zorder=4)
        rx, ry = np.sqrt(k95 * cov[0, 0]), np.sqrt(k95 * cov[1, 1])
        xs += [ctr[0] - rx, ctr[0] + rx]; ys += [ctr[1] - ry, ctr[1] + ry]
    xs += list(scores[:, 0]); ys += list(scores[:, 1])
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    mx, my = 0.07 * (x1 - x0), 0.07 * (y1 - y0)
    ax.set_xlim(x0 - mx, x1 + mx)
    ax.set_ylim(y0 - my, y1 + my + 0.36 * (y1 - y0))                # clear band for the legend
    # prune the lowest y tick so it can never collide with an x tick in the bottom-left corner
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(6, prune="lower"))
    ax.plot([], [], ls="--", lw=0.9, color=OI["grey"], label="95% ellipse ($\\chi^2$, 2 df)")
    ax.legend(loc="upper left", fontsize=6.2, handlelength=1.4, borderaxespad=0.2,
              labelspacing=0.32, markerscale=0.85)
    ax.set_xlabel(f"PC1 ({var[0] * 100:.1f}% of variance)")
    ax.set_ylabel(f"PC2 ({var[1] * 100:.1f}% of variance)")
    title(ax, f"PCA scores + 95% group ellipses (n = {n_per}/group, p = {p})")
    save(fig, "J08_pca_ellipses", "PCA scores + group confidence ellipses", "Omics-Cytometry")


# ============================================================ B. CORRELATION (ggplot2 journal-case additions)

def corr_mantel():
    """Lower-triangle Spearman heatmap + Mantel links to community matrices."""
    from matplotlib.lines import Line2D
    import matplotlib.patheffects as pe

    vars_ = ["N", "P", "K", "Ca", "Mg", "S", "Al", "Fe", "Mn", "Zn", "Mo",
             "Baresoil", "Humdepth", "pH"]
    n = len(vars_)
    # synthetic correlated data -> Spearman matrix (COMPUTED from the data)
    X = RNG.normal(size=(80, n)) + RNG.normal(size=(80, 1)) * 0.6
    M = stats.spearmanr(X).correlation
    Mc = np.clip(M, -0.999, 0.999)
    P = 2 * stats.norm.cdf(-np.abs(np.arctanh(Mc)) * np.sqrt(80 - 3))

    # Mantel statistics: synthetic draws (a real Mantel test needs distance matrices)
    specs = ["Spec01", "Spec02", "Spec03"]
    mr = RNG.uniform(0.02, 0.55, (3, n))
    mp = RNG.uniform(0, 1, (3, n))
    msign = RNG.choice(["Positive", "Negative"], size=(3, n), p=[0.7, 0.3])

    cmap = mpl.colormaps[DIV]; norm = mpl.colors.Normalize(-1, 1)
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_xlim(-7.2, 18.2); ax.set_ylim(-14.6, 1.4)

    def star(p):
        return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 5e-2 else ""

    # lower-triangle tiles (row i, col j<i) at (j, -i); asterisks inside
    for i in range(1, n):
        for j in range(i):
            c = cmap(norm(M[i, j]))
            ax.add_patch(mpl.patches.Rectangle((j - 0.5, -i - 0.5), 1, 1,
                         facecolor=c, edgecolor="white", lw=0.4, zorder=1))
            s = star(P[i, j])
            if s:
                lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
                ax.text(j, -i - 0.06, s, ha="center", va="center", fontsize=5.6,
                        color="white" if lum < 0.5 else "0.2", zorder=2)

    # spec community nodes on the right + curved Mantel links from diagonal cells
    spec_x = n + 2.0
    spec_y = {"Spec01": -3.0, "Spec02": -7.0, "Spec03": -11.0}
    rw = {"< 0.2": 0.5, "0.2 - 0.4": 1.0, ">= 0.4": 1.9}
    for si, sp in enumerate(specs):
        for vi in range(n):
            r, p, sg = mr[si, vi], mp[si, vi], msign[si, vi]
            if not (r > 0.28 or p < 0.05):
                continue
            rc = "< 0.2" if r < 0.2 else "0.2 - 0.4" if r < 0.4 else ">= 0.4"
            col = OI["green"] if p < 0.05 else OI["grey"]
            ls = "solid" if sg == "Positive" else (0, (3.5, 1.8))
            ax.add_patch(FancyArrowPatch((vi, -vi), (spec_x, spec_y[sp]),
                         connectionstyle="arc3,rad=-0.32", arrowstyle="-",
                         lw=rw[rc], color=col, linestyle=ls, alpha=0.7, zorder=1))
    for sp in specs:
        ax.scatter([spec_x], [spec_y[sp]], s=42, color=OI["vermillion"],
                   edgecolor="white", lw=0.6, zorder=5)
        ax.text(spec_x + 0.5, spec_y[sp], sp, ha="left", va="center",
                fontsize=7, fontweight="bold", zorder=5)

    # diagonal variable labels (nudged into the empty upper triangle, white halo)
    for k, v in enumerate(vars_):
        t = ax.text(k + 0.42, -k + 0.12, v, ha="center", va="center", fontsize=6.2,
                    fontweight="bold", color="0.1", zorder=4)
        t.set_path_effects([pe.withStroke(linewidth=2.0, foreground="white")])

    # --- three legends + colorbar packed in the empty left column ---
    lh_sign = [Line2D([0], [0], color="0.25", lw=1.3, ls="solid"),
               Line2D([0], [0], color="0.25", lw=1.3, ls=(0, (3.5, 1.8)))]
    l1 = ax.legend(lh_sign, ["Positive", "Negative"], title="Mantel's r sign",
                   loc="upper left", bbox_to_anchor=(0.005, 0.99), fontsize=6,
                   title_fontsize=6.5, handlelength=1.8, labelspacing=0.3, borderpad=0.3)
    ax.add_artist(l1)
    lh_r = [Line2D([0], [0], color="0.25", lw=rw["< 0.2"]),
            Line2D([0], [0], color="0.25", lw=rw["0.2 - 0.4"]),
            Line2D([0], [0], color="0.25", lw=rw[">= 0.4"])]
    l2 = ax.legend(lh_r, ["< 0.2", "0.2 - 0.4", ">= 0.4"], title="Mantel's r",
                   loc="upper left", bbox_to_anchor=(0.005, 0.75), fontsize=6,
                   title_fontsize=6.5, handlelength=1.8, labelspacing=0.3, borderpad=0.3)
    ax.add_artist(l2)
    lh_p = [Line2D([0], [0], color=OI["green"], lw=1.5),
            Line2D([0], [0], color=OI["grey"], lw=1.5)]
    l3 = ax.legend(lh_p, ["< 0.05", ">= 0.05"], title="Mantel's p",
                   loc="upper left", bbox_to_anchor=(0.005, 0.50), fontsize=6,
                   title_fontsize=6.5, handlelength=1.8, labelspacing=0.3, borderpad=0.3)
    ax.add_artist(l3)

    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    cax = ax.inset_axes([0.02, 0.06, 0.20, 0.03])
    cb = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cb.set_ticks([-1, 0, 1]); cb.ax.tick_params(labelsize=6, length=2)
    cb.set_label("Spearman's r", fontsize=6.5)
    cb.outline.set_linewidth(0.5)

    title(ax, "Mantel composite (soil variables x communities)")
    save(fig, "B19_mantel", "correlation heatmap + Mantel links", "Correlation")



# ============================================================ C. COMPARISON (ggplot2 journal-case additions)

def comp_cld_bars():
    """Grouped mean+/-s.d. bars with compact-letter-display significance groups."""
    conditions = ["Formulation A", "Formulation B", "Formulation C"]
    timepts = ["0 mo", "6 mo", "12 mo", "24 mo"]
    tcol = [OI["sky"], OI["blue"], OI["orange"], OI["vermillion"]]
    nrep = 4
    nc, nt = len(conditions), len(timepts)

    # synthetic replicate-level potencies: gamma cell means, replicate scatter from the s.d.
    cell_mu = np.maximum(0.4, RNG.gamma(shape=4.0, scale=0.42, size=(nc, nt)))
    cell_sd = cell_mu * RNG.uniform(0.08, 0.20, size=(nc, nt))
    reps = np.maximum(0.05, RNG.normal(cell_mu[..., None], cell_sd[..., None], size=(nc, nt, nrep)))
    means = reps.mean(axis=2)
    sds = reps.std(axis=2, ddof=1)

    # --- compact letter display (ILLUSTRATIVE of the CLD idiom) ---------------
    # Letters are assigned by a deterministic 1-D rule over the 12 cell means: bars whose means
    # differ by less than `thresh` share a letter (a Tukey-style "not significantly different"
    # grouping). Bars that share NO letter are the significant contrasts. thresh is tied to the
    # pooled replicate s.d. so the letters track the plotted error bars. This is a reproducible
    # stand-in for a real post-hoc test, not a computed p-value.
    flat = means.ravel()
    thresh = 2.6 * float(np.mean(sds))            # ~Tukey HSD scale from the pooled s.d.

    def cld_letters(values, thr):
        vals = np.asarray(values, float)
        order = np.argsort(vals)[::-1]            # descending: 'a' = highest group
        v = vals[order]
        n = len(v)
        far = [max((j for j in range(i, n) if v[i] - v[j] < thr), default=i) for i in range(n)]
        runs, prev = [], -1                       # keep only maximal contiguous runs
        for i in range(n):
            if far[i] > prev:
                runs.append((i, far[i])); prev = far[i]
        lab = [""] * n
        for k, (a, b) in enumerate(runs):
            ch = chr(ord("a") + k)
            for idx in range(a, b + 1):
                lab[idx] += ch
        out = [""] * n
        for pos, orig in enumerate(order):
            out[orig] = lab[pos]
        return out

    letters = np.array(cld_letters(flat, thresh)).reshape(nc, nt)

    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    width = 0.185
    offs = (np.arange(nt) - (nt - 1) / 2) * width
    xc = np.arange(nc)
    for t in range(nt):
        xpos = xc + offs[t]
        ax.bar(xpos, means[:, t], width, yerr=sds[:, t], color=tcol[t], label=timepts[t],
               error_kw=dict(elinewidth=0.8, capsize=2, capthick=0.8, ecolor=OI["black"]), zorder=2)
        for c in range(nc):
            jit = (RNG.uniform(-1, 1, nrep)) * width * 0.30
            ax.plot(xpos[c] + jit, reps[c, t], marker="o", linestyle="none", markersize=2.6,
                    markerfacecolor=OI["black"], markeredgecolor="none", alpha=0.55, zorder=3)
            top = max(means[c, t] + sds[c, t], reps[c, t].max())
            ax.text(xpos[c], top + 0.10, letters[c, t], ha="center", va="bottom", fontsize=6.5,
                    color=OI["black"])

    ax.set_xticks(xc)
    ax.set_xticklabels(conditions)
    ax.set_ylabel("Relative potency (fold vs reference)")
    ax.set_ylim(0, means.max() + sds.max() + 0.7)
    ax.set_xlim(-0.5, nc - 0.5)
    title(ax, "Stability potency with CLD significance groups")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.14), ncol=nt, fontsize=6.5,
              handlelength=1.1, columnspacing=1.3)
    fig.tight_layout()
    save(fig, "C17_cld_bars", "grouped bars with compact-letter significance", "Comparison")



# ============================================================ E. FLOW / NETWORK (ggplot2 journal-case additions)

def flow_circos():
    """Circular ideogram (karyotype arcs) with Bezier ribbon links = fusion partners."""
    from matplotlib.path import Path
    from matplotlib.patches import PathPatch, Wedge
    from matplotlib.lines import Line2D
    import matplotlib.patheffects as pe

    # --- hg19 chromosome lengths (bp) -> ideogram widths (domain constants) ---
    lens = {"1": 249250621, "2": 243199373, "3": 198022430, "4": 191154276,
            "5": 180915260, "6": 171115067, "7": 159138663, "8": 146364022,
            "9": 141213431, "10": 135534747, "11": 135006516, "12": 133851895,
            "13": 115169878, "14": 107349540, "15": 102531392, "16": 90354753,
            "17": 81195210, "18": 78077248, "19": 59128983, "20": 63025520,
            "21": 48129895, "22": 51304566, "X": 155270560, "Y": 59373566}
    chr_order = list(lens.keys())

    # --- gene loci (chr, bp) and fusion pairs -> partner -> driver, by 3 drivers ---
    loci = {"TFE3": ("X", 48.9e6), "TFEB": ("6", 41.7e6), "ALK": ("2", 29.4e6),
            "SFPQ": ("1", 35.2e6), "PRCC": ("1", 156.7e6), "NONO": ("X", 70.5e6),
            "ASPSCR1": ("17", 79.7e6), "CLTC": ("17", 57.7e6), "LUC7L3": ("17", 50.7e6),
            "MALAT1": ("11", 65.5e6), "ACTB": ("7", 5.5e6), "EIF4A2": ("3", 186.5e6),
            "MATR3": ("5", 138.6e6), "NPM1": ("5", 171.4e6), "TPM3": ("1", 154.1e6),
            "TFG": ("3", 100.4e6), "KIF5B": ("10", 32.3e6)}
    pairs = [("SFPQ", "TFE3", "TFE3"), ("PRCC", "TFE3", "TFE3"), ("NONO", "TFE3", "TFE3"),
             ("ASPSCR1", "TFE3", "TFE3"), ("CLTC", "TFE3", "TFE3"), ("LUC7L3", "TFE3", "TFE3"),
             ("MALAT1", "TFEB", "TFEB"), ("ACTB", "TFEB", "TFEB"), ("EIF4A2", "TFEB", "TFEB"),
             ("MATR3", "TFEB", "TFEB"), ("NPM1", "ALK", "ALK"), ("TPM3", "ALK", "ALK"),
             ("TFG", "ALK", "ALK"), ("KIF5B", "ALK", "ALK")]
    drv_col = {"TFE3": OI["vermillion"], "TFEB": OI["green"], "ALK": OI["blue"]}

    # --- angular layout: clockwise from the top (12 o'clock) ---
    gap, start = 1.4, 90.0
    total = sum(lens.values())
    avail = 360.0 - gap * len(chr_order)
    seg = {}
    cur = start
    for c in chr_order:
        w = lens[c] / total * avail
        seg[c] = (cur - w, cur)                 # (lo, hi) degrees; pos=0 at hi
        cur = cur - w - gap

    def gene_deg(g):
        c, p = loci[g]
        lo, hi = seg[c]
        return hi - (p / lens[c]) * (hi - lo)

    def pol(r, deg):
        a = np.radians(deg)
        return np.array([r * np.cos(a), r * np.sin(a)])

    R_out, R_in, R_lab = 1.0, 0.935, 1.24
    band_w = 0.052
    fig, ax = plt.subplots(figsize=(4.9, 4.9))
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.set_xlim(-1.94, 1.94); ax.set_ylim(-1.94, 1.94)

    # ideogram arc segments (grey karyotype band)
    for c in chr_order:
        lo, hi = seg[c]
        ax.add_patch(Wedge((0, 0), R_out, lo, hi, width=band_w,
                           facecolor="0.86", edgecolor="0.45", lw=0.5, zorder=3))

    # fusion links: cubic Bezier dipping toward the centre, coloured by driver
    def radial_txt(r, deg, s, fs, color, weight="normal", z=6, halo=False):
        a = deg % 360
        x, y = pol(r, deg)
        rot, ha = (a - 180, "right") if 90 < a < 270 else (a, "left")
        t = ax.text(x, y, s, rotation=rot, rotation_mode="anchor", ha=ha, va="center",
                    fontsize=fs, color=color, fontweight=weight, zorder=z)
        if halo:
            t.set_path_effects([pe.withStroke(linewidth=1.4, foreground="white")])
        return t

    for a_gene, b_gene, grp in pairs:
        A = pol(R_in, gene_deg(a_gene)); B = pol(R_in, gene_deg(b_gene))
        sep = abs((gene_deg(a_gene) - gene_deg(b_gene) + 180) % 360 - 180)   # 0..180
        pull = 0.34 - 0.20 * (sep / 180.0)      # closer pair -> shallower dip
        verts = [A, A * pull, B * pull, B]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        ax.add_patch(PathPatch(Path(verts, codes), fill=False, lw=1.1,
                               edgecolor=drv_col[grp], alpha=0.85, zorder=2,
                               capstyle="round"))

    # chromosome number labels, just outside the band, radial
    for c in chr_order:
        lo, hi = seg[c]
        radial_txt(R_out + 0.02, (lo + hi) / 2, c, 5.2, "0.15", z=5)

    # gene labels: angular de-clutter by 1-D relaxation (enforce a min label
    # separation across ALL neighbours) + leader lines — the circos idiom
    genes = list(loci.keys())
    gdeg = np.array([gene_deg(g) for g in genes])
    order = np.argsort(gdeg).tolist()
    sep = 12.5
    pos = gdeg.copy()
    for _ in range(500):
        moved = False
        for a, b in zip(order[:-1], order[1:]):
            gap = pos[b] - pos[a]
            if gap < sep:
                d = (sep - gap) / 2 + 1e-3
                pos[a] -= d; pos[b] += d; moved = True
        if not moved:
            break
    lab_deg = {genes[k]: pos[k] for k in range(len(genes))}
    for g in genes:
        td, ld = gene_deg(g), lab_deg[g]
        p0, p1 = pol(R_out + 0.005, td), pol(R_lab - 0.03, ld)
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="0.55", lw=0.5, zorder=4)
        col = drv_col.get(g, "0.1")
        radial_txt(R_lab, ld, g, 5.6, col if g in drv_col else "0.1",
                   weight="bold" if g in drv_col else "normal", z=6, halo=False)

    handles = [Line2D([0], [0], color=drv_col[k], lw=2.2) for k in ["TFE3", "TFEB", "ALK"]]
    leg = ax.legend(handles, ["TFE3", "TFEB", "ALK"], title="Fusion partner",
                    loc="center", bbox_to_anchor=(0.5, 0.46), fontsize=6.5,
                    title_fontsize=7, handlelength=1.6, borderpad=0.5, labelspacing=0.35)
    leg.set_zorder(10)
    leg.set_frame_on(True)
    leg.get_frame().set_facecolor("white"); leg.get_frame().set_edgecolor("none")
    leg.get_frame().set_alpha(0.82)
    title(ax, "Fusion-gene circos")
    save(fig, "E09_circos", "circular ideogram with ribbon links", "Flow-Network")



# ============================================================ G. SCIENTIFIC (ggplot2 journal-case additions)

def sci_swimmer():
    """Per-subject time-on-study bars, coloured by best response, with event markers."""
    from matplotlib.lines import Line2D

    n = 20
    resp = ["CR", "PR", "SD", "PD"]
    # best-response colours: green(best) -> vermillion(worst), all Okabe-Ito
    rcol = {"CR": OI["green"], "PR": OI["sky"], "SD": OI["orange"], "PD": OI["vermillion"]}
    base = {"CR": 74.0, "PR": 54.0, "SD": 30.0, "PD": 12.0}          # weeks on study by response
    # fixed response composition (=20) so every response tier is represented; weeks/events stay seeded
    counts = {"CR": 3, "PR": 6, "SD": 6, "PD": 5}
    response = np.array([r for r in resp for _ in range(counts[r])])
    RNG.shuffle(response)
    weeks = np.array([max(4.0, round(base[r] + RNG.normal(0, 11))) for r in response])

    # events: response start (on bar) for responders; end = ongoing (still on Rx) or progression (off study)
    responder = np.isin(response, ["CR", "PR", "SD"])
    resp_start = np.where(responder, np.clip(weeks * RNG.uniform(0.12, 0.32, n), 3, None), np.nan)
    ongoing = np.isin(response, ["CR", "PR"]) & (RNG.uniform(size=n) < 0.6)          # diamond at end
    progression = (~ongoing) & np.isin(response, ["SD", "PD"]) & (RNG.uniform(size=n) < 0.85)  # x at end

    order = np.argsort(weeks)          # ascending -> longest ends up at the top row
    response, weeks = response[order], weeks[order]
    resp_start, ongoing, progression = resp_start[order], ongoing[order], progression[order]
    y = np.arange(n)

    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    # month reference gridlines at 6/12/18 months (4 weeks per month convention)
    for mo in (6, 12, 18):
        ax.axvline(mo * 4, color=OI["grey"], lw=1.1, zorder=0)
        ax.text(mo * 4, n - 0.2, f"{mo} mo", ha="center", va="bottom", fontsize=6.5, color=OI["grey"])

    ax.barh(y, weeks, height=0.66, color=[rcol[r] for r in response], zorder=2)

    # response-start marker (open right-triangle) sits ON the bar
    m = ~np.isnan(resp_start)
    ax.plot(resp_start[m], y[m], marker=">", linestyle="none", markersize=4.5,
            markerfacecolor="white", markeredgecolor=OI["black"], markeredgewidth=0.8, zorder=4)
    # end markers just past the bar tip
    ax.plot(weeks[ongoing] + 1.6, y[ongoing], marker="D", linestyle="none", markersize=4.2,
            color=OI["black"], zorder=4)
    ax.plot(weeks[progression] + 1.6, y[progression], marker="x", linestyle="none", markersize=5,
            markeredgewidth=1.1, color=OI["black"], zorder=4)

    ax.set_xlim(0, max(weeks) + 12)
    ax.set_ylim(-0.7, n + 0.3)
    ax.set_yticks([])
    ax.set_xlabel("Time on study (weeks)")
    ax.set_ylabel("Subject (sorted by duration)")
    ax.set_xticks(np.arange(0, max(weeks) + 12, 12))
    title(ax, "Swimmer plot — response timeline")

    # two legends on the right: response colours + event glyphs
    col_h = [Rectangle((0, 0), 1, 1, color=rcol[r]) for r in resp]
    ev_h = [Line2D([], [], marker=">", linestyle="none", markerfacecolor="white",
                   markeredgecolor="k", markersize=5, label="Response start"),
            Line2D([], [], marker="D", linestyle="none", color="k", markersize=4.5, label="Ongoing (on Rx)"),
            Line2D([], [], marker="x", linestyle="none", color="k", markeredgewidth=1.1, markersize=5,
                   label="Progression")]
    leg1 = ax.legend(col_h, resp, title="Best response", loc="upper left",
                     bbox_to_anchor=(1.01, 1.0), fontsize=6.5, title_fontsize=7, handlelength=1.1)
    leg1._legend_box.align = "left"
    ax.add_artist(leg1)
    leg2 = ax.legend(handles=ev_h, title="Event", loc="upper left",
                     bbox_to_anchor=(1.01, 0.52), fontsize=6.5, title_fontsize=7, handlelength=1.1)
    leg2._legend_box.align = "left"

    fig.tight_layout()
    save(fig, "G22_swimmer", "per-subject response timeline (oncology)", "Scientific")



# ============================================================ H. 3D & FIELDS (ggplot2 journal-case additions)

def field_polar_heatmap():
    """Radial heatmap: concentric rings x angular sectors, wedges filled by partial r."""
    from matplotlib.patches import Wedge
    import matplotlib.patheffects as pe

    groups = {"Structure": ["Aliphatic", "Aromatic", "TS", "SA"],
              "Origin": ["Plant", "Microbial", "Necromass", "Input"],
              "Transform": ["F:B", "Fun.Ap", "Bac.Ap", "MRD"],
              "Stability": ["MOC", "Occlude", "C limitation", "Resource limitation"]}
    sectors = [v for g in groups.values() for v in g]
    ns = len(sectors)                            # 16 angular predictors
    rings = ["OR", "ST", "TS", "SA"]             # 4 radial process rings
    nr = len(rings)
    vals = np.round(RNG.uniform(-0.8, 0.8, (ns, nr)), 2)      # partial correlation r
    sig = np.abs(vals) > 0.45

    cmap = mpl.colormaps[DIV]; norm = mpl.colors.Normalize(-0.8, 0.8)
    r0, dr = 2.7, 1.0                            # centre hole + ring thickness
    sw = 360.0 / ns                              # sector width (deg)
    agap = 0.9                                   # angular gap (deg) each side

    fig, ax = plt.subplots(figsize=(4.3, 4.9))
    ax.set_aspect("equal"); ax.set_axis_off()
    lim = r0 + nr * dr + 2.5
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim + 1.9)

    def pol(r, deg):
        a = np.radians(deg)
        return r * np.cos(a), r * np.sin(a)

    for i in range(ns):
        cen = 90.0 - (i + 0.5) * sw              # clockwise from top
        lo, hi = cen - sw / 2 + agap, cen + sw / 2 - agap
        for k in range(nr):
            r_out = r0 + (k + 1) * dr
            c = cmap(norm(vals[i, k]))
            ax.add_patch(Wedge((0, 0), r_out, lo, hi, width=dr, facecolor=c,
                         edgecolor="black" if sig[i, k] else "white",
                         lw=1.3 if sig[i, k] else 0.5, zorder=2 if sig[i, k] else 1))
            lum = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
            x, y = pol(r0 + (k + 0.5) * dr, cen)
            ax.text(x, y, f"{vals[i, k]:.2f}", ha="center", va="center", fontsize=5.0,
                    color="white" if lum < 0.5 else "0.15", zorder=3)

    # sector labels around the rim, radial + upright
    r_lab = r0 + nr * dr + 0.35
    for i in range(ns):
        cen = 90.0 - (i + 0.5) * sw
        a = cen % 360
        x, y = pol(r_lab, cen)
        rot, ha = (a - 180, "right") if 90 < a < 270 else (a, "left")
        ax.text(x, y, sectors[i], rotation=rot, rotation_mode="anchor", ha=ha,
                va="center", fontsize=6.0, color="0.1", zorder=3)

    tc = ax.text(0, 0, "C poor soils\nPOC", ha="center", va="center", fontsize=6.8,
                 color="0.1", zorder=4)
    tc.set_path_effects([pe.withStroke(linewidth=1.5, foreground="white")])

    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.045, pad=0.02)
    cb.set_ticks([-0.8, -0.4, 0, 0.4, 0.8]); cb.ax.tick_params(labelsize=6.5, length=2.5)
    cb.set_label("Partial correlation coefficient r", fontsize=7)
    cb.outline.set_linewidth(0.5)

    title(ax, "Polar heatmap")
    save(fig, "H12_polar_heatmap", "radial heatmap (rings x sectors)", "3D-Fields")



# ============================================================ I. SPECIALIZED (ggplot2 journal-case additions)

def spec_binned_heatmap():
    """Resistance fold-change matrix in discrete colour bins with an aligned row-metadata table."""
    from matplotlib.colors import BoundaryNorm

    drugs = ["AMB", "POS", "FLU", "MCF", "CAS", "ANF", "5FC", "GEL"]
    clades = ["I", "I", "I", "I", "III", "III", "III", "III", "IV", "IV", "IV", "IV", "II", "II", "I", "III"]
    variants = ["M504I", "R318", "Y177*", "Q587*", "T369M", "M306I", "Transl.", "E86fs",
                "E311fs", "E329*", "R100fs", "E18Q", "R983S", "T244N", "E165*", "Q368*"]
    genes = ["ERG11", "ERG6", "ERG6", "NCP1", "ERG11", "ERG11", "NCP1", "ERG6",
             "ERG6", "ERG6", "ERG6", "ERG12", "HMG1", "ERG10", "ERG11", "NCP1"]
    nrow, ncol = len(variants), len(drugs)

    # RR(AUC): mostly modest around 1, with injected strong resistance / hypersensitivity
    rr = 10.0 ** RNG.normal(0.0, 0.55, size=(nrow, ncol))
    ridx = RNG.choice(nrow * ncol, size=10, replace=False)
    rr.flat[ridx] = RNG.uniform(8, 20, size=10)
    sidx = RNG.choice(nrow * ncol, size=16, replace=False)
    rr.flat[sidx] = RNG.uniform(0.03, 0.12, size=16)
    rr = np.round(np.clip(rr, 0.04, 30.5), 2)

    # discrete fold-change bins, diverging (blue<1<red) via BoundaryNorm on a resampled RdBu_r
    bounds = [0.03, 0.06, 0.125, 0.25, 0.5, 1, 2, 4, 8, 16, 32]
    labels = ["<0.06", "0.06-0.125", "0.125-0.25", "0.25-0.5", "0.5-1", "1-2", "2-4", "4-8", "8-16", ">16"]
    nbin = len(labels)
    cmap = mpl.colormaps[DIV].resampled(nbin)
    norm = BoundaryNorm(bounds, nbin)
    binidx = np.clip(np.digitize(rr, bounds) - 1, 0, nbin - 1)
    dark = {0, 1, 8, 9}                                     # bins that need white text for contrast

    fig = plt.figure(figsize=(6.4, 4.0))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.28, 3.55, 0.72], wspace=0.06)
    ax_meta = fig.add_subplot(gs[0, 0]); ax_meta.axis("off")
    ax = fig.add_subplot(gs[0, 1])
    ax_leg = fig.add_subplot(gs[0, 2]); ax_leg.axis("off")

    ax.imshow(rr, cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(np.arange(ncol)); ax.set_xticklabels(drugs, fontsize=6.5)
    ax.xaxis.set_ticks_position("top")
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.tick_params(length=0)
    for i in range(nrow):
        for j in range(ncol):
            ax.text(j, i, f"{rr[i, j]:.2f}", ha="center", va="center", fontsize=5.6,
                    color="white" if binidx[i, j] in dark else OI["black"])

    # aligned row-metadata table on the left (share the heatmap row coordinates)
    ax_meta.set_xlim(0, 3); ax_meta.set_ylim(nrow - 0.5, -0.5)
    mx = {"Clade": 0.30, "Strain": 1.15, "Variant": 1.95}
    for name, xx in mx.items():
        ax_meta.text(xx, -1.05, name, ha="left", va="bottom", fontsize=6.5, fontweight="bold")
    for i in range(nrow):
        ax_meta.text(mx["Clade"], i, clades[i], ha="left", va="center", fontsize=6)
        ax_meta.text(mx["Strain"], i, f"S{i + 1}", ha="left", va="center", fontsize=6)
        ax_meta.text(mx["Variant"], i, variants[i], ha="left", va="center", fontsize=6)

    # stepped/segmented legend (NOT a continuous colorbar), high -> low
    ax_leg.set_xlim(0, 1); ax_leg.set_ylim(0, nbin)
    for k in range(nbin):
        col = cmap(k)
        yb = nbin - 1 - k                                  # k=nbin-1 (>16) on top
        ax_leg.add_patch(Rectangle((0.0, yb + 0.08), 0.34, 0.84, facecolor=col, edgecolor="none"))
        ax_leg.text(0.42, yb + 0.5, labels[k], ha="left", va="center", fontsize=6)
    ax_leg.text(0.0, nbin + 0.15, "RR(AUC)", ha="left", va="bottom", fontsize=7, fontweight="bold")

    save(fig, "I13_binned_heatmap", "binned-color heatmap with row metadata", "Specialized")


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
    # --- Ex1 additions (reproduced from user-supplied reference figures) ---
    dist_sina, dist_paired_prepost, dist_broken_axis,
    corr_triangle, corr_parity_xy_err, corr_grouped_regression,
    comp_grouped_dot_on_bar, comp_dot_reference_zones,
    flow_alluvial, flow_radial_dendrogram, flow_network_communities,
    time_offset_traces,
    field_annotated_profile,
    spec_study_design, spec_pipeline_schematic, spec_pie_vs_bar,
    omics_embedding_feature_pair, omics_dotplot_matrix, omics_stacked_violin,
    omics_enrichment_dotplot, omics_gsea_running, omics_heatmap_tracks, omics_flow_gating,
    # --- reference-corpus additions (idioms the audited reproduce_*.py scripts surfaced) ---
    dist_psd_percentiles, corr_distribution_overlap, sci_annotated_spectrum,
    spec_biodistribution_route, spec_mechanism_cartoon, omics_pca_ellipses,
    # --- ggplot2 journal-case additions (idioms from GeneticistHere/ggplot2-20-journal-cases) ---
    corr_mantel, comp_cld_bars, flow_circos, sci_swimmer, field_polar_heatmap, spec_binned_heatmap,
]


CATEGORY_ORDER = ["Distributions", "Correlation", "Comparison", "Part-of-whole", "Flow-Network",
                  "Time-series", "Scientific", "Omics-Cytometry", "3D-Fields", "Specialized"]
CATEGORY_EMOJI = {"Distributions": "📊", "Correlation": "🔗", "Comparison": "📶",
                  "Part-of-whole": "🥧", "Flow-Network": "🕸️", "Time-series": "📈",
                  "Scientific": "🔬", "Omics-Cytometry": "🧬", "3D-Fields": "🌐",
                  "Specialized": "🧩"}


def write_readme():
    """Regenerate README.md from MANIFEST so the gallery index can never drift from the figures."""
    import re
    from collections import Counter
    cats = Counter(c for c, _, _ in MANIFEST)
    order = [c for c in CATEGORY_ORDER if c in cats] + [c for c in cats if c not in CATEGORY_ORDER]
    n = len(MANIFEST)
    L = [f"# Example gallery — {n} publication-quality figures\n",
         f"A comprehensive gallery of **{n} distinct chart types and variants** across {len(order)} "
         "categories, each generated from **synthetic (seeded, reproducible) data** by "
         "[`scripts/generate_gallery.py`](../scripts/generate_gallery.py) and built to the skill's "
         "publication-ready rules: "
         "one **colorblind-safe palette** (Okabe-Ito), sans-serif type, points shown on bars, exact "
         "stats, **sequential (never jet) colormaps**, clean de-spined axes. Each is exported as "
         "**PNG (300 dpi)** for preview and **PDF (vector)** for submission "
         "([`png/`](png/), [`pdf/`](pdf/)).\n",
         "Regenerate everything with `python3 scripts/generate_gallery.py` from the skill root (needs "
         "matplotlib, numpy, scipy, "
         "seaborn, networkx, pandas — no LaTeX). Every figure is checked by a deterministic "
         "text-overlap audit ([`_figure_qc.py`](../scripts/_figure_qc.py) — the F16 publication-ready gate) as it "
         "is built, and the run prints any collisions it finds.\n",
         "> Data are synthetic and illustrative — the figures demonstrate **form and standards**, "
         "not real results.\n",
         "| Category | Count | Category | Count |", "|---|---|---|---|"]
    for i in range(0, len(order), 2):
        a = order[i]
        row = f"| {CATEGORY_EMOJI.get(a, '')} {a} | {cats[a]} "
        if i + 1 < len(order):
            b = order[i + 1]
            row += f"| {CATEGORY_EMOJI.get(b, '')} {b} | {cats[b]} |"
        else:
            row += "|  |   |"
        L.append(row)
    # jump index — HTML id anchors (reliable on GitHub; emoji-heading auto-anchors are not)
    def _anchor(cat_name):
        return "cat-" + re.sub(r"[^a-z0-9]+", "-", cat_name.lower()).strip("-")
    L.append("**Jump to:** " + "  ·  ".join(
        f"[{CATEGORY_EMOJI.get(c, '')} {c}](#{_anchor(c)})" for c in order) + "\n")
    L.append("> Thumbnails are laid out three across; click any figure to open it full size. "
             "Regenerate in a different colour palette with "
             "`python3 scripts/generate_gallery.py --palette npg` "
             "(`--list-palettes` for the choices; okabe_ito is the colorblind-safe default).\n")
    L.append("\n---\n")
    for c in order:
        items = [(name, note) for cat, name, note in MANIFEST if cat == c]
        L.append(f'<a id="{_anchor(c)}"></a>')
        L.append(f"## {CATEGORY_EMOJI.get(c, '')} {c}  ·  {len(items)} figures\n")
        L.append("<table>")
        for i in range(0, len(items), 3):  # three thumbnails per row
            L.append("<tr>")
            for name, note in items[i:i + 3]:
                num, rest = name.split("_", 1)
                cap = f"<b>{num}. {rest.replace('_', ' ').title()}</b><br/><sub>{note}</sub>"
                L.append(f'<td width="33%" valign="top" align="center">'
                         f'<a href="png/{name}.png"><img src="png/{name}.png" width="100%"/></a>'
                         f'<br/>{cap}</td>')
            L.append("</tr>")
        L.append("</table>\n")
        L.append(f"<sub>[↑ back to top](#example-gallery--{n}-publication-quality-figures)</sub>\n")
    L += ["---\n",
          f"*{n} figures generated by `scripts/generate_gallery.py` (seed 20260706) for the "
          "[data-strength-elevator](../) graph-style library. Palette: Okabe-Ito (Wong 2011). "
          "Anti-pattern codes (AP1–AP16): see "
          "[`references/graph-style-library.md`](../references/graph-style-library.md).*"]
    with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def _category_of(fn):
    """The category is the 4th argument of the function's single save() call — read it statically.

    The first argument is usually `fig` but seaborn-built figures pass `g.figure`, so match any
    expression there rather than the literal name.
    """
    import inspect
    import re as _re
    m = _re.search(r'save\(\s*[\w.]+\s*,\s*"[^"]+"\s*,\s*"[^"]*"\s*,\s*"([^"]+)"', inspect.getsource(fn))
    return m.group(1) if m else "?"


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Generate the data-strength-elevator example gallery")
    ap.add_argument("--category", default="",
                    help="render only one category (e.g. Omics-Cytometry). Does NOT clean other "
                         "outputs and does NOT rewrite manifest.json/README.md — use for a quick preview.")
    ap.add_argument("--list-categories", action="store_true")
    ap.add_argument("--palette", default="okabe_ito",
                    help="categorical palette for the whole gallery (default: okabe_ito). Choices come "
                         "from graph_catalog.json — okabe_ito, npg, aaas, nejm, lancet, jama, "
                         "prism_colorblind_safe. Non-Okabe palettes print a colorblind-safety warning.")
    ap.add_argument("--list-palettes", action="store_true",
                    help="list the available categorical palettes and exit")
    a = ap.parse_args(argv)

    if a.list_palettes:
        for k, v in _load_palettes().items():
            safe = "  (colorblind-safe)" if k in _CB_SAFE_PALETTES else ""
            print(f"  {k:22s} {len(v)} colours{safe}")
        return

    if a.list_categories:
        from collections import Counter
        c = Counter(_category_of(fn) for fn in REGISTRY)
        for k in CATEGORY_ORDER:
            if k in c:
                print(f"  {k:16s} {c[k]}")
        for k in sorted(set(c) - set(CATEGORY_ORDER)):
            print(f"  {k:16s} {c[k]}")
        return

    registry = REGISTRY
    partial = bool(a.category)
    if partial:
        registry = [fn for fn in REGISTRY if _category_of(fn) == a.category]
        if not registry:
            print(f"No figures in category '{a.category}'. Try --list-categories.")
            return
        print(f"PARTIAL build: {len(registry)} figure(s) in '{a.category}' "
              f"(other outputs kept; manifest/README not rewritten)\n")
    else:
        clean_outputs()

    set_style()
    if a.palette and a.palette != "okabe_ito":
        apply_palette(a.palette)
        print(f"Palette: {a.palette} (non-default)\n")
    if not partial:
        print(f"Generating comprehensive gallery ({len(registry)} figures, synthetic seeded data)\n")
    ok, fail = 0, []
    for fn in registry:
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
    # F16 publication-ready gate: report actionable text-overlap collisions (tick-vs-tick
    # adjacency at panel/colorbar boundaries is layout density, not a misreading risk)
    if audit_overlaps_detailed is None:
        print("\nOVERLAP AUDIT: skipped (_figure_qc.py not importable)")
    elif OVERLAPS:
        print(f"\nOVERLAP AUDIT: {len(OVERLAPS)} figure(s) with actionable text collisions (F16):")
        for name, hits in OVERLAPS:
            print(f"  ! {name}: {len(hits)} collision(s)")
            for h in hits[:4]:
                print(f"      {h['a']} [{h['role_a']}]  <->  {h['b']} [{h['role_b']}]")
    else:
        print(f"\nOVERLAP AUDIT: clean — 0 text collisions across {len(MANIFEST)} figures (F16)")
    # write manifest + regenerate the README index so neither can drift from the figures.
    # A partial (--category) run must NOT touch them: MANIFEST holds only the rendered subset, so
    # writing it would truncate the index to that category.
    if partial:
        print("\nmanifest.json + README.md left untouched (partial build)")
        return
    import json
    json.dump(MANIFEST, open(os.path.join(OUT, "manifest.json"), "w"), indent=1)
    write_readme()
    print(f"manifest.json + README.md regenerated ({len(MANIFEST)} entries)")


if __name__ == "__main__":
    main()
