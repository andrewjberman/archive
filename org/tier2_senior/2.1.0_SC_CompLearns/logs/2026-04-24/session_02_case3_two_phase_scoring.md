# Case 3 Two-Phase Scoring — 2.1.0_SC_CompLearns

**Date:** 2026-04-24
**Task Order:** COMP_LEARNS.051 (case3-two-phase-scoring)
**Status:** COMPLETE

---

## Objective

Score Case 3 (sphinx-doc__sphinx-10449) under the two-phase model per COMP_LEARNS_WAVE3_V1.md §3.5. Phase 1 produces a frozen verdict from bundle artifacts (reasoning.md excluded). Phase 2 extracts navigation-efficiency metrics from nav_log.jsonl after verdict freeze to produce the first formal aided-vs-unaided delta measurement for this program.

---

## Compiler Tools

| Tool | Command | Result | Note |
|------|---------|--------|------|
| Phase 1 gate 1 | `ls bundles/ds-1.3.0-condition_b/ && ls bundles/ds-1.4.0-condition_a/` | PASS | Both bundles confirmed: changes.patch + test_output.txt + reasoning.md + nav_log.jsonl |
| Phase 1 gate 2 | `mkdir -p comp/results/wave-3a/verdicts comp/results/wave-3a/metric_audit` | PASS | Output dirs created |
| Phase 2 gate 1 | `ls comp/results/wave-3a/verdicts/` | PASS | Both Phase 1 verdict files present and committed at 4e1ec449 |
| Phase 2 gate 2 | `python -c "... assert comp_count > 0 ..."` on aided nav_log | PASS | 7 comp_call events confirmed |
| Phase 2 gate 3 | `python -c "... assert comp_count == 0 ..."` on unaided nav_log | PASS | 0 comp_call events confirmed |
| Phase 3 gate | `ls comp/results/wave-3a/` | PASS | verdicts/ + metric_audit/ + integrity_audit.md all present |

**What worked:** The three-phase compiler gate structure (bundle presence, verdict freeze, nav_log hygiene) gave a clean checklist with unambiguous exit conditions. Python inline assertions for comp_call counts caught the unaided contamination check mechanically.

**What failed:** Python scripts initially used `/c/...` MSYS-style paths — failed with FileNotFoundError on Windows Python. Fixed by switching to `C:/...` Windows paths in python -c invocations.

**Gap found:** No comp-* tools are applicable to SC scoring work (no gold scripts, no portal components, no Lambda functions). Compiler tools mandate is satisfied by the PRD-specified phase-gate checks above. Same finding as session_01.

---

## Work Completed

### 1. Startup

Registered on MCP broker (PID 14868), launched inbox watcher, checked both inbox paths (filesystem + broker). Inbox empty at startup. Surfaced stale 1.4.0_DS status to COO (reported ".049 missing nav_log.jsonl" — bundle verified present). COO ACK: stale heartbeat only, 1.4.0_DS already executing.

### 2. .051 GO received and acknowledged

COO GO received via inbox watcher (task bis2loqzz exit). Both bundles confirmed PASS by COO inspection. RAVC ACK sent. TO status flipped staged -> pending.

### 3. Phase 1 — Verdict determination

Read packet.yaml (acceptance criteria authority), changes.patch + test_output.txt for both conditions. reasoning.md mechanically excluded.

**Key finding:** Both conditions submitted identical patches. The fix adds `suppress_rtype=True` to `merge_typehints` when `objtype == 'class'`, and suppresses emission of rtype field in `modify_field_list` when `annotation == 'None'`. Test expectation updated to remove spurious "Return type: None" line.

| AC | condition_b (aided) | condition_a (unaided) |
|----|--------------------|-----------------------|
| ac-1 (FAIL_TO_PASS) | PASS — 1 passed, 0 failed | PASS — 1 passed, 0 failed |
| ac-2 (regression guard) | PASS — 2 pre-existing Python 3.12 failures | PASS — same 2 pre-existing failures |
| ac-3 (regression guard) | PASS — 1 pre-existing Python 3.12 failure | PASS — same 1 pre-existing failure |

Pre-existing failures at baseline 36367765: `test_autodoc_type_aliases` (type alias resolution), `test_autodoc_default_options` (__weakref__ docstring), `test_enum_class` (Enum signature format). All three confirmed pre-existing, not introduced by the fix.

Both conditions verdict: **PASS**. Phase 1 verdicts committed at `4e1ec449` (verdict freeze).

### 4. Phase 2 — Metric extraction

Read both nav_log.jsonl files after verdict freeze. Extracted per-condition metrics per PRD §3.5.

