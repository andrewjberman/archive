# Task Order: NFRA_EDGES P3 -- C3 AS SUBGRAPH (materialize the intra-system edges, not just CONTAINS)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-edges-p3-c3-subgraph</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B (emergence/spec) + 0.7.0_AE_CloudOps (graph-materialize/ingest, mirror the C3-materialize) | CTO arch-gate (AC4/AC5) + CVO cert</issued_to>
    <date>2026-07-08</date>
    <status>staged -- GO after P2. COORDINATE the re-derive with the in-flight N>1 C3 collision-hardening (shared node_id scheme -- do NOT collide). Gated on P2 + that coordination.</status>
    <prd_ref>docs/architecture/NFRA_EDGES_PRD.md (SS3-P3, SS4 AC2/AC4/AC5, SS5 Q2-C3-property, SS8 Q2-coordination)</prd_ref>
    <gate_note>A C3 system is really a SUBGRAPH (member nodes + the FLOWS_TO/RENDERS edges among them) but today materializes only its node-skeleton + CONTAINS. P3 materializes the intra-system estate EDGES so the C3 carries its data-flow SIGNATURE = a real subgraph.</gate_note>
  </metadata>

  <objective>Materialize the intra-system FLOWS_TO/RENDERS estate edges (not just CONTAINS) so a C3 carries its data-flow signature (firm-literal -> guarded-fork -> display-sink), and extend the C3 emergence connectivity to use edge-overlap alongside node-overlap. The C3 becomes a real subgraph.</objective>

  <requirements>
    <requirement id="1" priority="AC2 -- the headline">the materialized graph for a C3 carries the intra-system FLOWS_TO/RENDERS edges (the SUBGRAPH), not only CONTAINS. Materialize via the in-VPC derive/ingest path -- MIRROR the proven C3-materialize pattern (governed, exercised, deliberate deploy, NEVER-half-land ledger). Intra-system EDGES are CloudEdges keyed on edge-identity (PRD Q2).</requirement>
    <requirement id="2" priority="Q2 -- data-flow signature">the C3's data-flow signature is a PROPERTY of the C3 NODE (NOT a new node_type -- fewer collision surfaces; the C3 node already has a collision-safe id). Do NOT introduce a new node_type for the signature.</requirement>
    <requirement id="3">EMERGENCE: extend the C3-emergence connectivity to use EDGE-overlap alongside node-overlap (a system's boundary is defined by its flow-edges, not only shared members).</requirement>
    <requirement id="4" priority="LOAD-BEARING -- AC4 COLLISION-SAFE IDS + COORDINATION">the collision-safe C3 node_id is (RE)COMPUTED AFTER final membership (node + edge overlap) settles -- unique-by-construction from the settled tuple. CRITICAL COORDINATION (PRD SS8 Q2): the in-flight N>1 C3 collision-hardening re-derive (DS~B f875bc854 + 0.7.0's re-derive) SHARES this unique-by-construction node_id scheme -- SEQUENCE so they do NOT collide on the scheme. Land the collision-hardening FIRST (it's in-flight, near-cert), THEN P3 extends it to the edge-settled membership. Self-test: distinct C3-subgraphs -> distinct ids.</requirement>
    <requirement id="5" priority="LOAD-BEARING -- AC5 FRESHNESS CONTRACT">every materialized C3-subgraph entity (nodes + intra-system CloudEdges) carries snapshot_ts + CloudNode/CloudEdge-conforms -> covered by incremental-refresh + reconcile-oracle. Bind from day one.</requirement>
  </requirements>

  <acceptance_criteria>
    1. AC2: a C3's materialized graph carries its intra-system FLOWS_TO/RENDERS edges (round-trip verified live, mirroring the C3-materialize cert); the data-flow signature is a C3-node property.
    2. AC4: node_id recomputed post-membership, unique-by-construction, coordinated (not colliding) with the in-flight collision-hardening; self-test passes. AC5 conformance. CTO arch-gate (AC4/AC5 hard, + the deploy discipline of the C3-materialize) + CVO cert. RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
