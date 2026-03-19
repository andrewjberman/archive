# Task Order: ACAT Parameter Grid v2 — Gold Baseline Fix and Rerun — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-acat-param-grid-v2-gold-baseline</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH — CEO-directed. Supersedes parameter grid run 1 which was degenerate.</priority>
    <supersedes>acat-inkind-parameter-optimization.md (grid design) — keep for reference</supersedes>
  </metadata>

  <!-- ================================================================ -->
  <!-- SECTION 1 — WHAT WE WERE ATTEMPTING                              -->
  <!-- ================================================================ -->
  <background id="1" title="What We Were Attempting">
    The ACAT in-kind diagnostic (Phase 3, 2026-03-05) confirmed that 867 accounts show
    genuine ACAT in-kind transfer signals, representing ~$46M of NNA inflows that our
    transaction-based pipeline misses. The methodology: for each account's first 30 days,
    buys that cannot be explained by cash inflows or sell proceeds are attributed to
    positions that arrived via in-kind ACAT transfer — a flow Schwab counts as TOA NNA
    but BD's transaction feed does not capture.

    The Phase 3 default parameters (ONBOARDING_DAYS=30, BURST_THRESHOLD=3) were chosen
    by inspection. January 2025 showed a $72.6M overshoot in a single month, suggesting
    the parameters may not be optimal. Schwab publishes official monthly NNA figures for
    13 months (May 2024 - May 2025), giving us a ground truth series to optimize against.

    The goal of the parameter grid was: run all 24 combinations of (ONBOARDING_DAYS, BURST_THRESHOLD)
    against Schwab's official monthly NNA, compute Pearson correlation and 6 other metrics
    per combination, and identify the parameter set that maximizes alignment with Schwab's
    reported figures before committing to production implementation.
  </background>

  <!-- ================================================================ -->
  <!-- SECTION 2 — WHERE IT BROKE AND WHY                              -->
  <!-- ================================================================ -->
  <postmortem id="2" title="Where It Broke and Why">
    DT ran diag_acat_param_grid.py on i-01003b035d2988dfb. Script executed in ~8 minutes.
    All 33 parameter combinations returned flat Pearson r ≈ 0.088. Degenerate — no
    combination produced a meaningful correlation signal.

    Root cause: compute_baseline_nna_by_month() derived the baseline from raw
    silver/transactions without the production-grade caps that script 05 applies.

    The production script 05 applies three guard layers before computing NNA:
      Layer 1: $50M per-event clip (prevents single garbage transactions)
      Layer 2: AUA-based daily outflow cap per relationship (prevents phantom outflows
               from mispriced positions — catches Relationship "0", $345M lifetime)
      Layer 3: 90-day velocity cap (prevents sustained churn from inflating outflows)

    Without these caps, the raw silver baseline computes to approximately -$15B over
    13 months. Schwab's ground truth is +$353M. The ACAT adjustment ($50-100M depending
    on parameters) is 150× smaller than the uncapped noise floor. Any correlation
    between ACAT-adjusted NNA and Schwab NNA is statistically indistinguishable from
    zero — parameter choice is invisible in that ratio.

    DT's fix suggestions:
      Option A: Load gold/client_performance.parquet (already capped) as the baseline.
      Option B: Apply $50M event cap inline (one line fix to the silver baseline).

    COO recommendation: Option A. See Section 3.
  </postmortem>

  <!-- ================================================================ -->
  <!-- SECTION 3 — RECOMMENDED FIX AND WHY                             -->
  <!-- ================================================================ -->
  <architecture id="3" title="Recommended Data Source and Why">

    USE: gold/client_performance.parquet (s3://opal-data-bd/gold/client_performance.parquet)

    Grain: one row per (date × relationship_id)
    Key columns: date, relationship_id, cum_inflows, cum_outflows, nna
    Where: nna = cum_inflows − cum_outflows (cumulative since relationship inception)

    This parquet is the output of script 05_build_client_performance.py — the production
    gold layer artifact. All three cap layers are already applied. It is exactly what the
    portal reports to users today.

    Monthly firm-wide NNA is derived from it as follows:
      For each month M in the test window:
        1. Take the last available date in month M for each relationship_id → nna_end
        2. Take the last available date in the prior month → nna_start
        3. monthly_nna_by_rel = nna_end - nna_start  (delta of cumulative NNA)
        4. baseline_nna_month_M = sum(monthly_nna_by_rel across all relationship_ids)

    This is exactly how script 09_generate_partner_analytics.py derives period NNA
    from the same parquet (see its get_period_pairs() function). The derivation is
    straightforward and does not require reimplementing any cap logic.

    WHY NOT Option B ($50M inline clip):
      Option B only replaces Layer 1. The AUA-based outflow cap (Layer 2) requires
      joining positions data — it is not a one-liner. Without Layer 2, Relationship "0"
      ($345M lifetime phantom outflows, 2,101 accounts) still dominates the baseline
      and the noise floor remains orders of magnitude larger than the ACAT signal.
      Option B would produce a less degenerate result but still not a production-faithful
      baseline. Option A is correct because it uses what production already computed.

    NOTE ON CANONICAL FIX:
      The JNL/sweep canonical fix (committed 2026-03-05) has NOT been deployed. The
      current gold parquet in S3 does not include it. This is acceptable for the
      correlation test — the canonical fix reduces net NNA by ~$1.5M over 4 months,
      which is negligible relative to ACAT adjustment magnitudes ($46-98M) and will
      not change which parameter combination ranks highest. Test against the current
      deployed baseline: this answers "how much does ACAT add on top of what users
      see today," which is exactly the production question.
  </architecture>

  <!-- ================================================================ -->
  <!-- SECTION 4 — IMPLEMENTATION: WHAT TO BUILD                       -->
  <!-- ================================================================ -->
  <objective>
    Rewrite diag_acat_param_grid.py to use gold/client_performance.parquet as the
    baseline. The ACAT adjustment computation still reads silver/transactions (only
    the baseline source changes). Re-run the 24-combo primary grid + 9 secondary
    combos on EC2, compute correlation metrics, produce the ranked results table,
    and write the analysis session log with final parameter recommendation.
  </objective>

  <requirements>

    <requirement id="1">
      REWRITE: diag_acat_param_grid.py

      Replace compute_baseline_nna_by_month() with a gold-parquet-based derivation.
      The rest of the script (ACAT scan loop, metrics computation, S3 output) is
      unchanged from the prior version except as noted below.

      New baseline derivation function:

        def compute_baseline_nna_by_month(gold_s3_key='gold/client_performance.parquet'):
            """
            Derives monthly firm-wide NNA from the production gold parquet.
            All caps (50M event, AUA-based, velocity) are already applied in this artifact.
            """
            gold = _read_parquet(gold_s3_key)
            gold['date'] = pd.to_datetime(gold['date'])
            gold['ym'] = gold['date'].dt.to_period('M')

            # Last available date per (relationship, month) — same pattern as script 09
            idx = gold.groupby(['relationship_id', 'ym'])['date'].idxmax()
            monthly = gold.loc[idx][['relationship_id', 'ym', 'nna']].copy()
            monthly = monthly.sort_values(['relationship_id', 'ym'])

            # Delta NNA per relationship per month (cumulative → periodic)
            monthly['nna_delta'] = monthly.groupby('relationship_id')['nna'].diff().fillna(
                monthly['nna']  # first month for each relationship: use full cum value
            )

            # Sum across all relationships → firm-wide monthly NNA
            baseline = monthly.groupby('ym')['nna_delta'].sum()
            baseline.index = baseline.index.astype(str)  # '2024-05', '2024-06', etc.
            return baseline

      Call this function at the top of run_grid() to obtain the baseline vector,
      then add each ACAT adjustment on top of it per parameter combination.

      Data loading sequence in the revised script:
        1. Load gold/client_performance.parquet → baseline NNA by month (uses gold)
        2. Load silver/transactions (all partitions, parallel) → for ACAT scan (uses silver)
        3. Superset pre-computation (first 60 days, all buys/sells/nna per account)
        4. Parameter loop: for each combo, filter superset → acat_estimate by month
                           → adjusted = baseline + acat_estimate
                           → compute 7 correlation metrics vs SCHWAB_NNA
        5. Secondary MIN_ACAT tests on top 3 Pearson combinations
        6. Write results CSVs to S3, print ranked table

      Schwab ground truth vector (hardcoded — do not derive):
        SCHWAB_NNA = {
            '2024-05': 21_000_000,
            '2024-06':  9_000_000,
            '2024-07': 29_000_000,
            '2024-08': 22_000_000,
            '2024-09': 44_000_000,
            '2024-10': 64_000_000,
            '2024-11': 18_000_000,
            '2024-12': 46_000_000,
            '2025-01':  7_000_000,
            '2025-02':  9_000_000,
            '2025-03': 28_000_000,
            '2025-04': 46_000_000,
            '2025-05': 10_000_000,
        }

      All other logic from prior version is preserved:
        - ONBOARDING_DAYS grid: [7, 14, 21, 30, 45, 60]
        - BURST_THRESHOLD grid: [2, 3, 4, 5]
        - Secondary MIN_ACAT_ACCOUNT_ESTIMATE: [0, 25000, 100000] on top 3 Pearson combos
        - 7 metrics: Pearson r, Spearman r, sign_agreement_rate, RMSE, MAE,
                     total_gap, max_monthly_overshoot
        - BASELINE_NO_ACAT and V3_DEFAULT comparator rows in output
        - S3 output paths: acat_param_grid_results.csv, acat_param_grid_monthly_detail.csv
        - Stdout ranking table
        - No scipy — use np.corrcoef for Pearson, numpy argsort for Spearman rank transform
        - Canonical JNL/sweep exclusions applied in the ACAT scan NNA mask (unchanged)
    </requirement>

    <requirement id="2">
      COMMIT before writing the DT brief.
      Overwrite the existing diag_acat_param_grid.py in place (not a new file — same path).
      Also update diag_acat_correlation_summary.py if the CSV schema changes (it should not).

      Commit with DS authorship:
        git add data/black_diamond/scripts/diagnostics/diag_acat_param_grid.py
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DS_ClientPlatform: fix acat param grid -- gold baseline replaces raw silver"

      DO NOT push. DT pushes.
    </requirement>

    <requirement id="3">
      DT BRIEF at docs/briefs/devops-brief-acat-param-grid-v2-ec2-run.md

      Write new execution instructions for DT. The prior brief (devops-brief-acat-param-grid-ec2-run.md)
      is stale — mark it superseded with a note at the top, then write the new one.

      New brief must specify:
        - Script: diag_acat_param_grid.py (updated version, same path)
        - S3 upload: s3://opal-data-bd/scripts/diagnostics/diag_acat_param_grid.py
        - EC2 instance: bd-gold-layer-runner (i-01003b035d2988dfb)
        - Run command:
            python /tmp/diag_acat_param_grid.py 2>&1 | tee /tmp/acat_grid_v2_output.txt
        - Capture stdout:
            aws s3 cp /tmp/acat_grid_v2_output.txt s3://opal-data-bd/diagnostics/acat_grid_v2_stdout.txt
        - Expected runtime: ~15-20 min
            Gold parquet load: ~5-10s (single file, ~200MB estimated)
            Silver transactions load: ~40s (1,742 partitions, same as before)
            Grid computation: ~5 min (24 combos in memory after load)
            Secondary tests: ~2 min
        - The script writes its own output CSVs to S3 (acat_param_grid_results.csv,
          acat_param_grid_monthly_detail.csv). DT only needs to capture stdout.
        - No SSM inline code. S3 → EC2 → execute. EC2_CODE_DEPLOYMENT_STANDARD.md applies.
        - Note for DT: the gold parquet (~200MB) will be loaded in addition to
          silver/transactions (~3.4M rows). Total memory footprint is higher than v1 run.
          If instance OOMs, report to DS before attempting any fix.
    </requirement>

    <requirement id="4">
      ANALYSIS after DT runs v2 grid.

      Read both S3 CSVs. Run diag_acat_correlation_summary.py to produce the summary.
      Document the following in a session log:

      4a. Winning combination by Pearson r. State the exact values:
          (ONBOARDING_DAYS=X, BURST_THRESHOLD=Y, MIN_ACAT_ESTIMATE=Z)
          Pearson r = ?, Spearman r = ?, sign agreement = ?/13, RMSE = $?M, total gap = +/-$?M

      4b. Baseline comparator performance. How much does the best combination improve
          over BASELINE_NO_ACAT? What is the Pearson r of BASELINE_NO_ACAT against Schwab?
          This quantifies the total ACAT methodology contribution.

      4c. Sign agreement rate map. Which combination achieves the highest sign agreement?
          If it differs from the Pearson winner, document the trade-off explicitly:
          "Pearson winner is (X, Y) but sign agreement winner is (A, B) which gains
          N/13 sign agreement at a cost of Pearson delta = Z."
          CEO will make the final call between these if they diverge.

      4d. Sensitivity profile. Holding BURST_THRESHOLD at the Pearson-winning value,
          how does Pearson r change as ONBOARDING_DAYS varies across [7, 14, 21, 30, 45, 60]?
          Is the correlation surface flat (robust) or peaked (sensitive)? Same question
          for BURST_THRESHOLD holding ONBOARDING_DAYS fixed.
          A flat surface means the methodology is robust and parameter choice is
          not critical. A peaked surface means we must get the parameter right.

      4e. January 2025 behavior. For the Pearson-winning combination, what is the
          adjusted NNA for January 2025, and how does it compare to Schwab's $7M?
          The v3 default produced a $72.6M overshoot for this month. Does the
          winning combination reduce this? By how much?

      4f. Final recommendation. State the single recommended parameter set:
          ONBOARDING_DAYS = [recommended value]
          BURST_THRESHOLD = [recommended value]
          MIN_ACAT_ACCOUNT_ESTIMATE = [recommended value]
          Rationale: cite Pearson r, sign agreement, Jan 2025 behavior, and sensitivity.

      This analysis document is the direct input to the Phase 4 implementation task order.
      COO reviews before issuing Phase 4.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      diag_acat_param_grid.py rewritten and committed. compute_baseline_nna_by_month()
      loads gold/client_performance.parquet. No silver-based baseline computation remains.
    </criterion>
    <criterion id="2">
      DT brief at docs/briefs/devops-brief-acat-param-grid-v2-ec2-run.md written.
      Prior brief marked superseded.
    </criterion>
    <criterion id="3">
      Grid v2 output in S3 after DT run:
        s3://opal-data-bd/diagnostics/acat_param_grid_results.csv     (26 rows: 24 + 2 baselines)
        s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv
        s3://opal-data-bd/diagnostics/acat_grid_v2_stdout.txt
        s3://opal-data-bd/diagnostics/acat_correlation_summary.txt
    </criterion>
    <criterion id="4">
      Pearson r for best combination is materially above baseline (target: &gt;0.60,
      which would represent meaningful correlation vs prior flat 0.088).
      If best combination still shows Pearson &lt; 0.40, DS must document why and
      flag to COO before proceeding — this would suggest a structural problem
      beyond the baseline fix.
    </criterion>
    <criterion id="5">
      Session log documents 4a-4f. Final recommended parameters stated with full
      metric profile. No production scripts modified.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      ALL execution on EC2 via S3 artifact model. No local runs.
    </constraint>
    <constraint>
      Do not reimplement any of script 05's cap logic inline. The entire point of
      this architecture change is to consume the already-capped gold output, not
      to rebuild the capping logic. If something about the gold parquet is unexpected
      (wrong schema, missing months, etc.), stop and report to COO before attempting
      any workaround.
    </constraint>
    <constraint>
      The gold parquet baseline reflects the CURRENT deployed state (without the
      canonical JNL/sweep fix). Do not attempt to apply the canonical fix inline
      to the gold parquet. The $1.5M difference is not material to parameter selection.
    </constraint>
    <constraint>
      Phase 4 implementation task order (integrating winning parameters into script 05)
      will NOT be issued until COO and CEO review the analysis session log (requirement 4).
    </constraint>
    <constraint>
      Commit with DS authorship. DT handles all pushes.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform"
                task="EC2 run of revised diag_acat_param_grid.py"
                status="pending"
                note="DS commits fix and writes DT brief. DT runs on EC2. DS reads S3 output."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">diag_acat_param_grid.py (revised — gold baseline)</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-acat-param-grid-v2-ec2-run.md</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_param_grid_results.csv</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_correlation_summary.txt</deliverable>
    <deliverable type="document">Session log covering 4a-4f with final parameter recommendation</deliverable>
  </deliverables>

</task_order>
```
