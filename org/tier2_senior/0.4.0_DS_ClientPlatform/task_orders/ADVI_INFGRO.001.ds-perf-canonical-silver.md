<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.001</id>
    <project>ADVI_INFGRO</project>
    <title>Build INF_C_03.performance_canonical — new silver script from bronze/performance/</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>complete</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P0</priority>
    <estimated_effort>4-6 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §4.3 + §6.TO-INFGRO.001</ref>
    <ref type="taxonomy_yaml">data/orion/scripts/silver/orion_cashflow_taxonomy.yaml (upstream; Stage 0 output)</ref>
    <ref type="bronze_input">bronze/performance/{date}.parquet (with summaries block post TO-INFGRO.002)</ref>
    <ref type="silver_output">silver/performance_dim/{date}.parquet</ref>
    <ref type="gates">TO-INFGRO.000 COMPLETE (ece8e184b). TO-INFGRO.002 COMPLETE (DS~C same lane — do 002 first).</ref>
    <ref type="pattern">INF_C_01.canonical_nna.py — structural analogue (same silver layer, same date-partitioned pattern)</ref>
  </references>

  <context>
    ADVI_INFGRO decomposes AUA growth into NNA + Return + epsilon. The NNA leg is
    already handled by INF_C_01 (refactored in TO-INFGRO.000). The Return leg requires
    a new silver script: INF_C_03.performance_canonical.

    INF_C_03 reads bronze/performance/{date}.parquet (pulled by the Orion client
    performance REST puller) and produces silver/performance_dim/{date}.parquet. The
    critical design decision is: capture vendor-computed return data (both TWR factors
    AND the dollar gain from the summaries block) so that INF_C_02 (TO-003) can use
    vendor dollar directly rather than a rough approximation.

    Both INF_C_01 (NNA) and INF_C_03 (Return) read from orion_cashflow_taxonomy.yaml —
    though INF_C_03's primary dependency is the performance bronze, not the transaction
    taxonomy. The YAML is referenced to confirm the cashflow taxonomy doesn't
    accidentally double-count returns as NNA (taxonomy shows which type_desc values
    are Return-bucket, ensuring no overlap).

    Architectural invariant (PRD §3, Appendix C.4): INF_C_03 must read from the same
    orion_cashflow_taxonomy.yaml that INF_C_01 uses. No forked classification hardcoded
    inside INF_C_03 — both scripts point at the YAML as single source of truth.
  </context>

  <scope>
    <step>
      Read INF_C_01.canonical_nna.py to understand the structural pattern:
        - Date-partitioned read from bronze/silver
        - Per-date processing loop or date-range arg
        - Output partitioned by date
        - from __future__ import annotations header
        - coerce_silver_ids() call on all *_id columns before writing parquet
      Mirror this pattern in INF_C_03.
    </step>
    <step>
      Sample-read bronze/performance/{date}.parquet (post TO-INFGRO.002 amendment)
      to understand the actual schema including summaries-block columns.
      List all available columns and verify:
        - TWR factor columns present (weekly compounding factors)
        - summaries_gain_dollar (or equivalent) present for at least some accounts
        - client_id column present (for join keys)
    </step>
    <step>
      Author data/orion/scripts/silver/INF_C_03.performance_canonical.py.
      Required structure:
        - from __future__ import annotations as first import
        - Read orion_cashflow_taxonomy.yaml (to confirm Return-bucket type_descs;
          use only for reference/logging — INF_C_03 does NOT filter transactions,
          it reads performance data directly)
        - Date-partitioned processing: for each date in bronze/performance/,
          read the parquet and produce silver/performance_dim/{date}.parquet
        - Output schema per PRD §4.3:
            client_id (string)
            period_end_date (date)
            twr_factor_period (float)
            dollar_gain_period (float, nullable — from summaries block preferred; null if absent)
            period_basis (string — calendar quarter / fiscal / rolling-365)
            gross_or_net (string — gross-of-fees / net-of-fees per Orion config)
        - Apply coerce_silver_ids(['client_id']) before writing
        - Implement walk-back-to-healthy-snapshot (Appendix C.1): if target-date
          bronze partition has all-null TWR factors or zero rows, walk back to
          most-recent healthy partition rather than emit empty. Log when walkback occurs.
        - Skip-existing logic: if silver/performance_dim/{date}.parquet already exists
          and is non-empty, skip (idempotent re-runs)
    </step>
    <step>
      Validate output on a sample date:
        - silver/performance_dim/{date}.parquet exists
        - client_id populated for all rows (coerced)
        - twr_factor_period > 0 for all non-null rows (weekly factor sanity)
        - dollar_gain_period non-null for at least the advisors where summaries block was present
        - Row count matches expected account count (~848 active Inflection accounts)
    </step>
    <step>
      Run pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/silver/INF_C_03.performance_canonical.py`
      All three must pass: py_compile + AST undefined-name scan + ruff.
      Confirm coerce_silver_ids() is called (AST gate enforces this for build_* functions;
      your top-level function must also call it).
    </step>
    <step>
      S3 upload via `.tools/safe-deploy.sh` per ADHC_DSFLOW.005.
      Verify MATCH via `comp-pipescript deployed INF_C_03`.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-pipescript io INF_C_01 (understand analogue pattern)
      - Read bronze/performance/ sample (schema discovery)
      - Read orion_cashflow_taxonomy.yaml (confirm Return-bucket type_descs for reference)
    </phase>
    <phase name="before_commit">
      - .tools/ds-commit-gate.sh INF_C_03.performance_canonical.py (EXIT 0 required)
      - Verify from __future__ import annotations present
      - Verify coerce_silver_ids() called on client_id
    </phase>
    <phase name="after_commit">
      - comp-pipescript deployed INF_C_03 (MATCH required)
      - Sample read of silver/performance_dim/{date}.parquet — confirm schema + non-null twr_factor_period
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    DS~A (TO-INFGRO.003) will read silver/performance_dim/ produced by this TO.
    MCP DS~A when INF_C_03 silver/performance_dim/ is confirmed on S3 and schema is
    stable. DS~A must NOT start TO-003 until this TO signals RAVC2-complete with
    silver/performance_dim/ sample path + schema confirmation.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">silver/performance_dim/{date}.parquet exists for all dates with bronze coverage
      (or most-recent healthy walkback logged where bronze is stale/empty).</criterion>
    <criterion id="AC2">Output schema matches PRD §4.3: client_id (string/Int64), period_end_date,
      twr_factor_period, dollar_gain_period (nullable), period_basis, gross_or_net.</criterion>
    <criterion id="AC3">twr_factor_period > 0 for all non-null rows in sample validation.</criterion>
    <criterion id="AC4">dollar_gain_period non-null for at least one advisor's clients where
      summaries block was populated by TO-INFGRO.002.</criterion>
    <criterion id="AC5">coerce_silver_ids(['client_id']) called — confirmed by AST gate PASS.</criterion>
    <criterion id="AC6">comp-pipescript deployed MATCH post-S3-upload.</criterion>
    <criterion id="AC7">Pre-commit gate PASS (0 errors across all three checks).</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log in org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
    Must include Compiler Tools section. Report twr_factor_period range + dollar_gain_period
    non-null rate on sample date in session log (first empirical performance_dim characterization).
  </session_log_requirement>
</task_order>
