# Graph-Style Library — Exemplar Mining

**Source:** Wang, Xue, Markovic et al. "Blood-brain-barrier-crossing lipid nanoparticles for mRNA delivery to the central nervous system." *Nature Materials* 24, 1653-1663 (2025). DOI 10.1038/s41563-024-02114-5.

**What it is:** A materials/nanomedicine screening-and-optimization paper (72 lipids → lead formulation MK16). This is the archetypal "combinatorial screen → lead selection → mechanism → in-vivo efficacy → disease models" narrative. Its figure grammar is a near-perfect template for any dose-response / screening / delivery-efficiency data-strength job.

---

## 1) DISTINCT GRAPH / CHART STYLES (the full inventory)

The paper is disciplined: it reuses a **small number of chart archetypes** rather than inventing new ones per panel. That restraint is itself the lesson. The distinct styles:

1. **Grouped bar chart with per-bar error bars + overlaid raw-data dots ("bar-with-scatter" / dynamite-plus-points).**
   - *Where:* Fig 2a-g (screening luminescence across lipid series LD/DS/TM/TD/CD/MK/organs), Fig 3a,d,f,i,j, Fig 4f-i, Fig 5e.
   - *Plots:* normalized luminescence (delivery efficiency) or % GFP+/tdTomato+ per formulation or per cell type.
   - *Analytical point:* rank many candidates on one axis and let the reader eyeball the winner. Every bar carries its own s.d. whisker AND the n=3 individual replicate points sitting on top of the bar — so the reader sees both the summary and the raw spread. This is the modern replacement for a bare bar chart; **never plot a mean bar without its dots** at n≤~10.
   - *Variant — reference-line normalization:* all series are normalized to the MC3 (FDA-approved benchmark) bar = 1.0, so "fold-improvement over standard of care" is read directly off the y-axis.

2. **Grouped/clustered bar chart (condition × category), multiple colored series per x-tick.**
   - *Where:* Fig 3f (cell type on x, 5 dose/formulation series as colored bars), Fig 4i (cell type × PBS/MK16-1×/MK16-3×/MC3-1×/MC3-3×), Fig 2i (organ × 4 treatments).
   - *Analytical point:* two-factor comparison (which formulation × which cell type / organ) in one panel; the eye scans across clusters for the interaction (e.g., MK16 wins in neurons+astrocytes but ties MC3 in oligodendrocytes → n.s. labeled).

3. **Line-plot growth/kinetic curves with error bars (mean ± s.d. over time), multiple treatment lines.**
   - *Where:* Fig 6b (tumour luminescence vs day, 3 treatment lines PBS/control-mRNA/Pten-mRNA).
   - *Analytical point:* longitudinal divergence between arms; the flat blue (treatment) line vs rising red/grey (controls) makes efficacy self-evident. Error bars per timepoint show the growing variance in untreated arms.

4. **Kaplan-Meier survival curve (step function), multiple arms.**
   - *Where:* Fig 6d (survival % vs days, 3 arms).
   - *Analytical point:* time-to-event; log-rank (Mantel-Cox) test. Classic KM staircase with censoring implied; the treatment arm plateau at ~70% survival is the headline.

5. **Flow-cytometry pseudocolor density plots (2D dot/contour, SSC-A vs marker).**
   - *Where:* Fig 3g (Neuron/Astrocyte/Microglia × PBS/MK16, GFP on x, SSC-A on y), Fig 5 IFCM panels.
   - *Analytical point:* show the actual gating and the % positive as an on-plot annotation. Blue→green→red density heat encodes event count. Reproduces the primary measurement behind the % bar charts (Fig 3f) so a skeptic can check the gate.

6. **IVIS / bioluminescence anatomical heat-overlay images (perceptual color ramp on grayscale animal/organ).**
   - *Where:* Fig 2h (brains MC3 vs MK6), Fig 3b,e,k (brains), Fig 6c (whole-body mouse grid over 8 timepoints).
   - *Analytical point:* spatial signal intensity where it physically happens. A jet-like rainbow ramp (blue low → red high) sits on the grayscale specimen with a shared vertical colorbar in scientific-notation units (×10⁵–10⁷ photons s⁻¹ cm⁻² sr⁻¹). Used as the qualitative "seeing-is-believing" companion to the quantitative bar.

