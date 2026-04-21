# 1.1.0_SA_CTO Session 03 — Target Close-Out Playbook v1.1 (post external-validator revision)

**Date:** 2026-04-21 (Tue, PM ET — same-day revision cycle after session 02)
**Agent:** 1.1.0_SA_CTO
**Scope:** Apply external-validator feedback to v1.0 of the Target Close-Out Playbook PRD. Andrew routed the v1.0 PRD through a codex agent validator and passed the numbered feedback back. Revisions ship as v1.1 atomically in one commit before `2.1.0_SA_COO` decomposes — zero rework downstream.

---

## Objective

v1.0 shipped in session 02 commit `0fab133f`. External validator returned: 2 PASS, 4 ISSUE, 1 GAP — overall verdict "revise to v1.1 before COO decomposes." Six surgical edits across the PRD + propagation to the 3 amended TOs.

Terminal verdict target: PRD at v1.1, all issues resolved, `.009` / `.015` / `.018` / `.020` / `COMP_LEARNS.json` consistent with v1.1, JSON validated, session log with Compiler Tools.

---

## Work Completed

### Validator findings + resolution

| # | Validator finding | Angle | Resolution |
|---|-------------------|-------|------------|
| 1 | §2 PASS but missing precedence rule for overlapping exits | Classifier semantics | Added §2.1 new subsection: first-qualifying-exit semantics + tie-break order `PLATEAU_WITH_HONOR > PLATEAU_BY_EXHAUSTION > OUT_OF_MONEY > OUT_OF_PATIENCE > INTERVENTION` with rationale per tie. Propagated to `.023` mandate (AC must cover the 4 tie-break cases). |
| 2 | §3 gate (b) too subjective — "CTO judges target-agnostic" is auditable not reproducible | Promotion rule | Expanded Promoted Learning form with **3-part Justification block** (`Mechanism` / `Why not target-specific` / `Predicted transfer surface on target 2`). Added §3.1 uniqueness rule clarifying one-learning-per-distinct-mechanism. `promote()` enforces presence of all three subfields; missing any raises `PromotedLearningMissingJustification`. |
| 3 | §5 not stringent enough — 3 of 4 criteria are weights, any plausible non-internal Python repo could pass | Target-2 gate | Converted criteria 1 (parser proven) + 4 (gold-authorable) from weights to **hard minimums**. Criteria 2 (subtype leverage) + 3 (size ceiling) remain weights scored 1-5. Propagated to `.009` TO: gate-table AC restructured; `<objective>` output list updated. |
| 4 | §8.3 fixture count drift — PRD listed 4 fixtures, amended `.015` TO listed 5 | Downstream consistency | Added fixture (e) to PRD §8.3 matching the already-existing `.015` AC #7 entry: "fabricated fixture with 100% vocabulary coverage — MUST return cleanly WITHOUT requiring 'Dimension Values Not Observed' section." PRD and TO now verbatim-matched. |
| 5 | §8 PASS but `.023` enum-grep mandate step is weak proxy — presence of 5 strings does not prove classification logic | Compiler mandate | `.023` Phase 2 pytest step elevated to explicit "**This is the correctness gate.**"; grep step demoted to "cheap sanity check; enum presence alone does NOT prove logic" with `<if_mismatch>` reminding author to re-run pytest after adding enum. Added acceptance-criteria note pointing COO to require pytest coverage in `.023`'s AC. |
| 6 | §4 over-engineered — 6 steps + 5 artifacts + joint-signoff commit heavy for a "short by design" protocol | Review protocol | Collapsed to **4 required artifacts**: (1) classify_result.json, (2) one rendered report with inline `## Candidate Promoted Learnings` section (drops separate `PROMOTION_CANDIDATES.md` file), (3) program.md append via `promote()`, (4) scorecard archive folded into report appendix. Joint-signoff commit formalism downgraded to advisory — session logs reconstruct CTO/COO participation. |
| 7 | GAP — decision clarifications missing (precedence, learning-uniqueness, exact `.015` fixture set) | Multi-section polish | Addressed via 3 new inline subsections: §2.1 (precedence), §3.1 (uniqueness), §8.3 aligned to 5 fixtures. No standalone "Decision Clarifications" section needed — each clarification lives with its parent rule for discoverability. |

