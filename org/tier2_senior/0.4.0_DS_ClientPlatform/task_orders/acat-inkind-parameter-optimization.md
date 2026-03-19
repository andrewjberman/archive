# Task Order: ACAT In-Kind NNA — Parameter Optimization via Correlation Testing — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-03-05-acat-inkind-parameter-optimization</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-05</date>
    <status>complete</status>
    <priority>HIGH — CEO-directed. Optimize ACAT parameters before production integration.</priority>
  </metadata>

  <context>
    Phase 3 testing confirmed the ACAT in-kind FIFO methodology is sound (867 accounts,
    $46M gap recovery, &lt;5% false positive rate). The default parameters (ONBOARDING_DAYS=30,
    BURST_THRESHOLD=3) were chosen by inspection, not by optimization. The January 2025
    overshoot ($72.6M in one month) suggests the parameter space has not been fully explored.

    Schwab's official monthly NNA figures are available for 13 months (May 2024 - May 2025)
    from the SoT cross-reference. This gives us a ground truth series we can use to
    systematically search for parameter combinations that maximize correlation between our
    adjusted NNA and Schwab's reported NNA.

    ALL execution happens on EC2 via S3. Do not attempt to run any of these scripts locally.
    The transaction dataset (1,742 partitions, 3.4M rows) will OOM a local machine.
  </context>

  <objective>
    Design and execute a parameter grid search over the ACAT onboarding-window FIFO
    methodology. For each parameter combination, compute adjusted monthly NNA and measure
    correlation with Schwab's official 13-month figures. Identify the combination that
    best fits the ground truth and produce a ranked results table with trade-off analysis.
    The winning parameters will be used in the Phase 4 production implementation task order.
  </objective>

  <!-- ================================================================ -->
  <!-- FRAMEWORK DESIGN                                                   -->
  <!-- ================================================================ -->

  <framework>

    <section id="F1" name="Ground Truth Series">
      Schwab's official monthly NNA (May 2024 - May 2025, from REQ_schwab_sot_cross_reference.md).
      This is the 13-element vector we optimize against:

        May 2024:  $21,000,000
        Jun 2024:   $9,000,000
        Jul 2024:  $29,000,000
        Aug 2024:  $22,000,000
        Sep 2024:  $44,000,000
        Oct 2024:  $64,000,000
        Nov 2024:  $18,000,000
        Dec 2024:  $46,000,000
        Jan 2025:   $7,000,000
        Feb 2025:   $9,000,000
        Mar 2025:  $28,000,000
        Apr 2025:  $46,000,000
        May 2025:  $10,000,000

      Note: Schwab's NNA definition is broader than TOA (includes FDIC, cash flows).
      We are not targeting exact equality — we are targeting directional alignment
      and reduction in month-to-month divergence. Correlation is the right metric
      because it captures shape agreement without requiring level equivalence.
    </section>

    <section id="F2" name="Parameter Grid">
      Two primary parameters to vary. All other logic is held constant (canonical
      JNL/sweep exclusions always applied; existing $50M per-event cap always applied).

      ONBOARDING_DAYS (window length):
        [7, 14, 21, 30, 45, 60]
        Rationale range: 7 = aggressive advisors who invest immediately;
        60 = conservative advisors who hold positions 2 months before rebalancing.
        Below 7 is too narrow (settlement T+2 alone consumes it).
        Above 60 is unreliable (impossible to distinguish ACAT buys from regular activity).

      BURST_THRESHOLD (minimum Buy count in window to qualify):
        [2, 3, 4, 5]
        Rationale range: 2 = very sensitive (single-position ACATs);
        5 = very conservative (only multi-position ACAT portfolios).

      Full grid: 6 x 4 = 24 parameter combinations.

      Secondary parameter (tested after primary grid):
      MIN_ACAT_ACCOUNT_ESTIMATE (minimum per-account ACAT estimate to include):
        [0, 25000, 100000]
        Rationale: filtering tiny estimates reduces noise from small accounts that
        happen to pass the burst filter but contribute negligible real ACAT value.
        Only test the 3 best primary combinations against this secondary parameter.
        Total secondary tests: 3 x 3 = 9 additional runs.

      Total runs: 24 (primary grid) + 9 (secondary) = 33 runs.
    </section>

    <section id="F3" name="Correlation Metrics">
      For each parameter combination, compute all of the following against the
      Schwab 13-month NNA vector. Report all metrics — the "winner" is chosen
      by balancing across metrics, not by Pearson alone.

      PRIMARY METRIC:
        Pearson r  — linear correlation between our adjusted monthly NNA and
                     Schwab's monthly NNA. Measures whether our shape tracks
                     Schwab's shape. Target: maximize.

      SECONDARY METRICS:
        Spearman r — rank correlation. More robust to outlier months (e.g.,
                     Jan 2025). Target: maximize.
        Sign agreement rate — % of 13 months where sign(our_nna) == sign(schwab_nna).
                     Current baseline without ACAT: 6/13 (46%). Target: maximize.
        RMSE       — root mean squared error in dollars. Target: minimize.
        MAE        — mean absolute error in dollars. Less sensitive to outliers than RMSE.
                     Target: minimize.
        Total gap  — sum(our_adjusted_nna) - sum(schwab_nna) over 13 months.
                     Measures level bias, not shape. Target: nearest to zero.
        Max monthly overshoot — worst single-month deviation. Flags Jan 2025 type events.
                     Target: minimize.

      Baseline comparators to include in results (treated as parameter combinations):
        "BASELINE_NO_ACAT"   — our current NNA post-canonical-fix, no ACAT adjustment.
        "V3_DEFAULT"         — ONBOARDING_DAYS=30, BURST_THRESHOLD=3 (Phase 3 result).
      Both must appear in the output table so the grid results are interpretable
      relative to the starting point.
    </section>

    <section id="F4" name="Execution Architecture">
      Single-pass design: load transactions once, compute all 24 combinations in memory.
      Do NOT spawn 24 separate EC2 jobs — that is unnecessary and expensive.

      Step 1: Load all silver/transactions (1,742 partitions) once in parallel.
      Step 2: Apply canonical exclusions (JNL/sweep filter — same as script 05 post-fix).
      Step 3: Compute baseline monthly NNA (no ACAT) — store as the BASELINE_NO_ACAT vector.
      Step 4: Compute per-account onboarding data once (first_date, all buys/sells/nna
              within the longest window = 60 days). This superset covers all shorter windows.
      Step 5: For each (ONBOARDING_DAYS, BURST_THRESHOLD) combination:
                a. Filter superset to accounts with acct_age &lt;= ONBOARDING_DAYS
                b. Apply BURST_THRESHOLD filter
                c. Compute acat_estimate per account
                d. Aggregate acat_estimate by first_date month
                e. Add to baseline NNA → adjusted monthly NNA vector
                f. Compute all 7 metrics vs Schwab ground truth
                g. Append result row to results DataFrame
      Step 6: Run secondary MIN_ACAT_ACCOUNT_ESTIMATE tests on top 3 Pearson combinations.
      Step 7: Write results to s3://opal-data-bd/diagnostics/acat_param_grid_results.csv
              Also write full monthly detail (adjusted NNA per month per combo) to
              s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv
      Step 8: Print ranked results table to stdout (captured by DT to S3).
    </section>

  </framework>

  <!-- ================================================================ -->
  <!-- IMPLEMENTATION REQUIREMENTS                                        -->
  <!-- ================================================================ -->

  <requirements>

    <requirement id="1">
      SCRIPT: diag_acat_param_grid.py

      Write a single self-contained diagnostic script at:
        data/black_diamond/scripts/diagnostics/diag_acat_param_grid.py

      The script implements the single-pass architecture from Framework section F4.

      Key implementation notes:

      a) Superset pre-computation (efficiency):
         Compute all buy/sell/nna totals for every account within the MAXIMUM window
         (60 days) in a single groupby pass before the parameter loop. The per-parameter
         step then filters by acct_age &lt;= ONBOARDING_DAYS, not by re-loading data.
         This makes the full 24-combo grid feasible in a single EC2 run (&lt;10 min total
         estimated, vs 6+ hours if done naively).

      b) Schwab ground truth hardcoded in the script:
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

      c) Canonical NNA exclusions applied before baseline computation:
         Exclude JNL - LONG, JNL - SHORT (action field).
         Exclude TRF BTWN SCH ACCTS, TO SEP ACCT MGR, TRANSFER FUNDS TO SCHWAB BANK
         (description field). These are identical to the canonical_nna_logic.md fix
         already approved. Apply them to the baseline so the ACAT adjustment is
         isolated as the only variable.

      d) Monthly NNA computation:
         Baseline NNA = sum of net NNA flows (inflows - outflows) per calendar month.
         ACAT adjustment = acat_estimate amounts bucketed by account first_date month.
         Adjusted NNA = baseline NNA + ACAT adjustment, restricted to May 2024 - May 2025.

      e) Metrics computation:
         Use scipy.stats.pearsonr and spearmanr, or compute manually if scipy is not
         in the environment. If scipy is unavailable, implement Pearson r manually
         using numpy (it is 4 lines of arithmetic — do not add scipy as a new dependency
         without confirming it is in the gold-layer runtime environment).

      f) Output:
         Two CSV files written to S3:
           s3://opal-data-bd/diagnostics/acat_param_grid_results.csv
             Columns: onboarding_days, burst_threshold, min_acat_estimate,
                      pearson_r, spearman_r, sign_agreement_rate, rmse, mae,
                      total_gap, max_monthly_overshoot, accounts_flagged, total_acat_estimate
           s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv
             Columns: onboarding_days, burst_threshold, min_acat_estimate,
                      year_month, baseline_nna, acat_adjustment, adjusted_nna, schwab_nna, gap

         Both BASELINE_NO_ACAT and V3_DEFAULT must appear in the results CSV
         with onboarding_days=0 (baseline) and onboarding_days=30/burst=3 (default).

      g) Stdout output:
         After writing S3 files, print a formatted ranked results table sorted by
         Pearson r descending. Include the top 10 combinations and both baseline comparators.
         Format example (columns may vary):
           Rank  Days  Threshold  Min$    Pearson   Spearman  SignAgr   RMSE($M)  TotalGap($M)
              1    21          3      0    0.847      0.812    10/13      11.2       +8.1
              2    30          3      0    0.831      0.799     9/13      13.4      +13.2
              ...
           BASE     -          -      -    0.412      0.388     6/13      22.7      -32.7
    </requirement>

    <requirement id="2">
      SCRIPT: diag_acat_correlation_summary.py

      Write a lightweight analysis script at:
        data/black_diamond/scripts/diagnostics/diag_acat_correlation_summary.py

      This script reads the two S3 CSVs produced by diag_acat_param_grid.py and
      produces a human-readable analysis document. It does NOT re-load transactions.
      It can run locally OR on EC2. Primary use: DS reads S3 results and generates
      the summary after DT runs the grid.

      Output:
        a) Full ranked results table (all 33 combos sorted by Pearson r)
        b) Top 3 combinations with month-by-month adjusted NNA vs Schwab breakdown
        c) Sensitivity analysis: holding BURST_THRESHOLD=best, vary ONBOARDING_DAYS
           — how much does Pearson move? Quantify the sensitivity.
           Repeat: holding ONBOARDING_DAYS=best, vary BURST_THRESHOLD.
        d) Sign agreement heat map (text-based 6x4 grid showing sign_agreement_rate
           for each ONBOARDING_DAYS x BURST_THRESHOLD cell).
        e) Recommended combination with written justification.

      Write the output to a local file: diag_acat_correlation_summary_output.txt
      Then upload to S3: s3://opal-data-bd/diagnostics/acat_correlation_summary.txt
    </requirement>

    <requirement id="3">
      DT BRIEF: Write execution instructions for DT at:
        docs/briefs/devops-brief-acat-param-grid-ec2-run.md

      Must specify:
        - Script: diag_acat_param_grid.py
        - EC2 instance: bd-gold-layer-runner (same as previous diagnostic run)
        - S3 upload path for script: s3://opal-data-bd/scripts/diagnostics/diag_acat_param_grid.py
        - Run command:
            python /tmp/diag_acat_param_grid.py 2>&1 | tee /tmp/acat_grid_output.txt
        - Capture stdout: aws s3 cp /tmp/acat_grid_output.txt s3://opal-data-bd/diagnostics/acat_grid_stdout.txt
        - Expected runtime: ~10-15 min (single-pass; all 24 combos in memory after load)
        - Memory note: same load pattern as v3 (1,742 partitions, 3.4M rows, ~39s load).
          The grid loop adds negligible memory beyond the initial load.
        - The script writes its own output CSVs to S3 directly — DT only needs to
          capture stdout separately.
        - No SSM inline Python. Script goes S3 -> EC2 -> executes. See EC2_CODE_DEPLOYMENT_STANDARD.md.
    </requirement>

    <requirement id="4">
      ANALYSIS: After DT runs the grid and output lands in S3, DS reads both CSVs and
      runs diag_acat_correlation_summary.py to produce the analysis. Document findings
      in a session log covering:

      4a. Winning combination: which (ONBOARDING_DAYS, BURST_THRESHOLD) maximizes Pearson r?
          Does the Pearson winner also win on sign agreement rate? If not, which combination
          wins on sign agreement and how large is the Pearson trade-off?

      4b. Sensitivity: how much does Pearson r change across the ONBOARDING_DAYS axis
          (with BURST_THRESHOLD fixed at winner)? Is the correlation surface flat (robust
          to window choice) or peaked (only one window works)?
          Same question for BURST_THRESHOLD axis.

      4c. MIN_ACAT_ESTIMATE secondary test: does filtering small ACAT estimates ($25K, $100K
          minimum) improve correlation for the top 3 combos? If yes by how much?

      4d. Jan 2025 behavior: which parameter combination handles January 2025 best?
          (The v3 default produced a $72.6M overshoot that month.) Does tightening
          the window or raising the threshold reduce the Jan 2025 overshoot without
          materially hurting correlation in other months?

      4e. Final recommendation: the single parameter combination to use in Phase 4
          implementation, with written rationale covering:
            - Pearson r achieved
            - Sign agreement rate
            - Jan 2025 behavior
            - Any remaining known weaknesses

      This analysis is the direct input to the Phase 4 implementation task order.
      COO and CEO review the session log before implementation is authorized.
    </requirement>

    <requirement id="5">
      COMMIT PROTOCOL:
        - Commit diag_acat_param_grid.py and diag_acat_correlation_summary.py together
          under DS authorship before writing the DT brief.
        - Commit the DT brief separately.
        - DS cannot push. DT pushes CLOUD after committing the grid scripts.
        - Analysis session log committed after grid run completes and analysis is done.
        - Do NOT modify any production gold layer script during this task.
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      diag_acat_param_grid.py committed and verified runnable (no import errors).
      Covers full 6x4=24 primary grid + secondary MIN_ACAT tests on top 3 combos.
    </criterion>
    <criterion id="2">
      diag_acat_correlation_summary.py committed. Reads S3 CSVs, produces ranked table
      and sensitivity analysis.
    </criterion>
    <criterion id="3">
      DT brief written at docs/briefs/devops-brief-acat-param-grid-ec2-run.md
      with complete S3/EC2 execution instructions. Estimated runtime noted.
    </criterion>
    <criterion id="4">
      Grid output in S3 after DT run:
        s3://opal-data-bd/diagnostics/acat_param_grid_results.csv       (26 rows: 24 + 2 baselines)
        s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv
        s3://opal-data-bd/diagnostics/acat_grid_stdout.txt
        s3://opal-data-bd/diagnostics/acat_correlation_summary.txt
    </criterion>
    <criterion id="5">
      Session log documents all items in requirement 4a-4e. Final recommended parameter
      combination stated explicitly with full metric profile.
    </criterion>
    <criterion id="6">
      No production scripts modified. Implementation task order to follow separately.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      ALL execution on EC2 via S3 artifact model. No local runs. The transaction dataset
      OOMs local machines. Write the scripts, commit them, write the DT brief, wait for
      EC2 output. Do not attempt to shortcut by running locally.
    </constraint>
    <constraint>
      Single-pass architecture is mandatory. Loading 1,742 partitions 24 separate times
      would take ~16 hours and waste EC2 compute. The superset pre-computation approach
      (load once, filter per combo in memory) must be used.
    </constraint>
    <constraint>
      Do not add new Python dependencies (e.g., scipy, sklearn). Use numpy for all
      statistical computations. Pearson r is trivially computable with numpy:
        r = np.corrcoef(our_vector, schwab_vector)[0, 1]
      Spearman r: rank-transform both vectors with numpy argsort, then apply corrcoef.
    </constraint>
    <constraint>
      The 13-month Schwab NNA ground truth series is hardcoded in the script from
      REQ_schwab_sot_cross_reference.md. Do not re-derive it or round it. Use the
      exact figures specified in Framework section F2 of this task order.
    </constraint>
    <constraint>
      Canonical NNA exclusions (JNL/sweep fix) must be applied in the baseline
      computation. The grid measures the ACAT adjustment's marginal contribution on
      top of a clean baseline. Mixing the ACAT and canonical fix effects would
      contaminate the correlation signal.
    </constraint>
    <constraint>
      Phase 4 implementation task order will NOT be issued until DS session log
      (requirement 4) is complete and COO/CEO have reviewed the winning parameters.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform" task="EC2 run of diag_acat_param_grid.py"
                status="pending"
                note="DS writes scripts + DT brief first. DT runs on EC2. DS reads S3 output for analysis."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/diagnostics/diag_acat_param_grid.py</deliverable>
    <deliverable type="commit">data/black_diamond/scripts/diagnostics/diag_acat_correlation_summary.py</deliverable>
    <deliverable type="document">docs/briefs/devops-brief-acat-param-grid-ec2-run.md</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_param_grid_results.csv (26 rows)</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_param_grid_monthly_detail.csv</deliverable>
    <deliverable type="s3">s3://opal-data-bd/diagnostics/acat_correlation_summary.txt</deliverable>
    <deliverable type="document">Session log: full grid analysis covering 4a-4e, final parameter recommendation</deliverable>
  </deliverables>

</task_order>
```
