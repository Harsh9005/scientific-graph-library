# Exemplar Graph-Style Library — *Nature Biotechnology* 2024 (Brief Communication)

**Source:** Wang, Wang, Xue et al. "Intravenous administration of blood–brain barrier-crossing conjugates facilitate biomacromolecule transport into central nervous system." *Nat. Biotechnol.* 43, 1783–1789 (2024). DOI 10.1038/s41587-024-02487-7.
**Format:** Brief Communication — only **2 main display items** (Fig 1, Fig 2), so figure real estate is scarce and every panel is load-bearing. Supplementary carries the overflow. This is the canonical *NBT* house style: mechanism schematic + chemistry up top, quantitative bar/dot panels below, all one coherent visual system.

---

## 1) DISTINCT GRAPH / CHART STYLES (the full variety used)

The paper is deliberately **restrained** — it does NOT chase chart-type novelty. It leans on ONE workhorse quantitative style, repeated with disciplined consistency, plus schematics and chemistry. This restraint is itself the lesson: a top-tier delivery/therapeutics paper communicates almost entirely through the **bar-plus-overlaid-raw-dots** idiom. Styles present:

1. **Bar chart with overlaid individual data points (dot-on-bar), mean ± s.d. error bars** — THE dominant idiom. Used in Fig 1b, 1c, 1d and Fig 2b, 2c, 2d, 2e, 2g, 2i, 2j. Bars are open/white or fill-coded by condition; every replicate is plotted as a solid dot on top of its bar so the reader sees n, spread, and any outlier directly. Analytical point: **per-condition magnitude + full transparency of the raw sample distribution at small n (n = 3)**. This is the single most reusable style in the paper.
   - *Variant — single open bars, one factor:* Fig 1b screens 13 candidate conjugates (BCC1–12 + free-Cy5 control) as open bars ranked implicitly by the biology, each with its 3 dots. Point: **screen/rank many candidates on one axis to justify lead selection (BCC10).**
   - *Variant — grouped bars, two-factor (cell type × treatment):* Fig 2c and 2d group bars by cell type (Microglia / Neuron / Astrocyte / BCEC) and color-code the three treatments (PBS grey, Chol-Oligo blue, BCC10-Oligo red) within each group. Point: **interaction readout — which cargo enriches in which cell type — read across and within groups.**
   - *Variant — dose–response bars:* Fig 2b (1 vs 25 mg/kg groups) and Fig 2e (PBS/ASO + 1/12.5/25/50 mg/kg BCC10-ASO). Point: **monotonic dose-dependence shown as an ascending/descending staircase of bars.**
   - *Variant — two-bar head-to-head:* Fig 1d and Fig 2g are minimal two-bar contrasts (treatment vs inhibitor / PBS vs treatment) with a single p-value bracket. Point: **one clean effect, one statistic, no clutter.**

2. **Chemical-structure grid / small-multiples of molecules** — Fig 1a lays out all 12 BCC–Cy5 conjugate structures in a **4×3 skeletal-formula grid**, each captioned (BCC1–Cy5 … BCC12–Cy5). Analytical point: **combinatorial library at a glance — structural variation is the independent variable that Fig 1b then screens.** This is the "small-multiples for chemical space" pattern.

3. **Reaction-scheme / conjugation schematic** — Fig 2a shows the click-chemistry conjugation (Oligo-N₃ + DBCO-BCC10 → BCC10-Oligo) with the product structure drawn out. Point: **define the exact molecular entity being tested before any data.**

4. **Biological / experimental-design schematic (BioRender-style flow illustration)** — Fig 2f (human brain-tissue resection → sectioning → coincubation workflow, drawn as an anatomical cartoon with arrows) and Fig 2h (SOD1^G93A ALS mouse → single-dose i.v. of PBS/ASO/Chol-ASO/BCC10-ASO → 72 h → tissue collection, drawn as an icon pipeline). Point: **make the assay logic and treatment arms legible without reading Methods; each arm's color is pre-registered here and reused in the adjacent quantitative panel.**

