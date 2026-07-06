<!-- data-strength-elevator reference module. Distilled from 5 elite exemplars:
Nat Commun 2024 15:739; Nat Commun 2025 16:2198; Nat Mater 2025 24:1653;
Nat Biotechnol 2025 43:1783; Nat Biotechnol 2025 (Brief Communication).
Benchmarks in section (B) are as-extracted from those papers. READ ALONGSIDE
references/domain-conventions.md — do NOT launder wet-lab defaults onto
dissolution/PK/IVIVC/CFD/PINN work (see anti-mis-transfer rules there). -->

# Figure & Data-Visualization Strategy: An Elite-Standard Reference

*Distilled from 5 exemplar papers — Nature Communications ×2, Nature Materials ×1, Nature Biotechnology ×2 — all in the nanomedicine / LNP-RNA / drug-delivery space. This document covers ONE dimension: how elite papers turn measured data into figures. Use it to benchmark and rebuild the figure program of any drug-delivery / IVIVC / dissolution / PK / CFD manuscript.*

---

## (A) PRINCIPLES

**P1 — Pair every image with its own quantification, in the same figure.**
No micrograph, blot, IVIS scan, or flow plot is ever left to carry a claim on its own. Across all 5 papers, qualitative imagery is immediately followed by an n-backed bar/scatter panel: histology + epidermal-thickness bars (NC-2024 Fig 4f/g), CD31 IF + vessel-count bars (Fig 4h/i), flow dot-plots + %-positive summary bars (NC-2025 Fig 4c, Nat Biotech Fig 2c/d), cryo-TEM alongside size/PDI/EE bars. The image proves *plausibility*; the adjacent quantification proves *magnitude and reproducibility*. An unquantified image is treated as an unsupported assertion.

**P2 — Show every replicate as a dot on/around the bar; never a bare bar.**
All 5 papers overlay individual data points (dot-on-bar) so the reader sees n and spread, not just a mean. This is the single most consistent visual convention in the set — it converts "trust me" into "count them." Bare bars with only error whiskers are treated as a rigor failure.

**P3 — Every screen ends in the same panel as the clinical/approved benchmark.**
The lead formulation is never shown against blank or vehicle alone. Screens plot the full candidate library *and* the FDA/clinical gold-standard on a shared axis: MC3, ALC-0315, SM-102 (and electroporation / Lipofectamine / ciprofloxacin / cholesterol-conjugate as relevant). The winner must visibly tower over the accepted state-of-the-art, and the fold-change is stated. "Better than nothing" is disqualifying; "better than the marketed standard" is the bar.

**P4 — Chart type is chosen by data structure, not by habit.** The exemplars use a stable decision logic:
- **Categorical group comparison (formulations, doses, markers)** → bar + individual-point scatter + SD.
- **A continuous predictor (dose, concentration, molar ratio)** → line/scatter dose-response with error bars.
- **Time-to-event (wound closure, survival)** → Kaplan-Meier / step function + log-rank — *never* a bar of "% closed at endpoint" alone.
- **A continuous process over time (release, growth, expression kinetics)** → line + error band, plus an AUC summary bar.
- **High-dimensional panels (20+ cytokines, whole library)** → heatmap for gestalt, then zoom bars for the decisive few.
- **Distributions/particle sizing** → overlaid distribution curves.
Choosing the wrong primitive (e.g., a bar for survival) reads as statistical naïveté to editors.

**P5 — Multi-panel figures are argument arcs, not panel dumps.** Each composite figure walks one complete sub-argument in reading order: design → validate → screen → down-select → mechanism → function. NC-2024 Fig 2 marches screen → optimization table → dose-response → benchmark showdown → physicochemical QC → cryo-TEM. Efficacy figures triangulate ONE claim with 4 orthogonal readouts (photo montage → kinetic curve → AUC bar → log-rank survival), so no single measurement can be dismissed as biased.

**P6 — Overview-then-detail for anything high-dimensional.** When a readout spans many variables, show a log2 fold-change heatmap for the full set (the gestalt) *immediately followed by* absolute-value bars with stats for the ~8 that matter (NC-2025 Fig 5d-g: 26-cytokine heatmap → 8-analyte quantified bars). This avoids both 26 unreadable bar charts and a heatmap with no statistics. Directly portable to CFD/PK parameter sweeps and sensitivity maps.

