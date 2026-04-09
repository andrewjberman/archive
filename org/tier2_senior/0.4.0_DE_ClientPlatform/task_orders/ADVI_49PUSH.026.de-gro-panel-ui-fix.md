<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-026-de</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DE_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>partial -- frontend DONE (DEV 07aa797): Growth tile + types; validation (fix_1 Net Flows cross-check, smoke test) blocked on AE D_04 re-run</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>6</wave>
    <phase>P3 data correctness</phase>
    <mcp_identity>Register with MCP as "0.4.0_DE_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Update the GRO toggle hero metrics tiles in PartnerAnalytics.tsx to:
    1. Verify Net Flows tile correctly maps to the NNA-aligned field from DS .025
    2. Replace the "Total Change" tile with a percentage-based AUA growth decomposition tile
       showing total % growth broken into market and NNA contributions
    Update types.ts to reflect the new growth_decomposition period schema.
  </objective>

  <context>
    File: portal/src/pages/AdvisorIntelligence/components/PartnerAnalytics.tsx
    GRO hero metrics block: lines ~1812-1878

    Current tiles (3):
      1. Market     -- latest.market (dollar), cumMarket aggregate
      2. Net Flows  -- latest.nna (dollar), cumNna aggregate
      3. Total Change -- latest.total (dollar), cumTotal aggregate

    After DS .025 + AE re-run, each growth_decomposition period entry gains:
      total_pct:       total % AUA growth for the period
      market_pct:      market contribution as % of beginning AUA
      nna_pct:         NNA contribution as % of beginning AUA
      (dollar fields market, nna, total remain for audit trail)

    DS .025 also guarantees growth_decomposition[period].nna == nna[period].net,
    so Net Flows in GRO now matches the NNA toggle.

    Andrew's spec:
    - Net Flows: should show the same number as NNA in the NNA toggle. No tile redesign
      needed once data is fixed -- just verify the mapping is correct.
    - Total Change: REMOVE. Replace with a growth decomposition tile that shows
      total % growth for the period and breaks it down into market % and NNA %.
  </context>

  <fix_1 label="Verify Net Flows tile mapping">
    <description>
      After DS .025 ships and AE re-runs D_04:
      1. Open opalinvest.dev → Asset Overview → GRO toggle
      2. Note the Net Flows value for the latest period (e.g. Q1 2026)
      3. Switch to NNA toggle, same period -- confirm the values match exactly
      4. If they match: no code change needed for this tile (mapping is correct)
      5. If they still diverge after DS .025: investigate whether the frontend
         is reading from a stale cached response. Check React Query key:
         'advisor-intelligence', 'timeseries-overview', firmOverride
         Force a cache bust (hard reload or invalidate the key) and recheck.
      Document result in session log either way.
    </description>
  </fix_1>

  <fix_2 label="Replace Total Change tile with Growth Decomposition tile">
    <description>
      In PartnerAnalytics.tsx, GRO hero metrics block (lines ~1812-1878):

      REMOVE the "Total Change" tile (the third div.flex-col, lines ~1860-1869).

      REPLACE with a "Growth" tile that displays:
        Primary value: latest.total_pct formatted as a percentage (e.g. "+3.2%")
          - Color: green if positive, red if negative (same pattern as other tiles)
        Sub-line 1: "Market: +X.X%" (latest.market_pct)
        Sub-line 2: "NNA: +Y.Y%" (latest.nna_pct)
        Window line: windowLabel (same as other tiles)

      The cumulative aggregate for this tile (across the selected time window):
        Do NOT sum percentage fields -- percentages don't aggregate by summing.
        Instead, compute cumulative total % growth as:
          (aua_end_of_window - aua_start_of_window) / aua_start_of_window * 100
        This requires aua_start of the first period in the window. Use:
          aggregatedGroData[0].period_aua_start (added by DS .025)
        And aua_end of the last period in the window:
          You can get this from augmentedAuaData or from the NNA series end value.
          Alternatively, approximate as:
            aua_start_of_window * (1 + sum(total_pct) / 100)
          which is correct for small percentages but slightly off for large ones.
          Prefer the exact computation using period_aua_start from the first entry.

        For the cum market_pct and cum nna_pct sub-lines:
          cum_market_pct = (sum of market dollar values) / aua_start_of_window * 100
          cum_nna_pct    = (sum of nna dollar values) / aua_start_of_window * 100
          This requires the dollar fields (market, nna) to remain in the data -- they do.

      Tile styling: reuse the same border/background pattern as Market and Net Flows tiles.
      Use GRO.total color token (or define one if it doesn't exist -- check chartColors.ts).
      If no GRO.total token exists, use white/10 background with white/30 border (neutral).

      Label: "Growth" (not "Total Growth" or "Total Change")
    </description>
  </fix_2>

  <type_update label="Update TypeScript types">
    <description>
      In portal/src/pages/AdvisorIntelligence/types.ts, update TimeseriesOverviewGroPeriod:

      Before:
        export interface TimeseriesOverviewGroPeriod {
          period: string
          label: string
          market: number
          nna: number
          total: number
        }

      After:
        export interface TimeseriesOverviewGroPeriod {
          period: string
          label: string
          market: number
          nna: number
          total: number            // dollar AUA change (kept for audit, not displayed)
          total_pct: number        // % total AUA growth for the period
          market_pct: number       // market contribution as % of beginning AUA
          nna_pct: number          // NNA contribution as % of beginning AUA
          period_aua_start: number // beginning AUA for the period (for cum % computation)
        }

      Also update aggregatedGroData useMemo (line ~266) to pass through the new fields:
        .map((p: TimeseriesOverviewGroPeriod) => ({
          period: p.period, label: p.label,
          market: p.market, nna: p.nna, total: p.total,
          total_pct: p.total_pct, market_pct: p.market_pct, nna_pct: p.nna_pct,
          period_aua_start: p.period_aua_start,
        }))
    </description>
  </type_update>

  <validation>
    1. Build portal -- zero TypeScript errors
    2. GRO toggle shows exactly 2 tiles (Market, Net Flows) + 1 new tile (Growth)
       -- Total Change tile is gone
    3. Growth tile shows:
       a. Primary: latest period % growth (e.g. "+3.2%")
       b. Sub-line: Market: +X.X% and NNA: +Y.Y% approximately sum to primary
       c. Cumulative row shows window-aggregate % growth with market/nna breakdown
    4. Net Flows tile value matches NNA toggle value for the same period (cross-check)
    5. comp-transform schema-check PartnerAnalytics -- no new UNUSED fields introduced
    6. Smoke test on opalinvest.dev: switch between QTD/YTD/1Y/3Y windows,
       confirm Growth tile updates correctly for each window
  </validation>

  <acceptance_criteria>
    1. Total Change tile removed
    2. Growth tile present with total_pct primary, market_pct + nna_pct sub-lines
    3. Net Flows value confirmed matching NNA toggle (documented in log)
    4. TypeScript types updated, build clean
    5. All three time granularities (quarterly/monthly/annually) render correctly
  </acceptance_criteria>


  <compiler_tools>
    comp-transform trace PartnerAnalytics
      -- Run BEFORE coding. Shows the full data flow: getTimeseriesOverview() →
         growth_decomposition → aggregatedGroData → JSX. Tells you exactly which
         useMemo chains need to be updated for the new *_pct fields. Faster than
         reading 1,900 lines of PartnerAnalytics.tsx.

    comp-cache key advisor-intelligence timeseries-overview
      -- Confirms the React Query cache key for the timeseries overview fetch.
         Run after adding new fields to ensure the key invalidates correctly when
         the platinum file is updated.

    comp-transform schema-check PartnerAnalytics
      -- Run after changes are committed. Confirms total_pct, market_pct, nna_pct
         are all wired to JSX (not UNUSED). Catches the case where new type fields
         are added but never actually rendered.
  </compiler_tools>

</task_order>