7. **Small-multiples / image grid (matrix of micrographs).**
   - *Where:* Fig 4c-e (rows = PBS/MK16/MC3; columns = Nuclei/tdTomato/Neuron/Astrocyte/Merged), Fig 6c (rows = day, columns = treatment), Fig 5a.
   - *Analytical point:* faceted comparison holding one variable per axis. Fixed row=treatment, column=channel/marker lets the eye run down a column to compare treatments for one stain, or across a row to build the merged-overlay logic. Scale bar in only one panel; channels share it.

8. **Confocal/immunofluorescence multichannel overlay (colored-channel merge).**
   - *Where:* Fig 4b,c-e, Fig 5a — DAPI(blue)/tdTomato(red)/Map2-neuron(green)/GFAP-astrocyte(magenta)/merge.
   - *Analytical point:* colocalization = cell-type-specific delivery. Fixed channel→color mapping (nuclei always blue, target always red) reused across every micrograph so the reader learns the code once.

9. **Schematic / mechanism diagram (biological cartoon).**
   - *Where:* Fig 1a (formulation + 3 BBB-crossing routes + injection), Fig 3h,l (transwell assay; γ-secretase/caveolae mechanism), Fig 4a (LoxP-Stop-tdTomato genetics), Fig 5b,d (CPP behavioral protocol; ex-vivo human-tissue workflow), Fig 6a (treatment-regimen timeline).
   - *Analytical point:* orient the reader to the experimental logic BEFORE the data. Consistent BioRender-style flat vector cells with the same palette as the data figures.

10. **Chemical-structure panels (skeletal formulae, combinatorial R-group tables).**
    - *Where:* Fig 1b (6 lipid classes with shared R= tail library), Fig 1c (synthesis routes), Fig 3c (MK13-MK16 tail variants).
    - *Analytical point:* structure-activity — the R-group table sits directly beside the bar chart that ranks those same structures (Fig 3c next to 3d), so structure→function is a single eye-movement.

11. **Timeline / experimental-regimen bar (horizontal axis = study day, event markers).**
    - *Where:* Fig 6a (Day 0 tumour → Day 10-16 injections → imaging every 3 days).
    - *Analytical point:* when-what-happened; anchors the longitudinal Fig 6b/c/d.

**Notably ABSENT** (deliberate scope): no violin/raincloud/beeswarm-proper, no obs-vs-pred parity, no heatmap-with-dendrogram, no ROC/PR, no forest/tornado, no Sankey, no ridgeline, no waterfall, no slopegraph. The screen is shown as **ranked bars-with-dots**, not as a heatmap — a choice that keeps the fold-change axis literal. (For a future author: this exemplar teaches the *bar-with-dots + reference-normalization + IVIS-companion* idiom, not the ML-diagnostics idioms.)

---

## 2) MULTI-PANEL COMPOSITION (how panels tell one story)

- **One figure = one act of the argument.** Fig 1 = design (what we built). Fig 2 = screen (which one wins in cells + first in-vivo). Fig 3 = optimization (tune the winner) + mechanism. Fig 4 = functional proof (genetic reporter). Fig 5 = disease model 1 (addiction/CPP + human tissue). Fig 6 = disease model 2 (GBM efficacy + survival).
- **Screen figures use a 3×2 / 2×3 grid of near-identical bar panels** (Fig 2a-f), one lipid sub-library per panel, each self-normalized to MC3. Uniform y-axis scaling within the sweep (0-20) lets the reader compare peak heights *across* panels, not just within. Panel g (organs) and h (IVIS) and i (organ quant) close the figure by moving from cells → whole animal.
- **Panel-to-panel logic is "quantify then visualize then mechanize":** a bar/quant panel (e.g., 3a,d,f) is immediately paired with its IVIS image (3b,e,k) or its flow plot (3g), and then with a mechanism cartoon (3h,l). Number → picture → why.
- **Structure-beside-data pairing:** Fig 3c (chemical R-group ladder) sits immediately left of Fig 3d (the bar chart ranking those exact structures) — reading left-to-right *is* the structure-activity relationship.
- **Image grids share axes/labels, not repeat them:** in Fig 4c-e and Fig 6c, column headers and row labels appear once along the top/left edge; individual tiles are unlabeled. Scale bar lives in a single corner tile and is stated to apply to all.
- **Insets / shared legends:** each figure carries ONE legend key (color→treatment) placed to the right of the first panel that needs it and governing every panel in that figure (e.g., the PBS/MK16/MC3 swatch key in Fig 4, the Liver/Spleen/Heart/Kidney/Lung key in Fig 2i). Colorbars for IVIS are shared vertically beside the image cluster.

