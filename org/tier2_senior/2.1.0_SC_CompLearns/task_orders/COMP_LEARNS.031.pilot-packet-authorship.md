# COMP_LEARNS.031 — Pilot Packet Authorship (Cases 1 + 2)

**TO serial:** COMP_LEARNS.031  
**Author:** 2.1.0_SC_CompLearns  
**Date:** 2026-04-21  
**Dispatched by:** 2.0.0_SA_COO  
**Status:** complete  
**Scope:** Task packet authorship for PARALLELIZATION_V1 pilot wave (.032). No code changes. No deployment.

---

## Objective

Author two task packets for the .032 pilot scoring wave:
- **Case 1**: structural_bug_localization, httpx, 1.1.0_DS_CompLearns
- **Case 2**: regression_safe_refactor, click, 1.3.0_DS_CompLearns

Both packets must use real pinned baseline_commit SHAs, pass YAML parse-check, and receive CTO sign-off before pilot dispatch.

---

## Deliverables

### D1 — Case 1 Task Packet (httpx)
**File:** `comp/tasks/task-001/packet.yaml`  
**Status:** COMPLETE  
**Archetype:** structural_bug_localization  
**Target:** httpx  
**baseline_commit:** `354c4cac1f1796ee4d8861a4c978807398852ad5` (immediately before PR #1298 fix, 2020-09-18)  
**Bug:** NetRCInfo.get_credentials() passes full authority (host:port) to netrc.authenticators() instead of host-only. Silent failure for non-standard-port requests.  
**File:line:** `httpx/_utils.py:150-156` (NetRCInfo.get_credentials method)  
**Acceptance criteria:** ac-1 existing netrc tests pass; ac-2 new non-standard-port test added by DS passes; ac-3 full auth test suite regression-clean  
**YAML parse:** PASS

### D2 — Case 2 Task Packet (click)
**File:** `comp/tasks/task-002/packet.yaml`  
**Status:** COMPLETE  
**Archetype:** regression_safe_refactor  
**Target:** click  
**baseline_commit:** `934813e4d421071a1b3db3973c02fe2721359a6e` (click 8.1.8 tag)  
**Refactor scope:** `click/core.py` Group.invoke() and Group.parse_args() methods only  
**Invariants:** 8 named (I-1 through I-8), sourced from bl-click-001.yaml failure modes  
**Acceptance criteria:** ac-1 invariant fixture; ac-2 full test suite; ac-3 scope rubric  
**YAML parse:** PASS

### D3 — Invariant Fixture (Case 2)
**File:** `comp/tasks/task-002/fixtures/invariant_check.py`  
**Status:** COMPLETE  
**Description:** 8 pytest test functions (test_I1_* through test_I8_*), one per invariant. Read-only — DS must not modify. Tests are self-contained and import click from the refactored working tree.

---

## Acceptance criteria

- [x] D1 packet.yaml — real baseline_commit, bug selection reasoning documented, YAML parse-clean
- [x] D2 packet.yaml — real baseline_commit (click 8.1.8), 8 invariants named in packet + fixture, YAML parse-clean
- [x] D3 invariant_check.py — 8 test functions, each labeled I-1 through I-8, DO NOT MODIFY header
- [ ] CTO sign-off on D1 + D2 + D3
- [ ] Committed and pushed to CLOUD
- [ ] COO notified GREEN/COMPLETE

---

## Bug selection reasoning (Case 1 summary)

Selected httpx PR #1298 (NetRC host vs authority). Rationale:

1. **Cross-module span**: symptom at `_client.py` call site, root cause in `_utils.py`. Classic structural localization challenge.
2. **Non-obvious**: `authority` parameter naming conceals the bug; standard-port requests work correctly, masking it under typical usage.
3. **Minimal fix, medium localization**: 1-2 line fix after finding the right call site.
4. **Verifiable**: existing `.netrc` fixture + new non-standard-port test gives deterministic pass/fail gate.
5. **Harness-relevant**: httpx is the live COMP_LEARNS scoring target — condition_b DS can use the selector graph to navigate to `_utils.py`.

baseline_commit `354c4cac` = master immediately before PR #1298 merge. Bug confirmed present at this commit by direct code inspection.

---

## Invariant selection reasoning (Case 2 summary)

Eight invariants sourced from 1.3.0_DS click pre-read (2026-04-21), cross-referenced with bl-click-001.yaml. Selected for Group.invoke()/Group.parse_args() refactor scope because:
- All 8 map to observable behavioral contracts that a careless refactor would break
- Each is independently testable via the CliRunner pattern
- Together they cover: dispatch routing (I-1), param ordering (I-2, I-7), context propagation (I-3), chain validation (I-4), return value semantics (I-5), callback chaining (I-6), command resolution (I-8)

---

## Dependencies

- **Requires:** COMP_LEARNS.030 GREEN (satisfied — eba6cb26)
- **Blocks:** COMP_LEARNS.032 pilot dispatch (COO, pending CTO ACK)
- **CTO gate:** MCP 1.1.0_SA_CTO with packet content summary before commit