**Styles NOT used (and worth noting for the library, since a data-strength skill must know the *option space*):** no violin/raincloud, no box-and-whisker, no heatmap+dendrogram, no obs-vs-pred parity, no forest/tornado sensitivity, no Sankey/alluvial, no survival/KM (despite an ALS model — endpoint is molecular knockdown at 72 h, not survival), no ROC/PR, no ridgeline, no waterfall, no slopegraph. At n = 3 per group the authors correctly avoid distribution-shape plots (violin/box are misleading at n = 3) and instead **plot every point on a bar** — the honest choice at small n. (Confocal microscopy panels — CLSM, IF colocalization — live in Supplementary, not main.)

---

## 2) MULTI-PANEL COMPOSITION

**Universal story arc, top → bottom, left → right = "what it is → does it get in → does it work → is it safe":**

- **Fig 1 (design & characterization):** `a` = full chemical library (4×3 grid, spans full width, top) → `b` = brain-uptake screen of all 12 (wide bar panel, bottom-left, ~50% width) → `c` = mechanism test (γ-secretase/MK-0752 inhibition transwell, bottom-middle) → `d` = in-vivo mechanism confirmation (± nirogacestat, bottom-right). Logic: **library → winner → why it works in vitro → why it works in vivo.** Panels b/c/d share the same bar idiom and sit in a single bottom row so the eye scans the quantitative payoff left-to-right.

- **Fig 2 (efficacy):** a **4-row grid of 10 panels (a–j)**. Row 1: `a` conjugation scheme (full width). Row 2: `b` brain accumulation, `c`/`d` cell-type distribution at low/high dose. Row 3: `e` Malat1 dose–response, `f` human-tissue workflow schematic, `g` human-tissue knockdown result — schematic sits *immediately left of* the data it explains. Row 4: `h` ALS mouse design schematic, `i` Sod1 mRNA knockdown, `j` SOD1 protein (ELISA) — again **schematic-then-two-results**, mRNA then protein, the natural biological order. Logic: schematic panels are *inline* with their result panels (f→g, h→i,j) rather than banished to one corner — each design cartoon earns its place by directly setting up the bar chart beside it.

**Panel-to-panel devices:**
- **Shared color legend across a row:** Fig 2c/d reuse the identical PBS/Chol-Oligo/BCC10-Oligo legend; it is stated once and understood across both.
- **Dose pairing:** 2c (1 mg/kg) and 2d (25 mg/kg) are deliberately adjacent, same axes structure, so the reader diffs low vs high dose by eye.
- **mRNA→protein pairing:** 2i (mRNA) beside 2j (protein) closes the central-dogma loop for the same knockdown claim.
- No insets, no broken axes in main figures — density is managed by *splitting into more panels* rather than cramming.

---

## 3) COLOR-THEME PRACTICE

**One consistent, minimal palette across BOTH figures — high-restraint, near-monochrome-plus-accent:**

- **Fixed accent = red/crimson for the hero molecule (BCC10 / BCC10-Oligo / BCC10-ASO).** The lead conjugate is red in *every* panel it appears (Fig 1b–d dots, Fig 2b–e/i/j bars and dots). Red = "our winner / the key finding." This is textbook accent-color discipline: the ONE thing you want remembered is the ONE saturated color.
- **Fixed comparator colors, reused everywhere:** **grey = PBS/control**, **blue = Chol-Oligo/Chol-ASO (the prior-art benchmark)**, **red = BCC10 (new).** These three map 1:1 to entities and are held constant across Fig 2c, 2d, 2i, 2j — a reader learns the code once and reads all four panels fluently. Free-Cy5 / free-oligo / free-ASO controls sit in black/grey.
- **Open (white-fill, black-outline) bars** used when a panel shows only ONE factor and color would be redundant (Fig 1b, 1c screen bars) — dots still carry the red accent. Color is *spent only where it disambiguates.*
- **Palette is effectively colorblind-safe** because it relies on **grey / blue / red** (a blue–red axis is deuteranope-distinguishable) AND never asks color to work alone — position (which bar) + direct group labels carry the meaning, color is reinforcement.
- Schematics (2f, 2h) use muted anatomical/illustrative tones that *do not* compete with the saturated data-panel accents.

**Reusable rule:** assign each experimental entity a FIXED (color) at first appearance; give the hero the only warm/saturated hue; keep every control in neutral grey; never introduce a new color for an entity already colored elsewhere.

---

## 4) PUBLICATION-READY CRAFT (print at ~85 mm column / 100%)