---

## 3) COLOR-THEME PRACTICE

- **A single restrained palette across the whole paper.** Bars are rendered in a muted blue (in-vitro/screen, Fig 2a-f) and a muted salmon/red (in-vivo organ context, Fig 2g) — cool-for-cells, warm-for-tissue is used consistently.
- **Fixed entity→color mapping, reused in every figure.** The three canonical arms carry stable colors throughout: **PBS = light grey, MK16 (lead) = blue, MC3 (benchmark) = salmon/red.** This recurs identically in Fig 4f-i legend, Fig 5c,e, Fig 6b-d. A reader learns "blue = our winner, red = the standard, grey = vehicle" once and it holds paper-wide. Dose variants of the same agent are shown as a lighter/darker tint of that agent's hue (MK16 1× vs 3× in Fig 4i).
- **Fixed channel→color in micrographs:** nuclei/DAPI = blue, target reporter (tdTomato/ΔFOSB/GFP) = red/magenta, neuron marker = green, astrocyte = magenta — identical across Fig 4 and Fig 5, so overlays are legible without re-reading the key.
- **Accent for the key finding:** the lead formulation's bar is the tallest AND in the "hero" hue (blue), so the reader's eye lands on it first; the winner in each screen panel (LD10, DS11, CD6, TD5, MK6/MK16) visibly towers over its neighbors and over the normalized MC3=1 reference.
- **Perceptual ramp for intensity images:** IVIS/IFCM use a blue→cyan→green→yellow→red intensity ramp with a numbered colorbar. (This jet-style ramp is the journal convention for photon-count maps; it is *not* colorblind-optimal, but it is paired with a numeric colorbar and with quantitative bars so meaning is never color-only.)
- **Colorblind safety:** the blue/salmon/grey trio is reasonably deutan-safe (differs in lightness, not just hue), and — critically — **color is never the sole channel**: bars are separated on the x-axis, significance is text, and every color-coded arm also has a text legend. The rainbow IVIS ramp is the one non-CB-safe element, mitigated by the adjacent numeric scale.

---

## 4) PUBLICATION-READY CRAFT

- **Typography:** small, uniform sans-serif (Helvetica/Arial family) at Nature's ~7 pt axis/tick size, ~8 pt panel bold letters (a, b, c…) in the top-left of each panel. Consistent across every figure.
- **Axis titles are vertical on y, spelled out with units** ("Normalized luminescence intensity", "Luminescence intensity (×10⁶ p/s/cm²/sr)", "tdTomato positive (%)", "Survival rates (%)"). Units carried into the axis label via scientific notation multipliers rather than cluttering ticks.
- **Overlap avoidance:** x-tick labels for long screen series (LD1…LD13, MK1…MK16) are kept horizontal but short (codes, not names); the many-category axes stay readable because labels are terse alphanumeric IDs. Where categories are cell types (Neuron/Astrocyte/…), labels sit horizontally under each cluster.
- **Direct labeling vs legend:** significance is direct-labeled on the plot (P-values printed above bracket lines); treatment identity uses a compact swatch legend (one per figure). Micrograph channels are direct-labeled as column headers, not legended.
- **Axis treatment:** linear axes with clean 0-anchored ranges; uniform max within a screen sweep (0-20) for cross-panel comparability; time axes in real study days. No log axes needed here (fold-changes shown by normalization instead). Y-axes broken only implicitly via the ×10ⁿ multiplier.
- **Annotation style:** significance brackets are thin horizontal lines spanning the two compared bars with the exact P-value ("****P < 0.0001", "*P = 0.0277", "n.s.") printed above — **exact P reported, not just star tiers**, which is best practice. "n.s." is written out where non-significant (Fig 3f oligodendrocyte/NSC, Fig 4i).
- **Whitespace / density:** dense panels (the 6-panel screen, the multi-cell-type clustered bars) stay readable by (i) generous inter-cluster gaps, (ii) thin bars, (iii) offloading the raw replicate points as small open/filled dots rather than more bars, and (iv) one shared legend. At 85 mm column width the alphanumeric x-labels and 7-pt axis text remain legible.
- **Scale bars** stated once per micrograph set with the value in the caption ("Scale bar, 1 mm" / "50 µm" / "100 µm"), placed unobtrusively in a corner tile.

