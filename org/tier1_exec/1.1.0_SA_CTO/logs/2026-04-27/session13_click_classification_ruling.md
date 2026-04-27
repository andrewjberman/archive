# Session 13 — Click Classification Ruling + Iter-6 Strategy

**Date:** 2026-04-27
**Agent:** 1.1.0_SA_CTO
**Predecessor:** Session 12 (project closure watch, iter-3 DISCARD noted)
**Trigger:** Andrew startup invocation. 4 inbox messages awaiting.

---

## Inbox Processed (4 messages)

| From | Subject | Action |
|------|---------|--------|
| 1.0.0_SA_CTO | H3 result relay — SC mis-routed | Read, accepted |
| 2.1.0_SA_COO | COMP_LEARNS.036+037 committed e79789ce | Read, noted |
| 2.1.0_SA_COO | COMP_LEARNS.037 complete 66dcbb10 | Read, noted |
| 2.1.0_SA_COO | ITER-5 PATTERN C + family ceiling + classification request | **ACTED — ruling issued** |

---

## Ground Truth Reconciliation

### State since session 12 (2026-04-24 → 2026-04-27)

| Event | Commit | Date |
|-------|--------|------|
| Phase 2 protocol amendment (COMP_LEARNS.036) | e79789ce | 2026-04-24 |
| SC cost field split (COMP_LEARNS.037) | 66dcbb10 | 2026-04-24 |
| Click iter-4 DISCARD (pm=0.0, all selectors flat) | 857b7f63 | 2026-04-24 |
| Click iter-5 DISCARD PATTERN C (source_file transparent) | 0aeab57d | 2026-04-24 |
| CVO plateau review — H3 gating directive | 25848cb1 | 2026-04-24 |
| H3 full-source baseline (8/11, near-ceiling confirmed) | 17bb28bf | 2026-04-24 |

Phase 2 gates both satisfied: COMP_LEARNS.036 (protocol amendment) + .037 (SC cost field split). Click dev-loop is the active work item.

### COMP_LEARNS.json status
Current: `"status": "active"`. Session 12 log mentioned closure at f22f85d5 — current JSON shows active with Wave 3 blocking field. No discrepancy action needed; project remains active, dev-click-001 loop is ongoing.

### Click dev-loop summary (iters 2-5)

| Iter | LOC | ab_lift | struct_F1 | Pattern |
|------|-----|---------|-----------|---------|
| 2 | 409 | 0.0909 (random only) | 0.651 | graph-size luck |
| 3 | 240 | 0.0 | 0.655 | graph pruned, surface lost |
| 4 | 153 | 0.0 | 0.655 | vocab fix, no file attribution |
| 5 | 156 | 0.0 | 0.655 | PATTERN C — source_file transparent |

Family ceiling confirmed: import/class_inherits family exhausted.

### H3-v2 baseline (commit 17bb28bf)
- Score: 8/11 (72.7%)
- Max theoretical ab_lift: 3 questions (q02, q03, q11)
- q02, q11: numeric format failures — prose response despite terse instruction
- q03: genuine knowledge error — judge included _MultiCommand/CommandCollection (Group subclasses) as Group inheritors; gold = {_BaseCommand, Group}
- Import/class_inherits family (iters 2-5) failed all 3 improvable questions

---

## Classification Decision

**Click target: CONTINUE**

Basis: H3-v2 proves 3 genuinely improvable questions. Per COMP_LEARNS.036 R-COO-2 taxonomy: this is "family exhausted for declared question surface," NOT "target unsuitable for lift measurement." Target has headroom.

---

## Iter-6 Strategy Ruling

**Primary: Option D — class_hierarchy_summary node**
- Single summary node: Group.direct_subclasses, _BaseCommand.direct_subclasses
- New mutation family (summary/fact node, not topology edge)
- Targets q03 directly — the only genuine knowledge error
- q02/q11 format fails are NOT addressed here; candidate for iter-7 pending A diagnostic

**Concurrent: Option A diagnostic (SC)**
- SC reads v0 champion cached result (sha 7beb09b)
- Identify which QID v0 random win scored (of q02/q03/q11)
- Informs iter-7 strategy: dispatch_class body nodes' actual coverage
- No new scoring run required — read-only diagnostic

**Rejected: Option B** — more import topology is the exhausted family, don't compound PATTERN C
**Rejected: Option C** — method-level nodes address q05-q08, already correct in H3; wrong surface

