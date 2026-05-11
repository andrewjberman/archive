<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.003</id>
    <project>ADVI_INFGRO</project>
    <title>Extend INF_C_02.client_performance with 3-field GRO decomposition (NNA + Return + epsilon)</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>staged</status>
    <dispatch_held>true</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P0</priority>
    <estimated_effort>4-5 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §4.4 + §6.TO-INFGRO.003</ref>
    <ref type="script">data/orion/scripts/gold/INF_C_02.client_performance.py</ref>
    <ref type="current_output">gold/timeseries/client_performance.parquet</ref>
    <ref type="new_inputs">silver/performance_dim/{date}.parquet (TO-001 output); silver/canonical_nna/ (existing INF_C_01 output)</ref>
    <ref type="downstream">INF_C_04, INF_C_06, INF_D_00, INF_D_00b, INF_D_00d, INF_D_04 (86 total downstream nodes per comp-blast)</ref>
    <ref type="gates">TO-INFGRO.000 COMPLETE (ece8e184b). TO-INFGRO.001 COMPLETE — DS~C MCP-signals RAVC2 with silver/performance_dim/ sample path + schema.</ref>
  </references>

  <context>
    INF_C_02.client_performance currently produces gold/timeseries/client_performance.parquet
    with per-client AUA timeseries. CRITICAL: this script has 86 downstream nodes
    (comp-blast result). The extension MUST be additive — new columns only, no
    modification of existing column names, types, or semantics.

    The three new fields to add per (client, period):
      - nna_$ (float) — client-level NNA from silver/canonical_nna/ (INF_C_01 output)
      - return_pct_twr (float) — vendor TWR from silver/performance_dim/ (INF_C_03 output)
      - return_$ (float) — vendor dollar gain preferred (summaries block via INF_C_03);
                          fallback: aua_start_$ * return_pct_twr (rough; acknowledged imperfect)
      - epsilon_$ (float) — measured residual: aua_growth_$ - nna_$ - return_$
      - epsilon_data_quality (string) — "GREEN" if abs(epsilon_$) < $1,000 OR
                                       abs(epsilon_$) / aua_start < 0.005; else "YELLOW"

    The architectural invariant: AUA_growth_$ = NNA_$ + return_$ + epsilon_$, where
    epsilon_$ is MEASURED not assumed zero.

    Both new source reads (silver/canonical_nna/ and silver/performance_dim/) are
    date-partitioned. The join key is client_id. Period alignment: align on period_end_date.
  </context>

  <scope>
    <step>
      Read INF_C_02.client_performance.py in full.
      Understand: date-range args, inner loop structure, current column set, how
      accounts_dimension_latest.parquet is used (the only current read).
      Note all existing column names — these MUST be preserved unchanged.
    </step>
    <step>
      Run comp-pipescript io INF_C_02 and comp-blast INF_C_02 to confirm:
        - Current reads: gold/dimensions/accounts_dimension_latest.parquet
        - Current writes: gold/timeseries/client_performance.parquet
        - 86 downstream nodes (confirm count)
      Read the COLUMN GAPS section carefully — any columns accessed but not loaded
      are regressions waiting to happen.
    </step>
    <step>
      Extend INF_C_02 to also read, per date:
        - silver/canonical_nna/{date}.parquet (INF_C_01 output; contains client_id + nna_$ per period)
        - silver/performance_dim/{date}.parquet (INF_C_03 output; contains client_id + twr_factor_period + dollar_gain_period)
      Join both on client_id + period (align period_end_date).

      Handle missing joins gracefully:
        - If a client has no canonical_nna for the period: nna_$ = 0 (no transactions = no NNA)
        - If a client has no performance_dim entry: return_pct_twr = null, return_$ = null,
          epsilon_$ = null, epsilon_data_quality = "MISSING_PERF"
      Log counts of null-join clients per date in session log.
    </step>
    <step>
      Compute the 5 new columns:
        nna_$ = silver/canonical_nna/{date}.nna_net_$ (or equivalent column — check actual column name)
        return_pct_twr = silver/performance_dim/{date}.twr_factor_period (annualized vendor TWR)
        return_$ = COALESCE(silver/performance_dim/{date}.dollar_gain_period, aua_start_$ * return_pct_twr)
        aua_growth_$ = aua_end_$ - aua_start_$ (must use existing aua columns — do not recompute)
        epsilon_$ = aua_growth_$ - nna_$ - return_$
        epsilon_data_quality = "GREEN" if (abs(epsilon_$) &lt; 1000 OR
                                          (aua_start_$ > 0 AND abs(epsilon_$)/aua_start_$ &lt; 0.005))
                               else "YELLOW" (null if return_$ is null)
    </step>
    <step>
      Append new columns to existing output WITHOUT removing or renaming anything.
      Verify with a row-count + schema check: len(output.columns) == len(old_output.columns) + 5.
    </step>
    <step>
      Run on a sample date. Report in session log:
        - Count of GREEN / YELLOW / MISSING_PERF epsilon classifications
        - Median abs(epsilon_$), p95, p99, max
        - Firm-level totals: sum(nna_$) + sum(return_$) + sum(epsilon_$) vs sum(aua_growth_$)
          (these should be equal by construction)
    </step>
    <step>
      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/scripts/gold/INF_C_02.client_performance.py`
      Then safe-deploy + comp-pipescript deployed MATCH.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-pipescript io INF_C_02 (COLUMN GAPS section mandatory — catch missing reads)
      - comp-blast INF_C_02 (confirm 86 downstream nodes; additive-only extension means zero new blast)
      - comp-pipescript postdeps INF_C_02 (check if any post-steps required after INF_C_02 runs)
    </phase>
    <phase name="before_commit">
      - .tools/ds-commit-gate.sh INF_C_02.client_performance.py (EXIT 0 required)
      - Verify from __future__ import annotations present
    </phase>
    <phase name="after_commit">
      - comp-pipescript deployed INF_C_02 (MATCH required)
      - comp-validate INF_C_02 --artifact /tmp/client_performance.parquet if validate config exists
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    Upstream dependency: DS~C TO-INFGRO.001 must signal RAVC2-complete with silver/performance_dim/
    schema before DS~A starts this TO. Do NOT begin until DS~C's MCP arrives.
    silver/canonical_nna/ is existing INF_C_01 output — no new coordination needed for that read.

    Downstream: DS~A TO-INFGRO.004 (INF_D_00c extension) reads from this TO's output.
    MCP DS~A TO-004 receiver when gold/timeseries/client_performance.parquet schema extension
    is live and confirmed on S3.

    BLAST WARNING: 86 downstream nodes. Extension must be purely additive.
    If any existing column is modified (rename, type change, removal), flag to CTO immediately
    before committing — blast radius makes this a coordination event.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">gold/timeseries/client_performance.parquet schema includes 5 new columns:
      nna_$, return_pct_twr, return_$, epsilon_$, epsilon_data_quality.</criterion>
    <criterion id="AC2">All pre-existing columns unchanged (name, type, semantics) — spot-check
      5 pre-existing column values before and after on a sample row.</criterion>
    <criterion id="AC3">epsilon_$ = aua_growth_$ - nna_$ - return_$ holds exactly (float tolerance
      within $0.01) for all rows where return_$ is non-null.</criterion>
    <criterion id="AC4">Firm-level sum check: sum(nna_$) + sum(return_$) + sum(epsilon_$) == sum(aua_growth_$)
      within $1 rounding tolerance for sample date.</criterion>
    <criterion id="AC5">Session log reports epsilon distribution: median + p95 + p99 + max abs(epsilon_$).</criterion>
    <criterion id="AC6">comp-pipescript deployed MATCH.</criterion>
    <criterion id="AC7">Pre-commit gate PASS.</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log mandatory. Must include:
    - Compiler Tools section (all three phases)
    - Epsilon distribution table (median + p95 + p99 + max) on sample date
    - Null-join counts (clients missing performance_dim or canonical_nna)
    - Firm-level NNA + Return + epsilon vs AUA growth reconciliation
  </session_log_requirement>
</task_order>