---

## 5) STATISTICAL-PRESENTATION STYLES (what's shown ON the figure)

- **n is stated in the caption, not the panel** ("n = 3 biologically independent samples", "n = 9 mice", "n = 19/20 mice"), and — crucially — **the individual replicate points are plotted on every bar**, so the reader sees the actual n and its spread visually.
- **Uncertainty = mean ± s.d.**, drawn as symmetric error whiskers on each bar/timepoint. The caption names it explicitly ("Data are presented as mean ± s.d."). s.d. (not s.e.m.) is used, which is the more honest spread choice.
- **Effect size is shown by the height ratio against a normalized reference** (MC3 = 1.0): the reader reads "14.4-fold", "7.4-fold", "twofold" directly as bar-height multiples. This is the paper's signature move — effect size is *geometric on the axis*, not buried in text.
- **Significance:** exact P-values printed above comparison brackets, with the test named in the caption (one-way ANOVA + Dunnett's multiple-comparisons for multi-group vs a control; two-way ANOVA + Šidák/Fisher's LSD for two-factor; two-tailed Student's t for pairwise; log-rank Mantel-Cox for survival). Star-tier key given once ("*P<0.05, **P<0.01, ***P<0.001, ****P<0.0001") and "n.s." shown explicitly.
- **Flow % as on-plot text:** in the pseudocolor flow panels (Fig 3g) the gated % positive is printed inside each plot, tying the density picture to the summary bar.
- **The bar-with-dots + reference-normalization + exact-P bracket** is the reusable statistical-presentation unit a future author should copy for any screen/dose-response comparison.

---

## REUSABLE STYLE MENU (pick-list for a future author)

| # | Style | Use it when you need to… |
|---|-------|--------------------------|
| A | Bar + s.d. whisker + overlaid n replicate dots, normalized to a reference bar=1 | Rank many candidates / show fold-change vs standard of care |
| B | Clustered bars (condition × category), tinted dose variants | Two-factor comparison (formulation × cell type/organ) |
| C | Multi-arm line curves, mean±s.d. per timepoint | Longitudinal divergence between treatment arms |
| D | Kaplan-Meier step curve + log-rank | Time-to-event / survival |
| E | Flow pseudocolor density (SSC vs marker) + on-plot % | Show the primary gate behind a % bar |
| F | IVIS/anatomical heat-overlay + shared numeric colorbar | Spatial signal where it physically occurs |
| G | Small-multiples image grid (row=treatment, col=channel/day) | Faceted qualitative comparison; one shared scale bar |
| H | Multichannel IF overlay, fixed channel→color code | Colocalization / cell-type specificity |
| I | Mechanism/protocol schematic in the data palette | Orient reader to experimental logic before data |
| J | Chemical R-group ladder placed beside its ranking bar | Structure-activity in one eye-movement |

**Governing principles to carry over:** one palette paper-wide; every entity a fixed color+used-everywhere; hero finding in the accent hue and tallest bar; normalize to the benchmark so effect size is read off the axis; always plot the raw points at low n; exact P-values on brackets with the test named in the caption; number → picture → mechanism panel ordering.
