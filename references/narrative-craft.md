<!-- data-strength-elevator reference module. Distilled from 5 elite exemplars:
Nat Commun 2024 15:739; Nat Commun 2025 16:2198; Nat Mater 2025 24:1653;
Nat Biotechnol 2025 43:1783; Nat Biotechnol 2025 (Brief Communication).
Benchmarks in section (B) are as-extracted from those papers. READ ALONGSIDE
references/domain-conventions.md — do NOT launder wet-lab defaults onto
dissolution/PK/IVIVC/CFD/PINN work (see anti-mis-transfer rules there). -->

# Results → Discussion → Conclusion Craft: A Benchmarked Reference for Elite Nanomedicine / Drug-Delivery Manuscripts

*Distilled from exhaustive analysis of 5 top-tier papers: Nature Communications ×2 (LNP-RNA ASC wound healing 2024; LNP-RNA SARS-CoV-2 cancer immunity 2025), Nature Materials ×1 (BBB-crossing LNP mRNA), Nature Biotechnology ×2 (BBB-crossing conjugates for ASO delivery; peptibody mRNA for MDR pneumonia).*

This document covers **one dimension only**: the narrative machinery that turns data into prose across Results, Discussion, and Conclusion. It is a reusable module for a manuscript-strengthening skill. Apply it to any nanomedicine / IVIVC / dissolution / PK / CFD paper.

---

## (A) PRINCIPLES

Twelve distilled, non-obvious principles. Each is grounded in what all or most of the 5 exemplars actually did.

**P1 — Write finding-first: the topic sentence (and section header) IS the conclusion.**
Every exemplar led each Results block with an assertion, not a setup. The 2024 wound-healing paper uses findings *as section headers* ("Delivery of saRNA and E3 mRNA complex (SEC)... facilitates prolonged protein production in ASCs"; "CXCL12 DS-ASCs reprogram local immune microenvironment"). A skim of topic sentences alone reproduces the entire argument. Never open a paragraph with "To investigate X, we did Y" and bury the result at the end.

**P2 — The five-beat results paragraph is universal: CLAIM → what-was-done → FIGURE CALL-OUT → QUANTIFIED MAGNITUDE (with ± SD, vs a *named* comparator) → INTERPRETIVE CLAUSE that motivates the next experiment.**
All 5 papers execute this rigidly. The interpretive clause ("indicating…", "suggesting…", "which could be attributed to…") is what chains one experiment to the next and makes the paper read as a single argument rather than a list of assays.

**P3 — Nearly every results sentence carries a number, and magnitude is always expressed relative to a named competitor — never in isolation.**
The exemplars say "4.7-fold greater than MC3" / ">140-fold over ALC-0315" / "four-log reduction (3.3×10⁴ vs 1.1×10⁸ CFU/ml)" — never "improved delivery" or "significantly higher." Fold-change / % / log-reduction / AUC-ratio is the *effect-size currency*. P-value proves it's real; the fold-change proves it *matters*. Report both.

