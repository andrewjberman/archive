# Task Order: NFRA_MOTIF P2 -- C3 system emergence (compose motifs -> discovered architecture)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-motif-p2</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~Z (REDIRECTED 2026-07-14 from 0.4.0_DS~B [consumed by AoR lane] per SOVEREIGN REDIRECT @ 14c2aeeba + AMENDMENT-1 @ 552667ccd; BUILD ON the pre-staged C3-emergence core @ cd022f539, do not re-derive. Prior chain: DS~A down -> DS~B re-allocated 2026-07-08)</issued_to>
    <date>2026-07-07</date>
    <status>dispatched -- GO'd 2026-07-08 by COO~B to 0.4.0_DS~B. Both gates CLEARED: MOTIF-P1 C2 catalog CVO-certed (b783dd504) + MOTIF-P0 MET (91 CLUSTERS edges + 91 PanelCluster nodes + 241 CONTAINS_DRILLDOWN + 55 SHARES_SOURCE live at the fresh canonical HEAD, snapshot 20260708, via the FRESHGUARD derive un-freeze). CAVEAT: comp-kuzu canonical-DB rebuild to the new HEAD is FAILING (rc=143 Arrow-S3, serving stale pre-derive DB, BEHIND-flagged) -> QUERY THE AUTHORITATIVE snapshot 20260708 (not comp-kuzu) until the rebuild is fixed (tracked finding).</status>
    <gate_note>Gated on MOTIF-P1 (the C2 motif catalog). comp-ladder fidelity gate binds every C3 node.</gate_note>
  </metadata>

  <objective>Compose connected C2 motifs into C3 systems -- emergent (discovered from motif connectivity, NOT declared) + decomposable. Deliver the "discovered architecture" view: business capabilities the org never diagrammed (code: authentication = auth-middleware + protected-route + session motifs; org: release-management = approval + directive + verification motifs).</objective>

  <requirements>
    <requirement id="1">EMERGENCE (AC4): at least one C3 system DISCOVERED from connected motifs (not declared in advance) -- proving architecture-discovery.</requirement>
    <requirement id="2">DECOMPRESSION (AC2): every C3 system decomposes to its constituent motifs -> C1 -> C0 -> lexical evidence. No node without an intact chain.</requirement>
    <requirement id="3">STRUCTURAL only (AC1): systems emerge from graph connectivity + community detection, NEVER embedding-similarity.</requirement>
    <requirement id="4">FIDELITY GATE (AC6): every C3 system PASSES comp-ladder fidelity_check (reference org/modules/graph/comp_ladder.py; a non-decompressible node fails the build).</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_MOTIF.P1: the C2 motif catalog this composes. HARD PREREQUISITE.
    - GRAPHDEPTH CONTAINS-rollup engine (complete): reuse for the C2->C3 compression (don't build new).
    - NFRA_MOTIF.P3: consumes the emergent systems as promotion candidates.
    - comp-ladder (org/modules/graph/comp_ladder.py): the shared fidelity gate -- reference, do not rebuild.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. >=1 discovered (not declared) C3 system exists; it PASSES comp-ladder fidelity_check and decompresses to lexical evidence.
    2. Detection is structural (community detection over C1/C2), grep-proof no embedding-similarity.
    3. Ground on the live canonical graph (Rule 22). RAVC COO~B + CC CTO; CVO verifies emergence-is-real (a genuinely-undiagrammed system) + decompression holds.
  </acceptance_criteria>
</task_order>
```
