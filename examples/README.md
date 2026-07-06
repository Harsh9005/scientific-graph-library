# Example gallery — 103 publication-quality figures

This gallery holds **103 chart types and variants** across 9 categories. Every figure is drawn from **synthetic, seeded data** by [`generate_gallery.py`](generate_gallery.py), so rerunning the script hands back the same picture rather than something that drifts, and each one was built to follow the library's own rules: a single **colorblind-safe palette** (Okabe-Ito), sans-serif type, points sitting on the bars, exact statistics, **sequential colour maps rather than jet**, and clean axes. Everything is exported twice — a **PNG at 300 dpi** to preview here, and a **vector PDF** to drop straight into a manuscript ([`png/`](png/), [`pdf/`](pdf/)).

Regenerate everything with `python3 generate_gallery.py` (needs matplotlib, numpy, scipy, seaborn, networkx, pandas — no LaTeX).

> Data are synthetic and illustrative — the figures demonstrate **form and standards**, not real results.

| Category | Count | Category | Count |
|---|---|---|---|
| 📊 Distributions | 16 | 🔗 Correlation | 14 |
| 📶 Comparison | 14 | 🥧 Part-of-whole | 7 |
| 🕸️ Flow-Network | 5 | 📈 Time-series | 10 |
| 🔬 Scientific | 20 | 🌐 3D-Fields | 10 |
| 🧩 Specialized | 7 |  |   |

---

## 📊 Distributions

**A01. Histogram** — *single distribution*  
![A01_histogram](png/A01_histogram.png)

**A02. Histogram Multiple** — *compare two distributions*  
![A02_histogram_multiple](png/A02_histogram_multiple.png)

**A03. Histogram Kde** — *density overlay*  
![A03_histogram_kde](png/A03_histogram_kde.png)

**A04. Hist2D** — *joint density (binned)*  
![A04_hist2d](png/A04_hist2d.png)

**A05. Hexbin** — *joint density (hex)*  
![A05_hexbin](png/A05_hexbin.png)

**A06. Kde** — *smooth density*  
![A06_kde](png/A06_kde.png)

**A07. Kde Multiple** — *compare densities*  
![A07_kde_multiple](png/A07_kde_multiple.png)

**A08. Ridgeline** — *distribution over an ordered factor*  
![A08_ridgeline](png/A08_ridgeline.png)

**A09. Box Grouped** — *distribution summary + raw*  
![A09_box_grouped](png/A09_box_grouped.png)

**A10. Box Notched** — *median confidence via notch*  
![A10_box_notched](png/A10_box_notched.png)

**A11. Violin** — *distribution shape at large n*  
![A11_violin](png/A11_violin.png)

**A12. Violin Split** — *distribution by two factors*  
![A12_violin_split](png/A12_violin_split.png)

**A13. Raincloud** — *half-violin + strip*  
![A13_raincloud](png/A13_raincloud.png)

**A14. Strip** — *every point at small n*  
![A14_strip](png/A14_strip.png)

**A15. Ecdf** — *cumulative distribution*  
![A15_ecdf](png/A15_ecdf.png)

**A16. Qq** — *distributional check*  
![A16_qq](png/A16_qq.png)


## 🔗 Correlation

**B01. Scatter** — *two continuous variables*  
![B01_scatter](png/B01_scatter.png)

**B02. Scatter Groups** — *grouped scatter*  
![B02_scatter_groups](png/B02_scatter_groups.png)

**B03. Bubble** — *third variable via size*  
![B03_bubble](png/B03_bubble.png)

**B04. Regression** — *linear fit with confidence band*  
![B04_regression](png/B04_regression.png)

**B05. Marginal** — *joint + marginal distributions*  
![B05_marginal](png/B05_marginal.png)

**B06. Connected Scatter** — *ordered trajectory in 2D*  
![B06_connected_scatter](png/B06_connected_scatter.png)

**B07. Corr Heatmap** — *pairwise correlations*  
![B07_corr_heatmap](png/B07_corr_heatmap.png)

**B08. Clustermap** — *reordered heatmap + dendrograms*  
![B08_clustermap](png/B08_clustermap.png)

**B09. Density2D** — *smooth joint density*  
![B09_density2d](png/B09_density2d.png)

**B10. Pairplot** — *all pairwise relationships*  
![B10_pairplot](png/B10_pairplot.png)

**B11. Parity** — *model calibration*  
![B11_parity](png/B11_parity.png)

