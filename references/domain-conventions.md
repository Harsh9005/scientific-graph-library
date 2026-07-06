<!-- data-strength-elevator reference module — DOMAIN CORRECTNESS LAYER.
This module is the antidote to the exemplar corpus's blind spot. The 5 distilled
papers are a wet-lab LNP/mRNA in-vivo monoculture: NONE contains a dissolution
profile, f2, a release-kinetics fit, a Bland-Altman plot, an NCA/PBPK table, a CFD
mesh-convergence study, or a PINN loss curve. The other four reference modules
therefore transmit elite *rhetoric and rigor-signalling* correctly but would
structurally MIS-TEACH this researcher's core figure/stat conventions. This module
supplies what they cannot, and forbids laundering wet-lab defaults onto in-vitro /
in-silico / BE work. Read it WITH the other four modules — it overrides them wherever
a convention conflict exists for dissolution / release / IVIVC / PK / PBPK / CFD / PINN. -->

# Domain Conventions & Anti-Mis-Transfer Layer
### For IVIVC · dissolution/release · nanoparticle formulation · PK/NCA · PBPK · CFD · PINN

The four exemplar-derived modules (figures, statistics, narrative, style/fit) carry the
*transferable* strengths of Nature-family papers. This module carries the **domain-specific
conventions** those papers never show, plus a hard **do-not-blindly-copy** list. When a
convention here conflicts with a convention in another module, **this module wins for
in-vitro / in-silico / bioequivalence outputs.**

---

## (0) ANTI-MIS-TRANSFER — do NOT launder these wet-lab defaults

The exemplars are internally excellent but their conventions are **wrong defaults** for
several outputs this lab produces. Never copy them mechanically:

| Wet-lab exemplar habit | Wrong for | Correct domain convention |
|---|---|---|
| **mean ± SD on a linear axis** | PK exposure metrics (AUC, Cmax), bioequivalence | **Geometric mean + 90% CI**, log-transformed AUC/Cmax; report **%CV**; BE window **80–125%** |
| **n = 3 (biological triplicate)** | dissolution / release | **n ≥ 6** (often 12 units) per USP; report **%RSD/%CV** with acceptance limits (RSD ≤20% early, ≤10% after 85% released) |
| **one-way ANOVA + Dunnett for "is it different"** | profile comparison (dissolution, release) | **f2 similarity (≥50) / f1 difference (≤15)**, or model-independent **bootstrap-f2 CI**, or **Mahalanobis MSD** — a single ANOVA on endpoint % is not a profile comparison |
| **Kaplan–Meier + log-rank centrepiece** | release/PK/CFD kinetics | KM is for time-to-event only; use **profile overlays + kinetic model fits + AUC** |
| **exact p-value as the headline rigor signal** | model agreement (IVIVC, PBPK, CFD, PINN) | agreement is shown by **%PE, 2-fold error bounds, R²+CI, Bland–Altman bias±LoA, NRMSE / relative-L2**, not a p-value; a *non-significant* difference test is at best a weak equivalence argument |
| **R² alone "demonstrates" IVIVC** | IVIVC validation | R² is necessary, not sufficient: add **%PE for Cmax and AUC (<10% internal / <20% external, FDA)** and **out-of-sample (leave-one-formulation-out) validation** |

> **Rule of the layer:** the *rhetoric* transfers (benchmark by name, quantify magnitude,
> convergent evidence, honest limitations, complete reproducibility). The *statistics and
> chart primitives* must be the domain's, not the corpus's.

---

## (A) DOMAIN FIGURE CONVENTIONS (the elite standard the corpus omits)

