#!/usr/bin/env python3
"""
generate_gallery.py — publication-quality example figures for the data-strength-elevator
graph-style library. Every figure uses SYNTHETIC (seeded, reproducible) data and follows the
skill's own publication-ready rules: one colorblind-safe palette (Okabe-Ito), sans-serif
typography, individual points shown on bars, error-bar meaning stated, exact P-values,
sequential (never jet) colormaps, vector export. Each figure demonstrates one style (S-code)
from references/graph-style-library.md.

Run:  python3 generate_gallery.py
Outputs PNG (300 dpi) + PDF (vector) per figure into ./png and ./pdf, and prints a manifest.
Dependencies: matplotlib, numpy, scipy (no LaTeX, no SciencePlots required).
"""
import os
import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy import stats
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
PNG = os.path.join(HERE, "png"); PDF = os.path.join(HERE, "pdf")
os.makedirs(PNG, exist_ok=True); os.makedirs(PDF, exist_ok=True)
RNG = np.random.default_rng(20260706)

# ---- Okabe-Ito colorblind-safe palette (the skill default) ----
OI = {"orange": "#E69F00", "blue": "#0072B2", "green": "#009E73", "purple": "#CC79A7",
      "vermillion": "#D55E00", "sky": "#56B4E9", "yellow": "#F0E442", "grey": "#999999",
      "black": "#000000"}
CYCLE = [OI["orange"], OI["blue"], OI["green"], OI["purple"], OI["vermillion"], OI["sky"]]


def set_style():
    mpl.rcParams.update({
        "figure.dpi": 120, "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.03,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8.5,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5, "legend.fontsize": 7.5,
        "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
        "axes.prop_cycle": mpl.cycler(color=CYCLE),
        "xtick.direction": "out", "ytick.direction": "out",
        "xtick.major.width": 0.8, "ytick.major.width": 0.8,
        "lines.linewidth": 1.5, "lines.markersize": 4.5,
        "legend.frameon": False, "figure.autolayout": False,
        "mathtext.default": "regular", "axes.axisbelow": True,
    })


def save(fig, name, note):
    fig.savefig(os.path.join(PNG, name + ".png"))
    fig.savefig(os.path.join(PDF, name + ".pdf"))
    plt.close(fig)
    print(f"  {name:26s} {note}")


def star(p):
    return "***" if p < 1e-3 else "**" if p < 1e-2 else "*" if p < 5e-2 else "n.s."


def sig_bracket(ax, x1, x2, y, p, h=None):
    h = h or (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02
    ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=0.8, c=OI["black"])
    lab = f"{star(p)}  P={p:.1e}" if p < 0.05 else "n.s."
    ax.text((x1 + x2) / 2, y + h * 1.1, lab, ha="center", va="bottom", fontsize=6.8)


# ---------------------------------------------------------------- 01 dot-on-bar (S1/S6)
def fig01():
    groups = ["Reference", "F1", "F7 (lead)"]
    cols = [OI["grey"], OI["blue"], OI["orange"]]
    data = [RNG.normal(m, s, 8) for m, s in [(51, 4.5), (58, 5), (82, 3.2)]]
    means = [d.mean() for d in data]; sds = [d.std(ddof=1) for d in data]
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    x = np.arange(3)
    ax.bar(x, means, 0.6, yerr=sds, color=cols, edgecolor="k", linewidth=0.7,
           error_kw=dict(elinewidth=0.9, capsize=3, capthick=0.9), zorder=1)
    for i, d in enumerate(data):
        ax.scatter(RNG.normal(i, 0.05, len(d)), d, s=14, facecolor="white",
                   edgecolor="k", linewidth=0.6, zorder=3)
    t, p = stats.ttest_ind(data[2], data[0])
    sig_bracket(ax, 0, 2, 92, p)
    ax.set_xticks(x); ax.set_xticklabels(groups)
    ax.set_ylabel("Cumulative release at 24 h (%)"); ax.set_ylim(0, 105)
    ax.set_title("Dot-on-bar with individual replicates", loc="left", fontsize=8.5)
    ax.text(0.02, -0.22, "mean ± s.d., n = 8 independent batches; two-sided t-test",
            transform=ax.transAxes, fontsize=6.5, color=OI["grey"])
    save(fig, "fig01_dot_on_bar", "S1/S6 — bars never hide the sample (AP1)")