**P4 — Benchmark against the field's approved / gold-standard comparator by name, in the SAME sentence and the SAME figure panel — not a strawman, not "untreated."**
Every paper anchors superiority to a real competitor: FDA-approved lipids MC3 / ALC-0315 / SM-102, ciprofloxacin (the pneumonia paper's headline is literally "outperforms an FDA-approved antibiotic"), or the best prior-art conjugate (Chol-oligo in the ASO paper). "Better than nothing" persuades no one; "7.3-fold better than the current gold standard" clears the bar.

**P5 — Interpretation is distributed, not warehoused. Attach a one-clause mechanistic reading to each result; reserve the standalone Discussion for synthesis, mechanism-argument, literature-positioning, and limitations.**
The Nature Materials and both Nature Biotech Brief Communications *inline* their interpretation at the end of each Results block ("Nature-house compression") and keep the closing text short. The two Nature Communications papers use a fuller Discussion but still front-load a per-result interpretive clause. Either way: never let a data paragraph end on a bare number.

**P6 — Calibrate register: state owned data flatly with strong verbs; hedge inference explicitly and only where warranted.**
All 5 show the same split. Data: "confirmed," "demonstrated," "yielded," "eradicated," "retained 69.0±2.9%." Inference/mechanism: "could be attributed to," "we speculate," "may partially utilize," "suggesting." This calibrated register signals you know which claims your data actually license — a maturity marker editors read instantly.

**P7 — The Discussion opens by restating the gap + the core finding in mechanistic language, then benchmarks explicitly against the field.**
The 2024 paper opens by restating ASCs' "limited protein-generating ability," then states the DIMIT/chirality finding, then benchmarks: "considerably higher mRNA delivery efficiency than MC3, ALC-0315, and SM102, the three state-of-the-art lipid formulations currently approved by the FDA." Restate → mechanize → benchmark, in that order.

**P8 — Argue mechanism by walking the causal chain and tying each step to your own data AND to prior literature — never hand-wave.**
The exemplars trace explicit chains (saRNA → dsRNA → PKR/eIF2α → translational shutdown → E3 rescue; or caveolae + γ-secretase → transcytosis). Each step is cashed out by a dedicated measurement (phospho-PKR flow; inhibitor knockdown %) and cited to prior work. Convert every "this is probably because…" into at least one confirmatory readout.

**P9 — Handle limitations openly, specifically, and constructively — pair each limitation with its mitigation or the experiment you ran to address it.**
The BBB-conjugate paper flags the mouse→human translation gap *with citations* ("Results from mouse brain studies often do not correlate well with those in human brain cells") — which is precisely why they ran the ex vivo human-tissue experiment. Others list concrete, non-boilerplate next steps (GLP tox, dose escalation, repeat dosing, HLA typing, MTD studies). Candid limitation + named mitigation reads as confidence, not weakness.

**P10 — Report honest negatives and non-significant results in prose, not just figures.**
The 2024 paper explicitly states "there were no synergistic therapeutic effects when CXCL12- and HGF-DS-ASCs were combined" and prints "n.s. P=0.0510." The pneumonia paper flags where the inert LNP does *not* differ from PBS. Owning a negative pre-empts the reviewer who would otherwise find it, and it elevates the credibility of every positive claim.

**P11 — Conclusions follow a fixed three-move arc: CAPABILITY/PLATFORM RECAP (mechanistic, one sentence) → QUANTIFIED FEASIBILITY / named next steps → BOUNDED forward-looking impact.**
All 5 "In summary" paragraphs do this. Impact is scaled to the *platform*, not the single result, but stays bounded: "proof-of-concept," "a possible avenue," "new avenue," "promising platform," "provides great promises" — never "cure," never "will transform." The Nature Materials paper's deliberate use of "proof-of-concept" claims generality while conceding pre-clinical status — the exact register top journals reward.

**P12 — Ground the impact claim in a premise already established earlier in the paper; never let it float.**
The 2025 cancer paper's impact hook — "a significant portion of the global population has already received SARS-CoV-2 T cell memory, [so] this strategy provides a new avenue" — is a *logical consequence* of the population-scale premise set in the abstract, not a leap. The impact sentence should be derivable from something the reader already accepted.

---

## (B) BENCHMARKS

Concrete patterns extracted across the 5 papers. Compare your manuscript against these columns.

| Dimension | Paper 1 (NatComm '24, wound) | Paper 2 (NatComm '25, cancer) | Paper 3 (NatMater, BBB-LNP) | Paper 4 (NatBiotech, BBB-conjugate) | Paper 5 (NatBiotech, pneumonia) | **Elite convention** |
|---|---|---|---|---|---|---|
| Format | Full article | Full article | Full article | Brief Communication | Brief Communication | — |
| Main figures | 5 | 6 | 6 | 2 | 2 | 2 (Brief) / 5–6 (full) |
| Effect-size currency | fold-change, % ± SD | fold-change, %, CR-rate | fold-change, % ± SD | fold-change, %ID/g, % knockdown | fold, log-reduction, AUC | **fold / % / log / AUC — never bare "significant"** |
| Numbers per results sentence | ~1 (near-universal) | ~1–2 | ~1 (most sentences) | 1–3 | 2–4 | **≥1 in almost every results sentence** |
| Named FDA/gold-standard benchmark | MC3, ALC-0315, SM102, Regranex | ALC-0315, SM-102 | MC3, ALC-0315, SM-102 | Chol-oligo (best prior art), tofersen | Cipro, SM-102, MC3, ALC-0315 | **Present in nearly every quantitative panel** |
| Headline fold/magnitude vs benchmark | >140-fold, 22-fold | 5.4-fold, 22.0/18.2/7.5-fold | 4.7–14.6-fold, 8.3-fold | 220.5-fold, 66.0-fold, 7.3-fold | 4-log, 5.4-fold AUC | **quoted in-text next to figure call-out** |
| Error bar convention | mean ± SD | mean ± SD | mean ± s.d. | mean ± s.d. | mean ± s.d. | **SD, never silently SEM; stated in every legend** |
| P-value reporting | exact on bars | exact on bars | exact + asterisk key | exact on plots | exact on panels | **Exact P, not just asterisks** |
| Honest n.s. labeled | Yes (P=0.0510) | Yes | Yes | Yes (Fig.2e) | Yes (ED3) | **Non-sig comparisons shown, not hidden** |
| Statistical test matched to design | ANOVA+Dunnett; t-test; Log-rank | +2-way ANOVA; Log-rank | +2-way/Sidak/Fisher LSD; Log-rank | ANOVA+Tukey; t-test | ANOVA+Dunnett; t-test; Log-rank | **Log-rank for survival, ANOVA+post-hoc for multi-group — not ANOVA-for-everything** |
| Orthogonal readouts per core claim | 4 (photo/kinetics/AUC/Log-rank) | 2+ (in vitro + in vivo; AIM + ICS) | 4 (luc/biodist/flow/Cre) | 2 inhibitors × 2 systems; mRNA+protein | 3 (binding/uptake/killing) | **≥2 independent methods per central claim** |
| Honest negative reported in prose | Yes (no HGF/CXCL12 synergy) | Yes | Yes | Yes | Yes (n.s. SM-102) | **At least one explicit negative** |
| Discussion location | Standalone | Standalone | Distributed + Outlook | Distributed + summary | Compressed summary | **Full: standalone; Brief: distributed** |
| Limitations: concrete + mitigation | half-life → sustained delivery | HLA/memory/i.t.-route + fixes | GLP tox, dose-esc, repeat-dose | species gap → human tissue | codon/circRNA, extrapulmonary | **Named, non-boilerplate, each with a fix** |
| Conclusion structure | capability→feasibility→next→broad | recap→2 aspects→bounded impact | recap→agenda→"proof-of-concept" | recap→differentiator→platform | recap→platform→named next→impact | **3-move: recap → feasibility/next → bounded impact** |
| Impact-claim hedge word | "promising platform" | "new avenue," "potential" | "proof-of-concept" | "great promises" | "promising approach" | **Bounded; platform-level, never "cure"** |
| Translational ladder climbed | in vitro→db/db mouse | mouse→2 haplotypes→3 human | cells→mice→2 disease→human ex vivo | mouse→human tissue→ALS | acute→chronic→human lung→MDM | **≥1 rung toward human relevance** |

---

## (C) SCORING CHECKLIST

Run each check against a draft. Score **Elite (2) / Adequate (1) / Weak (0)**. A publication-ready Results→Discussion→Conclusion narrative scores ≥ 22/26.

| # | Check | Elite (2) | Adequate (1) | Weak (0) |
|---|---|---|---|---|
| 1 | **Finding-first topic sentences** | Every results paragraph (and section headers) states the conclusion up front | Most paragraphs lead with the result | Paragraphs open with "To investigate…" and bury the finding |
| 2 | **Five-beat paragraph structure** | Claim→done→figure→magnitude→interpretive clause, consistently | Present but interpretive clause often missing | Data dumped without call-out or interpretation |
| 3 | **Quantitative density** | ≥1 number in nearly every results sentence | ~half of sentences quantified | Qualitative adjectives dominate ("markedly improved") |
| 4 | **Magnitude vs named comparator** | Every effect stated as fold/%/log vs a named gold standard | Fold-changes given but vs vehicle/blank | "Significantly higher" with no magnitude or comparator |
| 5 | **Effect size + P together** | Fold-change/AUC AND exact P co-reported | One or the other | P-value only, or neither |
| 6 | **Register calibration** | Data flat + strong verbs; inference explicitly hedged | Mostly calibrated, occasional overreach | Everything asserted, or everything hedged |
| 7 | **Discussion opens gap+finding+benchmark** | Restates gap, states finding mechanistically, benchmarks by name | Two of three | Opens with generic background recap |
| 8 | **Mechanism argued via causal chain + data + lit** | Explicit chain, each step cashed out + cited | Chain asserted, thin evidence | Mechanism hand-waved |
| 9 | **Limitations concrete + mitigated** | Specific limitations, each paired with a fix/experiment | Limitations listed, no mitigation | Boilerplate or absent |
| 10 | **Honest negatives/n.s. in prose** | Explicit negative(s) narrated + n.s. labeled | n.s. in figures only | Negatives hidden |
| 11 | **Conclusion 3-move arc** | Recap→feasibility/next→bounded impact, all present | Two moves present | Restates abstract or overclaims |
| 12 | **Impact bounded & grounded** | Platform-level, hedged, derivable from an established premise | Bounded but ungrounded | "Cure"/"revolutionize"/floating claim |
| 13 | **Translational/orthogonal reach narrated** | Ladder + convergent evidence explicitly framed in prose | Mentioned in passing | Single readout, single model, unremarked |

---

## (D) BEFORE → AFTER TRANSFORMATIONS

Realistic weak text (invented) → elite-standard rewrite, in nanomedicine / IVIVC / dissolution / PK / CFD contexts.

### Example 1 — Results paragraph (dissolution / IVIVC)

**BEFORE (weak):**
> The optimized nanocrystal formulation showed improved dissolution compared to the control. As shown in Figure 3, drug release was faster and more complete. This suggests the formulation is promising for oral delivery.

*Problems: no finding-first sentence, no numbers, "improved/faster" vs an unnamed control, no interpretive mechanism, floating "promising."*

**AFTER (elite):**
> Reducing the crystal size to 210 ± 12 nm accelerated dissolution to near-completion within the absorption window (Fig. 3a). At 30 min, the F-NC formulation released 88.4 ± 3.1% of drug versus 24.7 ± 4.6% for the unmilled micronized reference and 41.2 ± 2.9% for the marketed comparator (Fanapt-equivalent), a 3.6-fold and 2.1-fold increase, respectively (one-way ANOVA + Dunnett's, P < 0.0001). This magnitude of enhancement is consistent with the ~9-fold gain in specific surface area measured by BET (Fig. 3b), indicating the improvement is surface-area-driven rather than a change in crystalline form (confirmed by unchanged PXRD, Supplementary Fig. 4), and predicts a corresponding rise in the in vivo absorption rate constant tested next.

### Example 2 — Discussion paragraph (PK / mechanism + limitation)

**BEFORE (weak):**
> Our formulation achieved higher bioavailability, which is a good result. The mechanism is likely related to better absorption. More studies are needed in the future to confirm these findings before clinical use.

*Problems: no benchmark, mechanism hand-waved, boilerplate "more studies needed" limitation with no specificity or mitigation.*

**AFTER (elite):**
> The lipid-based formulation raised oral bioavailability to 62.3 ± 5.8%, a 4.1-fold increase over the aqueous suspension and 1.7-fold over the marketed self-emulsifying reference (Neoral-type), placing it above the ~40% threshold generally required for once-daily dosing. We attribute this gain primarily to lymphatic-transport bypass of first-pass metabolism rather than to enhanced solubility alone: co-administration with the chylomicron-flow blocker cycloheximide abolished 71 ± 4% of the AUC advantage (Fig. 5d), reproducing pharmacologically what the lipid vehicle achieves — an orthogonal test that isolates the mechanism rather than inferring it. Two limitations bound this interpretation. First, the fed-state advantage was measured only in fasted rats; because dietary lipid competes for the same pathway, the human food effect must be characterized directly, which motivates the planned fed/fasted crossover study. Second, our IVIVC is a Level A correlation built on three release rates; extending it to a fourth, slower-releasing lot is required before it can support a biowaiver, as recommended by FDA guidance.

### Example 3 — Conclusion paragraph (CFD / in-silico-to-experimental)

**BEFORE (weak):**
> In conclusion, we developed a CFD model that predicts drug deposition well. This model could be very useful and may revolutionize inhaler design in the future. Our approach opens new possibilities for the field.

*Problems: no quantified feasibility, no named next step, unbounded "revolutionize," ungrounded "opens new possibilities."*

**AFTER (elite):**
> In summary, we developed a patient-specific CFD–PBPK model of regional lung deposition that reproduced γ-scintigraphy total-lung deposition to within 8.2% and predicted plasma Cmax to within 14% across three device configurations, validated against an independent in vivo dataset rather than against the model's own training cases. The workflow runs in under 6 h per geometry on a single workstation, making per-patient prediction tractable for formulation screening. Two concrete steps remain before clinical deployment: prospective validation in a ≥ 20-subject cohort spanning mild-to-severe airway obstruction, and coupling to a dissolution sub-model for suspension formulations, where deposition alone does not determine bioavailability. As a proof-of-concept, this work provides a possible route to replace a subset of costly early deposition studies with validated in-silico prediction, and — because the geometry-to-PK pipeline is device-agnostic — extends in principle to nasal and intratracheal delivery.

---

## (E) RED FLAGS

Signs a manuscript is weak on Results→Discussion→Conclusion craft. Each maps to a principle above.

1. **Qualitative-only results sentences** — "markedly improved," "significantly enhanced," "much faster" with no fold-change, %, or ± SD. (Violates P3.)
2. **Comparisons to nothing** — effects stated vs "control," "untreated," or blank instead of a *named* marketed/gold-standard formulation. (P4.)
3. **Setup-first paragraphs** — every block opens "To investigate whether…" and the reader hunts for the result at the end. (P1.)
4. **Orphan data** — a figure/number reported with no interpretive clause; the paragraph ends on a value, not a meaning. (P2, P5.)
5. **P-value theater** — walls of asterisks with no exact P, no effect size, and no error-bar definition; or SEM used silently to shrink error bars. (P3, and Benchmarks row "error bar convention.")
6. **Uniform statistics** — ANOVA (or t-test) applied to everything, including survival/time-to-event data that demands Log-rank; multiple-comparison correction absent. (Benchmarks "test matched to design.")
7. **Single-readout claims** — a central conclusion rests on one assay, one model, one modality, with no orthogonal or cross-model confirmation narrated. (P8, Benchmarks "orthogonal readouts.")
8. **Everything asserted** — no hedging on mechanism/inference; "proves," "demonstrates conclusively" applied to correlational or single-experiment findings. (P6.)
9. **Warehoused, generic Discussion** — opens with textbook background, never benchmarks by name, never walks a causal chain, cites literature only as a wall in the intro. (P7, P8.)
10. **Boilerplate limitations** — "further studies are needed," "future work will explore," with no specific gap and no mitigation; or no limitations at all. (P9.)
11. **Buried or absent negatives** — no honest negative anywhere; every panel "works"; n.s. results appear only in figures, never acknowledged in prose. (P10.)
12. **Overclaiming conclusion** — "cure," "revolutionize," "will transform"; impact scaled to a single result rather than a bounded platform; or an impact sentence that doesn't follow from any premise the paper established. (P11, P12.)
13. **Conclusion = abstract redux** — the closing paragraph merely restates the abstract with no forward-looking arc, no named next step, no calibrated impact register. (P11.)
14. **No translational/rigor register climb** — the paper never signals convergent evidence, a model ladder, or benchmark superiority in the narrative, so a reviewer cannot tell the work is de-risked. (P4, Benchmarks "translational ladder.")

---

*File this as the RESULTS→DISCUSSION→CONCLUSION module. Its companion dimensions (figure strategy, statistics reporting, abstract/intro funnel) live in separate references; cross-reference for benchmark counts, since figure and stats conventions here (SD, exact P, Log-rank, orthogonal readouts) are load-bearing for narrative credibility.*
