# Exemplar Graph-Style Library — *Nature Biotechnology* 2025

**Source:** Xue, Hou, Wang et al. "Antimicrobial peptide delivery to lung as peptibody mRNA in anti-inflammatory lipids treats multidrug-resistant bacterial pneumonia." *Nat. Biotechnol.* (2025). DOI 10.1038/s41587-025-02928-x. Brief Communication format.
**Figures mined:** Fig 1, Fig 2, Extended Data (ED) Figs 1–4, Reporting Summary.
**What this exemplar teaches:** how a Nature-tier *bench + in-vivo therapeutics* Brief Communication packs a full discovery→optimization→efficacy→translation arc into 2 main + 4 ED figures, with an ironclad color/entity convention and per-figure statistics on the plot itself. Use it as a pattern bank for any paper/grant that screens candidates, optimizes a formulation, then proves in-vivo efficacy.

---

## 1) DISTINCT GRAPH / CHART STYLES (the full catalogue)

Each entry: **chart type → what it plots → the analytical POINT it makes**. Pick from this list when a manuscript needs the same rhetorical move.

1. **Mechanism-of-action schematic (BioRender)** — Fig 1a, Fig 2h. Cartoon of the therapeutic construct + biology (peptibody domains → protease cleavage at infection site → phagocyte uptake → phagolysosome). *Point:* front-load the reader's mental model before any data; establishes every entity/label that later panels quantify. Always credited "Created using BioRender.com".

2. **Linear construct / cassette map** — Fig 1a top (5′ CAP–UTR–Peptibody–UTR–PolyA; Signal–Cathelin–AMP–Hinge–IgG1 Fc). *Point:* show the engineered molecule's modular architecture as a color-blocked ribbon so domain names are reusable labels downstream.

3. **Annotated western-blot / gel image** — Fig 1b (NR / R / PR3 lanes, kDa ladder, cartoon dimer/monomer glyphs beside bands). *Point:* orthogonal biochemical proof (disulfide-dimer forms, protease cleavage) with schematic glyphs mapping bands to molecular species.

4. **Code / legend table embedded as a panel** — Fig 1c (PB1–PB10 ↔ AMP identity), ED Fig 2a (optimization table: round, level, molar ratios). *Point:* a compact lookup table that indexes the x-axis categories of neighboring bar charts — lets dense screening panels use short codes without a bloated legend.

5. **Grouped/vertical bar chart with error bars + significance brackets** — Fig 1d,e; Fig 2d,g; ED Figs 3,4. Bacterial load / cytokine per condition. *Point:* rank many discrete candidates or conditions against a control; the workhorse "which one wins" panel. Error bars = s.d.; exact P over brackets.

6. **Large-N screening bar chart (candidate library sweep)** — ED Fig 1a,b (TS1–TS70 + MC3/ALC-0315/SM-102 benchmarks on one axis). *Point:* the "hit-picking" panel — dozens of formulations screened at once, hero (TS41/TS41S) visually towering, brackets only on the few meaningful comparisons. Teaches how to keep a ~70-category axis legible (thin bars, rotated tick codes, benchmarks parked at the right end).

7. **Dose–response bar series (paired % + magnitude)** — Fig 1f,g (AF488-positive % AND median fluorescence intensity vs PB9 concentration 0/15/7.5/3.75 µg mL⁻¹). *Point:* show binding is dose-dependent on two readouts side by side (fraction bound + intensity), monotonic decline as dose drops.

8. **Bar/quant panel paired with a representative micrograph (confocal/fluorescence)** — Fig 1f,g,h,i (bar quant + inset confocal of PB9 on bacteria / inside macrophage, scale bar 2.5 µm). *Point:* couple the population statistic to one visual exemplar so the reader sees *and* counts the effect. Micrograph carries a scale bar and channel-color labels.

9. **Two-timepoint grouped bars (temporal replication of an effect)** — Fig 1j,k (bacterial load at 6 h and 12 h, PBS vs LL37 vs PB9, 3-color). *Point:* prove the effect holds and grows over time; same 3-condition palette repeated in twin sub-panels.

10. **Longitudinal mean±s.d. line / trajectory curve** — Fig 2b,e; ED Fig 4b,d (relative body weight % over hours/days, one line per treatment). *Point:* recovery/decline kinetics; hero line stays high while controls dip. Shaded or capped error at each timepoint.

11. **Kaplan–Meier survival step-curve** — Fig 2c,f. Probability of survival vs time, one step-function per group, log-rank (Mantel–Cox) P listed in a stacked block. *Point:* the definitive "does it keep animals alive" endpoint; step drops mark deaths, hero curve plateaus high (80% / 75%).