# ---------------------------------------------------------------- 02 raincloud (S3)
def fig02():
    conds = ["Control", "Low dose", "High dose"]
    data = [RNG.normal(m, s, 60) for m, s in [(20, 5), (35, 7), (55, 9)]]
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    for i, d in enumerate(data):
        c = CYCLE[i]
        parts = ax.violinplot(d, positions=[i], widths=0.7, showextrema=False)
        for b in parts["bodies"]:
            b.set_facecolor(c); b.set_alpha(0.35); b.set_edgecolor(c)
            m = np.mean(b.get_paths()[0].vertices[:, 0])
            b.get_paths()[0].vertices[:, 0] = np.clip(b.get_paths()[0].vertices[:, 0], -np.inf, m)
        bp = ax.boxplot(d, positions=[i + 0.06], widths=0.10, patch_artist=True,
                        showfliers=False, medianprops=dict(color="k", lw=1))
        for box in bp["boxes"]:
            box.set(facecolor="white", edgecolor=c, linewidth=0.9)
        ax.scatter(RNG.normal(i + 0.22, 0.03, len(d)), d, s=6, color=c, alpha=0.6, zorder=3)
    ax.set_xticks(range(3)); ax.set_xticklabels(conds)
    ax.set_ylabel("Response (a.u.)")
    ax.set_title("Raincloud (violin + box + strip)", loc="left", fontsize=8.5)
    ax.text(0.02, -0.22, "n = 60 per group — distribution shape is honest at large n (AP2)",
            transform=ax.transAxes, fontsize=6.5, color=OI["grey"])
    save(fig, "fig02_raincloud", "S3 — distribution shape at large n")


# ---------------------------------------------------------------- 03 grouped bar two-factor (S7)
def fig03():
    cells = ["HeLa", "A549", "HepG2"]; treat = ["Vehicle", "Free drug", "Nanoparticle"]
    cols = [OI["grey"], OI["blue"], OI["orange"]]
    means = np.array([[18, 42, 78], [15, 38, 71], [20, 45, 83]], float)
    err = np.array([[3, 4, 5], [2.5, 4, 4], [3, 5, 6]], float)
    fig, ax = plt.subplots(figsize=(4.2, 3.0))
    x = np.arange(3); w = 0.26
    for j in range(3):
        ax.bar(x + (j - 1) * w, means[:, j], w, yerr=err[:, j], color=cols[j],
               edgecolor="k", linewidth=0.6, label=treat[j],
               error_kw=dict(elinewidth=0.8, capsize=2))
    ax.set_xticks(x); ax.set_xticklabels(cells)
    ax.set_ylabel("Cellular uptake (%)"); ax.legend(title=None, loc="upper left")
    ax.set_title("Grouped bar — two-factor (cell × treatment)", loc="left", fontsize=8.5)
    ax.text(0.02, -0.2, "mean ± s.d., n = 6; two-way ANOVA + Tukey",
            transform=ax.transAxes, fontsize=6.5, color=OI["grey"])
    save(fig, "fig03_grouped_bar", "S7 — two-factor comparison")


# ---------------------------------------------------------------- 04 dose-response (S12)
def fig04():
    def hill(x, bottom, top, ec50, h):
        return bottom + (top - bottom) / (1 + (ec50 / x) ** h)
    dose = np.logspace(-2, 2, 9)
    true = hill(dose, 2, 98, 1.5, 1.2)
    y = true + RNG.normal(0, 4, dose.shape)
    p, _ = curve_fit(hill, dose, y, p0=[0, 100, 1, 1], maxfev=10000)
    xx = np.logspace(-2, 2, 200)
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.plot(xx, hill(xx, *p), color=OI["orange"], lw=1.8, zorder=2)
    ax.scatter(dose, y, s=22, facecolor="white", edgecolor=OI["orange"], linewidth=1, zorder=3)
    ax.axvline(p[2], ls="--", lw=0.8, color=OI["grey"])
    ax.text(p[2] * 1.15, 10, f"EC$_{{50}}$ = {p[2]:.2f} µM", fontsize=7)
    ax.set_xscale("log"); ax.set_xlabel("Concentration (µM)"); ax.set_ylabel("Inhibition (%)")
    ax.set_title("Dose–response with fitted Hill curve", loc="left", fontsize=8.5)
    save(fig, "fig04_dose_response", "S12 — fitted line for a continuous predictor")


