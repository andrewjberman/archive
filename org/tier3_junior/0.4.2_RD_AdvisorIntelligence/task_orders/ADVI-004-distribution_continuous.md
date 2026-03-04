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
    <gate_status>CLEARED — DT Stream B1 deployed bd-v2.15.0. adv_drill + cla are LIVE in
      timeseries_chart.json. DE types committed portal DEV 7df26bb. START IMMEDIATELY.</gate_status>
    <updated_by>0.4.0_DE_ClientPlatform</updated_by>
    <updated_date>2026-03-04</updated_date>
  </metadata>

  <objective>
    Implement C2 (ADV continuous NNA with architect->client drill-down) and C4 (CLA continuous
    stacked area with full drill-down including city) in DistributionTab.tsx per the ADVI-004
    receipt. Both backend keys are now live. DE has typed them. Start now.
  </objective>

  <references>
    <ref type="receipt">org/tier3_junior/0.4.2_RD_AdvisorIntelligence/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.0_DE_ClientPlatform.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
    <ref type="types">portal/src/pages/AdvisorIntelligence/types.ts — CumulativeChartResponse.cla? and .adv_drill? are typed (portal DEV 7df26bb)</ref>
    <ref type="data_contract">org/tier2_senior/0.4.0_DS_ClientPlatform/deliverables/data_contract.xml</ref>
  </references>

  <requirements>

    <!-- ================================================================ -->
    <!-- STREAM C2 — Continuous NNA ADV (architect -> client drill)        -->
    <!-- ================================================================ -->
    <requirement id="C2.1">
      GATE CLEARED. adv_drill is LIVE in timeseries_chart.json (bd-v2.15.0).
      adv_drill is typed on CumulativeChartResponse as:
        adv_drill?: Record&lt;string, CumulativeChartView&gt;
      Key = architect display name matching adv.categories exactly.
    </requirement>
    <requirement id="C2.2">
      Implement ADV continuous NNA view in DistributionTab.tsx:
        - Top architects as separate series from adv.categories
        - Click architect -> drill to client/relationship level using chartData.adv_drill[architectKey]
          where architectKey is the adv.categories string (e.g. "Travis Penfield")
        - Client-level category keys = "{name} ({id})" (from DS implementation)
        - Breadcrumb returns to architect-level view
        - No drill-down past relationship level (client is terminal grain for ADV)
        - Guard on chartData?.adv_drill?.[key] before rendering drill view
    </requirement>

    <!-- ================================================================ -->
    <!-- STREAM C4 — Continuous CLA stacked area (full drill including city) -->
    <!-- ================================================================ -->
    <requirement id="C4.1">
      GATE CLEARED. cla is LIVE in timeseries_chart.json (bd-v2.15.0).
      cla is typed on CumulativeChartResponse as:
        cla?: {
          total: CumulativeChartView
          geo_drill: Record&lt;string, CumulativeChartView&gt;
          adv_drill: Record&lt;string, CumulativeChartView&gt;
          geo_city_drill?: Record&lt;string, Record&lt;string, CumulativeChartView&gt;&gt;
        }
    </requirement>
    <requirement id="C4.2">
      Implement continuous CLA view rendering all four drill levels:
        - cla.total: firm-wide two-series stacked area (NMNC/NMEC)
        - cla.geo_drill: per-state breakdown — click state to drill to cities
        - cla.geo_city_drill: per-city within state (guard: geo_city_drill may be absent)
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
        - cla.geo_drill keys = state abbreviations matching timeseries_chart.json geo.categories
        - cla.adv_drill keys = architect display names matching timeseries_chart.json adv.categories
        - "Other" bucket key is capital-O exactly ("Other")
      Same pattern as existing geo_drill lookup — follow that implementation.
    </requirement>
    <requirement id="C4.5">
      Guard on chartData?.cla before rendering CLA metric selector or view.
      CLA is only available in continuous mode (not snapshot). Do not add CLA to the
      snapshot metric selector.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">C2: ADV continuous NNA renders with architect series, and clicking an architect drills to client/relationship series (adv_drill[key]).</criterion>
    <criterion id="2">C2: Breadcrumb returns from client to architect level.</criterion>
    <criterion id="3">C4: CLA continuous renders as stacked area (NMNC/NMEC) at total level.</criterion>
    <criterion id="4">C4: GEO view offers state drill -> city drill (geo_city_drill guarded for absence).</criterion>
    <criterion id="5">C4: ADV view renders per-architect NMNC/NMEC (adv_drill).</criterion>
    <criterion id="6">Colors use CATEGORY_COLORS/GEO_COLORS — no backend colorMap dependency.</criterion>
    <criterion id="7">Record keys align with existing geo/adv category keys ("Other" capital-O).</criterion>
    <criterion id="8">bunx tsc -b passes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Gates are CLEARED. Do not wait. Start immediately.</constraint>
    <constraint>Implement per ADVI-004 receipt field names and types. Do not invent fields.</constraint>
    <constraint>Colors are frontend-only. Do not expect or require a backend colorMap field.</constraint>
    <constraint>DE reviews before DT pushes to DEV. Signal DE when commits are ready.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.2_RD_AdvisorIntelligence &lt;0.4.2_RD_AdvisorIntelligence@opal.agent&gt;" -m "0.4.2_RD_AdvisorIntelligence: AdvisorIntelligence/DistributionTab -- ..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">DistributionTab.tsx: C2 ADV continuous NNA with architect->client drill-down</deliverable>
    <deliverable type="commit">DistributionTab.tsx: C4 CLA continuous stacked area with full drill (total/geo/city/adv)</deliverable>
  </deliverables>
</task_order>
```
