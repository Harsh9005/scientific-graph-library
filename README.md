# Data-Strength Elevator — a scientific figure & data-presentation library

A reusable library for raising the **data-presentation strength** of a manuscript or grant to elite-journal standard: a curated **graph-style library** with a **deterministic decision engine**, a **reviewer-proof statistics** reference, domain-correct conventions for pharmaceutical / modelling work (IVIVC, dissolution, PK, PBPK, CFD, PINN), and a **gallery of 103 publication-quality example figures** built from synthetic data.

The goal is simple: stop *searching* for "which chart should I use?" and instead **decide** — with the rules for a high-impact figure enforced automatically.

<p align="center">
  <img src="examples/png/C07_dot_on_bar.png" width="30%"/>
  <img src="examples/png/G14_scree_pca.png" width="37%"/>
  <img src="examples/png/H06_field_heatmap.png" width="28%"/>
</p>

---

## What's inside

| Path | What it is |
|---|---|
| [`references/graph-style-library.md`](references/graph-style-library.md) | **45 graph styles** across 8 purposes + a **decision layer** + a 16-rule **anti-pattern registry** |
| [`references/publication-ready-figures.md`](references/publication-ready-figures.md) | Hard publication-craft standards: zero-overlap audit, print legibility, one colorblind-safe palette, per-entity consistency, screen-reader accessibility, **journal style-engines** (SciencePlots, ultraplot) and colorblind-gated journal palettes |
| [`references/statistics-rigor.md`](references/statistics-rigor.md) | Reviewer-proof statistics standard + a modeling / data-science statistics layer |
| [`references/domain-conventions.md`](references/domain-conventions.md) | Anti-mis-transfer conventions for IVIVC / dissolution / PK / PBPK / CFD / PINN |
| [`scripts/graph_catalog.json`](scripts/graph_catalog.json) | Single machine-readable index: styles + anti-patterns + palettes + style-engines + stat-methods |
| [`scripts/choose_graph.py`](scripts/choose_graph.py) | **Decision engine** — intent → ranked styles + enforced anti-patterns + palette/engine/stat |
| [`examples/`](examples/) | **103** publication-quality example figures across 9 categories (PNG + vector PDF) + the generator |

## The decision engine

```bash
python3 scripts/choose_graph.py --intent "compare means" --data categorical --n 4 --domain PK
```
```
## Recommended styles (ranked)
  S1  Bar + overlaid individual data points (dot-on-bar)   [intent:compare, domain:PK]
  S25 Confidence-interval / equivalence forest
  S30 Semi-log PK concentration–time profile
## Rules enforced
  [AP2]  REJECT violin/box; use S1/S2                (n < 20)
  [DS5]  REJECT mean±SD-linear + t-test; geometric mean, log, 90% CI
## Palette: okabe_ito (colorblind-safe)   ## Stat: geometric mean / 90% CI (BE 80–125%)
```

It queries `graph_catalog.json`, so styles and rules are stored once and answered instantly — no browsing. Options: `--intent --data --n --domain --journal --json`.

## The example gallery

**103** modern, high-impact-journal-ready figures across 9 categories (distributions, correlation, comparison, part-of-whole, flow/network, time-series, scientific/biomedical, 3D/fields, specialized) from **synthetic, seeded data**, each following the library's rules (one colorblind-safe palette, points-on-bars, exact P-values, sequential colormaps, vector output). See **[examples/README.md](examples/README.md)**. Regenerate with:

```bash
pip install -r requirements.txt          # matplotlib, numpy, scipy, seaborn, networkx, pandas (no LaTeX)
python3 examples/generate_gallery.py
```

## Design principles

- **Decide, don't browse.** A machine-readable catalog + a chooser, not a wall of options.
- **Colorblind-safe by default** (Okabe-Ito; Wong 2011). Journal palettes are opt-in and gated by a colorblind check.
- **Anti-patterns are enforced, not just listed** — bars that hide distributions, violins at small n, jet colormaps, pie/donuts, unreordered heatmaps (AP1–AP16, with primary-literature citations).
- **Domain-correct.** Modelling/data-science techniques never launder onto wet-lab endpoints; PK gets geometric mean + 90% CI, dissolution gets f2, models get parity + agreement.

## Attribution

Graph-style variety and modeling statistics distilled (technique/idiom only) from [Nathan Kutz's *Data-Driven Modeling & Scientific Computation*](https://github.com/nathankutz/ScientificComputing). Anti-pattern registry from [FriendsDontLetFriends](https://github.com/cxli233/FriendsDontLetFriends) (MIT) with its cited literature (Wong 2011, Weissgerber 2015). Journal style-engines from [SciencePlots](https://github.com/garrettj403/SciencePlots) and [ultraplot](https://github.com/ultraplot/ultraplot) (MIT); journal palette hex from [ggsci](https://github.com/nanxstats/ggsci) / [ggprism](https://github.com/csdaw/ggprism) (colour values are facts; their GPL-3 code is not used). Figure standards benchmarked against Nature-family exemplars (see `references/_exemplar_mining/`).

## License

MIT — see [LICENSE](LICENSE). The example data are synthetic and illustrative.