12. **Bar chart with jittered individual-data-point overlay (dot-on-bar / bar+beeswarm)** — Fig 2d,g,i–l; ED Fig 1c,h; ED Figs 3,4c,e. Every bar has each replicate plotted as a dot. *Point:* show n honestly, reveal spread and outliers, defend small-n in-vivo claims. THE house style — nearly every quantitative bar in the paper carries dots.

13. **Log-scaled quantitative axis** — Fig 2d,g (log₁₀ CFUs per ml); ED Fig 4c,e. *Point:* compress multi-order-of-magnitude bacterial-load differences so a 4-log reduction is readable in one frame.

14. **IVIS small-multiples / faceted image grid with a shared heat colorbar** — ED Fig 1d,f (grid of luminescent mouse lungs, one tile per LNP formulation, single radiance colorbar 1×10⁶–5×10⁸). *Point:* qualitative spatial confirmation across many conditions at a glance; shared color scale makes tiles directly comparable; hero tile is saturated red.

15. **Floating-bar / range-bar chart (min→max with mean line)** — ED Fig 2b,d (luminescence across factor levels 20/30/40/50 etc.). *Point:* orthogonal-array optimization — each bar spans the observed range at that factor level with a mean line, so you read the trend of a single factor while others vary. Compact alternative to box plots for DoE screens.

16. **Normalized bar chart across an A–W condition sweep with a dashed reference line** — ED Fig 2c,e (normalized luminescence for control + conditions A…W, dashed line at control = 1). *Point:* fold-change vs a baseline across a second optimization round; the dashed=1 line makes "better/worse than control" instantly legible.

17. **Dual-axis paired bars** — ED Fig 2f (hydrodynamic diameter + PDI on twin y-axes), ED Fig 2g (zeta potential + encapsulation efficiency). *Point:* report two linked physicochemical characterizations of one particle in a single compact panel.

18. **Cryo-TEM / electron micrograph with scale bar** — ED Fig 2h (single LNP, 100 nm bar). *Point:* structural ground-truth (spherical morphology, core-shell) for the optimized nanoparticle.

19. **Treatment-timeline / study-design schematic** — Fig 2a, ED Fig 4a (Hour/Day axis: infection → LNP treatment → sacrifice → organ dissection → homogenization → plating → quantification, with BioRender icons). *Point:* orient the reader to the in-vivo protocol so every downstream endpoint has temporal context.

20. **Genetic-switch / reporter schematic** — ED Fig 1g (LoxP–Stop–LoxP → tdTomato via Cre). *Point:* explain a reporter readout mechanism before its flow-cytometry quantification (ED Fig 1h).

21. **Cell-type-resolved grouped bars with a "Healthy" baseline anchor** — ED Fig 3a–g (ROS / neutrophil % / iNOS / IL-1β / IL-6 / TNF-α / IFN-γ; groups = Healthy, PBS, SM-102, TS41S). *Point:* place disease and treatment against a true naive baseline so "restores toward healthy" is provable, not just "lower than PBS".

**Styles NOT used (useful contrast for the library):** no heatmap+dendrogram, no volcano, no Sankey/alluvial, no ridgeline, no ROC/PR, no forest/tornado, no slopegraph, no raincloud/violin, no parity/obs-vs-pred plot, no radar. This is a *low-dimensional wet-lab therapeutics* visual grammar: schematics + bars-with-dots + survival + images. A modeling/omics paper would add the missing families.

---

## 2) MULTI-PANEL COMPOSITION (how panels tell one story)

