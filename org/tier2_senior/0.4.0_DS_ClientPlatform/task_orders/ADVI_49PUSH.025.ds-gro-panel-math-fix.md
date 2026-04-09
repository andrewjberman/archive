<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-025-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~D</issued_to>
    <date>2026-04-09</date>
    <status>in_progress</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>6</wave>
    <phase>P3 data correctness</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Fix confirmed critical data errors in the GRO toggle of the Asset Overview header panel,
    and replace the "Total Change" metric with a percentage-based AUA growth decomposition.
    All changes are in D_00.portal_aggregates.py and D_04.client_portal_summary.py.
    DE .026 is the companion frontend TO and depends on this one completing first.
  </objective>

  <context>
    The GRO toggle in PartnerAnalytics.tsx reads from
    platinum/firm/timeseries_overview.json → growth_decomposition[granularity].
    Each period entry is: { period, label, market, nna, total }.

    Andrew QA'd the panel and found three issues:
    1. Market -- CONFIRMED WRONG. Portal shows ~$79M market growth for Q1 2026.
       Opal manages ~85% of 49F holdings and aggregate performance was ~0.02% flat for Q1.
       True market appreciation on ~$1.4B managed AUA at 0.02% = ~$280K.
       The $79M figure is off by ~$78.7M -- this is not a rounding error, it is a
       fundamental calculation error.
    2. Net Flows -- CONFIRMED WRONG. Should equal the NNA toggle value for the same period.
    3. Total Change -- wrong concept. Replace with % growth decomposition.

    ROOT CAUSE (Market error -- multi-hypothesis, DS must determine which applies):

    D_00 reads account_performance (C_03) and maps the 'growth' column to 'market_growth'.
    C_03 schema:
      growth       = price_return + realized_gl + income  (true investment return)
      aua_residual = AUA_change - growth                  (accounting corrections, NOT NNA)
      total_aua    = canonical AUA from 08 account_ledger (includes aua_residual in the balance)

    D_00 growth decomposition (lines 1414-1458 of portal_aggregates.py):
      has_decomposition = True when account_performance loads successfully (expected in prod)
      market = sum(market_growth) = sum(growth column) for the month
      nna_net = nna_end - nna_start (diff of cumulative account_performance.nna = cum_inflows - cum_outflows)
      total_chg = aua_end - aua_start (period change in total_aua)

    CRITICAL: aua_residual is accounting flows -- reconciliation corrections, transfer
    adjustments, opening balance entries -- that affect AUA but are NOT:
      - True investment return (market appreciation/depreciation)
      - True client money flows (NNA)
    Andrew has confirmed: aua_residual must never be wrapped into market or NNA figures.

    The AUA identity is:
      total_aua_change = market_growth + nna_net + aua_residual_delta
    NOT:
      total_aua_change = market_growth + nna_net

    D_00 currently sets total = total_chg = aua_end - aua_start, which INCLUDES aua_residual.
    The growth_decomposition therefore violates the identity: total != market + nna unless
    aua_residual_delta = 0, which is not guaranteed.

    Three possible explanations for the $79M market figure, in order of likelihood:

    HYPOTHESIS A (most likely): C_03's 'growth' column (from 08 account_ledger) incorrectly
    includes aua_residual in the growth figure. i.e., 08 computes growth as
    AUA_change - net_flows (treating everything that's not a flow as "growth"),
    which bundles reconciliation items into price return. If aua_residual was +$78.7M
    for Q1, growth would show ~$79M even with ~0.02% true performance (~$280K).
    To test: compare sum(growth) to sum(aua_residual) across all accounts for Q1.
    If growth >> expected market return AND growth ≈ growth_clean + aua_residual,
    this hypothesis is confirmed.

    HYPOTHESIS B: has_decomposition = False in production (account_performance didn't load,
    fell back to client_performance which lacks the growth column). Then:
    market = total_chg - nna_net (residual), and the nna_net is understated by ~$79M
    vs the NNA toggle, causing market to absorb the gap.
    To test: check D_00 log for the FALLBACK message. If present, this is the active path.

    HYPOTHESIS C: has_decomposition = True, growth column is clean (~$280K for Q1), but
    the portal is reading a stale cached timeseries_overview.json from before C_06 was fixed,
    and the stale file had wrong data. To test: check generated_at timestamp on the file.
    If older than today's AE re-run, force a fresh D_04 run and recheck.

    Fix_1 below requires DS to determine which hypothesis is active and fix accordingly.

    Full data lineage:
      account_performance (C_03) → D_00 builds growth_decomposition.data (monthly)
        → timeseries_chart.json → D_04 reads + aggregates to q/m/y
        → timeseries_overview.json → growth_decomposition[granularity]

    Parallel NNA path (what the NNA toggle actually shows):
      timeseries_chart.json → nna.data (cumulative Inflows/Outflows daily series)
        → D_04._aggregate_nna_to_periods() → timeseries_overview.json → nna[granularity]
        → each period: { inflow, outflow, net }
        → frontend renders .net as the NNA toggle value
  </context>

  <fix_1 label="Diagnose market lineage -- determine active hypothesis and fix">
    <description>
      REQUIRED DIAGNOSIS -- do not skip. Work through the three hypotheses in order.

      Step 1: Confirm has_decomposition status.
        Read the account_performance.parquet column list from S3 (latest gold run).
        Check for presence of 'growth' column. Also check D_00 log for FALLBACK message.

        If FALLBACK active (Hypothesis B):
          NNA fix (fix_2) is the sole fix needed for market. After fix_2 corrects nna_net,
          market = total_chg - corrected_nna_net will land near the expected ~$280K.
          Verify after fix_2.

        If has_decomposition = True (account_performance loaded successfully):
          Proceed to Step 2.

      Step 2: Test Hypothesis A -- is growth column contaminated by aua_residual?
        Query account_performance.parquet for Q1 2026 (2026-01-01 to 2026-03-31):
          total_growth = sum(growth)
          total_aua_residual = sum(aua_residual)
        Compare:
          total_growth expected from performance: ~0.02% × $1.4B managed AUA ≈ $280K
          If total_growth >> $280K AND total_growth ≈ $280K + total_aua_residual:
            Hypothesis A confirmed. Fix: market must use 'growth' MINUS 'aua_residual'.
            In D_00 (line 865), change:
              market_growth=('growth', 'sum')
            to:
              market_growth=('growth', 'sum'),
              aua_residual_sum=('aua_residual', 'sum')
            Then in the growth_data loop, strip residual from market:
              market = float(grp_sorted['market_growth'].sum()) - float(grp_sorted['aua_residual_sum'].sum())
            And add aua_residual_delta as its own field in growth_data (see fix_3b below).

        If total_growth ≈ $280K (clean), Hypothesis A is ruled out.
        Proceed to Step 3.

      Step 3: Test Hypothesis C -- stale cached file.
        Check platinum/firm/timeseries_overview.json on S3: read generated_at field.
        If older than the latest AE gold run timestamp, request AE to re-run D_04.
        After fresh run, check market value again.

      Document all three hypothesis test results in session log.
      Post findings to CTO inbox before committing any fix to D_00.
    </description>
  </fix_1>

  <fix_3b label="Add aua_residual_delta to growth_decomposition (if Hypothesis A confirmed)">
    <description>
      If Hypothesis A is confirmed (growth column includes aua_residual), the corrected
      growth_decomposition must:
        1. Strip aua_residual from market: market = sum(growth) - sum(aua_residual)
        2. Add aua_residual_delta as a first-class field in each period entry:
           aua_residual_delta = aua_residual_end - aua_residual_start (same diff pattern as nna_net)
           This represents accounting flows for the period -- NOT to be shown in the portal
           but preserved in the data for audit trail and to ensure the identity holds:
             total_chg == market + nna_net + aua_residual_delta  (within rounding)
        3. Redefine 'total' in growth_decomposition to be market + nna_net ONLY
           (the economic story, excluding accounting flows).
           Rename field to 'economic_total' to make the exclusion explicit.

      Note: if Hypothesis A is NOT confirmed, skip fix_3b. Do NOT add aua_residual_delta
      unless the diagnosis confirms it is currently contaminating the market figure.

      The GRO panel in the portal should ONLY display economic figures:
        Market (true investment return)
        NNA (true client flows)
        Growth % decomposition (based on economic_total / aua_start)
      aua_residual_delta is audit-only -- never display in the portal.
    </description>
  </fix_3b>

  <fix_2 label="Fix NNA mismatch -- align growth_decomposition.nna with NNA toggle">
    <description>
      Root cause: growth_decomposition.nna and nna[granularity].net are computed from
      different source paths and diverge in practice.

      - D_00 computes nna_net = nna_end - nna_start from account_performance.nna
        (cumulative net). This is the nna field in growth_decomposition.data.
      - D_04._aggregate_nna_to_periods diffs timeseries_chart.nna.data Inflows/Outflows
        separately, producing period .net = period_inflow - period_outflow.

      The frontend NNA toggle renders nna[granularity].net.
      The GRO tile renders growth_decomposition[granularity].nna.
      Andrew confirmed these show different numbers for the same period.

      Fix in D_04.build_timeseries_overview():
        After computing both nna_periods and growth_periods, build a lookup:
          nna_lookup = { p['period']: p['net'] for p in nna_periods['monthly'] }
        Then replace the 'nna' field in each monthly growth_decomposition entry:
          for entry in gro_raw_aggregated['monthly']:
              entry['nna'] = nna_lookup.get(entry['period'], entry['nna'])
        Apply the same logic when aggregating to quarterly/annually in
        _aggregate_growth_to_periods: use the NNA-aligned monthly values as input,
        not the original D_00 growth_decomposition.nna values.

      This guarantees the GRO panel NNA = NNA toggle NNA for every period and granularity.

      Verify: after fix, spot-check 3 quarters and confirm growth_decomposition[q].nna
      exactly equals nna[q].net for the same period key.
    </description>
  </fix_2>

  <fix_3 label="Replace total with percentage growth decomposition">
    <description>
      Andrew: "Total Change" (dollar AUA change per period) should be removed.
      Replace with a decomposition of AUA growth rate into market and NNA contributions,
      both expressed as a percentage of beginning-of-period AUA (aua_start).

      New fields to add to each growth_decomposition period entry:
        total_pct:  (aua_end - aua_start) / aua_start * 100   -- total % growth for the period
        market_pct: market / aua_start * 100                   -- market contribution to growth %
        nna_pct:    nna_net / aua_start * 100                  -- NNA contribution to growth %

      Note: market_pct + nna_pct should approximately equal total_pct (up to synthetic/churn
      residuals if the decomposition columns exist). Document any residual.

      Where to compute:
        D_00 already has aua_start per monthly period (line 1435-1436 of portal_aggregates.py).
        Add total_pct, market_pct, nna_pct to each monthly entry in growth_data
        (alongside the existing market, nna, total fields -- do not remove the dollar fields yet,
        DE will switch the frontend in .026 and the dollar fields can be dropped once DE confirms
        the frontend no longer references them).

      D_04._aggregate_growth_to_periods must also sum and aggregate these new fields:
        - When aggregating to quarterly/annually, DO NOT sum the percentage fields directly.
          Recompute them from the summed dollar fields and the period's aua_start
          (which is the aua_start of the FIRST monthly period in the bucket).
        - Add a period_aua_start field to the monthly entries so D_04 can retrieve it during
          aggregation. Alternatively, D_04 can compute aua_start from the AUA cumulative series
          (aua[granularity][period-1].end_value).

      Acceptance: for each period in timeseries_overview.json growth_decomposition,
        total_pct, market_pct, nna_pct are present and non-null.
        market_pct + nna_pct ~= total_pct within 1 percentage point (residual tolerance).
    </description>
  </fix_3>

  <deliverables>
    1. Session log documenting market lineage findings (fix_1)
    2. D_00.portal_aggregates.py -- add period_aua_start, total_pct, market_pct, nna_pct
       to growth_data entries
    3. D_04.client_portal_summary.py -- _aggregate_growth_to_periods updated to:
       a. Accept and propagate period_aua_start through aggregation
       b. Recompute *_pct fields at each granularity level
       c. Align nna field from NNA-period lookup (fix_2)
    4. timeseries_overview.json schema change: each growth_decomposition period now has
       { period, label, market, nna, total, total_pct, market_pct, nna_pct, period_aua_start }
    5. Spot-check validation: 3 quarters confirmed, NNA matches NNA toggle,
       pct fields sum correctly
  </deliverables>

  <acceptance_criteria>
    1. growth_decomposition[q].nna == nna[q].net for every matching period key (all granularities)
    2. Each growth_decomposition period entry has total_pct, market_pct, nna_pct fields
    3. market_pct + nna_pct within 1pp of total_pct for every period
    4. Dollar fields (market, nna, total) still present in output (DE .026 removes from UI,
       not from data -- preserve for audit trail)
    5. Market lineage documented: active hypothesis identified, Q1 2026 market value after
       fix is consistent with ~0.02% performance (~$280K-$500K, not $79M). aua_residual
       is fully isolated from all displayed figures (market, nna, growth %). Findings
       posted to CTO inbox before any D_00 commit.
  </acceptance_criteria>


  <compiler_tools>
    Run these BEFORE investigating to map data paths without manual grepping:

    comp-platinum reverse platinum/firm/timeseries_overview.json
      -- Full back-trace: platinum file → D_04 → D_00 → account_performance → C_03.
         Shows the exact chain feeding the GRO panel. Replaces manually chasing imports.

    comp-pipescript io D_00
      -- Confirms D_00's full read/write manifest. Shows which column from which parquet
         feeds into growth_decomposition. Run once, stops the "where does nna come from"
         hunt cold.

    comp-pipescript io D_04
      -- Shows D_04's build_timeseries_overview inputs. Confirms TIMESERIES_CHART and
         which other artifacts feed into growth_decomposition aggregation.

    comp-blast gold/views/mix_daily_summary.json
      -- After C_06 fix: shows all downstream scripts consuming mix_daily_summary.
         Confirms D_03 and D_04 are both in the blast radius and will pick up the fix.
  </compiler_tools>

</task_order>
