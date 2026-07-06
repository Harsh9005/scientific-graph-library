# Exemplar Mining — Nature Communications 2025

**Source:** Xue, Hou, Zhong et al. "LNP-RNA-mediated antigen presentation leverages SARS-CoV-2-specific immunity for cancer treatment." *Nat Commun* 16:2198 (2025). DOI 10.1038/s41467-025-57149-2.
**Domain:** Nanomedicine / mRNA-LNP / cancer immunotherapy. Bench-heavy (screening, flow cytometry, in-vivo tumor, cytokine panels).
**Why mined:** High-density, multi-panel Nature-family figures where every panel earns its place. A model for how a bench paper composes a large screening library + mechanism + in-vivo efficacy into readable print figures.

---

## 1. DISTINCT GRAPH / CHART STYLES (the reusable catalog)

Each entry: **type → what it plots → the exact analytical point it makes.** Pick from these by intent.

### G1 — Large-N screening bar array (the "library screen")
- **Type:** Single-row vertical bar chart with ~50 categories (AA1…AA50 + 2 benchmark controls ALC-0315, SM-102), y = luminescence intensity (×10⁵ / ×10⁶ / ×10⁷).
- **Where:** Fig 2a, 2b (in-vitro cell lines); Fig 4a (in-vivo B16F10).
- **Point:** Rank the entire candidate library on one axis so the eye finds the winner(s) instantly against fixed benchmarks anchored at the far right. This is the canonical **"screen the whole panel, mark the hit"** chart. Benchmarks always sit last so every bar is read relative to them.
- **Reusable for:** any large formulation / compound / condition library where you must show the full distribution AND pick the lead. Dissolution-formulation screens, excipient panels, PINN-hyperparameter sweeps.

### G2 — Grouped/highlighted subset bar with pairwise stats (the "finalists")
- **Type:** Vertical bars, ~12 selected candidates + benchmarks, mean ± SD, individual data points overlaid, bracketed p-value annotations between specific pairs.
- **Where:** Fig 2c (normalized luminescence, lead subset).
- **Point:** Zoom from the full screen (G1) to the shortlist and now attach statistics only to the comparisons that matter (lead-vs-benchmark). G1 finds candidates; G2 proves the lead.
- **Note the composition logic:** G1 → G2 is a **funnel pair** (wide screen, then statistically-tested finalists). Reuse this two-step wherever a screen precedes a claim.

### G3 — Paired grouped bar, two-condition contrast (the "treatment vs control readout")
- **Type:** Grouped bars, x = treatment groups (e.g., SM-102 vs AA2), two colored bars per group (CE control epitope vs SE spike epitope), mean ± SD + dot overlay, per-pair p-values.
- **Where:** Fig 3b–e (AIM assay, %CD137⁺/CD69⁺ T cells); Fig 4g,h; Fig 5e,g cytokine bars.
- **Point:** Show the **effect of the intended stimulus over its matched control within each formulation**, side by side, so the reader sees both the absolute response and the control-subtracted specificity. The two-bar-per-group grammar is the workhorse for "specific vs nonspecific."
- **Small-multiples variant:** Fig 3 repeats this same G3 panel across 6 markers (CD137, CD69, CD69⁺CD137⁺, IFN-γ, TNF-α, GzmB) in a faceted row — identical axes/colors, one marker each. See §2 small-multiples.

### G4 — Grouped bar, 4-arm treatment comparison (the "regimen comparison")
- **Type:** Vertical bars, 4 fixed treatment arms (PBS / mSE-SCT / sCE-SCT / sSE-SCT) repeated for many cytokines, mean ± SD, stacked bracket p-values.
- **Where:** Fig 5e (tumor cytokines: IL-1α, IL-6, IL-7, IL-12p70, IL-15, IFN-γ, TNF-α, CXCL9), Fig 5g (blood, same panel).
- **Point:** Hold the arm set constant and sweep the readout (each cytokine = its own mini-panel) so cross-cytokine patterns emerge while every panel is directly comparable. Fixed arm colors carry the identity across ~8 sub-panels.

