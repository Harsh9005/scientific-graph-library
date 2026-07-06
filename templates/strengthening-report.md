# Data-Strength Elevator — Strengthening Report

- **Document:** {{path}}
- **Mode:** {{manuscript | grant}}
- **Domain:** {{IVIVC / dissolution / formulation / PK / PBPK / CFD / PINN / mixed}}
- **Target venue:** {{journal or funder}}  (translational calibration applied per domain-conventions §D)
- **Date:** {{YYYY-MM-DD}}

---

## 1. Verdict

**Grade: {{grade}}** — mean band {{x}}/5{{, BLOCKER fired: <check(s)>}}

One-paragraph plain-language summary of where the document stands and the 2–3 changes that
move the needle most.

## 2. Score table

*(paste `score_manuscript.py` output)*

| Dim | Name | Raw | % | Band | Failed |
|---|---|---|---|---|---|
| DS1 | Figures & Data Visualization | /50 | | | |
| DS2 | Statistics & Data-Analysis Rigor | /30 | | | |
| DS3 | Narrative Craft | /26 | | | |
| DS4 | Writing Style & Journal Fit | /30 | | | |
| DS5 | Domain Correctness | /20 | | | |
| G | Grant Add-on *(grant mode)* | /14 | | | |

## 3. Blockers (fix first — these are reject-on-sight)

For each fired blocker: the check, where it fails (figure/section + verbatim quote), and the fix.

- **[BLOCKER] {{ID}} — {{label}}**
  - Where: {{Fig/section + verbatim span}}
  - Fix: {{concrete, domain-correct instruction}}

## 4. Figure program rebuild (DS1 + domain)

Per-figure table: current chart → problem → elite-standard replacement (chart primitive, points,
benchmark on axis, on-plot stats, domain-correct units).

| Fig | Current | Problem | Rebuild to |
|---|---|---|---|
| | | | |

Missing figures to add (e.g. Bland–Altman for IVIVC, GCI plot for CFD, parity for PINN, RLD overlay).

**Publication-ready gate (per figure — `publication-ready-figures.md` R11).** Record pass (✓) / fail (✗) /
needs-source (~) for each figure. F16 and F19 are blockers (a ✗ caps DS1 at Not-ready); F22–F25 are the
figure-consistency checks (line weight/points · screen-reader a11y · scale uniformity · single story).

| Fig | F16 overlap* | F17 zoom | F18 theme | F19 cite* | F20 entity | F21 style | F22 lineweight | F23 a11y | F24 scale | F25 suite |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

*\* = blocker.* Also note the suite-level checks once for the whole set: F24 (are same-role sizes uniform
across all figures?) and F25 (do the figures read as one story?).

## 5. Statistics & data-analysis corrections (DS2 + domain)

Each correction as: current → correct test/metric/units, with the reason. Flag any **laundered
wet-lab default** (mean±SD/linear on PK, n=3 on dissolution, ANOVA-on-endpoint for profiles).

## 6. Narrative rewrites (DS3) — before → after

At least the abstract, one key results paragraph, one discussion paragraph, and the conclusion,
rewritten to the five-beat / three-move standard with numbers + named benchmarks.

**BEFORE:**
> {{verbatim}}

**AFTER:**
> {{rewrite}}

## 7. Style & journal-fit (DS4) + reporting-standard scaffold

Signposting, quantitative density, assert/hedge calibration; conformance to USP/ICH / FDA-IVIVC /
ASME V&V 20 / model-card as applicable; translational calibration to the named venue.

## 8. Grant-only (grant mode) — Aims/Significance/Innovation/Feasibility

Per grant-module.md: claim-first testable Aims + go/no-go, quantified benchmarked significance,
specific-referent innovation, risk+alternatives, small-lab-as-de-risking framing.

## 9. Prioritized action list

1. {{highest-leverage change}}
2. …

## 10. Re-score (after edits)

Provisional re-score to show the delta (grade before → after).
