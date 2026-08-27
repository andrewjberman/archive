# Task Order: NFRA_SEMCTL  -- Semantic Control Plane charter + decomposition-tracking umbrella + 2 governance cross-project TOs

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-semctl-charter</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO (charter) + 2.0.0_SA_COO (tracking)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_SEMCTL is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-18. Closed as a record act, not a work verdict. Prior status: active</status>
    <prd_ref>docs/architecture/NFRA_SEMCTL_PRD.md</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>The architecture charter (ratified) + the decomposition-tracking umbrella for the 5 components. comp-ladder fidelity-gate DONE. Sequence: CSE[done] -> FEDOBS[done] and COMPILERKIT[building] -> MOTIF -> PROMOTE(last).</objective>

  <requirements>
    <requirement id="1">comp-ladder fidelity-gate DONE (the shared acceptance instrument)</requirement>
    <requirement id="2">governance TO (a): unify GLDINV+PROMOTE+exercise-cert into one honesty/completion invariant-library</requirement>
    <requirement id="3">governance TO (b): the promoted-recognizer to live-compiler hot-registration seam</requirement>
    <requirement id="4">LAW-1 + LAW-2 are gating governance</requirement>
    <requirement id="5">every C1+ node binds comp-ladder fidelity_check</requirement>
  </requirements>
</task_order>
```
