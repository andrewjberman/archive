# Task Order: NFRA_MOTIF P1 -- absorb TSGRAPH D1-D7 detector-library as first C2 motif catalog + reuse GRAPHDEPTH rollup

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-motif-p1</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A (graph-lane, resolved 2026-07-07 -- thematic fit with its live COMPILERKIT parity-oracle/graph work) + 0.4.0_DE_ClientPlatform (gated)</issued_to>
    <date>2026-07-07</date>
    <status>pending</status>
    <prd_ref>docs/architecture/NFRA_MOTIF_PRD.md (P1)</prd_ref>
    <backfill_note>TO FILE backfilled 2026-07-07 -- the SEMCTL plane was dispatched + built via MCP + arch-gate RAVC but the durable TO records were not materialized (Andrew/CTO caught the gap 2026-07-07). This TO reflects the REAL current state. Standing-fix adopted: TO-file + MCP-dispatch, both, every time.</backfill_note>
    <lane_allocation_note>Lane-allocation resolved 2026-07-07 13:51Z (COO /drive cycle 3) -- generic "0.4.0_DS (graph-lane)" resolved to DS~A specifically, since DS~B is committed to CSE-P2 and DS~A's COMPILERKIT recognizer work is graph-adjacent. DS~A should treat this as queued behind COMPILERKIT-P1/P2, not drop current work -- DE is only gated pending an initial sync, not full DS~A availability.</lane_allocation_note>
  </metadata>

  <objective>ABSORB the TSGRAPH D1-D7 detector-library (CVO-certed) as the first C2 motif catalog + reuse GRAPHDEPTH CONTAINS-rollup for C1-to-C2-to-C3 compression. VERTICAL. Lane-allocation resolved 2026-07-07 -- DS~A + DE, DE-side work may start now; DS~A syncs when it reaches a checkpoint in its current COMPILERKIT queue.</objective>

  <requirements>
    <requirement id="1">absorb D1-D7 as C2 catalog (each carries a lossless decompression path)</requirement>
    <requirement id="2">reuse GRAPHDEPTH CONTAINS-rollup (no new engine)</requirement>
    <requirement id="3">every C2/C3 node PASSES comp-ladder fidelity_check</requirement>
    <requirement id="4">C2-in-graph gated on TSGRAPH P2-2 (DE-Andrew-parked) -> consume comp-cluster CLI until P2-2</requirement>
    <requirement id="5">output = motifs + C3 systems as PROMOTE candidates</requirement>
  </requirements>
</task_order>
```
