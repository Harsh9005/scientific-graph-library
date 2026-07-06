#!/usr/bin/env python3
"""
score_manuscript.py — deterministic aggregator for the data-strength-elevator rubric.

It does NOT judge a manuscript itself (that is the audit phases' job — a judgment call that
stays with the auditing agent/user). It consumes a JSON of per-check scores (0/1/2) produced
by the audit and emits reproducible dimension bands, an overall grade, blocker detection, and a
prioritized gap list. This is the mechanical half of the skill; the anchors live in
references/*.md.

Usage:
  python3 score_manuscript.py --template            > scores.json     # blank manuscript template
  python3 score_manuscript.py --template --grant    > scores.json     # includes grant add-on
  python3 score_manuscript.py scores.json                             # markdown report
  python3 score_manuscript.py scores.json --json                      # machine-readable report

Scores file shape:
  { "mode": "manuscript" | "grant",
    "meta": { "title": "...", "target_journal": "...", "domain": "IVIVC/dissolution/..." },
    "scores": { "F1": 2, "F2": 1, ..., "C1": 0, ..., "D1": 2, ... , "G1": 1 } }
Each value is 2 (elite) / 1 (adequate) / 0 (weak), or null/omitted if not yet scored.
"""
import sys, json

# ---- Canonical rubric (mirrors references/scoring-rubric.md) --------------------------------
CHECKS = {
    "DS1": {
        "name": "Figures & Data Visualization",
        "module": "references/figure-strategy.md §C + references/publication-ready-figures.md",
        "blockers": ["F1", "F3", "F5", "F16", "F19"],
        "labels": {
            "F1": "Individual data points shown (dots on bars)",
            "F2": "Image <-> quantification pairing",
            "F3": "Clinical/approved benchmark on the same axis",
            "F4": "Chart type matches data structure",
            "F5": "Error bars = SD, defined; n biological per panel",
            "F6": "Exact P-values on plot + threshold ladder + honest n.s.",
            "F7": "Statistical test named and matched to design",
            "F8": "Multi-panel figures build an argument",
            "F9": "Schematic-to-data ratio controlled (<=~15%)",
            "F10": "Consistent colour/group code across figures",
            "F11": "Full screen shown (losers incl.) + physicochemical QC per lead",
            "F12": "Overview-then-detail for high-dimensional data",
            "F13": "Mechanism by quantified loss-of-function",
            "F14": "Orthogonal / two-level validation in-figure",
            "F15": "Translational ladder visible in figure sequence",
            "F16": "F-overlap: zero text/mark overlap (audit at print size) [BLOCKER]",
            "F17": "F-zoom: legible at 100%/print size, >=300 dpi, point floors",
            "F18": "F-theme: one CB-safe manuscript-wide palette, reserved accent",
            "F19": "F-cite: every figure AND table cited in body text [BLOCKER]",
            "F20": "F-entity: same colour+marker/shape per entity everywhere",
            "F21": "F-style: figure typography (family/weight) matches manuscript, consistent",
            "F22": "F-lineweight: consistent line/marker weights; series & points distinguishable (no overplotting)",
            "F23": "F-a11y: screen-reader accessible - alt-text/described caption, non-colour encoding, contrast, vector text",
            "F24": "F-scale: same-role text & element sizes uniform across the suite (no per-figure zoom mismatch)",
            "F25": "F-suite: figures share one visual language + deliberate order - read as a single story",
        },
    },
    "DS2": {
        "name": "Statistics & Data-Analysis Rigor", "module": "references/statistics-rigor.md §C",
        "blockers": ["C1", "C2", "C3", "C4", "C5", "C6"],
        "labels": {
            "C1": "Error bars defined (mean +/- SD every legend)",
            "C2": "p-values exact on panel + ladder",
            "C3": "Test <-> design match (log-rank for survival etc.)",
            "C4": "Multiple-comparison correction named & applied",
            "C5": "n defined & biological vs technical distinguished",
            "C6": "Effect size (fold/%/log/AUC) beside every p",
            "C7": "Orthogonal validation (>=2 methods/core claim)",
            "C8": "Benchmark comparator on the same axes",
            "C9": "Controls ladder (vehicle+prior-art+mechanistic+positive)",
            "C10": "Individual data points on bars",
            "C11": "n.s. honesty (shown & labelled)",
            "C12": "Screen/DoE transparency (loser-included)",
            "C13": "Assumptions & power stated honestly",
            "C14": "Reproducibility scaffold (source data, versions, IDs)",
            "C15": "Model-data reconciliation (if any computation)",
        },
    },
    "DS3": {
        "name": "Narrative Craft (Results->Disc->Concl)", "module": "references/narrative-craft.md §C",
        "blockers": ["N3", "N4"],
        "labels": {
            "N1": "Finding-first topic sentences",
            "N2": "Five-beat paragraph structure",
            "N3": "Quantitative density (>=1 number / results sentence)",
            "N4": "Magnitude vs a NAMED comparator",
            "N5": "Effect size + P reported together",
            "N6": "Register calibration (assert data / hedge inference)",
            "N7": "Discussion opens gap + finding + benchmark",
            "N8": "Mechanism via causal chain + data + literature",
            "N9": "Limitations concrete + mitigated",
            "N10": "Honest negatives / n.s. in prose",
            "N11": "Conclusion 3-move arc",
            "N12": "Impact bounded & grounded in an established premise",
            "N13": "Translational / orthogonal reach narrated",
        },
    },
    "DS4": {
        "name": "Writing Style & Journal Fit", "module": "references/style-and-journal-fit.md §C",
        "blockers": ["S2", "S6"],
        "labels": {
            "S1": "Finding-first topic sentences (skim = argument)",
            "S2": "Quantitative density (numbers in prose)",
            "S3": "Named-benchmark comparison, primary figure",
            "S4": "Orthogonal validation of core claim",
            "S5": "Assert-vs-hedge calibration",
            "S6": "Error bars & stats reporting (SD, exact P)",
            "S7": "Correct test for design",
            "S8": "Replicate definition (biological vs technical)",
            "S9": "Honest negatives",
            "S10": "DoE optimization (not ad-hoc)",
            "S11": "Full physicochemical / model QC per lead",
            "S12": "Generalizability (>=2 axes)",
            "S13": "Translational ladder + human rung (target-calibrated)",
            "S14": "Objection pre-emption (biggest reviewer worry)",
            "S15": "Calibrated conclusion (platform / proof-of-concept)",
        },
    },
    "DS5": {
        "name": "Domain Correctness", "module": "references/domain-conventions.md §F",
        "blockers": ["D1", "D2", "D3", "D4", "D5"],
        "labels": {
            "D1": "Right chart primitive for the data type",
            "D2": "Profile comparison correct (f2/bootstrap/Mahalanobis)",
            "D3": "PK/BE in domain units (geo mean, 90% CI, log, 80-125%)",
            "D4": "IVIVC validated not just fitted (%PE, out-of-sample, Bland-Altman)",
            "D5": "Numerical/ML rigor stated (GCI / mesh-indep or RMSE/relative-L2 + seed)",
            "D6": "Reporting-standard conformance cited (USP/ICH/FDA-IVIVC/V&V20)",
            "D7": "Benchmark = RLD/established model on shared axis",
            "D8": "Model reconciled with data + quantified gap",
            "D9": "Journal-appropriate translational calibration",
            "D10": "No laundered wet-lab default (see §0)",
        },
    },
}
GRANT = {
    "name": "Grant Add-on", "module": "references/grant-module.md §E",
    "blockers": ["G1", "G3"],
    "labels": {
        "G1": "Aims claim-first + testable + go/no-go",
        "G2": "Gap & significance quantified and benchmarked",
        "G3": "Preliminary figures manuscript-grade & domain-correct",
        "G4": "Innovation has a specific referent",
        "G5": "Risk paired with alternative strategy + decision rule",
        "G6": "Small-lab profile framed as de-risking strength",
        "G7": "Rigor/reproducibility attachment complete",
    },
}