**P7 — Keep the schematic-to-data ratio low; make every schematic do narrative work.** Roughly **1 orienting schematic per figure, ~1 in 8–10 panels total** is a pure cartoon. Schematics scaffold (workflow, construct map, timeline, mechanism) and are placed *immediately adjacent to the data panel they set up*. A recurring visual motif (a construct cartoon, a color-coded mechanism) is reused verbatim across figures so complex objects stay recognizable. Papers heavy on cartoons and light on data are the anti-pattern.

**P8 — Establish one color/group code early and reuse it mechanically.** A fixed group palette (e.g., PBS grey / control-cargo blue / prior-art green / lead red) is introduced in the first data figure and carried unchanged through every downstream figure. Controls sit in a fixed screen position (benchmarks always far-right). Antigen/specificity pairs use a consistent two-color device (spike-epitope vs control-epitope) so each bar-pair is a built-in internal control. Learned once, the reader never re-decodes.

**P9 — Statistics live ON the plot: exact P-values, defined n, honest n.s.** All 5 print exact P-values on the brackets (P=0.0002, P=0.0069) rather than a wall of asterisks, define a threshold ladder in the legend, and explicitly label non-significant comparisons (n.s., even P=0.0510) instead of hiding them. Error bars are uniformly **mean ± SD** (never silently switched to SEM to shrink whiskers), and n is stated per panel as *biologically independent* samples (distinguished from technical replicates).

**P10 — Climb a translational ladder across the figure sequence.** The figure program escalates model relevance: in-vitro → reporter/normal animal → disease model → *ex vivo human tissue / human primary cells*. The human-tissue capstone panel is what separates a top-journal figure set from a good specialist one, and it is designed in from the start, not bolted on.

**P11 — Mechanism is shown by quantified loss-of-function, not asserted.** Mechanistic panels use matched perturbations with quantified knockdown (endocytosis-inhibitor panels: MβCD −43.3±1.7%, free-ligand competition −63.8±3.1%; two independent γ-secretase inhibitors in two systems), plus a null perturbation that does NOT move the readout. The CFD/PINN/PK analog: ablate one modeled transport pathway/parameter, show the predicted readout collapses versus an inert perturbation.

**P12 — Validate one claim at two molecular/orthogonal levels within one figure.** Knockdown is shown as mRNA *and* protein (qPCR → ELISA); delivery as luminescence *and* biodistribution imaging *and* single-cell flow *and* genetic recombination; particle quality as function *and* light-scattering *and* cryo-TEM. The mRNA→protein and prediction→experiment couplets are textbook orthogonal validation and belong side-by-side in the same figure.

---

## (B) BENCHMARKS

Concrete numbers extracted across the 5 papers. Compare your own manuscript against these.

| Metric | NC 2024 (wound) | NC 2025 (cancer) | Nat Mater (BBB LNP) | Nat Biotech (BCC) | Nat Biotech (peptibody) | **Elite norm** |
|---|---|---|---|---|---|---|
| Format | Full Article | Full Article | Full Article | Brief Comm. | Brief Comm. | — |
| Main figures | 5 | 6 | 6 | 2 | 2 | **2 (Brief) / 5–6 (Article)** |
| Total panels (main) | ~45 | ~62 | ~55 | ~14 | ~23 | **~9–12 panels/main fig** |
| Panels/figure range | 2–15 | 3–12 | ~4–12 | 4–10 | 11–12 | **3–15** |
| Extended/supp figures | ~15 supp | Reporting summary + supp | Reporting summary + supp | ~17 supp | 4 Extended + supp | **breadth offloaded to supp** |
| Pure-schematic panels | ~2 of 45 | ~7–8 of 62 | ~6 of 55 | 4 of 14 | ~4–5 of ~50 | **~10–15% of panels** |
| Schematic:data ratio | ~1:22 | ~1:8 | ~1:9 | ~3:7 | ~1:11 | **≤1 orienting schematic/figure** |
| Individual points on bars | Yes (all) | Yes (all) | Yes (all) | Yes (all 14) | Yes (all) | **5/5 — mandatory** |
| Image + adjacent quantification | Yes | Yes | Yes | Yes | Yes | **5/5** |
| Benchmark vs FDA/clinical std on same axis | Yes (MC3/ALC/SM/electro) | Yes (ALC/SM) | Yes (MC3/ALC/SM) | Yes (Chol-oligo) | Yes (Cipro/SM/MC3/ALC) | **5/5 — mandatory** |
| Exact P-values on plot | Yes | Yes | Yes | Yes | Yes | **5/5** |
| Error bar convention | mean ± SD | mean ± SD | mean ± SD | mean ± SD | mean ± SD | **SD, stated every legend** |
| n.s. labeled honestly | Yes | Yes | Yes | Yes | Yes | **5/5** |
| Survival by log-rank (not bar) | Yes (Fig 4e/5e) | Yes | Yes | — | Yes (Fig 2c/f) | **KM+log-rank whenever time-to-event** |
| Screen shown in full (losers included) | Yes (DIM1–10) | Yes (50 lipids) | Yes (72 lipids, small-multiples) | Yes (12 BCCs) | Yes (10 PB + 72 LNP) | **5/5** |
| Overview→detail (heatmap→bars) | — | Yes (26→8 cytokines) | — | — | Yes (cytokine panels) | **for high-D data** |
| Translational ladder incl. human tissue | Human n/a; 2 cargos | Human glioma+2 lung | Human ex vivo brain | Human brain (2 donors) | Human lung slices + MDMs | **4/5 reach human tissue** |
| Physicochemical QC per lead (size/PDI/zeta/EE + cryo-TEM) | Yes | Yes | Yes | Yes (+PK t½) | Yes | **5/5** |
| Statistical test matched to design | ANOVA+Dunnett / t / log-rank | +DoE L16 | +2-way ANOVA+Šidák/Fisher | +Tukey | ANOVA+Dunnett / t / log-rank | **named, matched per panel** |

