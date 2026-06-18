<to_id>NFRA_TSGRAPH.P2-1</to_id>
<project>NFRA_TSGRAPH</project>
<title>P2-1 -- page-rooted component-cluster extractor (PAGE->PANEL->DRILLDOWN) + community detection over the component<->data-source bipartite</title>
<assigned_to>0.4.0_DE_ClientPlatform</assigned_to>
<consult>0.7.0_AE_CloudOps (P2-2 materializes these nodes/edges into the canonical Nessie graph -- the additive node/edge schema is the shared interface; agree it BEFORE P2-2 derive-deploy)</consult>
<issued_by>2.0.0_SA_COO (CTO PRD section-9 handoff 151724Z; PRD docs/architecture/NFRA_TSGRAPH_PRD.md @ 2b61ac87e, Andrew-steered 2026-06-18)</issued_by>
<issued_date>2026-06-18</issued_date>
<status>pending</status>
<!-- GO 2026-06-18 (COO /drive cycle-1): DE 0.4.0 spawned LIVE (MSTR, pid 24732); P2-1 is the ready lead (rides live P1/P4 graph, HEAD-current). staged->pending. RAVC2 to COO (CC CTO). -->

<priority>HIGH -- Andrew-steered P2 (PAGE->PANEL->DRILLDOWN lens). Rides the LIVE P1/P4 graph (comp-kuzu HEAD-current, 12500n/19138e, pin==marker). Lead TO of P2; P2-2 + P2-3 gate on it.</priority>

<context>
P1 is cutover-signed (props live, 961 FLOWS_TO, parity-gate PASSED) and P4 cross-domain SERVED_FROM is live (29 both-ends under the real task-role). P2 extends the P1 ts-morph extractor to emit COMPONENT-CLUSTER structure under Andrew's PAGE->PANEL->DRILLDOWN lens. This is the lead P2 TO: it defines the cluster node/edge schema that P2-2 (AE) materializes and P2-3 (CLI) queries.
</context>

