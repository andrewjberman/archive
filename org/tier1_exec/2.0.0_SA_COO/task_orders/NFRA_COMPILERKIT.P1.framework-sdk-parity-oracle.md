# Task Order: NFRA_COMPILERKIT P1 -- shared Recognizer-SDK framework + refactor the 2 existing compilers (parity-oracle pair)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-compilerkit-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.8.0_AE_CloudComp~D (framework) + 0.4.0_DS_ClientPlatform~A (recognizers)</issued_to>
    <date>2026-07-07</date>
    <status>complete -- SPRING-CLEAN 2026-08-25: project NFRA_COMPILERKIT is complete; this TO was last touched 2026-07-07, predating the project close 2026-07-07. Closed as a record act, not a work verdict. Prior status: active</status>
    <prd_ref>docs/architecture/NFRA_COMPILERKIT_PRD.md (P1)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>Refactor the 2 EXISTING production compilers (comp-tools code #1 + TSGRAPH-TSX #2) onto ONE shared Recognizer-SDK (parity-oracle pair). WIRING-not-build: comp_ladder.py is the proto-SDK, cse_schema.py is the IR. CTO #3: PURE-LEXICAL provenance only; live-AWS recognizers re-home to FEDOBS.</objective>

  <requirements>
    <requirement id="1">SDK skeleton (comp_recognizer_sdk.py) CTO-arch-gate-approved + 11/11 self-test [DONE]</requirement>
    <requirement id="2">the 2 lexical compilers reconciled as a parity-oracle pair (reproduce the current graph)</requirement>
    <requirement id="3">every recognizer C0/C1 PASSES comp-ladder fidelity_check</requirement>
    <requirement id="4">PROMOTE_SEAM surfaced as a named critical-surface (hot-registration)</requirement>
    <requirement id="5">recognizers building (DS~A batch-1: DispatchCatalog + Mdpf, converges DEBTSCAN root-fix)</requirement>
  </requirements>
</task_order>
```
