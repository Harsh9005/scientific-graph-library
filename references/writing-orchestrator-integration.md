<!-- data-strength-elevator — PROPOSED integration into writing-orchestrator.
This is a design proposal for discussion, NOT an applied change. Nothing in
writing-orchestrator has been modified. Presented so the wiring is concrete when the
user decides to proceed. Modeled on the existing sister-skill integrations:
claim-citation-auditor (Phase 25.5) and self-citation-maximizer (Phase 20.6). -->

# Proposed integration into writing-orchestrator (for discussion)

**Status:** proposal only. `writing-orchestrator/SKILL.md` is unchanged.

## Why it fits a gap the orchestrator has

writing-orchestrator's quality gate is `references/six-dimension-rubric.md` — D1 Evidence
Relevance, D2 Falsifiability, D3 Scope Calibration, D4 Argument Coherence, D5 Exploration
Integrity, D6 Methodological Rigor. That rubric governs **argument rigor**: whether claims are
supported and well-scoped. It does **not** resolve, at figure/statistic/paragraph granularity,
*how the quantitative data is presented and discussed* — bare bars vs dots-on-bars, SEM vs SD,
laundered PK units, missing named benchmark, orphan simulations. A draft can pass D1–D6 and still
be a Weak DS1/DS2 draft. **data-strength-elevator deepens D6** and adds the data-presentation
craft the orchestrator currently leaves to chance.

## Three wiring points (recommended: adopt 1 + 2 first)

### 1. Drafting reference — cheapest, highest leverage (Phases 8 & 15)
Inject the five dimension checklists + the **anti-mis-transfer rule** (`domain-conventions.md` §0)
into the drafting-worker briefs so drafts are born data-strong.
- **Phase 8 (Aims/Outline):** add a **figure-plan** step — for each Aim/result, specify the chart
  primitive, the named benchmark on the axis, the on-plot statistic, and the domain-correct units,
  using `figure-strategy.md` + `domain-conventions.md §A`.
- **Phase 15 (Score-informed drafting):** prepend the DS1–DS5 checklists as drafting Hard Rules
  (mirrors how Rule 56 injects learned lessons). Workers write to the five-beat / three-move
  standard with numbers + named comparators from the start.

### 2. Dedicated audit gate — new Phase 17.6 (after 17.5 adversarial pre-review, before 18 dashboard)
A sister-skill pass modeled on **Phase 25.5** (claim-citation-auditor):
- Dispatch the data-strength 5-dimension audit on the drafted sections; run `score_manuscript.py`.
- Emit `output/data_strength/` (report + scores.json + gap list) and surface the grade + blockers
  in the **Phase 18 Review Dashboard** alongside the six-dimension scores.
- **Advancement rule (proposed):** no DS blocker AND mean band ≥ 3.8 to auto-advance; otherwise
  re-spawn drafting workers with the gap list (Rule 22 retry, max 2), or HALT with the
  accept-with-disclosure / remediate / abort options used elsewhere.
- **state.yaml:** new `phase_17_6_data_strength` block (enabled=true by default; skip only via
  Rule 7 named-phase override, flagged `⚠ no-data-strength-audit` in later checklists).

### 3. Wizengamot remediation axis — later (Phase 25)
Add data-strength as a scored axis the convergence loop optimizes toward, so the converged DOCX
reaches the data-strength target too (not just composite argument score). Deeper coupling; adopt
after 1 + 2 prove out.

## Rubric relationship (no conflict)
data-strength DS1–DS5 **layer under** six-dimension D6; they do not replace D1–D6. Both gates must
pass. Keep the two rubrics as separate files; the orchestrator reads both.

## Caveats
- The orchestrator does not render figures. Phase 17.6 outputs **figure specifications** (what each
  figure must show/prove); rendering stays with sci-figure-gen / gpai-fig / the user.
- Literature touched by any injected worker still obeys the **Universal Literature Tool Rule**
  (Consensus + scite), not this skill.
- If promoted to a mandatory phase, harden with **petrificus** (state.json + verify_phase gates)
  as was done for claim-citation-auditor before it became Phase 25.5.

## Minimal first step (if the user says "just wire the cheap part")
Adopt only **wiring point 1** (drafting reference): add the DS checklists + §0 anti-mis-transfer
rule to the Phase 8 figure-plan and Phase 15 drafting briefs. No new phase, no state schema change,
immediate quality lift, fully reversible.