<scope>
Extend the P1 ts-morph extractor (org/modules/graph/tsgraph_spike/** = DE lane) to emit, page-rooted:
- L1 Page = route-root component (portal/src/pages feature-dir).
- L2 Panel cluster = RENDERS-descendant components grouped by shared data-source {gold artifact | served key | endpoint | React-Query key | shared hook | shared type} via COMMUNITY DETECTION within the page.
- L3 Drilldown = nested RENDERS under a panel (*Modal.tsx / *Detail.tsx / json-tiered) -- FIRST-CLASS, carrying nesting-depth + the per-firm `_partners/{firm}` cohort axis (where the mode/cohort-fork display bugs live).
Emit: Cluster / PanelCluster nodes + CLUSTERS / CONTAINS_DRILLDOWN membership edges + cross-panel SHARES_SOURCE edges. ADDITIVE schema only -- string node/edge discriminators, NO schema break (mirrors the P4 props/SERVED_FROM derive precedent). The current Kuzu build lacks SPLIT() -- author cluster/detection queries WITHOUT it. Rule 20: QUERY the live graph, never rebuild to answer a traversal.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>comp-kuzu "MATCH (n) RETURN labels(n)[0] AS kind, count(*) ORDER BY count(*) DESC"</run>
      <expect>Node census returns Field/TypeDecl/Component (199 Component) and the edge set (RENDERS 2447, PROP_PASSES 1382, READS_FIELD 2110, FLOWS_TO 961, FETCHES 109). Provenance header = current (pin==marker HEAD).</expect>
      <if_mismatch>STOP. If header is BEHIND/UNKNOWN VINTAGE, do not build queries against a stale vintage -- surface to COO. The cluster extractor MUST ride the live P1/P4 graph.</if_mismatch>
    </step>
    <step>
      <run>comp-cache collisions</run>
      <expect>Existing shared-React-Query-key model enumerated -- P2 SHARES_SOURCE generalizes this component<->data-source coupling. Understand the existing collision surface before defining the cluster grouping key.</expect>
      <if_mismatch>If comp-cache errors or the key model is unclear, note it -- the SHARES_SOURCE grouping must be a superset (gold artifact + served key + endpoint + RQ key + hook + type), not RQ-key-only.</if_mismatch>
    </step>
  </phase>
  <phase id="2" when="before commit">
    <step>
      <run>comp-kuzu "MATCH (p:Page)-[:CLUSTERS]->(c:PanelCluster)-[:CONTAINS_DRILLDOWN*0..]->(d) RETURN p.name, count(DISTINCT c), count(DISTINCT d) LIMIT 25" (against the local/scratch emit)</run>
      <expect>The new Cluster/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN edges materialize in the local emit; drilldown nesting traverses; per-firm _partners cohort tagged on the drilldown nodes.</expect>
      <if_mismatch>STOP. If the cluster/membership emit is empty or the drilldown nesting does not traverse, the extractor is not emitting the additive schema correctly -- fix before commit.</if_mismatch>
    </step>
  </phase>
  <phase id="3" when="after commit">
    <step>
      <run>coverage check: enumerate coverage.unresolved over the 119-file page tree</run>
      <expect>119/119 page-tree files processed, coverage.unresolved EXPLICITLY enumerated (0 silent Unknown -- the PRD no-silent-Unknown invariant).</expect>
      <if_mismatch>Surface every unresolved file with its reason (visible-unresolved, never silent-dropped). A silent Unknown is a P2 acceptance failure.</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<cross_domain_coordination>
P2-2 (0.7.0_AE_CloudOps) MATERIALIZES the Cluster/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN/SHARES_SOURCE edges into the canonical Nessie graph via the derive runner (atomic-ledgered, P4 precedent). The ADDITIVE node/edge SCHEMA you define here is the shared interface -- MCP AE with the exact node labels + edge types + property keys BEFORE AE's derive-deploy, so the materialization matches your emit. No firm-pipeline cross-reference (this is the portal/graph estate, not bd/cot/inf). P2-3 (CLI) queries what P2-2 materializes -- same schema contract.
</cross_domain_coordination>

<acceptance_criteria>
1. The extractor emits Cluster/PanelCluster nodes + CLUSTERS/CONTAINS_DRILLDOWN membership edges + cross-panel SHARES_SOURCE edges, page-rooted, over the portal page tree.
2. Community detection groups panel clusters by shared data-source (the 6-source superset), validated on AdvisorIntelligence (the richest page) -- the panel->drilldown tree matches the real component structure.
3. Drilldown nesting-depth + per-firm `_partners` cohort axis are FIRST-CLASS on the drilldown nodes (queryable).
4. Coverage = 119/119 page-tree files, 0 silent Unknown (coverage.unresolved enumerated with reasons).
5. ADDITIVE schema only -- no break to the existing CloudNode/CloudEdge schema (string discriminators).
6. Session-log Compiler Tools section reproduces every <run> above with observed output + pass/fail vs <expect>. Missing rows = REWORK.
RAVC2 to COO (CC CTO). Intermediate RAVC2 on the local emit is fine for a checkpoint before P2-2 materialization.
</acceptance_criteria>

<dependencies>
  <dependency project="NFRA_TSGRAPH" task="P1" status="complete"/>
  <dependency artifact="live canonical graph (comp-kuzu, HEAD-current)" status="available"/>
</dependencies>

<references>
  <ref type="prd">docs/architecture/NFRA_TSGRAPH_PRD.md section 9 (Andrew-steered P2, 2b61ac87e)</ref>
  <ref type="code">org/modules/graph/tsgraph_spike/** (the P1 ts-morph extractor -- DE lane; P2 extends it)</ref>
</references>

<lane_note>
DE-primary (the ts-morph extractor extension = the hard TS/semantic work; you own the substrate from P1). 0.7.0_AE consult for the Nessie materialization (P2-2). GATE for GO: this is the P2 lead -- COO will GO it once a DE lane is live (0.4.0_DE is offline at authoring; spawn-vs-queue is the COO/MSTR/Andrew allocation call). RAVC2 to COO (CC CTO).
</lane_note>
