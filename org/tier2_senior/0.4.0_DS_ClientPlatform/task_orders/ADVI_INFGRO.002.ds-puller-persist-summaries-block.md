<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFGRO.002</id>
    <project>ADVI_INFGRO</project>
    <title>Amend pull_inflection_performance_rest.py — persist summaries block to bronze</title>
    <issued_to>0.4.0_DS_ClientPlatform~C</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-11</issued_date>
    <status>pending</status>
    <dispatch_held>false</dispatch_held>
    <dispatch_note>Receiver routing TBD — COO bench-state check 2026-05-12 morning. DS~A + DS~C killed or STANDDOWN 2026-05-11 ~22:31Z. Do NOT pick up this TO until COO issues GO.</dispatch_note>
    <priority>P0</priority>
    <estimated_effort>1-2 hours</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFGRO_PRD.md §4.7 + §6.TO-INFGRO.002</ref>
    <ref type="script">data/orion/scripts/ (bronze puller — locate pull_inflection_performance_rest.py)</ref>
    <ref type="bronze_artifact">bronze/performance/{date}.parquet</ref>
    <ref type="gates">None — this is the foundation for TO-INFGRO.001</ref>
  </references>

  <context>
    The Orion REST puller that fetches client performance data currently calls
    `/api/v1/Portfolio/Clients/{clientId}/Performance` and persists the weekly
    TWR factor chain BUT DROPS the summaries block entirely. The summaries block
    contains vendor-computed dollar_gain and period-dollar return fields — the
    preferred-from-vendor source for `return_$` in the three-field decomposition.

    Without the summaries block in bronze, INF_C_03 (TO-INFGRO.001) can only
    derive `return_$` via the rougher approximation `aua_start * return_pct_twr`,
    which is acknowledged imperfect when there are cashflows during the period.
    Getting the vendor dollar directly from summaries is materially better.

    The fix is additive: extend the bronze schema with summaries-block columns;
    stop dropping the fields. Existing factor-chain columns are unchanged.
  </context>

  <scope>
    <step>
      Locate the bronze puller script. It may be under:
        - data/orion/scripts/bronze/ or data/orion/scripts/pull/
        - Search for pull_inflection_performance or similar pattern.
      Read the script to understand how the API response is currently parsed and
      which fields are kept vs dropped.
    </step>
    <step>
      Identify the summaries block in the API response structure. From DS~D's
      Stage 2 probe (2026-05-11), the endpoint `/api/v1/Portfolio/Accounts/{id}/Performance`
      returns `summaries[0].performance` with annualized TWR per window. The client-level
      endpoint has a similar structure. Identify:
        - summaries[].performance (float; annualized TWR for the period)
        - summaries[].gain or similar dollar-gain field (if present)
        - summaries[].period or summaries[].periodType (period label)
      Read the raw Orion API response by sampling one client's live response if needed.
    </step>
    <step>
      Amend the puller to persist all summaries-block fields alongside the existing
      factor-chain columns. Schema extension is additive — do NOT remove or rename
      existing columns.

      Recommended column additions to bronze/performance/{date}.parquet:
        - summaries_gain_dollar (float, nullable) — vendor dollar gain for primary period
        - summaries_performance_pct (float, nullable) — vendor annualized TWR for primary period
        - summaries_period_type (string, nullable) — period type label from vendor
      Exact field names depend on the actual API response structure you observe.
      Nullable = True for all summaries columns (not all accounts will have summaries).
    </step>
    <step>
      Run the amended puller against a sample of 5-10 client IDs covering at least
      one client from each advisor (Peter Lee / Patrick Murphy / Joe Brandenburg / IWM).
      Verify output:
        - Existing TWR factor columns unchanged (spot-check 2 rows).
        - New summaries columns populated where vendor provides (may be null for some accounts).
        - bronze/performance/{date}.parquet includes both old + new columns.
    </step>
    <step>
      Run the pre-commit gate: `.tools/ds-commit-gate.sh &lt;puller_script_path&gt;`.
      Gate must pass (py_compile + AST + ruff).
      Script must start with `from __future__ import annotations`.
    </step>
    <step>
      S3 upload the amended script via `.tools/safe-deploy.sh` per ADHC_DSFLOW.005.
      Verify SHA MATCH via `comp-pipescript deployed &lt;script_name&gt;`.
    </step>
  </scope>

  <compiler_tools_mandate>
    <phase name="before_write">
      - comp-pipescript io &lt;puller_script_name&gt; (confirm I/O profile; identify downstream if any)
      - Read bronze/performance/ sample to understand existing schema
    </phase>
    <phase name="before_commit">
      - .tools/ds-commit-gate.sh &lt;puller_script_path&gt; (py_compile + AST + ruff; EXIT 0 required)
      - Verify from __future__ import annotations present
    </phase>
    <phase name="after_commit">
      - comp-pipescript deployed &lt;puller_script_name&gt; (MATCH required before signaling complete)
      - Sample read of bronze/performance/{date}.parquet to confirm new columns present
    </phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <none/>
    This TO operates only on the bronze puller + bronze/performance/ artifact.
    No shared S3 artifacts with other active TOs. TO-INFGRO.001 (DS~C same lane)
    depends on this output but will not start until this TO closes.
  </cross_domain_coordination>

  <acceptance_criteria>
    <criterion id="AC1">bronze/performance/{date}.parquet rows post-amend include summaries-block
      columns (summaries_gain_dollar, summaries_performance_pct, or equivalent vendor field names).</criterion>
    <criterion id="AC2">Existing TWR factor columns unchanged — spot-check pre-amend vs post-amend
      for 2 sample rows shows bit-for-bit match on existing columns.</criterion>
    <criterion id="AC3">Sample run covers all 4 advisors' clients (at least 1 per advisor);
      at least 1 row shows non-null summaries_gain_dollar where vendor provides it.</criterion>
    <criterion id="AC4">Pre-commit gate PASS (0 errors).</criterion>
    <criterion id="AC5">comp-pipescript deployed MATCH post-S3-upload.</criterion>
  </acceptance_criteria>

  <session_log_requirement>
    Session log in org/tier2_senior/0.4.0_DS_ClientPlatform/logs/{date}/
    Must include Compiler Tools section with all Phase 1-3 tool runs and results.
  </session_log_requirement>
</task_order>
