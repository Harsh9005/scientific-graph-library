<!-- data-strength-elevator reference module — GRAPH-STYLE LIBRARY.
Curated catalogue of chart styles distilled from the 5 elite exemplars
(Nat Commun 2024 15:739; Nat Commun 2025 16:2198; Nat Mater 2025 24:1653;
Nat Biotechnol 2024/2025 Brief Communications) in references/_exemplar_mining/,
then EXTENDED with the parity / uncertainty / model-diagnostic families the
wet-lab corpus structurally cannot teach. READ ALONGSIDE domain-conventions.md:
the PK/PBPK/IVIVC/dissolution/CFD/PINN notes below tell you which styles are
domain-correct and which are laundered wet-lab defaults you must NOT copy. -->

# Graph-Style Library — pick the sharpest chart for each point

*A catalogue so an author has VARIETY to select from and can communicate the exact analytical point in the best possible way. Each entry gives: **what it shows**, the **analytical point** it communicates best, **when to use / when NOT**, a **multi-panel pairing** suggestion, and — where relevant — the **domain-correct note** for PK / PBPK / IVIVC / dissolution / CFD / PINN so the skill never launders a wet-lab default onto an in-silico or bioequivalence output.*

**How to use this file.** In Phase 1 (DS1 audit) and Phase 7 (strengthening), for every claim ask *"what is the ONE analytical point this panel must land?"* then pick the style below whose "analytical point" matches. Do not pick by habit. A bar for a survival endpoint, or a bare contour for a "validated" CFD field, is a style-selection error that reads as naïveté to editors. The exemplars are disciplined: they reuse ~10–20 archetypes with iron consistency rather than chasing novelty — **restraint is the lesson**, but restraint *within a deliberately chosen* archetype, not defaulting to the same bar for everything.

**Provenance tag key:** [E] = used by ≥1 exemplar (panel cited); [D] = domain-required family the exemplars lack but PK/IVIVC/CFD/PINN work needs (grounded in `domain-conventions.md`, not in the wet-lab corpus); [K] = distilled from Nathan Kutz's *ScientificComputing* repository (*Data-Driven Modeling & Scientific Computation*, 2nd ed.) — technique/idiom only, no code copied — for the in-silico / signal / data-analysis families (GROUP 8).

---

## ⚡ DECISION LAYER — decide first, don't browse (this is how to USE the library)

**The library is an INDEX, not a reading list. To pick a chart, DECIDE — do not scroll 45 styles.** Two equivalent paths, both backed by the single machine-readable index `scripts/graph_catalog.json` (styles + anti-patterns + palettes + style-engines + stat-methods stored once, not re-derived):

**A. Deterministic (preferred) — run the chooser.** It returns a ranked short-list + the palette/style-engine to apply + the anti-patterns it REJECTS for your case + the matching statistical method:
```bash
python3 scripts/choose_graph.py --intent "<the ONE point the panel must land>" \
    [--data categorical|continuous|continuous_paired|time_series|time_to_event|field_2d|matrix|signal|high_dim|compositional] \
    [--n <per-group n>] [--domain general|dissolution|PK|PBPK|IVIVC|CFD|PINN|BE] \
    [--journal nature|science|ieee|npg|aaas|nejm|lancet|jama|prism] [--json]
```
Example: `--intent "compare means" --data categorical --n 4 --domain PK` → recommends S1 dot-on-bar + S25/S30, **rejects** violin (AP2) and mean±SD+t-test (DS5), palette Okabe-Ito, stat = geometric-mean / 90%-CI. **The chooser IS the decision** — the style entries below are the detail it points into, not a menu to read end-to-end.