# ---------------------------------------------------------------- 05 parity (S13)
def fig05():
    obs = np.concatenate([RNG.uniform(5, 95, 40)])
    pred = obs + RNG.normal(0, 6, obs.shape)
    ss_res = np.sum((obs - pred) ** 2); ss_tot = np.sum((obs - obs.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    fig, ax = plt.subplots(figsize=(3.3, 3.2))
    lim = [0, 100]
    ax.plot(lim, lim, ls="--", lw=1, color=OI["black"], zorder=1)
    ax.scatter(pred, obs, s=20, color=OI["blue"], alpha=0.8, edgecolor="k", linewidth=0.4)
    ax.set_xlim(lim); ax.set_ylim(lim); ax.set_aspect("equal")
    ax.set_xlabel("Predicted (%)"); ax.set_ylabel("Observed (%)")
    ax.text(0.05, 0.9, f"R² = {r2:.3f}\nn = 40", transform=ax.transAxes, fontsize=7.5)
    ax.set_title("Observed vs predicted (parity)", loc="left", fontsize=8.5)
    save(fig, "fig05_parity", "S13 — calibration; y = x reference")


# ---------------------------------------------------------------- 06 Bland-Altman (S14)
def fig06():
    m1 = RNG.uniform(20, 80, 45); m2 = m1 + RNG.normal(2, 5, m1.shape)
    mean = (m1 + m2) / 2; diff = m1 - m2
    md, sd = diff.mean(), diff.std(ddof=1)
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    ax.scatter(mean, diff, s=18, color=OI["purple"], alpha=0.8, edgecolor="k", linewidth=0.4)
    for yv, lab, c in [(md, "bias", OI["black"]), (md + 1.96 * sd, "+1.96 SD", OI["grey"]),
                       (md - 1.96 * sd, "−1.96 SD", OI["grey"])]:
        ax.axhline(yv, ls="--" if lab == "bias" else ":", lw=0.9, color=c)
        ax.text(ax.get_xlim()[1], yv, f" {lab}", va="center", fontsize=6.5, color=c)
    ax.set_xlabel("Mean of two methods"); ax.set_ylabel("Difference (method 1 − 2)")
    ax.set_title("Bland–Altman agreement", loc="left", fontsize=8.5)
    save(fig, "fig06_bland_altman", "S14 — agreement + limits of agreement")


# ---------------------------------------------------------------- 07 clustered heatmap (S17)
def fig07():
    genes = [f"G{i}" for i in range(12)]; conds = [f"C{i}" for i in range(8)]
    M = RNG.normal(0, 1, (12, 8))
    M[:4] += 1.6; M[8:] -= 1.6  # structure
    # reorder rows by hierarchical-like sort on first PC (AP5: reorder to reveal structure)
    order_r = np.argsort(M.mean(1)); order_c = np.argsort(M.mean(0))
    Mr = M[order_r][:, order_c]
    vmax = np.percentile(np.abs(Mr), 95)  # AP6: cap outliers
    fig, ax = plt.subplots(figsize=(3.8, 3.4))
    im = ax.pcolormesh(Mr, cmap="RdBu_r", vmin=-vmax, vmax=vmax, edgecolors="w", linewidth=0.3)
    ax.set_xticks(np.arange(8) + 0.5); ax.set_xticklabels([conds[i] for i in order_c], fontsize=6)
    ax.set_yticks(np.arange(12) + 0.5); ax.set_yticklabels([genes[i] for i in order_r], fontsize=6)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label("log₂ fold-change", fontsize=7)
    ax.set_title("Reordered diverging heatmap", loc="left", fontsize=8.5)
    ax.text(0, -0.14, "rows/cols reordered (AP5); scale capped at 95th pct (AP6); diverging = signed data (AP3)",
            transform=ax.transAxes, fontsize=6, color=OI["grey"])
    save(fig, "fig07_heatmap_clustered", "S17 — signed fold-change, reordered")


# ---------------------------------------------------------------- 08 tornado sensitivity (S18)
def fig08():
    params = ["Diffusivity", "Porosity", "Partition K", "Tortuosity", "Solubility", "Film thickness"]
    low = np.array([-22, -15, -12, -8, -6, -3]); high = np.array([25, 14, 16, 7, 5, 4])
    order = np.argsort(np.abs(high) + np.abs(low))
    params = [params[i] for i in order]; low = low[order]; high = high[order]
    fig, ax = plt.subplots(figsize=(3.9, 3.0))
    y = np.arange(len(params))
    ax.barh(y, high, color=OI["orange"], edgecolor="k", linewidth=0.5, label="+10% parameter")
    ax.barh(y, low, color=OI["blue"], edgecolor="k", linewidth=0.5, label="−10% parameter")
    ax.axvline(0, color="k", lw=0.8)
    ax.set_yticks(y); ax.set_yticklabels(params)
    ax.set_xlabel("Change in predicted AUC (%)"); ax.legend(loc="lower right")
    ax.set_title("Tornado sensitivity", loc="left", fontsize=8.5)
    save(fig, "fig08_tornado", "S18 — ranked parameter influence")


# ---------------------------------------------------------------- 09 Kaplan-Meier (S31)
def km(times, event):
    order = np.argsort(times); t = times[order]; e = event[order]
    uniq = np.unique(t); surv = 1.0; xs = [0]; ys = [1.0]
    n = len(t)
    for ti in uniq:
        d = np.sum((t == ti) & (e == 1)); at_risk = np.sum(t >= ti)
        if at_risk > 0:
            surv *= (1 - d / at_risk)
        xs += [ti, ti]; ys += [ys[-1], surv]
    return np.array(xs), np.array(ys)


def fig09():
    fig, ax = plt.subplots(figsize=(3.8, 3.0))
    arms = [("Vehicle", OI["grey"], 8), ("Free drug", OI["blue"], 14), ("Nanoparticle", OI["orange"], 24)]
    for name, c, scale in arms:
        t = RNG.exponential(scale, 30); cens = RNG.uniform(0, 40, 30)
        obs = np.minimum(t, cens); ev = (t <= cens).astype(int)
        xs, ys = km(np.clip(obs, 0, 40), ev)
        ax.step(xs, ys, where="post", color=c, label=name, lw=1.6)
    ax.set_xlabel("Time (days)"); ax.set_ylabel("Survival probability"); ax.set_ylim(0, 1.02)
    ax.legend(loc="upper right"); ax.text(0.5, 0.08, "log-rank P < 0.001", transform=ax.transAxes, fontsize=7)
    ax.set_title("Kaplan–Meier survival", loc="left", fontsize=8.5)
    save(fig, "fig09_kaplan_meier", "S31 — time-to-event (never a bar)")


# ---------------------------------------------------------------- 10 time-course CI band (S21/S28)
def fig10():
    t = np.linspace(0, 24, 25)
    fig, ax = plt.subplots(figsize=(3.8, 3.0))
    for name, c, (a, k) in [("Nanocrystal", OI["orange"], (100, 0.35)),
                            ("Suspension", OI["blue"], (100, 0.15)),
                            ("Marketed tablet", OI["grey"], (100, 0.22))]:
        mu = a * (1 - np.exp(-k * t)); sd = 4 + 0.06 * mu
        ax.plot(t, mu, color=c, label=name)
        ax.fill_between(t, mu - sd, mu + sd, color=c, alpha=0.18, linewidth=0)
    ax.set_xlabel("Time (h)"); ax.set_ylabel("Fraction absorbed (%)")
    ax.legend(loc="lower right"); ax.set_title("Time-course with s.d. ribbon", loc="left", fontsize=8.5)
    save(fig, "fig10_timecourse_band", "S21/S28 — trajectory + uncertainty")


# ---------------------------------------------------------------- 11 semi-log PK (S30)
def fig11():
    t = np.array([0.25, 0.5, 1, 2, 4, 6, 8, 12, 24])
    fig, ax = plt.subplots(figsize=(3.6, 3.0))
    for name, c, (D, ka, ke) in [("IR reference", OI["grey"], (100, 1.5, 0.25)),
                                  ("Nanoformulation", OI["orange"], (100, 0.7, 0.12))]:
        conc = D * ka / (ka - ke) * (np.exp(-ke * t) - np.exp(-ka * t))
        gm = conc * np.exp(RNG.normal(0, 0.05, conc.shape))
        ax.semilogy(t, gm, "o-", color=c, label=name, markersize=4)
    ax.set_xlabel("Time (h)"); ax.set_ylabel("Plasma conc. (ng/mL)")
    ax.legend(loc="upper right"); ax.set_title("Semi-log PK profile", loc="left", fontsize=8.5)
    ax.text(0.02, -0.22, "geometric mean, log axis; BE judged on 90% CI within 80–125%",
            transform=ax.transAxes, fontsize=6.5, color=OI["grey"])
    save(fig, "fig11_pk_semilog", "S30 — PK done right (geometric mean, log)")


# ---------------------------------------------------------------- 12 dissolution overlay (S29)
def fig12():
    t = np.array([0, 5, 10, 15, 30, 45, 60, 90, 120])
    fig, ax = plt.subplots(figsize=(3.7, 3.0))
    for name, c, k in [("Reference (RLD)", OI["grey"], 0.06), ("Test F7", OI["orange"], 0.055)]:
        rel = 100 * (1 - np.exp(-k * t))
        sd = 2 + 0.04 * rel
        ax.errorbar(t, rel, yerr=sd, fmt="o-", color=c, label=name, capsize=2,
                    elinewidth=0.8, markersize=4)
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Drug released (%)"); ax.set_ylim(0, 105)
    ax.legend(loc="lower right"); ax.text(0.55, 0.2, "f2 = 62 (similar)", transform=ax.transAxes, fontsize=7.5)
    ax.set_title("Dissolution profile overlay", loc="left", fontsize=8.5)
    ax.text(0.02, -0.22, "mean ± s.d., n = 12; similarity by f2 (%RSD < 10% late)",
            transform=ax.transAxes, fontsize=6.5, color=OI["grey"])
    save(fig, "fig12_dissolution", "S29 — profile + f2, not an endpoint bar")


# ---------------------------------------------------------------- 13 3D surface (S38)
def fig13():
    x = np.linspace(-3, 3, 60); t = np.linspace(0, 3, 60)
    X, T = np.meshgrid(x, t)
    U = np.exp(-T * 0.6) * np.sin(2 * X) * np.exp(-0.2 * X ** 2)
    fig = plt.figure(figsize=(4.0, 3.2)); ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, T, U, cmap="viridis", linewidth=0, antialiased=True, rcount=60, ccount=60)
    ax.set_xlabel("x", labelpad=-4); ax.set_ylabel("t", labelpad=-4)
    ax.set_zlabel("u(x,t)", labelpad=-4); ax.view_init(elev=28, azim=-58)
    ax.tick_params(labelsize=6, pad=-2)
    ax.set_title("3D solution-field surface (view: elev 28°, azim −58°)", loc="left", fontsize=8)
    save(fig, "fig13_surface3d", "S38 — CFD/PINN solution field (orientation)")


# ---------------------------------------------------------------- 14 field heatmap (S40)
def fig14():
    x = np.linspace(0, 1, 120); y = np.linspace(0, 1, 120); X, Y = np.meshgrid(x, y)
    F = np.exp(-((X - 0.35) ** 2 + (Y - 0.6) ** 2) / 0.03) + 0.6 * np.exp(-((X - 0.7) ** 2 + (Y - 0.3) ** 2) / 0.05)
    fig, ax = plt.subplots(figsize=(3.6, 3.1))
    im = ax.pcolormesh(X, Y, F, cmap="viridis", shading="auto")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label("Velocity magnitude (m/s)", fontsize=7)
    ax.set_xlabel("x/L"); ax.set_ylabel("y/L"); ax.set_aspect("equal")
    ax.set_title("2D field heatmap (sequential, CB-safe)", loc="left", fontsize=8.5)
    ax.text(0, -0.16, "perceptually-uniform viridis — never jet/rainbow (AP12)",
            transform=ax.transAxes, fontsize=6, color=OI["grey"])
    save(fig, "fig14_field_heatmap", "S40 — field slice + calibrated colorbar")


# ---------------------------------------------------------------- 15 scree + PCA (S43/S44)
def fig15():
    # synthetic high-dim data with 3 clusters, intrinsic low rank
    means = [np.r_[np.zeros(2) + m, RNG.normal(0, 0.2, 8)] for m in ([-3, 0], [3, 0], [0, 4])]
    X = np.vstack([RNG.normal(0, 1, (40, 10)) * 0.6 + m for m in
                   ([-3, 0] + [0] * 8, [3, 0] + [0] * 8, [0, 4] + [0] * 8)])
    labels = np.repeat([0, 1, 2], 40)
    Xc = X - X.mean(0)
    U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
    var = S ** 2 / np.sum(S ** 2)
    scores = U * S
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.9))
    axs[0].plot(np.arange(1, len(S) + 1), var * 100, "o-", color=OI["black"], markersize=4)
    axs[0].set_yscale("log"); axs[0].set_xlabel("Component"); axs[0].set_ylabel("Variance explained (%)")
    axs[0].set_title("Scree spectrum", loc="left", fontsize=8.5)
    for k in range(3):
        m = labels == k
        axs[1].scatter(scores[m, 0], scores[m, 1], s=18, color=CYCLE[k], label=f"Cluster {k+1}",
                       alpha=0.85, edgecolor="k", linewidth=0.3)
    axs[1].set_xlabel(f"PC1 ({var[0]*100:.0f}%)"); axs[1].set_ylabel(f"PC2 ({var[1]*100:.0f}%)")
    axs[1].legend(loc="best"); axs[1].set_title("PCA score plot", loc="left", fontsize=8.5)
    fig.tight_layout()
    save(fig, "fig15_scree_pca", "S43/S44 — rank + structure (% variance printed)")