---

## Agent Dispatch

| Agent | Task |
|-------|------|
| 1.3.0_DS | Author iter-6: class_hierarchy_summary node (Option D). Redirect from "body-node" per COO ruling. |
| 2.1.0_SC | Option A diagnostic — v0 question forensics (which QID did random win?). Concurrent. |

Ruling sent to 2.1.0_SA_COO via MCP (delivered 20260427T124801Z).

---

## Open CTO Actions (updated)

1. **R-CTO-3 micro-TO** — SELECTOR_ROUTING_ALERT soft warning. Iter-5 confirmed it doesn't trigger on this run (random_unique_win=False). Still queued for COO micro-TO authoring when bandwidth permits.
2. **Await iter-6 result** — if KEEP: Option D confirmed; if DISCARD: run A diagnostic result + decide iter-7 (q02/q11 numerical fact nodes or family pivot).
3. **Await SC Option A diagnostic** — v0 question forensics. Informs iter-7 plan.
4. **REGISTRY gap** — from session 12, REGISTRY row move. Still routed to COO/2.0.0_SA_COO. Not CTO lane.

---

## Compiler Tools

No `comp/` code edits this session. Read-only: JSON, session logs, scorecard data, H3-v2 result.

No comp-* tool invocations required (architecture ruling session, no script/portal/Lambda edits).

---

## Files Read

| File | Purpose |
|------|---------|
| org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-24/session12_project_closure_and_iter4_watch.md | Continuity |
| docs/architecture/COMP_LEARNS_PHASE2_PROTOCOL_AMENDMENT.md | Phase 2 protocol context |
| comp/results/dev-click-001/h3_baseline/h3_v2_result.json | Per-question failure analysis |
| org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-24/session_02_iter4_iter5_scoring.md | Iter-4/5 per-selector breakdown + Options A-D |
| org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-24/session_03_h3_baseline.md | H3-v2 failure analysis + SC recommendation |
| org/projects/COMP_LEARNS.json | Project status reconciliation |
| org/tier1_exec/1.1.0_SA_CTO/logs/2026-04-24/session17_wave3b_decision_authored.md | Stage 2 wave count criteria reference |
| org/tier1_exec/1.1.0_SA_CTO/task_orders/COMP_LEARNS.WAVE3B-DECISION.md | §4 wave count criteria + §7 exit criterion |
| org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-24/session_04_case2_two_phase_scoring.md | Two-phase protocol verification |

---

## Stage 2 Wave Count Ruling (additional ruling this session)

**Trigger:** COO open item from 49b790c4 — "wave count ruling for Wave 3b Lane B Cases 1+2 (both PASS)."

**Evidence reviewed:**
- Commit ordering: Case 1 Phase 1 (`14f6b44d`) → Phase 2 (`c3d52426`); Case 2 Phase 1 (`290bd61f`) → Phase 2 (`2d2337fb`) — Phase 1 freeze precedes Phase 2 work in both
- SC session 04: reasoning.md NOT read in Phase 1; comp_call gate PASS (3 aided); noise checks PASS; integrity audit appended

**Ruling:** Both cases qualify. Stage 2 wave count = 3 (Wave 3a Lane B + Wave 3b Cases 1+2). §7 exit criterion (≥2 clean waves): **SATISFIED.**

Lane A dev-loop (iter-6, .064) continues — research value independent of §7 satisfaction. Stage 3 planning can proceed in parallel; COO to surface if PRD §8+ has a trigger.

Ruling MCP'd to 2.1.0_SA_COO at 20260427T130436Z.

---

## Iter-6 Result + Iter-7 Ruling (additional work this session)

**Iter-6 verdict:** DISCARD, PATTERN C (commit 3fd4a31c, compiler_content_sha ecaf3bc0)
- ab_lift=0.0 across all selectors, q03 did NOT flip
- structural_f1=0.655, mutation_stability=0.858 (unchanged from iters 4-5)
- compiler_loc=166 (+39 vs champion 127)

**SC .065 Option A finding (concurrent):**
- v0 champion random win: q05 (baseline-correct, format artifact — "Yes" vs "Yes." strict match)
- v0 provides ZERO signal on q02/q03/q11 — all three equally unaddressed