**Rules of thumb the numbers imply:**
- A 5–6 figure Article carries **~45–62 quantified panels**; a 2-figure Brief carries **~14–23** and offloads breadth to a heavy supplement.
- **100%** of these papers put individual points on bars, pair images with quantification, benchmark against the clinical standard, print exact P, and use SD.
- Non-data schematics should be **≤~15%** of your panels. If a third or more of your figures are cartoons, you are under-quantified.

---

## (C) SCORING CHECKLIST

Run against any draft. Score each: **Elite (2) / Adequate (1) / Weak (0)**. F1–F15 target ≥ 24/30; with the publication-ready checks F16–F25 appended below, the full DS1 set is 25 checks / max 50 (target ≥ 39/50). F1 (points-on-bars), F3 (benchmark on axis), F5 (SD/n defined), **F16 (F-overlap)** and **F19 (F-cite)** are blockers — a 0 on any caps the DS1 grade.

1. **Individual data points shown.**
 Elite: every bar has dot-per-replicate overlay. Adequate: points on key panels only. Weak: bare bars with only error whiskers.

2. **Image ↔ quantification pairing.**
 Elite: every micrograph/blot/IVIS/flow plot has an adjacent n-backed quantification. Adequate: most images quantified. Weak: representative images stand alone as evidence.

3. **Clinical/approved benchmark on the same axis.**
 Elite: lead vs FDA/marketed comparator on shared axis in a *main* figure, fold-change stated. Adequate: benchmark in supplement. Weak: only vehicle/blank comparator.

4. **Chart type matches data structure.**
 Elite: dose→dose-response, time-to-event→KM+log-rank, kinetics→line+CI+AUC, high-D→heatmap+zoom. Adequate: mostly appropriate, one mismatch. Weak: bars used for survival/continuous predictors.

5. **Error bars = SD, defined; n stated as biological per panel.**
 Elite: "mean ± s.d.", biological n in every legend. Adequate: defined but inconsistent, or biological/technical ambiguous. Weak: SEM used to shrink bars, or n undefined.

6. **Exact P-values on the plot + threshold ladder + honest n.s.**
 Elite: exact P on brackets, ladder defined, n.s. labeled. Adequate: asterisks only. Weak: no on-plot stats or hidden non-significant comparisons.

7. **Statistical test named and matched to design.**
 Elite: ANOVA+Dunnett/Tukey for multi-group, t-test for two-group, log-rank for survival, 2-way for factorial — stated per panel; correction disclosed. Adequate: one global test named. Weak: no test named or wrong test.

8. **Multi-panel figures build an argument.**
 Elite: each figure = one sub-argument in reading order; efficacy triangulated by ≥3–4 orthogonal readouts. Adequate: logical but no triangulation. Weak: unordered panel dump.

9. **Schematic-to-data ratio controlled.**
 Elite: ≤~15% pure schematics, ~1 orienting schematic/figure, each adjacent to its data. Adequate: ~25%. Weak: cartoons dominate; schematics detached from data.

10. **Consistent color/group code across all figures.**
 Elite: one palette + fixed benchmark position, reused unchanged; recurring motif for complex objects. Adequate: consistent within figures, drifts across. Weak: colors/order change figure to figure.

