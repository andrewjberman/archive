<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-20-gldpre-002-ds-v3</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-20</date>
    <status>complete</status>
    <project_code>ADVI_GLDPRE</project_code>
  </metadata>

  <objective>
    Fix the AUA total divergence in 06b's firm_mix_views.json. Currently 06b
    computes total_aua by summing units*price from positions_cube independently,
    producing a total that diverges from client_performance by ~$7M. Replace
    06b's independently-computed total with the authoritative total from
    client_performance.parquet. This makes the Mix stacked bar chart in Assets
    Overview show the exact same AUA as the Clients stacked bar chart.
  </objective>

  <context>
    File: data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py

    The portal's Assets Overview panel has two modes:
    - "Clients": stacked bars by NMNC/NMEC. Reads from timeseries_chart.json.
      Source of truth: client_performance.parquet (script 05).
    - "Mix": stacked bars by Equity/FI/Alternatives/Cash. Reads from
      firm_mix_views.json. Source: script 06b.

    Problem: 06b builds firm_daily_new by summing per-position market values
    (lines 648-649: total += mv). This produces a different AUA than script 05
    because of ghost account exclusions, scoped price overrides, and AP active
    gate differences. Result: toggling Clients<->Mix shows bars at different
    heights for the same period.

    Fix: After 06b builds firm_daily_new (which has correct class PERCENTAGES),
    replace each date's 'total' with the client_performance total for that date.
    Then recompute class dollar values as total * class_pct. Cash remains residual.
    The class percentages from positions_cube classification are correct — only
    the denominator (total AUA) needs to come from client_performance.

    compute_period_views() at line 298 is where firm_mix_views.json gets its
    final shape. Line 350 reads total from the daily_dict entry. This is where
    the substitution should happen.
  </context>

  <scope>
    <files>
      <file action="modify">data/black_diamond/scripts/gold/06b_build_client_mix_timeseries.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Load client_performance.parquet in 06b. The script already loads
      positions_cube and accounts_dimension. Add a load of
      gold/client_performance.parquet, aggregate to firm-level daily totals:

        cp = read_parquet('gold/client_performance.parquet')
        cp_daily_total = cp.groupby('date')['total_aua'].sum()

      This gives {date -> firm_total_aua} from the authoritative source.
    </requirement>

    <requirement id="2">
      Pass the cp_daily_total into compute_period_views(). Currently the
      signature is compute_period_views(daily_dict). Add cp_daily_total
      as a second parameter.
    </requirement>

    <requirement id="3">
      In compute_period_views() > _build_granularity(), at line 350 where
      total is read from the daily_dict entry:

      BEFORE:
        total = float(entry.get('total', 0.0))

      AFTER:
        # Use client_performance total (authoritative) instead of
        # positions_cube sum (divergent)
        cp_total = cp_daily_total.get(pd.Timestamp(date_str))
        if cp_total is not None and cp_total > 0:
            total = float(cp_total)
        else:
            total = float(entry.get('total', 0.0))  # fallback

      Then recompute class dollar values from pcts:
        # Class pcts come from positions_cube (correct ratios)
        cube_total = float(entry.get('total', 0.0))
        for ac in _MIX_ASSET_CLASSES:
            pct = float(entry.get(ac, 0.0)) / cube_total if cube_total > 0 else 0.0
            val = round(total * pct, 2)
            row[ac] = {'value': val, 'pct': round(pct, 6)}

        # Cash is residual
        classified_sum = sum(row[ac]['value'] for ac in _MIX_ASSET_CLASSES)
        cash_val = max(0.0, round(total - classified_sum, 2))
        row['cash'] = {'value': cash_val, 'pct': round(cash_val / total, 6) if total > 0 else 0.0}

      This preserves the class ratios from positions_cube but scales them
      to the client_performance total. Cash absorbs any remainder.
    </requirement>

    <requirement id="4">
      The same fix applies to per-advisor and per-relationship mix outputs.
      For per-advisor: use client_performance grouped by relationship_id,
      joined to rel_architect_lookup, then summed per advisor per date.
      For per-relationship: use client_performance filtered to that
      relationship_id per date.

      If this is too complex for a single task order, do firm-level only
      and flag advisor/relationship as a follow-up. Firm-level is the
      priority — that's what Assets Overview reads.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">firm_mix_views.json quarterly[-1].total_aua matches client_performance total_aua sum for the same date (within $1)</criterion>
    <criterion id="2">sum(equity.value + fixed_income.value + alternatives.value + cash.value) == total_aua for every period</criterion>
    <criterion id="3">cash.value >= 0 for every period</criterion>
    <criterion id="4">Script runs without errors with --dry-run</criterion>
    <criterion id="5">Class percentages are unchanged from current positions_cube classification (only the dollar scaling changes)</criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do NOT change the classification logic — WS1 already did that (ETFClassifier)</constraint>
    <constraint>Do NOT change the output shape of firm_mix_views.json — the portal already reads it correctly</constraint>
    <constraint>Cash is ALWAYS residual (total - classified), never independently classified</constraint>
    <constraint>Fallback to positions_cube total if client_performance is missing for a date</constraint>
    <constraint>Commit with --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;"</constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.6.0_AE_PartnerETL" task="GLDPRE.005" status="pending">
      AE is BLOCKED on this commit for Phase 3 (S3 upload) and Phase 4
      (full gold rerun). Commit to CLOUD as soon as ready.
    </dependency>
  </dependencies>

  <deliverables>
    <deliverable type="commit">06b with client_performance total substitution, committed to CLOUD</deliverable>
  </deliverables>
</task_order>
