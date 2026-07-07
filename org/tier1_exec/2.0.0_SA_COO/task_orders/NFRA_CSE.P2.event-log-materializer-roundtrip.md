# Task Order: NFRA_CSE P2 -- C0 event log on store + C0-to-C1 materializer + AC4 structural round-trip + COMPUNIFY-wire

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cse-p2</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B (DS-items) + 0.5.0_AE_OpalETL (store-writer)</issued_to>
    <date>2026-07-07</date>
    <status>active</status>
    <prd_ref>docs/architecture/NFRA_CSE_PRD.md (P2)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
  </metadata>

  <objective>The C0 CSE event-log on the existing Iceberg/Nessie store (0.5.0 ingest-writer, no new store) + DS~B 2 items: AC4 STRUCTURAL round-trip (CSE-to-C1 reproduces the live CloudNode/CloudEdge graph) + COMPUNIFY-wire (add-a-primitive to live coverage-sweep).</objective>

  <requirements>
    <requirement id="1">AC4 structural re-materialize-diff reproduces the current graph</requirement>
    <requirement id="2">COMPUNIFY coverage-check wired to the version-bump path</requirement>
    <requirement id="3">C0 log rides the existing store, source+date partition, one-marker-commit for C0/C1 version-consistency</requirement>
    <requirement id="4">DS~B design RAVCd CTO 121122Z</requirement>
  </requirements>
</task_order>
```