def nat(cid):
    """Natural sort key: F2 before F10."""
    return (cid[0], int("".join(c for c in cid[1:] if c.isdigit()) or 0))


def band(pct):
    if pct is None:
        return None
    if pct >= 0.90: return 5
    if pct >= 0.75: return 4
    if pct >= 0.60: return 3
    if pct >= 0.40: return 2
    return 1


def score_dim(defn, scores):
    present = {cid: scores[cid] for cid in defn["labels"] if scores.get(cid) is not None}
    missing = [cid for cid in defn["labels"] if scores.get(cid) is None]
    raw = sum(present.values())
    mx = 2 * len(present)
    pct = (raw / mx) if mx else None
    failed = {cid: v for cid, v in present.items() if v < 2}
    blockers_fired = [cid for cid in defn["blockers"] if scores.get(cid) == 0]
    return {"raw": raw, "max": mx, "pct": pct, "band": band(pct),
            "failed": failed, "missing": missing, "blockers_fired": blockers_fired}


def grade(dim_results):
    bands = [r["band"] for r in dim_results.values() if r["band"] is not None]
    if not bands:
        return None, None, False
    mean = sum(bands) / len(bands)
    any_blocker = any(r["blockers_fired"] for r in dim_results.values())
    lt3 = any(b < 3 for b in bands)
    lt2 = any(b < 2 for b in bands)
    eq1 = any(b == 1 for b in bands)
    if any_blocker or mean < 2.0 or eq1:
        g = "Not ready"
    elif mean >= 4.5 and not lt3:
        g = "Elite / Submission-ready"
    elif mean >= 3.8 and not lt3:
        g = "Strong"
    elif mean >= 3.0 and not lt2:
        g = "Adequate - needs targeted work"
    elif mean >= 2.0:
        g = "Weak - substantial revision"
    else:
        g = "Not ready"
    return round(mean, 2), g, any_blocker