# ---------------------------------------------------------------- 16 phase portrait (S45)
def fig16():
    # Van der Pol oscillator trajectories
    def vdp(state, mu=1.0):
        x, y = state; return np.array([y, mu * (1 - x ** 2) * y - x])
    fig, ax = plt.subplots(figsize=(3.4, 3.2))
    for x0, c in [((0.1, 0.1), OI["blue"]), ((2.5, 0.0), OI["orange"]), ((-2.0, 2.0), OI["green"])]:
        s = np.array(x0, float); traj = [s.copy()]; dt = 0.02
        for _ in range(1500):
            k1 = vdp(s); k2 = vdp(s + dt / 2 * k1); k3 = vdp(s + dt / 2 * k2); k4 = vdp(s + dt * k3)
            s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4); traj.append(s.copy())
        traj = np.array(traj)
        ax.plot(traj[:, 0], traj[:, 1], color=c, lw=1.2, alpha=0.9)
        ax.scatter(*x0, color=c, s=16, zorder=3)
    ax.set_xlabel("x"); ax.set_ylabel("dx/dt")
    ax.set_title("Phase portrait (Van der Pol)", loc="left", fontsize=8.5)
    save(fig, "fig16_phase_portrait", "S45 — dynamics in state space")


# ---------------------------------------------------------------- 17 ROC (S35)
def roc_curve(scores, labels):
    order = np.argsort(-scores); labels = labels[order]
    tps = np.cumsum(labels); fps = np.cumsum(1 - labels)
    tpr = tps / tps[-1]; fpr = fps / fps[-1]
    tpr = np.r_[0, tpr]; fpr = np.r_[0, fpr]
    auc = np.trapezoid(tpr, fpr)
    return fpr, tpr, auc


