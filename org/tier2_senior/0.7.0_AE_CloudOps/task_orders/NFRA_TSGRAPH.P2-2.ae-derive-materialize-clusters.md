<to_id>NFRA_TSGRAPH.P2-2</to_id>
<project>NFRA_TSGRAPH</project>
<title>P2-2 -- materialize cluster nodes/edges into the canonical Nessie graph via the derive runner (atomic-ledgered, P4 precedent)</title>
<assigned_to>0.7.0_AE_CloudOps</assigned_to>
<consult>0.4.0_DE_ClientPlatform (P2-1 defines the Cluster/PanelCluster node + CLUSTERS/CONTAINS_DRILLDOWN/SHARES_SOURCE edge SCHEMA you materialize -- the shared interface)</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; 2b61ac87e)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<!-- GO 2026-06-18 (COO /drive): gate MET -- P2-1 schema delivered (DE fbf8549b1) + AE interface verified+aligned (AE broker status). SEQUENCE AFTER TO-D3 (it's a ledgered derive DEPLOY -- never-half-land; don't interleave with the scorer build). On materialize, DE's P2-1 close-verify fires (cluster edges on the live graph) -> P2-1+P2-2 close together. -->
<priority>HIGH -- gate MET (P2-1 schema delivered + AE-interface-aligned). Same atomic-ledgered / never-half-land derive deploy as P4. Sequence after TO-D3.</priority>

<gate>P2-1 <status>complete</status> AND the cluster node/edge schema agreed with DE (the additive CloudNode/CloudEdge string discriminators). COO GOes after P2-1 RAVC2 + schema-confirm.</gate>

<scope>
Materialize P2-1's Cluster/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN + cross-panel SHARES_SOURCE edges into the canonical Nessie graph via the globgrph derive runner. ADDITIVE, no schema break (string discriminators, same pattern as P4 props/SERVED_FROM). Run the FULL atomic-ledgered / never-half-land deploy discipline (P4 precedent): deploy-completion ledger OPEN at start -> commit -> safe-apply (if any IAM/TF) -> re-zip+rebuild derive image if code changed (CodeBuild builds from S3 ZIP not git -- prove in-container sha == committed, do not trust resolvedSourceVersion=null) -> re-derive -> comp-kuzu verify the cluster nodes/edges live on the canonical graph (HEAD current) -> RAVC2 -> CLOSE ledger in-session.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step><run>comp-iam service derive-runner (if the materialization adds any boto3/S3 -- EXPECTED NONE, same Nessie tables)</run><expect>No new IAM needed (additive to the same graph_nodes/graph_edges Iceberg tables).</expect><if_mismatch>If a new permission IS needed, comp-iam gaps + route the grant through the CTO+COO never-widen sign-off (P4 precedent) BEFORE apply.</if_mismatch></step>
  </phase>
  <phase id="3" when="after commit">
    <step><run>comp-kuzu "MATCH (c:PanelCluster) RETURN count(c)" + cluster edge count on the LIVE canonical graph (HEAD current)</run><expect>Cluster nodes/edges present on the canonical Nessie->Kuzu graph, vintage current; counts match P2-1's emit.</expect><if_mismatch>STOP. A no-op materialization (0 cluster nodes live) is a silent failure -- the ledger must NOT close until the live graph carries the clusters.</if_mismatch></step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>Same globgrph derive runner + Nessie/Iceberg tables as P4 + the nightly derive. Coordinate the deploy window so it does NOT race the 02:00Z nightly (P4 nightly-safety precedent). Deploy-completion ledger in org/critical_paths/change_management/ -- COO tracks ledger-close (no stranded leg).</cross_domain_coordination>

<acceptance_criteria>1. Cluster nodes/edges live on the canonical Nessie->Kuzu graph (comp-kuzu MATCH, HEAD current), counts == P2-1 emit. 2. Additive schema, no break to existing CloudNode/CloudEdge. 3. Atomic-ledgered deploy: ledger opened-at-start + CLOSED in-session, 0 stranded leg. 4. Session-log Compiler Tools section reproduces each <run>. RAVC2 to COO (CC CTO).</acceptance_criteria>

<dependencies><dependency project="NFRA_TSGRAPH" task="P2-1" status="staged"/></dependencies>
<references><ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9</ref></references>
<lane_note>AE derive-materialization lane (P4 precedent). Full mandate-triad finalizes at GO (the exact schema is P2-1's output). COO GOes post-P2-1.</lane_note>
