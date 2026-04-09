<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-04-09-49push-044-ds</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <date>2026-04-09</date>
    <status>complete</status>
    <project_code>ADVI_49PUSH</project_code>
    <wave>11</wave>
    <phase>Books tab data correctness</phase>
    <mcp_identity>Register with MCP as "0.4.0_DS_ClientPlatform" before starting.</mcp_identity>
  </metadata>

  <objective>
    Investigate and fix the asset class value discrepancy between the Books tab
    "Firm Overview" donut and the Assets Overview header panel. Both show current
    firm-level asset class breakdown but produce different numbers for the same date.
    The canonical logic must be the same source for both.
  </objective>

  <context>
    Observed discrepancy (2026-04-09):
      Fixed Income:  Firm Overview = $315M   vs  Assets Overview = $361M   (~$46M gap)
      Equity:        Firm Overview = $1.22B  vs  Assets Overview = $1.19B  (~$30M gap)

    Root cause hypothesis: the two panels read from different data paths.

    Assets Overview header (correct post C_06 fix):
      platinum/firm/timeseries_overview.json → mix[granularity]
      source chain: C_06 (classify_series, now fixed) → mix_daily_summary.json
                    → D_03 (firm_mix_views.json) → D_04

    Firm Overview donut (suspect):
      platinum/firm/mix_summary.json
      source chain: D_03 builds firm_composition.json from FIRM_COMPOSITION
                    (external/silver) OR from holdings_lots + ETFClassifier directly
                    → D_04 mix_summary.json

    D_03 reads TWO sources:
      FIRM_COMPOSITION: gold/views/firm_composition.json (external/silver writer)
      MIX_DAILY_SUMMARY: gold/views/mix_daily_summary.json (C_06)

    The donut uses the silver firm_composition path which bypasses C_06 entirely.
    The silver writer uses a different classification logic or different holdings snapshot
    than C_06, producing the ~$46M fixed income gap.
  </context>

  <investigation>
    Step 1: Confirm the source for mix_summary.json (donut).
      In D_03, find where mix_summary or firm_composition is built.
      Confirm which input it reads for the asset class snapshot.

    Step 2: Confirm the source for timeseries_overview.json mix (header).
      Confirmed as C_06 → mix_daily_summary.json → firm_mix_views.json.
      Verify the most recent period entry (current quarter) aligns with today's
      canonical_holdings using the ETFClassifier.

    Step 3: Identify what firm_composition.json (silver) uses for classification.
      Does it use the same ETFClassifier as C_06?
      Does it use the same holdings universe (canonical_holdings vs holdings_lots)?
      Does it apply the same filters (AP gate, relationship filter, market_value > 0)?

    Step 4: Quantify the discrepancy.
      For the most recent date, compare:
        sum(fixed_income) from mix_summary.json
        sum(fixed_income) from timeseries_overview.json current period
      Confirm the gap is exactly the numbers Andrew observed ($46M FI, -$30M equity).
  </investigation>

  <fix>
    The fix must make the Firm Overview donut use the SAME canonical classification
    logic as the Assets Overview header. Two options in preference order:

    OPTION A (preferred): Have D_04's mix_summary publisher read directly from
    mix_daily_summary.json (C_06 output, ETFClassifier-based) for the current period's
    snapshot, instead of from firm_composition.json (silver). This ensures both surfaces
    use identical classification. No change to C_06 or D_03 needed.

    OPTION B: Have D_03 rebuild firm_composition.json using ETFClassifier + canonical_holdings
    (same pipeline as C_06), replacing the silver writer's output. More invasive -- only
    pursue if Option A is not viable.

    Whichever option: after the fix, verify:
      mix_summary.json fixed_income = timeseries_overview.json current period fixed_income
      Within $1M tolerance (rounding/timing differences acceptable; $46M is not).
  </fix>

  <acceptance_criteria>
    1. Firm Overview donut fixed income matches Assets Overview header fixed income
       within $1M for the current period
    2. Same for equity and all other asset classes
    3. Source of truth documented: both panels confirmed to use C_06 classification
    4. Session log: root cause confirmed, option chosen, pre/post values recorded
  </acceptance_criteria>


  <compiler_tools>
    comp-platinum reverse platinum/firm/mix_summary.json
      -- The single most useful command here. Traces mix_summary.json back through
         D_04 → D_03 → source. Immediately shows whether the donut reads from
         firm_composition.json (silver) or mix_daily_summary.json (C_06).
         This is the hypothesis-confirming tool -- run it first.

    comp-platinum reverse platinum/firm/timeseries_overview.json
      -- Run in parallel with the above to see the header's path.
         Comparing the two back-traces reveals exactly where the two paths diverge.
         The divergence point is the fix target.

    comp-pipescript io D_03
      -- Shows all inputs D_03 reads for firm_composition vs mix paths.
         Confirms which source each downstream artifact uses.
  </compiler_tools>

</task_order>
