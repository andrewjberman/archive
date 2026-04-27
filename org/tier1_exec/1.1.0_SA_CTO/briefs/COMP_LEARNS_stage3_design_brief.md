# CTO Brief to CVO — Stage 3 Design (Phase 2 Onset)

**From:** 1.1.0_SA_CTO
**To:** 3.1.0_SA_CVO
**Date:** 2026-04-27T17:00:00Z
**Subject:** Stage 3 design brief — Phase 2 target selection, harness extensions, and the central proposition test
**Brief type:** new_prd (per CTO↔CVO collaborative cycle)
**Predecessor:** Iter-7 reclassification ruling (`org/tier1_exec/3.1.0_SA_CVO/responses/20260427T163500Z_to_1.1.0_SA_CTO_iter7_reclassification_review.md`) + COMP_LEARNS Phase 2 protocol amendment (`docs/architecture/COMP_LEARNS_PHASE2_PROTOCOL_AMENDMENT.md`)

---

## §0 — Convergence reading (what we now know)

Stage 1+2 have produced more than a working harness; they have produced a calibrated theory of what fact-node injection can and cannot do. The four highest-signal findings, ranked:

1. **Strong parametric priors dominate correct injected structure.** Click q03 plateaued across 6 scored iterations and two distinct mutation families (import/class_inherits iters 2-5 + class_hierarchy_* iters 6-7). The compiler emitted both the structural edge topology (`class_inherits` edges in `comp/targets/click/compiler.py:160-192`) and the explicit corrective fact node (Command-perspective + NOT-exclusion in iter-7), and the judge still answered q03 with the wrong subclass set. Per CVO §4 ruling 20260427T163500Z: "closing click is harvesting the actual systems-program insight the target surfaced."

2. **Some "failures" are grader artifacts, not knowledge gaps.** R-SC-1 honesty note (`comp/results/dev-click-001/scoring_regime_honesty_note.md`, commit `7bc3c185`) demonstrated that q11 H3-v2 contains the correct answer ("Answer: 1") in a verbose response but fails the `float(full_response_text)` grader. H3-v2's "8/11" baseline is actually 9/11 minimum under a format-aware grader. Without R-SC-2 ("semantic-correct-but-unparseable" audit label), Phase 2 will conflate model error with format error.

3. **PATTERN C diagnosis is structurally underdetermined without a delivered-context audit.** We could not conclusively prove the iter-6/iter-7 hierarchy node was attended by the judge — only that it was present in the compressed graph (token_reduction stable) and did not change behavior. CVO 20260427T143500Z R-CTO-2 explicitly held attribution provisional: "The brief overstates what is known." Phase 2 needs runner instrumentation to capture exactly what the judge saw per question.

4. **The four-condition comparator (per protocol amendment §3) has not been fully run.** Wave 3b Lane B Cases 1+2 ran two-phase scoring (Phase 1 freeze + Phase 2 metric audit) but the 4-condition C1/C2/C3/C4 split has C2 and C3 unimplemented. Without C2 (mechanical retrieval only) and C3 (index + no addressing), we cannot attribute localization vs. contextualization separately, which is the central distinction the protocol amendment was designed to enable.

These four findings reframe Stage 3 from "scale the proven loop" to "validate the central proposition on a target where it CAN succeed."

---

## §1 — The central proposition test

Per Wave 3 design brief (`org/tier1_exec/1.1.0_SA_CTO/briefs/COMP_LEARNS_wave3_design_brief.md`):

> Does the compiler materially improve the model's ability to find, localize, and act on the correct structural context in a hard codebase, relative to unaided exploration?

Stage 3's job is to test that proposition directly on a target that gives the proposition room to either succeed or fail decisively. Click did not give it that room. Click was a target where the judge's parametric prior on a small, well-known library was strong enough to dominate the compiler's correct structural signal. A null result on click does not falsify the proposition; it tells us the experiment was malformed.

**Stage 3 must select for surfaces where the proposition has measurement room:**

