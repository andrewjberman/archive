# Task Order: ADVI_NNAVAR.001 — Write NNA Gap Decomposition Diagnostic Script — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>ADVI_NNAVAR.001-DS.write-gap-decomposition-script</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
    <priority>HIGH — NNAVAR Phase 1 gating task. DT cannot run EC2 suites until this script is committed.</priority>
    <thread>ADVI_NNAVAR-001-nna-gap-decomposition-param-grid-analysi</thread>
    <project>ADVI_NNAVAR</project>
  </metadata>

  <!-- ================================================================ -->
  <!-- SECTION 1 — CONTEXT                                               -->
  <!-- ================================================================ -->
  <background id="1" title="Context">
    Thread ADVI_NNAVAR-001 is complete (DS turn 5 + DT turn 6, both converge).
    The agreed plan: write a new diagnostic script diag_nnavar_gap_decomposition.py
    that attributes the remaining -$119.8M 13-month NNA gap (vs Schwab) across 6
    suites (baseline, exclusions, dedup, caps, timing, coverage).

    ACAT params are decided: ONBOARDING_DAYS=30, BURST_THRESHOLD=3, MIN_ACAT_ESTIMATE=0.
    These are NOT part of this script — ACAT integration into script 05 is a later
    task order, after gap decomposition reveals what else needs to change.

    The script must NOT modify any production gold artifacts. It is diagnostics-only.
  </background>

  <!-- ================================================================ -->
  <!-- SECTION 2 — WHAT TO BUILD                                        -->
  <!-- ================================================================ -->
  <objective>
    Implement data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py
    with the 6-suite diagnostic framework agreed in thread ADVI_NNAVAR-001 (DS turn 5).
    Write a DT execution brief. Commit both.
  </objective>

  <requirements>

    <requirement id="1">
      IMPLEMENT: data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py

      Script design (from thread receipt):

      INPUTS:
        - gold/client_performance.parquet  (AUA spine: date, relationship_id, total_aua, nna)
        - silver/transactions/ (all partitions, parallel load — same as param grid)
        - CLI arg: --suite (one of: baseline, exclusions, dedup, caps, timing, coverage, all)
        - CLI arg: --run-date (YYYYMMDD, used to key S3 output paths; default: today)

      DESIGN:
        1. Load gold spine once (for AUA-based cap inputs and baseline monthly NNA).
        2. Load silver transactions once per invocation (suite-per-invocation pattern).
        3. For each variant in the selected suite, toggle filter/cap parameters and
           recompute flows from transactions, then apply caps using gold AUA.
        4. Derive monthly firm-wide NNA for Schwab window: May 2024 - May 2025 ('2024-05'...'2025-05').
        5. Compute metrics vs SCHWAB_NNA vector (below).
        6. Write outputs to S3 diagnostics prefix.

      DO NOT:
        - Scan or load positions_cube (not needed for this diagnostic).
        - Write to any gold/ or silver/ prefixes.
        - Modify script 05 or any production script.

      SCHWAB_NNA (hardcoded ground truth — same as param grid):
        {
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

      METRICS per variant (same 7 as param grid):
        - pearson_r, spearman_r, sign_agreement_count, sign_agreement_rate
        - rmse, mae, total_gap, max_monthly_overshoot

      SUITE DEFINITIONS (from thread DS turn 5):

        Suite 0 — baseline
          variant: baseline_current_gold
          Measure: derive monthly NNA from gold client_performance.parquet only.
          No transaction recomputation. Confirms starting-point r~=0.175, gap~=-$119.8M.

        Suite 1 — exclusions
          Load transactions, apply progressively more restrictive exclusion sets:
          variant 1: excl_none          (no action/description filter)
          variant 2: excl_action_only   (exclude action in {'JNL - LONG','JNL - SHORT'})
          variant 3: excl_action_plus_desc  (also exclude descriptions containing:
                     'TRF BTWN SCH', 'TO SEP ACCT MGR', 'TRANSFER FUNDS TO SCHWAB BANK')
          NOTE: excl_action_plus_desc corresponds to the committed canonical fix in script 05.

        Suite 2 — dedup
          variant 1: dedup_txnid_only          (deduplicate on transaction_id only)
          variant 2: dedup_composite_current   (account_id, trade_date, type_col, abs(market_value))
          variant 3: dedup_composite_plus_desc (same + description field)

        Suite 3 — caps
          variant 1: cap_event_only               ($50M per-event clip only)
          variant 2: cap_event_plus_aua            (+ AUA-based outflow cap per relationship)
          variant 3: cap_event_plus_aua_plus_velocity  (+ 90-day velocity cap; current full stack)

        Suite 4 — timing
          variant 1: month_last_date_delta   (current: last date per rel per month, diff cumulative nna)
          variant 2: month_sum_daily_flows   (sum daily net flows within calendar month)

        Suite 5 — coverage
          variant 1: rel_fallback_on    (current: missing relationship_id -> 'acct_{account_id}')
          variant 2: rel_drop_unmapped  (drop unmapped relationships entirely)

      S3 OUTPUT PATHS (write from script; diagnostics-only prefix):
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/summary.csv
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/{variant}/monthly_nna.csv
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/{variant}/metrics.json
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/stdout.txt
          (stdout captured by DT via SSM after execution)

      summary.csv schema (one row per variant):
        variant, pearson_r, spearman_r, sign_agreement_count, sign_agreement_rate,
        rmse, mae, total_gap, max_monthly_overshoot

      DT also requests a run_manifest.json per suite:
        s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/run_manifest.json
        Fields: git_commit_hash, ec2_instance_id (passed via CLI or placeholder), start_utc,
                end_utc, suite, variants_run, gold_rows_loaded, txn_rows_loaded, txn_rows_post_filter

      Memory management:
        - Call gc.collect() and del intermediates between variants.
        - Do not keep all variant outputs in memory simultaneously.
    </requirement>

    <requirement id="2">
      COMMIT the script before writing the DT brief.

      git add data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py
      git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
        -m "0.4.0_DS_ClientPlatform: ADVI_NNAVAR -- add diag_nnavar_gap_decomposition.py (suites 0-5)"

      DO NOT push. DT handles all pushes.
    </requirement>

    <requirement id="3">
      DT BRIEF at docs/briefs/devops-brief-nnavar-gap-decomposition-ec2-run.md

      Write execution instructions for DT covering:
        - Script: data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py
        - S3 upload path: s3://opal-data-bd/scripts/diagnostics/diag_nnavar_gap_decomposition.py
        - EC2 instance: bd-gold-layer-runner (i-01003b035d2988dfb)
        - Invocation mode: suite-per-invocation (one SSM command per suite)
          e.g.: python /tmp/diag_nnavar_gap_decomposition.py --suite exclusions --run-date 20260306
        - SSM pattern: use file://.tmp_ssm_params.json to avoid MSYS path mangling
          (same pattern as diag_acat_param_grid.py v2 run)
        - Capture stdout: aws s3 cp /tmp/nnavar_{suite}_stdout.txt
            s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/stdout.txt
        - Recommended suite order: baseline -> exclusions -> dedup -> caps -> timing -> coverage
          (stop early if a dominant driver is found -- COO decides after each suite)
        - Expected runtime per suite: baseline ~1-3 min, exclusions ~8-12 min,
          dedup ~10-15 min, caps ~8-15 min, timing ~2-6 min, coverage ~2-6 min
        - EC2_CODE_DEPLOYMENT_STANDARD.md applies (no inline code; S3 artifact model only)
        - If instance OOMs or any suite errors, report to DS/COO before retrying.

      Commit brief with DS authorship:
        git add docs/briefs/devops-brief-nnavar-gap-decomposition-ec2-run.md
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DS_ClientPlatform: ADVI_NNAVAR -- add DT brief for gap decomposition EC2 run"
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      diag_nnavar_gap_decomposition.py committed at
      data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py.
      All 6 suites implemented (baseline, exclusions, dedup, caps, timing, coverage).
      Script outputs summary.csv + per-variant artifacts + run_manifest.json to
      s3://opal-data-bd/diagnostics/nnavar/{run_date}/{suite}/.
    </criterion>
    <criterion id="2">
      Script does not import, load, or write to any gold/ or silver/ production paths
      except: gold/client_performance.parquet (read-only) and
      silver/transactions/ (read-only) and silver/prices/canonical_prices.parquet (read-only if needed).
    </criterion>
    <criterion id="3">
      DT brief at docs/briefs/devops-brief-nnavar-gap-decomposition-ec2-run.md committed.
      Specifies suite-per-invocation, SSM params file pattern, stdout capture, runtime estimates.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      No production scripts modified. This is a new diagnostic script only.
    </constraint>
    <constraint>
      No positions_cube scan. Caps must be computed from gold spine AUA, not from positions_cube.
    </constraint>
    <constraint>
      No scipy. Use np.corrcoef for Pearson; numpy rank transform for Spearman (same as param grid).
    </constraint>
    <constraint>
      All execution happens on EC2 via S3 artifact model. Do not run this locally or inline in SSM.
    </constraint>
    <constraint>
      Commit with DS authorship. DT pushes.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform"
                task="EC2 execution (ADVI_NNAVAR.002)"
                status="blocked on this task order"
                note="DT cannot execute until DS commits script and DT brief."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/diagnostics/diag_nnavar_gap_decomposition.py</deliverable>
    <deliverable type="commit">docs/briefs/devops-brief-nnavar-gap-decomposition-ec2-run.md</deliverable>
  </deliverables>

</task_order>
```
