# Task Order: NFRA_EDGES P1 -- EDGE REIFICATION in the MOTIF ladder (lift FLOWS_TO/RENDERS into C1 *Edge nodes)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-08-nfra-edges-p1-reify</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~B (SEMCTL lane, drafted the brief -- P1 owner) | CTO arch-gate (AC4/AC5 hard) + CVO cert (fidelity + collision-safe + freshness)</issued_to>
    <date>2026-07-08</date>
    <status>complete -- CLOSED 2026-08-05 ~2350Z (2.0.0_SA_COO). Phase closed 2026-07-09, both gates MET, commit 262053a3d cited in org/projects/NFRA_EDGES.json. Surfaced as a stale-open row by 0.4.0_DS_ClientPlatform's backlog triage (addressed to the then-non-live ~B lane); dispositioned by 0.0.0_AB_MSTR grounded on the project record before closing.</status>
    <prd_ref>docs/architecture/NFRA_EDGES_PRD.md (SS2 reify-into-existing-Node, SS3-P1, SS4 AC1/AC4/AC5, SS5 Q1-hybrid)</prd_ref>
    <gate_note>THE GAP (CVO-confirmed grounded-EXACT, a COMPLETENESS gap not a correctness bug): the frontend MOTIF pipeline FLATTENS the defining FLOWS_TO/RENDERS edges into rule-TEXT -> a C3 materializes as a node-SKELETON, not the SUBGRAPH it is. The algebra + the reference comp_ladder ALREADY reify edges co-equally; this brings the frontend MOTIF pipeline to the same bar. NO new store, NO new fidelity gate -- reify into the EXISTING comp_ladder.Node model.</gate_note>
  </metadata>

  <objective>Reify the motif-defining FLOWS_TO/RENDERS edges into first-class C1 *Edge Nodes (reusing comp_ladder.Node): children = {src node, sink node, a C0 flow-fact carrying EdgeKind + guard condition}. Prove on firm-conditional-display: it decompresses to BOTH node AND edge constituents, each bottoming out in C0 evidence, fidelity_check green.</objective>

  <requirements>
    <requirement id="1">REIFY *Edge C1 NODES: for each motif-defining edge (D1's guarded FLOWS_TO, RENDERS), create a reified `FlowsToEdge`/`RendersEdge` Node via comp_ladder.Node -- children = {src, sink, a C0 flow-fact (the source line of the relationship + its `condition`)}, carrying EdgeKind ({passthrough, rename, recompute_guarded}) + the guard condition. NO new node_type where avoidable (PRD Q2 -- fewer collision surfaces); the edge-node reuses the Node model.</requirement>
    <requirement id="2">FIDELITY (AC1): the reified edge-node decompresses to its C0 flow-fact + passes fidelity_check IDENTICALLY to a node (a LATENT edge-node FAILS fidelity, same as a latent node). Prove firm-conditional-display decompresses to BOTH its node constituents AND its FLOWS_TO/RENDERS edge constituents, all grounded to C0.</requirement>
    <requirement id="3" priority="LOAD-BEARING -- AC4 COLLISION-SAFE IDS (MANDATORY, non-negotiable, gates THIS phase)">every reified *Edge node_id is UNIQUE-BY-CONSTRUCTION from its defining tuple: `FlowsToEdge <- stable-hash(src, sink, edge_type, condition)` -- NEVER a reused label. Inherits the C3 collision-safe discipline (f875bc854). SELF-TEST (gates the phase): two DISTINCT edges sharing a label yield DISTINCT node_ids. WITHOUT this, NFRA_EDGES reintroduces the EXACT silent store-side MERGE corruption f875bc854 just closed. CTO arch-gates this hardest.</requirement>
    <requirement id="4" priority="LOAD-BEARING -- AC5 FRESHNESS CONTRACT (bind from day one)">every materialized *Edge entity conforms to CloudNode/CloudEdge + carries the `snapshot_ts` producer-stamp, so the incremental-kuzu-refresh + reconcile-oracle drift-safety (CVO-certed this session) COVERS it. Bind now -- else born drift-blind.</requirement>
    <requirement id="5">REIFY HYBRID (PRD Q1): eager only where the subgraph earns its store cost (the intra-system edges of a materialized C3 -- P3); P1 proves the reification MECHANISM on firm-conditional-display (lazy/on-decompress is the default elsewhere). P1 = the mechanism + the proof, not a full eager sweep.</requirement>
  </requirements>

  <acceptance_criteria>
    1. firm-conditional-display decompresses to BOTH node AND reified-edge constituents, each bottoming out in C0; fidelity_check green on the edge-nodes (a latent edge-node fails).
    2. AC4 self-test PASSES (distinct-label edges -> distinct node_ids, unique-by-construction hash). AC5: edge-entities carry snapshot_ts + CloudNode/CloudEdge-conform.
    3. NO new store/fidelity-gate (reified into the existing Node model). CTO arch-gate (AC4/AC5 hard) + CVO cert (fidelity + collision-safe + freshness-conformance). RAVC COO~B.
  </acceptance_criteria>
</task_order>
```
