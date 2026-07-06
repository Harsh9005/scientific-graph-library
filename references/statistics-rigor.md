<!-- data-strength-elevator reference module. Distilled from 5 elite exemplars:
Nat Commun 2024 15:739; Nat Commun 2025 16:2198; Nat Mater 2025 24:1653;
Nat Biotechnol 2025 43:1783; Nat Biotechnol 2025 (Brief Communication).
Benchmarks in section (B) are as-extracted from those papers. READ ALONGSIDE
references/domain-conventions.md — do NOT launder wet-lab defaults onto
dissolution/PK/IVIVC/CFD/PINN work (see anti-mis-transfer rules there). -->

# Statistics & Data-Analysis Rigor: The Reviewer-Proof Standard
### A benchmarked reference distilled from 5 elite papers (Nat. Commun. ×2, Nat. Mater., Nat. Biotechnol. ×2)

This module governs ONE dimension of manuscript strength: the reporting of statistics and data analysis. It converts what these papers *actually did* into a standard a small lab can hit without a biostatistics core. Every principle below is grounded in the exemplars; the numbers in §B are extracted from them.

---

## (A) PRINCIPLES

**P1 — Pair every image/qualitative readout with its own n-backed quantification in the same figure.**
None of these papers let a micrograph, blot, or dot-plot carry a claim alone. The Nat. Commun. wound-healing paper couples *every* immunofluorescence stain with a bar+scatter quantification (CD31→vessels/area, αSMA→cells/area, IL-6, IL-10). The Nat. Biotech peptibody paper reads knockdown at *two* molecular levels (Sod1 mRNA by qPCR → SOD1 protein by ELISA). Rule: if you show a picture, show the number beside it; if you show a transcript effect, show the protein/functional effect.

**P2 — Prove one claim with two orthogonal methods before advancing.**
This is the single most repeated pattern. "mRNA crosses the BBB" is shown four independent ways (luciferase = translation, Alexa-647-RNA biodistribution = physical delivery, GFP flow = single-cell %, Cre/tdTomato = permanent genetic readout). "Delivery works" = in-vitro luminescence AND in-vivo IVIS. "It kills bacteria" = binding (flow) AND uptake (confocal) AND intracellular killing. Efficacy is always kinetics AND survival. Convergent evidence, not a single technique, is the rigor signature.

**P3 — Benchmark against the field's approved/best-prior-art comparator on the SAME axes — never against a strawman.**
Every screen ends in the FDA-approved lipids (MC3, ALC-0315, SM-102) or the clinical standard (ciprofloxacin, cholesterol-oligo, electroporation) as fixed reference bars, and effects are stated as fold-change over that named comparator ("7.3-fold over Chol-oligo", "4-log below cipro"). "Better than nothing (PBS/blank)" is present but is never the headline claim.

**P4 — Match the named test to the data structure, and say the name.**
The tests are not decorative — they fit the design: one-way ANOVA + Dunnett's (many groups vs one control), two-tailed Student's t-test (two groups), **log-rank / Mantel-Cox for all time-to-event / survival** (never ANOVA on a survival curve), two-way ANOVA + Sidak/Fisher-LSD for two-factor time×treatment designs. Correct survival-test selection appears in *all four* papers that have a survival/closure endpoint. Post-hoc correction (Dunnett's or Tukey's) is the built-in multiple-comparison handling.

**P5 — Report EXACT p-values on the panel, not just asterisks; and label n.s. honestly.**
Every paper prints P=0.0002, P=0.012, P=0.0069 etc. directly on brackets, alongside a defined threshold ladder. Non-significant comparisons are shown, not hidden — the wound paper prints "n.s. P=0.0510", the pneumonia paper prints n.s. where the inert LNP fails to differ from PBS. Honest n.s. reporting reads as competence, not weakness.

**P6 — State error bars as SD uniformly — never silently switch to SEM.**
All five papers use mean ± s.d. in *every* legend and never mix in SEM. SEM shrinks error bars artificially; the elite convention is SD, stated explicitly each time.

**P7 — Report effect size as an interpretable magnitude (fold-change, %-reduction, log-reduction, AUC ratio) in the prose, adjacent to the p-value.**
P<0.0001 says it's real; the fold-change says whether it *matters*. The texts are saturated with "220.5-fold", "4-log reduction", "69.0±2.9% vs 5.8±1.8%", "AUC 5.4-fold". Magnitude currency here is fold-change/percent, not Cohen's d (Reporting Summaries mark d / Pearson r "n/a").