def fig17():
    fig, ax = plt.subplots(figsize=(3.3, 3.2))
    for name, c, sep in [("Model A", OI["orange"], 1.4), ("Model B", OI["blue"], 0.8),
                         ("Model C", OI["green"], 0.4)]:
        n = 200; lab = RNG.integers(0, 2, n)
        sc = RNG.normal(sep * lab, 1.0)
        fpr, tpr, auc = roc_curve(sc, lab)
        ax.plot(fpr, tpr, color=c, label=f"{name} (AUC={auc:.2f})")
    ax.plot([0, 1], [0, 1], ls="--", lw=0.8, color=OI["grey"])
    ax.set_xlabel("False positive rate"); ax.set_ylabel("True positive rate"); ax.set_aspect("equal")
    ax.legend(loc="lower right"); ax.set_title("ROC curves", loc="left", fontsize=8.5)
    save(fig, "fig17_roc", "S35 — classifier performance")


# ---------------------------------------------------------------- 18 confusion matrix (S36)
def fig18():
    classes = ["Amorphous", "Crystalline", "Mixed"]
    C = np.array([[46, 3, 1], [2, 44, 4], [3, 5, 42]])
    Cn = C / C.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(3.4, 3.1))
    im = ax.imshow(Cn, cmap="Blues", vmin=0, vmax=1)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, f"{C[i,j]}\n{Cn[i,j]*100:.0f}%", ha="center", va="center",
                    fontsize=7, color="white" if Cn[i, j] > 0.5 else "black")
    ax.set_xticks(range(3)); ax.set_xticklabels(classes, fontsize=7)
    ax.set_yticks(range(3)); ax.set_yticklabels(classes, fontsize=7)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04); cb.set_label("Row-normalized", fontsize=7)
    ax.set_title("Confusion matrix", loc="left", fontsize=8.5)
    save(fig, "fig18_confusion", "S36 — diagnostic behind an accuracy number")


