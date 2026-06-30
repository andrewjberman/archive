<to_id>NFRA_TSGRAPH.P2-3</to_id>
<project>NFRA_TSGRAPH</project>
<title>P2-3 -- comp-cluster CLI (panel->drilldown tree + per-node data-sources + cross-panel coupling) + graph-call-manifest.yaml entry</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>DT lane for the graph-call-manifest.yaml registration (canonical comp-* entry)</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; 2b61ac87e)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<!-- GO 2026-06-30T2313Z (COO~B): gate met (P2-2 materialized+verified live; P2-1 ACCEPTED 6/6 ACs); CTO inv-2 edge ruling landed (22cb21116) -> canonical CONTAINS+depth / CLUSTERS / SHARES_SOURCE. staged->pending. Execute. RAVC2 COO~B cc CTO. -->
<!-- BUILT+VERIFIED, LANDING HELD (Andrew->MSTR fold-in) 2026-06-30T2346Z (0.4.0_DE): comp-cluster built + ALL ACs verified locally (comp-cluster AdvisorIntelligence = real PAGE->PANEL->DRILLDOWN tree depth 1..4 + per-firm cohort fork; comp-manifest-check exit 0; comp_coverage_view --verify 35/35; comp-which routing 34/35 (lone fail comp-drift PRE-EXISTING); coverage 118/119 + 1 visible unresolved, 0 silent). LANDING is lane-blocked for a DE: comp_cluster_cli.py -> infra/aws/globgrph (AE lane), graph-call-manifest.yaml entry -> ANY_EXEC lane, .tools/comp-cluster -> .gitignore negation needed. Andrew steered the approach to 0.0.0_AB_MSTR for fold-in into a more-developed approach (brief: docs/briefs/comp-cluster-graph-manifest-approach-brief-20260630.md; durable bundle + landing recipe in scratchpad p2-3-comp-cluster-bundle/). Status held pending: built+verified but NOT landed (awaiting MSTR fold-in decision on engine-home/landing). Shared-tree edits reverted (preserved in bundle patch); new engine+wrapper remain on-disk (comp-cluster runs). -->
<priority>MEDIUM -- GATED on P2-2 (the CLI queries the materialized cluster graph). Generalizes comp-cache collisions.</priority>

<gate>P2-2 <status>complete</status> (cluster nodes/edges live on the canonical graph). COO GOes after P2-2 RAVC2.</gate>

<scope>
Build the `comp-cluster <page>` CLI: returns the panel->drilldown tree + per-node data-sources + cross-panel shared-source coupling edges, querying the materialized cluster graph (Rule 20: QUERY the live graph, never rebuild). Generalizes `comp-cache collisions` (component<->data-source coupling). Register a canonical entry in org/modules/graph/graph-call-manifest.yaml (the mandated catalog) so comp-which surfaces it.
</scope>

<compiler_tools_mandate>
  <phase id="3" when="after commit"><step><run>comp-manifest-check</run><expect>comp-cluster registered in graph-call-manifest.yaml, manifest gate PASS, comp-which resolves "cluster" questions to comp-cluster.</expect><if_mismatch>STOP. An unregistered tool fails the manifest gate -- the CLI must be in the catalog.</if_mismatch></step></phase>
</compiler_tools_mandate>

<cross_domain_coordination>Reads the cluster graph P2-2 materialized -- same schema contract as P2-1/P2-2. No firm-pipeline cross-ref.</cross_domain_coordination>

<acceptance_criteria>1. `comp-cluster AdvisorIntelligence` (richest page) returns the panel->drilldown tree matching real structure; drilldown nesting-depth + per-firm _partners cohort surfaced; cross-panel shared-source coupling edges shown. 2. Registered in graph-call-manifest.yaml (comp-manifest-check PASS). 3. Coverage 119/119 page-tree, 0 silent Unknown. 4. Session-log Compiler Tools reproduces each <run>. RAVC2 to COO (CC CTO).</acceptance_criteria>

<dependencies><dependency project="NFRA_TSGRAPH" task="P2-2" status="staged"/></dependencies>
<references><ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9</ref></references>
<lane_note>DE-primary (queries) + DT (manifest registration). Full mandate-triad finalizes at GO. COO GOes post-P2-2.</lane_note>