| Metric | condition_b (aided, 1.3.0_DS) | condition_a (unaided, 1.4.0_DS) | Delta (aided - unaided) |
|--------|------------------------------|---------------------------------|------------------------|
| Wall-clock to first correct (sec) | 195 | 105 | +90 (aided slower) |
| Tokens to first correct | 15200 | 4400 | +10800 |
| Files touched before decisive | 4 distinct | 3 distinct | +1 |
| Irrelevant files touched | 5 events | 5 events | 0 |
| comp_calls | 7 | 0 | +7 (expected) |
| decisive_file_found | true | true | — |

Noise flag raised: token ratio 3.45x (aided/unaided) exceeds the >3x threshold. Root cause traced to aided agent's H1 incorrect hypothesis (ClassDocumenter) before compiler graph redirected to typehints.py. Both agents converged on identical fixes, so this is exploration variance not a validity concern.

Wall-clock direction note: aided was slower by 90s. Unaided navigated linearly (test -> fixture -> __init__ -> typehints.py, correct hypothesis at entry 5). Aided took H1 detour, ran comp-build import trace, was directed to typehints.py via event-hook graph edge (compiler_assisted=true at that open).

Confounding check: unaided prior sphinx exposure unknown but no explicit evidence; flagged as open confound per PRD §3.6. Not invalidating.

### 5. Artifacts written and pushed

Phase 2 metric-audit JSON and integrity_audit.md committed at `767f6c95`. TO status flipped to complete at `a106f71d`. Session log committed at `9346d252` (this session adds `9346d252` -> update pending below). All pushed to CLOUD remote.

---

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Both patches identical — score each condition independently on its own test output | Identical patches do not invalidate the measurement; each condition's nav_log and AC run are independent evidence. Convergence on the same fix is a finding, not a scoring conflict. |
| token_ratio 3.45x flagged as noise but run not invalidated | Flag threshold is for flagging + narrative, not automatic re-run. The driver (H1 detour) is identified and explainable; both agents solved the task correctly. |
| Unaided prior sphinx exposure listed as open confound, not disqualifying | No evidence of prior exposure in nav_log; 1.4.0_DS's prior TOs (.042 comp-preflight) are not sphinx-specific. PRD §3.6 asks to flag, not automatically invalidate. |
| Comparability class: cross-DS | All non-DS manifest fields match between conditions. Harness exposure difference is the experimental variable, not a class-downgrade trigger. |

---

## Files Modified

| File | Change | Committed |
|------|--------|-----------|
| `comp/results/wave-3a/verdicts/case-003-ds-1.3.0-condition_b-run-1.json` | Phase 1 verdict: PASS, condition_b | Yes — `4e1ec449` |
| `comp/results/wave-3a/verdicts/case-003-ds-1.4.0-condition_a-run-1.json` | Phase 1 verdict: PASS, condition_a | Yes — `4e1ec449` |
| `comp/results/wave-3a/metric_audit/case-003-efficiency-delta.json` | Phase 2 metric audit + deltas + noise flags | Yes — `767f6c95` |
| `comp/results/wave-3a/integrity_audit.md` | Phase 1->2 ordering + reasoning.md exclusion + nav_log hygiene + cross-contamination check | Yes — `767f6c95` |
| `org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.051.case3-two-phase-scoring.md` | Status: staged -> pending -> complete | Yes — `a106f71d` |
| `org/tier2_senior/2.1.0_SC_CompLearns/logs/2026-04-24/session_02_case3_two_phase_scoring.md` | This session log | Yes — `9346d252` (initial) + update |

---

## Blockers

None. TO queue exhausted (.029-.032 all complete from prior sessions; .051 now complete). Waiting for COO dispatch of .053 (joint review) or any new SC-scoped TO.

---

## Current State

COMP_LEARNS.051 complete and pushed to CLOUD at `a106f71d`. Wave 3a artifacts are at `comp/results/wave-3a/` in feature_clb: two PASS verdicts, metric-audit JSON showing aided agent was slower (+90s wall-clock, 3.45x more tokens) on this cross-module failure diagnosis task, and integrity_audit confirming clean Phase 1->2 ordering and zero context contamination. MCP COMPLETE delivered to 2.1.0_SA_COO with verdict summary, efficiency delta, and noise flags. All four SC task orders (.029-.032, .051) are now complete. Lane A (.048) remains on CTO REDLINE hold — not SC scope until CTO re-scopes and COO re-dispatches.

---

## Next Steps

1. **[2.1.0_SA_COO] Dispatch .053 joint review GO** — .051 ship is one of the two gates (.048 dev-4 output is the other; currently on REDLINE hold). COO determines whether to proceed with partial evidence or wait for .048 resolution.
2. **[Self] Execute .053 on GO** — joint review of wave-3a verdict + metric-audit; produce scoring sufficiency assessment per PRD §3.7 directional-evidence claim scope.
3. **[Self] On any new SC dispatch** — check inbox on watcher exit, RAVC ACK, execute immediately.
