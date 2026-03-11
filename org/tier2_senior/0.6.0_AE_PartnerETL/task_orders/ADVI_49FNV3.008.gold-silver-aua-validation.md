<task_order>
  <metadata>
    <id>0.4.0_DE_ClientPlatform-2026-03-11-gold-silver-aua-validation</id>
    <issued_by>0.4.0_DE_ClientPlatform</issued_by>
    <issued_to>0.6.0_AE_PartnerETL</issued_to>
    <date>2026-03-11</date>
    <status>pending</status>
    <project>ADVI_49FNV3</project>
  </metadata>

  <objective>
    Add a daily AUA validation step to the gold pipeline that cross-checks the
    positions-cube-derived AUA against the silver allocations parquet for the same date.
    Now that we have daily silver allocation snapshots (opal-data-bd/silver/allocations/
    YYYY-MM-DD.parquet, covering 2026-01-16 to present), we have a ground truth signal
    to validate against on every pipeline run.

    Background: The gold AUA model was originally necessary because historical time series
    could not be reconstructed from BD snapshots alone. We reverse-engineered AUA by
    replaying transactions through the positions cube × canonical prices. Now that daily
    allocations exist, we can validate whether that model is producing correct values.

    A DE investigation on 2026-03-11 found the following for 2026-03-09:
      Gold AUA:   $1,604,943,633  (positions cube × canonical prices)
      Silver AUA: $1,599,225,407  (BD reported market values)
      Raw gap:    +$5,718,227  (0.36%)

    The gap decomposes into two offsetting errors:
      (a) 83 accounts in silver NOT in the gold accounts dimension → missing $14.8M
      (b) Canonical price feed runs ~$20.5M hot vs BD reported prices → gold overcorrects

    These errors cancel to produce a result that looks close to correct but is not.
    A validation step would have caught this immediately.
  </objective>

  <scope>
    <files>
      <file action="create">data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py</file>
      <file action="modify">infra/aws/lambda/bd-pipeline/bd-gold-layer/lambda_function.py</file>
    </files>
  </scope>

  <requirements>
    <requirement id="1">
      Create data/black_diamond/scripts/gold/05c_validate_aua_vs_silver.py.

      This script runs immediately after 05_build_client_performance.py in the pipeline.
      It should:
        1. Determine if a silver allocation parquet exists for today's run date:
           s3://opal-data-bd/silver/allocations/YYYY-MM-DD.parquet
        2. If no silver file exists for that date, skip validation and log:
           "SKIP: No silver allocation for {date} — validation deferred"
        3. If silver file exists, compute:
           a. gold_aua = client_performance[date].total_aua.sum()
           b. silver_aua = silver_alloc.account_market_value.sum()
           c. silver_aua_excl_liabilities = silver_aua excluding account_type IN
              ('CreditCard', 'Mortgage', 'Loans')
           d. gap_abs = gold_aua - silver_aua
           e. gap_pct = gap_abs / silver_aua
        4. Account-level gap decomposition:
           a. accounts_in_silver_not_in_gold: account_ids in silver but not in
              gold/accounts_dimension_latest.parquet — report count + total MV
           b. price_divergence_estimate = gap_abs - accounts_missing_mv
        5. Write validation result to:
           s3://opal-data-bd/gold/validation/aua_validation_{YYYY-MM-DD}.json
           Schema:
           {
             "date": "YYYY-MM-DD",
             "gold_aua": float,
             "silver_aua": float,
             "silver_aua_excl_liabilities": float,
             "gap_abs": float,
             "gap_pct": float,
             "accounts_missing_from_gold": int,
             "accounts_missing_mv": float,
             "price_divergence_estimate": float,
             "status": "PASS" | "WARN" | "FAIL",
             "liability_types_in_silver": {
               "CreditCard": {"count": int, "mv": float},
               "Mortgage":   {"count": int, "mv": float},
               "Loans":      {"count": int, "mv": float},
               "Insurance":  {"count": int, "mv": float},
               "TermLife":   {"count": int, "mv": float},
               "Annuity":    {"count": int, "mv": float}
             }
           }
        6. Thresholds:
           PASS: abs(gap_pct) &lt;= 0.5%  AND  accounts_missing_from_gold &lt;= 10
           WARN: abs(gap_pct) &lt;= 1.0%  OR   accounts_missing_from_gold &lt;= 50
           FAIL: abs(gap_pct) &gt; 1.0%   OR   accounts_missing_from_gold &gt; 50
        7. On FAIL: log the full decomposition at ERROR level. Do NOT halt the pipeline
           (gold data is still published). The FAIL is a signal for investigation, not
           a hard stop.
    </requirement>

    <requirement id="2">
      Wire 05c into bd-gold-layer/lambda_function.py after the step that runs
      05_build_client_performance.py (and 05b if present). The validation step must
      run before 09_generate_partner_analytics.py so that a FAIL is visible in logs
      before the portal JSON is published.

      Add a pipeline step entry with the same S3-artifact pattern as other steps:
        Step label: "05c: validate AUA vs silver"
        Script: 05c_validate_aua_vs_silver.py
        On SKIP: continue (no silver file)
        On PASS/WARN: continue
        On FAIL: continue but emit a CloudWatch metric or structured log that
                 can be alarmed on separately
    </requirement>

    <requirement id="3">
      Backfill: after wiring, run 05c against all 35 existing silver allocation dates
      (2026-01-16 through 2026-03-09) to establish a baseline validation history.
      Output one JSON per date to gold/validation/.

      Document the trend: is the gap stable, growing, or shrinking? Are the same
      accounts consistently missing from gold?
    </requirement>

    <requirement id="4">
      Investigate and resolve the two root causes identified in the 2026-03-11 analysis:
        (a) 83 accounts present in silver but absent from gold/accounts_dimension:
            - Most are IRA (24 accounts, $4.0M) and "No Account Type Assigned" (7, $4.2M)
            - Identify why they are missing (never had transactions? pre-history accounts?
              BD export gap?) and fix the accounts dimension builder if appropriate.
        (b) Canonical price divergence (~$20.5M hot vs BD prices):
            - Identify which assets/asset classes drive the largest price deltas
            - Determine if canonical prices are stale, use wrong source, or apply
              different rounding than BD
            - Note: DO NOT change canonical prices if they are intentionally different
              (e.g., using market close vs BD's intraday). Document the methodology
              difference if that is the case.

      These are separate root causes. Fix (a) if tractable. Document (b) regardless.
    </requirement>
  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      05c_validate_aua_vs_silver.py runs cleanly on 2026-03-09 silver data and
      writes gold/validation/aua_validation_2026-03-09.json with correct values
    </criterion>
    <criterion id="2">
      Pipeline log shows "PASS", "WARN", or "FAIL" with gap_pct and
      accounts_missing_from_gold for every run where silver exists
    </criterion>
    <criterion id="3">
      35-date backfill complete — gold/validation/ has one JSON per silver date
    </criterion>
    <criterion id="4">
      Root cause (a) documented — missing accounts explained and fix proposed or applied
    </criterion>
    <criterion id="5">
      Root cause (b) documented — price divergence methodology difference explained
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>Do not halt the pipeline on FAIL — validation is observational, not a gate</constraint>
    <constraint>05c reads client_performance from S3, not from a local temp file — must be runnable standalone</constraint>
    <constraint>Exclude liabilities (CreditCard, Mortgage, Loans) from the primary gap metric but report them separately — they are valid BD accounts but may not belong in AUA</constraint>
    <constraint>Script must handle dates where no silver allocation exists gracefully (SKIP, not error)</constraint>
  </constraints>

  <context>
    Silver allocations available: s3://opal-data-bd/silver/allocations/YYYY-MM-DD.parquet
    Date range: 2026-01-16 to present (35 files as of 2026-03-11), daily cadence
    Gold client performance: s3://opal-data-bd/gold/client_performance.parquet
    Gold accounts dimension: s3://opal-data-bd/gold/accounts_dimension_latest.parquet

    Known baseline (2026-03-09):
      gold_aua:                    $1,604,943,633
      silver_aua:                  $1,599,225,407
      gap_abs:                     +$5,718,227 (0.36%)
      accounts_missing_from_gold:  83 accounts, $14,797,306 MV
      price_divergence_estimate:   ~$20,515,533
      status: WARN (gap within 1%, but 83 missing accounts exceeds PASS threshold)
  </context>

  <deliverables>
    <deliverable type="commit">05c_validate_aua_vs_silver.py — new validation script</deliverable>
    <deliverable type="commit">bd-gold-layer/lambda_function.py — 05c wired into pipeline</deliverable>
    <deliverable type="document">Session log with backfill results, root cause analysis for (a) and (b)</deliverable>
    <deliverable type="data">35 JSON files in s3://opal-data-bd/gold/validation/</deliverable>
  </deliverables>
</task_order>
