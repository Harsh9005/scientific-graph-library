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

**Provenance tag key:** [E] = used by ≥1 exemplar (panel cited); [D] = domain-required family the exemplars lack but PK/IVIVC/CFD/PINN work needs (grounded in `domain-conventions.md`, not in the wet-lab corpus); [K] = distilled from Nathan Kutz's *ScientificComputing* repository (*Data-Driven Modeling & Scientific Computation*, 2nd ed.) — technique/idiom only, no code copied — for the in-silico / signal / data-analysis families (GROUP 8); [R] = added from the user-supplied published-figure corpus (GROUP 9, S46–S62; GROUP 9b, S63–S68), each rebuilt from synthetic data in `examples/`.

---

## ⚡ DECISION LAYER — decide first, don't browse (this is how to USE the library)

**The library is an INDEX, not a reading list. To pick a chart, DECIDE — do not scroll 74 styles.** Two equivalent paths, both backed by the single machine-readable index `scripts/graph_catalog.json` (styles + anti-patterns + palettes + style-engines + stat-methods stored once, not re-derived):

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

## GROUP 9 — REFERENCE-FIGURE ADDITIONS (S46–S62) [R]

*Added 2026-07-19 from a set of user-supplied published reference figures. These fill decision gaps the
first 45 styles could not answer — paired designs, threshold-banded readouts, dual-encoded matrices,
enrichment/GSEA, cytometry gating, multi-stage flow, and study/pipeline orientation panels. Every one is
rendered from synthetic seeded data in `examples/` (IDs in brackets). **Scope rule (DS5):** the
omics/cytometry family (S49–S54) belongs to omics / single-cell / cytometry deliverables — never launder
a dot-plot matrix or a gating panel onto a dissolution, PK, BE or bioequivalence endpoint.*

**S46. Paired before/after plot with per-subject connecting lines** [D] · *gallery A18*
- **Shows:** each subject's own two measurements joined by a line, over a box/violin at each timepoint.
- **Best point:** *the within-subject change* — direction and consistency, which two side-by-side boxes destroy.
- **Use when:** the design is paired (crossover, pre/post, matched). **NOT when:** groups are independent.
- **Pairing:** colour the lines by direction of change so responders/non-responders separate visually.
- **Domain note:** **PK/BE crossover** data are paired by subject — pair the points *and* analyse paired, on the log scale (S25/S30). Hiding the pairing overstates variance and is a DS2 error.

**S47. Dot plot against shaded reference / threshold zones** [D] · *gallery C16*
- **Shows:** one estimate per unit on a common axis, with interpretation bands behind them.
- **Best point:** turns a bare ranking into a *call* — below / within / above the target.
- **Use when:** a decision threshold exists (therapeutic window, breakpoint, spec limit). **NOT when:** no principled threshold exists — invented bands are editorialising.
- **Pairing:** sort units by value so the crossing point is obvious.
- **Domain note:** **PK** — a trough/therapeutic-window band must cite its source; state whether it is a label limit, a guideline, or this study's own definition.

**S48. Broken-axis dot plot for a long-tailed count** [D] · *gallery A19*
- **Shows:** a compressed upper segment so a heavy tail does not crush the low-value groups.
- **Best point:** keeping *both* ends readable when the range spans orders of magnitude.
- **Use when:** dots/points (position encodes value). **NOT when:** bars — **AP9 forbids breaking a bar axis** because length must encode value. Try a log axis first; a break is the fallback.
- **Pairing:** mark the break on both facing spines and state the compression.
- **Domain note:** particulate/CFU/event counts are the usual case; consider a log axis or a count model before breaking the axis at all.

**S49. Dual-encoded dot-plot matrix (size = fraction, colour = level)** [K] · *gallery J02*
- **Shows:** two statistics per cell of a feature × group matrix — the fraction of units positive (dot area) and the mean level (dot colour).
- **Best point:** *prevalence and intensity together*, which a heatmap (one number per cell) cannot carry.
- **Use when:** both statistics exist and both matter. **NOT when:** only one does — then use a heatmap and stop implying a second.
- **Pairing:** a size legend AND a colorbar; scale colour across the whole matrix, not per row, or near-zero features render bright and mislead.
- **Domain note:** **single-cell/omics** idiom. Do not transplant it onto formulation endpoints where "% expressing" has no meaning.

