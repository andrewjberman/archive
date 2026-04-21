# COMP_LEARNS.030 — Schemas and Doctrine Extensions for PARALLELIZATION_V1

**TO serial:** COMP_LEARNS.030  
**Author:** 2.1.0_SC_CompLearns  
**Date:** 2026-04-21  
**Dispatched by:** 2.0.0_SA_COO  
**Status:** complete  
**Scope:** Schema authoring + doctrine documentation. No code changes. No deployment.

---

## Objective

Author the full schema, doctrine, and undocumented-surfaces documentation package required to launch PARALLELIZATION_V1 pilot wave (.032). This package is the pre-requisite for:
- Task packet authoring (COO)
- Scorer worktree provisioning (SC)
- DS intervention-runner dispatch (COO → DS agents)
- CTO schema sign-off

---

## Deliverables

### D1 — Task Packet Schema Scaffold
**File:** `comp/tasks/task-000-example/packet.yaml`  
**Status:** COMPLETE  
**Description:** Annotated reference packet showing all REQUIRED/OPTIONAL/LOCKED fields. Serves as the canonical schema anchor for all real packets at `comp/tasks/<packet_id>/packet.yaml`. Includes: identity fields, task definition, target pinning, harness exposure conditions (condition_a unaided + condition_b aided_full), acceptance_criteria, measurement_axes, budgets, scorer_regime, candidate_bundle spec, backlog_provenance, wave assignment.

### D2 — Scoring Context Manifest Schema
**File:** `comp/tasks/scoring-context-manifest-schema.yaml`  
**Status:** COMPLETE  
**Description:** 10-field comparability key manifest schema. Defines `manifest_hash` (SHA-256 of all comparability-relevant fields excluding `scored_at`). Includes full `comparability_class_definitions` block (locally_valid → within_task → cross_ds → cross_model downgrade ladder) and a fully populated `example_filled` section for task-001-httpx. CTO sign-off required before pilot dispatch.

### D3 — DS Role Addendum (Intervention-Runner Mode)
**File:** `docs/architecture/COMP_LEARNS_DS_ROLE_ADDENDUM.md`  
**Status:** COMPLETE  
**Description:** Mode-switch doctrine for DS agents transitioning from Phase 0-3 implementer mode to PARALLELIZATION_V1 intervention-runner mode. Covers: trigger conditions for each mode, input constraints (§2a), artifact discipline (diff + test_output.txt + reasoning.md, §2b), scope discipline (§2c), no-deploy-cycle rule (§2d), context isolation discipline per §4.13 (§2e), handoff protocol (MCP COO not scorer, §4), harness conditions operational definition (§5), pilot wave constraints (§6: 1.1.0_DS Case 1 / 1.3.0_DS Case 2).

### D4 — Undocumented Load-Bearing Surfaces
**File:** `docs/architecture/COMP_LEARNS_UNDOCUMENTED_SURFACES.md`  
**Status:** COMPLETE  
**Description:** Authoritative record of 3 surfaces discovered during Phase 3 close certification (COMP_LEARNS.029 §12). Each surface has: actual behavior, documented claim (if incorrect), exact file:line proof, operational consequence, resolution status. Surfaces: (1) ABCache double-nesting `ab_cache/ab_cache/` (cache.py:101-103 + ratchet.py:615-616), (2) Cache not git-tracked (filesystem-confirmed), (3) Scorecard.__eq__ excludes judge_model_id/judge_mode (scorecard.py:157-168). Activation timeline. Track 2 micro-TO scope.

---

## Acceptance criteria

- [x] All 4 deliverable files written and readable
- [x] D1 packet.yaml contains all REQUIRED fields per PARALLELIZATION_V1.md §3
- [x] D2 manifest schema matches 10-field comparability key per PARALLELIZATION_V1.md §4
- [x] D3 covers both modes, all artifact constraints, and pilot wave assignments
- [x] D4 covers all 3 surfaces found in §12 of scorer_stability_baseline.md with file:line proof
- [ ] CTO sign-off on D1 + D2 (required before pilot dispatch)
- [ ] Committed to CLOUD under `--author="2.1.0_SC_CompLearns <2.1.0_SC_CompLearns@opal.agent>"`
- [ ] Pushed to remote
- [ ] COO notified GREEN/COMPLETE with commit sha

---

## Dependencies and blockers

- **Requires:** COMP_LEARNS.029 COMPLETE (satisfied — phase_3_certification.md, YELLOW verdict)
- **Blocks:** COMP_LEARNS.031 packet authoring (COO), .032 pilot dispatch
- **Track 2 dependency:** Docstring fixes (ab.py, cache.py ABCache constructor, scorecard.py __eq__) routed to COO → micro-TO → 1.2.0_DS_CompLearns. Must ship before .030 packet tooling begins.

---

## Notes

COO dispatch (GO message): "scope is: schemas (packet.yaml scaffold + scoring-context-manifest-schema.yaml), DS role addendum, undocumented surfaces doc. TO path: org/tier2_senior/2.1.0_SC_CompLearns/task_orders/COMP_LEARNS.030.schemas-and-doctrine-ext.md (author this yourself per your role; I am providing scope here). MCP CTO for sign-off on schema files before commit. MCP me GREEN/COMPLETE when CTO accepts + commit sha."

CTO sign-off gate: D1 + D2 must be reviewed by 1.1.0_SA_CTO before any .032 pilot packets reference these schemas as authoritative.
