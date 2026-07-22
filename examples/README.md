# Example gallery — 138 publication-quality figures

A comprehensive gallery of **138 distinct chart types and variants** across 10 categories, each generated from **synthetic (seeded, reproducible) data** by [`scripts/generate_gallery.py`](../scripts/generate_gallery.py) and built to the skill's publication-ready rules: one **colorblind-safe palette** (Okabe-Ito), sans-serif type, points shown on bars, exact stats, **sequential (never jet) colormaps**, clean de-spined axes. Each is exported as **PNG (300 dpi)** for preview and **PDF (vector)** for submission ([`png/`](png/), [`pdf/`](pdf/)).

Regenerate everything with `python3 scripts/generate_gallery.py` from the skill root (needs matplotlib, numpy, scipy, seaborn, networkx, pandas — no LaTeX). Every figure is checked by a deterministic text-overlap audit ([`_figure_qc.py`](../scripts/_figure_qc.py) — the F16 publication-ready gate) as it is built, and the run prints any collisions it finds.

> Data are synthetic and illustrative — the figures demonstrate **form and standards**, not real results.

| Category | Count | Category | Count |
|---|---|---|---|
| 📊 Distributions | 20 | 🔗 Correlation | 19 |
| 📶 Comparison | 17 | 🥧 Part-of-whole | 7 |
| 🕸️ Flow-Network | 9 | 📈 Time-series | 11 |
| 🔬 Scientific | 22 | 🧬 Omics-Cytometry | 8 |
| 🌐 3D-Fields | 12 | 🧩 Specialized | 13 |
**Jump to:** [📊 Distributions](#cat-distributions)  ·  [🔗 Correlation](#cat-correlation)  ·  [📶 Comparison](#cat-comparison)  ·  [🥧 Part-of-whole](#cat-part-of-whole)  ·  [🕸️ Flow-Network](#cat-flow-network)  ·  [📈 Time-series](#cat-time-series)  ·  [🔬 Scientific](#cat-scientific)  ·  [🧬 Omics-Cytometry](#cat-omics-cytometry)  ·  [🌐 3D-Fields](#cat-3d-fields)  ·  [🧩 Specialized](#cat-specialized)

> Thumbnails are laid out three across; click any figure to open it full size. Regenerate in a different colour palette with `python3 scripts/generate_gallery.py --palette npg` (`--list-palettes` for the choices; okabe_ito is the colorblind-safe default).


---

<a id="cat-distributions"></a>
## 📊 Distributions  ·  20 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A01_histogram.png"><img src="png/A01_histogram.png" width="100%"/></a><br/><b>A01. Histogram</b><br/><sub>single distribution</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A02_histogram_multiple.png"><img src="png/A02_histogram_multiple.png" width="100%"/></a><br/><b>A02. Histogram Multiple</b><br/><sub>compare two distributions</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A03_histogram_kde.png"><img src="png/A03_histogram_kde.png" width="100%"/></a><br/><b>A03. Histogram Kde</b><br/><sub>density overlay</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A04_hist2d.png"><img src="png/A04_hist2d.png" width="100%"/></a><br/><b>A04. Hist2D</b><br/><sub>joint density (binned)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A05_hexbin.png"><img src="png/A05_hexbin.png" width="100%"/></a><br/><b>A05. Hexbin</b><br/><sub>joint density (hex)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A06_kde.png"><img src="png/A06_kde.png" width="100%"/></a><br/><b>A06. Kde</b><br/><sub>smooth density</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A07_kde_multiple.png"><img src="png/A07_kde_multiple.png" width="100%"/></a><br/><b>A07. Kde Multiple</b><br/><sub>compare densities</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A08_ridgeline.png"><img src="png/A08_ridgeline.png" width="100%"/></a><br/><b>A08. Ridgeline</b><br/><sub>distribution over an ordered factor</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A09_box_grouped.png"><img src="png/A09_box_grouped.png" width="100%"/></a><br/><b>A09. Box Grouped</b><br/><sub>distribution summary + raw</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A10_box_notched.png"><img src="png/A10_box_notched.png" width="100%"/></a><br/><b>A10. Box Notched</b><br/><sub>median confidence via notch</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A11_violin.png"><img src="png/A11_violin.png" width="100%"/></a><br/><b>A11. Violin</b><br/><sub>distribution shape at large n</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A12_violin_split.png"><img src="png/A12_violin_split.png" width="100%"/></a><br/><b>A12. Violin Split</b><br/><sub>distribution by two factors</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A13_raincloud.png"><img src="png/A13_raincloud.png" width="100%"/></a><br/><b>A13. Raincloud</b><br/><sub>half-violin + strip</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A14_strip.png"><img src="png/A14_strip.png" width="100%"/></a><br/><b>A14. Strip</b><br/><sub>every point at small n</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A15_ecdf.png"><img src="png/A15_ecdf.png" width="100%"/></a><br/><b>A15. Ecdf</b><br/><sub>cumulative distribution</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A16_qq.png"><img src="png/A16_qq.png" width="100%"/></a><br/><b>A16. Qq</b><br/><sub>distributional check</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A17_sina.png"><img src="png/A17_sina.png" width="100%"/></a><br/><b>A17. Sina</b><br/><sub>violin + every raw point</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A18_paired_prepost.png"><img src="png/A18_paired_prepost.png" width="100%"/></a><br/><b>A18. Paired Prepost</b><br/><sub>paired before/after with subject lines</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/A19_broken_axis.png"><img src="png/A19_broken_axis.png" width="100%"/></a><br/><b>A19. Broken Axis</b><br/><sub>long tail without crushing the low group</sub></td>
<td width="33%" valign="top" align="center"><a href="png/A20_psd_percentiles.png"><img src="png/A20_psd_percentiles.png" width="100%"/></a><br/><b>A20. Psd Percentiles</b><br/><sub>size distribution with D10/D50/D90</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-correlation"></a>
## 🔗 Correlation  ·  19 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B01_scatter.png"><img src="png/B01_scatter.png" width="100%"/></a><br/><b>B01. Scatter</b><br/><sub>two continuous variables</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B02_scatter_groups.png"><img src="png/B02_scatter_groups.png" width="100%"/></a><br/><b>B02. Scatter Groups</b><br/><sub>grouped scatter</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B03_bubble.png"><img src="png/B03_bubble.png" width="100%"/></a><br/><b>B03. Bubble</b><br/><sub>third variable via size</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B04_regression.png"><img src="png/B04_regression.png" width="100%"/></a><br/><b>B04. Regression</b><br/><sub>linear fit with confidence band</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B05_marginal.png"><img src="png/B05_marginal.png" width="100%"/></a><br/><b>B05. Marginal</b><br/><sub>joint + marginal distributions</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B06_connected_scatter.png"><img src="png/B06_connected_scatter.png" width="100%"/></a><br/><b>B06. Connected Scatter</b><br/><sub>ordered trajectory in 2D</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B07_corr_heatmap.png"><img src="png/B07_corr_heatmap.png" width="100%"/></a><br/><b>B07. Corr Heatmap</b><br/><sub>pairwise correlations</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B08_clustermap.png"><img src="png/B08_clustermap.png" width="100%"/></a><br/><b>B08. Clustermap</b><br/><sub>reordered heatmap + dendrograms</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B09_density2d.png"><img src="png/B09_density2d.png" width="100%"/></a><br/><b>B09. Density2D</b><br/><sub>smooth joint density</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B10_pairplot.png"><img src="png/B10_pairplot.png" width="100%"/></a><br/><b>B10. Pairplot</b><br/><sub>all pairwise relationships</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B11_parity.png"><img src="png/B11_parity.png" width="100%"/></a><br/><b>B11. Parity</b><br/><sub>model calibration</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B12_bland_altman.png"><img src="png/B12_bland_altman.png" width="100%"/></a><br/><b>B12. Bland Altman</b><br/><sub>method agreement + LoA</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B13_residual.png"><img src="png/B13_residual.png" width="100%"/></a><br/><b>B13. Residual</b><br/><sub>diagnostic for a fit</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B14_loess.png"><img src="png/B14_loess.png" width="100%"/></a><br/><b>B14. Loess</b><br/><sub>nonparametric trend</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B15_corr_triangle.png"><img src="png/B15_corr_triangle.png" width="100%"/></a><br/><b>B15. Corr Triangle</b><br/><sub>lower-triangle correlogram + significance</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B16_parity_xy_err.png"><img src="png/B16_parity_xy_err.png" width="100%"/></a><br/><b>B16. Parity Xy Err</b><br/><sub>parity with x/y error + flagged outliers</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B17_grouped_regression.png"><img src="png/B17_grouped_regression.png" width="100%"/></a><br/><b>B17. Grouped Regression</b><br/><sub>pooled fit + per-group r (Simpson check)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/B18_distribution_overlap.png"><img src="png/B18_distribution_overlap.png" width="100%"/></a><br/><b>B18. Distribution Overlap</b><br/><sub>quantified overlap of two distributions</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/B19_mantel.png"><img src="png/B19_mantel.png" width="100%"/></a><br/><b>B19. Mantel</b><br/><sub>correlation heatmap + Mantel links</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-comparison"></a>
## 📶 Comparison  ·  17 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C01_bar.png"><img src="png/C01_bar.png" width="100%"/></a><br/><b>C01. Bar</b><br/><sub>categorical magnitude (zero-based)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C02_bar_horizontal.png"><img src="png/C02_bar_horizontal.png" width="100%"/></a><br/><b>C02. Bar Horizontal</b><br/><sub>ranked categories</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C03_grouped_bar.png"><img src="png/C03_grouped_bar.png" width="100%"/></a><br/><b>C03. Grouped Bar</b><br/><sub>two-factor comparison</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C04_stacked_bar.png"><img src="png/C04_stacked_bar.png" width="100%"/></a><br/><b>C04. Stacked Bar</b><br/><sub>composition per category</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C05_percent_stacked.png"><img src="png/C05_percent_stacked.png" width="100%"/></a><br/><b>C05. Percent Stacked</b><br/><sub>proportion per category</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C06_diverging_bar.png"><img src="png/C06_diverging_bar.png" width="100%"/></a><br/><b>C06. Diverging Bar</b><br/><sub>signed values around zero</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C07_dot_on_bar.png"><img src="png/C07_dot_on_bar.png" width="100%"/></a><br/><b>C07. Dot On Bar</b><br/><sub>bars never hide the sample (AP1)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C08_lollipop.png"><img src="png/C08_lollipop.png" width="100%"/></a><br/><b>C08. Lollipop</b><br/><sub>ranked values, low ink</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C09_cleveland_dumbbell.png"><img src="png/C09_cleveland_dumbbell.png" width="100%"/></a><br/><b>C09. Cleveland Dumbbell</b><br/><sub>paired change per category</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C10_radar.png"><img src="png/C10_radar.png" width="100%"/></a><br/><b>C10. Radar</b><br/><sub>multivariate profile</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C11_parallel_coords.png"><img src="png/C11_parallel_coords.png" width="100%"/></a><br/><b>C11. Parallel Coords</b><br/><sub>high-dim comparison</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C12_slope.png"><img src="png/C12_slope.png" width="100%"/></a><br/><b>C12. Slope</b><br/><sub>before/after ranking change</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C13_bump.png"><img src="png/C13_bump.png" width="100%"/></a><br/><b>C13. Bump</b><br/><sub>rank evolution over time</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C14_point_ci.png"><img src="png/C14_point_ci.png" width="100%"/></a><br/><b>C14. Point Ci</b><br/><sub>position-based estimates</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C15_grouped_dot_on_bar.png"><img src="png/C15_grouped_dot_on_bar.png" width="100%"/></a><br/><b>C15. Grouped Dot On Bar</b><br/><sub>two-factor bars that still show replicates</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/C16_dot_reference_zones.png"><img src="png/C16_dot_reference_zones.png" width="100%"/></a><br/><b>C16. Dot Reference Zones</b><br/><sub>estimates against banded thresholds</sub></td>
<td width="33%" valign="top" align="center"><a href="png/C17_cld_bars.png"><img src="png/C17_cld_bars.png" width="100%"/></a><br/><b>C17. Cld Bars</b><br/><sub>grouped bars with compact-letter significance</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-part-of-whole"></a>
## 🥧 Part-of-whole  ·  7 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/D01_stacked_area.png"><img src="png/D01_stacked_area.png" width="100%"/></a><br/><b>D01. Stacked Area</b><br/><sub>composition over time</sub></td>
<td width="33%" valign="top" align="center"><a href="png/D02_treemap.png"><img src="png/D02_treemap.png" width="100%"/></a><br/><b>D02. Treemap</b><br/><sub>hierarchical proportions</sub></td>
<td width="33%" valign="top" align="center"><a href="png/D03_sunburst.png"><img src="png/D03_sunburst.png" width="100%"/></a><br/><b>D03. Sunburst</b><br/><sub>nested hierarchy</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/D04_venn.png"><img src="png/D04_venn.png" width="100%"/></a><br/><b>D04. Venn</b><br/><sub>set overlap</sub></td>
<td width="33%" valign="top" align="center"><a href="png/D05_dendrogram.png"><img src="png/D05_dendrogram.png" width="100%"/></a><br/><b>D05. Dendrogram</b><br/><sub>hierarchical clustering</sub></td>
<td width="33%" valign="top" align="center"><a href="png/D06_waffle.png"><img src="png/D06_waffle.png" width="100%"/></a><br/><b>D06. Waffle</b><br/><sub>part-of-whole as unit squares</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/D07_mosaic.png"><img src="png/D07_mosaic.png" width="100%"/></a><br/><b>D07. Mosaic</b><br/><sub>two categorical variables</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-flow-network"></a>
## 🕸️ Flow-Network  ·  9 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/E01_sankey.png"><img src="png/E01_sankey.png" width="100%"/></a><br/><b>E01. Sankey</b><br/><sub>mass/flow balance</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E02_network.png"><img src="png/E02_network.png" width="100%"/></a><br/><b>E02. Network</b><br/><sub>nodes + edges, degree-scaled</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E03_arc.png"><img src="png/E03_arc.png" width="100%"/></a><br/><b>E03. Arc</b><br/><sub>network on a line</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/E04_bipartite.png"><img src="png/E04_bipartite.png" width="100%"/></a><br/><b>E04. Bipartite</b><br/><sub>two-set relationships</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E05_adjacency.png"><img src="png/E05_adjacency.png" width="100%"/></a><br/><b>E05. Adjacency</b><br/><sub>network as a matrix</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E06_alluvial.png"><img src="png/E06_alluvial.png" width="100%"/></a><br/><b>E06. Alluvial</b><br/><sub>multi-stage cohort flow with ribbons</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/E07_radial_dendrogram.png"><img src="png/E07_radial_dendrogram.png" width="100%"/></a><br/><b>E07. Radial Dendrogram</b><br/><sub>radial tree with value-scaled tips</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E08_network_communities.png"><img src="png/E08_network_communities.png" width="100%"/></a><br/><b>E08. Network Communities</b><br/><sub>communities + hub labels</sub></td>
<td width="33%" valign="top" align="center"><a href="png/E09_circos.png"><img src="png/E09_circos.png" width="100%"/></a><br/><b>E09. Circos</b><br/><sub>circular ideogram with ribbon links</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-time-series"></a>
## 📈 Time-series  ·  11 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/F01_line.png"><img src="png/F01_line.png" width="100%"/></a><br/><b>F01. Line</b><br/><sub>single series over time</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F02_multiline.png"><img src="png/F02_multiline.png" width="100%"/></a><br/><b>F02. Multiline</b><br/><sub>several series</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F03_line_ci.png"><img src="png/F03_line_ci.png" width="100%"/></a><br/><b>F03. Line Ci</b><br/><sub>trajectory + uncertainty</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/F04_area.png"><img src="png/F04_area.png" width="100%"/></a><br/><b>F04. Area</b><br/><sub>magnitude over time</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F05_streamgraph.png"><img src="png/F05_streamgraph.png" width="100%"/></a><br/><b>F05. Streamgraph</b><br/><sub>flowing composition</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F06_waterfall.png"><img src="png/F06_waterfall.png" width="100%"/></a><br/><b>F06. Waterfall</b><br/><sub>family of profiles</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/F07_candlestick.png"><img src="png/F07_candlestick.png" width="100%"/></a><br/><b>F07. Candlestick</b><br/><sub>financial time-series</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F08_spectrogram.png"><img src="png/F08_spectrogram.png" width="100%"/></a><br/><b>F08. Spectrogram</b><br/><sub>time–frequency (chirp)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F09_decomposition.png"><img src="png/F09_decomposition.png" width="100%"/></a><br/><b>F09. Decomposition</b><br/><sub>trend + seasonal + residual</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/F10_step.png"><img src="png/F10_step.png" width="100%"/></a><br/><b>F10. Step</b><br/><sub>piecewise-constant series</sub></td>
<td width="33%" valign="top" align="center"><a href="png/F11_offset_traces.png"><img src="png/F11_offset_traces.png" width="100%"/></a><br/><b>F11. Offset Traces</b><br/><sub>many traces via offset + scale bar</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-scientific"></a>
## 🔬 Scientific  ·  22 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G01_dose_response.png"><img src="png/G01_dose_response.png" width="100%"/></a><br/><b>G01. Dose Response</b><br/><sub>sigmoidal fit</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G02_kaplan_meier.png"><img src="png/G02_kaplan_meier.png" width="100%"/></a><br/><b>G02. Kaplan Meier</b><br/><sub>time-to-event</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G03_forest.png"><img src="png/G03_forest.png" width="100%"/></a><br/><b>G03. Forest</b><br/><sub>effect sizes across studies</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G04_pk_semilog.png"><img src="png/G04_pk_semilog.png" width="100%"/></a><br/><b>G04. Pk Semilog</b><br/><sub>geometric mean, log axis</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G05_dissolution.png"><img src="png/G05_dissolution.png" width="100%"/></a><br/><b>G05. Dissolution</b><br/><sub>profile + f2</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G06_roc.png"><img src="png/G06_roc.png" width="100%"/></a><br/><b>G06. Roc</b><br/><sub>classifier discrimination</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G07_pr_curve.png"><img src="png/G07_pr_curve.png" width="100%"/></a><br/><b>G07. Pr Curve</b><br/><sub>PR for imbalanced classes</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G08_calibration.png"><img src="png/G08_calibration.png" width="100%"/></a><br/><b>G08. Calibration</b><br/><sub>probability reliability</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G09_confusion.png"><img src="png/G09_confusion.png" width="100%"/></a><br/><b>G09. Confusion</b><br/><sub>per-class classifier behaviour</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G10_volcano.png"><img src="png/G10_volcano.png" width="100%"/></a><br/><b>G10. Volcano</b><br/><sub>differential expression</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G11_manhattan.png"><img src="png/G11_manhattan.png" width="100%"/></a><br/><b>G11. Manhattan</b><br/><sub>GWAS-style genome scan</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G12_ma_plot.png"><img src="png/G12_ma_plot.png" width="100%"/></a><br/><b>G12. Ma Plot</b><br/><sub>intensity-dependent ratio</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G13_tornado.png"><img src="png/G13_tornado.png" width="100%"/></a><br/><b>G13. Tornado</b><br/><sub>ranked parameter influence</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G14_scree_pca.png"><img src="png/G14_scree_pca.png" width="100%"/></a><br/><b>G14. Scree Pca</b><br/><sub>rank + structure</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G15_biplot.png"><img src="png/G15_biplot.png" width="100%"/></a><br/><b>G15. Biplot</b><br/><sub>scores + loadings</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G16_embedding.png"><img src="png/G16_embedding.png" width="100%"/></a><br/><b>G16. Embedding</b><br/><sub>nonlinear low-dim embedding</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G17_stem.png"><img src="png/G17_stem.png" width="100%"/></a><br/><b>G17. Stem</b><br/><sub>discrete/sparse coefficients</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G18_bifurcation.png"><img src="png/G18_bifurcation.png" width="100%"/></a><br/><b>G18. Bifurcation</b><br/><sub>route to chaos (logistic map)</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G19_gci.png"><img src="png/G19_gci.png" width="100%"/></a><br/><b>G19. Gci</b><br/><sub>mesh-independence / order</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G20_control_chart.png"><img src="png/G20_control_chart.png" width="100%"/></a><br/><b>G20. Control Chart</b><br/><sub>process monitoring ±3σ</sub></td>
<td width="33%" valign="top" align="center"><a href="png/G21_annotated_spectrum.png"><img src="png/G21_annotated_spectrum.png" width="100%"/></a><br/><b>G21. Annotated Spectrum</b><br/><sub>spectrum with assigned bands</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/G22_swimmer.png"><img src="png/G22_swimmer.png" width="100%"/></a><br/><b>G22. Swimmer</b><br/><sub>per-subject response timeline (oncology)</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-omics-cytometry"></a>
## 🧬 Omics-Cytometry  ·  8 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/J01_embedding_feature_pair.png"><img src="png/J01_embedding_feature_pair.png" width="100%"/></a><br/><b>J01. Embedding Feature Pair</b><br/><sub>clusters + same embedding by feature</sub></td>
<td width="33%" valign="top" align="center"><a href="png/J02_dotplot_matrix.png"><img src="png/J02_dotplot_matrix.png" width="100%"/></a><br/><b>J02. Dotplot Matrix</b><br/><sub>two statistics at once (size + colour)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/J03_stacked_violin.png"><img src="png/J03_stacked_violin.png" width="100%"/></a><br/><b>J03. Stacked Violin</b><br/><sub>per-gene distributions across groups</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/J04_enrichment_dotplot.png"><img src="png/J04_enrichment_dotplot.png" width="100%"/></a><br/><b>J04. Enrichment Dotplot</b><br/><sub>ratio, count and FDR in one panel</sub></td>
<td width="33%" valign="top" align="center"><a href="png/J05_gsea_running.png"><img src="png/J05_gsea_running.png" width="100%"/></a><br/><b>J05. Gsea Running</b><br/><sub>running enrichment + rank ticks</sub></td>
<td width="33%" valign="top" align="center"><a href="png/J06_heatmap_tracks.png"><img src="png/J06_heatmap_tracks.png" width="100%"/></a><br/><b>J06. Heatmap Tracks</b><br/><sub>matrix + categorical sample tracks</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/J07_flow_gating.png"><img src="png/J07_flow_gating.png" width="100%"/></a><br/><b>J07. Flow Gating</b><br/><sub>sequential gating strategy with % kept</sub></td>
<td width="33%" valign="top" align="center"><a href="png/J08_pca_ellipses.png"><img src="png/J08_pca_ellipses.png" width="100%"/></a><br/><b>J08. Pca Ellipses</b><br/><sub>PCA scores + group confidence ellipses</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-3d-fields"></a>
## 🌐 3D-Fields  ·  12 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/H01_surface3d.png"><img src="png/H01_surface3d.png" width="100%"/></a><br/><b>H01. Surface3D</b><br/><sub>solution field u(x,t)</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H02_wireframe.png"><img src="png/H02_wireframe.png" width="100%"/></a><br/><b>H02. Wireframe</b><br/><sub>surface as mesh</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H03_scatter3d.png"><img src="png/H03_scatter3d.png" width="100%"/></a><br/><b>H03. Scatter3D</b><br/><sub>three continuous variables</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/H04_contour.png"><img src="png/H04_contour.png" width="100%"/></a><br/><b>H04. Contour</b><br/><sub>iso-lines of a field</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H05_contourf.png"><img src="png/H05_contourf.png" width="100%"/></a><br/><b>H05. Contourf</b><br/><sub>field with colorbar</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H06_field_heatmap.png"><img src="png/H06_field_heatmap.png" width="100%"/></a><br/><b>H06. Field Heatmap</b><br/><sub>2D field, viridis (never jet)</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/H07_quiver.png"><img src="png/H07_quiver.png" width="100%"/></a><br/><b>H07. Quiver</b><br/><sub>vector field arrows</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H08_streamplot.png"><img src="png/H08_streamplot.png" width="100%"/></a><br/><b>H08. Streamplot</b><br/><sub>flow streamlines</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H09_polar.png"><img src="png/H09_polar.png" width="100%"/></a><br/><b>H09. Polar</b><br/><sub>periodic / directional data</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/H10_ternary.png"><img src="png/H10_ternary.png" width="100%"/></a><br/><b>H10. Ternary</b><br/><sub>3-component composition</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H11_annotated_field_profile.png"><img src="png/H11_annotated_field_profile.png" width="100%"/></a><br/><b>H11. Annotated Field Profile</b><br/><sub>field + companion profile, annotated</sub></td>
<td width="33%" valign="top" align="center"><a href="png/H12_polar_heatmap.png"><img src="png/H12_polar_heatmap.png" width="100%"/></a><br/><b>H12. Polar Heatmap</b><br/><sub>radial heatmap (rings x sectors)</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

<a id="cat-specialized"></a>
## 🧩 Specialized  ·  13 figures

<table>
<tr>
<td width="33%" valign="top" align="center"><a href="png/I01_multipanel_abc.png"><img src="png/I01_multipanel_abc.png" width="100%"/></a><br/><b>I01. Multipanel Abc</b><br/><sub>composed figure with a/b/c labels</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I02_small_multiples.png"><img src="png/I02_small_multiples.png" width="100%"/></a><br/><b>I02. Small Multiples</b><br/><sub>one grammar, many panels</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I03_annotated_heatmap.png"><img src="png/I03_annotated_heatmap.png" width="100%"/></a><br/><b>I03. Annotated Heatmap</b><br/><sub>matrix with cell values</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/I04_horizon.png"><img src="png/I04_horizon.png" width="100%"/></a><br/><b>I04. Horizon</b><br/><sub>dense time-series in little height</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I05_upset.png"><img src="png/I05_upset.png" width="100%"/></a><br/><b>I05. Upset</b><br/><sub>many-set intersections</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I06_colormap_demo.png"><img src="png/I06_colormap_demo.png" width="100%"/></a><br/><b>I06. Colormap Demo</b><br/><sub>perceptual uniformity, not rainbow</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/I07_model_vs_data.png"><img src="png/I07_model_vs_data.png" width="100%"/></a><br/><b>I07. Model Vs Data</b><br/><sub>overlay with uncertainty</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I08_study_design.png"><img src="png/I08_study_design.png" width="100%"/></a><br/><b>I08. Study Design</b><br/><sub>study-design / dosing timeline</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I09_pipeline_schematic.png"><img src="png/I09_pipeline_schematic.png" width="100%"/></a><br/><b>I09. Pipeline Schematic</b><br/><sub>analysis / model pipeline diagram</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/I10_pie_vs_bar.png"><img src="png/I10_pie_vs_bar.png" width="100%"/></a><br/><b>I10. Pie Vs Bar</b><br/><sub>AP10/AP11: why pie loses to a bar</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I11_biodistribution_route.png"><img src="png/I11_biodistribution_route.png" width="100%"/></a><br/><b>I11. Biodistribution Route</b><br/><sub>route of administration and organ fate</sub></td>
<td width="33%" valign="top" align="center"><a href="png/I12_mechanism_cartoon.png"><img src="png/I12_mechanism_cartoon.png" width="100%"/></a><br/><b>I12. Mechanism Cartoon</b><br/><sub>receptor binding and uptake pathway</sub></td>
</tr>
<tr>
<td width="33%" valign="top" align="center"><a href="png/I13_binned_heatmap.png"><img src="png/I13_binned_heatmap.png" width="100%"/></a><br/><b>I13. Binned Heatmap</b><br/><sub>binned-color heatmap with row metadata</sub></td>
</tr>
</table>

<sub>[↑ back to top](#example-gallery--138-publication-quality-figures)</sub>

---

*138 figures generated by `scripts/generate_gallery.py` (seed 20260706) for the [data-strength-elevator](../) graph-style library. Palette: Okabe-Ito (Wong 2011). Anti-pattern codes (AP1–AP16): see [`references/graph-style-library.md`](../references/graph-style-library.md).*