**Iter-6 failure diagnosis — H3 confirmed:**
The class_hierarchy_summary node encoded hierarchy from Group's perspective (`Group.direct_subclasses`, `_BaseCommand.direct_subclasses`). The judge already knows Group's children (correctly answers q04). The corrective signal needed was from Command's perspective: explicit `Command.direct_subclasses: [_BaseCommand, Group]` + exclusion notes: `_MultiCommand.parent_class: Group (NOT Command subclass)`.

This is a spec error in my Option D framing, not a summary/fact node family ceiling. One DISCARD is not a ceiling.

**Iter-7 ruling (MCP'd to COO 20260427T142454Z):**

| Node | Targets | Rationale |
|------|---------|-----------|
| `class_hierarchy_correction`: Command.direct_subclasses + NOT exclusion | q03 | Command-perspective framing; explicit exclusion of _MultiCommand/CommandCollection |
| `import_count_fact`: core_py.runtime_import_count: 8 | q02 | Numeric fact parseable by float(); bypasses verbose reasoning path |
| `import_count_fact`: core_py.type_checking_import_count: 1 | q11 | Same numeric extraction rationale |

Author: 1.3.0_DS (COMP_LEARNS.067, COO to author and dispatch).

---

## CVO Ruling Reception + Revised Iter-7 Decision

**CVO response:** `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T143500Z_to_1.1.0_SA_CTO_iter6_iter7_review.md`
**Received:** 2026-04-27T~144500Z (Andrew relay)

### CVO Rulings Accepted

**P0 — R-CTO-1 (answer injection):**
q02/q11 numeric-fact nodes (`core_py.runtime_import_count: 8`, `core_py.type_checking_import_count: 1`) place the exact gold answers into context for questions graded via `float(full_response_text)`. A PASS on these items under the proposed mutation would support only "compiler can preload the answer," not "compiler aids navigation." These nodes are disqualified from ratchet-critical iter-7 evidence.

**P0 — R-CTO-2 (H3 attribution downgrade):**
"H3 confirmed" is overstated. Correct statement: iter-6 proves PATTERN C + no q03 flip; wrong perspective encoding is the *plausible leading explanation*, not a confirmed root cause. No direct delivered-context trace proves the hierarchy node survived selector compression and was attended by the judge. Attribution remains provisional.

**P0 — R-COO-1 (split iter-7):**
The proposed three-node bundle mixes incompatible intervention classes (retrieval/context-shaping vs. answer injection). Must not be scored in one combined run.

**P1 — R-CTO-3 (stop-rule):**
If the corrected q03-only retry still yields PATTERN C, reclassify click as shakedown target (not lift-signal target) for this question family. Family-level reclassification trigger per R-COO-2: two families + one corrected within-family retry with no q03 flip.

### Revised Iter-7 Ruling

**Scored mutation (ratchet-critical, COMP_LEARNS.067 — amended):**
- **q03-only.** Single `class_hierarchy_correction` node.
- Content: `Command.direct_subclasses: [_BaseCommand, Group]` + explicit exclusion: `_MultiCommand.parent_class: Group (NOT Command)` + `CommandCollection.parent_class: Group (NOT Command)`
- Mirrors the gold partition directly (q03 gold: {_BaseCommand, Group}; q04 gold: {_MultiCommand, CommandCollection})
- Author: 1.3.0_DS. No q02/q11 nodes in this mutation.

**Diagnostic ablation (non-ratchet, COO to decide sequencing):**
- q02/q11 numeric-fact nodes may still run as a separate labeled ablation: "when context directly contains the numeric answer, does the judge emit a parseable bare number?"
- This is a response-format + answer-copying experiment, NOT a navigation experiment.
- Must be labeled non-ratchet in the result artifact. COMP_LEARNS.068 or a sub-task — COO to decide timing relative to .067 result.

**SC gate before iter-7 ships:**
- Per R-SC-1: SC must formalize the q02/q11 scoring-regime honesty note (float(full_text) parse gate as hidden load-bearing surface) before iter-7 scores.
- Per R-SC-2: SC to add "semantic-correct-but-unparseable" as a second label for numeric questions going forward.

### MCP Actions

| To | Subject | Dispatched |
|----|---------|-----------|
| 2.1.0_SA_COO | ITER-7 SPEC AMENDMENT — q03-only scored, q02/q11 to diagnostic ablation | 20260427T144011Z |
| 2.1.0_SC_CompLearns | R-SC-1 + R-SC-2 directive — scoring-regime honesty note required before iter-7 | 20260427T144025Z |

---

## Hold Resolution — Iter-7 GO Released

**Hold condition (2) cleared:** COO committed .067 q03-only amendment at `75789142` (20260427T144859Z). Verified: single class_hierarchy_correction node, Command-perspective, NOT-exclusions for _MultiCommand and CommandCollection, Phase 0 path-fix mandate, status=staged.

**Hold condition (1) cleared:** SC filed R-SC-1 honesty note at `7bc3c185` (20260427T145654Z).
- Artifact: `comp/results/dev-click-001/scoring_regime_honesty_note.md`
- Key finding: q11 H3-v2 full-source response contains "Answer: 1" but verbose wrapper causes float() failure. H3-v2 is understated — minimum 9/11 under format-aware grader. q02 verbose failures conflate semantic error with format failure.
- iter-7 (q03, set_membership grader) is unaffected by this finding.
- R-SC-2 (semantic-correct-but-unparseable audit label) queued for iter-8.

**GO dispatched to COO:** 20260427T145826Z. COO to dispatch .067 GO to 1.3.0_DS.

**Iter-7 compiler delivered:** 1.3.0_DS shipped at 20260427T150546Z.
- `f5095ac0` — runner.py experiment_log path fix (3-4 LOC, redirects to comp/results/dev-click-001/)
- `7ee0859c` — compiler v7, class_hierarchy_correction node
- Node content (verbatim): `Command.direct_subclasses: [_BaseCommand, Group]` + `_MultiCommand.parent_class: Group (NOT a direct Command subclass)` + `_CommandCollection.parent_class: Group (NOT a direct Command subclass)`
- compiler_content_sha: 923071d5. comp-build: 1198 nodes / 979 edges.
- All gates passed: ds-commit-gate.sh, pytest 458/0, experiment_log 6 entries intact.

**COO validated** and dispatched .068 scoring TO to 2.1.0_SC_CompLearns (commit 6cd1e4c2).
**Runner path fix active** — iter-7 experiment_log will auto-append, no manual backfill needed.

**Iter-7 verdict:** DISCARD, PATTERN C (commit 4e0ecd69)
- ab_lift=0.0 across all selectors
- q03 did NOT flip with Command-perspective + NOT-exclusion framing
- Two mutation families now exhausted: import/class_inherits (iters 2-5) + class_hierarchy_* (iters 6-7)
- R-CTO-3 stop-rule TRIGGERED: corrected within-family retry still PATTERN C

**Stop-rule ruling issued:** Click dev-click-001 reclassified from lift-signal to shakedown target for q03 surface.

**CVO brief filed:** `org/tier1_exec/3.1.0_SA_CVO/inbox/20260427T162800Z_from_1.1.0_SA_CTO_iter7_result_reclassification_ruling_brief.md`

**Provisional iter-8 position:** No further scored fact-node mutations on q03. Run q02/q11 non-ratchet diagnostic ablation (.069), then close click dev-loop. Awaiting CVO Q1 ruling before dispatch.

**Open items:**
- experiment_log path fix: f5095ac0 ineffective for click target — DS fix required
- R-SC-2 (semantic-correct-but-unparseable label): pre iter-8
- ADVI_RDVSDS DT RAVC: separate CTO ruling needed (Phase 1 leaderboard gap — outside COMP scope)

---

## CVO Reclassification Ruling + Iter-8 Decisions

**CVO response:** `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T163500Z_to_1.1.0_SA_CTO_iter7_reclassification_review.md`

**R-CTO-1 (P0):** Reclassification confirmed. Click q03 CLOSED as scored lift target. Edge topology was already in the failed evidence base (class_inherits edges in iters 2-5). No unexamined mechanism justifies further scored iterations.

**R-CTO-2 (P1):** Position-based injection is a new presentation-policy mechanism family, not iter-8. If run later, label it separately — do not keep click open for it.

**R-CTO-3 (P1 — design lesson):** Strong parametric priors can dominate correct injected structure even when the graph is already right. CVO §4: "closing click is harvesting the actual systems-program insight the target surfaced."

**Iter-8 ruling issued to COO (20260427T163733Z):**
- Click q03 scored mutations: CLOSED
- Allowable: (1) .069 q02/q11 non-ratchet diagnostic ablation — gated on SC implementing R-SC-2 simultaneously; (2) experiment_log path fix (DS); (3) click post-mortem
- Stage 3 planning begins in parallel

**Current state:** Waiting for COO to author .069 TO and click closeout task. Stage 3 design brief pending.

---

## Stage 3 Design Brief Cycle (codified per workflow doctrine)

**Brief filed:** `org/tier1_exec/3.1.0_SA_CVO/inbox/20260427T170000Z_from_1.1.0_SA_CTO_stage3_design_brief.md` (archived at briefs/COMP_LEARNS_stage3_design_brief.md). Commit `fd0baa13`.

**Workflow doctrine codified at same commit:** prompt.md §5 — CTO↔CVO collaborative cycle, brief types (iteration_close / closeout / new_prd / ad_hoc_review), 7-section skeleton, routing pattern, iteration cadence rules.

**CVO ruling received:** `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T171500Z_to_1.1.0_SA_CTO_stage3_design_review.md` (commit b5ddd614).

### Rulings actioned

| Ruling | Priority | Status | Action |
|--------|----------|--------|--------|
| R-CTO-1 | P0 | Accepted | Pre-screen redefined as triage tool, NOT ceiling detector. Wrong\|Wrong → INVESTIGATE for structured-context opportunity, not automatic ceiling. Correct\|Wrong → INVESTIGATE for grader/overload artifact. Will codify in Stage 3 PRD. |
| R-CTO-2 | P0 | Accepted | All 4 conditions (C1+C2+C3+C4) mandatory from primary case dispatch. No phasing. Will codify in PRD. |
| R-CTO-3 | P0 | Accepted | Delivered-context audit ship-blocker. Per-question per-condition sidecar referenced by scorecard, not raw text in scorecard JSON. R-DS-1 dispatched to DS. |
| R-CTO-4 | P1 | Accepted | R-SC-2 status correction — it is COMPLETE per scoring_regime_honesty_note.md:72-93 with artifact at r_sc_2_failure_mode_audit.md. Premise drift in brief acknowledged. |
| R-COO-1 | P0 | Dispatched to COO | Two-lane partition: INCLUDE pool (primary metric) + SENTINEL pool (excluded but retained in metadata). Both preregistered before iteration. |
| R-COO-2 | P1 | Dispatched to COO | Path A (sphinx) default with HARD off-ramp to Path B if pre-screen fails sphinx. |
| R-SC-1 | P0 | Dispatched to SC | Stage 3 dispatch blocked on R-SC-2 SEMANTICS integrated into pre-screen, not just R-SC-2 existence. |
| R-SC-2 | P1 | Dispatched to SC | Add "full-source overload candidate" label to pre-screen output to distinguish genuine ceilings from compression-recoverable Wrong\|Wrong. |
| R-DS-1 | P1 (gates dispatch) | Dispatched to DS | Per-question per-condition delivered-context sidecar implementation. |
| R-DS-2 | P1 | Dispatched to DS | Preserve ability to run pilot on Wrong\|Wrong INVESTIGATE candidates. |

### CVO §4 unknown-unknown (critical)

CVO's epistemological warning: "the Stage 3 pre-screen could optimize too aggressively for compiler success and weaken the program's ability to discover null results honestly." Fix: PRE-REGISTER both INCLUDE pool AND excluded/sentinel pool BEFORE iteration begins. Then a null on the INCLUDE pool is a serious challenge to the proposition; success only on INCLUDE pool is honestly reported as "success under pre-screened measurement-room conditions," not a universal claim. This is a binding design constraint for Stage 3 PRD.

### CVO §5 cross-cutting framing

"The most valuable Stage 3 design move is not sphinx itself. It is the shift from 'find a harder target' to 'define measurement room, attribution clarity, and null-result survivability before the next PRD exists.' That is the right correction after click."

### Next CTO action

Author Stage 3 PRD (`docs/architecture/COMP_LEARNS_STAGE3.md` or amendment to existing PRDs). PRD must codify:
1. Triage-not-ceiling pre-screen with R-SC-2 semantic integration
2. Two-lane partition with pre-registration discipline
3. All 4 conditions mandatory
4. Delivered-context audit as per-question sidecar
5. Path A default + Path B off-ramp criteria
6. Null-result survivability protocol

**MCPs dispatched:** COO (R-COO-1/2 + ship-blockers binding) | SC (R-SC-1/2) | DS (R-DS-1/2). All workers have rulings in their inbox.

---

## Stage 3 PRD V1 Authored

**PRD:** `docs/architecture/COMP_LEARNS_STAGE3.md` — V1, 2026-04-27, 1.1.0_SA_CTO

**Codifies all CVO Stage 3 rulings:**
- §2 Triage-not-ceiling pre-screen with R-SC-2 semantic consumption (R-CTO-1 P0, R-SC-1 P0)
- §2.4 Wrong|Wrong subtype distinction with "full-source overload candidate" label (R-SC-2 P1)
- §3 Two-lane partition (INCLUDE + SENTINEL) with preregistration discipline (R-COO-1 P0)
- §4 All 4 conditions mandatory from primary case dispatch + decision tree codified (R-CTO-2 P0)
- §5 INVESTIGATE pilot machinery with promotion/demotion rules (R-DS-2 P1)
- §6 Per-question per-condition delivered-context sidecar (NOT scorecard bloat) (R-CTO-3 P0, R-DS-1)
- §7 Sphinx Path A default + Path B mandatory off-ramp criteria (R-COO-2 P1)
- §8 Click design lesson promotion → COMP_LEARNS_DESIGN_LESSONS.md (follow-on, not ship-blocker)
- §9 Null-result survivability — preregistration, decision tree, sidecar, reporting discipline as structural defenses (CVO §4 unknown-unknown)
- §10 Ship-blocker checklist (9 items joint CTO+COO+SC+DS gate before dispatch)

**COMP_LEARNS.json updated** to register Stage 3 PRD as canonical artifact.

**Next CTO action:** File brief to CVO for Stage 3 PRD V1 review per workflow doctrine (new_prd brief type → CVO ruling → V2 amendment if needed → COO TO decomposition).

---

## Stage 3 PRD V1.1 — CVO Review Feedback Applied

CVO PRD review feedback received (informal direct relay from Andrew). Five corrections applied:

| Issue | Section | V1 → V1.1 change |
|-------|---------|------------------|
| INVESTIGATE pilot rule too permissive | §5.2 | N raised 3-5 → 8 per condition; paired C4+C1 trials; promotion requires absolute floor (≥5/8) AND positive delta (C4-C1 ≥ 2). Adds prior-dominated demotion rule (C1 ≥ 6/8 + delta ≤ 0). |
| Either-pool-empty hard fail too rigid | §3.1 | INCLUDE empty still hard-rejects; SENTINEL empty allowed only with explicit `sentinel_review_note` in packet manifest. Asymmetric rule reflects asymmetric risk. |
| "Compression gain" naming loose | §4.3 | Renamed to "Addressed-delivery gain" with caveat that C3→C4 bundles delivery-shape and addressing, not pure compression. |
| Status metadata drift | §1 header | "Authoring (V1)" → "V1.1" with CVO review reference. |
| Sidecar audit integrity gap | §6.3 | Added per-blob SHA-256 hashes in manifest + manifest SHA on scorecard. End-to-end content addressing for audit verifiability. |

**Pilot cost recomputed:** |INVESTIGATE| × 8 trials × 2 conditions = 16 calls per investigated question; <100 calls per target.

**PRD V1.1 committed.** Ready for COO TO decomposition once SC and DS receive R-SC-1/R-SC-2/R-DS-1/R-DS-2 implementation TOs.

---

## Stage 3 TO Decomposition + Parallel-Wave Progress

**COO decomposition complete:** Stage 3 PRD V1.1 (e4ac581c) decomposed into 8 TOs (.069-.076) at commit 592b0b2b. .073 packet schema shipped at 3ccdd425 (asymmetric empty-pool rule confirmed).

| TO | Owner | Scope | Status |
|----|-------|-------|--------|
| .069 | COO | q02/q11 diagnostic ablation (non-ratchet) | STUB/DEFERRED — gates on .068 + R-SC-2 |
| .070 | 1.3.0_DS | Sidecar R-DS-1: per-Q per-condition context blobs + SHA-256 hashes + manifest_sha | GO dispatched |
| .071 | 1.2.0_DS | Pilot machinery R-DS-2: paired C4+C1 N=8, dual-condition gate | GO dispatched |
| .072 | 2.1.0_SC | R-SC-2 taxonomy + pre-screen protocol | COMPLETE (07fbc543 + 4806174b + b12872a1) — partial-correct ambiguity escalated to CTO |
| .073 | COO | Stage 3 packet schema | COMPLETE (3ccdd425) — schema_version=3, sentinel_review_note field, preregistration_reviewers gate |
| .074 | 1.1.0_DS | Sphinx question pool (≥10 candidates, ≥5 cross-module) | GO dispatched |
| .075 | 2.1.0_SC | Sphinx pre-screen execution | Gates on .072 + .074 |
| .076 | 1.1.0_SA_CTO (me) | Pre-screen review + Path A/B off-ramp gate + preregistration | Gates on .075 |

**Sequencing:** parallel wave (.070+.071+.072+.073+.074) all started; sequential (.075 then .076 then primary case dispatch).

**.072 partial-correct ambiguity ruling issued:**
SC escalated a real protocol gap: a response giving M of N gold set members in prose, with the remaining (N-M) members ABSENT (not asserted-wrong), did not map cleanly to any of the 5 R-SC-2 labels. SC's heuristic ("non-trivial structure of missing member") was correct in spirit but too subjective for protocol use.

**Ruling:** Add a sixth primary label `semantic-partial-correct-unparseable` with deterministic cross-regime subtype rules:
- (zero-shot partial, full-source full-correct) → promote to INCLUDE
- (zero-shot partial, full-source partial w/ MORE coverage) → full_source_overload_candidate, pilot_eligible=true
- (zero-shot partial, full-source partial w/ SAME coverage) → grader_artifact (knowledge gap), pilot_eligible=false
- (zero-shot partial, full-source partial w/ FEWER coverage) → grader_artifact (anomaly), pilot_eligible=false
- (zero-shot partial, full-source partial w/ DIFFERENT coverage) → semantic-ambiguous, escalate
- Multi-trial guard: stable partial coverage across ≥4/6 trials required for label assignment; otherwise semantic-ambiguous.

Click q03 retroactive: NOT partial-correct (response was {_BaseCommand, Group, _MultiCommand, CommandCollection}, set was extracted, set was wrong → parseable-wrong). Reclassification stands.

**.065 v0 forensic finding (independent confirmation of reclassification):**
SC's v0 random_unique_win forensic concluded the v0 win was on q09 or q10 (prior-knowledge questions), NOT on q02/q03/q11. Probable-luck training-prior hit. v0 graph does not even contain _BaseCommand. The iter-7 reclassification ruling stood on its own merits; .065 confirms it independently.

**Path fix shipped (DS):** f8695a29 — _TARGET_RESULTS_MAP={"click":"dev-click-001"} closes the experiment_log integrity gap.

**Current state:** 3 TOs in flight (.070, .071, .074), .075 waiting for .072 amendment + .074, .076 (mine) waiting for .075. R-SC-1 + R-SC-2 + R-DS-1 + R-DS-2 + R-COO-1 + R-COO-2 all in active implementation. CTO is idle until SC amends .072 with the new label OR .076 dispatches.

---

## Sphinx Pre-Screen + .076 Ruling + Grader-Format Design Escalation

**.075 SC delivered (commit 0bb57890):** sphinx pre-screen complete. 12 questions: INCLUDE=2, SENTINEL=0, INVESTIGATE=10. PATH_B trigger 1 fired (INCLUDE < 5).

**Critical finding:** 8 of 10 INVESTIGATE = grader_artifact dominance. Judge gives correct answers from parametric prior in BOTH zero-shot AND full-source but wraps in markdown the exact-match grader cannot parse. This is target-independent — Path B alone won't fix it.

**.076 ruling shipped (commit 38d00105):** `org/tier1_exec/1.1.0_SA_CTO/deliverables/COMP_LEARNS.076_pre_screen_review_ruling.md`
- Ruling 1: q01/q07 reclassified INCLUDE → grader_artifact (SC default B). Format-elicitation by context bulk does not satisfy "find/localize/act on correct structural context."
- Ruling 2: PATH_B_MANDATORY confirmed by trigger 1
- HOLD on Path B target re-selection pending CVO grader-format ruling
- Answer-key schema gap (sphinx ab_answer_key.yaml) routed to COO for DS dispatch
- .069 q02/q11 ablation further deferred under same grader question

**CVO closeout brief filed (same commit):** `org/tier1_exec/3.1.0_SA_CVO/inbox/20260427T195000Z_from_1.1.0_SA_CTO_sphinx_prescreen_closeout_grader_format_design_question.md`
- Three options: A (format-aware grader) / B (constrained question types) / C (two-grader cross-check)
- CTO lean: Option C — preserves exact-match rigor while making format-elicitation surface visible as runtime data
- Q1 (grader resolution) + Q2 (q03/q05 pilot under unresolved grader) are P0 — must rule before Path B target re-selection or sphinx pilot dispatch
- Q3 (PRD amendment timing) + Q4 (click re-audit) are P1
- Q5 (second-order unknown-unknowns) is P0+ epistemological

**Significance:** This is the CVO §4 unknown-unknown materializing. The Stage 3 PRD V1.1 design (R-SC-2 semantic labels + asymmetric SENTINEL rule + sentinel_review_note) made the grader-artifact pattern visible — without those defenses, the 0-SENTINEL result would have read as "no prior dominance" instead of "8-10 prior-dominated under format-aware grading." The pre-screen surfaced exactly what Stage 3 was designed to catch: a structural measurement problem before iteration burned compute.

**Workforce idle:** All workers and COO are now idle pending CVO ruling. No Path B work begins until CVO Q1/Q2 ruling lands.

**ACKs dispatched:** COO (PATH_B confirmed + HOLD), SC (Ruling 1 accepted + brief filed for awareness).

---

## CVO Grader-Governance Ruling + V1.2 PRD

**CVO ruling received:** `org/tier1_exec/3.1.0_SA_CVO/responses/20260427T200500Z_to_1.1.0_SA_CTO_sphinx_prescreen_grader_format_review.md` (commit e3393b26).

**CVO refinement of my Option C:** Not a single-choice grader replacement question — a **governance split**:
- Semantic-aware grading governs **pre-screen partitioning + artifact characterization + INVESTIGATE/SENTINEL triage**
- Exact-match grading remains the **primary ratchet/champion score**
- Disagreement rate becomes a **first-class runtime metric**

This is a better design than my proposal — preserves Stage 1+2 ratchet continuity while making format-elicitation visible as runtime data instead of post-hoc audit.

**Rulings actioned (V1.2 PRD shipped at 95f8c0d3):**

| Ruling | Priority | Status | V1.2 location |
|--------|----------|--------|---------------|
| R-CTO-1 | P0 | Codified | §11.1-11.2 governance split + reasoning |
| R-CTO-2 | P0 | Codified | §11.5 Path B HOLD until §11.3 ships |
| R-CTO-3 | P1 | Followed | precise reactive amendment, not speculative rewrite |
| R-CTO-4 | P2 | Acknowledged | click q03 reclassification stands, no re-audit |
| R-COO-1 | P0 | Dispatched to COO | sphinx q03/q05 pilot AUTHORIZED in parallel + Path B HOLD |
| R-COO-2 | P1 | Codified | §11.4 pilot scope cap (diagnostic-only, no override of PATH_B_MANDATORY, no packet authoring) |
| R-SC-1 | P0 | Dispatched to SC | per-question + per-target disagreement emission |
| R-SC-2 | P1 | Dispatched to SC | grader_artifact split into format-elicitation vs semantic-prior unparseable |
| R-DS-1 | P1 | Dispatched to DS | runner dual-output emission, both grader outputs in scorecard |
| R-DS-2 | P2 | Dispatched to DS | sphinx answer-key schema gap kept SEPARATE from governance work |

**Ship-blocker checklist updated (§10):**
- First 8 boxes CLOSED for sphinx (R-SC-2 semantics, FSO-C label, sidecar, pilot machinery, packet schema, Path A criteria, sphinx pre-screen run, off-ramp gate)
- 4 NEW boxes OPEN for V1.2: grader governance implementation, Path B target sub-PRD authoring, Path B pre-screen run, Path B off-ramp gate

**§11.4 sphinx q03/q05 pilot in flight:**
COO authoring TO. Diagnostic only — uses .071 paired C4+C1 N=8 machinery, scored under exact-match grader (V1.2 governance not yet shipped; semantic-aware data on q03/q05 is best-effort SC manual audit during scoring).

**§12 future preregistration question** flagged per CVO §4 unknown-unknown: is the program testing "knowledge delivery to the judge" or "gradeable answer production by the judge"? Surface for next CVO design cycle when a future target shows chronic unparseable formatting under all conditions.

**Workforce status:** SC + DS have V1.2 governance implementation directives. COO authoring sphinx q03/q05 pilot TO (parallel work) + 3 governance TOs (sequential gate). All four lanes activated.