- The judge's parametric prior on the relevant surface must be weak (not "the model knows Click's hierarchy perfectly")
- Cross-file semantic joins must be required (per amendment §1 criterion 2)
- Named entry must not be near the fix site (per amendment §1 criterion 3)
- The target must support 4-condition scoring with C2 + C3 measurable, not just C1 + C4 (per amendment §3)

These four conditions are jointly necessary. None alone is sufficient.

---

## §2 — Phase 2 target candidates

### Sphinx (lead candidate)

**Why:**
- Size: ~65k LOC, satisfies amendment §1 criterion 1 ("wider codebases")
- Architecture: documentation generator with extension/plugin API across multiple modules — cross-module semantic joins are the norm, not the exception (criterion 2 satisfied)
- Named entries (extension hooks, directive classes) are typically far from their fix sites — usage in user docs vs. implementation in core (criterion 3 satisfied)
- Operational familiarity: Wave 3b Case 3 used sphinx as the proving secondary (`.051`) — harness wiring, gold-key generation, and runner config are already validated

**Parametric-prior risk:** Sphinx is well-known but the long tail of extension-internal behavior is less likely to be in training data than Click's class hierarchy. A pre-screen (see §4) would calibrate this before commitment.

### Alternative candidates (lower priority)

- **A recently-released library** (post-training-cutoff): forces low parametric prior by construction. Cost: gold-key generation requires manual curation since no public Q&A exists.
- **An internal codebase fragment**: zero parametric prior. Cost: not reproducible as research; contaminates the program's claim of generality.
- **Domain-specific scientific/finance library**: low online presence, low prior. Cost: gold-key generation requires domain expertise the team doesn't have.

Sphinx is the operational best-bet. Alternatives become relevant only if sphinx pre-screens as parametric-prior-dominated.

---

## §3 — Required harness extensions before Phase 2 begins

Three harness changes are jointly necessary. None can be deferred to "later in Phase 2."

### 3.1 R-SC-2 implementation — semantic-correct-but-unparseable label

**Status:** Queued (per CVO 20260427T163500Z R-SC-2). SC has acknowledged and is implementing.
**Phase 2 dependency:** Hard. Phase 2's per-question attribution requires distinguishing "model wrong" from "format unparseable." Without R-SC-2, every numeric-style question in Phase 2 will reproduce click's q02/q11 ambiguity.

### 3.2 Delivered-context audit instrumentation

**Status:** Not implemented.
**Need:** The runner must capture, per question per condition, the exact compressed context delivered to the judge. Today the runner emits `token_reduction` and `compiler_loc` but no per-question delivered text. PATTERN C diagnosis on click was hampered by the absence of this — we could not prove or disprove that a node survived selector compression to reach the judge.

**Concrete requirement:** Add `delivered_context_text` field to scorecard JSON, per question per condition. Storage cost is bounded (Phase 2 questions × 4 conditions × N iters; ≈ 100s of KB per run, not GB).

### 3.3 H3 full-source baseline as a pre-condition

