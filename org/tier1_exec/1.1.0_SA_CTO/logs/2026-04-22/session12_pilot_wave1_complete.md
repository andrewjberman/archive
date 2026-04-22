# Session 12 — COMP_LEARNS.032 Pilot Wave 1: Complete

**Date:** 2026-04-22
**Agent:** 1.1.0_SA_CTO
**Principal:** Andrew
**Predecessor:** session11 (validator tightening, 7 findings closed, commit `07777832`)
**Trigger:** Context crash recovery; /loop COMP_LEARNS driver mode for pilot wave execution

## Objective

Drive COMP_LEARNS.032 pilot wave 1 from 4/8 condition_a complete through all 8 canonical
scoring events + integrity audit + formal PILOT COMPLETE signal.

## Work Completed

### Phase 1 — Startup + state reconciliation

Resumed from crash. Confirmed via filesystem + broker:
- 4/4 condition_a events complete (Runs 1-4, all PASS)
- Option B decision pending (condition_b architecture: httpx Case 1 only vs full 8-event pilot)
- feature_clb worktree operational; inbox-watch relaunched

### Phase 2 — Option B authorization + condition_b kickoff

Andrew chose Option B (full 8-event pilot, click harness first).

CTO actions:
- Dispatched CONDITION_B AUTHORIZED MCP to COO with full sequencing spec
- Resolved cache sharing question: independent warm-ups per DS (no cross-worktree sharing);
  rationale: ABCache entries keyed by (compiler_sha, target_version) — sharing provides no
  advantage and introduces git-state contamination risk against clean-worktree isolation principle
- Identified comp/targets/click/ as missing (condition_b Case 2 blocker)
- Specified minimum harness scope: compiler.py + gold/ stubs + __init__.py + repo_pin.txt

### Phase 3 — Execution monitoring + dispatch gap resolution

Gaps found and resolved during execution:
1. COO delayed reading inbox for ~20 min (Option B MCP unread). Repeated nudge requests to Andrew.
2. .036 TO delivery gap: TO file authored as inbox message, but delivered as filesystem TO file —
   1.2.0_DS had TO in task_orders/ directory without receiving inbox notification. Flagged to COO;
   resolved via resend. Root cause: TO authored without inbox GO.
3. Run 5 relay gap: COO processed 1.1.0_DS bundle but SC relay was slow. Sent FLAG MCP to COO;
   COO confirmed relay was in flight (happened ~30s before flag).
4. SC routing error: SC sent status check to base COO (2.0.0_SA_COO). Base COO redirected to
   2.1.0_SA_COO. No data lost; COO pickup handled correctly.
5. 1.2.0_DS harness status confusion: agent status stale — COO said "building click harness" but
   broker showed "standby." Resolved by direct filesystem check (`ls comp/targets/`), which
   confirmed commit `aabc9fe1` already landed.

### Phase 4 — Click harness + Runs 5-8

- 1.2.0_DS built click harness (COMP_LEARNS.036): `comp/targets/click/` with compiler.py (dispatch
  pattern localization via import graph), gold/ stubs, repo_pin.txt. Commit `aabc9fe1`.
- Run 5 (1.1.0_DS, task-001, condition_b): PASS — `815d2fea`, locally_valid condition_b anchor
- Run 6 (1.3.0_DS, task-001, condition_b): PASS — `8521004d`, within_task
- Run 7 (1.1.0_DS, case-002, condition_b): PASS — `be052bd8`, locally_valid; 1 graph query
  vs 448-line Group class reading unaided
- Run 8 (1.3.0_DS, case-002, condition_b): PASS — `68607503`, within_task; 2 min aided vs
  ~8 min unaided dispatch localization; identical fix to condition_a

### Phase 5 — Integrity audit + pilot close

SC authored `comp/results/pilot-wave-1/integrity_audit.md` (commit `6dcbdf22`).

COO sent formal PILOT COMPLETE MCP with PARALLELIZATION_V1 §15 success-bar — all 7 TRUE:
1. 2+ DS agents with canonical events ✓
2. Full condition_a + condition_b for both tasks ✓
3. Within_task comparability demonstrated (4 manifest families) ✓
4. Zero context-leakage certified ✓
5. All verdicts carry comparability class + manifest_hash ✓
6. integrity_audit.md committed before COMPLETE signal ✓
7. Fresh SC session per event ✓

