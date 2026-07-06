# Exemplar Graph-Style Library — Nat. Commun. 2024, 15:739

**Source:** Xue, Zhang, Zhong et al. "LNP-RNA-engineered adipose stem cells for accelerated diabetic wound healing." *Nature Communications* 15:739 (2024). DOI 10.1038/s41467-024-45094-5.
**Domain:** nanomedicine / LNP formulation screening → RNA delivery → ex vivo cell engineering → in vivo diabetic wound healing.
**Figure count mined:** 5 main composite figures (Fig. 1 schematic/chemistry; Figs. 2–5 data). This is a Nature-family, high-density-multipanel exemplar. Use it as the reference for *screening-to-in-vivo* storyline figures.

---

## 1. DISTINCT GRAPH / CHART STYLES (the reusable catalog)

Every distinct visual idiom actually used, with what it plots and the exact analytical point it lands:

1. **Workflow / process schematic (biological pipeline).** (Fig. 1a) Left-to-right icon storyboard: ASC isolation → LNP-RNA treatment → hydrogel encapsulation → in-vivo embedding → protein release → healing. BioRender-style. POINT: orient the reader to the whole experimental arc *before* any data — a single "story spine" panel.
2. **Reaction-scheme / chemical-synthesis diagram.** (Fig. 1b) Structural formulae with reagent/condition arrows, plus a boxed combinatorial R-group legend (R1–R10 mapped to DIM1–DIM10). POINT: define every molecular entity by name once, so downstream bar labels ("DIM1", "DIM7"…) are unambiguous. The R-group inset is a *library key*.
3. **Grouped/simple bar chart with mean ± SD error bars + individual data dots overlaid.** (Fig. 2a, 2e; Fig. 3a, 3b; Fig. 4g,i,k; Fig. 5g,i,k,m,o) The workhorse. Each bar = a condition (a lipid, a formulation, a treatment group); dots = the n=3 (or n=10) replicates sitting on the bar. POINT: show central tendency **and** the raw spread + n simultaneously; never a bare bar. This is the house default for any categorical comparison.
4. **Screening bar chart, wide categorical axis, log-ish dynamic range, with a significance bracket spanning the extremes.** (Fig. 2a) ~25 candidate lipids + FDA controls (MC3, ALC-0315, SM102) + electroporation, all on one axis, one clear "winner" bar towering over the rest. POINT: the hit-selection panel — visually screams which candidate wins against the full library AND against gold-standard benchmarks in the same frame.
5. **Line-with-error-bar "factor sweep" / one-factor-at-a-time optimization plots (small-multiples row).** (Fig. 2c) Four side-by-side line plots: luminescence vs molar ratio of DIM1 / DOPE / cholesterol / DMG-PEG. Each is a mean ± SD trend across levels. POINT: show the response surface of an orthogonal optimization one variable at a time — reveals the optimum level per component.
6. **Paired-round "before/after optimization" grouped bar (two-color series).** (Fig. 2d) First-round (blue) vs second-round (green) fold-change per formulation, side by side. POINT: quantify the *improvement delta* from iterative optimization; color encodes optimization round.
7. **Dual-axis / twin-metric bar (two y-axes, one per physical property).** (Fig. 2f) Size (nm) on left axis + PDI on right axis for the same particle. POINT: co-present two characterization metrics that share the sample identity but not the scale. Also Fig. 2g (encapsulation efficiency % left / zeta potential right).
8. **Kinetic time-course line plot (expression over days), multiple treatment series.** (Fig. 3a "Day1/Day2"; Fig. 3d; Fig. 4a; Fig. 5a) Luminescence or protein concentration vs time post-treatment, one line/series per RNA cargo (mRNA/saRNA/SEC). POINT: the central mechanistic claim of the paper — SEC gives *durable, prolonged* expression; the divergence of curves over time IS the finding.
9. **Overlaid size-distribution / spectral trace (intensity vs diameter).** (Fig. 3c) DLS-style curves for mRNA / saRNA / SEC LNPs superimposed. POINT: show the three formulations are physically equivalent (overlapping curves) so downstream biology isn't a size artifact — a "controls-matched" panel.
10. **Cryo-TEM micrograph with scale bar.** (Fig. 2h; Fig. 3i CLSM) Representative electron/confocal image. POINT: morphology/qualitative ground-truth (spherical, intact particles; cytosolic dye diffusion). Always with an explicit scale bar and "representative of n=3".
11. **Flow-cytometry histogram stack / overlay (offset density curves).** (Fig. 3e) For each surface marker (CD106, CD44, CD29, SCA-1, CD11b/CD45): overlaid ISO/WT/DS fluorescence-intensity density curves, stacked as a small-multiples row of markers. POINT: show engineered cells retain identity (phenotype unchanged) — histogram overlap = "no phenotypic drift."
12. **Fluorescence micrograph channel grid (multi-channel + merge columns).** (Fig. 3i) Rows = condition (Untreated / DIM1T LNP); columns = Calcein / Alexa-647 / Bright field / Merge. POINT: co-localization / uptake evidence read across channels in one row. Classic imaging small-multiple matrix.
13. **Longitudinal photographic panel grid (specimen over time).** (Fig. 4b, Fig. 5b) Rows = treatment group; columns = Day 0/3/6/9/12/15/18; each cell = a wound photo. POINT: the qualitative efficacy montage — reader sees wounds shrink faster in the lead group across a shared time axis. Shared scale bar for the whole grid.
14. **Relative-outcome decay curves with error bars (wound-size vs time), one line per group + significance callouts.** (Fig. 4c, Fig. 5c) Normalized wound size 1.0→0 over days; lead group's curve drops fastest. POINT: quantitative efficacy trajectory; the *separation between curves* is the effect.
15. **Normalized AUC summary bar (collapsing a time-course into one number per group).** (Fig. 4d, Fig. 5d) Bar of normalized area-under-the-wound-curve per group + dots + significance. POINT: distills each decay curve (panel c) into a single comparable scalar — the "summary statistic of the kinetics."
16. **Kaplan–Meier-style step function for "time-to-event" (time-to-closure / % closed wounds).** (Fig. 4e, Fig. 5e) Step curves of % closed wounds vs day, analyzed by Log-rank test. POINT: survival-analysis idiom repurposed for wound closure — when a group reaches 50%/100% closure. Dashed 50% reference line.
17. **Histology whole-section montage (stain rows × group columns).** (Fig. 4f, Fig. 5f) Rows = MTS (Masson's trichrome) and H&E; columns = the treatment groups. POINT: tissue-architecture evidence (epidermal thickness, collagen) across groups at matched magnification.
18. **Immunofluorescence marker montage + paired quantification bar.** (Fig. 4h/i CD31 vessels; 4j/k αSMA myofibroblasts; Fig. 5h–o adds IL-6, IL-10) IF image grid (group columns) *immediately paired* with a quantification bar chart (vessels·mm⁻², cells·mm⁻²). POINT: qualitative image + quantitative count sit adjacent so the reader validates the number against the picture — image-and-its-metric pairing is a signature move.
19. **Orthogonal-design factor table (inline data table as a figure panel).** (Fig. 2b) A gridded table of molar ratios / mass ratios / N/P ratios for each optimization run. POINT: make the DOE reproducible on the figure itself; a table used *as* a panel, not relegated to methods.

**Notably absent** (candidate styles this paper did NOT need): obs-vs-pred parity, heatmap+dendrogram, forest/tornado sensitivity, Sankey/alluvial, ridgeline, waterfall, ROC/PR, slopegraph, raincloud/violin, beeswarm-on-violin. Useful negative signal: a screening→in-vivo efficacy story is carried almost entirely by **bar+dots, kinetic lines, KM step, AUC bars, and image/montage grids** — not by ML-style diagnostic plots.

---

## 2. MULTI-PANEL COMPOSITION (how panels tell one story)

- **Whole-paper spine = "funnel" narrative.** Fig.1 orient (schematic + chemistry) → Fig.2 screen & characterize the material (find the winning LNP) → Fig.3 mechanism & cell-level durability (why SEC works, cells stay healthy) → Fig.4 in-vivo efficacy of therapeutic protein #1 (HGF) → Fig.5 second, better protein (CXCL12) + immune remodeling. Each figure is one act.
- **Within a composite figure, panels run top-left→bottom-right as claim → evidence → quantification.** E.g. Fig.4: (a) protein kinetics → (b) wound photo montage → (c) size-decay curves → (d) AUC bar → (e) closure KM → (f) histology → (g) epidermal-thickness bar → (h–k) IF images each with its paired count bar.
- **Image-then-quantify pairing** is the dominant intra-figure logic: every representative image panel is followed by a bar panel that quantifies exactly what the image shows (CD31 image → CD31 vessel-count bar). The eye and the statistic are placed next to each other.
- **Small-multiples rows** for anything with a sub-dimension: the marker set in flow histograms (Fig.3e), the four factor-sweep line plots (Fig.2c), the day columns in wound montages, the stain rows in histology. Shared axis ranges / shared time axis across the row make cells directly comparable.
- **Shared scale bars & shared legends** serve a whole grid rather than per-cell (one scale bar per montage; one color legend per figure reused across its bar panels).
- **Table-as-panel** (Fig.2b) is embedded beside its own bar charts so the DOE numbers and their luminescence outcomes are read together.

---

## 3. COLOR-THEME PRACTICE

- **Fixed condition→color mapping reused across figures (the key discipline).** The RNA cargo classes get consistent colors wherever they appear: mRNA = green, saRNA = blue, **SEC = red/pink (the hero cargo)**. This holds across Fig.3a/b/d, Fig.4a, Fig.5a. The reader learns "red = the durable/best condition" once and carries it.
- **Accent color reserved for the key finding / lead group.** The lead in-vivo groups (HGF DS-ASCs, CXCL12 DS-ASCs) are drawn in the warm accent (red/orange) while comparators (Vehicles = grey, WT ASCs = green, DM-ASCs = blue) stay cooler. The hero is always the warm/saturated one — the eye goes to it by design.
- **Two-series encodings are semantic, not decorative.** Optimization-round bars: round-1 = blue, round-2 = green (Fig.2d). Twin-axis property bars keep one color per axis.
- **Muted/greyscale for baselines and "untreated/vehicle".** Grey = do-nothing control throughout, so accent color always reads as "the treatment doing something."
- **Palette is limited and consistent** — roughly a 4–5 color set (grey, green, blue, red/pink, orange) reused everywhere rather than a new rainbow per figure. Fluorescence images use channel-native colors (calcein green / Alexa-647 magenta / DAPI blue / CD31 red / αSMA green).
- **Colorblind note:** the green-vs-red pairing (mRNA green vs SEC red) is *not* fully deuteranope-safe. The paper compensates by (a) fixed left-to-right ordering, (b) direct category labels, and (c) always overlaying data dots + brackets so meaning survives loss of hue. A future author should prefer a blue/orange (Okabe-Ito) hero pairing when possible, but if keeping green/red, replicate their redundancy (order + labels + shape).

---

## 4. PUBLICATION-READY CRAFT (print-size legibility)

- **Dense panels kept readable by ruthless small-multiples + shared axes.** Rather than cramming series into one plot, they split into a row of small panels (Fig.2c four sweeps; Fig.3e five markers), each simple, each with a shared y-scale.
- **Direct category labels on the x-axis** (lipid names DIM1…, group names) instead of a legend the reader must cross-reference — legends are used only for the 2–3 series colors.
- **Significance shown as thin brackets with the exact P-value printed** (e.g. "\*\*\*\*P<0.0001", "\*\*\*P=0.0002") directly above the compared bars, rather than only asterisks — the numeric P is on the figure.
- **Consistent error-bar + dot styling** at small size: thin caps, open/filled dots sized to remain visible at ~85 mm column width.
- **Scale bars are explicit and stated in the legend** ("scale bar = 50 nm", "7 mm (b); 1 mm (f); 50 µm (h,j)") — one per montage, burned into the image corner.
- **Whitespace / alignment:** panels share baseline gridlines; image grids are tightly gridded with uniform cell size and a single shared scale bar, avoiding per-image clutter.
- **Axis treatment:** wide-dynamic-range screening (Fig.2a) uses a large linear y with scientific-notation tick labels (×10⁷) so the tall winner and short losers coexist; time axes are shared and evenly spaced across small-multiples.
- **Every image panel is annotated "Representative images from n=3 independent experiments"** in the legend — qualitative panels carry their own n and reproducibility statement.

---

## 5. STATISTICAL-PRESENTATION STYLES (stats shown ON the figure)

- **Raw data always visible:** individual replicate **dots overlaid on every bar** (n=3 in vitro; n=10 wounds in vivo). The n is stated per panel in the legend.
- **Uncertainty = mean ± SD** shown as error bars on bars and as error-bar bands on line plots (explicitly "mean ± standard deviation (s.d.)" in legends). IQR/CI ribbons are not used here — SD is the house convention.
- **Significance printed numerically:** exact P-values on brackets, plus the asterisk key defined in the legend (\*P<0.05, \*\*P<0.01, \*\*\*P<0.001, \*\*\*\*P<0.0001) and "n.s." where non-significant (Fig.3d spells out "n.s. P=0.0510").
- **Test named per panel in the legend, matched to design:** one-way ANOVA + Dunnett's multiple-comparison for multi-group comparisons; two-tailed Student's t-test for two-group; **Log-rank test for the time-to-closure KM curves.** The right test is announced for each analysis.
- **Effect size communicated by design, not a coefficient:** the "winner" bar towering in the screening panel, the fold-change bars (Fig.2d), and the normalized-AUC bars (Fig.4d/5d) each turn an effect into a single readable magnitude. Kinetic separation between colored curves is itself the effect-size display.
- **Reproducibility statement standardized:** "Data are from n=… biologically independent samples and are presented as mean ± s.d.; statistical significance by [test]" appears in every legend; a "Statistics & reproducibility" methods block confirms ≥2 independent experiments, 4–5 mice/group, no data excluded, all points shown.

---

## QUICK PICK-LIST (for a future author choosing a style)

| Need | Use this idiom from this exemplar |
|---|---|
| Compare many candidates + benchmarks, pick a winner | wide screening bar (dots + spanning bracket + FDA controls in-frame) — §1.4 |
| Any categorical comparison | bar + mean±SD error + individual dots — §1.3 |
| Optimize a formulation over factor levels | small-multiples line sweeps, one panel per factor — §1.5 |
| Show improvement from iteration | two-color paired-round bars — §1.6 |
| Two physical properties, one sample | dual y-axis bar — §1.7 |
| Durability / kinetics is the point | multi-series time-course lines, hero cargo in accent color — §1.8 |
| Collapse a kinetic curve to one number | normalized-AUC summary bar — §1.15 |
| "How fast did it resolve" | KM step function + Log-rank + 50% reference line — §1.16 |
| Prove phenotype unchanged | offset flow-histogram small-multiples across markers — §1.11 |
| Qualitative efficacy over time | photographic montage grid (group rows × day columns, shared scale bar) — §1.13 |
| Validate a count against a picture | IF image panel immediately paired with its quantification bar — §1.18 |
| Make a DOE reproducible | inline factor table used as a figure panel — §1.19 |

**One-line house style to import:** limited fixed palette with a warm accent reserved for the hero condition, every bar carries dots + mean±SD + numeric P, images are gridded small-multiples with one shared scale bar and a "representative of n=X" note, and each figure is one act of a screen→mechanism→in-vivo funnel.
