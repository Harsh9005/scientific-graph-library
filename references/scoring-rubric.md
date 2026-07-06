<!-- data-strength-elevator reference module — CONSOLIDATED SCORING RUBRIC.
Canonical dimension/check IDs, anchored bands, grade ladder. scripts/score_manuscript.py
implements this exactly. Every "elite" anchor cites the exemplar evidence so a score is
auditable, not asserted (per the build-time verification judge's refinement). -->

# Consolidated Data-Strength Scoring Rubric
### Five dimensions, anchored 0/1/2 checks, reproducible grade ladder

This rubric aggregates the five dimension modules into one score. It is deliberately
**auditable**: each dimension's checks live in its own module with an explicit Elite/Adequate/Weak
anchor, and each "Elite" bar names the exemplar convention it is grounded in (e.g. "5/5 papers
overlay individual points"). A grader must be able to point at the check that failed and the
exemplar it derives from — never a bare score.

> **Scoring principle (from build-time verification):** do not assert "2/30" or "5/5 exemplars"
> as rhetoric. Every check is scored **0/1/2 against a written anchor**, and the exemplar
> evidence for the "elite" band is stated in the source module. Reproducible, not persuasive.

---

## The five dimensions and their check sets

| Dim | Name | Checks | Max | Source module | Blocker checks (a 0 here caps the grade) |
|---|---|---|---|---|---|
| **DS1** | Figures & Data Visualization | 25 (F1–F25) | 50 | `figure-strategy.md` §C + `publication-ready-figures.md` | F1 (points-on-bars), F3 (benchmark on axis), F5 (SD/n defined), **F16 (F-overlap)**, **F19 (F-cite)** |
| **DS2** | Statistics & Data-Analysis Rigor | 15 (C1–C15) | 30 | `statistics-rigor.md` §C | C1–C6 |
| **DS3** | Narrative Craft (Results→Disc→Concl) | 13 (N1–N13) | 26 | `narrative-craft.md` §C | N3 (quant density), N4 (named comparator) |
| **DS4** | Writing Style & Journal Fit | 15 (S1–S15) | 30 | `style-and-journal-fit.md` §C | S2 (quant density), S6 (stats reporting) |
| **DS5** | Domain Correctness | 10 (D1–D10) | 20 | `domain-conventions.md` §F | D1–D5 |
| *(grant mode)* | Grant Add-on | 7 (G1–G7) | 14 | `grant-module.md` §E | G1 (testable Aims), G3 (prelim rigor) |

Score every check **Elite = 2 / Adequate = 1 / Weak = 0** against its module's written anchor.

### DS1 publication-ready checks (F16–F25) — appended

DS1 now carries **ten** publication-ready craft checks on top of the original F1–F15, anchored in
`publication-ready-figures.md`. They exist because the user requires **submission-ready** output —
a figure that is analytically correct but not publication-ready is not done. When choosing the
chart primitive for a panel, consult `graph-style-library.md` (45 styles across 8 purposes) so the
sharpest chart is picked for each analytical point. F18/F20/F21 plus F22–F25 together enforce the
six-part figure-consistency test (same fonts & sizes · similar line weights & distinguishable
points · intentional repeated colors · screen-reader + colorblind accessible · consistent scale ·
one coherent story).

| Check | Governs | Anchor | Blocker? |
|---|---|---|---|
| **F16 F-overlap** | zero text/mark overlap; **deterministic `assert_no_overlaps(fig)` bbox-intersection audit must pass** (wired as a build-time gate before save) + zoom-crop of each dense region as backstop — visual-only inspection of a downsampled PNG does NOT satisfy it | pub-ready R1 | **YES** |
| **F17 F-zoom** | legible at 100%/print size; ≥ 300 dpi or vector; point floors (per-figure) | pub-ready R2 | no |
| **F18 F-theme** | one manuscript-wide colorblind-safe palette; reserved accent | pub-ready R4 | no |
| **F19 F-cite** | every figure AND table cited in body text at the point it supports | pub-ready R6 | **YES** |
| **F20 F-entity** | same color + marker/shape per entity in every figure and table | pub-ready R5 | no |
| **F21 F-style** | figure typography (family/weight) matches the manuscript, consistent across figures | pub-ready R3 | no |
| **F22 F-lineweight** | consistent line/marker weights across figures; series & data points distinguishable (greyscale test; no overplotting) | pub-ready R7 | no |
| **F23 F-a11y** | screen-reader accessible: alt-text/described caption, redundant (non-color) encoding, contrast, real vector text | pub-ready R8 | no |
| **F24 F-scale** | same-role text & element sizes uniform across the suite; no per-figure zoom mismatch | pub-ready R9 | no |
| **F25 F-suite** | figures share one visual language + deliberate order — read as a single story | pub-ready R10 | no |

**Why F16 and F19 are blockers:** an overlapping, unreadable figure and an uncited display are
defects a reviewer/editor flags on sight — neither is acceptable in a publication-ready submission.
A 0 on either caps the overall grade at **Not ready** (same mechanism as the existing blockers).
F22–F25 are quality checks, not blockers. DS1 max rises from 30 (F1–F15) → 42 (F16–F21) →
**50** (F22–F25 added); the per-dimension band is computed on the current max.

---

## Per-dimension band (raw % → 1–5)

Each dimension's raw score is converted to a 1–5 band (aligns with the writing-orchestrator
six-dimension rubric so scores are comparable across skills):

| Dimension % of max | Band |
|---|---|
| ≥ 90% | 5 |
| 75–89% | 4 |
| 60–74% | 3 |
| 40–59% | 2 |
| < 40% | 1 |

---

## Grade ladder (mean of DS1–DS5, with floors and blockers)

| Grade | Condition |
|---|---|
| **Elite / Submission-ready** | mean ≥ 4.5 AND no dimension < 3 AND no blocker check = 0 |
| **Strong** | mean ≥ 3.8 AND no dimension < 3 AND no blocker check = 0 |
| **Adequate — needs targeted work** | mean ≥ 3.0 AND no dimension < 2 |
| **Weak — substantial revision** | mean ≥ 2.0 |
| **Not ready** | mean < 2.0 OR any dimension = 1 OR any blocker check = 0 |

**Blocker rule:** a 0 on any blocker check caps the overall grade at **"Not ready"** regardless of
the mean, because these are the rigor failures a reviewer rejects on sight (undefined error bars,
wrong test for design, no named benchmark, laundered wet-lab units, non-testable Aims).

**Grant mode:** the 5 dimensions still apply to preliminary figures + prose; the Grant Add-on
(G1–G7) is scored and reported separately, and G1/G3 are blockers for the grant verdict.

---

## Output contract

The scorer (`scripts/score_manuscript.py`) consumes a JSON of check scores and emits:

1. **Per-dimension:** raw/max, %, band (1–5), and the list of failed checks with IDs.
2. **Overall:** mean band, grade, and whether any blocker fired (with which one).
3. **Prioritized gap list:** blockers first, then 0-scored checks, then 1-scored checks, each with
   its module reference so the fix is one lookup away.

A grade is never reported without the failed-check list that produced it.

---

## How this complements (does not replace) the writing-orchestrator six-dimension rubric

`writing-orchestrator/references/six-dimension-rubric.md` scores **argument rigor** — D1 Evidence
Relevance, D2 Falsifiability, D3 Scope Calibration, D4 Argument Coherence, D5 Exploration Integrity,
D6 Methodological Rigor. That rubric governs *whether the claims are supported and well-scoped*.

This rubric governs **how quantitative data is presented and discussed** — the craft the
six-dimension rubric does not resolve at figure/stat/paragraph granularity. The two are orthogonal
and layer cleanly: a draft can pass argument-rigor D1–D6 and still be a Weak DS1/DS2 draft (bare
bars, SEM, no named benchmark). Use both. This rubric **deepens** six-dimension D6 (Methodological
Rigor) with the figure/statistic/narration specifics that D6 scores only at a high level.
