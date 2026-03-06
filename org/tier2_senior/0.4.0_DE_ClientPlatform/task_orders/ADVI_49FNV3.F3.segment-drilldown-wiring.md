<task_order>
  <metadata>
    <id>ADVI_49FNV3.F3.segment-drilldown-wiring</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>pending</status>
  </metadata>

  <objective>
    Investigate and wire F3: city-level and client-level drilldowns in the Snapshot NNA section of
    Segment Analytics (DistributionTab.tsx). Data exists in the data contract (Y6b city drill,
    Y6d relationship drill). The click handlers for the Snapshot NNA panel are not wired.
  </objective>

  <scope>
    <pages>
      <page>portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</page>
    </pages>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx</file>
      <file action="modify">portal/src/pages/AdvisorIntelligence/types.ts</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">Read `DistributionTab.tsx` and `types.ts`. Locate the Snapshot NNA geo donut.
      Check if `nna_geo_drill` data from `timeseries_chart.json` is being consumed by this component.
      If not, wire it: clicking a state in the NNA geo donut drills to cities within that state.</requirement>
    <requirement id="2">Clicking a city should drill to individual clients. Wire the client-level click
      handler using Y6d relationship drill data if available in the published JSON.</requirement>
    <requirement id="3">If the drill data exists in the JSON but the click handler is missing, wire it.
      If the drill data is not present in the JSON (Lambda not emitting it), write a brief for DS
      identifying what needs to be added to the publisher output.</requirement>
    <requirement id="4">Type all new drill levels in `types.ts`. No `any` types.</requirement>
    <requirement id="5">After wiring, issue an RD task order for visual implementation of the drill
      UI (city/client drill panel) if the wiring confirms data is available.</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Clicking a state in Snapshot NNA geo donut drills down to cities.</criterion>
    <criterion id="2">Clicking a city drills to individual clients OR a clear data gap brief is written
      identifying what the publisher needs to emit.</criterion>
    <criterion id="3">TypeScript types updated. Portal DEV commit with `--author` flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not issue RD task order until you have confirmed the data path exists in the JSON.
      If the publisher is not emitting the data, fix that first (DS task or publisher change).</constraint>
    <constraint>Do not duplicate drill logic that already exists for the cumulative NNA chart views.
      Reuse patterns already present in DistributionTab.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit wiring NNA geo drill click handlers.</deliverable>
    <deliverable type="document">Optional: brief for DS if publisher gap found.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md</ref>
  </references>
</task_order>
