<task_order>
<metadata>
  <to_id>ADVI_INFLV2.014</to_id>
  <project>ADVI_INFLV2</project>
  <title>Inflection Dim Pull Requests Spec (INFLEC_DIM_PULL_REQUESTS.md) — 5 Logical Dims for Andrew Manual Pulls</title>
  <assigned_to>0.4.0_DS_ClientPlatform~B</assigned_to>
  <issued_by>2.0.0_SA_COO</issued_by>
  <issued_date>2026-04-27</issued_date>
  <status>complete</status>
  <priority>HIGH</priority>
  <references>
    <ref type="prd">docs/architecture/ADVI_INFLV2.md</ref>
    <ref type="amended_scope">CTO amendment 20260427T220500Z — replaces original INFLEC_FIELD_GAP_MATRIX.md with INFLEC_DIM_PULL_REQUESTS.md dim-table request packets for Andrew manual pulls</ref>
    <ref type="prerequisite_thread">ADVI_INFLV2.013 joint enrichment scoping (commit 5788d8cd) — 22 mapped fields, 6 clusters; .014 spec flows from .013 Cluster E + F findings</ref>
    <ref type="deliverable">docs/architecture/INFLEC_DIM_PULL_REQUESTS.md (commit 9772ea67, CLOUD)</ref>
  </references>
  <dependencies>
    <dependency>ADVI_INFLV2.013 COMPLETE (5788d8cd) — cluster mapping + pull priority ranking gates .014 dim selection</dependency>
  </dependencies>
</metadata>

<scope>
Author INFLEC_DIM_PULL_REQUESTS.md — 5 logical dim table request packets, each operationally unambiguous for Andrew to execute as separate manual Orion pulls. DS~B leads authoring; DS~A advises data semantics; DE confirms panel dependencies via MCP.

Per-dim required content:
- Name + tag list (verbatim Orion catalog tags, [VERIFY_SPELLING] preserved)
- Named join keys
- Grain + time range
- Splittability hints (can it be pulled in quarters vs full range?)
- Dependent panels + verdict-shifts per panel
- DS receiving-side acceptance criteria (what to check when data arrives)

5 dims (ordered by pull priority):
1. Billing/Fee dim (Cluster E — highest unblocking leverage; flips N1-1 + Panel #10 + L3-3 + Panel #11 from DEFER to PORT_DEGRADED)
2. Performance dim (potential to replace BD gold 05/05b parallel — highest strategic upside)
3. Tax/Cost basis dim (Cluster F — simplification, no new panel unblock alone)
4. Account enrichment dim (cheap additive; backfills views.cla decomp)
5. Household/Suitability dim (product-call; lowest unblocking leverage)

Empirical grounding required in Billing/Fee dim: 2 actual pulls profiled (Pull 1 current-period + Pull 2 history lookback). Key findings to encode: MV=N/A on closed periods; 9-month lookback ceiling; is_fee_earning derivation; $20M non-fee-earning gap vs INFGRD scope.
</scope>

<compiler_tools_mandate>
  <phase id="1" when="before write">
    <step>
      <run>N/A — documentation-only deliverable; no code changes</run>
      <expect>N/A</expect>
      <if_mismatch>N/A</if_mismatch>
    </step>
  </phase>
</compiler_tools_mandate>

<acceptance_criteria>
1. INFLEC_DIM_PULL_REQUESTS.md committed on CLOUD with all 5 dim sections.
2. Each section includes: exact tag names, join keys, grain, time range, splittability hints, dependent panels + verdict-shifts, DS receiving-side acceptance criteria.
3. Billing/Fee dim empirically informed by actual pulls (Pull 1 current-period + Pull 2 history lookback findings).
4. Cluster E billing verdict-shifts documented: N1-1 DEFER->PORT_DEGRADED, Panel #10 DEFER->PORT_DEGRADED, L3-3 DEFER->PORT_DEGRADED, Panel #11 DEFER->PORT_DEGRADED.
5. RAVC to COO with commit hash.

STATUS: COMPLETE.
Deliverable: docs/architecture/INFLEC_DIM_PULL_REQUESTS.md v0.1
Commit: 9772ea67 (CLOUD, 2026-04-27)
DS~B RAVC received: 20260427T230014Z
COO RAVC4 sent: 20260427T234337Z
All 5 ACs met per DS~B RAVC evidence.
</acceptance_criteria>

<cross_domain_coordination>
<none/>
</cross_domain_coordination>
</task_order>
