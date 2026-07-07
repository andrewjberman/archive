# Task Order: NFRA_FEDOBS P1 -- federate 5 shipped observers (two-observer x C1 join) + read-only-on-truth boundary + live-AWS applied-state observer

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-fedobs-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.5.0_AE_OpalETL</issued_to>
    <date>2026-07-07</date>
    <status>active</status>
    <prd_ref>docs/architecture/NFRA_FEDOBS_PRD.md (P1)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>Federate the 5 SHIPPED observers (COMPDRIFT/COMPDIFF/PIPESCRIPT/DEBTSCAN/GRAPHS-D8) via Trino over the existing globgrph store; prove the two-observer x C1 horizontal correlation; read-only-on-truth boundary. + the 6th observer = live-AWS APPLIED-state to the desired-vs-applied drift-join (Rule-22a as a plane primitive, CTO #3). FEDERATE-not-build. Houses the re-homed TOOLHEALTH EFFECTIVE-axis.</objective>

  <requirements>
    <requirement id="1">AC1 two-observer x C1 join proven live (CTO-accepted, 2408 findings)</requirement>
    <requirement id="2">AC2 read-only-on-truth boundary CVO-certed (FedobsDenyWriteTruth, Deny-overrides-Allow physical, Rule-22a)</requirement>
    <requirement id="3">obs_findings Glue binding to the live join (coordinated apply, in-flight)</requirement>
    <requirement id="4">live-AWS applied-state observer + desired-vs-applied drift-join (follow-on)</requirement>
    <requirement id="5">bind comp-ladder fidelity on any C-node</requirement>
  </requirements>
</task_order>
```
