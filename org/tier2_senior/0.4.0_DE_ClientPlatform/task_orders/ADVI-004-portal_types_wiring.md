# Task Order: Portal Types + Wiring for adv_drill + cla_timeseries — 0.4.0_DE_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-ADVI-004-de-portal_types_wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-03</date>
    <status>pending</status>
    <thread_serial>ADVI-004</thread_serial>
    <thread_ref>org/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c/</thread_ref>
  </metadata>

  <objective>
    Define TypeScript interfaces and wire API endpoints for adv_drill and cla_timeseries
    per the binding contract in the ADVI-004 receipt. The receipt specifies exact interface
    names and shapes agreed with DS and RD — implement those, not your own interpretation.
  </objective>

  <references>
    <ref type="receipt">org/tier2_senior/0.4.0_DE_ClientPlatform/threads/ADVI-004-pattern-0-advdrill--clatimeseries-data-c_0.4.0_DS_ClientPlatform+0.4.2_RD_AdvisorIntelligence.md</ref>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_COMPLETION.md</ref>
  </references>

  <requirements>

    <requirement id="TY.1">
      Add the following TypeScript interfaces to portal/src/pages/AdvisorIntelligence/types.ts
      per the ADVI-004 receipt (exact names and field types from the thread convergence):
        - AdvDrillResponse (or the name agreed in receipt)
        - ClaTimeseriesResponse (or the name agreed in receipt)
        - Any supporting types (CumulativeChartView extensions, colorMap type)
      Read the receipt for the exact interface shapes. Do not add fields not in the receipt.
    </requirement>
    <requirement id="TY.2">
      Wire the new data into the existing query/fetch pattern in
      portal/src/api/endpoints/advisor-intelligence.ts. Add query keys and endpoint
      paths per the receipt contract. The data arrives as new fields in
      timeseries_chart.json — no new API endpoint needed, just type the response correctly.
    </requirement>
    <requirement id="TY.3">
      Note: cla.geo_city_drill is BLOCKED (gold layer limitation). Do NOT add a type
      for city-level CLA drill-down. The interface should type cla.total, cla.geo,
      and cla.adv only.
    </requirement>
    <requirement id="TY.4">
      Review RD implementation (C2 + C4) when those streams are ready. Signal DT
      to push to DEV only after review. Document review in your session log.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">TypeScript interfaces match ADVI-004 receipt field names and types exactly.</criterion>
    <criterion id="2">API endpoint wiring updated to include new response fields.</criterion>
    <criterion id="3">No type for cla.geo_city_drill (blocked).</criterion>
    <criterion id="4">bunx tsc -b passes after changes.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Types must match the ADVI-004 receipt. Do not add speculative fields.</constraint>
    <constraint>Do not push. DT pushes after DE review of RD work.</constraint>
    <constraint>No emojis in code.</constraint>
    <constraint>Commit with: git commit --author="0.4.0_DE_ClientPlatform &lt;0.4.0_DE_ClientPlatform@opal.agent&gt;" -m "..."</constraint>
  </constraints>

  <deliverables>
    <deliverable type="commit">types.ts: AdvDrillResponse + ClaTimeseriesResponse interfaces</deliverable>
    <deliverable type="commit">advisor-intelligence.ts: endpoint wiring updates</deliverable>
  </deliverables>
</task_order>
```
