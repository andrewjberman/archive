# Task Order: Portal Types + Wiring for adv_drill + cla_timeseries — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI_V1VERS.004.de-portal-types-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>complete</status>
    <thread_serial>ADVI_V1VERS-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
  </metadata>

  <objective>
    Define TypeScript interfaces for adv_drill and cla per the ADVI-004 receipt,
    with CTO scope correction: cla includes geo_city_drill (not blocked). No new
    endpoint or query key needed — existing getCumulativeChart() covers this.
  </objective>

  <references>
    <ref type="receipt">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <requirements>

    <requirement id="TY.1">
      Add the following to portal/src/pages/AdvisorIntelligence/types.ts as an
      extension on CumulativeChartResponse (non-breaking, optional key):
        cla?: {
          total: CumulativeChartView
          geo_drill: Record&lt;string, CumulativeChartView&gt;
          adv_drill: Record&lt;string, CumulativeChartView&gt;
          geo_city_drill?: Record&lt;string, Record&lt;string, CumulativeChartView&gt;&gt;
        }
      geo_city_drill is optional (?) at the type level since it may not be present
      in older cached responses during rollout.
    </requirement>
    <requirement id="TY.2">
      No new endpoint needed. No new React Query key needed. Existing
      getCumulativeChart() -> GET /api/scoped/advisor-intelligence/timeseries_chart.json
      already covers these new fields. Just type the response correctly.
    </requirement>
    <requirement id="TY.3">
      No backend colorMap field in the contract. RD uses existing frontend hex
      palettes (CATEGORY_COLORS, GEO_COLORS in DistributionTab.tsx). Do NOT add
      a colorMap type.
    </requirement>
    <requirement id="TY.4">
      Blocked by DS delivering A1/A2 — DS updates data_contract.xml first, then
      DE types after to ensure alignment. Read DS's updated data_contract.xml
      before finalizing your types.
    </requirement>
    <requirement id="TY.5">
      Review RD implementation (C2 + C4) when those streams are ready. Signal DT
      to push to DEV only after review. Document review in your session log.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">cla type on CumulativeChartResponse includes total, geo_drill, adv_drill, and optional geo_city_drill.</criterion>
    <criterion id="2">No new endpoint, no new query key added.</criterion>
    <criterion id="3">No colorMap type defined (frontend-only colors).</criterion>
    <criterion id="4">bunx tsc -b passes after changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Types must match DS's data_contract.xml. Read it before finalizing.</constraint>
    <constraint>Do not push. DT pushes after DE review of RD work.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">types.ts: cla type extension on CumulativeChartResponse</deliverable>
  </deliverables>
</task_order>
```
