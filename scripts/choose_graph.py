#!/usr/bin/env python3
"""choose_graph.py — deterministic chart + analysis-method chooser for data-strength-elevator.

Queries scripts/graph_catalog.json (the single machine-readable index) and returns a RANKED
short-list of graph styles for a stated analytical intent, PLUS the palette + journal style-engine
to apply, the anti-patterns it REJECTS for this case, the rules it REQUIRES, and the matching
statistical method. The point is to DECIDE and cite the rule, not to browse the library.

The rubric/skill is unchanged by this tool: it operationalises the existing graph-style-library.md,
publication-ready-figures.md, statistics-rigor.md, and domain-conventions.md — it does not add checks.

Usage:
  choose_graph.py --intent "compare means" [--data categorical] [--n 4] [--domain PK]
                  [--journal nature|science|ieee|npg|aaas|nejm|lancet|jama|prism] [--top 4] [--json]

Exit 0 always (advisory tool). Reads the catalog beside this script.
"""
import argparse, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "graph_catalog.json")

# intent synonyms -> canonical intent tokens used in the catalog
SYN = {
    "means": "compare", "comparison": "compare", "vs": "compare", "versus": "compare",
    "spread": "distribution", "variation": "distribution", "raw": "distribution",
    "predicted": "agreement", "observed": "agreement", "calibrate": "calibration",
    "validate": "agreement", "validation": "agreement", "accuracy": "agreement",
    "timecourse": "time_course", "time-course": "time_course", "kinetic": "kinetics",
    "over_time": "time_course", "release": "time_course", "profile": "time_course",
    "parts": "composition", "proportion": "composition", "whole": "composition",
    "rank": "ranking", "importance": "sensitivity", "driver": "sensitivity",
    "surface": "field", "flow": "field", "spectrum": "spectral", "frequency": "spectral",
    "reduce": "dimensionality", "pca": "dimensionality", "svd": "dimensionality",
    "cluster": "clustering", "dose": "dose_response", "exposure": "exposure",
    "survival": "survival", "classify": "classification", "roc": "classification",
    "convergence": "convergence", "mesh": "convergence", "loss": "convergence",
    "magnitude": "magnitude", "effect": "magnitude",
}


def norm_tokens(text):
    toks = re.split(r"[\s,/;]+", (text or "").lower().strip())
    out = []
    for t in toks:
        if not t:
            continue
        c = SYN.get(t, t)
        if c not in out:          # dedupe so synonyms ("compare means") don't double-count
            out.append(c)
    return out


def load_catalog():
    with open(CATALOG, encoding="utf-8", errors="ignore") as f:
        return json.load(f)


def score_style(s, intents, datas, domain, n):
    """Return (score, reasons, excluded_reason_or_None)."""
    score, reasons = 0, []
    si = set(s.get("intent", []))
    for t in intents:
        if t in si:
            score += 3; reasons.append(f"intent:{t}")
    sd = set(s.get("data_structure", []))
    for t in datas:
        if t in sd:
            score += 2; reasons.append(f"data:{t}")
    df = s.get("domain_fit", {}) or {}
    if domain and domain in df:
        v = str(df[domain])
        if "required" in v:
            score += 4; reasons.append(f"domain:{domain}={v}")
        else:
            score += 2; reasons.append(f"domain:{domain}={v}")
    # min-n exclusion (e.g. violin/box at small n -> AP2)
    minn = s.get("min_n", 0) or 0
    if n is not None and minn and n < minn:
        return (score, reasons, f"n={n} < min_n={minn} for {s['id']} ({s.get('note','')})")
    return (score, reasons, None)


def triggered_rules(rules, intents, datas, domain, n, journal, palette_obj):
    """Deterministic trigger logic keyed by rule id; message/ref pulled from the catalog."""
    by = {r["id"]: r for r in rules}
    fired = []

    def add(rid):
        r = by.get(rid)
        if r:
            fired.append({"id": rid, "enforce": r["enforce"], "ref": r.get("ref", "")})

    iset, dset = set(intents), set(datas)
    if iset & {"compare", "magnitude"} and "categorical" in dset:
        add("R-bars")
    if n is not None and n < 20 and ("distribution" in iset or "categorical" in dset):
        add("R-violin-n")
    if iset & {"magnitude", "field", "sensitivity"}:
        add("R-diverging")
    if "compositional" in dset or "composition" in iset:
        add("R-partsofwhole")
    if iset & {"field", "overview", "sensitivity"} and (dset & {"matrix", "field_2d"}):
        add("R-heatmap")
    if "compare" in iset and n is not None and n > 12:
        add("R-bar-meadow")
    if iset & {"compare", "magnitude"} and "categorical" in dset:
        add("R-zerobase")
    if domain == "PK" and (iset & {"exposure", "compare", "magnitude"}):
        add("R-PK")
    if domain == "dissolution":
        add("R-dissolution")
    if domain in {"CFD", "PINN", "IVIVC"} and (iset & {"agreement", "calibration", "convergence"}):
        add("R-modelval")
    if palette_obj and not palette_obj.get("colorblind_safe", False) and journal:
        add("R-palette")
    return fired


JOURNAL_ENGINE = {"nature": "scienceplots_nature", "science": "scienceplots_science",
                  "ieee": "scienceplots_ieee"}
