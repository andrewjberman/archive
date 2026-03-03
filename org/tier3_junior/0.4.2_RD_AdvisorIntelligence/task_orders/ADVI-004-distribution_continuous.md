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
    area with full drill-down including city) in DistributionTab.tsx per the ADVI-004
    receipt. Blocked by DT Stream B1 deploy.
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
        - adv_drill in timeseries_chart.json will work with the existing portal
          drill lookup pattern once DS deploys — wire the render
        - Top architects as separate series
        - Search input for architects not in top list
        - Click architect -> drill to client/relationship level (adv_drill[architectKey])
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level (client is terminal grain for ADV)
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA stacked area (full drill including city) -->
    <!-- BLOCKED: DT Stream B1 deploy must complete first                  -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE: Same as C2 — requires cla deployed in timeseries_chart.json.
    </requirement>
    <requirement id="C4.2">
      Implement continuous CLA view rendering all four drill levels:
        - cla.total: firm-wide two-series stacked area (NMNC/NMEC)
        - cla.geo_drill: per-state breakdown — click state to drill to cities
        - cla.geo_city_drill: per-city within state (city IS available, not blocked)
        - cla.adv_drill: per-architect breakdown (architect is terminal grain for ADV-CLA)
      Y-axis = absolute dollar AUM. Two stacked areas: NMNC and NMEC.
    </requirement>
    <requirement id="C4.3">
      Colors: use existing frontend hex palettes already in DistributionTab.tsx
      (CATEGORY_COLORS, GEO_COLORS). No backend colorMap field — all color assignment
      is frontend-only.
    </requirement>
    <requirement id="C4.4">
      Record key alignment (critical for drill lookup):
        - cla.geo_drill keys = state abbreviations matching timeseries_chart.json.geo.categories
        - cla.adv_drill keys = architect display names matching timeseries_chart.json.adv.categories
        - "Other" bucket key is capital-O exactly ("Other", not "other" or "OTHER")
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C2: ADV continuous NNA renders with architect series, search, and client drill-down.</criterion>
    <criterion id="2">C4: CLA continuous renders as stacked area with NMNC/NMEC at total, geo_drill, geo_city_drill, and adv_drill levels.</criterion>
    <criterion id="3">CLA GEO view offers city drill-down (geo_city_drill is implemented).</criterion>
    <criterion id="4">Colors use CATEGORY_COLORS/GEO_COLORS — no backend colorMap dependency.</criterion>
    <criterion id="5">Record keys align with existing geo/adv category keys ("Other" capital-O).</criterion>
    <criterion id="6">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Both C2 and C4 are BLOCKED by DT Stream B1 deploy. Do not start until confirmed.</constraint>
    <constraint>Implement per ADVI-004 receipt field names and types.</constraint>
    <constraint>Colors are frontend-only. Do not expect or require a backend colorMap field.</constraint>
    <constraint>DE reviews before DT pushes to DEV.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: C2 ADV continuous NNA with drill-down</deliverable>
    <deliverable type="commit">DistributionTab.tsx: C4 CLA continuous stacked area with full drill (total/geo/city/adv)</deliverable>
  </deliverables>
</task_order>
```