**Dissolution / release**
- % cumulative release vs time **overlay** of all formulations + the **reference-listed drug (RLD)/marketed product** on the same axis (the corpus's "benchmark on shared axis" lesson, domain-translated).
- Error bars = **SD of n ≥ 6–12**; disclose sink conditions, apparatus (USP I/II/IV), rpm, medium, volume, temperature; show **multi-pH panels** (pH 1.2 / 4.5 / 6.8) side by side.
- **Release-kinetics fits** overlaid (zero-order, first-order, Higuchi, Korsmeyer–Peppas, Weibull) with **R²(adj), AICc, and the KP release exponent *n*** annotated; include a **residual plot**.
- **f2 annotated on the comparison figure** (value + threshold), with the ≤1-point-after-85% rule respected.

**IVIVC**
- Fraction absorbed in vivo vs fraction dissolved in vitro with the **line of unity**, regression, **R² + 95% CI**, and the IVIVC **Level (A/B/C)** stated.
- **Bland–Altman** agreement plot (bias ± 1.96 SD limits) for predicted vs observed Cmax/AUC — the single most important agreement figure in this field and absent from the corpus.
- **Observed-vs-predicted** goodness-of-fit with **line of identity + 2-fold bounds**.

**PK / NCA**
- Concentration–time on **semi-log AND linear axes side by side**; report Cmax, Tmax, AUC0–t, AUC0–∞, t½, CL/F, Vz/F.
- **Geometric-mean** profiles; individual-subject spaghetti overlay where n is small.
- Forest plot of **parameter fold-errors** vs observed for model arms.

**PBPK**
- Observed-vs-predicted with **2-fold (and 1.25-fold) error bounds**; **Visual Predictive Check (VPC)** with 5th/50th/95th prediction-interval bands; **parameter sensitivity** tornado/heatmap.

**CFD**
- **Mesh-convergence / GCI plot** (solution metric vs cell count) — mandatory; **y+ contour**; velocity / **wall-shear-stress field** with a *quantitative* colorbar; streamlines; and a **validation overlay** against analytical or experimental data (never a bare contour asserting "agrees well").

**PINN / ML surrogate**
- **Training vs validation loss** (log-y), with the **PDE-residual term broken out**; **parity plot** (predicted vs ground-truth field); residual-of-PDE map; **loss-term ablation** panel; **uncertainty band**.

**Nanoparticle characterization (directly portable from the corpus — adopt as-is)**
- DLS **size + PDI (target <0.2)** twin-axis; **EE% + zeta** twin-axis; **cryo-TEM/TEM with scale bar**; apparent **pKa (TNS)**; **full size-distribution histogram** and a **stability/timepoint** panel (the corpus under-shows the last two — add them).

**The in-silico analogue of "never let an image carry a claim without a number":**
**every model curve must sit next to its residual / goodness-of-fit metric** (R²adj, AICc, %PE, NRMSE, GCI). A simulation with no quantified agreement figure is the modelling equivalent of an orphan micrograph.

---

## (B) DOMAIN STATISTICS (what "reviewer-proof" means here)

- **Dissolution profile comparison:** f2 (≥50) / f1 (≤15); when variability is high (CV >20% early / >10% late) use **bootstrapped f2 with 90% CI** or **model-independent multivariate (Mahalanobis) distance**. State n (≥6–12), %RSD, and apparatus.
- **Release kinetics:** fit competing models; select by **AICc / adjusted R² / runs test**, not raw R²; use **weighted least squares** when variance grows with response; report the **KP exponent *n*** and interpret transport mechanism.
- **PK / NCA:** **geometric mean + 90% CI**, log-transform AUC/Cmax, **%CV** as dispersion; bioequivalence judged on **80–125%** of the 90% CI of the GMR — *not* SD-on-linear-scale, *not* a t-test on raw means.
- **IVIVC:** R² **plus** %PE for Cmax and AUC against the **FDA threshold** (mean %PE <10% internal, <20% external), with **leave-one-formulation-out** external validation; report predictive check, not fit-set self-agreement.
- **PBPK:** predicted/observed within **2-fold** (parameters) reported per parameter; VPC coverage; sensitivity analysis on key parameters.
- **CFD numerical rigor:** **Grid-Convergence Index (GCI)** via Richardson extrapolation; report discretization + iterative-convergence error and the **mesh-independence** criterion; this is the domain's "error bar."
- **PINN/ML:** **RMSE / MAE / relative-L2**, R²; **k-fold CV**; disclose **train/val/test split, random seed, epochs, optimizer, learning rate, architecture** (reproducibility items).

**KEEP and PORT from the corpus (cheap, high-trust, domain-agnostic):**
report **effect size / magnitude alongside every inferential statistic** (here: %PE, f2, fold-change in AUC, NRMSE — not just p); **name the test and match it to the design**; **define n as biological vs technical in every caption**; **state the error-bar meaning every time**; **test assumptions (normality/variance)**; **name multiple-comparison correction**; **state exclusions**; **list software + versions**; **provide source data**.

**Modeling / data-science statistics layer (in-silico deliverables):** for CFD / PINN / IVIVC-modeling / PBPK / data-analysis work, the model-selection, cross-validation, regularization, dimensionality-reduction (SVD/PCA scree), and analysis-knob-reporting discipline is consolidated in `statistics-rigor.md` §F, with the matching field / spectral / reduced-order graph styles in `graph-style-library.md` GROUP 8 (S38–S45). **These are hard-scoped to modeling outputs — never launder cross-validation, LASSO, or an SVD truncation onto a dissolution / PK / BE / biological endpoint (a DS5 mis-transfer in the opposite direction).**

---

## (C) REPORTING-STANDARD SCAFFOLDS (the domain's "Reporting Summary")

Cheap credibility for a small lab; each is the field-specific analogue of Nature's Reporting Summary. Cite conformance explicitly:

- **Dissolution:** USP <711>/<724>, **ICH Q6A / Q1A**; method fully disclosed (apparatus, medium, sink, n, rpm, sampling).
- **IVIVC:** **FDA Guidance for Industry — Extended Release Oral Dosage Forms (IVIVC)**; EMA equivalents.
- **Bioequivalence / PK:** FDA/EMA BE guidance; NCA method + software version (Phoenix WinNonlin / PKNCA).
- **PBPK:** regulatory PBPK best-practice reporting (e.g., Shebley et al. 2018; FDA/EMA PBPK guidances) — model assumptions, verification, sensitivity.
- **CFD:** **ASME V&V 20** verification-and-validation; report GCI and validation metric.
- **ML/PINN:** a model card / reproducibility checklist (data, seed, hyperparameters, code/weight availability).

---

## (D) TARGET-JOURNAL FIT for this lab's realistic venues

The exemplars are Nat Commun / Nat Materials / Nat Biotech — resource-heavy venues that reward an in-vivo→human-tissue capstone. **Most of this lab's work targets journals that reward mechanistic in-vitro + in-silico rigor and do NOT require an in-vivo/human capstone.** Calibrate the "translational ladder" and "human-tissue rung" checks accordingly for these targets:

| Journal | What it rewards | Data-strength emphasis |
|---|---|---|
| **J Control Release** | mechanism of release/delivery, quantitative rigor | kinetics fits, IVIVC, orthogonal release methods |
| **Int J Pharmaceutics / IJP: X** | formulation + biopharmaceutics breadth | DoE, dissolution vs RLD, stability |
| **Mol Pharmaceutics** | mechanistic + modelling | PBPK/CFD/PINN with V&V, structure–property |
| **Eur J Pharm Biopharm** | biopharmaceutics, IVIVC | Level A IVIVC, %PE, biorelevant media |
| **Pharmaceutics / AAPS PharmSciTech / Drug Delivery** | applied formulation | complete physicochemical QC, reproducibility |

For a genuine **Nature-family** bid, the exemplar bar applies in full: a human-tissue/ex-vivo rung, a second-modality generalizability axis, and a dedicated safety/objection package become necessary, not optional.

---

## (E) "CHEAP ELITE WINS" — domain-translated adoption list

Every one of these is adoptable by a small in-vitro/in-silico lab and each maps to an exemplar habit:

1. **Benchmark against the RLD / reference product / established model** on a shared axis in a *primary* figure (not vs blank, not in SI).
2. **Report magnitude + inferential stat together** — %PE, f2, fold-change in AUC, NRMSE **and** the test — never a bare "significant/good."
3. **DoE / Taguchi / factorial** screen for formulation or hyperparameter selection instead of "we varied it until it worked."
4. **Orthogonal validation:** pair each in-silico prediction with (a) an independent experiment **and** (b) an independent computational/analytical solution (e.g. PINN vs FVM vs UV-imaging).
5. **Reconcile model with data in one explicit sentence** (the corpus's docking→"consistent with experiment" move, copied to CFD/PINN/PBPK) with a quantified gap.
6. **Mechanism by quantified loss-of-function vs a matched null perturbation** (ablate the convective term; shuffle a boundary that should not matter → n.s.).
7. **Full physicochemical / model-validation QC every time** (size+PDI+zeta+EE+pKa+cryo-TEM; or mesh-independence + parity + residuals).
8. **Climb exactly one rung** above comfort where cheap: one biorelevant-medium, one ex-vivo, or one small-animal PK arm — never overclaim beyond it.
9. **Complete reproducibility disclosure** (methods params, software+versions, seed, source data) — the domain's Reporting Summary.

---

## (F) SCORING CHECKLIST — Domain Correctness (Dimension 5)

Score each **Elite (2) / Adequate (1) / Weak (0)**. Target ≥ 16/20. Any 0 on D1–D5 is a blocker.

| # | Check | Elite (2) | Adequate (1) | Weak (0) |
|---|---|---|---|---|
| **D1** | Right chart primitive for the data type | dissolution overlay+f2; PK semilog+linear; obs-vs-pred+identity/2-fold; CFD GCI; PINN loss+parity | mostly right, one mismatch | wet-lab primitive forced (bar of endpoint %, KM for release) |
| **D2** | Profile comparison done correctly | f2/f1 or bootstrap-f2 CI / Mahalanobis, n≥6, %RSD | f2 stated, n or RSD missing | ANOVA/t-test on endpoint % passed off as profile comparison |
| **D3** | PK/BE reported in domain units | geometric mean, 90% CI, log-scale, %CV, 80–125% | some domain units, some SD/linear | mean±SD on linear axis, t-test on raw AUC |
| **D4** | IVIVC validated, not just fitted | R²+CI, %PE<threshold, out-of-sample, Bland–Altman | R² + one validation element | bare R² "demonstrates Level A" |
| **D5** | Numerical/ML rigor stated | GCI/mesh-independence or RMSE/relative-L2 + seed/split | partial | "agrees well" / "accurate" with no metric |
| **D6** | Reporting-standard conformance cited | USP/ICH/FDA-IVIVC/V&V20/model-card named | some methods disclosed | method under-specified, no guideline |
| **D7** | Benchmark = RLD/established model on shared axis | yes, primary figure | in SI or secondary | vs blank/untreated only |
| **D8** | Model reconciled with data explicitly + quantified gap | one clear sentence + % gap | agreement implied | model orbits unattached |
| **D9** | Journal-appropriate translational calibration | ladder scaled to the *target* journal (no over/under-reach) | slightly mis-scaled | Nature-capstone expected of an IJP paper, or in-vitro-only pitched at Nature |
| **D10** | No laundered wet-lab default | every convention domain-correct | one slip | multiple §0 violations |

---

## (G) RED FLAGS (domain-specific)

- Dissolution/release compared by ANOVA on a single timepoint instead of **f2**; n = 3 instead of ≥6; SEM instead of SD; sink/apparatus undisclosed.
- IVIVC claimed from **R² alone** with no %PE, no out-of-sample validation, no Bland–Altman.
- PK/BE reported as **mean ± SD on a linear axis** with a t-test on raw AUC/Cmax (should be geometric mean, log, 90% CI, 80–125%).
- Release "modelled" with **one equation and raw R²** — no competing models, no AICc, no residual plot, no KP exponent.
- CFD result shown as a **bare contour** with "agrees well" — no GCI, no y+, no validation overlay.
- PINN/surrogate reported as "accurate" with **no RMSE/relative-L2, no train/val/test split, no seed**.
- A simulation figure with **no adjacent residual/goodness-of-fit metric** (in-silico orphan image).
- Translational **mis-calibration**: an in-vitro/in-silico study over-pitched at a Nature-family venue with no human rung, OR a solid mechanistic IJP-level study buried under an unnecessary in-vivo demand.
