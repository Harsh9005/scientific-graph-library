#!/usr/bin/env python3
"""sweep_rng_robustness.py — prove every gallery figure stays overlap-clean under different random draws.

Why this exists. The gallery shares ONE seeded RNG (`generate_gallery.RNG`) consumed in registry order,
so a figure's data depends on WHERE it sits in the registry. Insert a new figure and every later figure
gets different draws — and a layout tuned to one draw can collide under another. A single clean build
therefore proves the current arrangement is fine, not that the figures are robust.

This re-seeds the module RNG and re-renders every figure N times, running the F16 overlap audit on each
render and reporting any figure that ever collides. It writes NO files and never touches png/ or pdf/,
so it is safe to run at any time.

Run:  python3 sweep_rng_robustness.py [--trials 5] [--category Distributions]

Exit 0 if every figure is clean in every trial; exit 1 if any figure ever collided (so it can gate CI).
Cost: one render per figure per trial — ~132 x N renders, so start with the default N.
"""
import argparse
import sys
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt

import generate_gallery as G
from _figure_qc import audit_overlaps_detailed


def main():
    ap = argparse.ArgumentParser(description="RNG-robustness sweep over the gallery")
    ap.add_argument("--trials", type=int, default=5, help="how many different random draws to test (default 5)")
    ap.add_argument("--category", default="", help="limit to one category")
    ap.add_argument("--base-seed", type=int, default=20260706)
    a = ap.parse_args()

    registry = G.REGISTRY
    if a.category:
        registry = [fn for fn in G.REGISTRY if G._category_of(fn) == a.category]
        if not registry:
            print(f"No figures in category '{a.category}'.")
            return 0

    G.set_style()
    collisions = {}   # figure name -> set of trial indices
    errors = {}       # figure name -> first error repr
    captured = {}     # id(fn) -> name, learned from the save() interception

    real_save = G.save

    def probe_save(fig, name, note, cat):
        captured[name] = cat
        try:
            hits = [h for h in audit_overlaps_detailed(fig) if h["actionable"]]
            if hits:
                collisions.setdefault(name, set()).add(probe_save.trial)
        except Exception:
            pass
        plt.close(fig)          # audit only — deliberately do NOT write PNG/PDF

    G.save = probe_save
    try:
        for t in range(a.trials):
            probe_save.trial = t
            G.RNG = np.random.default_rng(a.base_seed + t)
            for fn in registry:
                try:
                    fn()
                except Exception as e:
                    errors.setdefault(fn.__name__, repr(e))
            print(f"  trial {t + 1}/{a.trials} done "
                  f"({len(registry)} figures, {len(collisions)} figure(s) collided so far)")
    finally:
        G.save = real_save

    print(f"\nSWEEP: {len(registry)} figures x {a.trials} draws = {len(registry) * a.trials} renders")
    if errors:
        print(f"\n{len(errors)} figure(s) RAISED:")
        for n, e in errors.items():
            print(f"  ✗ {n}: {e}")
    if collisions:
        print(f"\n{len(collisions)} figure(s) collided in at least one draw (F16):")
        for n, trials in sorted(collisions.items()):
            print(f"  ! {n}: {len(trials)}/{a.trials} draws")
        print("\nA figure listed here is fragile: it is clean at its current registry position but will\n"
              "collide if the shared RNG stream shifts (i.e. as soon as a figure is added before it).")
        return 1
    if errors:
        return 1
    print("clean — every figure passed the overlap audit under every draw")
    return 0


if __name__ == "__main__":
    sys.exit(main())