11. **Full screen shown (losers included) + physicochemical QC per lead.**
 Elite: whole candidate library on one axis + size/PDI/zeta/EE + cryo-TEM for the lead. Adequate: winner-only bar + partial QC. Weak: no screen shown; lead appears without justification.

12. **Overview-then-detail for high-dimensional data.**
 Elite: heatmap/sensitivity map for the full set → quantified zoom bars for the decisive few. Adequate: full-set table only. Weak: dozens of unreadable individual bar charts.

13. **Mechanism by quantified loss-of-function.**
 Elite: matched perturbation with quantified knockdown + inert null control. Adequate: perturbation shown, not quantified. Weak: mechanism asserted in prose only.

14. **Orthogonal / two-level validation of the core claim in-figure.**
 Elite: claim shown two ways (mRNA+protein; prediction+experiment; function+imaging). Adequate: one orthogonal pair somewhere in paper. Weak: single method carries the conclusion.

15. **Translational ladder visible in the figure sequence.**
 Elite: escalates to a disease model and human tissue/primary-cell panel. Adequate: one in-vivo confirmation. Weak: in-vitro only, no relevance climb.

### Publication-ready craft checks (F16–F25) — see `publication-ready-figures.md`

These append to F1–F15. They govern whether a *correct* figure is *submission-ready*. **F16 (F-overlap) and F19 (F-cite) are BLOCKERS** — a 0 caps the DS1 grade at Not-ready, because the user requires publication-ready output. Also consult `graph-style-library.md` when choosing the primitive so the sharpest chart is selected for each analytical point.

The six-part figure-consistency test — *same fonts & sizes (F21 family/weight + F24 sizes) · similar line weights and distinguishable points (F22) · intentional, repeated colors (F18 + F20) · accessible to screen-reader and colorblind readers (F23 + F18) · consistent scale across figures (F24) · one coherent story (F25)* — is enforced by F18/F20/F21 plus the four checks F22–F25 below.

16. **F-overlap — zero text overlap.** *(BLOCKER)*
 Elite: the deterministic `assert_no_overlaps(fig)` bbox-intersection audit passes (wired as a build-time gate before save) AND each dense region was zoom-cropped and read as backstop; no label/annotation/legend/tick/bracket/mark overlaps any other text or mark; direct labeling + legends outside axes + staggered brackets. Adequate: programmatic audit passes but one minor visual crowding remains in a non-key panel. Weak: labels collide, legends float over data, OR the programmatic `assert_no_overlaps` audit was not run (visual-only inspection of a downsampled PNG does not satisfy this check — a few-pixel collision is invisible at that scale). See `publication-ready-figures.md` R1 for the audit method and the reusable snippet.

17. **F-zoom — legible at 100% / print size.**
 Elite: exported ≥ 300 dpi (or vector); every text element clears the point floors (≥ 7 pt ticks, ≥ 8 pt axis titles/annotations at ~85 mm) at the intended print width. Adequate: legible but one element under-size, or dpi unconfirmed. Weak: text only readable when zoomed in; sub-floor type; raster < 300 dpi. *(Per-figure legibility floors; consistency of those sizes across the whole suite is F24/F-scale.)*

18. **F-theme — one consistent colorblind-safe palette.**
 Elite: single manuscript-wide Okabe-Ito (or equivalent CB-safe) palette reused unchanged, one accent reserved for the key finding, color never the sole channel. Adequate: consistent within figures, drifts across. Weak: rainbow-per-figure, non-CB-safe pairing relied on alone.

19. **F-cite — every figure and table cited in the text.** *(BLOCKER)*
 Elite: every main/supp figure and every table has an in-text callout at the point it supports, pointing to the correct panel. Adequate: most cited, ≤1 uncited or one wrong-panel callout. Weak: uncited displays present (a defect).

20. **F-entity — same color + marker/shape per entity everywhere.**
 Elite: each API/molecule/condition has a fixed color AND marker/shape (and hatch) reused in every figure AND every table, per a written mapping table. Adequate: color consistent but marker/shape drifts, or table-vs-figure mismatch. Weak: an entity changes color or shape between displays.

21. **F-style — figure typography matches the manuscript.**
 Elite: figure font family/weight matches the document body and is identical across all figures (set once in a shared style file). Adequate: matched in most figures, one outlier. Weak: figures use a different/ inconsistent font than the manuscript. *(Family/weight here; consistent font *sizes* across figures is F24/F-scale.)*

