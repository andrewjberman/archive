# Task Order: NFRA_CSE P1 -- versioned semantic-algebra + CSE contract + fail-closed validator (the SEMCTL UNBLOCKER)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cse-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <completed>2026-07-07</completed>
    <completion_note>DONE + landed canonical (org/modules/graph/cse_schema.py) + CVO AC5+AC4 exercise-cert PASS (self-test 10/10 + 8/8 adversarials + AC4 vs live 52+52 0-unmapped). CTO arch-gate PASS. --live fail-loud hygiene-fix (f98d4ff77). COO SoD-landed canonical. FEDOBS and COMPILERKIT unblocked.</completion_note>
    <prd_ref>docs/architecture/NFRA_CSE_PRD.md + NFRA_CSE_algebra_schema_v0.1.md</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>Build the versioned semantic-algebra (4 primitive families) + CSE event contract (provenance mandatory) + fail-closed validator (LAW-1) + publish as the authoritative FEDOBS/COMPILERKIT interface. UNIFY-not-build (the C1 typed graph exists).</objective>

  <requirements>
    <requirement id="1">AC1 versioned algebra + migration governance</requirement>
    <requirement id="2">AC2 fail-closed validator</requirement>
    <requirement id="3">AC3 map CloudNode/CloudEdge types INTO the algebra (52+52 live)</requirement>
    <requirement id="4">AC4 published-contract emits/validates WITHOUT P2/P3</requirement>
    <requirement id="5">AC5 comp-ladder fidelity_check bind (non-decompressible = NOT DONE)</requirement>
    <requirement id="6">AC6 C0-log binds GLOBGRPH marker-HEAD + GRAPHUNI one-HEAD</requirement>
  </requirements>
</task_order>
```