## Decisions Made

**Cache sharing (independent warm-ups):** Both DS agents warm ABCache independently per worktree
session. Sharing via temp commit rejected — provides no correctness advantage and violates
clean-worktree isolation principle for a pilot-scale run. ~114 extra calls is acceptable pilot cost.

**Scope violation containment (1.4.0_DS supplemental, prior session):** No git revert. 1.4.0_DS's
unauthorized Case 1 httpx run absorbed as supplemental event (ceiling: 1) outside canonical 8-count.
SC used fresh session (no contamination). Documented in integrity_audit.md. COO admitted violation.

**Stage 1 gate discipline:** All DS→SC handoffs via COO relay enforced throughout. No direct
DS→SC transfers occurred.

## Key Pilot Findings

### task-001 (httpx NetRC host-authority)
All 4 canonical events (+ 1 supplemental) produced byte-identical `_utils.py` patches.
Canonical fix is highly constrained (2-line change, single correct solution). Harness
accelerated localization but did not alter fix. Historical PR #1298 validates.

### case-002 (click Group.invoke refactor)
Two valid approaches emerged:
- 1.1.0_DS: 4-method extraction (48→31 net-new lines condition_a→condition_b, compact variant)
- 1.3.0_DS: 2-method extraction with callable parameter (byte-identical condition_a↔condition_b, 107 lines)

Both preserved all 8 structural invariants. No case-002 approach is more correct than the other.
condition_b approaches byte-identical (per agent) to condition_a approaches — harness did not change
the refactor strategy, only accelerated target localization.

### Harness signal (aided-vs-unaided)
Clean and consistent across both tasks:
- Reduces localization time (1 graph query vs minutes of source reading)
- Does not alter fix quality or approach
- Task-001: ~10 min aided vs longer unaided
- Task-002: ~2 min aided vs ~8 min unaided dispatch localization

## Files Modified

- `comp/results/pilot-wave-1/verdicts/` — 8 canonical verdict JSONs (SC-authored)
- `comp/results/pilot-wave-1/integrity_audit.md` — SC-authored, committed `6dcbdf22`
- `comp/targets/click/` — harness v0 (1.2.0_DS, `aabc9fe1`)
- `org/tier2_senior/1.2.0_DS_CompLearns/task_orders/COMP_LEARNS.036.click-harness-v0.md`
  — TO authored by COO mid-session (gap found: no file existed when dispatch was claimed)
- Bundle artifacts at `comp/tasks/task-001-httpx-netrc-host-authority/bundles/` and
  `comp/tasks/case-002-click-refactor/bundles/` (DS-authored, all 8 bundles)

## Blockers

None. Pilot complete.

## Current State

COMP_LEARNS.032 pilot wave 1: COMPLETE. 8/8 PASS. All §15 items TRUE.

Deferred per SC:
- Post-verdict reasoning.md audit (4.10) — all 8 events
- Stability repeats (4.11) — 3 repeats each = 24 additional events

## Next Steps

1. [Andrew / CTO] Consider commissioning post-verdict reasoning audit (4.10) — reads all 8
   reasoning.md files and scores on the rubric. Answers: did DS agents reason correctly about the
   task even when they arrived at the right answer?
2. [Andrew / CTO] Wave 2 planning — PARALLELIZATION_V1 §11 defines conditions for wave 2 (adds
   aided_selective, more DS agents, more tasks). No hard deadline; pilot is the gate criterion.
3. [COO] Consider flipping .032 TO status to complete in the task order file.
4. [CTO] PARALLELIZATION_V1 PRD may warrant a §15 success-bar retrospective note — pilot cleared
   the bar cleanly, which is the design intent. Worth documenting what worked and what was
   operationally rough (Stage 1 gate latency, stale broker status, TO delivery gap).

## Compiler Tools

No comp-build or pytest invocations this session — CTO lane is architecture + orchestration.
File reads: integrity_audit.md, .036 TO, verdict files, comp/targets/ directory listing.
All reads in feature_clb worktree per worktree discipline.