**P8 — Define n unambiguously per panel and distinguish biological from technical replicates.**
Legends state "n=3 biologically independent samples", and where it could be ambiguous they spell it out: "n=9 (9 biological samples from three mice)", "n=4 (4 biological samples from two human donors)". In-vivo n scales up appropriately (n=7–20 animals) versus in-vitro (n=3). Reviewers can never ask "what is a replicate here?"

**P9 — Show the full screen/optimization funnel, loser-included; use a formal DoE for optimization.**
Down-selection is shown as data: all 50–72 candidates plotted against the reference (not just the winner), so the lead is visibly *not* cherry-picked. Formulation optimization uses a stated orthogonal-array / Taguchi / L16(4⁴) DoE table, signalling systematic rather than one-factor-at-a-time tuning.

**P10 — Build controls as a layered ladder: vehicle → best prior art → mechanistic (loss-of-function) → positive.**
Beyond PBS/vehicle, they include the clinical benchmark, a scrambled/inactive-cargo control that isolates the *engineering* benefit (control-epitope, FLuc/LL37 mRNA, control mRNA), mechanistic knock-outs (two independent γ-secretase inhibitors; endocytosis-inhibitor panels; FcRγ⁻/⁻ genetic control), and — sophisticated — a *positive* control that reproduces the mechanism by an independent route (C16 PKR-inhibitor mirroring the genetic E3 evasion).

**P11 — Establish mechanism by quantified loss-of-function with a matched null perturbation.**
Mechanism is not asserted; it is shown by ablating the proposed pathway and quantifying collapse against a perturbation that should do nothing: MβCD (caveolae) drops uptake 43–97% while clathrin/macropinocytosis inhibitors give n.s.; free ligand competitively inhibits 63.8%. This is the directly transferable template for CFD/PINN/PBPK: knock out one modeled pathway/parameter, show the readout collapses vs a null perturbation that does not.

**P12 — Disclose reproducibility exhaustively and reconcile any model with data in one explicit sentence.**
All papers carry a "Statistics & reproducibility" block: normality/equal-variance assumptions *formally tested*; sample size not power-predetermined (stated honestly); no data/animals excluded (stated); randomization + partial blinding described *with a reason* where blinding was impossible; complete software+version list (GraphPad Prism 9, ImageJ 1.53, FlowJo 10.4, AutoDock Vina 1.2.0); source data + Reporting Summary + data/PDB availability provided. Where computation is used, it is closed with an explicit reconciliation ("these computational data are consistent with the experimental results").

---

## (B) BENCHMARKS

Concrete conventions extracted across the 5 exemplars. Compare your manuscript row-by-row.

