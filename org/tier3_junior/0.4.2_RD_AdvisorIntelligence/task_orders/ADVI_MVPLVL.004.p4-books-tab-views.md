```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-13-p4-books-tab-views</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-03-13</date>
    <status>pending</status>
    <thread_serial>ADVI_MVPLVL-004</thread_serial>
    <thread_ref>org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</thread_ref>
  </metadata>

  <objective>
    Implement Books Tab L3/L4 view enhancements: paired Mix + Concentration panels
    with linked selection, compact AUA/NNA time series charts, and advisor listing
    UI consistency (4h). MVP scope is L3 (relationship) + L4 (account) only;
    L2 (advisor) deferred pending DS 4a mapping confirmation.
  </objective>

  <scope>
    <files>
      <file action="modify">portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx</file>
    </files>
  </scope>

  <requirements>
    <requirement id="4e-mix">
      Mix (asset class breakdown) panels at L3 and L4.

      - Pie chart showing asset class allocation.
      - Data from composition endpoint: mix[] array with asset_class (enum key),
        label (display), market_value, pct.
      - Asset class color mapping: use stable asset_class keys for consistent colors.
      - Linked to Concentration (4f): clicking a Mix slice sets selectedAssetClass
        state, which filters Concentration. Click same slice again clears filter.
    </requirement>

    <requirement id="4f-concentration">
      Concentration (security-level) panels at L3 and L4, linked to Mix.

      - Pie chart or ranked list showing top 10 securities + Other.
      - Data from composition endpoint: concentration.items[] + concentration.other.
      - When selectedAssetClass is set (from Mix click): filter items to only show
        securities matching that asset_class.
      - When selectedAssetClass is null: show all securities.
      - Use items[].key for React keys (stable, unique per DS contract).
    </requirement>

    <requirement id="4e4f-layout">
      Mix + Concentration layout:

      - Desktop (lg+): two panels side-by-side in 2-col grid. Left = Mix, Right = Concentration.
      - Mobile: stacked vertically, Mix above Concentration.
      - Linked selection state: selectedAssetClass: string | null.
      - At L4 (account): can be collapsible/accordion to manage vertical space.
    </requirement>

    <requirement id="4g-timeseries">
      Compact AUA/NNA time series charts at L3 and L4.

      - Two compact inline charts (or single chart with metric toggle):
        - AUA (line chart)
        - NNA (line or diverging bars; line acceptable for MVP)
      - Controls: inherit page-level granularity from AdvisorIntelligence.tsx props.
        Local time window toggle (1Y/3Y/Max) acceptable.
      - Data from timeseries endpoint: daily rows with date, total_aua, cum_inflows,
        cum_outflows, nna.
      - Client-side aggregation: "aggregate full history then filter for display" pattern
        (same as PartnerAnalytics). Defensively sort input by date ascending.
      - At L4 (account): same pattern, using account timeseries endpoint.
    </requirement>

    <requirement id="4h-advisor-listing">
      Advisor listing UI consistency (N1 global view).

      - The AdvisorSummaryTable at ClientsTab.tsx:976-1034 should use the same
        card-like row design as the leaderboard from 3d (AdvisorsTab.tsx).
      - Apply same typography, color treatment, padding, and rank styling.
      - This is blocked on 3d completion — the design language must match.

      Since 3d is now complete (portal commit 64b9b35), apply the same visual treatment:
      text-sm values, NNA green/red coloring, growth % gradient pills, generous padding.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">L3 (relationship) shows Mix + Concentration paired panels with linked selection</criterion>
    <criterion id="2">L4 (account) shows Mix + Concentration (collapsible acceptable)</criterion>
    <criterion id="3">L3 shows compact AUA + NNA time series charts with aggregation</criterion>
    <criterion id="4">L4 shows compact AUA + NNA time series charts</criterion>
    <criterion id="5">Clicking a Mix asset class filters Concentration to that class; clicking again clears</criterion>
    <criterion id="6">N1 advisor summary table matches 3d leaderboard visual design</criterion>
    <criterion id="7">bunx tsc -b passes clean</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>L2 (advisor-level) composition and timeseries are DEFERRED — implement L3/L4 only</constraint>
    <constraint>Do not modify files outside portal/src/pages/AdvisorIntelligence/</constraint>
    <constraint>If shared hooks/components in portal/src/api/ are needed, DE must own those</constraint>
    <constraint>Commit on portal DEV branch with --author="0.4.2_RD_AdvisorIntelligence"</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-proxy-wiring" status="pending">
      RD needs proxy routes and types before wiring data fetches
    </dependency>
    <dependency agent="0.4.0_DS_ClientPlatform" task="ADVI_MVPLVL.004.p4-books-backend-endpoints" status="pending">
      Endpoints must be deployed before live data flows
    </dependency>
  </dependencies>

  <references>
    <ref type="prd">docs/architecture/ADVI_MVPLVL_PRD.md (Part 4, items 4e/4f/4g/4h)</ref>
    <ref type="thread">org/threads/ADVI_MVPLVL-004-p4-books-tab-alignment/</ref>
  </references>

  <deliverables>
    <deliverable type="commit">Portal DEV commit with L3/L4 Mix+Concentration panels, time series charts, and N1 advisor listing redesign</deliverable>
  </deliverables>
</task_order>
```