**B12. Bland Altman** — *method agreement + LoA*  
![B12_bland_altman](png/B12_bland_altman.png)

**B13. Residual** — *diagnostic for a fit*  
![B13_residual](png/B13_residual.png)

**B14. Loess** — *nonparametric trend*  
![B14_loess](png/B14_loess.png)


## 📶 Comparison

**C01. Bar** — *categorical magnitude (zero-based)*  
![C01_bar](png/C01_bar.png)

**C02. Bar Horizontal** — *ranked categories*  
![C02_bar_horizontal](png/C02_bar_horizontal.png)

**C03. Grouped Bar** — *two-factor comparison*  
![C03_grouped_bar](png/C03_grouped_bar.png)

**C04. Stacked Bar** — *composition per category*  
![C04_stacked_bar](png/C04_stacked_bar.png)

**C05. Percent Stacked** — *proportion per category*  
![C05_percent_stacked](png/C05_percent_stacked.png)

**C06. Diverging Bar** — *signed values around zero*  
![C06_diverging_bar](png/C06_diverging_bar.png)

**C07. Dot On Bar** — *bars never hide the sample (AP1)*  
![C07_dot_on_bar](png/C07_dot_on_bar.png)

**C08. Lollipop** — *ranked values, low ink*  
![C08_lollipop](png/C08_lollipop.png)

**C09. Cleveland Dumbbell** — *paired change per category*  
![C09_cleveland_dumbbell](png/C09_cleveland_dumbbell.png)

**C10. Radar** — *multivariate profile*  
![C10_radar](png/C10_radar.png)

**C11. Parallel Coords** — *high-dim comparison*  
![C11_parallel_coords](png/C11_parallel_coords.png)

**C12. Slope** — *before/after ranking change*  
![C12_slope](png/C12_slope.png)

**C13. Bump** — *rank evolution over time*  
![C13_bump](png/C13_bump.png)

**C14. Point Ci** — *position-based estimates*  
![C14_point_ci](png/C14_point_ci.png)


## 🥧 Part-of-whole

**D01. Stacked Area** — *composition over time*  
![D01_stacked_area](png/D01_stacked_area.png)

**D02. Treemap** — *hierarchical proportions*  
![D02_treemap](png/D02_treemap.png)

**D03. Sunburst** — *nested hierarchy*  
![D03_sunburst](png/D03_sunburst.png)

**D04. Venn** — *set overlap*  
![D04_venn](png/D04_venn.png)

**D05. Dendrogram** — *hierarchical clustering*  
![D05_dendrogram](png/D05_dendrogram.png)

**D06. Waffle** — *part-of-whole as unit squares*  
![D06_waffle](png/D06_waffle.png)

**D07. Mosaic** — *two categorical variables*  
![D07_mosaic](png/D07_mosaic.png)


## 🕸️ Flow-Network

**E01. Sankey** — *mass/flow balance*  
![E01_sankey](png/E01_sankey.png)

**E02. Network** — *nodes + edges, degree-scaled*  
![E02_network](png/E02_network.png)

**E03. Arc** — *network on a line*  
![E03_arc](png/E03_arc.png)

**E04. Bipartite** — *two-set relationships*  
![E04_bipartite](png/E04_bipartite.png)

**E05. Adjacency** — *network as a matrix*  
![E05_adjacency](png/E05_adjacency.png)


## 📈 Time-series

**F01. Line** — *single series over time*  
![F01_line](png/F01_line.png)

**F02. Multiline** — *several series*  
![F02_multiline](png/F02_multiline.png)

**F03. Line Ci** — *trajectory + uncertainty*  
![F03_line_ci](png/F03_line_ci.png)

**F04. Area** — *magnitude over time*  
![F04_area](png/F04_area.png)

**F05. Streamgraph** — *flowing composition*  
![F05_streamgraph](png/F05_streamgraph.png)

**F06. Waterfall** — *family of profiles*  
![F06_waterfall](png/F06_waterfall.png)

**F07. Candlestick** — *financial time-series*  
![F07_candlestick](png/F07_candlestick.png)

**F08. Spectrogram** — *time–frequency (chirp)*  
![F08_spectrogram](png/F08_spectrogram.png)

**F09. Decomposition** — *trend + seasonal + residual*  
![F09_decomposition](png/F09_decomposition.png)

**F10. Step** — *piecewise-constant series*  
![F10_step](png/F10_step.png)


## 🔬 Scientific

**G01. Dose Response** — *sigmoidal fit*  
![G01_dose_response](png/G01_dose_response.png)