**S50. Matrix heatmap with categorical annotation tracks** [K] · *gallery J06*
- **Shows:** the value matrix plus thin categorical strips (group, batch, timepoint) aligned above the columns.
- **Best point:** whether the block structure follows the *biology* or a *confounder* — the question a bare heatmap begs.
- **Use when:** samples carry metadata worth auditing. **NOT when:** the matrix is unordered (AP5 — reorder or cluster first).
- **Pairing:** order columns by the annotation; direct-label groups inside the track where they fit.
- **Domain note:** use a diverging scale ONLY if the matrix is genuinely signed (z-score); sequential otherwise (AP3).

**S51. Enrichment dot plot (ratio on x, count as size, FDR as colour)** [K] · *gallery J04*
- **Shows:** enriched sets ranked, with gene ratio, set size and adjusted significance in one panel.
- **Best point:** three quantities where an enrichment *bar* shows one.
- **Use when:** reporting over-representation results. **NOT when:** you have a ranked-metric question — that is GSEA (S52).
- **Pairing:** enrichment dot plot for the landscape → the specific genes/pathway that carries the claim.
- **Domain note:** adjust p across **all** sets tested, not just those plotted, and state the background universe — an unadjusted or selectively-adjusted FDR is a DS2 defect.

**S52. GSEA running-enrichment plot (ES curve + member rug + ranked metric)** [K] · *gallery J05*
- **Shows:** the running enrichment statistic over the ranked list, where set members fall, and the metric itself — three tiers on one x.
- **Best point:** *is this set concentrated at one end of the ranking* — a threshold-free question over-representation cannot answer.
- **Use when:** you have a full ranked list. **NOT when:** you only have a cut-off gene list (use S51).
- **Pairing:** the running plot for the headline set; a table/dot plot for the family.
- **Domain note:** NES and FDR must come from a real permutation null over a **family** of sets — an FDR computed over a single set is meaningless decoration.

**S53. Embedding + feature-plot couplet** [K] · *gallery J01*
- **Shows:** one embedding twice — coloured by cluster, then the identical coordinates re-coloured by one continuous feature.
- **Best point:** ties an unsupervised structure to an interpretable quantity without a second layout.
- **Use when:** explaining what a cluster *is*. **NOT when:** you imply the projection proves a difference.
- **Pairing:** direct on-plot cluster labels beat a long legend; keep coordinates identical between panels.
- **Domain note:** a separated embedding is a **hypothesis, not a test** — back a class claim with a held-out classifier (S35/S36) and cross-validation.

**S54. Sequential gating-strategy panel row** [D] · *gallery J07*
- **Shows:** each gate applied to the population the previous gate kept, with the % of parent at every step.
- **Best point:** makes a reported percentage *auditable* — the reader sees the chain that produced it.
- **Use when:** any cytometry/sorting percentage is a headline number. **NOT when:** a single bivariate plot already tells it (use S33).
- **Pairing:** the gating row above the summary bar it justifies (the M3 image-then-quantify move).
- **Domain note:** report % of parent AND final % of total; a bare "45% CD8+" with no gating panel is unreviewable.

**S55. Multi-stage alluvial / cohort flow with proportional ribbons** [D] · *gallery E06*
- **Shows:** a fixed cohort branching through sequential stages, ribbon width ∝ count.
- **Best point:** *where the cohort goes and what it costs* across several decision points at once.
- **Use when:** ≥3 stages. **NOT when:** one split (that is a stacked bar).
- **Pairing:** label n at every node and state the conserved total.
- **Domain note:** **mass must balance** at every stage — an alluvial whose widths do not sum is a data error, not a style choice. For a dose/mass balance, say what the conserved quantity is.

