<!-- data-strength-elevator reference module — PUBLICATION-READY FIGURE CRAFT.
HARD, checkable standards for turning a correct figure into a SUBMISSION-READY
one. Grounded in the print-legibility / color / typography practice mined from
the 5 exemplars (references/_exemplar_mining/*.md §4) and the user's hard
requirement that every generated figure and table be publication-ready and
cited. READ ALONGSIDE graph-style-library.md (which chart) and
domain-conventions.md (domain-correct units/stats). This module governs HOW the
chosen chart is finished. -->

# Publication-Ready Figure Craft — hard, checkable standards

*A figure is not "done" when it is correct; it is done when it is **submission-ready**: zero text overlap, legible at 100% / print size, typographically matched to the manuscript, on one consistent colorblind-safe theme, per-entity consistent across every display, rendered with consistent line/point weight so every series and data point stays distinguishable, accessible to screen-reader as well as colorblind readers, uniformly scaled across the whole figure suite, coherent as a single visual story, and **cited in the body text**. Each rule below is written to be checked, not admired. The exemplar craft (`_exemplar_mining/*.md §4`) is the evidence base; the entity mapping is instantiated for this manuscript's sunscreen-filter set.*

**Two rules are non-negotiable** — a figure that fails either is not publication-ready: **F-overlap** (zero text overlap) and **F-cite** (every figure/table cited in text).

---

## R1 — ZERO TEXT OVERLAP  *(check: F-overlap — BLOCKER)*

**Rule.** No label, annotation, legend entry, tick label, axis title, panel letter, significance bracket, or data mark may overlap any other text or any data mark. Every glyph is fully legible with clear separation. A single overlap fails the check.

**How to achieve it (in priority order):**
1. **Direct labeling over legends.** Put the category name on the x-tick or beside the line/bar, not in a legend the reader must cross-reference. The exemplars label screen axes directly (DIM1…, TS1–TS70, PB1–10, cell types under each cluster) and reserve legends only for a treatment dimension that repeats across panels (`natcommun2024a §4`, `natbiotech2024 §4`).
2. **Legend outside the axes.** When a legend is unavoidable, place it outside the plot area (right of the panel cluster, declared once per figure and reused), never floating over data (`natcommun2025 §2` shared-legend practice).
3. **Offset with leader lines.** For a crowded annotation, offset the text and draw a thin leader to its target rather than cramming it in place.
4. **Programmatic de-collision.** In matplotlib use `adjustText` (or equivalent) to repel overlapping point labels; stack and **stagger significance brackets** (short brackets low, long spanning bracket high) so multiple comparisons never cross (`natcommun2025 §4`, `natbiotech2025 §4`).
5. **Rotate / shorten tick labels.** Rotate long category labels (the 13-bar and 50–70-bar screens rotate ticks) or replace names with short codes whose identity lives in a table-as-panel (S27) — never shrink type below the R2 floor to make labels fit.
6. **Split, don't cram.** Manage density by splitting into more small panels with shared axes (the Brief-Communication discipline), not by overloading one axis. No panel carries two y-axes unless it is the deliberate dual-axis idiom (S9).

**Why visual inspection alone is not enough (root cause).** The prior overlap check was "render the figure, then look at the PNG." That is unreliable. The rendered PNG is **downsampled** when viewed, and in a dense multi-panel figure each panel is small, so a few-pixel collision — a callout box clipping a bar's value label, a tick from one facet bleeding into the panel beside it — is **invisible to the eye at that scale** even though it is a real defect in the vector output at print size. A real example slipped through exactly this way: a callout box overlapped a bar's "1.4x" value label in a 4-panel figure, and out-of-range log ticks bled between two facing panels — none of it visible on the downsampled raster, all of it caught immediately by a deterministic bounding-box check. **Visual inspection of a downsampled raster is not a valid overlap test.** It stays only as a human backstop; the primary check is programmatic.

**Overlap audit (mandatory — deterministic programmatic audit is the PRIMARY check).**

**A figure is not publication-ready until `assert_no_overlaps` passes AND a zoom-crop of each dense region is inspected.** The programmatic audit is authoritative; the visual zoom-crop is the backstop, never the other way around.

*Primary — deterministic bbox-intersection audit.* After rendering (before saving), use matplotlib's renderer to get the on-canvas bounding box of every visible text/box artist and test all pairs for intersection. Query `fig.canvas.get_renderer()`, call `artist.get_window_extent(renderer)` on every **visible** `Text` artist (titles, axis titles, tick labels, annotations, panel letters, captions), every `Legend` frame, and every annotation `FancyBboxPatch`, then intersect every pair. Rules that keep it correct (no false positives, no misses):

- **Measure the text glyph box, not the arrow-inclusive extent.** For an `Annotation` with an arrow, `get_window_extent()` on the annotation includes the arrow and false-positives against the target it points at. Measure the text sub-artist's box (its glyph extent) — the box you would draw around the characters — not the arrow-inclusive extent.
- **Exclude same-artist pairs** (an artist never overlaps itself) **and exclude a Text vs its own bbox-patch** (an annotation's text legitimately sits inside its own `FancyBboxPatch`; that is not a collision).
- **Skip non-visible / empty artists** (`get_visible()` is False, or empty string) — they have degenerate boxes that create spurious hits.
- **Apply a small tolerance** so two boxes merely touching at the edge (shared axis spine, adjacent ticks) do not register; only genuine interpenetration beyond the tolerance counts.

Reusable snippet — wire `assert_no_overlaps` as a **BUILD-TIME GATE**: call it inside the figure-save path (or immediately before every `fig.savefig(...)`) so the build **FAILS on any overlap** and no overlapping figure can ever be written to disk.

```python
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
    """Visible Text (incl. Annotation text), Legend frames, annotation FancyBboxPatches."""
    out = []
    for ax in fig.get_axes():
        out += [ax.title, ax.xaxis.label, ax.yaxis.label]
        out += list(ax.get_xticklabels()) + list(ax.get_yticklabels())
        for ch in ax.get_children():
            if isinstance(ch, (Text, Annotation, Legend)):
                out.append(ch)
            elif isinstance(ch, FancyBboxPatch):
                out.append(ch)
    out += [t for t in fig.texts if isinstance(t, Text)]  # suptitle, fig-level captions/panel letters
    if fig.legends:
        out += list(fig.legends)
    # keep visible, non-empty artists only
    seen, uniq = set(), []
    for a in out:
        if a is None or id(a) in seen:
            continue
        seen.add(id(a))
        if not a.get_visible():
            continue
        if isinstance(a, Text) and not a.get_text().strip():
            continue
        uniq.append(a)
    return uniq

def _own_bbox_patch(text_artist, patch):
    """True if `patch` is the bbox-patch belonging to `text_artist` (not a collision)."""
    bp = getattr(text_artist, 'get_bbox_patch', lambda: None)()
    return bp is not None and bp is patch

def audit_overlaps(fig, tol_px=1.0):
    """Return list of (labelA, labelB) glyph-box intersections beyond `tol_px`."""
    fig.canvas.draw()  # renderer must exist and layout must be final
    r = fig.canvas.get_renderer()
    arts = _audit_artists(fig)
    boxes = []
    for a in arts:
        try:
            bb = _glyph_bbox(a, r)
        except Exception:
            continue
        if bb.width <= 0 or bb.height <= 0:
            continue
        boxes.append((a, bb))
    hits = []
    for (a, ba), (b, bb) in combinations(boxes, 2):
        if a is b:
            continue                                   # same artist
        if _own_bbox_patch(a, b) or _own_bbox_patch(b, a):
            continue                                   # text vs its own bbox-patch
        inter = ba.intersection(ba, bb)
        if inter is None:
            continue
        if inter.width > tol_px and inter.height > tol_px:
            hits.append((_lbl(a), _lbl(b)))
    return hits

def _lbl(a):
    if isinstance(a, Text):
        return f"Text({a.get_text()!r})"
    return type(a).__name__

def assert_no_overlaps(fig, tol_px=1.0):
    """BUILD-TIME GATE: raise on any overlap so the build fails before save."""
    hits = audit_overlaps(fig, tol_px=tol_px)
    if hits:
        lines = "\n".join(f"  - {x}  <->  {y}" for x, y in hits)
        raise AssertionError(f"Figure overlap audit FAILED ({len(hits)} collision(s)):\n{lines}")

# Wire as a build-time gate — no figure is saved until the audit passes:
#   assert_no_overlaps(fig)      # raises AssertionError -> build fails on any overlap
#   fig.savefig(path, dpi=300)
```

*Backstop — human-visible zoom-crop.* After `assert_no_overlaps` passes, **zoom-crop each dense region and read it**: crop each multi-panel cluster / crowded axis to that region alone and inspect it at high magnification (use the preview/screenshot tools to render and read the crop), rather than eyeballing the whole downsampled figure. This catches semantic problems the bbox audit cannot (a label that is separated but ambiguous, a leader line pointing at the wrong bar). It is a backstop, not the test of record.

Record BOTH results in the strengthening report: the `assert_no_overlaps` pass/fail (with any reported collisions) and the zoom-crop inspection. A figure whose build did not run `assert_no_overlaps`, or whose dense regions were not zoom-cropped and read, is treated as **failing F-overlap** regardless of how it looks at full size.

---

## R2 — READABLE AT 100% ZOOM / PRINT SIZE  *(check: F-zoom)*

**Rule.** All text must be legible when the figure is placed at its **intended print width**, not only when zoomed in on screen. Minimum on-figure font sizes, stated in **points at ~85 mm single-column width** (the Nature column the exemplars target, `§4` in every mining file, ~5–8 pt house sizes):

| Element | Minimum at ~85 mm column |
|---|---|
| Axis tick labels | ≥ **7 pt** |
| Axis titles (with units) | ≥ **8 pt** |
| Annotations / P-values / data labels | ≥ **8 pt** |
| Panel letters (bold lowercase a, b, c…) | ≥ **8 pt** |
| Legend / key text | ≥ **7 pt** |

At a wider double-column (~170 mm) placement, scale up proportionally; the floor is defined by the *final placed width*, so if a figure will be printed small, its text must still clear these sizes there.

**Export.** Raster figures at **≥ 300 dpi** (600 dpi for line art / gels); prefer **vector** (PDF/EPS/SVG) for plots so text stays crisp at any size. State the rule explicitly: **text must be legible at the intended print width, not just when zoomed** — a figure that only reads at 400% zoom fails F-zoom.

**How to verify.** Export at final size and 300 dpi, place it at the target column width, and confirm the smallest text (usually tick labels) is comfortably readable. Units always live in the axis title via scientific-notation multipliers (×10⁶ …) to keep tick labels short and legible (`natmater2024 §4`).

---

## R3 — TEXT STYLE MATCHES THE MANUSCRIPT  *(check: F-style)*

**Rule.** The figure font **family and weight** are consistent with the document's typography, and **identical across ALL figures**. If the manuscript body is a sans-serif (Nature house = Helvetica/Arial family, `§4` every mining file), every figure uses that same family; panel letters are **bold lowercase** in the Nature convention. Do not mix a serif figure with a sans-serif manuscript, and do not let Figure 3 use a different font than Figure 1.

**How to achieve it.** Set the font once in a shared style/rc file (e.g., a matplotlib `rcParams` block or a stylesheet) and import it into every figure script so typography cannot drift panel-to-panel. Sentence-case axis titles with units in parentheses, matching the exemplars.

---

## R4 — ONE CONSISTENT COLORBLIND-SAFE THEME  *(check: F-theme)*

**Rule.** Define **ONE manuscript-wide palette, once**, and reuse it unchanged in every figure. The palette is **colorblind-safe** (default: **Okabe-Ito**), and **one accent color is reserved for the key finding** — the hero condition/watch-item gets the single warmest saturated hue, held fixed everywhere (the exemplars reserve red for the winner in every panel; `natbiotech2024 §3`, `natcommun2025 §3`). Controls stay neutral grey; the benchmark/comparator gets one fixed cool hue.

**Okabe-Ito reference palette (colorblind-safe):**

| Role | Color | Hex |
|---|---|---|
| Accent / key finding | orange | `#E69F00` |
| Comparator / benchmark | blue | `#0072B2` |
| Secondary | bluish-green | `#009E73` |
| Tertiary | reddish-purple | `#CC79A7` |
| Quaternary | vermillion | `#D55E00` |
| Quinary | sky-blue | `#56B4E9` |
| Senary | yellow | `#F0E442` |
| Control / baseline | grey | `#999999` |
| Reference / identity line | black dashed | `#000000` |

**How to achieve it.** Put the palette in the same shared style file as the fonts (R3). Never introduce a new color for an entity already colored elsewhere. Color is **reinforcement, never the sole channel** — always back it with position + a direct text label + (for points) a marker shape, so a colorblind reader loses nothing (every mining file makes this point; the green↔red pairing in `natcommun2024a §3` is flagged as *not* deutan-safe, which is why the Okabe-Ito default swaps to orange/blue).

**Journal color cycles (opt-in — colorblind-GATED).** Official publisher cycles are available (hex ported from `ggsci` / `ggprism`; their code is GPL-3 and NOT used — hex values are facts). **Okabe-Ito remains the default because most journal cycles are NOT verified colorblind-safe.** Use a journal cycle only if the venue demands it AND you keep the R5 redundancy (position + direct label + marker/shape). `choose_graph.py --journal <name>` returns the cycle and **warns when it is not CB-safe**.

| Cycle | First hexes | CB-safe? | Use rule |
|---|---|---|---|
| **Okabe-Ito** (default) | `#E69F00 #0072B2 #009E73 #CC79A7 #D55E00 #56B4E9 #F0E442` | ✅ yes | default everywhere |
| **Prism-CB** (GraphPad look) | `#000000 #FF0066 #107F80 #40007F #AA66FF #66CCFE` | ✅ yes | biomedical audiences wanting the Prism aesthetic |
| NPG (Nature) | `#E64B35 #4DBBD5 #00A087 #3C5488 #F39B7F …` | ⚠ no (red↔green) | only with full R5 redundancy, else prefer Okabe-Ito |
| AAAS (Science) | `#3B4992 #EE0000 #008B45 #631879 …` | ⚠ no | verify / add redundancy |
| NEJM | `#BC3C29 #0072B5 #E18727 #20854E …` | ⚠ no | verify / add redundancy |
| Lancet | `#00468B #ED0000 #42B540 #0099B4 …` | ⚠ no | verify / add redundancy |
| JAMA | `#374E55 #DF8F44 #00A1D5 #B24745 #79AF97 …` | ⚠ safer (muted, lightness-separated) but verify | verify / add redundancy |

For a 2D field / heatmap the cycle is irrelevant — use a **sequential, perceptually-uniform** map (viridis/cividis), never jet/rainbow (AP12; `graph-style-library.md` S40).

---

## R5 — PER-ENTITY CONSISTENCY (same color AND marker/shape everywhere)  *(check: F-entity)*

**Rule.** The **same entity** (API / molecule / condition / arm) gets the **same color AND the same marker/shape (and hatch)** in **every figure and every table** of the manuscript. Assign the mapping ONCE at first appearance and never reassign it. Marker/shape is a second, colorblind-robust channel that must also be consistent — not just color. Jittered points inherit their bar's color so entity identity survives even in the point cloud (`natbiotech2025 §3`).

**Template — fill once, reuse everywhere.** The author completes this table at the start and every figure/table script reads from it:

| Entity | Color (hex) | Marker / shape | Hatch (if bars overlap in B/W) | Role |
|---|---|---|---|---|
| _(entity 1)_ | | | | |
| _(entity 2)_ | | | | |
| _(control)_ | `#999999` grey | — | — | baseline |
| _(reference/identity line)_ | `#000000` black dashed | — | — | reference |
| _(base-case, models)_ | `#999999` grey | — | — | base-case |

**Concrete mapping for THIS manuscript (sunscreen-filter set — instantiated, reuse verbatim):**

| Entity | Color | Marker | Role |
|---|---|---|---|
| **oxybenzone** | orange `#E69F00` | ● circle | **accent = watch-item / key finding** |
| octinoxate | blue `#0072B2` | ◆ diamond | comparator |
| octocrylene | green `#009E73` | ■ square | comparator |
| octisalate | reddish-purple `#CC79A7` | ▲ triangle | comparator |
| reference / identity line | black dashed | — | reference / y = x |
| base-case (model) | grey `#999999` | — | base-case |

Oxybenzone is the accent because it is the watch-item; it is orange + circle in **every** figure and **every** table (including any parity, tornado, or profile panel). Octinoxate is always blue + diamond, octocrylene always green + square, octisalate always reddish-purple + triangle. Identity/reference lines are always black dashed; the model base-case is always grey. A reader learns the code once and reads the whole manuscript fluently.

**How to verify.** Cross-check every display against the mapping table: if oxybenzone is orange-circle in Fig 2 but appears red or as a square in Fig 5 or in Table 1, F-entity fails.

---

## R6 — MANDATORY CITATION: every figure and table is called out in the text  *(check: F-cite — BLOCKER)*

**Rule.** EVERY generated figure and table MUST be **cited (called out) in the manuscript body text** at the point in the argument it supports (e.g., "…a 1.6-fold increase over the reference product (Fig. 3b)."). An **uncited display is a defect** — it means the figure is either unmotivated or the text has a gap. This applies to main figures, supplementary/extended figures, and every table.

**How to verify (F-cite check).** Build a cross-reference ledger: for each display item, find its in-text callout and the sentence it supports. Any display with **zero** in-text callouts fails F-cite. Any callout that points to the wrong panel (says Fig. 3b but the data are in 3c) is also a defect. The exemplars anchor every figure to a quantified claim in prose ("220.5-fold higher," "four-log reduction") that names the panel — the number and the panel reinforce each other (`natbiotech2024 §5`).

---

## R7 — CONSISTENT LINE/POINT WEIGHT; DATA POINTS DISTINGUISHABLE  *(check: F-lineweight)*

**Rule.** Line weights, marker sizes, error-bar caps, and axis-spine/tick weights are **consistent within and across every figure**, and no data point or series is lost to overplotting. A reader must be able to tell adjacent series apart and resolve individual points — not squint at a tangle of same-weight lines or a solid blob of overlapping markers.

**How to achieve it.**
1. **One weight vocabulary, set once.** Fix a small ladder in the shared style file (R3): e.g. data lines ~1.2–1.5 pt, reference/identity line ~1.0 pt dashed, axis spines ~0.8 pt, error-bar caps ~0.8 pt — and reuse it in every figure so Figure 3's lines are not visibly heavier than Figure 1's. The exemplars keep stroke weights uniform panel-to-panel (`natmater2024 §4`, `natbiotech2025 §4`).
2. **Separate coincident series by a second channel.** Where two lines run close, differentiate by **line style** (solid / dashed / dotted) AND color AND, at sampled points, marker shape — never by color alone (ties into R4/R5). Curves that cross should differ in dash pattern so a colorblind or greyscale reader still separates them.
3. **Defeat overplotting.** For dense scatter/jittered points, use **transparency (alpha ~0.4–0.7), jitter, or hex/2-D-density binning** so individual observations remain countable rather than fusing into one mass; keep marker size large enough to read (≥ ~3–4 pt) but small enough not to merge. Jittered replicate dots inherit their group's color+shape (`natbiotech2025 §3`).
4. **Cap error bars visibly** and ensure caps do not vanish under marker size; make the point marker and its error bar distinguishable.

**How to verify.** Zoom-crop the densest series region and the densest point cloud: can you (a) trace each line individually, (b) count/resolve individual points, and (c) tell every series apart with color removed (greyscale test)? If any fails, F-lineweight fails. Confirm the weight ladder is identical across figures (no figure with visibly heavier/lighter lines than the rest).

---

## R8 — SCREEN-READER + NON-COLOR ACCESSIBILITY  *(check: F-a11y)*

**Rule.** Every figure is accessible to a **screen-reader user** and to readers who cannot rely on color. This extends R4's colorblind-safety to full accessibility: a text equivalent exists, information is encoded redundantly (never by color alone), and contrast is sufficient.

**How to achieve it.**
1. **Alt-text / described caption.** Every figure carries a concise **text alternative** that states what the figure shows and its finding (not "Figure 3" — e.g. "Bar chart; oxybenzone permeation 1.6× the reference product, individual replicates overlaid"). Supply it as the figure's alt-text on submission and ensure the caption itself conveys the finding in prose so a non-visual reader loses nothing. This reuses the F-cite quantified claim (R6) as the spoken description.
2. **Redundant encoding (never color-only).** Every distinction carried by color is **also** carried by position + a direct text label + marker shape / line style / hatch (R4, R5, R7). A greyscale print of the figure must remain fully interpretable. This is the accessibility face of "color is reinforcement, never the sole channel."
3. **Contrast.** Text and key marks meet a legibility-contrast floor against their background (aim ≥ 4.5:1 for small text); avoid light-on-light tick labels and low-contrast gridlines competing with data.
4. **Accessible export.** Where the venue supports it, export into a **tagged / accessible PDF** with figures given alt-text; at minimum, keep figure text as real text (vector) not rasterized pixels so it is machine-readable (ties to R2 vector preference).

**How to verify.** For each figure: (a) an alt-text/description exists and states the finding; (b) greyscale-convert it — is every series/category still distinguishable? (c) the caption alone conveys the result without the image. Any failure fails F-a11y.

---

## R9 — CONSISTENT SIZE & SCALE ACROSS THE FIGURE SUITE  *(check: F-scale)*

**Rule.** Figures are **scaled consistently** so the reader never needs 200% magnification on one and to zoom out on another. Comparable elements are the **same physical size** across the suite: font sizes for the same role (tick, axis title, panel letter) are identical figure-to-figure, panels of the same kind share dimensions, and the data-ink scale (marker size, line weight, bar width) is uniform. This is the cross-figure companion to R2 (which sets per-figure floors) and R3 (which fixes family/weight): R9 fixes the **sizes** too.

**How to achieve it.**
1. **Fix sizes in the shared style file.** Tick/axis-title/annotation/panel-letter point sizes live in the same rc/style block as fonts and palette (R3/R4), so every figure inherits identical sizes — Figure 1's 7 pt ticks are Figure 5's 7 pt ticks.
2. **Standardize figure/panel dimensions.** Use a small set of canonical widths (single-column ~85 mm, double-column ~170 mm) and consistent panel heights; do not let one figure render at half the linear scale of another such that its text and marks are visibly smaller/larger when both sit at their print width.
3. **Consistent element scale.** Marker sizes, line weights (R7), and bar widths are uniform across figures showing comparable data, so nothing needs re-zooming to read.

**How to verify.** Place all figures at their intended print widths side by side: do the same-role text elements appear the **same size**? Do comparable panels have comparable dimensions? If one figure reads only at 200% while another needs zooming out, F-scale fails.

---

## R10 — SINGLE-STORY VISUAL COHERENCE (the suite reads as one narrative)  *(check: F-suite)*

**Rule.** The figures **look like they belong to one paper telling one story**. Taken as a set, they share a consistent visual grammar (palette, entity mapping, typography, sizing, chart idioms) and are ordered so each figure builds on the last toward the central claim. A reader who learns the visual language in Figure 1 reads the whole suite fluently.

**How to achieve it.**
1. **One visual language, everywhere.** F-theme (R4) palette, F-entity (R5) color+shape map, F-style (R3) typography, and F-scale (R9) sizes are held constant across all figures — the four consistency checks are what *produce* single-story coherence.
2. **Repeated chart idioms for repeated questions.** The same kind of analytical question uses the same chart primitive throughout (e.g. every dose–response is the same S12 idiom; every parity plot the same S-parity idiom), so form signals meaning consistently (`graph-style-library.md`).
3. **Twinned / paralleled panels.** Panels that differ in one variable (organism, timepoint, dose, readout) share axes, palette, and mirrored layout so the reader learns the panel once and reads its twin free (`natbiotech2025 §64`, `natmater2024 §4` faceted rows).
4. **Deliberate figure order.** The figure sequence traces the argument — setup → mechanism → validation → translation — so the suite has a narrative arc, not a pile of unordered plots.

**How to verify.** Lay the figures out in order and ask: do they look like one paper (same palette/type/sizing/idioms), and does the sequence build one argument? If a figure looks like it came from a different manuscript, or the order does not advance a story, F-suite fails.

---

## R11 — PUBLICATION-READY GATE (the figure is not "done" until it passes)

A figure/table is **submission-ready** only when it passes ALL of:

- [ ] **F-overlap** — deterministic `assert_no_overlaps(fig)` bbox-intersection audit passes (wired as a build-time gate before save) AND each dense region zoom-cropped and read as backstop; zero text/mark overlaps. Visual-only inspection does NOT satisfy this check. *(BLOCKER)*
- [ ] **F-zoom** — exported ≥ 300 dpi (or vector); every text element clears the R2 point floors at the intended print width.
- [ ] **F-style** — font family/weight matches the manuscript and is identical across all figures.
- [ ] **F-theme** — one manuscript-wide colorblind-safe palette; accent reserved for the key finding.
- [ ] **F-entity** — every entity has the same color + marker/shape in every figure AND table, per the R5 mapping.
- [ ] **F-lineweight** — consistent line/marker weights across figures; every series and data point is distinguishable (no overplotting; passes the greyscale-separation test).
- [ ] **F-a11y** — screen-reader accessible: alt-text/described caption states the finding, information encoded redundantly (not color-only), contrast sufficient, text kept as real (vector) text.
- [ ] **F-scale** — same-role text and elements are the same size across the suite; no figure needs 200% magnification while another needs zooming out.
- [ ] **F-suite** — the figures share one visual language and a deliberate order, reading as a single story.
- [ ] **F-cite** — every figure and table is called out in the body text at the point it supports. *(BLOCKER)*

Plus the core correctness checks (points-on-bars, benchmark-on-axis, SD/n defined, the right chart primitive) and the domain-correctness gate from `domain-conventions.md` (no laundered wet-lab defaults). A figure that is correct but fails any gate item is **not done**; F-overlap and F-cite are the two that make a figure unusable if missed.

**Reporting.** Record the R11 checklist result per figure. State honestly which items passed on inspection versus which need the author's source files (e.g., "F-zoom cannot be confirmed until the vector export is regenerated at 300 dpi").

---

## R12 — JOURNAL STYLE ENGINES (apply the rules, don't re-hand-code them)  *(implementation aid — not a gate)*

**Rule.** The R2/R3/R4 typography-size-and-color rules are already implemented by maintained, journal-calibrated matplotlib style packages — use one as the shared style file (R3) instead of re-setting rcParams by hand. This is a helper, not a new gate; the F-checks still decide.

- **SciencePlots** (MIT — freely usable). Pre-built `.mplstyle` for the exact house rules: ticks-inward, thin 0.5 pt axes, physical single-column sizing, sans-serif at Nature's ~7 pt.
  - Nature: `plt.style.use(['science','nature','no-latex'])` → 3.3×2.5 in, 7 pt, sans-serif (DejaVu/Arial/Helvetica).
  - IEEE: `plt.style.use(['science','ieee','no-latex'])` → 600 dpi, B/W-safe line-style cycler.
  - Base science: `plt.style.use(['science','no-latex'])` (serif).
  - **Caveat (state honestly):** the base `science` style sets `text.usetex:True` and needs a LaTeX install (TeX Live); the **`no-latex` overlay removes that dependency** — include it unless you have LaTeX and want LaTeX math. `pip install SciencePlots`.
- **ultraplot** (MIT — active `proplot` fork) for multi-panel layout: `import ultraplot as uplt; fig, axs = uplt.subplots(ncols=…, nrows=…, abc=True, share=3)` gives **automatic a/b/c panel letters** (F-style/R3 convention), shared/spanning axes, unified `fig.colorbar`/`fig.legend`, and figure sizing in **mm/cm** (so R2's 89 mm column is a direct spec). `pip install ultraplot`.

Use `choose_graph.py` to get the right engine + palette for a target journal in one call. These packages implement the rules; they do **not** replace the R7/R11 gate — a SciencePlots figure still passes the overlap audit, F-cite, and the six-part consistency test.

---

*Reference — publication-ready figure craft. Grounded in the print-legibility / color / typography practice mined from the 5 exemplars (`_exemplar_mining/*.md §4`), extended with journal style-engines (SciencePlots, ultraplot) and colorblind-gated journal color cycles (ggsci/ggprism hex). F-overlap and F-cite are the two non-negotiable checks.*
