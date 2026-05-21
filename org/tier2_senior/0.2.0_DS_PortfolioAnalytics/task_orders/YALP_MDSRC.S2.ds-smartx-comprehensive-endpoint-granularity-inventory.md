<task_order>
  <metadata>
    <id>YALP_MDSRC.S2</id>
    <slug>ds-smartx-comprehensive-endpoint-granularity-inventory</slug>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.2.0_DS_PortfolioAnalytics</issued_to>
    <date>2026-05-21</date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_unblock_condition>GO ON PICKUP — Andrew-direct (2026-05-21). RETROACTIVE FORMALIZATION: Andrew directed 0.2.0_DS on this comprehensive SmartX reverse-engineering ask; 0.2.0_DS began on the directive (correctly not idle-waiting for COO scope) and the deliverable is substantively complete + committed before this TO was authored. S2 is the formal wrapper so the work RAVC2s cleanly — it documents the scope Andrew set + the ACs the committed deliverable meets. Not new work to start; a TO to close.</dispatch_unblock_condition>
    <project_code>YALP_MDSRC</project_code>
    <priority>P1 — Andrew-direct. Establishes how deep SmartX goes — every backend endpoint + granularity — to gauge the snapshot + historical portfolio-analytics depth procurable from the platform. Feeds WS-5 / v0.4.</priority>
    <sla>~1-2 effort-days — substantively complete at TO-authoring time.</sla>
  </metadata>

  <references>
    <directive>Andrew, 2026-05-21 (verbatim): "we need to know how deep smartx goes, need to know all available endpoints and granularities to gauge the extent of snapshot and historical portfolio analytics and raw info for downstream portfolio analytics that can be procured on the platform."</directive>
    <deliverable>docs/briefs/mdsrc-smartx-comprehensive-endpoint-inventory-20260521.md — the SmartX comprehensive endpoint+granularity inventory. v1 draft 54c072791; v2 (api/3.1 exhaustion folded in) e2bd44014, origin/CLOUD.</deliverable>
    <rest_baseline>docs/briefs/smartx-rest-api-inventory-20260521.md (b2597ea25, 0.4.0_DS) — the B1/S1/SXPL_RESTIN.001 REST baseline S2 extends from.</rest_baseline>
    <standard>docs/architecture/THIRD_PARTY_DATA_INTEGRATION_STANDARD.md (RATIFIED) — reverse-engineer the provider's backend API; never "scrape".</standard>
  </references>

  <context>
    A3-class mapping exists for YCharts; S1 + B1 + SXPL_RESTIN.001 touched ~13 SmartX REST endpoints. Andrew asked for a COMPREHENSIVE SmartX picture — all backend surfaces, all endpoints, all granularities — to size what portfolio-analytics depth is procurable. 0.2.0_DS ran a 3-prong reverse-engineering effort: (A) live api/3.1 exhaustion via the SXPL_RESTIN ROPC-JWT probe harness, (B) GraphQL schema introspection, (C) the existing portal.managedaccounts.io.har web-app baseline. S2 formalizes that scope. The B1 overlap (0.4.0_DS owns the SmartX model-performance pull) is coordinated DS-to-DS — S2 extends from b2597ea25, no double-probing.
  </context>

  <scope>
    <in_scope>
      - Comprehensive SmartX backend inventory: all reachable surfaces (api.smartxadvisory.com/api/3.1 REST, smartx.managedaccounts.io/api/3.0 legacy, performance.smartxadvisory.com, graphql.smartxadvisory.com, portal.managedaccounts.io/ng_api) — endpoint patterns, params, auth model.
      - Per endpoint: entity-grain x time-grain (snapshot vs daily/weekly/monthly series + history depth) x analytics-primitive yielded.
      - A procurable-vs-gap read: what portfolio-analytics depth SmartX can serve vs what it cannot.
      - GraphQL: schema introspection to bound what the GraphQL API is (not assume).
      - Empirically bound the absent surfaces (404/absent endpoints), not just inferred gaps.
    </in_scope>
    <out_of_scope>
      - Building any SmartX pull pipeline — S2 is the inventory/assessment; pipeline work is separate (B1/B2 + future v0.4 TOs).
      - Re-probing what B1 (0.4.0_DS, the SmartX model-performance pull) already owns.
    </out_of_scope>
  </scope>

  <compiler_tools_mandate>
    <note>S2 is a backend-API reverse-engineering investigation — it modifies no gold script, portal component, route, IAM, or schema. No comp-* graph tool covers SmartX backend-API probing; the assertion below is a structural self-check (the audit record the TO_COMPILER_GATE requires).</note>
    <phase id="2" when="before declaring complete">
      <step>
        <run>Verify the committed inventory covers every claimed SmartX surface with per-endpoint grain + the procurable-vs-gap table, and that absent endpoints are empirically confirmed (404/probe), not inferred.</run>
        <expect>5 surfaces inventoried; api/3.1 exhausted (live sweep, not HAR-only); GraphQL introspected; absent-endpoint set empirically bounded.</expect>
        <if_mismatch>Any surface left HAR-only-inferred is incomplete — run the live confirmation before RAVC2.</if_mismatch>
      </step>
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    - B1 overlap: 0.4.0_DS owns the SmartX model-performance pull; S2 extends from b2597ea25 and coordinates DS-to-DS — no double-probing. 0.2.0_DS flagged the b2597ea25 caveat-7 contradiction (the new daily model-return finding) to 0.4.0_DS directly.
    - PROBE-SCRIPT LANDING: the GraphQL introspection probe + the api/3.1 sweep probe belong in data/smartx/scripts/ (SHARED_OPAL_ETL lane). Base 0.2.0_DS is correctly hook-blocked from that lane; the probes are retained in .runtmp. Landing them is a follow-on: route to 0.7.0_AE_CloudOps~A (added to SHARED_OPAL_ETL 2026-05-21, 789a2f21c) or the OpalETL lane owner when it boots. Not an S2 blocker — S2's deliverable is the inventory brief; the probe-script landing is a tracked follow-on.
    - No silver/bronze/gold or S3-data changes — auto-rule 4 N/A.
  </cross_domain_coordination>

  <acceptance_criteria>
    - AC1 — all reachable SmartX backend surfaces inventoried (REST api/3.1, legacy api/3.0, performance service, GraphQL, ng_api); committed brief.
    - AC2 — per endpoint: entity-grain x time-grain (snapshot vs daily/weekly/monthly + history depth) x analytics-primitive recorded.
    - AC3 — a procurable-vs-gap table: portfolio-analytics depth SmartX can serve vs cannot; absent endpoints empirically confirmed.
    - AC4 — material findings called out explicitly, incl. the /api/3.1/models/{id}/performance daily/weekly/monthly model-return series (supersedes the "SmartX monthly-only" consensus) and the GraphQL API's actual nature (compliance microservice, not analytics).
    - AC5 — session log Compiler Tools section reproduces the Phase-2 self-check; RAVC2 to COO + CC CTO. The committed deliverable is docs/briefs/mdsrc-smartx-comprehensive-endpoint-inventory-20260521.md (e2bd44014).
  </acceptance_criteria>
</task_order>