def label_of(cid):
    for d in CHECKS.values():
        if cid in d["labels"]:
            return d["labels"][cid], d["module"]
    if cid in GRANT["labels"]:
        return GRANT["labels"][cid], GRANT["module"]
    return cid, "?"


def template(grant=False):
    scores = {}
    for d in CHECKS.values():
        for cid in d["labels"]:
            scores[cid] = None
    if grant:
        for cid in GRANT["labels"]:
            scores[cid] = None
    return {"mode": "grant" if grant else "manuscript",
            "meta": {"title": "", "target_journal": "", "domain": ""},
            "scores": scores}


def build_report(data):
    scores = data.get("scores", {})
    mode = data.get("mode", "manuscript")
    dim_results = {k: score_dim(v, scores) for k, v in CHECKS.items()}
    mean, g, any_blocker = grade(dim_results)
    grant_res = score_dim(GRANT, scores) if mode == "grant" else None
    # Completeness guard: an under-populated scores.json (checks omitted, not set 0/1/2)
    # must NOT read as a clean grade — omitted checks silently inflate the band AND
    # a never-scored blocker can never fire. A partial run is INCOMPLETE, not passing.
    unscored = [cid for r in dim_results.values() for cid in r["missing"]]
    if grant_res:
        unscored += grant_res["missing"]
    complete = len(unscored) == 0
    if not complete:
        g = f"INCOMPLETE ({len(unscored)} unscored) - provisional: {g}"
    # prioritized gaps: blockers -> 0s -> 1s
    prio = []
    for k, r in dim_results.items():
        for cid in r["blockers_fired"]:
            prio.append((0, cid))
        for cid, v in r["failed"].items():
            if cid not in r["blockers_fired"]:
                prio.append((1 if v == 0 else 2, cid))
    if grant_res:
        for cid in grant_res["blockers_fired"]:
            prio.append((0, cid))
        for cid, v in grant_res["failed"].items():
            if cid not in grant_res["blockers_fired"]:
                prio.append((1 if v == 0 else 2, cid))
    prio.sort(key=lambda x: (x[0], nat(x[1])))
    return dim_results, grant_res, mean, g, any_blocker, prio, complete, unscored


def main():
    args = sys.argv[1:]
    if "--template" in args:
        print(json.dumps(template("--grant" in args), indent=2))
        return
    paths = [a for a in args if not a.startswith("-")]
    if not paths:
        sys.exit("usage: score_manuscript.py scores.json [--json]  |  --template [--grant]")
    data = json.load(open(paths[0]))
    dim_results, grant_res, mean, g, any_blocker, prio, complete, unscored = build_report(data)

    if "--json" in args:
        out = {"grade": g, "mean_band": mean, "any_blocker": any_blocker,
               "complete": complete, "unscored_count": len(unscored),
               "unscored": sorted(unscored, key=nat),
               "dimensions": {k: {kk: vv for kk, vv in r.items()} for k, r in dim_results.items()},
               "grant": grant_res, "prioritized_gaps": [c for _, c in prio]}
        print(json.dumps(out, indent=2))
        return

    meta = data.get("meta", {})
    partial = not complete
    print("# Data-Strength Score Report")
    if meta.get("title"): print(f"**Document:** {meta['title']}")
    if meta.get("target_journal"): print(f"**Target:** {meta['target_journal']}")
    if meta.get("domain"): print(f"**Domain:** {meta['domain']}")
    print(f"\n## OVERALL: {g}   (mean band {mean}/5" + (", BLOCKER fired" if any_blocker else "") + ")")
    if partial:
        print("> PARTIAL: some checks unscored — grade is provisional until all checks are set.")
    print("\n## Dimensions\n")
    print("| Dim | Name | Raw | % | Band | Failed |")
    print("|---|---|---|---|---|---|")
    for k, r in dim_results.items():
        pct = f"{round(r['pct']*100)}%" if r["pct"] is not None else "n/a"
        bd = r["band"] if r["band"] is not None else "-"
        fl = ", ".join(sorted(r["failed"], key=nat)) or "-"
        print(f"| {k} | {CHECKS[k]['name']} | {r['raw']}/{r['max']} | {pct} | {bd} | {fl} |")
    if grant_res:
        pct = f"{round(grant_res['pct']*100)}%" if grant_res["pct"] is not None else "n/a"
        print(f"| G | {GRANT['name']} | {grant_res['raw']}/{grant_res['max']} | {pct} | {grant_res['band'] or '-'} | {', '.join(sorted(grant_res['failed'], key=nat)) or '-'} |")
    print("\n## Prioritized gaps (fix top-down)\n")
    if not prio:
        print("None — every scored check is Elite (2).")
    for rank, cid in prio:
        lab, mod = label_of(cid)
        tag = {0: "BLOCKER", 1: "weak(0)", 2: "adequate(1)"}[rank]
        print(f"- **[{tag}] {cid}** — {lab}  _(see {mod})_")


if __name__ == "__main__":
    main()