**S56. Radial dendrogram with value-scaled tip markers** [K] · *gallery E07*
- **Shows:** a hierarchy in polar layout with a measured value encoded at each tip.
- **Best point:** *selectivity across a large fixed family* — many tips readable in a compact square.
- **Use when:** the tree is a known reference structure and your data are the tip values. **NOT when:** the clustering itself is the result — use a rectangular dendrogram (D05) where branch lengths are readable.
- **Pairing:** a size legend; colour by clade.
- **Domain note:** state the linkage and distance metric; a radial layout hides branch length, so never make a distance claim from it.

**S57. Network with detected communities + labelled hubs** [K] · *gallery E08*
- **Shows:** a force-directed graph coloured by detected community, sized by degree/centrality, with only the hubs labelled.
- **Best point:** *modular structure and who the hubs are* — the interpretable layer over a hairball.
- **Use when:** the graph has real modularity. **NOT when:** labelling every node (unreadable) or asserting structure from one layout.
- **Pairing:** the network for the landscape → bars/tables for the quantities.
- **Domain note:** **AP8** — appearance drives interpretation, so name the layout AND its seed, name the community algorithm, and report modularity; try more than one layout before believing what you see.

**S58. Study-design / dosing-timeline schematic** [D] · *gallery I08*
- **Shows:** arms as rows on a real time axis, with dose events, treatment windows and labelled milestones.
- **Best point:** the reader can *reproduce the study* before reading a single result panel.
- **Use when:** any in-vivo/clinical/multi-arm design. **NOT when:** it would restate a simple two-group design already stated in one sentence.
- **Pairing:** this is the **M2 "panel a = orientation"** figure; every downstream panel reuses its labels and colours.
- **Domain note:** **PK** — the sampling schedule must be legible enough to reproduce; **dissolution** — state medium, apparatus and sampling times on the schematic itself.

**S59. Analysis / model pipeline block schematic** [K] · *gallery I09*
- **Shows:** data → processing → model → output as labelled blocks with branch/merge arrows.
- **Best point:** makes an in-silico method *auditable at a glance* and fixes the vocabulary for the results.
- **Use when:** the pipeline has branches a paragraph would garble. **NOT when:** it is a linear three-step method.
- **Pairing:** schematic first, then the validation evidence.
- **Domain note:** **orientation only.** A pipeline diagram never substitutes for the convergence/parity evidence a modelling claim owes — loss curves (S19), GCI (S20), parity (S13/S61), %PE / relative-L2.

**S60. Offset trace array with a scale bar (no y-axis)** [K] · *gallery F11*
- **Shows:** many simultaneous traces stacked by a constant offset, with a scale bar instead of a y-axis and marked events.
- **Best point:** *relative timing and propagation* across many channels in one compact panel.
- **Use when:** traces share a time base and timing is the message. **NOT when:** absolute amplitudes must be compared across rows — use small multiples with a shared y-scale (M7).
- **Pairing:** the trace array above the quantification of the latency/amplitude it shows.
- **Domain note:** if the y-axis is dropped, the scale bar must carry **both** units; an unlabelled offset is an undeclared transformation.

**S61. Parity plot with bidirectional (x and y) error bars + flagged outliers** [D] · *gallery B16*
- **Shows:** predicted vs observed with uncertainty on *both* axes, the identity line, and the divergent cases named.
- **Best point:** honest calibration when the "truth" axis is itself measured with error.
- **Use when:** both axes carry measurement error. **NOT when:** x is exact — ordinary parity (S13) suffices.
- **Pairing:** parity (S13/S61) + Bland–Altman (S14) — correlation and bias are different questions.
- **Domain note:** **IVIVC** — required alongside **%PE** (<10% internal) and leave-one-formulation-out; a bare R² is a DS5 blocker. **CFD** pair with GCI (S20); **PINN** with relative-L2 and loss curves (S19). Never "agrees well" without a number.

