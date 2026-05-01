<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.006</id>
    <project>ADVI_HISTBF</project>
    <title>Wave A — Performance silver (weekly TWR time series): pull_inflection_performance_rest.py + convert_performance_to_silver.py</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>complete</status><!-- DS~B 2026-05-01: convert_performance_to_silver.py authored, ds-commit-gate clean, committed 3204797c2, S3 MATCH opal-data-inf/code/silver/convert_performance_to_silver.py MD5=f46821e447f34d26c1a8bfc78e54cb96. Docstring patches by DS~A at f2c75eb98. COO RAVC4 accepted. -->
    <priority>high</priority>
    <estimated_effort>0.5-1d (Wave A local code; no EC2)</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling">CTO arch ruling 2026-04-30: 2 separate TOs — transactions + performance have distinct schemas, grains, validate configs</ref>
    <ref type="dsb_discovery">DS~B Phase 0 final 39372ff12: GET /api/v1/Portfolio/Clients/{clientId}/Performance; returns 309 weekly TWR factors from inception (2020-06-04) in one call per client; 314 clients; DO NOT request 5y+ windows (times out); no chunking needed</ref>
    <ref type="dsb_silver_spec">DS~B Phase 2b spec: weekly-factor time series per client; client-level grain; inception-to-date accumulation; silver path silver/orion-rest/performance_weekly/{client_id}/data.parquet</ref>
    <ref type="rate_limiter">data/orion/scripts/bronze/rate_limiter.py (a1e268511)</ref>
    <ref type="jwt_guard">data/orion/manual_api/jwt_freshness.py (81a7a5684)</ref>
    <ref type="wave_structure">Wave A (code) → Gate → AE chain reg → Wave B (AE EC2) → Wave C (silver execution)</ref>
  </references>

  <context>
    DS~B discovery confirmed GET /Clients/{id}/Performance returns the full inception-to-date weekly TWR factor series in a single call per client — 309 weekly factors from 2020-06-04, no pagination. 314 clients × 1 call = 314 total calls. Estimated ~5min at 1 req/s. Trivially fast.

    HARD LIMIT: do NOT request 5y+ rolling windows. The endpoint times out. Single-call inception-to-date is the correct approach — it returns all factors without a window constraint.

    The existing Envision-based performance silver (rolling-window TWR summary at snapshot_date) is a different artifact serving a different use case. The new silver here stores the actual weekly factor time series, enabling historical portfolio performance reconstruction at any date.

    This is Wave A code work — local only, no EC2. Wave C execution gates on Wave B bronze completion.
  </context>

  <scope>

    1. **pull_inflection_performance_rest.py** at data/orion/manual_api/pull_inflection_performance_rest.py:
       - GET /api/v1/Portfolio/Clients/{clientId}/Performance per client (inception-to-date; no window param)
       - Iterates all 314 clients (read client_id list from accounts_v2 silver or dedicated client dim)
       - Accepts: --cycle-id UUID (telemetry)
       - HARD LIMIT: single call per client — no date window params. Do not add --start/--end to this script.
       - Integrates AdaptiveRateLimiter: state file s3://opal-data-inf/orion/rate_limit_state_performance.json
       - Integrates CallTelemetry: per-call capture
       - assert_fresh_or_exit() at startup
       - Output: s3://opal-data-inf/bronze/orion-api-v2/performance/{client_id}/data.json (per-client JSON)
       - Status: 404 = client has no performance data (treat as success; log SKIP); 401/429/5xx = rate_limiter failure path
       - from __future__ import annotations; ds-commit-gate.sh clean

    2. **convert_performance_to_silver.py** at data/orion/scripts/silver/convert_performance_to_silver.py:
       - Reads all per-client bronze JSONs from s3://opal-data-inf/bronze/orion-api-v2/performance/
       - Explodes to weekly-factor rows; deduplicates on (client_id, week_date)
       - Silver schema (one row per client per week):
         - client_id (str)
         - week_date (date — the period end date of the weekly factor)
         - twr_factor (float — weekly return factor; cumulative product = inception-to-date TWR)
         - cumulative_twr (float — derived: product of all factors from inception to week_date)
         - inception_date (date — first week_date in the series; 2020-06-04 expected)
         - weeks_from_inception (int — ordinal position)
       - Output: s3://opal-data-inf/silver/orion-rest/performance_weekly/client_id={client_id}/data.parquet (per-client partition)
       - Accepts: --upload
       - from __future__ import annotations; ds-commit-gate.sh clean

    3. **S3 upload + deployment gate**:
       - aws s3 cp pull_inflection_performance_rest.py s3://opal-data-inf/code/bronze/
       - aws s3 cp convert_performance_to_silver.py s3://opal-data-inf/code/silver/
       - comp-pipescript deployed pull_inflection_performance_rest → MATCH
       - comp-pipescript deployed convert_performance_to_silver → MATCH
       - MCP AE 0.6.1 with MATCH confirmation (chain reg gate signal — combine with HISTBF.005 MATCH signal into one MCP if both ship same session)

    4. **Pre-commit gate**: ds-commit-gate.sh + from __future__ import annotations on both files.

  </scope>

  <acceptance_criteria>
    1. pull_inflection_performance_rest.py shipped: 314 clients, single-call inception-to-date, rate-limiter + JWT guard, no 5y+ window requests.
    2. convert_performance_to_silver.py shipped: weekly-factor time series schema; cumulative_twr derived field; per-client S3 partition.
    3. comp-pipescript deployed MATCH on both scripts.
    4. MCP AE 0.6.1 with MATCH confirmation sent (may combine with HISTBF.005 signal).
    5. Pre-commit gate PASS.
    6. RAVC4 to COO with: commit hashes, S3 upload paths, comp-pipescript MATCH exit codes, silver schema summary.

    Wave C execution (actual silver conversion run) is OUT OF SCOPE — runs after Wave B bronze completes.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>New scripts producing new bronze + silver artifacts not previously extant; existing Envision-based performance silver (rolling-window summary) is a separate artifact and coexists; no downstream consumers read the new weekly-factor silver until gold scripts are updated to consume it</no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io [accounts_v2 or client dim silver path] — confirm client_id field for iteration list</check>
    </before_write>
    <before_commit>
      <check>ds-commit-gate.sh pull_inflection_performance_rest.py convert_performance_to_silver.py</check>
      <check>from __future__ import annotations on both files</check>
    </before_commit>
    <after_commit>
      <check>comp-pipescript deployed pull_inflection_performance_rest → MATCH</check>
      <check>comp-pipescript deployed convert_performance_to_silver → MATCH</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination_protocol>
      DS BASE owns Wave A code entirely. Combine MCP AE 0.6.1 MATCH confirmation with HISTBF.005 signal if both ship same session — one AE chain reg update covers all 5 dims. Direct MCP to DS~B for any endpoint schema questions (HAR + probe logs in their session).
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
