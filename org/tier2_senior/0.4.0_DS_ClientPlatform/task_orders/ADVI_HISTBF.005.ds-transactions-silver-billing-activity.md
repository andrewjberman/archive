<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_HISTBF.005</id>
    <project>ADVI_HISTBF</project>
    <title>Wave A — Transaction silver (billing + activity): pull_inflection_transactions_rest.py + convert_transactions_to_silver.py</title>
    <issued_to>0.4.0_DS_ClientPlatform</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-04-30</issued_date>
    <status>complete</status><!-- DS~B 2026-05-01: convert_transactions_to_silver.py authored, ds-commit-gate clean, committed 3204797c2, S3 MATCH opal-data-inf/code/silver/convert_transactions_to_silver.py MD5=a2f67e3ac0ee6a244be29b434d6bab43. Docstring patches by DS~A at f2c75eb98. COO RAVC4 accepted. -->
    <priority>high</priority>
    <estimated_effort>0.5-1d (Wave A local code; no EC2)</estimated_effort>
  </metadata>

  <references>
    <ref type="cto_ruling">CTO arch ruling 2026-04-30: 2 separate TOs for Phase 2b (transactions + performance separate schemas)</ref>
    <ref type="dsb_discovery">DS~B Phase 0 final 39372ff12: GET /api/v1/Portfolio/Accounts/{accountId}/Transactions; transTypeId 24/110 (fees) + 8/51 (contributions/distributions); ~590 account calls; full history per call; no Envision async</ref>
    <ref type="dsb_silver_spec">DS~B Phase 2b spec: transaction-level silver (one row per event); account_id + household_id JOIN from accounts_v2; rep_id_is_historical=False flag; billing + activity combined from same endpoint</ref>
    <ref type="rate_limiter">data/orion/scripts/bronze/rate_limiter.py (a1e268511) — AdaptiveRateLimiter + CallTelemetry</ref>
    <ref type="jwt_guard">data/orion/manual_api/jwt_freshness.py (81a7a5684) — assert_fresh_or_exit()</ref>
    <ref type="wave_structure">Wave A (code) → Gate (DS S3 upload + comp-pipescript MATCH) → AE chain reg → Wave B (AE EC2 dispatch) → Wave C (silver execution)</ref>
  </references>

  <context>
    DS~B discovery (39372ff12) confirmed GET /Accounts/{id}/Transactions returns full transaction history per account in a single REST call. transTypeId values: 24 = Management Fee, 110 = Fee Credit, 8 = Contribution, 51 = Distribution. ~590 account calls total. Billing and activity are the same endpoint with different transTypeId filters — one pull script, one silver converter covering both.

    The existing Envision-based billing/activity silver builders (convert_orion_api_to_silver.py build_activity) store rolling-window aggregate buckets at snapshot_date — they CANNOT backfill transaction-level time series. New converter required.

    Rep attribution: REST /Transactions response has no rep_id field. Silver must JOIN against accounts_v2 silver (current-state mapping). All historical records carry current-state rep attribution. Acceptable for firm-level totals; disclose limitation for per-advisor views via rep_id_is_historical=False flag.

    This is Wave A code work — local only, no EC2. Execution (Wave C) gates on Wave B bronze completion.
  </context>

  <scope>

    1. **pull_inflection_transactions_rest.py** at data/orion/manual_api/pull_inflection_transactions_rest.py:
       - GET /api/v1/Portfolio/Accounts/{accountId}/Transactions per account
       - Iterates all accounts from accounts_v2 silver (reads silver parquet for account_id list)
       - No date filtering on the pull — retrieve full history per account; silver converter handles date filtering
       - Accepts: --cycle-id UUID (telemetry attribution)
       - Integrates AdaptiveRateLimiter (rate_limiter.py): state file s3://opal-data-inf/orion/rate_limit_state_transactions.json
       - Integrates CallTelemetry: per-call capture (timestamp, elapsed, status, bytes, record_count)
       - assert_fresh_or_exit() at startup (jwt_freshness.py)
       - Output: s3://opal-data-inf/bronze/orion-api-v2/transactions/{account_id}/data.json (per-account JSON; timestamp in filename)
       - Status code handling: 401/429/503/504 = failure (rate_limiter fallback); 200/206 = success; 404 = ambiguous (treat as success — account may have no transactions)
       - from __future__ import annotations; ds-commit-gate.sh clean

    2. **convert_transactions_to_silver.py** at data/orion/scripts/silver/convert_transactions_to_silver.py:
       - Reads all per-account bronze JSONs from s3://opal-data-inf/bronze/orion-api-v2/transactions/
       - Explodes to transaction-level rows; deduplicates on trans_id
       - Silver schema (one row per transaction event):
         - account_id (str)
         - household_id (str, JOIN from accounts_v2 silver)
         - rep_id (str, JOIN from accounts_v2 silver — current-state)
         - rep_id_is_historical (bool = False — machine-readable attribution caveat)
         - trans_id (str)
         - trans_date (date)
         - amount (float)
         - trans_type_id (int)
         - trans_type_desc (str) — derived from transTypeId: 24="Management Fee", 110="Fee Credit", 8="Contribution", 51="Distribution"
         - category (str) — derived: transTypeId 24/110 → "billing"; 8/51 → "activity"
       - Output: s3://opal-data-inf/silver/orion-rest/transactions/snapshot_date={YYYY-MM-DD}/data.parquet
         snapshot_date = date the silver conversion ran (not the transaction date)
       - Accepts: --snapshot-date YYYY-MM-DD (default: today); --upload
       - from __future__ import annotations; ds-commit-gate.sh clean

    3. **S3 upload + deployment gate**:
       - aws s3 cp pull_inflection_transactions_rest.py s3://opal-data-inf/code/bronze/
       - aws s3 cp convert_transactions_to_silver.py s3://opal-data-inf/code/silver/
       - comp-pipescript deployed pull_inflection_transactions_rest → MATCH
       - comp-pipescript deployed convert_transactions_to_silver → MATCH
       - MCP AE 0.6.1 with MATCH confirmation — this is the chain reg gate signal

    4. **Unit tests** (optional but preferred): test transTypeId→category mapping; test rep_id JOIN; test dedup on trans_id; test 404-as-success path.

    5. **Pre-commit gate**: ds-commit-gate.sh + from __future__ import annotations on both files.

  </scope>

  <acceptance_criteria>
    1. pull_inflection_transactions_rest.py shipped: iterates all accounts, rate-limiter + JWT guard integrated, output to s3 per-account JSON.
    2. convert_transactions_to_silver.py shipped: transaction-level schema with rep_id_is_historical flag; billing + activity both covered via category field.
    3. comp-pipescript deployed MATCH on both scripts.
    4. MCP AE 0.6.1 with MATCH confirmation sent (chain reg gate signal).
    5. Pre-commit gate PASS.
    6. RAVC4 to COO with: commit hashes, S3 upload paths, comp-pipescript MATCH exit codes, silver schema summary.

    Wave C execution (actual silver conversion run) is OUT OF SCOPE for this TO — that runs after Wave B bronze completes.
  </acceptance_criteria>

  <data_reprocess_scope>
    <no_reprocess_needed>New scripts producing new bronze + silver artifacts not previously extant; no existing silver data overwritten; existing billing/activity Envision-based silver (rolling-window aggregates at snapshot_date) is a separate artifact and coexists; no downstream consumers read the new transaction-level silver until gold scripts are explicitly updated to consume it</no_reprocess_needed>
  </data_reprocess_scope>

  <compiler_tools_mandate>
    <before_write>
      <check>comp-pipescript io [accounts_v2 silver path] — confirm account_id field name + parquet schema for JOIN</check>
    </before_write>
    <before_commit>
      <check>ds-commit-gate.sh pull_inflection_transactions_rest.py convert_transactions_to_silver.py</check>
      <check>from __future__ import annotations on both files</check>
    </before_commit>
    <after_commit>
      <check>comp-pipescript deployed pull_inflection_transactions_rest → MATCH</check>
      <check>comp-pipescript deployed convert_transactions_to_silver → MATCH</check>
    </after_commit>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <coordination_protocol>
      DS BASE owns Wave A code work entirely. On MATCH confirmation for both scripts, MCP AE 0.6.1 directly — that triggers AE chain reg update (HISTBF.003 gate). Do NOT coordinate with AE before MATCH is confirmed. Direct MCP to DS~B for any endpoint schema questions (they have the full HAR analysis and probe logs).
    </coordination_protocol>
  </cross_domain_coordination>
</task_order>
