<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFNNA.SILVER</id>
    <project>ADVI_INFNNA</project>
    <title>Silver builds for tax + performance + billing + assets_v2 + positions_daily over historical date range</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>active</status>
    <priority>high</priority>
    <estimated_effort>~1h once bronze streams complete</estimated_effort>
  </metadata>

  <references>
    <ref type="incident">INFNNA.001 root cause RAVC2 — Joe Brandenburg rep_id=6 missing from bronze pull, accounts_v2 silver missing rep_id filter, canonical_nna stale under old IWM-aggregated attribution</ref>
    <ref type="bronze_streams">COO-local 8 streams launched 17:51Z 2026-05-07: tax+perf, billing, assets_v2, positions_daily (all per-date over 2020-03-11 → 2026-05-05); transactions full-history + new_portfolio + reps complete</ref>
    <ref type="silver_builders">data/orion/scripts/silver/convert_orion_api_to_silver.py + run_silver_backfill_parallel.py + build_billing_dim.py + build_tax_dim.py</ref>
    <ref type="completed_silvers">transactions (1.15M rows), accounts_v2 (848 rows / $203.2M filtered), representatives (18 rows) — all for snapshot 2026-05-07</ref>
  </references>

  <context>
    Bronze streams running locally on Andrew's machine fill historical gaps in tax, performance,
    billing, assets_v2, and positions_daily over the 2020-03-11 → 2026-05-05 range. As each
    bronze stream completes (or as bronze parquets/CSVs land), corresponding silver builds
    must run to produce the per-date silver/api_dims/* parquets that downstream gold scripts
    (canonical_nna, INF_D_*) consume.

    The transactions silver and accounts_v2 silver are already done for snapshot 2026-05-07.
    Per-date historical silvers for the other dims are the immediate next step. Without these,
    the gold canonical_nna rebuild (INFNNA.GOLD TO) cannot run end-to-end with corrected
    historical attribution.
  </context>

  <scope>
    <step>
      Wait for bronze streams to complete (status visible via .runtmp/logs/full_backfill_*.log).
      Streams A (tax+perf) ETA ~3h, B (billing) ETA ~2.4h, C+D (assets/positions) ~12h.
      Silver builds can begin per-stream as each completes — no need to wait for all 4.
    </step>
    <step>
      For each completed bronze stream, run the corresponding silver builder for ALL dates
      that have new bronze data (use S3 listing to identify the date set):

      tax:
        for date in dates_with_new_bronze:
          INF_PREFER_S3=true python data/orion/scripts/silver/convert_orion_api_to_silver.py \
            --dim tax --snapshot-date {date} --upload
        OR use build_tax_dim.py if that's the canonical builder. Confirm by reading the file
        header for current canonical pattern.

      performance:
        same pattern with --dim performance

      billing:
        same pattern with --dim billing
        (or build_billing_dim.py if v1.7.31+ canonical pattern preferred)

      assets_v2:
        run_silver_backfill_parallel.py --dims assets_v2 --start 2020-03-11 --end 2026-05-05
        (handles parallelism internally)

      positions_daily:
        run_silver_backfill_parallel.py --dims positions_mv --start 2020-03-11 --end 2026-05-05
    </step>
    <step>
      Apply INFLECTION_REP_IDS filter where missing. Per INFNNA.001 root cause, accounts_v2
      silver was previously letting through all custodian-matched accounts (2,215 rows /
      $476.9M) instead of just the 4 advisors (848 rows / $203.2M). Audit each silver
      builder's filter logic — if any other dim is missing the {3,6,11,12} filter, add it
      mirroring the accounts_v2 pattern just landed by COO.
    </step>
    <step>
      For each silver build, verify Guard B passes (INFGRD AUA sanity check). Guards may
      need recalibration per INFNNA.GUARDS-AUDIT TO; coordinate with that scope.
    </step>
    <step>
      RAVC1 (incremental): on each completed dim's silver build, RAVC with row counts +
      total AUA + S3 path verification.
    </step>
    <step>
      RAVC2 (final): all 5 per-date dims have silver coverage from 2020-03-11 → 2026-05-05.
      Provide summary table (dim, date count, total rows, total AUA, S3 prefix).
    </step>
  </scope>

  <acceptance_criteria>
    <criterion id="AC1">tax silver: per-date parquets at silver/api_dims/tax/snapshot_date={date}/data.parquet for all dates with new bronze, scoped to INFLECTION_REP_IDS {3,6,11,12}.</criterion>
    <criterion id="AC2">performance silver: per-date parquets, INFLECTION_REP_IDS scoped.</criterion>
    <criterion id="AC3">billing silver: per-month parquets at silver/api_dims/billing/.</criterion>
    <criterion id="AC4">assets_v2 silver: per-date parquets at silver/api_dims/accounts_v2/ scoped to INFLECTION_REP_IDS.</criterion>
    <criterion id="AC5">positions_daily silver: per-date parquets.</criterion>
    <criterion id="AC6">No Guard B FAIL on any silver build (or Guard B thresholds updated per INFNNA.GUARDS-AUDIT).</criterion>
    <criterion id="AC7">Sanity check: tax silver totals roll up to ~$203M for recent dates (within 3% of accounts_v2).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>Bronze streams (COO-local) must complete or be in flight. Silver builds run incrementally as bronze lands.</upstream>
    <downstream>INFNNA.GOLD (canonical_nna rebuild) requires this TO to complete for the date range it covers.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Begin incremental silver builds as each bronze stream completes. RAVC per-dim, not blocked on full set.</message>
  </go_signal>
</task_order>
