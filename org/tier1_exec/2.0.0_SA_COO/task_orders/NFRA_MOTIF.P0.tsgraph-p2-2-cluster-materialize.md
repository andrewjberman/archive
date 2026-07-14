# Task Order: NFRA_MOTIF P0 -- FINISH TSGRAPH P2-2: materialize the comp-cluster clusters as live C2 edges on the canonical graph (the MOTIF accelerator)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO~B-2026-07-07-nfra-motif-p0</id>
    <issued_by>2.0.0_SA_COO~B</issued_by>
    <issued_to>0.8.0_AE_CloudComp~Z (globgrph derive -- REDIRECTED 2026-07-14 from 0.7.0_AE_CloudOps [buried: FRESHGUARD+OPAL_ASSETS] per SOVEREIGN REDIRECT @ 14c2aeeba + AMENDMENT-1 @ 552667ccd; CONSTRAINT TRAVELS: coordinate with 0.7.0 before touching the globgrph TF module -- ONE applier per module) + 0.4.0_DE_ClientPlatform (producer publish + live verify, gated on base-DE release -- UNCHANGED, DE publish stays DE-gated)</issued_to>
    <date>2026-07-07</date>
    <status>dispatched -- GO'd 2026-07-08 by COO~B to 0.7.0_AE (globgrph derive lane), QUEUED behind INFRPT recurring-schedule + GUARD-REFILE + AGENTBUS-S3. Unblocks MOTIF-P1's C2-in-graph leg. Primary path is 0.7.0_AE (locate/regenerate portal_clusters.json + run derive + verify cluster edges live via comp-cluster/comp-kuzu query -- no hard DE dependency); DE producer-publish only if the JSON is stale/missing (coordinate base COO for DE-base).</status>
    <prd_ref>docs/architecture/NFRA_MOTIF_PRD.md (P1 gate) + docs/architecture/NFRA_TSGRAPH_PRD.md (P2-2, re-homed to MOTIF)</prd_ref>
    <dispatch_state>STAGED -- the MOTIF accelerator, sequence FIRST within MOTIF. FINISH-AND-VERIFY, not a rebuild. Authored by COO~B on the NFRA full-program completion drive.</dispatch_state>
    <gate_note>Unblocks MOTIF-P1's C2-in-graph leg. RECORDS CONFLICT: a 07-02 record claims "materialized+verified"; the freshest 07-07 CVO grounding (SEMCTL synergy #3b) says the cluster edges are NOT live on the canonical graph. GROUND ON THE LIVE CANONICAL GRAPH, never the stale record (Rule 22). DE-verify leg holds until base COO releases 0.4.0_DE from its live client call.</gate_note>
  </metadata>

  <objective>Finish TSGRAPH P2-2 -- materialize the 91 extracted comp-cluster clusters (15 pages) as live C2 cluster nodes/edges on the canonical Kuzu/Nessie graph. The derive plumbing already EXISTS (infra/aws/globgrph/derive_runner.py::ingest_cluster_producer, L1240-1290, invoked at L1696; folds Page/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN/SHARES_SOURCE edges into the Iceberg commit, with the CVO COND-A layer='portal' relabel) but is best-effort/skip-if-absent. Finish = publish the producer JSON, run the derive with it present, and DE-verify the edges are LIVE on the canonical graph.</objective>

  <requirements>
    <requirement id="1">Publish `producers/ts-semantic/portal_clusters.json` (the DE P2-1 producer) to S3 so `ingest_cluster_producer` no longer WARNs+SKIPs.</requirement>
    <requirement id="2">Run the globgrph derive with the producer present -> Page/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN/SHARES_SOURCE edges land in the Iceberg commit (layer='portal', CVO COND-A relabel applied).</requirement>
    <requirement id="3">DE RE-VERIFY LIVE (the binding gate): `comp-cluster` (or comp-kuzu) query confirms the 91 clusters are MATERIALIZED C2 edges on the CANONICAL graph -- not merely extract-complete. Report the live edge count vs the 91 extracted.</requirement>
  </requirements>

  <cross_domain_coordination>
    - NFRA_MOTIF.P1 (0.4.0_DS~A): blocked on this TO for its C2-in-graph leg (can consume the comp-cluster CLI extraction in the meantime).
    - infra/aws/globgrph/derive_runner.py (0.7.0_AE_CloudOps lane): the derive that materializes; the plumbing exists.
    - 3.0.0_SA_CVO: the freshest grounding said NOT-live -- CVO re-confirms on the live canonical graph post-derive.
  </cross_domain_coordination>

  <acceptance_criteria>
    1. `comp-cluster` / comp-kuzu query shows the clusters as MATERIALIZED C2 edges on the canonical graph (live edge count reported; ~91), not extract-only.
    2. DE-verified LIVE (exercise, not the stale record); ground on the canonical graph state (Rule 22).
    3. RAVC COO~B + CC CTO + CVO. On live-confirm -> MOTIF-P1's C2-in-graph leg unblocks.
  </acceptance_criteria>
</task_order>
```