- **One figure = one act of the narrative.** Fig 1 = *design & mechanism* (schematic → construct → biochemical proof → screen → binding → phagocytosis → intracellular killing). Fig 2 = *in-vivo efficacy & translation* (timeline → weight → survival → load, repeated for two infection models, then human-tissue translation). ED figures = the supporting evidence each main claim rests on (LNP screen, formulation DoE, anti-inflammatory panel, chronic-model replication).
- **Reading order is left→right, top→bottom, and it is causal.** A panel's output becomes the next panel's premise: construct (a) → it forms dimers (b) → here are the 10 designs (c) → design PB9 kills best (d,e) → PB9 binds bacteria (f,g) → binding drives phagocytosis (h,i) → phagocytosis kills intracellular bacteria (j,k).
- **Schematic-first, quantify-after.** Every mechanism/schematic panel (1a, 2a, 2h, ED1g, ED4a) sits at the top-left of its figure and defines labels the data panels reuse. Never a data panel before its explanatory cartoon.
- **Twinned panels for two models / two timepoints / two readouts.** The paper repeatedly pairs sub-panels that differ in ONE variable: *S. aureus* vs *P. aeruginosa* (1d/1e, 1f/1g, 1h/1i, 2b-d/2e-g), 6 h vs 12 h (1j/1k), % vs MFI (1f left/right). Same axes, same palette, mirrored layout — the reader learns the panel once and reads its twin free.
- **Representative image as an inset beside its own quantification** (1f,g,h,i): the micrograph sits immediately right of the bar chart that summarizes it, sharing the panel letter.
- **Shared legend blocks placed once per figure**, to the right of a panel cluster (Fig 2's PBS/Cipro/FLuc/LL37/PB9 legend serves b–g; the survival-curve P-value stack sits beside the KM plots). Color key is defined once and honored across all panels in the figure.
- **Small-multiples share a single colorbar** (ED1d,f) rather than one bar per tile.
- **Dense screening axes park benchmarks at the far right** (ED1a,b: TS1…TS70 then MC3, ALC-0315, SM-102) so the eye finds the reference standards in a fixed location.

---

## 3) COLOR-THEME PRACTICE (fixed-entity palette — the strongest lesson)

- **ONE palette across the entire paper, with fixed color = fixed entity.** The convention is rigid and reused in every figure:
  - **Grey = PBS / untreated / negative control** (and "Healthy" often light grey).
  - **Blue (mid, ~steel/cerulean) = the benchmark comparator** — SM-102 LNP, or LL37 (the naked-AMP control), i.e. "the thing we beat".
  - **Red / coral = the hero** — TS41S LNP and PB9, the lead design. The key finding is always the red bar/line/tile.
  - Additional muted categorical fills (mauve, gold/tan) for extra drug controls (Cipro, FLuc) in the survival/efficacy figures, but grey-blue-red always anchor control/comparator/hero.
- **The accent color IS the argument.** Red is reserved for the winning condition; a reader can skim any figure and the red element is the takeaway. This is disciplined accent usage, not decoration.
- **Marker/point overlay inherits the bar color.** The jittered dots on each bar are drawn in the same hue as the bar, so entity identity survives even in the point cloud.
- **Single continuous heat scale for images** (IVIS radiance: blue→green→yellow→red, low→high) with the colorbar shown once — the paper's only sequential/continuous scale, kept separate from the categorical grey/blue/red system.
- **Colorblind considerations:** the grey/blue/red trio is reasonably deutan/protan-distinguishable (grey vs blue vs red differ in lightness *and* hue), and — critically — **position + always-present text labels + dot overlays** mean color is never the sole channel. The blue↔red pairing is the one at mild deutan risk, but they are never adjacent-ambiguous because each bar is directly labeled and grey sits between them by convention. *Lesson for the skill:* pair the hue system with a lightness difference and never rely on color alone.

**Reusable rule to lift into the skill:** assign every molecule/condition a FIXED (color, and where points are shown, the same color for the dots) at figure 1 and never reassign it; reserve the warmest accent for the single hero condition; keep control = neutral grey.

---

## 4) PUBLICATION-READY CRAFT (print-legibility at ~85 mm column)

- **Typography:** small sans-serif (Helvetica/Arial family), panel letters in **bold lowercase a, b, c…** at top-left of each panel. Axis titles ~6–7 pt, tick labels ~5–6 pt, consistent across figures. Units always in the axis title with scientific notation ("×10⁷ CFUs per ml", "log₁₀ CFUs per ml", "Luminescence intensity (×10⁶)").
- **Direct labeling over legends where axis space allows.** Screening axes (ED1, PB codes, TS codes, A–W) put the identity on the x-tick itself; legends are only used when the same 3–5 conditions recur across many panels (Fig 2).
- **Overlap avoidance:** long category lists use short codes (PB1–10, TS1–70, A–W) rotated/stacked on the x-axis rather than full names; the code↔name mapping lives in a separate table panel (Fig 1c, ED2a). Significance brackets are vertically stacked and staggered so multiple comparisons don't collide.
- **Axis treatment:** log₁₀ for bacterial load (multi-order effects); scientific-notation multipliers to keep tick labels short; y-axes start at 0 for bars; body-weight curves use a zoomed band (~80–110%) to make small divergences visible; survival y-axis fixed 0–100%.
- **Scale bars on every micrograph** (2.5 µm confocal in Fig 1; 100 nm cryo-TEM in ED2h), with the value in the legend, not cluttering the image.
- **Annotation style:** exact P-values printed above thin square brackets spanning the compared bars; a stacked list of P-values beside KM curves. Channel/entity labels (e.g., "S. aureus", "Macrophage", "PB9") placed inside micrographs in the channel color.
- **Whitespace / density management:** twinned panels share layout so the eye reuses one mental template; benchmarks parked in fixed positions; a single shared colorbar/legend per cluster; representative image sized small (inset) so the quantitative panel dominates. Dense 70-bar panels stay readable because bars are thin, uniformly colored, and only 2–3 significance brackets are drawn (the meaningful ones), not all pairwise.
- **BioRender for all biological schematics** — consistent icon library gives a uniform "house" look across every schematic panel.

---

## 5) STATISTICAL-PRESENTATION STYLES (stats live ON the figure)

- **Individual data points overlaid on every bar** (dot-on-bar) — the single most consistent statistical-honesty device. Reader sees n, spread, and outliers directly; no hidden distribution behind a mean bar.
- **n stated explicitly in every legend** ("n = 3 / 5 / 7 / 8 biologically independent samples"), plus whether samples are biological replicates and mean ± s.d. (or ± SD in ED). The paper is scrupulous about "biologically independent".
- **Uncertainty = error bars (s.d.)** capped on every bar; longitudinal curves carry s.d. at each timepoint. IQR/CI are not used here — s.d. is the house uncertainty measure (declared in-legend).
- **Exact P-values, not just star codes, printed on the plot** above brackets (e.g., "P = 0.0003", "P < 0.0001"). The star convention (\*P<0.05, \*\*P<0.01, \*\*\*P<0.001, \*\*\*\*P<0.0001) is *defined in the legend* but the numeric P is shown on the graph for the key comparisons — best of both.
- **Test named per panel in the legend:** one-way ANOVA + Dunnett's multiple-comparison test for multi-group bar charts; two-tailed Student's t-test for two-group comparisons; log-rank (Mantel–Cox) for survival curves. Multiple-comparison correction is explicitly named (Dunnett's), matching the Reporting Summary tick for "adjustment for multiple comparisons".
- **Effect size shown as raw magnitude in the text tied to the figure** ("four-log reduction", "5.4-fold greater AUC", "80% survival") rather than a standardized d/r on the plot — the log axis + labeled bars carry the effect size visually. (The Reporting Summary marks Cohen's d / Pearson r as n/a — effect size is communicated by the plotted magnitude, not a coefficient.)
- **Baseline anchoring for "restoration" claims:** including a "Healthy" group (ED3) lets significance brackets show both disease-vs-healthy elevation and treatment-vs-disease reduction, quantifying how far toward normal the therapy pushes each readout.
- **Reproducibility declared centrally** (Methods "Statistics and reproducibility" + Reporting Summary): replicates are biological, ≥3, no exclusions, randomized allocation, P<0.05 threshold — the figure stats and the reporting checklist are internally consistent.

---

## QUICK PICK-LIST (for a future author choosing a style)

| Rhetorical need | Style to lift | Exemplar panel |
|---|---|---|
| Explain the construct/biology first | BioRender MoA schematic + linear cassette map | Fig 1a |
| Screen many candidates, pick a hit | Large-N thin-bar screen, hero towering, benchmarks parked right | ED Fig 1a,b |
| "Which condition wins" against control | Grouped bars + dots + s.d. + exact-P brackets | Fig 1d,e |
| Optimize a formulation (DoE) | Floating min→max range bars per factor level; then normalized bars vs dashed control=1 | ED Fig 2b–e |
| Dose-dependence on two readouts | Paired % + magnitude dose-response bars | Fig 1f,g |
| Population stat + see-it proof | Bar quant beside representative confocal (scale bar) | Fig 1h,i |
| Effect persists/grows over time | Twin timepoint bars (6 h / 12 h) | Fig 1j,k |
| Recovery kinetics | Mean±s.d. trajectory curves (zoomed y-band) | Fig 2b,e |
| Does it keep them alive | Kaplan–Meier step curve + log-rank P | Fig 2c,f |
| Multi-order-of-magnitude difference | log₁₀ y-axis bars + dots | Fig 2d,g |
| Spatial confirmation across conditions | IVIS small-multiples, one shared heat colorbar, hero saturated | ED Fig 1d,f |
| Two linked particle properties | Dual-axis paired bars | ED Fig 2f,g |
| Structural ground-truth | Cryo-TEM/EM micrograph + scale bar | ED Fig 2h |
| "Restores toward normal" | Grouped bars with a Healthy baseline anchor | ED Fig 3a–g |
| Orient to the in-vivo protocol | Treatment-timeline schematic | Fig 2a, ED Fig 4a |

**Two convention rules worth hard-coding into the skill:** (1) fixed color-per-entity — grey control / blue comparator / red hero — reused in every figure, warm accent reserved for the winner; (2) dots-on-every-bar + exact-P-on-plot + n-and-test-in-legend as the default statistical-honesty package.