22. **F-lineweight — consistent line/point weight; data points distinguishable.**
 Elite: one weight ladder (line, spine, error-cap, marker sizes) set once and reused across every figure; adjacent series separable by style+color+shape and pass the greyscale-separation test; dense scatter defeats overplotting (alpha/jitter/density-binning) so individual points stay countable. Adequate: weights roughly consistent but one figure heavier/lighter, or mild overplotting in a non-key panel. Weak: line weights drift figure-to-figure, series indistinguishable without color, or points fuse into a blob. See `publication-ready-figures.md` R7.

23. **F-a11y — screen-reader + non-color accessibility.**
 Elite: every figure has an alt-text/described caption stating the finding, all color distinctions are redundantly encoded (position + label + shape/style/hatch), contrast meets the floor, and text is exported as real (vector) text so it is machine-readable. Adequate: captions convey the finding and encoding is redundant, but alt-text/tagged export not confirmed. Weak: color-only encoding, no text equivalent, or rasterized figure text. See `publication-ready-figures.md` R8.

24. **F-scale — consistent size & scale across the figure suite.**
 Elite: same-role text (tick/axis-title/panel-letter) is the same point size in every figure, panels of a kind share dimensions, and marker/line/bar scale is uniform, so no figure needs 200% magnification while another needs zooming out. Adequate: mostly uniform, one figure visibly off-scale. Weak: figures rendered at inconsistent scales; sizes vary figure-to-figure. See `publication-ready-figures.md` R9.

25. **F-suite — figures read as a single story.**
 Elite: one visual language (palette F18, entity map F20, typography F21, sizing F24) held across all figures, repeated chart idioms for repeated questions, twinned/paralleled panels, and a deliberate figure order that builds the argument (setup→mechanism→validation→translation). Adequate: consistent language but the sequence does not clearly build a story. Weak: a figure looks like it came from a different paper, or the order is an unordered pile. See `publication-ready-figures.md` R10.

*Target with F16–F25: ≥ 39/50, with F-overlap and F-cite ≥ 1 (a 0 on either is a blocker).*

---

## (D) BEFORE → AFTER TRANSFORMATIONS

*(Realistic weak drafts vs. elite-standard rewrites, in nanomedicine / IVIVC / dissolution / PK / CFD contexts.)*

### Example 1 — Formulation screen (weak bar) → benchmarked dot-on-bar with clinical comparator

**BEFORE (weak).**
> *Figure 3.* Cumulative drug release at 24 h for our optimized PLGA nanoparticle (F7). F7 showed higher release than the other formulations. Bars represent mean values (n = 3). *[Single grey bar per formulation, no points, no error bars, no marketed comparator, "higher" unquantified.]*