**S62. Grouped regression with pooled + per-group fits (Simpson check)** [D] · *gallery B17*
- **Shows:** one pooled regression line across all points *plus* a line within each group, with every r reported.
- **Best point:** exposes **Simpson's paradox** — a pooled correlation that reverses or vanishes within groups.
- **Use when:** the data are grouped and you want to claim a correlation. **NOT when:** there is genuinely one population.
- **Pairing:** the grouped scatter beside the per-group coefficient table.
- **Domain note:** report the pooled r AND every within-group r with n per group. Reporting only the pooled fit for grouped data is the classic confounded-correlation error.

### GROUP 9b — idioms surfaced by the published-figure corpus (S63–S68) [R]

*A second pass over a reference corpus of 1,505 figures from 284 Nature-family PDFs (supplied by the
user, indexed and searched during this work, then deleted to reclaim 1.1 GB — the source PDFs remain in
`~/Agent_HM/Research topics/Articles`) surfaced six more idioms the 126 did not cover. The scripts that
first drew them were audited and found to contain 123 defects, so these were **rebuilt to house
standard**, not ported — each `requires` line below encodes the specific defect that audit caught.*

**S63. Size distribution with percentile readout (D10/D50/D90 + span)** [R] · *gallery A20*
- **Shows:** a particle-size distribution on a log-diameter axis with the decile points marked and a companion cumulative-undersize curve.
- **Best point:** *the width and tails of the distribution*, not just its centre — plus the span (D90−D10)/D50 that reviewers ask for.
- **Use when:** any sizing readout (DLS, laser diffraction, NTA). **NOT when:** a single scalar genuinely suffices — but for a formulation that is rare.
- **Pairing:** the PSD beside the cryo-TEM (S23) and the size/PDI bar (S9) — the physicochemical-QC cluster.
- **Domain note:** compute the percentiles from the cumulative curve; typed-in values drift from the plotted data. State the **weighting** (volume Q3 / number Q0) and the technique — an unweighted "size" is ambiguous, and a Z-average alone hides bimodality.