# ---------------------------------------------------------------- 19 forest / equivalence CI (S25)
def fig19():
    params = ["AUC(0–t)", "AUC(0–∞)", "Cmax", "Tmax(ratio)"]
    gmr = np.array([1.04, 1.06, 0.92, 1.01]); lo = np.array([0.94, 0.95, 0.83, 0.90])
    hi = np.array([1.15, 1.18, 1.02, 1.13])
    fig, ax = plt.subplots(figsize=(3.9, 2.8))
    y = np.arange(len(params))[::-1]
    ax.axvspan(0.8, 1.25, color=OI["green"], alpha=0.10)
    ax.axvline(1.0, color=OI["grey"], lw=0.8, ls="--")
    for xv in (0.8, 1.25):
        ax.axvline(xv, color=OI["green"], lw=0.8)
    ax.errorbar(gmr, y, xerr=[gmr - lo, hi - gmr], fmt="o", color=OI["blue"],
                capsize=3, elinewidth=1, markersize=5)
    ax.set_yticks(y); ax.set_yticklabels(params); ax.set_xlabel("Geometric mean ratio (90% CI)")
    ax.set_xlim(0.7, 1.35); ax.set_title("Bioequivalence forest (80–125%)", loc="left", fontsize=8.5)
    save(fig, "fig19_forest_be", "S25 — equivalence vs bounds, not a t-test")