### G5 — Heatmap with signed diverging color (the "multiplex fold-change matrix")
- **Type:** Rows = analytes (~24 cytokines/chemokines), columns = treatment arms (mSE/sCE/sSE), cell color = log₂(fold change vs PBS) on a **blue↔white↔red diverging scale** (−4 … +8).
- **Where:** Fig 5d (tumor), Fig 5f (blood).
- **Point:** Compress a 24-analyte × 3-arm multiplex panel into one glance that shows **which arm turns on which analyte and by how much**, with sign encoded by hue. The paired heatmap (tumor vs blood) lets the reader compare compartments. Selected rows are then "promoted" to G4 bar panels for the analytes with p-values — **heatmap for the landscape, bars for the proof.**
- **Reusable for:** any wide multiplex (Luminex, transcript panels, multi-timepoint kinetics). Diverging scale is mandatory when the quantity is a signed fold-change.

### G6 — Flow-cytometry dot/density plots as raw-data insets (the "gate evidence")
- **Type:** 2-D scatter/density (SSC-A vs marker, or H-2Kb vs β2m) with quadrant %-gates printed in-plot, shown as a time series (24h/48h/72h) or condition pair (PBS vs treatment).
- **Where:** Fig 4c (mSE-SCT vs sSE-SCT over 3 timepoints), Fig 4d (PBS vs sOP-SCT), Fig 6h–j (human samples).
- **Point:** Provide the **primary cytometry evidence** behind a summarizing bar chart placed immediately adjacent — the dot plot shows the gate is real, the bar quantifies it across replicates. Always pair raw-plot + summary-bar.

### G7 — Tumor-growth spaghetti / mean-trajectory line (the "efficacy curve")
- **Type:** Line chart, x = days post-inoculation, y = tumor volume (mm³), one line per arm, mean ± SD error bars, arm-colored.
- **Where:** Fig 5b, Fig 6b, Fig 6e.
- **Point:** Show divergence of tumor burden over time between arms — the core efficacy readout. Error bars grow with time (biological spread), which is expected and honest.

### G8 — Kaplan–Meier survival step curve (the "survival benefit")
- **Type:** Step function, x = days post-inoculation, y = percent survival, one step-line per arm, arm-colored, log-rank (Mantel–Cox) p-values stacked in a corner.
- **Where:** Fig 5c, Fig 6c, Fig 6f.
- **Point:** Standard survival endpoint. Always paired directly to the right of its matching tumor-growth curve (G7) — **G7 (burden) + G8 (survival)** is a fixed couplet in this paper. Reuse the couplet for any longitudinal efficacy claim.

### G9 — Schematic / timeline strip (the "experimental design")
- **Type:** Icon-based workflow with a horizontal day-axis timeline (Prime → Boost → Sacrifice / Tumor inoculation → Treatment), BioRender-style illustration.
- **Where:** Fig 3a, Fig 4b (construct maps), Fig 5a, Fig 6a/d/g.
- **Point:** Anchor every results figure with a design schematic as **panel a**, so dosing/timing is unambiguous before any data. Construct diagrams (5′-CAP–UTR–Replicase–SCT–UTR–AAA; SCT domain cassette) double as "what was built."

### G10 — In-vivo bioluminescence image grid (the "spatial readout")
- **Type:** Small-multiples grid of IVIS mouse images, rows = formulation (AA2/ALC-0315/SM-102), columns = timepoint (6h/24h), shared radiance colorbar (p/sec/cm²/sr).
- **Where:** Fig 2d.
- **Point:** Show the actual spatial/biodistribution signal with one shared intensity scale so images are quantitatively comparable across formulation and time. Always carry the calibrated colorbar.

### G11 — Chemical-structure + R-group library plate (the "design space")
- **Type:** Skeletal structures of the three head-group scaffolds (AA1–AA26, AA27–AA45, AA46–AA50) beside a boxed R-group/tails legend (R1…R9) and a reaction-scheme row.
- **Where:** Fig 1b (structures + tails), Fig 1c (synthetic routes).
- **Point:** Define the combinatorial design space compactly — one scaffold column + one tails column communicates a 50-member library without 50 drawings. The "menu" grammar for any structure-activity library.