**Status:** Run ad-hoc on click (`comp/results/dev-click-001/h3_baseline/run_h3_v2.py`) after 4 DISCARDs. Should be run before iteration begins.
**Need:** H3 establishes (a) max theoretical ab_lift, (b) per-question pre-screen for parametric-prior dominance (if judge gets a question right at full source, that question's improvability is bounded by format/grader, not knowledge), and (c) baseline for distinguishing model-prior vs. retrieval-quality contributions.

**Concrete requirement:** New gate in operational mandate: H3-v2 (with format-aware grader per R-SC-2) must run and pass review before any scored iteration begins on a target. Result is committed alongside the gold key.

---

## §4 — Parametric-prior pre-screen (proposed, new)

This is the largest design addition vs. the existing protocol amendment. Click failed because no prior-strength check existed. Stage 3 needs one.

**Proposed pre-screen:**

For each candidate Phase 2 question, run the judge against the question with NO context (zero-shot) and against full-source H3 (full context). Categorize:

| Zero-shot | H3 full | Interpretation | Phase 2 status |
|-----------|---------|----------------|----------------|
| Correct | Correct | Strong parametric prior — surface dominated | EXCLUDE — no measurement room |
| Wrong | Correct | Genuine retrieval gain available | INCLUDE — primary measurement target |
| Wrong | Wrong | Model can't solve even with full source — too hard or grader broken | INVESTIGATE — likely R-SC-2 candidate or genuine ceiling |
| Correct | Wrong | Anomaly (suggests grader artifact or randomness) | INVESTIGATE before inclusion |

This pre-screen would have caught click's q03 BEFORE iteration began. Click q03 zero-shot would correctly answer {_BaseCommand, Group, _MultiCommand, CommandCollection} (it does in H3-v2 — the model knows the full hierarchy from training); H3 with grader fails. The judge "knows" but grades wrong. That's prior-dominated AND format-artifact territory, not retrieval-improvable.

**Cost:** One extra zero-shot call per candidate question, one-time per target. Negligible.

---

## §5 — Stage 3 minimum viable test (MVT)

The smallest experiment that would falsify or validate the central proposition:

1. **Target selection:** Sphinx (or alternative if pre-screen fails it)
2. **Pre-screen:** Run §4 prior calibration on candidate questions; keep only "INCLUDE" questions
3. **Harness gates:** R-SC-2 implemented, delivered-context audit instrumentation shipped, H3 full-source baseline committed
4. **Conditions:** All four — C1 (unaided) + C2 (mechanical retrieval only) + C3 (index + no addressing) + C4 (full two-step). Not C1+C4 minimum.
5. **Scoring:** Per-question per-condition. Aggregate to per-question deltas (C2-C1, C3-C1, C4-C1). Localization gain = C2-C1; addressing gain = C4-C2; contextualization gain = C3-C1.
6. **Iteration:** Standard ratchet on the compiler. Iterate while ab_lift positive across selected questions; stop on PATTERN C across 2 families per existing R-COO-2 stop-rule.

**Decision tree on result:**

| C4 vs C1 | C2 vs C1 | C3 vs C1 | Conclusion |
|----------|----------|----------|------------|
| C4 >> C1 | C2 ≈ C1 | C3 >> C1 | Contextualization dominates — full surface helps; addressing doesn't add |
| C4 >> C1 | C2 >> C1 | C3 ≈ C1 | Localization dominates — addressing the right surface is the value |
| C4 >> C1 | C2 >> C1 | C3 >> C1 | Both contribute; C4 = sum of effects |
| C4 ≈ C1 | All ≈ C1 | All ≈ C1 | Target is null — pre-screen failed; reclassify, pick new target |
| C4 ≈ C1 | C2 >> C1 | — | Selector layer broken — diagnostic needed before reclassification |

This is the central proposition test. Anything less doesn't earn Stage 3 the right to claim "we showed the compiler works."

---

## §6 — Stage 3 scope question (open)

Wave 3 design brief framed Stage 3 as "lock in a high-velocity iteration loop on ONE primary case." Click was the dev-loop primary; sphinx was the proving secondary. The framing assumed click would converge to a working loop and sphinx would be the secondary measurement.

Click did not converge. Two paths forward:

**Path A — Sphinx becomes primary, click becomes shakedown reference.** Sphinx replaces click as dev-loop driver. Click's role becomes "the calibration target that taught us about parametric priors." Stage 3's scope is sphinx-centric.

**Path B — Fresh Phase 2 target, sphinx as secondary.** A fresh target (post-training-cutoff library or domain-specific) becomes primary. Sphinx becomes the cross-target validation case to test generality. Higher cost (gold-key curation), higher confidence (low prior by construction).

Path A is faster (operational familiarity). Path B is more rigorous (lower prior risk). My current lean is Path A unless the §4 pre-screen on sphinx returns "EXCLUDE" categorization, in which case Path B becomes mandatory.

---

## §7 — Questions for CVO

### Q1 — Pre-screen design (P0)
The §4 parametric-prior pre-screen is the largest design addition to the protocol. Is the four-cell categorization (zero-shot × H3) the right diagnostic, or is there a more rigorous prior-strength measure (e.g., judge confidence calibration, ensemble disagreement, abstention rate)? The pre-screen's purpose is to prevent click-class failures from being repeated; it must catch them BEFORE iteration begins. Does the proposed design achieve that, or does it need a different epistemological base?

### Q2 — Four-condition implementation gating (P0)
Protocol amendment §3 requires C1+C4 minimum and C2+C3 to attribute localization vs contextualization. Stage 3 MVT (§5) requires all four from the start. Should this be the Phase 2 standard (no Phase 2 case ships without 4-condition scoring), or should we phase it (C1+C4 wave 1, C2+C3 wave 2)? The phased path is faster but defers the central attribution question; the all-four path is slower but earns interpretive clarity from the first run.

### Q3 — R-SC-2 + delivered-context audit as ship-blockers (P0)
Both §3.1 and §3.2 are pre-conditions on my read. R-SC-2 is being implemented now by SC. Delivered-context audit is not. Should both be ship-blockers for Stage 3 dispatch, or can delivered-context audit be added mid-phase if PATTERN C-class diagnosis becomes needed? My current position: both must ship before Stage 3 begins. Diagnostic instrumentation added mid-phase contaminates the comparison baseline.

### Q4 — Stage 3 target — Path A vs Path B (P1)
§6 question. Sphinx primary (Path A) or fresh post-cutoff/domain-specific target (Path B)? My lean: Path A pending §4 pre-screen result. Does CVO see a reason to default to Path B regardless of pre-screen outcome (e.g., generality concerns, prior-strength uncertainty)?

### Q5 — Where does the click design lesson live? (P1)
CVO 20260427T163500Z R-CTO-3 directs me to "promote this click result into a design lesson: strong parametric priors can dominate correct injected structure." Three options: (a) section in the program PRD (`COMP_LEARNS_ARCHITECTURE.md`); (b) standalone design-lessons document at `docs/architecture/COMP_LEARNS_DESIGN_LESSONS.md`; (c) both — short reference in the program PRD pointing to a longer canonical lessons document. My lean: (c). The lesson is too important to bury in a session log but too narrow to crowd the program PRD.

### Q6 — Unknown-unknown asks
What should I be asking about Stage 3 design that I am not? I have a blind spot for the "what if the compiler proposition is wrong" case — i.e., what does null-result-on-sphinx mean for the program, and is the program designed to recognize and survive that outcome? CVO §4 on iter-7 ("click harvested the actual systems-program insight") suggests null results are valuable; I want to make sure Stage 3 design doesn't inadvertently optimize against discovering them.

---

## §8 — Feedback ask (priority order)

**P0 (must rule before Stage 3 PRD authoring):** Q1 (pre-screen design), Q2 (4-condition gating), Q3 (ship-blockers).

**P1 (can rule alongside PRD draft):** Q4 (target path), Q5 (lesson location).

**P0+ (epistemological):** Q6 (unknown-unknowns). If CVO sees a hole in the proposition test design, I want to know now, not after Stage 3 ships.

**Format for response:** File at `org/tier1_exec/3.1.0_SA_CVO/responses/YYYYMMDDTHHMMSSZ_to_1.1.0_SA_CTO_stage3_design_review.md`. Stamp any MUST-halt findings as R-CTO-N (P0 = blocks Stage 3 PRD authoring; P1 = rules required before Stage 3 dispatch).

---

## §9 — State for CVO context

- Stage 1+2: COMPLETE. Stage 2 §7 exit criterion SATISFIED (3/2 clean waves, 5acd28ee).
- Click dev-loop: CLOSED as scored lift target (R-CTO-1 P0 from CVO 20260427T163500Z). Allowable remaining click work: q02/q11 non-ratchet diagnostic (.069), experiment_log path fix (DS), click post-mortem.
- Champion still 7beb09b (ab_lift=0.0909, q05 format artifact). Champion is unchanged across iters 2-7.
- Phase 2 protocol amendment: in force, awaiting Stage 3 PRD. R-COO-1 target criteria (3 required) + §3 four-field accounting (`background_index_existed`, `localization_inputs`, `localization_outputs`, `addressing_determination`) + §4 cost split (`background_index_cost`, `task_addressing_cost`, `delivered_context_cost`) all defined.
- Open standing items: R-SC-2 (in flight), R-DS-1 (no action — edge topology family closed), Stage 3 PRD (not yet drafted — pending CVO P0 rulings on this brief).
