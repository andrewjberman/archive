# Task Order: NFRA_FEDOBS P1 -- federate 5 shipped observers (two-observer x C1 join) + read-only-on-truth boundary + live-AWS applied-state observer

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-fedobs-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <prd_ref>docs/architecture/NFRA_FEDOBS_PRD.md (P1)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
    <closure_note>2026-07-07 ~1319Z, post-reboot restart session. All 3 core legs independently certed, none resting on self-report: AC1 two-observer x C1 join (CTO-accepted); AC2 read-only-on-truth boundary (CVO PASS 11:57Z, `org/tier1_exec/3.0.0_SA_CVO/logs/2026-07-07/cvo_NFRA_FEDOBS_P1_AC2_boundary_exercise-cert_PASS.md`); obs_findings Glue-binding + live join re-verify (CVO independent re-run PASS, commit `0c095d6a2`, `org/tier1_exec/3.0.0_SA_CVO/logs/2026-07-07/cvo_NFRA_FEDOBS_P1_join-reverify_exercise-cert_PASS_FULLY-DONE.md`). Requirement 4 (live-AWS applied-state / desired-vs-applied drift-join, the "6th observer") is an explicit FOLLOW-ON, not a P1 blocker -- tracked as NFRA_FEDOBS Phase-B. Requirement 5 (comp-ladder fidelity bind) satisfied via the shared comp_ladder.py fidelity gate already binding every SEMCTL C-node.</closure_note>
  </metadata>

  <objective>Federate the 5 SHIPPED observers (COMPDRIFT/COMPDIFF/PIPESCRIPT/DEBTSCAN/GRAPHS-D8) via Trino over the existing globgrph store; prove the two-observer x C1 horizontal correlation; read-only-on-truth boundary. + the 6th observer = live-AWS APPLIED-state to the desired-vs-applied drift-join (Rule-22a as a plane primitive, CTO #3). FEDERATE-not-build. Houses the re-homed TOOLHEALTH EFFECTIVE-axis.</objective>

  <requirements>
    <requirement id="1">AC1 two-observer x C1 join proven live (CTO-accepted, 2408 findings) -- DONE</requirement>
    <requirement id="2">AC2 read-only-on-truth boundary CVO-certed (FedobsDenyWriteTruth, Deny-overrides-Allow physical, Rule-22a) -- DONE</requirement>
    <requirement id="3">obs_findings Glue binding to the live join (coordinated apply, in-flight) -- DONE, CVO join re-verify PASS</requirement>
    <requirement id="4">live-AWS applied-state observer + desired-vs-applied drift-join (follow-on) -- DEFERRED to Phase B, tracked separately</requirement>
    <requirement id="5">bind comp-ladder fidelity on any C-node -- DONE (shared gate)</requirement>
  </requirements>
</task_order>
```