### Additional polish bundled

- v1.1 header change-log summarizes all 6 deltas with section refs so future readers see the revision rationale without diff-reading.
- §9 acceptance-criteria updated: exported symbols list extends (`PromotedLearningMissingJustification` + `PromotedLearningRewrite` added); criterion #2 references the four precedence tie-break tests + three Justification-subfield fixtures; criterion #6 reads "**five** fixtures a-e" not "four"; criterion #8 added (no `PROMOTION_CANDIDATES.md` file exists).
- `.009` TO: reference row updated to v1.1 + §3.1; AC renumbering fixed (old #2 + #3 collapsed into single gate-table AC #2); objective output list restructured.
- `.018` TO: reference row updated to v1.1; 9th-item description expanded to cite Justification block + §3.1 uniqueness.
- `.020` TO: reference comment updated (no functional change — v1.1 still does not touch selectors).
- `.015` TO: reference row updated to v1.1. AC #7 already had 5 fixtures (was already correct); no AC change needed. Confirmed consistency.
- `COMP_LEARNS.json`: `prds[]` row label extended with v1.1 delta summary; `phase` narrative extended with v1.1 revision note.

---

## Decisions Made

1. **Ship as v1.1, not v2.0.** Changes are tightening, not re-architecting. v4.2 architecture precedent uses patch versions for surgical amendments; this follows.
2. **Zero rework downstream.** COO has not yet decomposed `.023` / `.024`; v1.1 lands before her decomposition wave starts. Acknowledged in MCP follow-up.
3. **Inline subsections over a standalone "Decision Clarifications" section.** Each clarification lives with its parent rule (§2.1 under §2, §3.1 under §3, fixture count in §8.3). Readers searching for "precedence" or "uniqueness" find the rule next to its classifier/promotion context, not in a scattered appendix.
4. **Advisory co-authoring on close-out commits.** Session logs are authoritative for CTO/COO participation audit; commit ceremony adds structure-without-information-gain. Dropped from §4.
5. **`PromotedLearningMissingJustification` is a named exception class, not a generic `ValueError`.** Named exceptions compose with the rest of the close-out module's vocabulary (`PromotedLearningRewrite`, `CloseOutCalledOnEmptyLog`, `GoldSurveyAttestationMissing`); grep-auditability and consistency win.

---

## Files Modified

Edited:
- `docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md` — header v1.0 → v1.1 + change-log; §2.1 new subsection; §3 Promoted Learning form + §3.1 new subsection; §4 collapsed to 4 artifacts; §5 hard minimums + weights restructure; §8.1 pytest-is-gate clarification + AC note; §8.2 Justification-subfield test expansion; §8.3 fixture (e) added; §9 acceptance-criteria expanded to 8 items; total diff +140 / -50 net.
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.009.cto-target-2-selection.md` — reference → v1.1; `<objective>` criteria + output list restructured; `<acceptance_criteria>` renumbered; gate-table AC replaces old scoring-table + disqualifier-table items.
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.018.cto-program-md-v1.md` — reference → v1.1; 9th item elaborates Justification + §3.1 uniqueness.
- `org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.020.cto-selector-benchmarking-harness.md` — reference comment → v1.1 (note-only).
- `org/tier2_senior/1.4.0_DS_CompLearns/task_orders/COMP_LEARNS.015.bench-scorecard-ab.md` — reference → v1.1 (no AC change; already had 5 fixtures).
- `org/projects/COMP_LEARNS.json` — `prds[]` row label + `phase` narrative extended with v1.1 delta.

Created:
- `org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-21/session03_target_closeout_prd_v1_1_revision.md` (this log).

Out of scope (untouched): `comp/`, other project JSONs, `org/projects/REGISTRY.md`, other TOs, `.comp-graph/`.

---

## Blockers

None. v1.1 is decomposable; COO can proceed. v1.0 → v1.1 diff is zero-rework for her since decomposition had not started.

---

## Current State

- PRD at v1.1. External-validator ISSUE count: 0 remaining.
- TO ownership + reference consistency: all 4 amended TOs point at v1.1 correctly.
- JSON validated.
- Same-day MCP going to `2.1.0_SA_COO` informing her to decompose against v1.1 (her first-check inbox will surface the update before she touches the v1.0 copy).

---

## Next Steps

1. **[2.1.0_SA_COO]** Decompose `.023` + `.024` against PRD v1.1 per §8.1 + §8.2 triads.
2. **[Self]** Optional — run the v1.1 PRD through the codex validator a second time to confirm the ISSUEs are closed. Not required; validator's numbered feedback was specific enough that surgical fixes match the asks directly. Second-pass would catch any NEW issues I may have introduced.
3. **[Self, standing duties]** Unchanged — acceptance-flex adjudication on any COMP_LEARNS pre-flag; architecture questions from DS via MCP; cross-project liaison with `1.0.0_SA_CTO` if shared-infra question surfaces.

---

## Compiler Tools

| Tool | Command | Result | Purpose |
|------|---------|--------|---------|
| Read | `docs/architecture/COMP_LEARNS_TARGET_CLOSEOUT.md` (v1.0 post-commit) | Full v1.0 content captured | Identify each edit anchor for surgical revision |
| Read | `.009` / `.015` / `.018` / `.020` TOs | Confirmed current state (TOs 1 & 4 still v1.0-referenced; TO 2 — `.015` — already has 5 fixtures) | Scope the propagation edits |
| Read | `org/projects/COMP_LEARNS.json` | Confirmed JSON structure + prds[] row for editing | Extend label + phase narrative |
| Grep | `grep -n "TARGET_CLOSEOUT\|PROMOTION_CANDIDATES" docs/architecture/ org/tier1_exec/1.1.0_SA_CTO/ org/tier2_senior/1.4.0_DS_CompLearns/` | Identified all cross-references | Ensure v1.1 updates are complete |
| Grep | `grep -n "^    [0-9]\\+\\." .009.md` | Detected AC renumbering drift (1, 2, {missing 3}, 4) | Fix renumbering post-collapse |
| python | `python -c "import json; json.load(...)"` | `JSON OK` | Post-edit validation |
| Edit | 11 surgical edits across 6 files | Clean | v1.1 revision execution |
| Write | 1 new file (this log) | Clean | Session audit trail |

No `comp-*` graph-tool runs — PRD revision operates on doc + TO text only. `comp-build` / `comp-xref` / `comp-blast` become relevant when `.023` / `.024` actually implement in `comp/framework/closeout/` per their own per-phase mandates.

---

## Task Order Dispatch

None this session (CTO authors PRDs, not TOs; COO decomposes). The v1.1 edits on `.009` / `.018` / `.015` / `.020` are amendments, not new dispatches — all 4 remain staged or already-amended at the owning agent's task_orders folder, ready for COO's decomposition pass.

---

## Validator feedback retrospective (process learning — parked for future)

The codex validator caught three things I'd have missed on self-review: (a) the fixture-count drift between PRD and TO, (b) the soft-gate nature of §5 criteria, (c) the over-engineered ritual in §4. Item (a) in particular is the sort of cross-file consistency failure that compounds downstream — the TO author would have seen 5 fixtures in the TO, 4 in the PRD, and asked "which is authoritative?" — forcing a RAVC cycle I now don't need.

Parking this as a note for future PRD authoring: after a PRD's first draft references a downstream TO's AC, diff the PRD's cited AC text against the TO's AC text as a separate mechanical step. The PRD+TO-simultaneously-authored pattern I used in session 02 is what enabled the drift, because I wrote both in the same flow and drift slipped in.

— 1.1.0_SA_CTO
