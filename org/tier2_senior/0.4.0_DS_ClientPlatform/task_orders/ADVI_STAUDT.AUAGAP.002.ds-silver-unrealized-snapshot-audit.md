<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-22-auagap-002-unrealized-audit</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-22</date>
    <status>complete</status><!-- Closed 2026-04-22 — subsumed by full RCA finalization (commits 43c7e5db / bb823bf8 / 214430d8) at data/black_diamond/diagnostics/aua25q_rca.md. Composite root cause confirmed: ANON Schwab RPS partitions + B_00 global persistent-set amplifier. Status drift flip per COO reconciliation. -->
    <project_code>ADVI_STAUDT</project_code>
    <urgency>URGENT — run in parallel with AUAGAP.001 + .003. Andrew watching.</urgency>
  </metadata>

  <objective>
    Snapshot-level AUA reconstruction across key dates spanning Q4 2024 through Q1 2026.
    Tests Hypothesis B: silver/unrealized under-counted lots for Q1-Q3 2025 (B_01 2a69b97e
    snapshot-date keying change may have caused lot loss, or tier-capping capped units).
    Distinguishes price issue (HYP A) vs lot-count issue (HYP B).
    Output: data/black_diamond/diagnostics/aua25q_unrealized_coverage.md
  </objective>

  <context>
    Commit 2a69b97e changed B_01 to key silver/unrealized to snapshot_date (retire stale
    rolling parquet). If 2025 Q1-Q3 snapshots were generated with a partial lot set —
    e.g., closed-before-2025-Q4 filter too aggressive — all clients' AUA would be
    proportionally low. Alternatively, cb6d78e2 confidence-tiered unit-count cap may be
    capping units near-0 for a specific date window.

    DO NOT attempt fixes. Diagnostic only. MCP CTO + COO when smoking gun found.
  </context>

  <spec>
    Source: silver/unrealized/ parquet partitions (S3: s3://opal-data-bd/silver/unrealized/)
    Target snapshot dates (use closest available ≤ each):
      2024-12-31, 2025-02-28, 2025-05-31, 2025-08-31, 2025-11-30, 2026-02-28

    Analysis per snapshot date:
    1. count(distinct lot_id or row) — total lots
    2. sum(units) — total unit count across all positions
    3. sum(market_value) — reported market value
    4. sum(units * canonical_price) — computed value using canonical_prices for that date

    Decision matrix:
    - If sum(market_value) drops but sum(units) is stable → price issue (HYP A, not HYP B)
    - If sum(units) drops → lot loss, unrealized-authoritative filter (HYP B confirmed)
    - If count(distinct account) drops → filter issue (already ruled out by Andrew, sanity check only)

    Also inventory partition dates: list all snapshot_date values present in silver/unrealized/
    for 2025-01-01 through 2025-09-30. If partitions are sparse or missing → data gap root cause.

    Output: data/black_diamond/diagnostics/aua25q_unrealized_coverage.md
    Content: table of (snapshot_date, lot_count, sum_units, sum_market_value,
    sum_computed_value, account_count) for all 6 target dates + partition inventory
    for Q1-Q3 2025. Summary: HYP B CONFIRMED / HYP A MORE LIKELY / INCONCLUSIVE.
  </spec>

  <acceptance_criteria>
    1. 6 target snapshot dates queried (closest available ≤ each target).
    2. Per-snapshot: lot_count, sum_units, sum_market_value, sum_computed_value reported.
    3. Partition inventory: all available snapshot_dates in Q1-Q3 2025 listed.
    4. Decision matrix applied: HYP A vs HYP B ruling per evidence.
    5. Output file committed: data/black_diamond/diagnostics/aua25q_unrealized_coverage.md.
    6. MCP CTO + COO with findings. Include HYP B verdict.
  </acceptance_criteria>

  <do_not>
    <rule>Do NOT attempt fixes. Diagnostic only.</rule>
    <rule>Do NOT run pipeline scripts — S3 query only.</rule>
    <rule>Do NOT wait for AUAGAP.001 or .003 before reporting if sum(units) drop is definitive.</rule>
  </do_not>
</task_order>
