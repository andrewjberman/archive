# Task Order: ADVI_AUAVAR.001 — Write AUA Gap Decomposition Diagnostic Script — 0.4.0_DS_ClientPlatform

```xml
<task_order>
  <metadata>
    <id>ADVI_AUAVAR.001-DS.write-aua-gap-diagnostic</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-06</date>
    <status>complete</status>
    <priority>HIGH — AUAVAR Phase 1 gating task. DT cannot run EC2 diagnostic until this is committed.</priority>
    <thread>ADVI_AUAVAR-001-aua-gap-segment-decomposition-bd-allocat</thread>
    <project>ADVI_AUAVAR</project>
  </metadata>

  <!-- ================================================================ -->
  <!-- SECTION 1 — CONTEXT                                               -->
  <!-- ================================================================ -->
  <background id="1" title="Context">
    Thread ADVI_AUAVAR-001 is complete (DS turn 5 + DT turn 6, both converge).

    Problem: BD reports ~$1.605B non-cash AUA (2026-03-03 snapshot).
    Our gold layer reports ~$1.545B. The ~$55M gap (3.4%) needs to be attributed
    to named segments.

    CORRECTION (2026-03-06, 1.0.0_SA_CTO): The $1.236B figure from the Phase 1
    DS investigation was erroneous — the prior agent conflated NNA and AUA metrics.
    Our actual non-cash AUA is ~$1.545B. There is NO gold-vs-gold discrepancy to
    resolve. The real gap is simply BD (~$1.60B) vs our model (~$1.545B) = ~$55M.
    All references to $1.236B in prior logs and thread messages should be disregarded.

    The diagnostic script will:
      1) Establish gold baseline for D=2026-03-02 (expected: ~$1.545B)
      2) Run household aggregation check (positions_cube x prices vs client_performance — should be ~0)
      3) Decompose BD-vs-gold gap into coverage + residual segments
      4) Emit a stable JSON waterfall artifact for COO/memo use

    COO DECISION GATE:
      Cash treatment (Segment 3) is diagnostics-only for now. Do NOT net cash from
      headline totals unless COO explicitly confirms the non-cash AUA mask definition.
      Include cash totals as a separate diagnostic block if allocations has security_name.
  </background>

  <!-- ================================================================ -->
  <!-- SECTION 2 — WHAT TO BUILD                                        -->
  <!-- ================================================================ -->
  <objective>
    Implement data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py
    for anchor date D=2026-03-02. Write a DT execution brief. Commit both.
  </objective>

  <requirements>

    <requirement id="1">
      IMPLEMENT: data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py

      ANCHOR DATE: D = 2026-03-02 (known gold AUA print: $1.551965B from DT script09 log)

      INPUTS (S3, all read-only):
        Gold:
          s3://opal-data-bd/gold/client_performance.parquet   (filter date == D)
          s3://opal-data-bd/gold/positions_cube/2026-03-02.parquet
          s3://opal-data-bd/gold/accounts_dimension_latest.parquet
          s3://opal-data-bd/silver/prices/canonical_prices.parquet  (filter date == D or closest)
        Allocations (try both; use as_of_date column to determine which to use):
          s3://opal-data-bd/silver/allocations/2026-03-02.parquet
          s3://opal-data-bd/silver/allocations/2026-03-01.parquet

      DATA AVAILABILITY NOTE:
        If positions_cube/2026-03-02.parquet does not exist, log the error and fall back to
        reporting only the client_performance total for D, with a flag: positions_cube_missing=true.
        Do NOT error out silently. Do NOT fabricate data. Report what is available.

      ALLOCATION DATE CONVENTION RESOLUTION:
        1. Load the candidate allocation file.
        2. If column as_of_date exists: report unique values; use that as the allocations as-of date.
        3. If as_of_date absent: report both alignments (filename date == D and filename date == D-1)
           in the JSON under diagnostics.alloc_date_convention_note.

      STEP 1 — GOLD BASELINE (per 2026-03-06 correction; no unexpected discrepancy expected):
        A. gold_cp_total = sum(total_aua) from client_performance where date == D
                           (relationship grain). Expected: ~$1.545B.
        B. gold_cube_total = sum(units * price) from positions_cube/D x canonical_prices for D
                             (account grain). Needed for Segment 2 check and Segment 4 residual.
        C. Report both totals. If abs(A - B) / A > 0.01 (>1%), flag as WARN. No large discrepancy
           is expected (the $1.236B figure in prior logs was a prior agent error; ignore it).

      STEP 2 — SEGMENT DECOMPOSITION (BD-vs-gold):

        Segment 1: Account Coverage Gap
          A = set of account_id in allocations (post as_of_date alignment)
          B = set of account_id in accounts_dimension_latest
          C = set of account_id in positions_cube/D

          Compute:
            missing_in_accounts_dimension: A \ B -> count and sum allocations account_market_value
            missing_in_positions_cube: A \ C -> count and sum allocations account_market_value

        Segment 2: Household Aggregation Check (should be near-zero)
          delta = gold_cp_total - gold_cube_total  (from Step 1)
          Report as segment. If abs(delta) > $1M, classify as WARN: addressable bug.

        Segment 3: Cash Treatment (diagnostic-only, no headline netting)
          If allocations has security_name column:
            cash_mask_pattern = r'(?i)(cash|money market|sweep)'
            alloc_cash_total = sum(account_market_value) where security_name matches mask
            alloc_noncash_total = alloc_total - alloc_cash_total
          If positions_cube has asset_name column (or similar):
            apply analogous mask to compute gold_cash_total, gold_noncash_total
          Report as diagnostics block only, not subtracted from headline.

        Segment 4: Account-Level Residual (Pricing / Holdings Mismatch)
          For accounts in A INTERSECT C:
            per_account_delta = alloc_mv(account) - gold_cube_mv(account)
          residual_total = sum(per_account_delta)
          top_account_residuals = top 20 accounts by abs(per_account_delta)
          This is the "pricing/holdings" bucket — label honestly as account-level residual.

      OUTPUTS (S3):
        Script upload:   s3://opal-data-bd/diagnostics/diag_aua_gap_decomposition.py
        Results JSON:    s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02.json
        Stdout capture:  s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt

      JSON SCHEMA (locked from thread DT turn 6):
        {
          "run_metadata": {
            "gold_date": "2026-03-02",
            "allocations_files_tested": [...],
            "allocations_as_of_date_detected": "...",
            "generated_at_utc": "..."
          },
          "totals": {
            "gold_client_performance_total_aua": ...,
            "gold_positions_cube_total_aua": ...,
            "bd_allocations_total_market_value": ...,
            "delta_bd_minus_gold_positions": ...,
            "delta_pct_of_bd": ...
          },
          "coverage": {
            "alloc_accounts": ...,
            "positions_cube_accounts": ...,
            "accounts_dimension_accounts": ...,
            "missing_in_accounts_dimension": {"count": ..., "bd_value": ...},
            "missing_in_positions_cube": {"count": ..., "bd_value": ...}
          },
          "segments": [
            {"name": "account_coverage_missing_in_accounts_dimension", "value": ..., "count": ...},
            {"name": "account_coverage_missing_in_positions_cube", "value": ..., "count": ...},
            {"name": "household_aggregation_check_gold_cp_minus_gold_cube", "value": ...},
            {"name": "residual_bd_minus_gold_on_covered_accounts", "value": ...}
          ],
          "top_account_residuals": [
            {"account_id": "...", "bd_mv": ..., "gold_mv": ..., "delta": ...}
          ],
          "diagnostics": {
            "alloc_columns": [...],
            "has_alloc_as_of_date": true/false,
            "alloc_rows": ...,
            "alloc_rows_per_account_avg": ...,
            "alloc_date_convention_note": "...",
            "positions_cube_missing": false,
            "cash_treatment": {
              "alloc_cash_total": ...,
              "alloc_noncash_total": ...,
              "gold_cash_total": ...,
              "gold_noncash_total": ...
            }
          }
        }
    </requirement>

    <requirement id="2">
      COMMIT the script:

      git add data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py
      git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
        -m "0.4.0_DS_ClientPlatform: ADVI_AUAVAR -- add diag_aua_gap_decomposition.py (D=2026-03-02)"

      DO NOT push. DT handles all pushes.
    </requirement>

    <requirement id="3">
      DT BRIEF at docs/briefs/devops-brief-auavar-gap-decomposition-ec2-run.md

      Write execution instructions for DT:
        - Script: data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py
        - S3 upload: s3://opal-data-bd/diagnostics/diag_aua_gap_decomposition.py
        - EC2 instance: bd-gold-layer-runner (i-01003b035d2988dfb)
        - Run command:
            python /tmp/diag_aua_gap_decomposition.py 2>&1 | tee /tmp/aua_gap_stdout.txt
        - Capture stdout:
            aws s3 cp /tmp/aua_gap_stdout.txt
              s3://opal-data-bd/diagnostics/aua_gap_decomposition_2026-03-02_stdout.txt
        - Expected runtime: ~5-10 min (single date, no multi-partition transaction scan)
        - EC2_CODE_DEPLOYMENT_STANDARD.md applies
        - SSM params file pattern (file://.tmp_ssm_params.json) to avoid MSYS mangling

      Commit brief with DS authorship:
        git add docs/briefs/devops-brief-auavar-gap-decomposition-ec2-run.md
        git commit --author="0.4.0_DS_ClientPlatform &lt;0.4.0_DS_ClientPlatform@opal.agent&gt;" \
          -m "0.4.0_DS_ClientPlatform: ADVI_AUAVAR -- add DT brief for AUA gap diagnostic EC2 run"
    </requirement>

  </requirements>

  <acceptance_criteria>
    <criterion id="1">
      diag_aua_gap_decomposition.py committed. Establishes gold baseline (~$1.545B expected),
      runs household aggregation check, and decomposes BD-vs-gold gap for D=2026-03-02.
      Emits JSON with locked schema.
    </criterion>
    <criterion id="2">
      Script handles missing positions_cube gracefully (flag, do not error).
      Cash treatment reported as diagnostics-only block. Headline totals are gross (not net of cash).
    </criterion>
    <criterion id="3">
      DT brief committed at docs/briefs/devops-brief-auavar-gap-decomposition-ec2-run.md.
    </criterion>
  </acceptance_criteria>

  <constraints>
    <constraint>
      Do not modify any production scripts (05, 05b, 07, 08, 09, 10).
    </constraint>
    <constraint>
      Do not write to gold/ or silver/ prefixes. Outputs go to diagnostics/ only.
    </constraint>
    <constraint>
      Cash treatment: diagnostic block only. Do NOT subtract cash from headline totals
      unless COO explicitly confirms the non-cash AUA mask definition in a follow-up task order.
    </constraint>
    <constraint>
      Commit with DS authorship. DT pushes.
    </constraint>
  </constraints>

  <dependencies>
    <dependency agent="0.4.0_DT_ClientPlatform"
                task="ADVI_AUAVAR.002-DT (EC2 execution)"
                status="blocked on this task order"
                note="DT cannot execute until DS commits script and DT brief."/>
  </dependencies>

  <deliverables>
    <deliverable type="commit">data/black_diamond/scripts/diagnostics/diag_aua_gap_decomposition.py</deliverable>
    <deliverable type="commit">docs/briefs/devops-brief-auavar-gap-decomposition-ec2-run.md</deliverable>
  </deliverables>

</task_order>
```
