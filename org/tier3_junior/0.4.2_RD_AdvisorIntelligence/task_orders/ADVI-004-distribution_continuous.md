# Task Order: Distribution Tab Continuous Views (C2 + C4) — 0.4.2_RD_AdvisorIntelligence

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-004-rd-distribution_continuous</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
  </metadata>

  <objective>
    Implement C2 (ADV continuous NNA with drill-down) and C4 (CLA continuous stacked
    area) in DistributionTab.tsx per the ADVI-004 binding contract. Both are blocked
    by DT Stream B1 deploy — do not start until DT confirms the publisher update
    is deployed and adv_drill + cla_timeseries are present in timeseries_chart.json.
  </objective>

  <references>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV (architect -> client drill)        -->
    <!-- BLOCKED: DT Stream B1 deploy must complete first                  -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE: Do not start until DT confirms adv_drill is deployed in
      timeseries_chart.json S3 output (Stream B1).
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view per ADVI-004 receipt:
        - Top architects as separate series using adv_drill data
        - Search input for architects not in top list
        - Click architect -> drill to client/relationship level (adv_drill[architectKey])
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level (client is terminal grain for ADV)
        - colorMap per the receipt (portal tokens, not placeholders)
      Use the same chart pattern as C1 (GEO continuous) where possible.
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA stacked area                           -->
    <!-- BLOCKED: DT Stream B1 deploy must complete first                  -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE: Same as C2 — requires cla_timeseries deployed in timeseries_chart.json.
    </requirement>
    <requirement id="C4.2">
      Implement continuous CLA view per ADVI-004 receipt:
        - Stacked area chart: NMNC AUM (green) and NMEC AUM (blue) over time
        - Y-axis = absolute dollar AUM
        - Grains: cla.total (firm-wide), cla.geo (state), cla.adv (architect terminal)
        - Search + drill for GEO view (state level only — NO city drill-down)
        - colorMap per receipt
    </requirement>
    <requirement id="C4.3">
      CLA city drill-down is BLOCKED (cla.geo_city_drill not implemented due to gold
      layer limitation). Do NOT add city-level drill-down for the CLA view. State is
      the terminal grain for CLA GEO. This is different from NNA GEO (which has city drill).
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C2: ADV continuous NNA renders with architect series, search, and client drill-down per receipt.</criterion>
    <criterion id="2">C4: CLA continuous renders as stacked area with NMNC/NMEC at total/geo/adv grains per receipt.</criterion>
    <criterion id="3">CLA GEO view does NOT offer city drill-down (state is terminal grain).</criterion>
    <criterion id="4">colorMap values are real portal tokens per receipt, not placeholders.</criterion>
    <criterion id="5">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Both C2 and C4 are BLOCKED by DT Stream B1 deploy. Do not start until confirmed.</constraint>
    <constraint>Implement per ADVI-004 receipt field names and types. Do not invent fields.</constraint>
    <constraint>No CLA city drill-down (cla.geo_city_drill blocked at gold layer).</constraint>
    <constraint>DE reviews before DT pushes to DEV.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: C2 ADV continuous NNA with drill-down</deliverable>
    <deliverable type="commit">DistributionTab.tsx: C4 CLA continuous stacked area</deliverable>
  </deliverables>
</task_order>
```
