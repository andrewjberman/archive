# ADVI_GLDOPS.003 — DS: Market Growth Accuracy Diagnostic

<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-04-03-gldops-003-ds</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-04-03</date>
    <status>complete</status>
    <priority>P1</priority>
    <project_code>ADVI_GLDOPS</project_code>
  </metadata>

  <objective>
    Investigate why portal GRO shows ~1% market growth for 2025 when actual
    49Financial portfolio returns were 10-12%. Quantify the gap, isolate the
    cause(s), and recommend the fix. This is the big analytical lift.
  </objective>

  <references>
    <ref type="prd">docs/architecture/ADVI_GLDOPS_PRD.md (WS2 section)</ref>
  </references>

  <context>
    The portal GRO decomposition is computed by bd-portal-publisher Lambda
    (lines 886-927) using: `market = delta(AUA) - delta(NNA)`. It reads
    `total_aua` and `nna` from `gold/client_performance.parquet`, produced by
    script 05 (`05_build_client_performance.py`).

    Script 05 now computes (after your GLDRST.017 work, commit 7fa6947d):
    `market_growth = delta(total_aua) - delta(nna) - delta(synthetic_aua)`

    But the publisher still computes its own monthly aggregation from raw columns,
    ignoring synthetic_correction.

    Four hypotheses in priority order:
    A. Silver AUA override clips gold AUA gains (SILVER_OVERRIDE_ENABLED = True,
       OVERRIDE_THRESHOLD = 0.20, lines 123-124 of script 05)
    B. NNA inflated by misclassified transaction types (dividends, rebalances, fees)
    C. Price carry-forward suppresses AUA growth for sparse-priced assets
    D. Dollar residual formula is fundamentally insufficient (need TWR)

    Fix A/B/C first. If gap remains, D becomes necessary.
  </context>

  <deliverables>
    **Phase 1 — Quantify the gap** (can run against existing gold output on S3):

    1. For firm 49Financial, compute 2025 year-over-year:
       - Starting AUA (2025-01-02), ending AUA (2025-12-31)
       - Cumulative NNA at start and end
       - `market_dollars = (end_AUA - start_AUA) - (end_NNA - start_NNA)`
       - `market_pct = market_dollars / start_AUA`
       - Expected: ~10-12%. Actual: ~1%.

    2. Same calculation for top 10 relationships by AUA — which ones are worst?

    3. Gold AUA vs silver AUA comparison for 2025-12-31:
       How many accounts had override applied? What was the aggregate override
       impact (sum of gold_aua - silver_aua for overridden accounts)?

    **Phase 2 — Isolate the cause** (diagnostic scripts, no deploy):

    1. **Silver override impact**: Using existing gold data, compute what
       market_growth would be WITHOUT the override. Two approaches:
       a. Read the `_override_count` column if it exists in client_performance
       b. Or: compute gold AUA from positions * canonical_prices directly,
          compare to the overridden total_aua column

       If disabling the override accounts for most of the 9-11pp gap, that's
       the primary cause.

    2. **NNA audit**: For top 10 relationships, pull raw BD transaction detail.
       Categorize by transaction type. Flag any types that should NOT be counted
       as cash flows: dividend reinvestments, internal rebalance transfers, fee
       payments. Quantify how much these inflate cumulative NNA.

    3. **Price coverage**: For 2025-12-31, what % of total AUA has same-day
       canonical prices vs carry-forward? If >20% of AUA is on stale prices,
       that suppresses market growth.

    **Phase 3 — Recommend fix** (written analysis, no code change yet):

    Based on Phase 1-2 findings, recommend one of:
    - Disable silver override (or raise threshold / switch to soft damping)
    - Filter NNA transaction types
    - Improve canonical price coverage
    - Implement TWR methodology
    - Combination of the above

    Include publisher alignment recommendation: should publisher read
    pre-aggregated `market_growth` column from script 05 output instead of
    recomputing its own monthly aggregation?

    **Output**: Write findings to your session log. COO will use findings to
    issue the fix task order (separate TO).
  </deliverables>

  <dependencies>
    None -- this diagnostic reads existing gold data on S3. Independent of WS1.
    Do .002 (pending marker fix) first since it is P0, then start this.
  </dependencies>
</task_order>
