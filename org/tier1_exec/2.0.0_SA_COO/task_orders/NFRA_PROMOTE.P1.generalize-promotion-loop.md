# Task Order: NFRA_PROMOTE P1 -- generalize TH-C clause-A + COMPLEARN loop into the directive/write-back plane (LAST)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-promote-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>1.0.0_SA_CTO (ratify) + AE/DS (materializers)</issued_to>
    <date>2026-07-07</date>
    <status>forming</status>
    <prd_ref>docs/architecture/NFRA_PROMOTE_PRD.md</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>Generalize NFRA_TOOLHEALTH TH-C CLAUSE-A (CVO-certed dispatch) + the COMPLEARN-activation charter as the reference loop. Ground on the EXERCISED clause-A, NOT the pending TH-C EFFECTIVE axis. LAST plane (only write-back). DISPATCH PENDING -- detailed decomposition in flight.</objective>

  <requirements>
    <requirement id="1">the 5 promotion invariants are the gate</requirement>
    <requirement id="2">generalize clause-A + COMPLEARN charter (PROMOTE-P0)</requirement>
    <requirement id="3">4 reversible materializers</requirement>
    <requirement id="4">hot-registration seam (materializer side) pairs with COMPILERKIT registry side</requirement>
    <requirement id="5">gated behind observe/measure/validate arms</requirement>
  </requirements>
</task_order>
```
