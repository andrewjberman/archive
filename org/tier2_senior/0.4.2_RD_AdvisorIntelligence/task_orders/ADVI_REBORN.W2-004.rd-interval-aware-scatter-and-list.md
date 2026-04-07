# ADVI_REBORN.W2-004 — RD: Wire interval selector to fee scatter + advisor list

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-07-reborn-w2-004-rd</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.2_RD_AdvisorIntelligence</issued_to>
    <date>2026-04-07</date>
    <status>complete</status>
    <!-- Completed 2026-04-07. Portal DEV commit be72c0b. Period selector wired to windowed data. -->
    <project_code>ADVI_REBORN</project_code>
    <priority>high</priority>
    <phase>WS2</phase>
  </metadata>

  <objective>
    Make the Books N1 fee efficiency scatter plot and advisor list interval-aware.
    When the user toggles the period selector (QTD/YTD/1Y/3Y/Max), the scatter
    dots, regression line, and advisor metrics all update from the selected window.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_NNAFEE_FEE_EFFICIENCY_VIEWS.md</ref>
    <ref type="design-note">org/tier2_senior/0.4.0_DE_ClientPlatform/task_orders/ADVI_NNAFEE.007.design-note-interval-aware-advisor-list.md</ref>
  </references>

  <scope>
    File: portal/src/pages/AdvisorIntelligence/tabs/ClientsTab.tsx (FeeEfficiencyPanel)

    1. Add period selector state: useState<FeeEfficiencyWindow>('trailing_1y')
    2. Add period toggle buttons matching existing pattern (QTD/YTD/1Y/3Y/Max)
    3. Read from feeData.windows[selectedWindow] instead of top-level feeData.regression/advisors
    4. Fall back to top-level regression/advisors if windows not present (backward compat)
    5. Scatter plot updates: dots, regression line, R^2 annotation all from selected window
    6. Table view updates: advisor metrics from selected window's advisors array
    7. Advisor list below the panel: NNA, Growth, New Clients, Revenue, Fee Yield, Efficiency all from selected window
    8. AUA stays as latest snapshot (does NOT change with interval — AUA is timeless)

    Key rule from DE design note:
    - AUA: always latest snapshot
    - Everything else: changes with interval
  </scope>

  <requirements>
    <requirement id="1">Period selector with QTD/YTD/1Y/3Y/Max options</requirement>
    <requirement id="2">Scatter plot re-renders with window-specific regression + advisor data</requirement>
    <requirement id="3">Table view re-sorts with window-specific metrics</requirement>
    <requirement id="4">AUA column stays static regardless of period selection</requirement>
    <requirement id="5">Graceful fallback when windows field is absent (use top-level data)</requirement>
    <requirement id="6">44px touch targets on period toggle (per ADHC_DESIGN audit)</requirement>
    <requirement id="7">Commit as you go. bun run build after each.</requirement>
  </requirements>

  <dependencies>
    <dependency agent="0.4.0_DE_ClientPlatform" task="ADVI_REBORN.W2-003" status="complete">Windowed types must exist</dependency>
  </dependencies>

  <commit_pattern>feat(FeeEfficiencyPanel): interval-aware scatter + advisor list</commit_pattern>
</task_order>