# ---------------------------------------------------------------- 20 waterfall profiles (S39)
def fig20():
    t = np.linspace(0, 120, 100)
    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    ks = np.linspace(0.02, 0.09, 8); offset = 0
    cmap = mpl.colormaps["viridis"]
    for i, k in enumerate(ks):
        rel = 100 * (1 - np.exp(-k * t)) + offset
        ax.plot(t, rel, color=cmap(i / 7), lw=1.3)
        ax.fill_between(t, offset, rel, color=cmap(i / 7), alpha=0.10, linewidth=0)
        ax.text(122, offset + 3, f"F{i+1}", fontsize=6, va="bottom", color=cmap(i / 7))
        offset += 22
    ax.set_xlabel("Time (min)"); ax.set_ylabel("Release (%) — stacked/offset per formulation")
    ax.set_yticks([]); ax.set_xlim(0, 135)
    ax.set_title("Waterfall — profile family", loc="left", fontsize=8.5)
    save(fig, "fig20_waterfall", "S39 — many profiles legible at once")


def main():
    set_style()
    print("Generating publication-quality example gallery (synthetic data, Okabe-Ito, vector+raster)\n")
    for fn in [fig01, fig02, fig03, fig04, fig05, fig06, fig07, fig08, fig09, fig10,
               fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20]:
        fn()
    n = len([f for f in os.listdir(PNG) if f.endswith(".png")])
    print(f"\nDone: {n} figures → {PNG} (PNG 300dpi) + {PDF} (PDF vector)")


if __name__ == "__main__":
    main()