| Dimension | Elite standard (what the 5 papers do) | Observed range/values |
|---|---|---|
| Error-bar convention | **mean ± s.d.**, stated in *every* legend; SEM never used | 5/5 papers SD-only |
| p-value reporting | **Exact p on-panel** (e.g. P=0.0002) + defined asterisk ladder | 5/5 exact-p; ladder n.s./*/**/***/**** = >0.05 / <0.05 / <0.01 / <0.001 / <0.0001 |
| n.s. handling | Non-significant comparisons shown & labelled "n.s." | 5/5 (e.g. n.s. P=0.0510) |
| Multi-group test | One-way ANOVA + **Dunnett's** (vs common control) or **Tukey's** (all-pairs) | 5/5 |
| Two-group test | Two-tailed Student's t-test | 5/5 |
| Survival / time-to-event | **Log-rank (Mantel-Cox)** — never ANOVA | 4/4 papers with a survival endpoint |
| Two-factor design | Two-way ANOVA + Sidak or Fisher-LSD post-hoc | used where time×treatment (e.g. CPP place-preference, longitudinal tumor) |
| Multiple-comparison correction | Post-hoc (Dunnett/Tukey) disclosed in Reporting Summary | 5/5 |
| n type | Explicit "biologically independent samples"; bio vs technical distinguished | 5/5 |
| In-vitro n | n = 3 (typical floor) | 3 across all |
| In-vivo n | n = 7–20 animals / wounds | wound n=10; CPP n=19–20; GBM survival n=9–10; pneumonia n=7–8 |
| Human/ex-vivo n | n = 3–4 tissue slices, 2 donors | stated explicitly |
| Individual data points on bars | Every replicate plotted as a dot over/around the bar | 5/5 ("all 3 mice visible as red dots") |
| Effect-size currency | Fold-change / %-reduction / log-reduction / AUC ratio in prose | 5/5; e.g. 4.7–220.5-fold, 4-log CFU, AUC 5.4-fold |
| Orthogonal validation per core claim | ≥2 independent methods (often 3–4) | delivery 2×; BBB-crossing 4×; knockdown 2× (mRNA+protein) |
| Screen transparency | Full library plotted vs approved comparator (loser-included) | 50–72 candidates shown |
| DoE optimization | Formal orthogonal array / Taguchi / L16(4⁴) table | ≥3/5 |
| Physicochemical QC per lead formulation | size, PDI, ζ, EE% (RiboGreen), pKa, cryo-TEM | PDI <0.15; EE ≈ 80–90%; near-complete organ mass-balance reported |
| Assumption testing | Normality + equal-variance formally tested & stated | 5/5 |
| Power calculation | Honestly stated as NOT done; n≥3 justified from prior work | 5/5 |
| Data exclusions | "No data/animals excluded" stated | 5/5 |
| Reproducibility scaffold | Source data + Reporting Summary + software versions + data/PDB IDs | 5/5 |
| Schematic-to-data panel ratio | Low; ~1 orienting schematic per figure | ≈1:7 to 1:8 |

---

## (C) SCORING CHECKLIST

Run against any draft. Score each 2 (elite) / 1 (adequate) / 0 (weak). Target ≥ 26/30; any 0 on C1–C6 is a blocker.

| # | Check | Elite (2) | Adequate (1) | Weak (0) |
|---|---|---|---|---|
| **C1** | Error bars defined | "mean ± s.d." in every legend | SD stated once globally | Undefined, or SEM used to shrink bars |
| **C2** | p-values | Exact p on every panel + ladder | Asterisks + threshold key only | Bare "significant"/no p |
| **C3** | Test↔design match | Named test fits each design incl. **log-rank for survival** | Named but generic (ANOVA everywhere) | Unnamed or wrong (t-test on 4 groups, ANOVA on survival) |
| **C4** | Multiple-comparison correction | Dunnett's/Tukey's named & applied | Mentioned, not clearly applied | Many uncorrected pairwise t-tests |
| **C5** | n defined & bio vs technical | Per-panel "n biologically independent…", ambiguity spelled out | n given, type unclear | n missing or n=technical replicates masquerading as biological |
| **C6** | Effect size | Fold-change/%/log/AUC beside every p | Some magnitudes given | "significantly higher" with no number |
| **C7** | Orthogonal validation | Each core claim ≥2 independent methods | One claim double-validated | Every claim rests on one technique |
| **C8** | Benchmark comparator | Approved/best-prior-art on same axes | Comparator in supplement only | Only vs blank/PBS |
| **C9** | Controls ladder | Vehicle + prior-art + mechanistic + positive | Vehicle + one comparator | Vehicle only |
| **C10** | Individual data points | Dots on every bar | Dots on some | Bars only, spread hidden |
| **C11** | n.s. honesty | n.s. shown & labelled | Present but easy to miss | Non-significant results omitted |
| **C12** | Screen/DoE transparency | Full funnel (loser-included) + DoE table | Winner + a few comparators | Only the winner shown |
| **C13** | Assumptions & power | Normality/variance tested; power/exclusions stated honestly | Partially stated | Silent |
| **C14** | Reproducibility scaffold | Source data + Reporting Summary + software versions + data IDs | Some elements | None |
| **C15** | Model–data reconciliation (if any computation) | Explicit agreement sentence + quantified | Model shown, agreement implied | Model orbits unattached to data |

---

## (D) BEFORE → AFTER (nanomedicine / IVIVC / dissolution / PK / CFD)

### Example 1 — Dissolution / formulation screen
**BEFORE (weak):**
> Formulation F7 showed significantly improved dissolution compared to the other formulations (p < 0.05, n = 3). Error bars represent standard error.

**AFTER (elite):**
> Across all nine formulations (F1–F9), F7 gave the highest 60-min dissolution — 92.4 ± 3.1% released versus 41.7 ± 4.8% for the marketed reference tablet (2.2-fold; one-way ANOVA with Dunnett's post-hoc vs the reference, P = 0.0007; n = 3 biologically independent dissolution runs, individual runs shown as dots; mean ± s.d.). F3 did not differ from the reference (n.s., P = 0.214). The full nine-formulation screen is plotted against the reference on shared axes (Fig. 2a), and F7's advantage is confirmed orthogonally by USP-IV flow-through release (Fig. 2b) and by a 1.9-fold higher Cₘₐₓ in the rat PK arm (Fig. 4c).

*Why:* named test matched to the many-vs-reference design (P4), Dunnett's correction (C4), exact p (P5), SD (P6), fold-change vs the marketed comparator not blank (P3/C8), loser-included screen (P9), n.s. shown (P5/C11), and orthogonal confirmation by a second release method + PK (P2).

---

### Example 2 — IVIVC correlation claim
**BEFORE (weak):**
> A good correlation was observed between in-vitro release and in-vivo absorption (R² = 0.94), demonstrating a Level A IVIVC.

**AFTER (elite):**
> In-vitro fraction dissolved and in-vivo fraction absorbed were linearly correlated across all four formulations spanning slow-to-fast release (Level A IVIVC: slope 0.98, R² = 0.94, 95% CI 0.89–0.99; n = 6 animals per formulation, mean ± s.d.). Predictive performance meets the FDA internal-validation criterion — mean absolute prediction error 7.3% for Cₘₐₓ and 5.1% for AUC (both < 10%), computed by leave-one-formulation-out cross-validation rather than on the fitting set. The correlation is reproduced with an independent deconvolution method (Loo–Riegelman vs Wagner–Nelson agree within 4%), and the two computational estimates are consistent with the observed plasma profiles.

*Why:* replaces a bare R² with CI + %PE against the regulatory threshold (P7/C6), out-of-sample validation not fit-set self-congratulation, orthogonal deconvolution methods (P2), explicit model–data reconciliation (P12/C15), and defined n (P8).

---

### Example 3 — CFD / in-silico transport claim
**BEFORE (weak):**
> The CFD model shows that wall shear stress drives nanoparticle deposition, in agreement with experiment.

**AFTER (elite):**
> The CFD model predicts nanoparticle deposition rises 3.4-fold as wall shear stress falls from 12 to 2 dyn cm⁻² (Fig. 5a). Loss-of-function testing isolates shear as the causal driver: setting the shear term to zero collapses predicted deposition by 78%, whereas a matched null perturbation (randomising the inlet phase, which should not affect steady deposition) changes it by 2.1% (n.s.). Predictions are validated orthogonally against microfluidic deposition counts (n = 4 independent chips, mean ± s.d.; predicted vs observed within 9%, two-tailed t-test P = 0.31, i.e. not distinguishable) and against an analytical Lévêque-solution estimate (within 6%). These computational and experimental results are consistent, quantifying the shear–deposition relationship rather than asserting it.

*Why:* quantified mechanism by loss-of-function with a matched *null* perturbation (P11), fold-change magnitude (P7), orthogonal experimental + analytical validation (P2), defined biological n on the wet arm (P8), and an explicit agreement statement with a % gap (P12/C15). Note the correct use of a *non-significant* t-test to argue predicted≈observed.

---

## (E) RED FLAGS

A manuscript is weak on this dimension if any of these appear:

- **SEM error bars**, or error bars whose meaning is never stated — usually SEM chosen to make bars look tight.
- **Asterisks with no exact p-values**, and no non-significant comparisons anywhere (n.s. results silently dropped).
- **One test for everything** — ANOVA (or t-tests) applied to every panel, including survival/time-to-event data that demand log-rank.
- **A wall of pairwise t-tests** across many groups with **no multiple-comparison correction**.
- **"n = 3" with no biological-vs-technical distinction** — or triplicate wells of one experiment reported as n=3.
- **"Significantly improved / enhanced release" with no fold-change, %, CI, or AUC** — significance without magnitude.
- **Comparison only to blank/vehicle/PBS**; the approved or standard-of-care comparator is absent or buried in supplements.
- **Only the winning formulation shown** — the screen funnel and the losing candidates are hidden, so cherry-picking cannot be ruled out.
- **Single-method claims** — each conclusion rests on one technique; no orthogonal readout, no mRNA→protein or in-vitro→in-vivo cross-check.
- **Micrographs/blots with no adjacent quantification** — images asked to carry a claim without an n-backed number.
- **Mechanism asserted, never perturbed** — "this is likely because…" with no loss-of-function experiment, no null-perturbation control.
- **A model/simulation left unreconciled** — computational result reported without an explicit, quantified statement of agreement (or disagreement) with data.
- **No reproducibility scaffold** — assumptions not tested, exclusions/randomization/blinding unaddressed, software versions absent, no source data / Reporting Summary.
- **R² presented as sufficient IVIVC evidence** — no prediction error against a regulatory threshold, no out-of-sample validation.

---

## (F) MODELING & DATA-SCIENCE STATISTICS (in-silico domains only)

*Distilled from Nathan Kutz's `ScientificComputing` / `Data-Driven Modeling & Scientific Computation` (2nd ed.; https://github.com/nathankutz/ScientificComputing) — technique/idiom only, no code copied. These strengthen DS2 for the **model-based** side of this lab's work — **CFD / PINN / IVIVC-modeling / PBPK / data-analysis** — which the wet-lab exemplar biostatistics corpus does not cover. They are guidance the existing checks already point to (C7 test-matched-to-design; the model-selection and out-of-sample requirements in `domain-conventions.md` §B) — no new rubric check IDs.*

**⚠ Hard scope rule (mirrors DS5 §0 anti-mis-transfer).** None of these replace the wet-lab conventions. A cross-validation split, a LASSO penalty, or an SVD truncation is NOT a substitute for geometric-mean + 90% CI on PK, f2 / bootstrap-f2 on dissolution, or an exact test matched to the design on a biological endpoint. Use them ONLY where the deliverable *is* a model or a data reduction, and pair every one with the domain validation in `domain-conventions.md` §0/§B. Recommending any of them as a default for a dissolution, PK/BE, or biological-endpoint dataset is a **DS5 mis-transfer — the same laundering failure, in the opposite direction.**

1. **Fit with residual diagnostics, not just a coefficient.** Report a least-squares / `curve_fit` result WITH its residual plot and a goodness metric (R²adj, RMSE/NRMSE); a fit line without residuals hides structure and heteroscedasticity. (Already required for IVIVC/release, `domain-conventions.md` §A; it is the general rule for any regression.)
2. **Model selection is a comparison, not a single R².** When competing functional forms exist (release kinetics, empirical PK, surrogate models), select by **information criteria (AIC/AICc/BIC)** and/or **cross-validation** and report the ranked candidates — not the one model with the highest raw R². (Reinforces `domain-conventions.md` §B release-kinetics.)
3. **Cross-validation / out-of-sample is the honesty test for a predictive model.** Any model asked to *predict* must show held-out performance — k-fold CV, or a leave-one-out / leave-one-formulation-out split (the IVIVC external-validation requirement). In-sample fit is necessary, never sufficient. State the split and that it was unseen during fitting.
4. **Overfitting control = regularization, stated.** For high-parameter or sparse fits (PINN, PDE-FIND / SINDy, many-descriptor regressions), use **ridge / LASSO / elastic-net** and report the penalty (λ) and how it was chosen (CV). An unregularized high-capacity fit that "matches the data" is the overfitting red flag; a sparsity claim needs the held-out reconstruction (graph-style S42).
5. **Dimensionality reduction must be justified numerically.** SVD / PCA / POD truncation to r modes needs the singular-value (scree) spectrum + variance-captured at r + reconstruction error (graph-style S43/S44) — "we kept the leading modes" without the scree and cumulative-energy curve is an unjustified cut.
6. **Uncertainty on a computed quantity: bootstrap or propagate, don't assert.** A derived / model-predicted quantity gets an interval — a bootstrap CI, or forward uncertainty propagation — not a bare point. (For BE this is the 90% CI; for a model output it is the predictive interval.)
7. **Report the analysis knobs.** Window length (spectrogram / Gabor), truncation r, penalty λ, CV folds, random seed/split — each is a real choice that changes the result. An unstated knob is a hidden degree of freedom, exactly as an undefined error bar is in the wet-lab standard.

---

*Reference document — Statistics & Data-Analysis Rigor dimension. Sections A–E are the reviewer-proof biostatistics standard distilled from the 5 elite exemplars; section F is the modeling / data-science statistics layer distilled from the Kutz repo for the in-silico domains only, hard-scoped so it never launders onto wet-lab endpoints.*
