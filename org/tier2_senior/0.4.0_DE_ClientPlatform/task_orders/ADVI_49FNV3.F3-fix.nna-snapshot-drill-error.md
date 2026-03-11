<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-09-F3-fix</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform</issued_to>
    <date>2026-03-09</date>
    <status>complete</status>
    <thread_serial>ADVI_49FNV3-001</thread_serial>
  </metadata>

  <objective>
    F3 was prematurely marked complete. The NNA snapshot drill in DistributionTab.tsx is
    erroring when the user clicks a state to drill into city-level or relationship-level NNA.
    Andrew confirmed this on 2026-03-09: the drill triggers an error, not just "no data."

    The prior F3 investigation (2026-03-06) concluded "city-to-client is a data constraint,
    not a wiring gap" and closed the task order without a code change. That conclusion is
    being challenged by Andrew — the existing data structure should support this drill. Go
    back in and fix it.
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

  <context>
    The snapshot NNA drill code path is:

    1. `nnaDrillData` (line 1707-1715): reads `analyticsData.views.nna[period].geo.drill`
       from `header_metrics_quarterly.json`. This is the NNA distribution drill data, NOT
       the timeseries `nna_geo_drill` from `timeseries_chart.json`.

    2. `handleSegmentClick` (line 1815-1834): on state click, checks if
       `nnaDrillData?.[seg.key]` exists. If falsy, falls back to segment toggle instead of
       drilling. If truthy, sets `geoDrillLevel('city')` and `selectedStateKey`.

    3. City segment builder (line 1655-1691): when drilled, reads
       `nnaDrillData[selectedStateKey].by_city` to build city-level donut segments.

    4. ADV drill (line 1680-1688): reads `parent.clients` from the donut segment itself
       (not from nnaDrillData). Different data path than GEO.

    The error could be in any of these:
    - `nnaDrillData` is present but shaped wrong (missing `by_city`, wrong key format)
    - The drill data is null/undefined causing a runtime error on property access
    - The city segment builder produces malformed DonutSegment objects (missing required
      fields like `color`, `aua_pct`) that crash the donut renderer
    - Type mismatch between what EC2 script 09 emits and what the frontend expects

    EC2 script 09 (`09_generate_partner_analytics.py`, Y6b block, lines 1061-1087)
    emits: `geo_drill_dist[state] = { total: ..., by_city: { city_key: DistributionStats } }`
    for states with >= 2 relationships in any city.
  </context>

  <requirements>
    <requirement id="1">Reproduce the error. Load the AdvisorIntelligence page, go to
      Distribution tab, select NNA metric, GEO cohort, Snapshot view. Click any state
      segment. Identify the exact error (console error, blank render, crash).</requirement>
    <requirement id="2">Trace the data path end-to-end. Fetch the actual JSON from the
      portal API (or read a sample from S3/local cache) and confirm the shape of
      `views.nna[period].geo.drill[stateKey]`. Does `by_city` exist? What are the keys
      and values?</requirement>
    <requirement id="3">Fix the drill so clicking a state in NNA snapshot GEO mode shows
      city-level NNA segments. If the data is there but the frontend misreads it, fix the
      frontend. If the data shape is subtly wrong (e.g., nested differently than expected),
      adapt the frontend to the actual shape.</requirement>
    <requirement id="4">Fix or gracefully handle the relationship-level drill (city to
      client). If per-relationship data exists in the drill structure, wire it. If it truly
      does not exist, the drill should NOT error — it should either show an informative
      state or simply not offer the click affordance at the city level.</requirement>
    <requirement id="5">No errors on any drill path: GEO state -> city (must work),
      city -> client (must work or gracefully degrade), ADV architect -> client (must work
      or gracefully degrade).</requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">Clicking a state in NNA snapshot GEO donut drills to cities without error.</criterion>
    <criterion id="2">City-level NNA donut renders with correct city names, NNA values, and client counts.</criterion>
    <criterion id="3">If city-to-client drill data does not exist, the UI does not offer a clickable affordance at the city level (no dead-end click that errors).</criterion>
    <criterion id="4">ADV architect-to-client drill does not error.</criterion>
    <criterion id="5">Portal DEV commit with --author flag.</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT mark this complete with "no code change needed" again. Andrew
      confirmed the drill errors. Something is broken — find it and fix it.</constraint>
    <constraint>Do NOT assume the EC2 script output matches the expected shape without
      verifying against the actual JSON. Read real data.</constraint>
    <constraint>If a data change is genuinely required (EC2 script 09 is not emitting the
      right structure), write a brief for DS and issue a task order — but also add defensive
      handling in the frontend so it degrades gracefully instead of erroring.</constraint>
  </constraints>

  <dependencies/>

  <deliverables>
    <deliverable type="commit">Portal DEV commit fixing NNA snapshot drill error.</deliverable>
    <deliverable type="document">If data gap found: brief for DS identifying exact shape
      mismatch between EC2 script 09 output and frontend expectations.</deliverable>
  </deliverables>

  <references>
    <ref type="prd">docs/architecture/ADVISOR_INTELLIGENCE_49FN_V3_PRD.md (F3 section)</ref>
    <ref type="prior">org/tier2_senior/0.4.0_DE_ClientPlatform/logs/2026-03-06/advi_49fnv3_f3_f5_n1n2_investigation.md (prior investigation — conclusion challenged)</ref>
    <ref type="source">portal/src/pages/AdvisorIntelligence/tabs/DistributionTab.tsx (lines 1655-1834)</ref>
    <ref type="data">data/black_diamond/scripts/gold/09_generate_partner_analytics.py (Y6b block, lines 1061-1087)</ref>
  </references>
</task_order>
