<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.001b</id>
    <project>ADVI_INFREL</project>
    <title>pull_inflection_performance_dim.py — bronze producer + orchestrator DimSpec wiring</title>
    <issued_to>0.4.0_DS_ClientPlatform~B</issued_to>
    <issued_to_secondary>0.6.1_AE_PartnerETL</issued_to_secondary>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>complete</status><!-- COO-authored per CTO spec 20260506T140423Z. Fix B follow-on from INFREL.001 consumer trace (3 active consumers: INF_D_00c + INF_D_02 + INF_D_04 all read silver/api_dims/performance/). Option 2 (remove from SILVER_BUILDERS) BLOCKED — Option 1: author bronze producer script. DS~B LEAD (bronze script authoring). AE 0.6.1 SECONDARY (DimSpec wiring + validation). Non-blocking on Fix A+C+D. Fix D (tax exit=2) sequential within DS~B lane is fine. -->
    <priority>normal</priority><!-- NOT P0. All 3 consumers have graceful fallback (WARN + null). Performance silver stale since 2026-04-28 with no production breakage. Ship at normal cadence. -->
    <estimated_effort>~0.5d (DS~B script authoring + gate); ~0.25d (AE 0.6.1 DimSpec wiring + validation)</estimated_effort>
  </metadata>

  <references>
    <ref type="predecessor">ADVI_INFREL.001 Fix B — consumer trace surfaced 3 active gold consumers (INF_D_00c + INF_D_02 + INF_D_04); Option 2 pre-condition tripped → Option 1 ruling from CTO 20260506T140423Z</ref>
    <ref type="cto_ruling">1.0.0_SA_CTO message 20260506T140423Z — full spec delivered; COO authors TO</ref>
    <ref type="reference_script">data/orion/manual_api/pull_inflection_billing_dim.py — model for auth pattern + JWT lifecycle</ref>
    <ref type="silver_builder">infra/aws/lambda/inf-silver-chain/lambda_function.py — SILVER_BUILDERS `build_performance` function; orchestrator.py DimSpec wire-in point</ref>
    <ref type="rate_ceiling">docs/data/inflec_histbf_rate_limiter_constants.md + commit 10dc81e9b — empirical ≥300 RPS vendor ceiling; set INITIAL_RATE=30</ref>
    <ref type="consumers">INF_D_00c + INF_D_02 + INF_D_04 — all read silver/api_dims/performance/; currently emit graceful-fallback WARN; will auto-clear post fix</ref>
    <ref type="gold_freshness">gold_freshness_config.yaml silver/api_dims/performance/ monitor entry — stays valid post fix; data resumes flowing without edit</ref>
  </references>

  <context>
    INFREL.001 Fix B consumer trace found 3 active gold consumers reading `silver/api_dims/performance/`.
    The `build_performance` function exists in SILVER_BUILDERS but the bronze input
    (`bronze/orion-api/{date}/performance_dim.csv`) was never being written — the orchestrator had
    no DimSpec entry for performance_dim. Result: silver builder silently skips performance every run,
    gold scripts emit WARN + null fallback on every chain fire (since 2026-04-28 when gold consumers
    were added). No production breakage — all consumers have graceful fallback.

    Fix: author the missing bronze producer script + wire DimSpec in orchestrator.py.
    The silver builder (build_performance) already exists and will resume working once bronze data flows.
  </context>

  <scope_ds_b note="DS~B lead — bronze script authoring + pre-commit gate + S3 upload">

    <phase id="0" when="before authoring">
      <step>Run `comp-pipescript io pull_inflection_billing_dim.py` to confirm the reference script's
      I/O shape. This establishes the auth pattern, JWT lifecycle, S3 write path, and rate_limiter
      constructor usage to mirror in the new script.</step>
      <step>Cross-ref `convert_orion_api_to_silver.py` `build_performance` function for the column
      requirements silver expects. Confirm the Orion API field set maps correctly.</step>
    </phase>

    <phase id="1" when="authoring">
      <step>
        Author `data/orion/manual_api/pull_inflection_performance_dim.py` modeled on `orion_billing_dim.py`:
        - Same Orion API auth pattern (JWT freshness check + token refresh)
        - Same rate_limiter constructor pattern — set `INITIAL_RATE = 30` (NOT default 1 RPS).
          Rationale: empirical vendor ceiling ≥300 RPS confirmed (commit 10dc81e9b + rate constants doc);
          paying the 1 RPS rediscovery tax on every cron fire wastes wall time unnecessarily.
        - Output path: `bronze/orion-api/{date}/performance_dim.csv` (date = today UTC ISO)
        - Confirm `from __future__ import annotations` present (Rule 15)
      </step>
    </phase>

    <phase id="2" when="pre-commit gate">
      <step>Run `.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_performance_dim.py`
      — py_compile + AST undefined-name scan + ruff py39. Must exit 0 before commit.</step>
    </phase>

    <phase id="3" when="commit + S3 upload">
      <step>Commit via safe-commit.sh:
        `.tools/safe-commit.sh --author "0.4.0_DS_ClientPlatform~B &lt;0.4.0_DS_ClientPlatform~B@opal.agent&gt;" \
            -m "feat(ADVI_INFREL.001b): pull_inflection_performance_dim.py bronze producer

        New Orion bronze script for performance_dim. Fills the missing DimSpec gap
        that caused silver/api_dims/performance/ to stay stale since 2026-04-28.
        INITIAL_RATE=30 per empirical rate-ceiling finding (10dc81e9b)." \
            -- data/orion/manual_api/pull_inflection_performance_dim.py`
      </step>
      <step>Push to CLOUD: `git push origin CLOUD`</step>
      <step>S3 upload: `aws s3 cp data/orion/manual_api/pull_inflection_performance_dim.py s3://opal-data-inf/code/gold/pull_inflection_performance_dim.py`
      (confirm bucket path with comp-pipescript or existing billing_dim upload path)</step>
      <step>RAVC3 to AE 0.6.1: commit SHA + S3 path + field mapping confirmation. AE 0.6.1 proceeds with DimSpec wiring on receipt.</step>
    </phase>

  </scope_ds_b>

  <scope_ae_0_6_1 note="AE 0.6.1 secondary — DimSpec wiring + freshness validation">

    <phase id="1" when="after DS~B RAVC3">
      <step>Add DimSpec entry for `performance_dim` in `orchestrator.py` (inf-bronze-runner).
      Pattern: mirror the `billing_dim` or `accounts_v2` DimSpec entry (same csv output prefix pattern).</step>
      <step>Confirm `build_performance` reference in `SILVER_BUILDERS` (inf-silver-chain lambda_function.py)
      still resolves correctly — only the bronze input was missing; the builder function exists.
      No lambda edit should be needed; verify via grep.</step>
      <step>Confirm `gold_freshness_config.yaml` `silver/api_dims/performance/` monitor entry remains valid
      (no edit needed — data will start flowing once DimSpec wires + bronze cron fires).</step>
      <step>EC2 deploy orchestrator.py change per EC2_DEPLOYMENT_PROTOCOL.md (S3 upload + SSM).</step>
    </phase>

    <phase id="2" when="post-deploy validation">
      <step>`comp-pipescript deployed pull_inflection_performance_dim.py` — MATCH confirm on inf-bronze-runner.</step>
      <step>`comp-pipescript consumers silver/api_dims/performance/` — re-confirm consumer set hasn't drifted (should still be INF_D_00c + INF_D_02 + INF_D_04).</step>
      <step>After next inf-bronze-runner cron fire (12:43 UTC): confirm `bronze/orion-api/{date}/performance_dim.csv` exists with non-empty payload.</step>
      <step>After silver chain fires post-bronze: confirm `silver/api_dims/performance/snapshot_date={date}/data.parquet` written.</step>
      <step>24h post-ship: confirm INF_D_00c / INF_D_02 / INF_D_04 CW logs no longer emit `WARN: silver/api_dims/performance/ partition missing`.</step>
      <step>Confirm `gold_freshness_config.yaml` monitor for `silver/api_dims/performance/` clears alarm state.</step>
      <step>RAVC5 to COO with: orchestrator.py commit + EC2 deploy confirmation + cron fire evidence + silver partition confirmation + gold WARN cleared.</step>
    </phase>

  </scope_ae_0_6_1>

  <acceptance_criteria>
    <criterion id="AC1">Bronze cron fire writes `bronze/orion-api/{TODAY}/performance_dim.csv` with non-empty payload + schema matching `build_performance` column requirements.</criterion>
    <criterion id="AC2">Silver chain Lambda fires post-bronze and writes `silver/api_dims/performance/snapshot_date={TODAY}/data.parquet`.</criterion>
    <criterion id="AC3">24h post-ship: INF_D_00c + INF_D_02 + INF_D_04 stop emitting `WARN: silver/api_dims/performance/ partition missing` in CW logs.</criterion>
    <criterion id="AC4">`gold_freshness_config.yaml` monitor for `silver/api_dims/performance/` clears its alarm state.</criterion>
    <criterion id="AC5">Empirical RPS measurement during first cron fire confirms 30+ RPS sustained without 429 (validates INITIAL_RATE=30 for this endpoint family).</criterion>
    <criterion id="AC6">DS~B: pre-commit gate exit 0; commit + push to CLOUD; S3 upload + deployed MATCH.</criterion>
    <criterion id="AC7">AE 0.6.1: orchestrator.py DimSpec entry + EC2 deployed; RAVC5 to COO with full evidence package.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0_ds_b" when="DS~B before authoring">comp-pipescript io pull_inflection_billing_dim.py — confirm reference I/O shape</phase>
    <phase id="2_ds_b" when="DS~B before commit">.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_performance_dim.py — exit 0 required</phase>
    <phase id="2_ae" when="AE 0.6.1 post-deploy">comp-pipescript deployed pull_inflection_performance_dim.py — MATCH required; comp-pipescript consumers silver/api_dims/performance/ — consumer set re-confirm</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>DS~B authors and S3-uploads script, then RAVC3 to AE 0.6.1. AE 0.6.1 wires DimSpec + deploys. Sequential handshake.</item>
    <item>Non-blocking on INFREL.001 Fix A+C+D (all independent paths). Fix D (DS~B tax exit=2 investigation) runs sequential within DS~B lane — this TO next-up after Fix D closes.</item>
    <item>No portal submodule changes. No Terraform changes from DS~B scope. AE 0.6.1 EC2 deploy per EC2_DEPLOYMENT_PROTOCOL.md.</item>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT set INITIAL_RATE=1 (default discovery rate). The empirical ceiling is confirmed ≥300 RPS. Use INITIAL_RATE=30.</rule>
    <rule>Do NOT modify the SILVER_BUILDERS build_performance function — it already exists and is correct. Only the bronze input was missing.</rule>
    <rule>Do NOT touch gold_freshness_config.yaml — the monitor entry is already correct and will clear once data flows.</rule>
  </do_not>

  <go_signal>
    <issued_at>20260506T~1410Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO — non-P0, normal cadence. DS~B executes Fix D (tax exit=2) first if in flight; INFREL.001b next-up within DS~B lane. AE 0.6.1 executes DimSpec wiring after DS~B RAVC3.</message>
  </go_signal>
</task_order>
