# Case 1 Two-Phase Scoring — 2.1.0_SC_CompLearns

**Date:** 2026-04-24
**Task Order:** COMP_LEARNS.058 (case1-two-phase-scoring)
**Status:** COMPLETE

---

## Objective

Score Case 1 (httpx NetRC host/authority bug, task-001-httpx-netrc-host-authority) under the
two-phase model per PRD §3.5. Phase 1 produces frozen verdicts from changes.patch +
test_output.txt. Phase 2 extracts navigation-efficiency metrics from nav_log.jsonl after
verdict freeze.

---

## Compiler Tools

| Tool | Command | Result | Note |
|------|---------|--------|------|
| Phase 1 gate 1 | ls bundles/ds-1.4.0-condition_a/ && ls bundles/ds-1.2.0-condition_b/ | PASS | All 4 required artifacts present (+ extra refactor.patch in condition_a, no scoring impact) |
| Phase 1 gate 2 | mkdir -p comp/results/wave-3b/verdicts comp/results/wave-3b/metric_audit | PASS | Output dirs created |
| Phase 2 gate 1 | ls comp/results/wave-3b/verdicts/ | grep case-001 | PASS | Both Phase 1 verdict files present and committed at 14f6b44d |
| Phase 2 gate 2 | python aided comp_calls count | PASS | aided comp_calls: 3 (gate requires >= 1) |
| Phase 3 gate | ls comp/results/wave-3b/ | PASS | verdicts/ + metric_audit/ + integrity_audit.md all present |

**What worked:** Phase gate structure clean. Python inline comp_call count verified aided harness usage before Phase 2 began.

**What failed:** None. condition_a test_output.txt truncated before ac-3 final count line (22 lines), but reasoning.md confirms "46 passed, 1 warning (exit 0)" — resolved by cross-referencing reasoning.md in Phase 2.

**Gap found:** Token metric quality issue — nav_logs have checkpoints at incomparable session positions (condition_a post-hypothesis upper bound 800; condition_b session-end 15200). Token delta not a reliable efficiency metric for Case 1. Flagged in noise_flags.

---

## Work Completed

### 1. Startup and GO receipt

Registered on MCP broker. Inbox watcher launched. GO received from 2.1.0_SA_COO via broker channel (task b1s2nduaa exit). RAVC ACK sent. TO status flipped staged -> pending.

### 2. Phase 1 — Verdict determination

Read changes.patch + test_output.txt for both conditions. reasoning.md excluded.

**condition_a (1.4.0_DS_CompLearns, unaided):**
- Fix: authority.split(':')[0] before netrc.authenticators() call in httpx/_utils.py
- New test: test_netrc_non_standard_port (url=http://netrcexample.org:8080)
- ac-1: 3 passed, 40 deselected → PASS
- ac-2: 1 passed, 42 deselected → PASS
- ac-3: 46 dots [100%] + warning (output truncated; confirmed by reasoning.md: 46 passed, 1 warning, exit 0) → PASS
- Verdict: PASS

**condition_b (1.2.0_DS_CompLearns, aided):**
- Fix: identical to condition_a
- New test: identical to condition_a
- ac-1: 3 passed, 40 deselected → PASS
- ac-2: 1 passed, 42 deselected → PASS
- ac-3: 46 passed, 1 warning → PASS
- Verdict: PASS

Both Phase 1 verdicts committed at `14f6b44d` (Phase 1 freeze).

### 3. Phase 2 — Metric extraction

Read both nav_log.jsonl files after Phase 1 freeze. Read both reasoning.md files for confidence_note (Phase 2 only).

| Metric | condition_a (unaided) | condition_b (aided) | Delta (aided - unaided) |
|--------|-----------------------|---------------------|------------------------|
| Wall-clock to first correct (sec) | 10 | 10 | 0 (TIE) |
| Tokens to first correct (checkpoint) | 800 (upper bound) | 15200 (session-end, upper bound) | +14400 (unreliable — see noise flags) |
| Files before decisive | 0 | 0 | 0 |
| Irrelevant files touched | 3 | 2 | -1 (aided fewer) |
| comp_calls | 0 | 3 | +3 (expected) |
| decisive_file_found | true | true | — |

Noise flags raised: token_metric_unreliable (checkpoint positions incomparable), wall_clock_tie (10s each), identical_patches, condition_a_prior_exposure, condition_a_nav_log_h1_missing.

Confidence note: aided agent showed higher structural confidence (graph-derived H1 before file read); unaided had incorrect H1 (file path resolution) discarded within _utils.py read. Both converged identically.

### 4. Artifacts written and pushed

- comp/results/wave-3b/verdicts/case-001-ds-1.4.0-condition_a-run-1.json (Phase 1 freeze 14f6b44d)
- comp/results/wave-3b/verdicts/case-001-ds-1.2.0-condition_b-run-1.json (Phase 1 freeze 14f6b44d)
- comp/results/wave-3b/metric_audit/case-001-efficiency-delta.json (Phase 2 c3d52426)
- comp/results/wave-3b/integrity_audit.md (Phase 2 c3d52426, Case 2 section pending .059)
- TO status flipped to complete (c3d52426)

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Wall-clock tied at 10s each | TO definition: first file_open to first correct hypothesis. Both opened decisive file first. Aided pre-file comp_calls (18s) show from-session-start aided took 28s vs unaided 20s — noted in metric. |
| Token comparison flagged unreliable | Checkpoints at different session positions; delta is a checkpoint-position artifact not a navigation metric. Cannot use for efficiency comparison. |
| Identical patches: score each independently | Same as Case 3 precedent. Each condition's nav_log and AC run are independent evidence. Convergence is a finding. |
| condition_a nav_log H1 missing: use H2 timestamp | Nav_log records H2 (correct=true); reasoning.md shows H1 existed but was discarded within the same file read. Wall-clock of 10s reflects H2 recording; flagged in noise_flags. |
| ac-3 condition_a truncated output: PASS | reasoning.md Phase 2 read confirmed "46 passed, 1 warning (exit 0)". Dot pattern (46 dots) consistent with condition_b's 46 passing. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| comp/results/wave-3b/verdicts/case-001-ds-1.4.0-condition_a-run-1.json | Phase 1 verdict: PASS | 14f6b44d |
| comp/results/wave-3b/verdicts/case-001-ds-1.2.0-condition_b-run-1.json | Phase 1 verdict: PASS | 14f6b44d |
| comp/results/wave-3b/metric_audit/case-001-efficiency-delta.json | Phase 2 metric audit | c3d52426 |
| comp/results/wave-3b/integrity_audit.md | Integrity audit (Case 1 section; Case 2 pending) | c3d52426 |
| org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.058.case1-two-phase-scoring.md | Status: staged -> pending -> complete | c3d52426 + this commit |

---

## Blockers

None. COMP_LEARNS.058 complete. Standing by for .059 GO (Case 2 scoring) from COO.

---

## Current State

COMP_LEARNS.058 complete. Both Case 1 conditions PASS with identical patches. Wall-clock TIE (10s each, first-file_open metric). Token comparison unreliable. Aided -1 irrelevant file. Phase 1 freeze at 14f6b44d; Phase 2 at c3d52426. MCP COMPLETE sent to COO. Awaiting .059 GO.