JOURNAL_PALETTE = {"npg": "npg", "aaas": "aaas", "nejm": "nejm", "lancet": "lancet",
                   "jama": "jama", "prism": "prism_colorblind_safe"}


def main():
    ap = argparse.ArgumentParser(description="Deterministic chart + analysis-method chooser")
    ap.add_argument("--intent", required=True, help="e.g. 'compare means', 'distribution', 'predicted vs observed', 'field', 'dimensionality', 'PK exposure'")
    ap.add_argument("--data", default="", help="categorical|continuous|continuous_paired|time_series|time_to_event|field_2d|matrix|signal|high_dim|compositional|ordinal|scores|state_space|discrete")
    ap.add_argument("--n", type=int, default=None, help="sample size per group (enables AP2/AP15 small-n rejects)")
    ap.add_argument("--domain", default="general", help="general|dissolution|PK|PBPK|IVIVC|CFD|PINN|BE")
    ap.add_argument("--journal", default="", help="nature|science|ieee (style engine) | npg|aaas|nejm|lancet|jama|prism (palette)")
    ap.add_argument("--top", type=int, default=4)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    cat = load_catalog()
    intents = norm_tokens(a.intent)
    datas = norm_tokens(a.data)
    domain = a.domain.strip() if a.domain else "general"
    journal = a.journal.strip().lower()

    ranked, excluded = [], []
    for s in cat["styles"]:
        sc, reasons, excl = score_style(s, intents, datas, domain, a.n)
        if excl:
            if sc > 0:
                excluded.append({"id": s["id"], "name": s["name"], "reason": excl})
            continue
        if sc > 0:
            ranked.append((sc, s, reasons))
    ranked.sort(key=lambda x: (-x[0], x[1]["id"]))
    top = ranked[:a.top]

    # palette
    pal_key = JOURNAL_PALETTE.get(journal, "okabe_ito")
    palette = dict(cat["palettes"][pal_key]); palette["key"] = pal_key
    # engine
    eng_key = JOURNAL_ENGINE.get(journal, "scienceplots_nature")
    engine = dict(cat["style_engines"][eng_key]); engine["key"] = eng_key

    fired = triggered_rules(cat["decision_rules"], intents, datas, domain, a.n, journal, palette)

    # stat method: from the top styles' 'stat', else infer from intent
    stat_key = next((s["stat"] for _, s, _ in top if s.get("stat")), None)
    if not stat_key:
        infer = {"exposure": "PK_exposure", "survival": "survival", "agreement": "agreement_pred_obs",
                 "dimensionality": "dimensionality", "classification": "classifier_perf",
                 "dose_response": "dose_response", "compare": "compare_multi_groups"}
        for t in intents:
            if t in infer:
                stat_key = infer[t]; break
    stat = {"key": stat_key, **cat["stat_methods"][stat_key]} if stat_key else None

    result = {
        "query": {"intent": a.intent, "data": a.data, "n": a.n, "domain": domain, "journal": journal},
        "recommended_styles": [{"id": s["id"], "name": s["name"], "score": sc,
                                "why": reasons, "requires": s.get("requires", []),
                                "note": s.get("note", "")} for sc, s, reasons in top],
        "rejected_for_this_case": excluded,
        "enforced_rules": fired,
        "palette": {"key": palette["key"], "colorblind_safe": palette.get("colorblind_safe"),
                    "hex": palette.get("hex"), "note": palette.get("note")},
        "style_engine": {"key": engine["key"], "apply": engine.get("apply"),
                         "caveat": engine.get("caveat", ""), "note": engine.get("note", "")},
        "multi_panel": cat["style_engines"]["ultraplot_multipanel"]["apply"],
        "statistical_method": stat,
    }

    if a.json:
        print(json.dumps(result, indent=2)); return

    q = result["query"]
    print(f"# DECISION — intent='{q['intent']}' data='{q['data']}' n={q['n']} domain={q['domain']}"
          + (f" journal={q['journal']}" if journal else ""))
    if not top:
        print("\n⚠ No style matched. Broaden --intent/--data, or consult graph-style-library.md GROUP index.")
    print("\n## Recommended styles (ranked)")
    for r in result["recommended_styles"]:
        print(f"  {r['id']}  {r['name']}   [{', '.join(r['why'])}]")
        if r["requires"]:
            print(f"        REQUIRES: {'; '.join(r['requires'])}")
        if r["note"]:
            print(f"        note: {r['note']}")
    if excluded:
        print("\n## Rejected for this case")
        for r in result["rejected_for_this_case"][:6]:
            print(f"  {r['id']}  — {r['reason']}")
    if fired:
        print("\n## Rules enforced (follow these for a best-outcome figure)")
        for r in fired:
            print(f"  [{r['ref']}] {r['enforce']}")
    p = result["palette"]
    tag = "colorblind-safe" if p["colorblind_safe"] else "⚠ NOT verified colorblind-safe"
    print(f"\n## Palette: {p['key']} ({tag})\n  {p['note']}")
    e = result["style_engine"]
    print(f"\n## Style engine: {e['key']}\n  apply: {e['apply']}")
    if e["caveat"]:
        print(f"  caveat: {e['caveat']}")
    print(f"  multi-panel (a/b/c, shared axes, mm sizing): {result['multi_panel']}")
    if stat:
        print(f"\n## Statistical method: {stat['key']}\n  {stat['method']}\n  see: {stat['see']}")


if __name__ == "__main__":
    main()