**B. Human decision tree** (same logic, when you can't run the script). Ask the ONE analytical point, then:

| The point is… | Go to | Obey the rule |
|---|---|---|
| magnitude / compare categories | dot-on-bar **S1** (n≤~15) → **S6** finalists w/ stats | show points (AP1); zero-based bars (AP9); violin only n≥20 (AP2) |
| distribution shape | strip **S2** (small n) / violin **S3** (n≥20) | never violin/box/hist at small n (AP2/AP15/AP16) |
| a whole screen / ranking | **S5** screen → **S6** finalists | show losers (anti-cherry-pick); facet, no bar-meadow (AP4) |
| dose / concentration response | **S8** ladder (few levels) / **S12** fitted line (many) | — |
| model predicts data | **S13** parity + **S14** Bland–Altman | not bare R² (DS5); required for IVIVC / CFD / PINN |
| what drives the result | **S17** heatmap → promoted bars / **S18** tornado | reorder rows/cols (AP5), cap outliers (AP6); diverging only if signed (AP3) |
| parts of a whole | **stacked / side-by-side bar** (see S24) | never pie or donut (AP10/AP11); reorder segments (AP13) |
| kinetics / time-course | **S28** band line / **S29** dissolution / **S30** semi-log PK | never a single-timepoint bar; PK = geometric mean / log / 90% CI |
| time-to-event | **S31** Kaplan–Meier + log-rank | never an endpoint bar |
| 2D field / parameter sweep | **S38** surface (orientation) + **S40** heatmap (values) | sequential CB-safe map, never jet (AP12); pair with GCI/parity |
| signal / frequency | **S41** spectrogram / **S42** stem | state the window length |
| dimensionality / rank | **S43** scree + **S44** PCA score | print % variance; show reconstruction error |
| dynamics of an ODE model | **S45** phase portrait + **S21** time trace | — |
| classifier performance | **S35** ROC/PR + **S36** confusion/calibration | report cross-validation |

**Domain override (DS5 — always wins over the table above):** PK/BE → geometric mean, log, 90% CI, 80–125% (never mean±SD+t-test); dissolution → profile + f2 / bootstrap-f2 / Mahalanobis + %RSD; CFD → GCI / mesh-independence; PINN → loss + parity + relative-L2. GROUP-8 (S38–S45) styles are for **in-silico / signal / data-analysis only** — never launder them onto a wet-lab endpoint.

---

## 🛑 ANTI-PATTERN REGISTRY (AP1–AP16) — the "never do this" rules the decision layer enforces

*Distilled from `FriendsDontLetFriends` (C. Li, MIT; DOI 10.5281/zenodo.7542491) with the primary literature it cites. The chooser rejects any candidate style that violates one of these; in a manual DS1 audit, treat any of these as a figure defect. `choose_graph.py` fires the relevant AP as an "enforced rule" for the query.*

| # | Anti-pattern | Do this instead | Ref |
|---|---|---|---|
| AP1 | Bars for means separation (bars hide the distribution) | dot-on-bar / strip / box (S1/S2/S3) | Weissgerber 2015, 10.1371/journal.pbio.1002128 |
| AP2 | Violin / box at small n | strip / dot (quartiles stabilize ~n>50; never <20) | — |
| AP3 | Diverging scale for unidirectional data | sequential scale; endpoints = real max/min/zero | — |
| AP4 | Bar-plot meadow (many bars, multifactor) | facet / group by the factor (M7 small-multiples) | Matand 2020, 10.1186/s12870-020-2243-7 |
| AP5 | Heatmap without reordering rows / columns | cluster / reorder to reveal structure | Li 2022, 10.1101/2022.07.04.498697 |
| AP6 | Heatmap without checking outliers | cap the color scale (~95th pct) so outliers don't wash out signal | — |
| AP7 | Not checking data range per factor level | check per-factor range; narrow effects hide on a shared scale | — |
| AP8 | Network graph with a single layout | try multiple layouts (appearance drives interpretation) | — |
| AP9 | Confusing position- vs length-based encodings | bars zero-based (length encodes value); dots/box are position-based; no broken-axis bars | — |
| AP10 | Pie chart | stacked / side-by-side bars (length beats angle/area) | — |
| AP11 | Concentric donuts | unwrap to stacked bars (outer rings exaggerate) | — |
| AP12 | Red/green & rainbow (jet) color scales | viridis / cividis (colorblind- & greyscale-safe) | Wong 2011, 10.1038/nmeth.1618 |
| AP13 | Stacked bar without reordering segments | order stack segments meaningfully | — |
| AP14 | Mixing stacked bars with mean separation | don't combine proportion-stacking with mean ± error | — |
| AP15 | Histogram for small n | dot / strip | — |
| AP16 | Boxplot for bimodal data | show the distribution (raincloud / histogram) | — |

---

## GROUP 1 — DISTRIBUTIONS (show n, spread, and every raw point)

**S1. Bar + overlaid individual data points (dot-on-bar), mean ± s.d.** [E]
- **Shows:** per-condition central tendency AND every replicate as a dot on/around the bar.
- **Best point:** magnitude *with full transparency of the raw sample at small n* — the reader can count n and see spread/outliers. The single most consistent convention across all 5 exemplars (NBT-2024 Fig 1b–d; NC-2024 Fig 2a; NMat Fig 2a–g).
- **Use when:** any categorical comparison at n ≤ ~15. **NOT when:** the predictor is continuous (use a line/dose-response) or the endpoint is time-to-event (use KM).
- **Pairing:** put it immediately beside the representative image it quantifies (image-then-quantify couplet).
- **Domain note:** for **dissolution** the honest version is a profile, not an endpoint bar; if you must bar a single metric, plot **%RSD** and n ≥ 6–12, never mean±SD with a t-test. For **PK** endpoints (Cmax, AUC) prefer **geometric mean + individual points on a log axis**, not arithmetic mean±SD (see S13, S16).

**S2. Jittered strip / beeswarm (points only, no bar)** [E-variant]
- **Shows:** the raw distribution of a modest-n sample with no bar to imply false precision.
- **Best point:** "here is every measurement" when even a bar overstates certainty. Exemplars overlay dots *on* bars; a pure strip is the honest floor at very small n.
- **Use when:** n is small and the mean is secondary. **NOT when:** you need to communicate a summary magnitude to a broad reader (add the bar back).
- **Pairing:** row of strips across markers/conditions with a shared y-axis.
- **Domain note:** at **n = 3** never use violin/box (S3) — the shape is a lie; strip or dot-on-bar only.

**S3. Violin / box-and-whisker / raincloud** [D — use with care]
- **Shows:** distribution shape (median, IQR, tails, density).
- **Best point:** distribution *shape* at large n — skew, bimodality, outliers.
- **Use when:** n ≳ 20–30 per group. **NOT when:** small n (all 5 exemplars deliberately avoid violin/box at n = 3 and plot points instead — copy that restraint).
- **Pairing:** violin behind a jittered strip (raincloud) so shape and raw points co-exist.
- **Domain note:** for **PK** parameter distributions across a virtual population (PBPK), a box/violin on a **log axis** is appropriate; report **geometric** median/IQR, not arithmetic.

**S4. Overlaid distribution / spectral trace (intensity vs size/wavelength)** [E]
- **Shows:** full curves superimposed (e.g., DLS size distributions for several formulations).
- **Best point:** the distributions are equivalent (overlap) or shifted — a "controls-matched" panel proving a downstream effect is not a size/artifact confound (NC-2024 Fig 3c).
- **Use when:** proving physical equivalence or a shift in a continuous property. **NOT when:** a single scalar (mean size) suffices — then use S1/S9.
- **Pairing:** distribution overlay beside the cryo-TEM (S23) and the size/PDI dual-axis bar (S9).
- **Domain note:** for **particle sizing** always show the distribution, not just Z-average; report PDI. For **dissolution** the analogous "overlay" is the release-profile family (S17), not a distribution.

---

## GROUP 2 — COMPARISONS (rank candidates, contrast conditions)

**S5. Large-N screening bar array (the "library screen")** [E]
- **Shows:** the whole candidate library on one axis (tens of bars), hero towering, benchmarks parked at the far right.
- **Best point:** rank the entire library AND show the winner beats the accepted standard *in the same frame* — the reader sees it wasn't cherry-picked (NC-2025 Fig 2a AA1–AA50 + ALC-0315/SM-102; NMat 72-lipid sweep; NBT-2025 ED1 TS1–TS70).
- **Use when:** a screen/sweep justifies a lead. **NOT when:** ≤ ~5 conditions (use grouped bars S7).
- **Pairing:** **funnel** — the wide screen (S5) → statistically-tested finalists (S6). Park benchmarks in a fixed position (always far right).
- **Domain note:** for a **dissolution/excipient screen** or **PINN-hyperparameter sweep** this is the correct idiom; keep the FDA/marketed reference on the same axis. Uniform bar fill within a screen (height carries the message); do NOT recolor benchmarks to bias the eye.

**S6. Finalist bar + pairwise significance brackets** [E]
- **Shows:** the shortlist (~8–12) with mean ± s.d., dots, and exact-P brackets only on the comparisons that matter.
- **Best point:** *prove* the lead after the screen found it — attach statistics to lead-vs-benchmark, not to every pair (NC-2025 Fig 2c).
- **Use when:** you have a lead to defend. **NOT when:** you have not yet shown the full screen (do S5 first — a finalist panel without the screen looks cherry-picked).
- **Pairing:** the back half of the S5→S6 funnel.

**S7. Grouped / clustered bar (two-factor: condition × category)** [E]
- **Shows:** two-factor structure — e.g., formulation × cell type / organ / timepoint — as colored series within each x-cluster.
- **Best point:** the *interaction* — which treatment wins in which context, read across and within clusters (NBT-2024 Fig 2c/d cell type × treatment; NMat Fig 4i; NC-2025 Fig 3).
- **Use when:** two categorical factors. **NOT when:** one factor (use S1) or one factor is continuous (use S8/S12).
- **Pairing:** small-multiples row of the same grouped panel across readouts with fixed colors (S3-grammar reused).
- **Domain note:** analyze with **two-way ANOVA + a named post-hoc** (Šidák/Tukey), not a stack of t-tests — a mismatched test here is a DS2/DS5 flag.

**S8. Dose–response bar ladder (ascending/descending staircase)** [E]
- **Shows:** monotonic dose-dependence as a staircase of bars + dots (NBT-2024 Fig 2e; NBT-2025 Fig 1f/g).
- **Best point:** "the effect scales with dose" when the doses are a few discrete levels.
- **Use when:** 3–5 discrete dose levels. **NOT when:** a true continuous predictor with many levels (use the dose-response *line/curve* S12 and fit it).
- **Pairing:** two readouts side by side (% positive AND intensity) so dose-dependence is shown on two axes.
- **Domain note:** for a real **concentration-response** with a fitted EC50/Emax, use the **sigmoid line fit** (S12) on a **log-concentration axis**, not bars.

**S9. Dual-axis paired bar (two linked properties of one sample)** [E]
- **Shows:** two physicochemical metrics that share sample identity but not scale — size (nm) + PDI, or zeta + EE% — on twin y-axes (NC-2024 Fig 2f/g; NBT-2025 ED2f/g).
- **Best point:** compact co-report of two linked characterizations of one particle.
- **Use when:** exactly two linked metrics per sample. **NOT when:** the two axes tempt a misleading visual correlation — if the point is a relationship, use a scatter (S10), not twin bars.
- **Pairing:** with cryo-TEM (S23) and the size distribution (S4) as the physicochemical-QC cluster every lead needs.

**S10. Floating / range bar (min→max with mean line) for DoE** [E]
- **Shows:** the observed range at each factor level with a mean line — an orthogonal-array optimization readout (NBT-2025 ED2b/d).
- **Best point:** read the trend of ONE factor while the others vary — a compact box-plot alternative for DoE screens.
- **Use when:** one-factor-at-a-time or orthogonal-array optimization. **NOT when:** you have full factorial interaction data (use a response-surface/heatmap).
- **Pairing:** followed by a **normalized bar with dashed reference = 1** (S11) for the next optimization round.
- **Domain note:** for **formulation DoE** this pairs with an inline **factor table as a panel** (S27) so the design is reproducible on the figure.

**S11. Normalized bar with a dashed reference line (= 1 or = control)** [E]
- **Shows:** fold-change vs a baseline across a condition sweep, with a dashed line at control = 1 (NBT-2025 ED2c/e; NMat normalizes every screen to MC3 = 1.0).
- **Best point:** "better/worse than the standard of care" read **directly off the y-axis** — effect size becomes geometric on the axis.
- **Use when:** the message is fold-improvement over a named benchmark. **NOT when:** absolute values are the point.
- **Pairing:** normalize an entire screen (S5) to the FDA/marketed reference bar so the fold-change is literal.
- **Domain note:** in **IVIVC/PK** the analogous normalization is **within-run to the reference (RLD) arm** to control inter-day variability — state it in the legend.

**S12. Dose–response / concentration–response line with fit** [E-variant]
- **Shows:** a fitted curve (sigmoid/Emax) of response vs a continuous predictor, mean ± s.d. per level.
- **Best point:** the *shape* of the response and derived parameters (EC50, Hill, optimum) — NC-2024 Fig 2c factor sweeps.
- **Use when:** a continuous predictor with enough levels to fit. **NOT when:** 2–3 levels (use S8).
- **Pairing:** a row of small-multiple sweeps, one per factor, shared y-scale.
- **Domain note:** plot on a **log-concentration x-axis**; report the fit with its CI, not just R².

---

## GROUP 3 — RELATIONSHIPS / PARITY (predicted vs observed, correlation)

**S13. Observed-vs-predicted parity plot (y = x line)** [D]
- **Shows:** every prediction against its measurement with the identity line and a scatter band.
- **Best point:** *calibration* of a model — points hug y = x or they don't. The exemplars lack this (they are wet-lab); it is **mandatory** for any PBPK/IVIVC/PINN/CFD prediction claim.
- **Use when:** you claim a model predicts data. **NOT when:** you have no held-out or independent measurements (a parity of training data alone is not validation).
- **Pairing:** parity plot **beside a Bland–Altman** (S14) — parity shows correlation, B-A shows bias/agreement; you need both.
- **Domain note:** **IVIVC** — parity of predicted vs observed Cmax/AUC with the **%PE** annotated (< 10% internal, < 15% mean external), NOT a bare R². **PINN** — parity of predicted vs reference field values with **relative-L2**. **CFD/PBPK** — parity of predicted vs experimental with the identity line, never "agrees well".

**S14. Bland–Altman (difference vs mean) agreement plot** [D]
- **Shows:** the difference between two methods against their mean, with bias line and 95% limits of agreement.
- **Best point:** *systematic bias and the spread of disagreement* — the question a parity plot (S13) cannot answer.
- **Use when:** comparing a prediction to a measurement, or two assays/methods. **NOT when:** you only have correlation (parity) and no paired differences.
- **Pairing:** the companion to every parity plot in IVIVC/PBPK validation.
- **Domain note:** required by **IVIVC** best practice alongside %PE; the limits-of-agreement, not R², tell a reviewer whether the model is fit for regulatory use.

**S15. Correlation / regression scatter with CI band** [D]
- **Shows:** two continuous variables with a fitted line and its confidence band.
- **Best point:** the strength AND uncertainty of a relationship — the band matters as much as the slope.
- **Use when:** an association between two measured quantities. **NOT when:** the x is a designed predictor (use dose-response S12) or the claim is agreement (use S13/S14).
- **Pairing:** annotate with the regression equation, R² or ρ, n, and the test — never a naked cloud.
- **Domain note:** **IVIVC Level A** is a point-to-point correlation of fraction-absorbed vs fraction-dissolved — show the line, the band, and the validation metrics, not R² alone.

**S16. Levy plot (in-vivo time vs in-vitro time)** [D]
- **Shows:** the time-scaling relationship between in-vitro dissolution and in-vivo absorption.
- **Best point:** the IVIVC time correspondence — the classical dissolution↔absorption mapping.
- **Use when:** establishing/illustrating an IVIVC time relationship. **NOT when:** no in-vivo absorption data exist.
- **Pairing:** with the fraction-absorbed-vs-fraction-dissolved parity (S15) and the deconvolution profiles.
- **Domain note:** a dissolution/IVIVC-native idiom the wet-lab corpus has no analog for — reach for it instead of forcing a generic scatter.

---

## GROUP 4 — SENSITIVITY / UNCERTAINTY (what drives the result, how sure are we)

**S17. Diverging log2 fold-change heatmap (overview) + promoted bars (detail)** [E]
- **Shows:** a wide matrix (analytes × arms) as signed color on a blue↔white↔red diverging scale, then the decisive rows re-plotted as bars with stats (NC-2025 Fig 5d→e: 24-cytokine heatmap → quantified bars).
- **Best point:** **the landscape then the proof** — compress a high-dimensional multiplex into one glance, then quantify the few that matter. Avoids both an unreadable wall of bars and a heatmap with no statistics.
- **Use when:** many variables × few conditions, quantity is a signed fold-change. **NOT when:** the quantity is not signed (use a sequential, not diverging, scale).
- **Pairing:** heatmap (gestalt) → zoom bars (S6-style) for the decisive few; share the arm color key.
- **Domain note:** directly portable to **CFD/PBPK parameter sweeps** and **PINN hyperparameter maps** — sensitivity as a heatmap, then zoom bars for the dominant parameters (see the figure-strategy Example 3 rebuild).

**S18. Tornado / forest sensitivity plot** [D]
- **Shows:** the swing in an output as each input is varied ±, bars sorted by magnitude around a base-case line.
- **Best point:** *which parameters dominate the outcome*, ranked — the one-glance sensitivity ranking a heatmap gestalt cannot order.
- **Use when:** local one-at-a-time sensitivity of a PBPK/CFD/PK model. **NOT when:** you need interaction structure (use the heatmap S17 or a response surface).
- **Pairing:** tornado (ranking) beside the parameter's parity impact — ablating the top parameter should collapse the parity (mechanism by loss-of-function, in-silico).
- **Domain note:** the base-case reference line is drawn in **grey** (see publication-ready-figures.md entity map); label the axis with the actual output units, not "sensitivity".

**S19. Loss / convergence curve (training + validation)** [D]
- **Shows:** loss (and metric) vs epoch for train and validation, on a log-y axis.
- **Best point:** the model *converged and did not overfit* — the train/val gap is the story.
- **Use when:** ANY PINN/ML result. **NOT when:** a single scalar accuracy is claimed with no curve — that is a DS5 red flag ("accurate" without a loss curve).
- **Pairing:** loss curve → parity (S13) → relative-L2 report; seeds/splits stated.
- **Domain note:** **PINN** must show loss curves + parity + relative-L2 + seed/split, never "accurate" (domain-conventions §0).

**S20. Grid-convergence / mesh-independence plot (GCI)** [D]
- **Shows:** a monitored quantity vs mesh resolution (or 1/N cells) approaching an asymptote, with the GCI band.
- **Best point:** the CFD result is *mesh-independent* — the discretization is not driving the answer.
- **Use when:** ANY CFD claim. **NOT when:** a single contour is shown with "agrees well" and no convergence evidence (DS5 blocker).
- **Pairing:** GCI plot + y+ check + a validation overlay (predicted vs measured) — the CFD credibility triad.
- **Domain note:** required by **ASME V&V 20**; a bare contour without GCI/y+/validation is a laundered "seeing-is-believing" panel that reviewers reject.

**S21. Error / uncertainty band on a time-course (CI or s.d. ribbon)** [E]
- **Shows:** a line with a shaded band per timepoint.
- **Best point:** the trajectory AND its uncertainty over time in one continuous read (NC-2025 tumor-growth ± s.d.; NMat Fig 6b).
- **Use when:** a continuous process over time with replicate spread. **NOT when:** discrete conditions (use bars).
- **Pairing:** band curve → AUC summary bar (S24) collapsing the kinetics to one scalar.
- **Domain note:** for **PK profiles** show mean concentration–time as a line with s.d. band on the linear axis AND a **semi-log** companion (S13-adjacent) so the terminal phase is legible; report the exposure summary as geometric-mean AUC (S24).

---

## GROUP 5 — FLOW / COMPOSITION (design space, structure, pipelines)

**S22. Chemical-structure grid / R-group library plate (small-multiples of molecules)** [E]
- **Shows:** a combinatorial library as a grid of skeletal structures + a boxed R-group legend (NBT-2024 Fig 1a 4×3; NC-2024 Fig 1b R1–R10; NC-2025 Fig 1b; NMat Fig 1b).
- **Best point:** the structural variation that is the independent variable — "here is the design space" in one panel, so downstream bar labels (DIM1…) are unambiguous.
- **Use when:** a structure–activity library. **Pairing:** place the R-group ladder *immediately left of* the bar chart that ranks those exact structures (S5) — reading left-to-right IS the SAR.

**S23. Micrograph with scale bar (cryo-TEM / EM / confocal)** [E]
- **Shows:** structural/morphological ground-truth for the lead (NC-2024 Fig 2h; NBT-2025 ED2h 100 nm).
- **Best point:** *plausibility* — the particle is spherical/intact, the dye is cytosolic. The image proves plausibility; the adjacent quantified panel proves magnitude.
- **Use when:** a lead formulation is claimed. **NOT when:** it stands alone as evidence (orphan image = red flag) — always pair with quantification.
- **Pairing:** micrograph + size/PDI/zeta/EE bar (S9) + distribution (S4) = the mandatory physicochemical-QC cluster.

**S24. AUC / summary-scalar bar (collapse a curve to one number)** [E]
- **Shows:** the area under a time-course as one bar per group + dots (NC-2024 Fig 4d normalized wound-AUC).
- **Best point:** distill a kinetic curve into a single comparable scalar so groups can be tested.
- **Use when:** a time-course needs a statistical summary. **NOT when:** it replaces the profile — show BOTH the curve (S21) and its AUC.
- **Domain note:** **PK** — AUC is the exposure metric, but report **dose-normalized, geometric-mean AUC** with the profile; for **BE**, the endpoint is the **90% CI of the AUC/Cmax ratio within 80–125%**, not a bar with a t-test (S25).

**S25. Confidence-interval / equivalence forest (ratio vs bounds)** [D]
- **Shows:** point estimate + CI for each metric against equivalence bounds.
- **Best point:** *bioequivalence* — does the 90% CI of the test/reference ratio fall within 80–125%.
- **Use when:** BE / comparative bioavailability. **NOT when:** mean±SD + t-test is used instead (that is the classic laundered-PK error and a DS5 blocker).
- **Pairing:** CI forest for Cmax and AUC with the 80–125% band drawn as reference lines.

**S26. Sankey / alluvial / flow diagram** [D]
- **Shows:** how quantities or cohorts split and merge across stages.
- **Best point:** mass balance or cohort flow (e.g., dose disposition, patient/animal accounting, model compartment fluxes).
- **Use when:** a conserved quantity redistributes across compartments/stages. **NOT when:** a simple bar of proportions suffices.
- **Domain note:** for **PBPK** a compartment-flux Sankey can make disposition legible; keep it schematic, pair with the quantitative fractions.

**S27. Inline data table as a figure panel (DoE / lookup)** [E]
- **Shows:** the molar/mass/N:P ratios of each optimization run, or a code↔identity legend, rendered as a panel (NC-2024 Fig 2b; NBT-2025 ED2a; NBT-2025 Fig 1c PB code table).
- **Best point:** make the design reproducible *on the figure*, and let dense screen axes use short codes without a bloated legend.
- **Use when:** a DoE or a coded screen. **Pairing:** table-as-panel beside the bar charts it indexes.

---

## GROUP 6 — TIME-COURSE (kinetics, trajectories, longitudinal)

**S28. Multi-series kinetic / time-course line (mean ± s.d.)** [E]
- **Shows:** a continuous process over time, one line per condition (NC-2024 Fig 3a expression durability; NBT-2025 Fig 2b body weight).
- **Best point:** the **divergence of curves over time IS the finding** — durability, recovery, decline kinetics.
- **Use when:** a continuous readout sampled over time. **NOT when:** one endpoint (then it is a bar — but ask whether you are throwing away the profile).
- **Pairing:** kinetic line (S28) → AUC summary bar (S24); hero condition in the accent hue.
- **Domain note:** **dissolution** and **PK** profiles are this family — see S17-release and S21-PK. Never reduce a release/PK profile to a single-timepoint bar (figure-strategy Example 2 anti-pattern).

**S29. Dissolution / release profile overlay (% released vs time)** [D]
- **Shows:** cumulative % released vs time for each formulation + the reference product, with n ≥ 6–12 and error bars.
- **Best point:** the *whole release behaviour* and its similarity to the reference — the dissolution-native profile.
- **Use when:** any dissolution/release claim. **NOT when:** an endpoint bar at 24 h stands in for the profile (anti-pattern).
- **Pairing:** profile overlay + an **f2 / bootstrap-f2 CI / Mahalanobis** similarity readout (NOT ANOVA on an endpoint %).
- **Domain note:** this is a DS5 correctness point — the similarity metric is f2/bootstrap-f2/Mahalanobis, and the profile carries %RSD, per `domain-conventions.md` §0.

**S30. Semi-log PK concentration–time profile** [D]
- **Shows:** plasma concentration vs time on a log-y axis, one line per treatment.
- **Best point:** the *terminal elimination phase* and multi-phasic kinetics that a linear axis hides.
- **Use when:** any PK profile. **NOT when:** only a linear plot is shown (the terminal phase becomes illegible).
- **Pairing:** semi-log profile + linear profile companion + geometric-mean AUC/Cmax bar (S24) + BE forest (S25).
- **Domain note:** **PK** uses geometric mean, log-scale, 90% CI, 80–125% — never mean±SD on a linear axis + t-test (domain-conventions §0).

**S31. Kaplan–Meier survival / time-to-event step curve + log-rank** [E]
- **Shows:** probability vs time as a step function per group, log-rank (Mantel–Cox) P stacked in a corner (NBT-2025 Fig 2c; NC-2024 Fig 4e wound-closure repurposed).
- **Best point:** the definitive time-to-event endpoint — a bar of "% responded at endpoint" is the classic wrong primitive here.
- **Use when:** survival, time-to-closure, time-to-progression. **NOT when:** the endpoint is a molecular readout at a fixed time (then a bar is correct).
- **Pairing:** fixed couplet — tumor-growth line (S21) immediately left of its KM survival (S31), same arm colors.

**S32. IVIS / spatial heat-overlay image grid (shared calibrated colorbar)** [E]
- **Shows:** small-multiples of luminescent animals/organs, rows = formulation, columns = timepoint, ONE shared radiance colorbar (NC-2025 Fig 2d; NMat Fig 2h; NBT-2025 ED1d/f).
- **Best point:** spatial/biodistribution signal *where it physically happens*, quantitatively comparable because tiles share the scale.
- **Use when:** spatial confirmation of a quantitative bar. **NOT when:** tiles have independent scales (uncomparable) or the rainbow LUT is used for categorical data.
- **Pairing:** the qualitative companion to the quantitative uptake bar (S1); hero tile saturated.

---

## GROUP 7 — CLASSIFICATION / GATES / DIAGNOSTIC (raw evidence behind a summary)

**S33. Flow-cytometry density / dot plot with on-plot % gate** [E]
- **Shows:** 2-D density (marker × SSC) with the quadrant % printed in-plot, often as a timepoint or condition series (NC-2025 Fig 4c; NMat Fig 3g).
- **Best point:** the **primary gate is real** behind the summarizing bar placed immediately adjacent — the dot plot shows the gate, the bar quantifies it across replicates.
- **Use when:** a % positive is claimed. **NOT when:** the summary bar stands alone (orphan statistic) — always pair raw-plot + summary-bar.
- **Pairing:** flow plot (S33) beside its quantifying bar (S1/S7).

**S34. Flow-histogram overlay stack (offset density curves per marker)** [E]
- **Shows:** overlaid fluorescence-intensity density curves across conditions, small-multiples per marker (NC-2024 Fig 3e CD markers).
- **Best point:** "phenotype unchanged" — histogram overlap = no drift.
- **Use when:** showing identity/phenotype is preserved. **Pairing:** a row of markers with a shared x-axis.

**S35. ROC / PR curve** [D]
- **Shows:** true-positive vs false-positive (ROC) or precision vs recall (PR) across thresholds, with AUC.
- **Best point:** classifier discrimination — the exemplars lack it; needed for any diagnostic/classification model.
- **Use when:** a classification model with a probabilistic score. **NOT when:** the outcome is regression (use parity S13) or classes are heavily imbalanced without PR (prefer PR over ROC).
- **Pairing:** ROC/PR + a calibration plot + a confusion matrix at the operating threshold.

**S36. Confusion matrix / calibration plot** [D]
- **Shows:** predicted vs actual class counts (confusion) or predicted probability vs observed frequency (calibration).
- **Best point:** *where* a classifier errs, and whether its probabilities are trustworthy.
- **Use when:** reporting a classifier's operating behaviour. **Pairing:** with ROC/PR (S35); state the threshold, n, and class balance.

**S37. Multichannel IF overlay + small-multiples micrograph matrix** [E]
- **Shows:** rows = condition, columns = channel/day, fixed channel→color code, one shared scale bar (NC-2024 Fig 3i; NMat Fig 4c–e).
- **Best point:** colocalization / cell-type-specific delivery read across channels; faceted qualitative comparison.
- **Use when:** multichannel imaging. **Pairing:** image matrix + its paired quantification bar (image-then-quantify).

---

## GROUP 8 — FIELDS, SPECTRA & DIMENSIONALITY (in-silico, signal & data-analysis) [K]

*Distilled from Nathan Kutz's `ScientificComputing` notebooks (`Data-Driven Modeling & Scientific Computation`, 2nd ed.) — the field / spectral / reduced-order idioms the wet-lab exemplar corpus structurally cannot teach. **Scope rule (DS5):** these are for **CFD / PINN / IVIVC-modeling / PBPK / signal / data-analysis** deliverables. They are NOT wet-lab defaults — never put a scree plot or a phase portrait where a dissolution profile or a dot-on-bar belongs, and never let a pretty field surface stand in for the GCI / parity / validation a modeling claim owes (S13 / S14 / S19 / S20).*

**S38. 3D solution-field surface (`plot_surface`) with view-angle control** [D-K]
- **Shows:** a scalar field over two coordinates — u(x, t), a CFD pressure/velocity field, a PINN solution surface — rendered as a surface.
- **Best point:** the *global shape* of a solution/field at a glance (fronts, shocks, decay, boundary-layer structure) that a flat line cannot convey.
- **Use when:** communicating the qualitative structure of a 2D field as an orientation panel. **NOT when:** the reader needs exact values (pair with a heatmap S40 or line-cuts) — a surface is for gestalt, not measurement, and a rotated view can hide error.
- **Pairing:** surface for shape → S40 heatmap / 1D line-cuts for quantitative reading → S13 parity + S20 GCI for the validation the surface does NOT provide.
- **Domain note:** **CFD/PINN** — a solution surface is an *orientation* panel only; it never substitutes for mesh-independence (S20), parity (S13), or relative-L2/%PE. State the view angle so the figure is reproducible.

**S39. Waterfall / stacked-offset profile plot** [D-K]
- **Shows:** a family of 1D curves stacked with a depth/vertical offset so many profiles are legible at once — release curves across formulations, spectra over time, a PDE solution evolving.
- **Best point:** *evolution or family structure* — how a profile shifts across a condition/time without 20 overplotted lines.
- **Use when:** many related 1D traces share an x-axis and the story is how they change. **NOT when:** you need precise cross-profile comparison at a fixed x (use an overlay S29 or small-multiples M7) — offsets distort direct reading.
- **Pairing:** waterfall for the family → S29 overlay (with f2 / %RSD) for the two profiles that carry the claim.
- **Domain note:** **dissolution/release** — a waterfall of release curves is a legitimate *landscape* panel, but the similarity claim still needs the S29 overlay + f2 / bootstrap-f2 / Mahalanobis + %RSD (`domain-conventions.md` §0); the waterfall does not replace it.

**S40. 2D field / matrix heatmap (`pcolormesh` / `imshow`) + calibrated colorbar** [D-K]
- **Shows:** a 2D field slice, a parameter-sweep grid, or a matrix (correlation, distance) as color, with a quantitative colorbar.
- **Best point:** *where* in a 2D domain the magnitude concentrates — a field slice, a sensitivity grid, a correlation structure.
- **Use when:** the quantity is genuinely 2D and continuous. **NOT when:** it is a signed fold-change over a control (use the diverging S17) or a spatial luminescence overlay on anatomy (use S32). Use a **sequential, perceptually-uniform, colorblind-safe** map (viridis/cividis), never jet.
- **Pairing:** heatmap for the landscape → zoom bars (S6) for the decisive cells (the M4 landscape-then-proof move).
- **Domain note:** **CFD/PBPK/PINN** — label the colorbar with real output units, and pair a field slice with its GCI/validation (S20), never a bare "agrees well" field.

**S41. Spectrogram / time-frequency (Gabor / STFT)** [D-K]
- **Shows:** how a signal's frequency content changes over time (time on x, frequency on y, power as color).
- **Best point:** *non-stationary* structure — transients, drift, mode-switching — invisible in either a raw time trace or a single FFT.
- **Use when:** a time-series / sensor / unsteady-CFD signal has time-varying spectral content. **NOT when:** the signal is stationary (a single power spectrum S42 suffices) or the axis is not time.
- **Pairing:** raw time trace above → spectrogram below (shared time axis) → denoised reconstruction if the point is filtering.
- **Domain note:** state the **window length** (the Gabor/STFT time–frequency resolution trade-off) — an unstated window is a hidden knob, like an undeclared bin width.

**S42. Stem plot — discrete / sparse spectrum** [D-K]
- **Shows:** discrete coefficients as stems from a baseline — an FFT magnitude spectrum, or the *sparse* nonzero terms a LASSO / PDE-FIND / compressed-sensing fit selected.
- **Best point:** *which discrete modes/terms are active and how large* — sparsity and dominance, without a continuous line implying values between the integers.
- **Use when:** the x-axis is genuinely discrete (frequencies, mode indices, library terms). **NOT when:** the underlying variable is continuous (use a line).
- **Pairing:** stem of selected terms beside the reconstructed-vs-true signal (the sparse-identification "these few terms suffice" argument).
- **Domain note:** **PINN / data-driven modeling** — a sparse-governing-equation claim (PDE-FIND / SINDy) needs the stem of selected coefficients + a held-out reconstruction, paired with the cross-validation that chose the sparsity (`statistics-rigor.md` §F).

**S43. Singular-value (scree) spectrum + cumulative-variance** [D-K]
- **Shows:** the SVD singular values (or PCA eigenvalues) on a **semilog** axis, with a companion cumulative-energy curve.
- **Best point:** *effective rank / how many modes matter* — the justification for a reduced-order model or a truncation r.
- **Use when:** you reduce dimensionality (SVD / PCA / POD / ROM) and must defend the cut-off. **NOT when:** there is no reduction step — a scree plot on a 3-point dataset is theatre.
- **Pairing:** scree (choose r) → S44 score plot in the retained modes → reconstruction error vs r.
- **Domain note:** **CFD/PINN/data-analysis** — state the variance captured at the chosen r and show reconstruction error; "we kept the top modes" without the scree + cumulative curve is an unjustified truncation.

**S44. PCA / low-dimensional projection (score plot) + variance-explained** [D-K]
- **Shows:** data projected onto its leading principal components (PC1 vs PC2/PC3), points colored by condition, with the % variance on each axis and — where it aids interpretation — the loadings.
- **Best point:** *structure in high-dimensional data* — clusters, separation, gradients — reduced to a readable 2D/3D scatter.
- **Use when:** many variables per sample and the question is grouping/separation. **NOT when:** you imply the projection *proves* a difference — a separated score plot is a hypothesis, not a test (back it with a held-out classifier S35/S36 + cross-validation).
- **Pairing:** score plot → S43 scree (how much variance those axes hold) → S36 confusion/calibration if a class claim is made.
- **Domain note:** always print **% variance per axis**; a PCA scatter without it hides how much structure was discarded. Color by entity per the manuscript-wide map (`publication-ready-figures.md` R5).

**S45. Phase portrait / state-space trajectory** [D-K]
- **Shows:** a dynamical system's trajectory in state space (x vs ẋ, or a 3D attractor) rather than each variable vs time.
- **Best point:** *qualitative dynamics* — fixed points, limit cycles, attractors, stability — that time-series hide.
- **Use when:** the system is a dynamical/ODE model and the point is its qualitative behaviour. **NOT when:** the audience needs magnitudes vs time (pair with a time trace S21).
- **Pairing:** time trace (S21) beside the phase portrait — the reader sees both "when" and "the geometry of the dynamics."
- **Domain note:** **PK/PBPK compartmental** and **reduced-order dynamical** models — a phase portrait can make stability/steady-state legible, but the quantitative claim still lives in the concentration–time profile (S30) and its exposure metrics.

---

## MULTI-PANEL STORYTELLING PATTERNS (compose panels into an argument)

The exemplars never dump panels; each figure walks **one act** of the argument in reading order. Reuse these composition patterns:

**M1. The funnel (screen → finalists → proof).** Wide large-N screen (S5) → statistically-tested finalist bar (S6) → mechanism/readout. *Archetype:* NC-2025 Fig 2. Reuse wherever a screen precedes a claim (dissolution/excipient/hyperparameter screens included).

**M2. Panel `a` = orientation, always.** Every results figure opens with a mechanism schematic or a study-timeline (S9-family) as panel `a`, defining the labels every data panel reuses. Never a data panel before its explanatory cartoon.

**M3. Image-then-quantify couplet.** A representative image (micrograph S23 / IVIS S32 / flow S33) sits immediately beside the bar that quantifies exactly what it shows. The eye and the statistic are adjacent, so a skeptic validates the number against the picture. All 5 exemplars do this; it is the single most portable intra-figure move.

**M4. Landscape-then-proof.** A wide diverging heatmap (S17) gives the whole landscape; a curated row of bars (S6/S7) re-plots only the entries carrying significance. Heatmap for gestalt, bars for statistics — they share the color key. Portable to CFD/PBPK/PINN sensitivity maps.

**M5. Fixed couplets.** Tumor-growth line (S21) + KM survival (S31), left-to-right, same colors. Raw flow plot (S33) + its summary bar. mRNA panel + protein panel (orthogonal two-level validation of one claim). Twin panels differing in ONE variable (S. aureus vs P. aeruginosa; 6 h vs 12 h; low vs high dose) so the reader learns the panel once and reads its twin free.

**M6. Structure-beside-data.** The R-group ladder (S22/S27) immediately left of the bar chart ranking those exact structures (S5) — reading left-to-right IS the structure–activity relationship.

**M7. Small-multiples with shared axes.** Anything with a sub-dimension (markers, factors, cell types, days) becomes a row of identical-grammar small panels with a shared y-scale and ONE shared legend — scannable as a single comparison rather than a dozen re-decoded charts.

**M8. Translational ladder across the sequence.** The figure program escalates model relevance: in-vitro → reporter/normal animal → disease model → ex-vivo human tissue / primary cells. The human-tissue capstone is designed in from the start. *In-silico analog:* toy problem → benchmark case → real geometry/population → prospective/out-of-sample validation.

**M9. In-silico validation triad (domain-required).** For any modeling figure, compose: **loss/convergence** (S19) or **GCI** (S20) → **parity** (S13) → **Bland–Altman / relative-L2 / %PE** (S14) → **sensitivity** (S17/S18) with mechanism-by-ablation. This is the M3/M5 discipline translated into the PK/PBPK/IVIVC/CFD/PINN world the wet-lab corpus cannot teach.

---

## QUICK-PICK INDEX (intent → style)

| If the point is… | Use |
|---|---|
| Show n and spread honestly at small n | S1 dot-on-bar (never S3 violin at n=3) |
| Rank a whole library, mark the hit vs benchmark | S5 large-N screen → S6 finalists |
| Two-factor interaction | S7 grouped bar (two-way ANOVA) |
| Dose-dependence, few levels / many levels | S8 bar ladder / S12 fitted line |
| Two linked particle properties | S9 dual-axis bar |
| DoE optimization | S10 range bars → S11 normalized-to-control → S27 table |
| Fold-change over standard of care | S11 normalized, dashed ref = 1 |
| Model predicts data (calibration + bias) | S13 parity + S14 Bland–Altman |
| IVIVC correlation / time-scaling | S15 regression + %PE / S16 Levy |
| Which parameters dominate | S17 heatmap (landscape) / S18 tornado (ranking) |
| PINN converged, didn't overfit | S19 loss curves + parity + relative-L2 |
| CFD is mesh-independent | S20 GCI + y+ + validation overlay |
| Trajectory + uncertainty over time | S21 band curve → S24 AUC bar |
| Design space / SAR | S22 structure grid beside S5 ranking |
| Physicochemical QC of a lead | S23 cryo-TEM + S9 + S4 |
| Bioequivalence | S25 90% CI forest vs 80–125% (never mean±SD+t-test) |
| Dissolution behaviour + similarity | S29 profile overlay + f2/bootstrap-f2/Mahalanobis |
| PK exposure | S30 semi-log profile + geometric AUC + S25 BE forest |
| Time-to-event | S31 Kaplan–Meier + log-rank (never an endpoint bar) |
| Spatial signal across conditions | S32 IVIS grid, shared calibrated colorbar |
| Raw gate behind a % | S33 flow density + adjacent bar |
| Classifier performance | S35 ROC/PR + S36 confusion/calibration |
| Colocalization | S37 multichannel IF matrix + paired count bar |
| Structure of a 2D solution field | S38 3D surface (orientation) + S40 heatmap (values) |
| A family of profiles evolving over condition/time | S39 waterfall → S29 overlay for the claim |
| Where magnitude concentrates in a 2D field/sweep | S40 field heatmap (sequential CB-safe map + colorbar) |
| Non-stationary / time-varying frequency content | S41 spectrogram (state the window length) |
| Which discrete modes / sparse terms are active | S42 stem (FFT / LASSO / PDE-FIND) |
| How many modes to keep (rank / truncation) | S43 scree + cumulative variance |
| Structure / clusters in high-dimensional data | S44 PCA score plot (+ % variance per axis) |
| Qualitative dynamics of an ODE / dynamical model | S45 phase portrait + S21 time trace |

---

*Reference document — Graph-Style Library dimension. Styles tagged [E] are grounded in the 5 exemplar mining files in `_exemplar_mining/`; styles tagged [D] are the domain-required families (`domain-conventions.md`) the wet-lab corpus lacks; styles tagged [K] (GROUP 8, S38–S45) are the in-silico / signal / dimensionality families distilled from Nathan Kutz's `ScientificComputing` repo (`Data-Driven Modeling & Scientific Computation`, 2nd ed.; https://github.com/nathankutz/ScientificComputing) — technique/idiom only, no code copied. Selecting a style is a DS1 craft decision; the domain-correctness of that style is a DS5 gate — read both modules together. GROUP-8 styles carry a hard scope rule: they are for modeling / signal / data-analysis deliverables and must never be laundered onto wet-lab dissolution / PK / BE / biological-endpoint outputs.*

*Access model: don't browse this file top-to-bottom — use the **DECISION LAYER** at the top (`scripts/choose_graph.py`, backed by `scripts/graph_catalog.json`) to get a ranked answer + the enforced anti-patterns + palette/engine/stat in one call; the **ANTI-PATTERN REGISTRY** (AP1–AP16, from `FriendsDontLetFriends`, MIT) is the reject-rule set; journal style-engines (SciencePlots, ultraplot — MIT) and colorblind-gated journal palettes (ggsci/ggprism hex; GPL-3 code NOT used) live in `publication-ready-figures.md` R4/R12. The style entries here are the detail the chooser points into.*