**G02. Kaplan Meier** — *time-to-event*  
![G02_kaplan_meier](png/G02_kaplan_meier.png)

**G03. Forest** — *effect sizes across studies*  
![G03_forest](png/G03_forest.png)

**G04. Pk Semilog** — *geometric mean, log axis*  
![G04_pk_semilog](png/G04_pk_semilog.png)

**G05. Dissolution** — *profile + f2*  
![G05_dissolution](png/G05_dissolution.png)

**G06. Roc** — *classifier discrimination*  
![G06_roc](png/G06_roc.png)

**G07. Pr Curve** — *PR for imbalanced classes*  
![G07_pr_curve](png/G07_pr_curve.png)

**G08. Calibration** — *probability reliability*  
![G08_calibration](png/G08_calibration.png)

**G09. Confusion** — *per-class classifier behaviour*  
![G09_confusion](png/G09_confusion.png)

**G10. Volcano** — *differential expression*  
![G10_volcano](png/G10_volcano.png)

**G11. Manhattan** — *GWAS-style genome scan*  
![G11_manhattan](png/G11_manhattan.png)

**G12. Ma Plot** — *intensity-dependent ratio*  
![G12_ma_plot](png/G12_ma_plot.png)

**G13. Tornado** — *ranked parameter influence*  
![G13_tornado](png/G13_tornado.png)

**G14. Scree Pca** — *rank + structure*  
![G14_scree_pca](png/G14_scree_pca.png)

**G15. Biplot** — *scores + loadings*  
![G15_biplot](png/G15_biplot.png)

**G16. Embedding** — *nonlinear low-dim embedding*  
![G16_embedding](png/G16_embedding.png)

**G17. Stem** — *discrete/sparse coefficients*  
![G17_stem](png/G17_stem.png)

**G18. Bifurcation** — *route to chaos (logistic map)*  
![G18_bifurcation](png/G18_bifurcation.png)

**G19. Gci** — *mesh-independence / order*  
![G19_gci](png/G19_gci.png)

**G20. Control Chart** — *process monitoring ±3σ*  
![G20_control_chart](png/G20_control_chart.png)


## 🌐 3D-Fields

**H01. Surface3D** — *solution field u(x,t)*  
![H01_surface3d](png/H01_surface3d.png)

**H02. Wireframe** — *surface as mesh*  
![H02_wireframe](png/H02_wireframe.png)

**H03. Scatter3D** — *three continuous variables*  
![H03_scatter3d](png/H03_scatter3d.png)

**H04. Contour** — *iso-lines of a field*  
![H04_contour](png/H04_contour.png)

**H05. Contourf** — *field with colorbar*  
![H05_contourf](png/H05_contourf.png)

**H06. Field Heatmap** — *2D field, viridis (never jet)*  
![H06_field_heatmap](png/H06_field_heatmap.png)

**H07. Quiver** — *vector field arrows*  
![H07_quiver](png/H07_quiver.png)

**H08. Streamplot** — *flow streamlines*  
![H08_streamplot](png/H08_streamplot.png)

**H09. Polar** — *periodic / directional data*  
![H09_polar](png/H09_polar.png)

**H10. Ternary** — *3-component composition*  
![H10_ternary](png/H10_ternary.png)


## 🧩 Specialized

**I01. Multipanel Abc** — *composed figure with a/b/c labels*  
![I01_multipanel_abc](png/I01_multipanel_abc.png)

**I02. Small Multiples** — *one grammar, many panels*  
![I02_small_multiples](png/I02_small_multiples.png)

**I03. Annotated Heatmap** — *matrix with cell values*  
![I03_annotated_heatmap](png/I03_annotated_heatmap.png)

**I04. Horizon** — *dense time-series in little height*  
![I04_horizon](png/I04_horizon.png)

**I05. Upset** — *many-set intersections*  
![I05_upset](png/I05_upset.png)

**I06. Colormap Demo** — *perceptual uniformity, not rainbow*  
![I06_colormap_demo](png/I06_colormap_demo.png)

**I07. Model Vs Data** — *overlay with uncertainty*  
![I07_model_vs_data](png/I07_model_vs_data.png)


---

*103 figures generated by `generate_gallery.py` (seed 20260706) for the [data-strength-elevator](../) graph-style library. Palette: Okabe-Ito (Wong 2011). Anti-pattern codes (AP1-AP16): see [`references/graph-style-library.md`](../references/graph-style-library.md).*