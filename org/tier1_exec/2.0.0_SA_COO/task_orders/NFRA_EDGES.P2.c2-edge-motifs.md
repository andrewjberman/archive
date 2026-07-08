# Task Order: NFRA_EDGES P2 -- C2 EDGE-MOTIFS (the D1-D7 detectors emit the edge configuration, not just the sink node)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-edges-p2-edge-motifs</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B (graph-lane) | CTO arch-gate (AC4/AC5) + CVO cert (fidelity + collision-safe + freshness + recurrence)</issued_to>
    <date>2026-07-08</date>
    <status>staged -- GO after P1 (the *Edge reification mechanism proven). Gated on P1.</status>
    <prd_ref>docs/architecture/NFRA_EDGES_PRD.md (SS3-P2, SS4 AC3/AC4/AC5, SS5 Q4-recurrence)</prd_ref>
    <gate_note>The D1-D7 motifs ARE edge-patterns (D1 = ">=2 guarded FLOWS_TO into one sink") -- but today they materialize only the sink NODE. P2 emits the EDGE CONFIGURATION (the guarded-fork subgraph) as a first-class edge-motif.</gate_note>
  </metadata>

  <objective>Extend the D1-D7 detectors to emit the recurring EDGE CONFIGURATION as a first-class C2 EDGE-MOTIF (the guarded-fork subgraph over the P1-reified *Edge nodes), not just its sink node. Recurrence + fidelity apply unchanged.</objective>

  <requirements>
    <requirement id="1">EDGE-MOTIF EMISSION: each D1-D7 detector emits the edge-motif (the canonical edge-SET forming the guarded-fork/recurring configuration) as a C2 node over the P1 *Edge C1 nodes -- carrying the configuration, not just the sink. Reuse the existing recurrence + fidelity machinery (no new gate).</requirement>
    <requirement id="2" priority="RECURRENCE (PRD Q4)">recurrence bar STARTS at AC3's >=2, TUNABLE in P2: an edge-configuration is a higher-order pattern, so MEASURE whether edge-config recurrence is sparser/noisier than node-motif recurrence -- if so, tune the bar (don't pre-optimize). Report the measured edge-motif recurrence distribution.</requirement>
    <requirement id="3" priority="LOAD-BEARING -- AC4 COLLISION-SAFE IDS (gates THIS phase)">every edge-motif node_id is UNIQUE-BY-CONSTRUCTION: `edge-motif <- stable-hash(its canonical edge-set)`, NEVER a reused label. SELF-TEST (gates the phase): two DISTINCT edge-motifs sharing a label yield DISTINCT node_ids. Inherits f875bc854 -- non-negotiable (the silent-MERGE-corruption guard).</requirement>
    <requirement id="4" priority="LOAD-BEARING -- AC5 FRESHNESS CONTRACT">every materialized edge-motif conforms to CloudNode/CloudEdge + carries snapshot_ts -> covered by the incremental-refresh + reconcile-oracle. Bind from day one.</requirement>
    <requirement id="5">AC3 (coverage-sweep): the reified edge-motifs EXERCISE the coverage-sweep's Relationship + EdgeKind families (no new gap; the sweep already gates them -- confirm green).</requirement>
  </requirements>

  <acceptance_criteria>
    1. D1-D7 emit first-class edge-motifs (the guarded-fork subgraph), recurrence + fidelity green; the measured edge-config recurrence distribution reported (bar tuned if warranted).
    2. AC4 self-test PASSES (distinct edge-motifs -> distinct ids); AC5 conformance; AC3 coverage-sweep green. CTO arch-gate + CVO cert. RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