**Style count in this paper: 11 distinct graph styles** (G1 large-N screen bar, G2 finalist bar+stats, G3 two-condition grouped bar, G4 multi-arm grouped bar, G5 diverging heatmap, G6 flow dot-plot inset, G7 tumor-growth line, G8 KM survival, G9 schematic/timeline, G10 IVIS image grid, G11 structure/scheme plate).

---

## 2. MULTI-PANEL COMPOSITION

- **Panel `a` is always orientation:** either a mechanism schematic or an experimental timeline (G9). The reader learns the design before seeing a single bar. Every main figure obeys this.
- **Funnel logic within a figure:** wide screen (G1) → shortlist with stats (G2) → mechanism/readout (G3/G6). Fig 2 is the archetype: 2a/2b screen two cell lines, 2c narrows to lead + stats, 2d shows spatial signal, 2e shows the antibody consequence.
- **Fixed couplets:** tumor-growth line (G7) immediately followed by its KM survival (G8), left-to-right, same arm colors — Fig 5b/c, 6b/c, 6e/f. And raw flow plot (G6) immediately beside its quantifying bar (G3) — Fig 4c, 4d.
- **Landscape-then-proof:** the wide diverging heatmap (G5, Fig 5d/f) gives the whole analyte landscape; a curated row of bar panels (G4, Fig 5e/g) then re-plots only the analytes carrying significance. The heatmap and bars share the same arm color key.
- **Small-multiples / faceted rows:** Fig 3b–e and Fig 5h–l are rows of identical-grammar panels differing only in the readout (one T-cell marker or one immune-cell population each). Identical y-scaling conventions and identical colors make the row scannable as a single comparison. Fig 5 packs cDC1/cDC2/Mφ/CD4/CD8, then activation markers, into ~12 aligned sub-panels.
- **Insets:** quadrant-% printed inside flow plots (G6); radiance colorbar embedded in the IVIS grid (G10); p-value brackets sit inside the plot area, not in captions.
- **Shared legends:** one arm/color legend serves an entire figure block (e.g., the PBS/mSE/sCE/sSE key above Fig 5d governs 5d–5l). Legends are declared once per figure, reused across all its panels.

---

## 3. COLOR-THEME PRACTICE

- **Consistent restrained palette across the whole paper.** Not a rainbow. A small set of hues reused with fixed meaning.
- **Fixed entity→color mapping (the key discipline):** each treatment arm keeps ONE color everywhere it appears.
  - PBS / negative → **grey** (always the baseline color).
  - mSE-SCT (mRNA) → **blue**.
  - sCE-SCT (saRNA control epitope) → **green**.
  - sSE-SCT (saRNA spike epitope, the hero arm) → **red** — the key finding gets the warm accent color, consistently.
  - In the CE-vs-SE two-bar grammar (Fig 3): CE control → **light blue/teal**, SE spike → **dark red**. Same two colors in every one of the 6 faceted marker panels.
- **Accent for the winner:** red is reserved for the best-performing / spike-specific arm throughout, so the eye is trained early ("red = the thing that works").
- **Screen bars (G1/G2):** a single sky-blue fill for all library bars (2a/2b/4a) or a single salmon fill (2c) — uniform within a screen so height alone encodes the message; benchmarks share the same fill (not recolored) to avoid biasing the eye.
- **Heatmap:** blue–white–red **diverging** scale for signed log₂ fold-change (Fig 5d/f), matched between tumor and blood panels.
- **IVIS:** rainbow radiance LUT (blue→red) but only inside the calibrated imaging colorbar — never for categorical data.
- **Colorblind note:** the grey/blue/green/red arm scheme is *mostly* CVD-distinguishable via the grey anchor and value labels, but blue-vs-green and red-vs-green are the weak pairs; direct labeling + fixed left-to-right arm order compensates. A stricter reuse should swap green→orange for full CVD-safety.

---

## 4. PUBLICATION-READY CRAFT (print at ~85 mm column)

