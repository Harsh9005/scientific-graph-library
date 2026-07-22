#!/usr/bin/env python3
"""_figure_qc.py — deterministic publication-ready QC gate for gallery figures.

Implements the skill's F16 F-overlap blocker (references/publication-ready-figures.md R1):
a bbox-intersection audit over every visible Text / Legend / annotation box, so a figure
with colliding labels can be caught programmatically instead of by eyeballing a downsampled
PNG. Import `assert_no_overlaps(fig)` (raises on collision) or `audit_overlaps(fig)` (returns
the collision list) and call it after layout is final, immediately before `fig.savefig(...)`.

Source: verbatim from references/publication-ready-figures.md R1 (the skill's own standard),
extracted here as a reusable module so the gallery generator and any figure script can gate on it.
No external dependencies beyond matplotlib.
"""
from itertools import combinations
from matplotlib.text import Text, Annotation
from matplotlib.legend import Legend
from matplotlib.patches import FancyBboxPatch


def _glyph_bbox(artist, renderer):
    """On-canvas box of the glyphs/frame only — never the arrow-inclusive extent."""
    if isinstance(artist, Annotation):
        # The arrow inflates get_window_extent -> measure the text glyphs only.
        return Text.get_window_extent(artist, renderer)
    return artist.get_window_extent(renderer)


def _audit_artists(fig):
    """Visible Text (incl. Annotation text), Legend frames, annotation FancyBboxPatches.

    Returns a list of (artist, role) pairs. `role` lets a caller tier the report — a title or
    legend collision is a craft defect, whereas two tick labels touching at a panel boundary is
    layout density. Artists belonging to an axes with the axis turned off (`ax.axison is False`)
    are skipped: matplotlib leaves their `visible` flag True even though they are never drawn,
    which would otherwise report phantom collisions (e.g. theta labels on a `set_axis_off` polar).
    """
    out = []
    for ax in fig.get_axes():
        axis_on = getattr(ax, "axison", True)
        if axis_on:
            out += [(ax.title, "title"), (ax.xaxis.label, "axis-label"), (ax.yaxis.label, "axis-label")]
            out += [(t, "tick") for t in list(ax.get_xticklabels()) + list(ax.get_yticklabels())]
        else:
            out += [(ax.title, "title")]  # a title still renders with the axis off
        for ch in ax.get_children():
            if isinstance(ch, Legend):
                out.append((ch, "legend"))
            elif isinstance(ch, (Text, Annotation)):
                out.append((ch, "text"))
            elif isinstance(ch, FancyBboxPatch):
                out.append((ch, "box"))
    out += [(t, "text") for t in fig.texts if isinstance(t, Text)]  # suptitle, panel letters
    if fig.legends:
        out += [(lg, "legend") for lg in fig.legends]
    seen, uniq = set(), []
    for a, role in out:
        if a is None or id(a) in seen:
            continue
        seen.add(id(a))
        if not a.get_visible():
            continue
        if isinstance(a, Text) and not a.get_text().strip():
            continue
        uniq.append((a, role))
    return uniq


def _own_bbox_patch(text_artist, patch):
    """True if `patch` is the bbox-patch belonging to `text_artist` (not a collision)."""
    bp = getattr(text_artist, 'get_bbox_patch', lambda: None)()
    return bp is not None and bp is patch


def _lbl(a):
    if isinstance(a, Text):
        return f"Text({a.get_text()!r})"
    return type(a).__name__


def audit_overlaps_detailed(fig, tol_px=1.0):
    """Return list of dicts {a, b, role_a, role_b, actionable} for each glyph-box intersection.

    `actionable` is False only when BOTH sides are tick labels — two tick labels touching at a
    panel or colorbar boundary is layout density, not a misreading risk. Every other collision
    (title vs legend, annotation vs tick, label vs label) is a genuine craft defect.
    """
    fig.canvas.draw()  # renderer must exist and layout must be final
    r = fig.canvas.get_renderer()
    boxes = []
    for a, role in _audit_artists(fig):
        try:
            bb = _glyph_bbox(a, r)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        boxes.append((a, role, bb))
    hits = []
    for (a, ra, ba), (b, rb, bb) in combinations(boxes, 2):
        if a is b:
            continue
        if _own_bbox_patch(a, b) or _own_bbox_patch(b, a):
            continue
        inter = ba.intersection(ba, bb)
        if inter is None:
            continue
        if inter.width > tol_px and inter.height > tol_px:
            hits.append({"a": _lbl(a), "b": _lbl(b), "role_a": ra, "role_b": rb,
                         "actionable": not (ra == "tick" and rb == "tick")})
    return hits


def audit_overlaps(fig, tol_px=1.0):
    """Return list of (labelA, labelB) glyph-box intersections beyond `tol_px`."""
    return [(h["a"], h["b"]) for h in audit_overlaps_detailed(fig, tol_px=tol_px)]


def assert_no_overlaps(fig, tol_px=1.0):
    """BUILD-TIME GATE: raise on any overlap so the build fails before save."""
    hits = audit_overlaps(fig, tol_px=tol_px)
    if hits:
        lines = "\n".join(f"  - {x}  <->  {y}" for x, y in hits)
        raise AssertionError(f"Figure overlap audit FAILED ({len(hits)} collision(s)):\n{lines}")
