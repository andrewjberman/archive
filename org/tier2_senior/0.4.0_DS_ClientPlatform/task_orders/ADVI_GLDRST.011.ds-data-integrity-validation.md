# Task Order: ADVI_GLDRST.011 — Data Integrity Validation

```xml
<task_order>
  <metadata>
    <id>1.0.0_SA_CTO-2026-03-26-gldrst-011</id>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <date>2026-03-26</date>
    <status>superseded</status>
    <!-- Superseded 2026-04-02. Validation covered piecemeal by ADHC_HISTRY diagnostics, RPS reconciliation, ADVI_PRICES runs, phantom exclusion fix. AE confirmed 04-02. -->
    <project_code>ADVI_GLDRST</project_code>
  </metadata>

  <objective>
    Validate gold layer data integrity after the full GLDRST migration.
    This is a READ-ONLY validation task. Do NOT modify any code, S3 keys,
    or infrastructure. Produce a structured pass/fail report.
  </objective>

  <context>
    After .009 (migration gold rerun), all gold layer data exists at BOTH
    old and new S3 key paths (dual-write). This task validates that the
    data at the new paths is correct, complete, and matches expectations.

    The preflight snapshot at s3://opal-data-bd/gldrst/preflight/20260326-171617.json
    contains the pre-migration baseline (10,886 gold keys with version IDs).
  </context>

  <depends_on>.009 (migration gold rerun must complete successfully)</depends_on>

  <scope>
    Run the following validation checks. Report each as PASS or FAIL with
    evidence (row counts, checksums, sample values).

    ## Check 1: Core Parquet Schema Validation

    For each of these parquets at their NEW path, verify the schema (column
    names and dtypes) matches the expected schema:

    - gold/dimensions/accounts_dimension_latest.parquet
    - gold/dimensions/advisor_assignments_history.parquet
    - gold/dimensions/client_dimension.parquet
    - gold/timeseries/client_performance.parquet
    - gold/timeseries/account_performance.parquet
    - gold/views/nna_aua_by_advisor.parquet
    - gold/views/rel_architect_lookup.parquet
    - gold/views/client_tax_liability.parquet

    Method: download each parquet, read with pandas, print df.dtypes.
    Compare against the SAME file at the OLD path. Schemas must match exactly.

    ## Check 2: Row Count Comparison (New vs Old)

    For each core parquet above, compare row counts between old and new paths.
    They must be identical (migration does not add or remove rows).

    ## Check 3: AUA Reconciliation

    Read gold/timeseries/client_performance.parquet (new path).
    Compute total AUA as of the most recent date.
    Compare against gold/client_performance.parquet (old path).
    Tolerance: must match within 0.01% (rounding only).

    ## Check 4: Pre-Computed Views Completeness

    Count the number of _views.json files under gold/client_timeseries/.
    Count the number of _composition.json files under gold/client_timeseries/.
    Compare against the total number of unique relationship_ids in
    client_performance.parquet. Coverage should be >95%.

    For 5 sample relationship IDs, download the _views.json and verify:
    - Valid JSON
    - Contains quarterly, monthly, and annual period arrays
    - Each period has date, aua, nna fields
    - Values are numeric and non-null

    ## Check 5: Entity Key Completeness

    Count advisor entity keys at gold/entities/advisors/*/composition.json.
    Compare against distinct advisor count in rel_architect_lookup.parquet.
    Coverage should be >95%.

    Count client entity keys at gold/entities/clients/*/timeseries.json.
    Compare against distinct relationship_id count in client_performance.parquet.
    Coverage should be >95%.

    ## Check 6: Pipeline Manifest

    Read gold/meta/pipeline-manifest.json (if .006 was deployed).
    Verify it contains entries for all 16 gold scripts.
    Verify each entry has: script_name, status, row_count, s3_keys_written, duration_seconds.

    If .006 was not yet deployed, mark as SKIP (not FAIL).

    ## Check 7: Partitioned Timeseries

    Count files under gold/timeseries/positions_cube/.
    Count files under gold/timeseries/holdings_lots/.
    Both should have >30 files (one per recent trading day).
    Compare counts against old paths (gold/positions_cube/, gold/holdings_lots/).

    ## Check 8: No Orphaned Keys

    Run verify_migration.py gate3 --verbose.
    All checks must pass.
  </scope>

  <deliverable>
    A structured validation report in your session log with:
    - Each check: PASS/FAIL/SKIP with evidence
    - Summary: X/8 checks passed
    - If any FAIL: root cause analysis and which TO (.001-.009) likely introduced the issue
    - Final verdict: CLEAR or BLOCKED (with blocking reason)

    Report to COO via send_message when complete.
  </deliverable>

  <constraints>
    - READ-ONLY. Do not modify any files, S3 keys, or code.
    - Do not run gold layer scripts. Do not invoke Lambdas.
    - Download parquets to /tmp for analysis, then delete local copies.
    - Use the preflight snapshot for baseline comparison where needed.
  </constraints>
</task_order>
```