- **Category-axis rotation:** the 50-member screen (G1) uses vertical/angled x-tick labels (AA1…AA50) in a small sans-serif so all 52 categories fit one row without overlap.
- **Direct labeling over legends where it fits:** timepoint columns (6h/24h/72h) and arm names sit directly above panels; flow-gate %-values printed on the plot. Legends only for color-coded multi-arm panels.
- **p-value brackets, not asterisk soup:** exact p-values are printed on horizontal brackets spanning the compared bars (e.g., "*P = 0.012", "****P < 0.0001"), with the significance code defined once in the caption. Brackets are stacked (short brackets low, long spanning bracket high) to avoid crossing.
- **Error bars = mean ± SD**, stated in every caption, with **individual data points overlaid** on bars (dot-on-bar) so n and spread are visible — reviewers can count replicates.
- **n is always stated in caption** ("Data in (e) are from n = 6 biologically independent samples"), and the test named ("one-way ANOVA followed by Dunnett's"; "two-tailed Student's t-test"; "log-rank (Mantel–Cox)").
- **Shared axes across small-multiples** keep the faceted rows honest and scannable; y-units carried once per row.
- **Whitespace / density management:** dense figures (Fig 5 has 12 panels) stay readable because (i) one shared legend, (ii) fixed arm colors, (iii) heatmap absorbs the wide landscape so bars can be few and large, (iv) schematic panel `a` offloads all design text out of the data panels.
- **Colorbars are calibrated and labeled** (radiance units; log₂ FC range printed on the scale).
- **Typography:** clean sans-serif throughout, panel letters bold lowercase (a, b, c…) top-left, axis titles concise with units in parentheses.

---

## 5. STATISTICAL-PRESENTATION STYLES (what appears ON the figure)

- **Effect size shown as the bar height itself**, with fold-change called out in text and encoded by color-magnitude in the heatmap (log₂ FC). The screen makes effect size visual (winner is ~2–5× taller).
- **Uncertainty = mean ± SD error bars + overlaid individual dots** (dot-on-bar); survival uncertainty is implicit in the step curve; growth curves carry ± SD whiskers per timepoint.
- **Significance = exact p-values on brackets** (not just stars), plus a caption code (*P<0.05, **P<0.01, ***P<0.001, ****P<0.0001) and explicit "n.s." labels when not significant (honest reporting of null pairs, e.g., Fig 4e n.s. P = 0.056; Fig 5i n.s. P = 0.0707).
- **Test named per panel** in caption (ANOVA+Dunnett for multi-arm; Student's t for pairwise; Mantel–Cox for survival).
- **n reported per panel** and "biologically independent samples" specified.
- **Normalization stated** where used ("intensity normalized to the ALC-0315 group," Fig 2c) so cross-panel numbers are interpretable.
- **Only meaningful comparisons are bracketed** — they do not bracket every pair, only lead-vs-benchmark or SE-vs-CE, keeping the figure uncluttered while still rigorous.

---

## QUICK PICKER (for a future author)

| Intent | Use style |
|---|---|
| Rank a whole candidate library, mark the hit vs benchmarks | G1 large-N screen bar |
| Prove the lead with stats after screening | G2 finalist bar + p-brackets |
| Specific vs control readout within each formulation | G3 two-condition grouped bar |
| Compare fixed treatment arms across many readouts | G4 multi-arm grouped bar (small-multiples) |
| Whole multiplex landscape (many analytes × few arms) | G5 diverging log₂FC heatmap |
| Show the raw gate behind a summary number | G6 flow dot-plot inset + adjacent bar |
| Longitudinal efficacy | G7 tumor-growth line + G8 KM survival (couplet) |
| Orient the reader to design/dosing | G9 schematic + day-axis timeline as panel a |
| Spatial / biodistribution signal | G10 IVIS image grid + calibrated colorbar |
| Combinatorial design space (SAR) | G11 scaffold + R-group menu plate |

**One-line doctrine distilled:** *Panel `a` = design schematic; funnel wide-screen → statistically-tested finalists; fix one color per arm and reuse it in every panel; reserve the warm accent for the winner; heatmap for the landscape, bars for the proof; pair every raw plot with its summary and every growth curve with its survival; print exact p-values on stacked brackets over dot-on-bar mean±SD.*