**S64. Quantified overlap of two distributions (overlap coefficient)** [R] · *gallery B18*
- **Shows:** two densities with their intersection shaded and the overlap **quantified** on the panel, plus the crossing threshold.
- **Best point:** *how separable two groups actually are* — the question "mean ± SD" and a p-value both dodge.
- **Use when:** arguing a marker discriminates (or fails to). **NOT when:** you need a decision rule — then add ROC/PR (S35).
- **Pairing:** overlap plot → ROC/PR for the operating point → confusion matrix at the chosen threshold.
- **Domain note:** label the shaded area as **exactly** the statistic computed (OVL = ∫min(f₁,f₂)dx, a probability in [0,1]); the audit found the original shading one quantity and naming another. Add a magnitude (AUC or Cohen's d). For **PK**, overlap is *not* bioequivalence — BE needs S25.

**S65. Annotated spectrum with assigned bands** [R] · *gallery G21*
- **Shows:** one spectroscopic trace with its diagnostic peaks labelled by assignment.
- **Best point:** *the assignment is the argument* — an unassigned spectrum proves nothing.
- **Use when:** FTIR/Raman/NMR evidence of encapsulation, interaction or a polymorph change. **NOT when:** comparing many spectra (use the waterfall S39 or an overlay).
- **Pairing:** spectrum + the orthogonal method that confirms the same conclusion (DSC, XRD).
- **Domain note:** **detect** peak positions from the array so labels cannot drift; render units as real superscripts (`cm$^{-1}$`, not a literal caret — a defect found in the audited original); keep the conventional axis direction (FTIR runs high→low wavenumber).

**S66. PCA score plot with per-group confidence ellipses** [R] · *gallery J08*
- **Shows:** PC1 vs PC2 with a 95% covariance ellipse per group and the % variance on each axis.
- **Best point:** *group dispersion and overlap* — bare scores show location but hide spread.
- **Use when:** many variables per sample and the question is separation. **NOT when:** you imply the ellipses test a difference.
- **Pairing:** scree (S43) for how much variance those axes hold → the ellipse score plot → a held-out classifier (S35/S36) if you make a class claim.
- **Domain note:** run a **real** decomposition and print variance from the singular values — the audited original asserted "38.2%/15.5%" for two-column data, where the two components must sum to 100%. State that the ellipse is a **covariance** ellipse (χ², 2 df), not a confidence interval of the mean.

**S67. Route-of-administration / biodistribution schematic** [R] · *gallery I11*
- **Shows:** dosing route → systemic compartment → organ fan-out, each organ carrying its share of dose.
- **Best point:** *where the dose actually goes*, as a single orienting picture that is also quantitative.
- **Use when:** opening an in-vivo study. **NOT when:** the organ data deserve a full comparison (then bar/heatmap it — this is orientation).
- **Pairing:** the M2 panel `a` for a biodistribution figure; the quantitative panels reuse its colours.
- **Domain note:** shares must be **%ID or %ID/g — say which** — and must account for the dose including the blood pool and the unrecovered fraction. A decorative organ cartoon with no numbers earns nothing.

**S68. Mechanism cartoon (binding → uptake pathway), numbered steps** [R] · *gallery I12*
- **Shows:** the proposed molecular/cellular route, drawn step by step with numbered stages.
- **Best point:** *fixes the vocabulary* for every panel that follows, so the reader knows what is being tested.
- **Use when:** the mechanism claim has ≥3 steps a sentence would garble. **NOT when:** the mechanism is the *result* — then show the evidence, not the cartoon.
- **Pairing:** cartoon first, then the blocking experiments (inhibitor, 4 °C, knockdown) that test each drawn step.
- **Domain note:** **every step the caption names must be visible as an artist on the canvas, and elements described as touching must actually touch** — the audited original claimed a binding event with a measured 9.2 px gap and drew no pathway at all. Verify the geometry numerically. A mechanism cartoon is a hypothesis diagram; it never substitutes for the experiment.

---

## GROUP 9c — JOURNAL-CASE ADDITIONS (S69–S74) [R]

*Added 2026-07-19 from a public collection of 20 ggplot2 journal-figure recipes
(github.com/GeneticistHere/ggplot2-20-journal-cases). 14 of the 20 were already covered by the gallery
(Manhattan=G11, paired box=A18, raincloud=A13, split violin=A12, treemap=D02, mosaic/sunburst=D07/D03,
multi-level Sankey≈E06, module network≈E08, error dot-plots≈A14/C14, multi-group volcano≈G10+small
multiples, multi-group correlation heatmap≈B07/J06, importance-streams & Sankey-bubble = composites of
existing pieces). These six were genuinely absent. Each is rebuilt from synthetic data in matplotlib
house style (IDs in brackets) — the ggplot theming is NOT copied.*

**S69. Swimmer plot (per-subject response timeline)** [R] · *gallery G22*
- **Shows:** one horizontal bar per subject, length = time on study, colour = best response category,
  with on/off-study event glyphs and duration ordering.
- **Best point:** *individual durability* — who responded, how deeply, and for how long — which an
  aggregate survival curve hides.
- **Use when:** per-subject follow-up with events (oncology/immunotherapy; also a per-formulation
  stability timeline). **NOT when:** you only need the aggregate — use Kaplan–Meier (S8/G02).
- **Pairing:** swimmer for the individual stories → Kaplan–Meier for the population summary.
- **Domain note:** state what the bar length measures; give BOTH a colour legend (response) and a glyph
  legend (events) — an unlabelled marker is unreadable.

**S70. Grouped bars with compact-letter-display (CLD) significance** [R] · *gallery C17*
- **Shows:** grouped means ± s.d. with post-hoc **letters** (a/ab/bc/c) above each bar — bars sharing a
  letter are not significantly different — plus the replicate points.
- **Best point:** reports the *entire* pairwise-comparison outcome compactly, where a few brackets show
  only the pairs you chose.
- **Use when:** one factor with several levels after a significant ANOVA/Kruskal. **NOT when:** the
  design is paired (S46) or the endpoint is a dissolution/PK profile (f2 / geometric-mean rules apply).
- **Pairing:** the lettered bars beside the ANOVA/post-hoc table.
- **Domain note:** the letters MUST come from a real post-hoc (Tukey HSD, Dunn); eyeballed letters are a
  DS2 fabrication. Show the points (AP1); letter geometric means for PK (S30), not linear mean±SD.

**S71. Binned-colour heatmap with row-metadata table (antibiogram)** [R] · *gallery I13*
- **Shows:** a matrix whose continuous values are mapped onto **discrete colour bins** (a stepped
  legend, not a continuous ramp), with the value printed in each cell and an aligned categorical
  row-metadata table on the left.
- **Best point:** turns a continuous ratio into *decision categories* (susceptible/intermediate/
  resistant; within/out of spec) so the reader classifies at a glance.
- **Use when:** the thresholds carry the meaning (MIC fold-change, resistance ratio, ratio-to-RLD).
  **NOT when:** the smooth gradient itself is the message — use a continuous heatmap (I03/J06).
- **Pairing:** the binned matrix + the row table that explains each row's genotype/condition.
- **Domain note:** centre the bins on the meaningful value (1 for a ratio); diverging is legitimate only
  because the ratio is signed around it (AP3).

**S72. Circos / circular ideogram with ribbon links** [R] · *gallery E09*
- **Shows:** a positional axis wrapped into a ring (chromosomes as arc segments) with interior **ribbon
  links** connecting paired loci, coloured by a categorical driver.
- **Best point:** many pairwise relationships around ONE cyclic/positional axis, seen together.
- **Use when:** the axis is genuinely cyclic or positional (genomic loci, migration between regions).
  **NOT when:** the axis is not cyclic — a bipartite graph (E04) or alluvial (S55) is more readable.
- **Pairing:** the Circos overview → a table/bar of the specific links that matter.
- **Domain note:** links must dip toward the centre (Bézier), never straight chords; colour by driver
  with a legend; keep rim labels from colliding (radial text, staggered leaders when dense).

**S73. Mantel composite (correlation heatmap + linked test edges)** [R] · *gallery B19*
- **Shows:** a lower-triangle correlation heatmap of predictor variables PLUS curved links from groups
  of predictors to one or more community/response matrices, the links encoding a Mantel statistic.
- **Best point:** relates a *predictor correlation structure* to *community responses* in one panel —
  the standard microbiome/ecology figure.
- **Use when:** you have environment-variable correlations AND distance-based associations to communities.
  **NOT when:** it is a single pairwise question (use parity S13 / Bland–Altman S14).
- **Pairing:** the composite + the Mantel/PERMANOVA table.
- **Domain note:** encode statistic→width, p→colour, sign→solid/dashed with THREE legends. A real Mantel
  needs distance matrices and a permutation p; never relabel an ordinary Pearson correlation as Mantel.

**S74. Polar (radial) heatmap — concentric rings × angular sectors** [R] · *gallery H12*
- **Shows:** a heatmap wrapped to polar coordinates — inner rings = a few response metrics, angular
  sectors = many predictors — each wedge filled by value with the number printed.
- **Best point:** a compact overview when the sectors are a natural cycle or a long categorical list.
- **Use when:** compactness and pattern matter more than precise magnitude reading. **NOT when:** precise
  magnitude comparison is needed — a rectangular heatmap (I03) is more accurate; angle/area distort.
- **Pairing:** the radial overview → a rectangular heatmap for the cells that carry the claim.
- **Domain note:** distinct from a polar *rose* (H09, which encodes magnitude by radius). Keep numbers
  upright; diverging scale only for genuinely signed values (partial r), sequential otherwise (AP3).

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
| The design is PAIRED (crossover, pre/post, matched) | S46 connecting lines + a PAIRED test (never two independent boxes) |
| Read estimates against a decision threshold | S47 dot plot on shaded reference zones |
| A heavy tail crushes the low groups | S48 broken-axis DOT plot (never a broken bar — AP9); try log first |
| Two statistics per cell (prevalence AND intensity) | S49 dual-encoded dot-plot matrix (size + colour, two keys) |
| Is the block structure biology or batch? | S50 heatmap + categorical annotation tracks |
| Rank enriched sets from a cut-off list | S51 enrichment dot plot (ratio × count × FDR) |
| Is a set concentrated at one end of a ranking? | S52 GSEA running-enrichment (permutation NES + FDR) |
| Explain what a cluster IS | S53 embedding + feature-plot couplet (hypothesis, not proof) |
| Justify a reported cytometry percentage | S54 sequential gating panels, % of parent at each step |
| A cohort through ≥3 sequential decisions | S55 alluvial ribbons (mass must balance) |
| Values across a large fixed hierarchy | S56 radial dendrogram, value-scaled tips |
| Modules and hubs in a big graph | S57 communities + hub labels (name layout, seed, algorithm — AP8) |
| Orient the reader before any result panel | S58 study-design / dosing timeline (the M2 panel a) |
| Make an in-silico method auditable | S59 pipeline schematic — orientation only, never instead of S13/S19/S20 |
| Relative timing across many channels | S60 offset traces + scale bar carrying both units |
| Both axes carry measurement error | S61 parity with x AND y error bars + named outliers |
| A correlation on grouped data | S62 pooled + per-group fits (Simpson check) — report every r |
| Particle size — width and tails, not just a mean | S63 PSD + D10/D50/D90 + span (state the weighting) |
| How separable are two groups, really? | S64 overlap coefficient (shade ∫min(f₁,f₂)) + AUC or Cohen's d |
| Prove an interaction / encapsulation spectroscopically | S65 annotated spectrum — the band assignment IS the argument |
| Group separation AND spread in high-dim data | S66 PCA + 95% covariance ellipses (+ real % variance per axis) |
| Where does the dose actually go? | S67 route/biodistribution schematic carrying %ID |
| The proposed mechanism, before the evidence panels | S68 numbered mechanism cartoon (draw every step you name) |
| Per-subject durability with events (who responded, how long) | S69 swimmer plot (sort by duration; legend colours AND glyphs) |
| Report every pairwise ANOVA outcome compactly | S70 grouped bars + compact-letter-display (real post-hoc, not eyeballed) |
| Classify a continuous ratio into decision bands | S71 binned-colour heatmap + stepped legend (+ row-metadata table) |
| Many pairwise links around one cyclic/positional axis | S72 circos (Bézier links dip to centre; colour by driver) |
| Relate a predictor correlation structure to communities | S73 Mantel composite (width=r, colour=p, solid/dashed=sign — 3 legends) |
| A compact overview over a cyclic or long categorical axis | S74 polar heatmap (rings × sectors; rectangular I03 for precise magnitude) |

---

*Reference document — Graph-Style Library dimension. Styles tagged [E] are grounded in the 5 exemplar mining files in `_exemplar_mining/`; styles tagged [D] are the domain-required families (`domain-conventions.md`) the wet-lab corpus lacks; styles tagged [K] (GROUP 8, S38–S45) are the in-silico / signal / dimensionality families distilled from Nathan Kutz's `ScientificComputing` repo (`Data-Driven Modeling & Scientific Computation`, 2nd ed.; https://github.com/nathankutz/ScientificComputing) — technique/idiom only, no code copied. Selecting a style is a DS1 craft decision; the domain-correctness of that style is a DS5 gate — read both modules together. GROUP-8 styles carry a hard scope rule: they are for modeling / signal / data-analysis deliverables and must never be laundered onto wet-lab dissolution / PK / BE / biological-endpoint outputs.*

*Access model: don't browse this file top-to-bottom — use the **DECISION LAYER** at the top (`scripts/choose_graph.py`, backed by `scripts/graph_catalog.json`) to get a ranked answer + the enforced anti-patterns + palette/engine/stat in one call; the **ANTI-PATTERN REGISTRY** (AP1–AP16, from `FriendsDontLetFriends`, MIT) is the reject-rule set; journal style-engines (SciencePlots, ultraplot — MIT) and colorblind-gated journal palettes (ggsci/ggprism hex; GPL-3 code NOT used) live in `publication-ready-figures.md` R4/R12. The style entries here are the detail the chooser points into.*
