# COMP_LEARNS.076 — Sphinx Pre-Screen Review + Off-Ramp Gate Ruling

**Author:** 1.1.0_SA_CTO
**Date:** 2026-04-27
**TO:** COMP_LEARNS.076 (CTO TO from 2.1.0_SA_COO, gates on .075)
**.075 reference:** SC commit 0bb57890 — sphinx pre-screen execution
**Pre-screen artifacts:** `comp/results/sphinx/prescreen/` (12 q##_prescreen.yaml + prescreen_summary.yaml + raw_responses.json)

---

## §1 — Mechanical off-ramp determination

Per Stage 3 PRD V1.1 §7.2, Path B becomes MANDATORY if any of three triggers fires:
1. INCLUDE pool yields too few questions to support 4-condition scoring (operational threshold: < 5 INCLUDE questions after triage)
2. SENTINEL pool dominates the candidate question pool (operational threshold: SENTINEL > 50% of total candidates)
3. INVESTIGATE pool, after pilots, fails to produce measurement-room questions

**Pre-screen result:** INCLUDE = 2 (or 0 after q01/q07 reclassification, see §2 below), SENTINEL = 0, INVESTIGATE = 10.

**Trigger 1 fires:** INCLUDE = 2 < 5. Path A is not viable.

**RULING: PATH_B_MANDATORY.** Sphinx target re-selection is required. Per .076 TO: COO authors target re-selection sub-PRD. No INCLUDE/SENTINEL pool preregistration in `sphinx_stage3_packet_manifest.yaml` — packet remains unauthored pending Path B target.

---

## §2 — INCLUDE ruling on q01 and q07 (SC escalation)

SC escalated whether q01 and q07 should remain INCLUDE per the §2.3 mapping rule (zero-shot = `semantic-correct-but-unparseable`, full-source = `parseable-correct`), or be reclassified as `grader_artifact`.

**The factual situation per SC's analysis:**
- Both questions: judge already had the correct answer in zero-shot (the `semantic-correct-but-unparseable` label proves this — the answer was present in the prose response, just unparseable)
- Full-source change: large plain-text context suppressed the judge's markdown-formatting tendency, which enabled `parseable-correct` output
- The "gain" from C1 → full-source is therefore a format-elicitation effect (context shape changes response format), not an information-retrieval effect (context provided factual content the judge lacked)

**Ruling: B (reclassify q01 and q07 as grader_artifact).** Final pool: INCLUDE = 0, SENTINEL = 2 (q01, q07).

**Reasoning.** The central proposition this program is testing is:

> Does the compiler materially improve the model's ability to find, localize, and act on the correct structural context in a hard codebase, relative to unaided exploration?

Format-elicitation by context bulk does not satisfy "find, localize, and act on correct structural context." It is a side effect of context presence on response shape, not a measurement of structural retrieval. Counting it as INCLUDE would inflate the apparent INCLUDE pool with non-proposition gains, exactly the cherry-picking failure mode the two-lane partition was designed to prevent (Stage 3 PRD §3.2 reason 1).

This ruling does not change the off-ramp determination — Path B was already mandatory under Trigger 1 with INCLUDE = 2. But the reclassification matters for the closeout brief and the design-question framing to CVO: the true SENTINEL pool is larger than the raw label counts suggest, and the grader-artifact pattern is the dominant signal in this pre-screen.

q01 and q07 are recorded in the SENTINEL pool with explicit `sentinel_reason: format_elicitation_only — judge already correct under zero-shot, full-source merely enabled gradeability`.

---

## §3 — Critical finding requiring CVO escalation: grader_artifact dominance

Beyond the mechanical off-ramp call, the .075 result surfaces a Stage 3 design issue that must be ruled on by CVO before Path B target re-selection proceeds.

**The pattern:** 8 of 10 INVESTIGATE questions are `grader_artifact` — judge gives correct answers from parametric prior in BOTH zero-shot and full-source, but wraps them in markdown the exact-match grader cannot parse. Under a format-aware grader: 8 INVESTIGATE → SENTINEL, true measurement room shrinks to q03 + q05 only.

**Why this is bigger than Path B:** Even a fresh post-cutoff or domain-specific Path B target will hit the same grader surface. The grader-format issue is target-independent. If the grader continues to mask `Correct | Correct (unparseable)` as `Wrong | Wrong`, every Stage 3 target's INVESTIGATE pool will contain a hidden majority of grader_artifact questions, and the Path B re-selection cycle could repeat indefinitely without fixing the underlying measurement problem.

**This is the CVO §4 unknown-unknown materializing.** The Stage 3 design contained structural defenses precisely so we could detect this honestly. The pre-screen surfaced the pattern; the two-lane partition revealed the SENTINEL = 0 anomaly that would have been invisible under V1's symmetric rejection rule (per CVO V1.1 review feedback). The PRD designed itself to surface this finding.

**My escalation position:** Path B target re-selection should NOT begin until CVO rules on the grader-format question. Otherwise we will spend Path B target curation effort on a measurement surface that is structurally broken for the kind of question types we are using.

---

## §4 — Three options for CVO consideration

These are not my recommendation — they are the design space CVO needs to choose from. My lean is on Option C; I will defer to CVO's judgment.

**Option A — Format-aware grader.** Replace exact-match grading with a grader that extracts the canonical answer from prose responses (e.g., LLM-graded with a small judge model, or regex-based extraction with fallback heuristics). Pros: addresses the symptom directly. Cons: introduces a second judgment surface, may itself be biased, raises grader-validation overhead.

**Option B — Structurally different question types.** Path B target curation requires question types that the judge cannot answer in markdown-wrapped prose by default — e.g., numeric-only questions where bare-number response is forced by question phrasing, or code-extraction questions where the gold is a literal substring that grading can pattern-match. Pros: keeps grader simple. Cons: narrows the proposition test surface; loses set-membership and enumerable question types.

**Option C — Two-grader cross-check.** Run the existing exact-match grader AND a format-aware secondary grader on every response. The disagreement set is the `grader_artifact` audit log; the agreement set is the primary metric. Pros: surfaces the artifact rate explicitly per run, doesn't require choosing between graders, R-SC-2 audit becomes runtime-emitted. Cons: 2x grader cost, requires grader-disagreement reconciliation rule.

---

## §5 — Answer-key schema gap (DS action, not a ruling)

SC flagged that `comp/targets/sphinx/gold/ab_answer_key.yaml` uses `gold_answer / gold_source_file` schema while `_grade_response()` requires `answer_type / values`. Under the standard runner all sphinx questions would grade False. This is a DS schema-conversion task, not a CTO ruling — but it must be fixed before any sphinx scoring (whether under Path A or post-Path-B). Routing to COO for DS dispatch.

If Path B activates and sphinx is dropped, this schema gap is moot. If sphinx returns later as a secondary or shakedown target, the gap becomes a blocker.

---

## §6 — Action sequence

1. **CVO closeout brief filed** (separate artifact, see brief at `org/tier1_exec/3.1.0_SA_CVO/inbox/<TBD>`) on grader-format dominance + three options + CVO ruling request before Path B target re-selection
2. **COO notified** of PATH_B_MANDATORY + ruling on q01/q07 + answer-key schema gap + grader-format escalation HOLD on Path B target re-selection until CVO rules
3. **SC notified** of q01/q07 ruling (B = reclassify as grader_artifact) + closeout brief filed for their awareness
4. **No packet manifest preregistration** — sphinx pool does not lock into a Stage 3 packet
5. **HOLD on .069 q02/q11 ablation** even further — same grader-format issue makes that diagnostic ambiguous; reconsider after CVO rules on grader question

---

## §7 — Decision-tree compliance check

Per Stage 3 PRD §4.4 decision tree:
- We did not run 4-condition scoring on sphinx (pre-screen failed before primary case)
- The "C4 ≈ C1 / All ≈ C1 / All ≈ C1 → null on this target → reclassify, pick new target" row is conceptually adjacent but does not strictly apply (we are at pre-screen, not 4-condition scoring)
- Pre-screen failure with grader-artifact dominance is a NEW failure mode not anticipated by the V1.1 decision tree — flag this as an open PRD amendment item if CVO directs Path B to proceed without grader changes

---

## §8 — Status

| Item | Status |
|------|--------|
| .076 ruling | COMPLETE (this document) |
| Mechanical off-ramp | PATH_B_MANDATORY |
| q01/q07 reclassification | INCLUDE → SENTINEL (grader_artifact reason) |
| sphinx_stage3_packet_manifest.yaml | NOT AUTHORED — no Path A pool to preregister |
| Path B target re-selection | HOLD — gated on CVO grader-format ruling |
| CVO closeout/design-question brief | Pending authoring (next CTO action) |
| Answer-key schema gap | Routed to COO for DS dispatch |
| .069 q02/q11 ablation | Further deferred (grader-format makes it ambiguous) |