- **Typography:** small, uniform sans-serif (Nature house ~5–7 pt on-figure). Axis titles sentence-case with units in parentheses on the axis (`%ID/g brain`, `Cy5⁺ cells (%)`, `Malat1 level (% PBS control)`, `SOD1 concentration (ng g⁻¹)`). Panel letters are bold lowercase (**a**, **b**…) at top-left of each panel — the Nature convention.
- **Direct labeling over legends where possible:** x-axis categories are written under each bar/group (BCC1-Cy5 … BCC12-Cy5; Microglia/Neuron/Astrocyte/BCEC; the dose ladder 1/12.5/25/50) — the reader never hunts a legend to know *what* a bar is. Legends are reserved only for the *treatment* dimension (the 3-color code) that repeats across grouped panels.
- **Rotated tick labels** on the crowded 13-bar screen (Fig 1b) and dose panels to avoid label collision without shrinking type.
- **Whitespace / density management:** the Brief-Communication length limit forces splitting into many small panels rather than overloading axes; each panel does exactly one comparison. No panel carries two y-axes.
- **Axis treatment:** all main panels use **linear axes** (values are % of injected dose or % of control, naturally bounded) — no log axes, no axis breaks, because the dynamic range is modest and honesty at small n is prioritized. y-axis starts at 0 so bar heights are truthful.
- **Annotation style for the winner:** the tall red BCC10 bar is left to speak for itself (position + color), with the significance bracket drawn *to* it — the eye lands on the accent bar and the p-value that certifies it.

---

## 5) STATISTICAL-PRESENTATION STYLES (on the figure itself)

- **Raw data always shown:** individual replicate dots overlaid on every bar — n is *countable directly* (n = 3 mice/group in most panels; n = 9 biological samples from 3 mice where pooled; n = 4 human samples). The dot cloud IS the uncertainty display.
- **Error bars = mean ± s.d.**, stated explicitly in every legend ("All data are presented as the mean ± s.d."). s.d. (not s.e.m.) is the honest wider interval — a rigor signal.
- **Exact p-values printed on the figure**, never bare asterisks: `P < 0.0001`, `P = 0.0220`, `P = 0.0003`, `P = 0.0013`, drawn with a horizontal **significance bracket** spanning the two compared bars. Non-significant contrasts are labeled **NS** (with the convention "Not significant (NS), P > 0.05" in the legend) rather than hidden.
- **Test named per panel in the legend:** "unpaired two-tailed Student's *t*-test" for two-group panels (1d, 2g); "one-way ANOVA with Tukey post hoc test" for multi-group panels (1b,c; 2b,c,d,e,i,j). The legend maps *which test to which panel* by letter — a reproducibility best-practice.
- **Effect size communicated in-text, anchored to the figure:** fold-changes ("220.5-fold higher," "66.0-fold and 7.3-fold," "78.1% reduction," "81.3% reduction," "44.2% reduction") are quoted in prose and *visually corroborated* by the towering red bar vs the flat grey/blue comparators — the figure and the number reinforce each other.
- **n and sample provenance disambiguated in the legend** (mice vs biological samples vs pooled replicates from N animals) — critical at small n so the reader knows whether dots are technical or biological.

---

## QUICK-PICK SUMMARY (for a future author)

| Need | Style to lift from this paper |
|---|---|
| Screen/rank many candidates → justify a lead | Open bars + raw dots, one row, one axis (Fig 1b) |
| Show a clean two-arm effect | Two bars + dots + one p-value bracket (Fig 1d, 2g) |
| Dose–response | Ascending bar ladder + dots (Fig 2e) |
| Two-factor (cell type × treatment) | Grouped bars, fixed 3-color treatment code (Fig 2c/d) |
| mRNA vs protein of same knockdown | Twin adjacent bar panels (Fig 2i, 2j) |
| Combinatorial chemical space | 4×3 skeletal-structure small-multiples (Fig 1a) |
| Define the molecular entity | Reaction/conjugation scheme (Fig 2a) |
| Make assay logic legible | Inline BioRender-style design schematic placed *beside* its result (Fig 2f→g, 2h→i,j) |
| Uncertainty at small n | Overlay every replicate dot; mean ± s.d.; NEVER violin/box at n=3 |
| Highlight the key finding | One saturated accent color (red) for the hero, held fixed across all panels; grey control, blue prior-art benchmark |