**AFTER (elite).**
> *Figure 3.* Cumulative release at 24 h across the full formulation library (F1–F10) benchmarked against the marketed reference product (Ref) and free drug, on a shared axis. F7 released 82.4 ± 3.1% versus 51.2 ± 4.0% for the reference product — a 1.6-fold increase (one-way ANOVA + Dunnett's, P = 0.0007); F1–F6 and F8–F10 did not differ significantly from Ref (n.s., P > 0.05, labeled). Individual replicate values are overlaid as dots; bars are mean ± s.d.; n = 3 biologically independent batches. *[Full library shown, individual points, exact P on brackets, clinical benchmark on the same axis, effect as fold-change, n.s. labeled.]*

---

### Example 2 — Dissolution/PK time course (bar of one endpoint) → kinetics + AUC + correct summary stat

**BEFORE (weak).**
> *Figure 4.* Plasma concentration was higher for the nanocrystal formulation than the coarse suspension at 4 h (bar chart, *P < 0.05, asterisks only). This demonstrates improved bioavailability. *[Single-timepoint bar, no profile, no AUC, no exposure metric, asterisk-only, no dose-normalization.]*

**AFTER (elite).**
> *Figure 4.* (a) Mean plasma concentration–time profiles (0–24 h) for the nanocrystal, coarse suspension, and marketed tablet, each as a line with s.d. error band; n = 6 animals/group. (b) Dose-normalized AUC(0–24 h) as bar + individual-animal scatter: nanocrystal 3,120 ± 210 vs suspension 1,180 ± 190 ng·h·mL⁻¹ (2.6-fold; one-way ANOVA + Tukey, P = 0.0003) and vs marketed tablet 2,010 ± 240 (1.6-fold, P = 0.011). (c) Cmax and Tmax reported alongside. AUC is normalized within-run to the reference arm to control inter-day variability. *[Full profile as line+CI, AUC as the correct exposure summary with points, clinical comparator included, magnitude as fold-change, within-run normalization stated.]*

---

### Example 3 — CFD/PBPK model result (untethered simulation) → prediction↔data couplet with quantified agreement and loss-of-function

**BEFORE (weak).**
> *Figure 6.* CFD simulation of wall shear stress in the dissolution vessel. The model shows high shear near the paddle. Our simulated release profile agrees well with experiment. *[Contour plot alone, "agrees well" unquantified, no experimental overlay, no sensitivity/perturbation, mechanism asserted.]*

**AFTER (elite).**
> *Figure 6.* (a) CFD wall-shear-stress field (contour, quantitative colorbar in Pa) with the schematic paddle geometry inset. (b) Overlay of CFD-predicted vs experimentally measured fraction released over 0–120 min (simulation = solid line, experiment = dots ± s.d., n = 3); predictions fall within the experimental s.d. at all timepoints and the IVIVC correlation is R² = 0.98 (Level A). (c) Parameter sensitivity map (heatmap, log2 change in predicted t₅₀) across the swept inputs, then (d) zoom bars for the two dominant parameters (hydrodynamic boundary-layer thickness, diffusivity) with quantified effect; ablating the shear-driven convective term collapses the predicted–observed agreement (R² 0.98 → 0.41), whereas perturbing an inert parameter does not (R² 0.97, n.s.). *[Quantitative colorbar, prediction–experiment overlay with numeric agreement, overview→detail sensitivity map, mechanism proved by quantified loss-of-function vs inert null.]*

---

## (E) RED FLAGS

Signs a manuscript is weak on figure & data-visualization strategy:

- **Bare bars.** Error whiskers but no individual data points — the reader cannot see n or spread. (All 5 exemplars overlay points.)
- **Orphan images.** A micrograph, blot, IVIS scan, or "representative" flow plot presented as evidence with no adjacent quantified panel.
- **Straw-man comparators.** The lead is only compared to blank/vehicle/untreated; the FDA-approved or marketed standard is absent or buried in a supplement.
- **Winner-only presentation.** The lead formulation appears with no visible screen — the reader can't tell it wasn't cherry-picked.
- **Wrong primitive for the data.** A bar of "% closed/responded at endpoint" instead of a Kaplan-Meier + log-rank; a bar at one timepoint instead of a kinetic profile + AUC; a bar for a continuous dose predictor.
- **SEM masquerading as precision.** Error bars silently reported as SEM (smaller) rather than SD, or the error-bar type left undefined.
- **Asterisk walls / hidden n.s.** Only \*/\*\*/\*\*\* with no exact P-values, or non-significant comparisons quietly dropped rather than labeled.
- **Undefined or technical-only n.** "n = 3" with no statement of whether replicates are biological or technical.
- **Test not named or mismatched.** No named statistical test, no multiple-comparison correction for multi-group data, or a t-test/ANOVA used where survival/factorial designs demand log-rank / two-way ANOVA.
- **Cartoon-heavy, data-light.** More than ~15–20% of panels are schematics, or schematics float detached from the data they should introduce.
- **Palette drift.** Group colors or comparator ordering change from figure to figure, forcing constant re-decoding.
- **High-dimensional data dumped as raw grids.** 20+ analytes shown as an unreadable wall of bar charts with no heatmap gestalt, or a heatmap with no statistics and no quantified zoom.
- **Mechanism asserted, not shown.** "This is likely due to caveolae-mediated uptake" with no inhibitor/loss-of-function panel and no quantified knockdown against an inert control.
- **Single-method conclusions.** A knockdown claimed at transcript level only (no protein), or a simulation reported with no experimental overlay and no numeric agreement metric.
- **No relevance climb.** Everything is in-vitro; no disease-model or human-tissue/primary-cell panel anchors real-world relevance.
- **Missing physicochemical QC.** A lead nanoparticle reported without size/PDI/zeta/encapsulation-efficiency and a direct morphology image (cryo-TEM/TEM).

---

*Reference document — Figure & Data-Visualization Strategy dimension only. Grounded in 5 exemplar papers (Nat Commun 2024 15:739; Nat Commun 2025 16:2198; Nat Mater 2025 24:1653; Nat Biotechnol 2025 43:1783; Nat Biotechnol 2025 Brief Communication). Numbers in §B are as-extracted from the supplied analyses.*
