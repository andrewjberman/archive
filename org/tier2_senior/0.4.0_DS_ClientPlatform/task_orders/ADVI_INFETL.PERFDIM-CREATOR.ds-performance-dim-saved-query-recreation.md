<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.PERFDIM-CREATOR</id>
    <project>ADVI_INFETL</project>
    <title>Performance Dim saved-query recreation + pull-script date-bug fix verification — unblocks performance bronze + chronically-failing silver builder</title>
    <issued_to>0.4.0_DS_ClientPlatform~A</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>high</priority>
    <estimated_effort>~1-1.5h (mirrors UAD-CREATOR pattern shipped today)</estimated_effort>
    <urgency>HIGH — Andrew direct 2026-05-07T~21:42Z. Address tonight after current SHAPE-VERIFY work.</urgency>
  </metadata>

  <references>
    <ref type="andrew_directive">2026-05-07T~21:38Z: "If we're getting nothing for performance then we need to assess if we're calling the endpoint incorrectly" + 21:42Z "create a TO addressed to DS~A that covers everything they need to know to test and fix this issue, we will address it later tonight."</ref>
    <ref type="precedent_pattern">commit 4d99a1fb2 — "fix(ADVI_INFREL.001b): creator scripts use Billing Dim verbose as runtime template -- inline schema with empty additionalOptions caused /Generate 400 'Could not find activity 1'" (today's UAD-CREATOR + tax fix landed via this exact pattern)</ref>
    <ref type="related_to_today">ADVI_INFNNA.UAD-CREATOR (DS~B `ec6f19c00`) — same bug class, same fix shape — mirror that creator-script architecture verbatim</ref>
    <ref type="target_script">data/orion/manual_api/pull_inflection_performance_dim.py</ref>
    <ref type="needs_authoring">data/orion/manual_api/create_performance_dim_query.py (NEW — analog to create_unified_account_dim_query.py)</ref>
    <ref type="orion_query_id">b22505ec-54e7-42e3-8a34-4e30dc22067c (current "Performance Dim" saved query — to be RECREATED)</ref>
    <ref type="silver_consumer">data/orion/scripts/silver/convert_orion_api_to_silver.py — build_performance() (chronically failing/stale because bronze is empty SKIP markers)</ref>
    <ref type="downstream">INF_D_00c + INF_D_02 + INF_D_04 portal scripts read silver/api_dims/performance/ — currently emit graceful WARN + null fallback (no prod breakage but missing functionality)</ref>
  </references>

  <context>
    SYMPTOM: Every performance bronze pull has been writing `performance_dim_SKIP.json` (110-byte
    empty marker) instead of real data. Silver builder for performance has been chronically
    failing/stale; INF_D_00c/02/04 emit graceful WARN + null fallback for performance fields.

    Andrew flagged today during diagnosis of why backfill streams are slow. Root cause
    investigation surfaced TWO sequential bugs:

    BUG #1 — pull_inflection_performance_dim.py ignores ORION_PULL_DATE env + --snapshot-date arg
    when building the report request body. Line 146 (pre-fix):
        today = dt.datetime.now(dt.timezone.utc).date()  # HARDCODED to current UTC date
    Compare to working sibling scripts (orion_billing_dim.py:142, orion_tax_dim.py:154):
        today = _pull_date()  # reads ORION_PULL_DATE env, falls back to now()
    Net: backfill runner sets ORION_PULL_DATE=2023-04-12 but performance script asks Orion for
    "today minus 3y to today" = same identical 3y-window-from-now report submitted 2247 times.

    BUG #2 (STRUCTURAL — this TO's primary scope) — "Performance Dim" saved query in Orion has
    EMPTY additionalOptions field. Empirically confirmed via verbose endpoint:
        GET /api/v1/Reporting/Envision/ExcelReports/Verbose/{performance_dim_id}
        -> verbose["additionalOptions"] = (missing/empty)
    This is the SAME bug class fixed for tax + UAD today via creator-script pattern
    (commit 4d99a1fb2 + DS~B ec6f19c00). Generate API returns 400 "Could not find activity 1"
    when additionalOptions is empty. Affects ALL pull dates — not just pre-onboarding.

    COO ACTIONS ALREADY TAKEN (uncommitted on disk):
      - Edited pull_inflection_performance_dim.py (3 changes — Bug #1 fix):
        * Added `import os` (alongside existing imports)
        * Added `_pull_date()` helper mirroring billing/tax (reads ORION_PULL_DATE env)
        * Replaced `today = dt.datetime.now(dt.timezone.utc).date()` with `today = _pull_date()` in build_generate_body
        * Added env sync in main(): `os.environ["ORION_PULL_DATE"] = args.snapshot_date` when --snapshot-date passed
      - py_compile PASS
      - Empirical test on 2024-06-15: still 400 SKIP (CONFIRMS Bug #2 is the structural blocker — Bug #1 fix alone is insufficient)
      - Diagnostic test left a SKIP marker at s3://opal-data-inf/bronze/orion-api/2024-06-15/performance_dim_SKIP.json (clean up post-fix)

    DS~A scope tonight: review my date-bug edits + commit them; author creator script for new
    "Performance Dim" saved query mirroring UAD-CREATOR pattern; recreate the saved query in
    Orion; verify a sample post-onboarding date pulls real performance.csv data; then performance
    backfill becomes possible (separate work).
  </context>

  <scope>
    <step>
      Phase 0 — Review COO's date-bug edits (Bug #1 fix), uncommitted on disk:
        git diff data/orion/manual_api/pull_inflection_performance_dim.py
      Expected diff: 4 hunks
        (1) `import os` added to imports block
        (2) `_pull_date()` helper added below `s3 = boto3.client(...)`
        (3) `today = _pull_date()` replaces hardcoded line in build_generate_body
        (4) `os.environ["ORION_PULL_DATE"] = args.snapshot_date` env-sync in main() when --snapshot-date is passed
      Verify the diff matches billing/tax pattern. If you want to refactor (e.g., move _pull_date
      to a shared utility module), that's a separate hygiene TO — for tonight, ship as-is or with
      micro-tweaks only. Do NOT revert; the date bug is real.

      Pre-commit gate: `.tools/ds-commit-gate.sh data/orion/manual_api/pull_inflection_performance_dim.py`
      Expect all three checks PASS (py_compile + ds-precommit-check + ruff).
    </step>
    <step>
      Phase 1 — Author creator script:
        data/orion/manual_api/create_performance_dim_query.py
      Mirror the architecture of:
        data/orion/manual_api/create_unified_account_dim_query.py (DS~B's UAD-CREATOR shipped earlier today, ec6f19c00)
        data/orion/manual_api/orion_billing_dim_creator.py (or whatever the billing creator file is named — search via `ls data/orion/manual_api/*creator*`)

      Required behavior:
        - Fetch Billing Dim's verbose schema as the runtime template (same as UAD-CREATOR)
        - Extract Billing Dim's `additionalOptions` block — this is the load-bearing fix
        - Build a new saved query body for Performance Dim:
          * name = "Performance Dim" (or "Performance Dim v2" if you want to keep the broken one alive for rollback comparison; my recommendation: replace in place — broken query has zero successful consumers)
          * category = "Sample Queries" (matches existing)
          * databaseIdList = [4698] (matches existing)
          * requiredOptions: select-entity (Database) + daterange (lookback window per --window arg) — KEEP AS-IS from existing Performance Dim verbose
          * additionalOptions: CLONE FROM BILLING DIM VERBOSE — this is the fix
          * deliveryOptions: Csv DirectDownload Aggregate (matches all working dims)
        - POST to /api/v1/Reporting/Envision/ExcelReports/{existing_id}/Update OR /Create
          (Mirror UAD-CREATOR's exact verb + endpoint — DS~B already validated the right call)
        - Verify post-creation: GET verbose on the new saved query, confirm additionalOptions is populated

      Performance-specific schema preservation:
        Performance Dim's `requiredOptions` schema includes a 3y/5y/1y/ytd lookback window option
        (per build_generate_body in pull script). PRESERVE this — don't accidentally truncate to
        Billing Dim's window options. The fix is additionalOptions only; requiredOptions stays
        Performance-specific.

      Performance Dim columns preservation:
        The saved query's `schema` field (column list) is what determines the pull's CSV columns
        (TWR, drawdown, risk ratios, rep_id, account_id, household_id, etc.). PRESERVE the
        schema verbatim from the existing Performance Dim verbose. DO NOT clone Billing Dim's
        schema — that would change the silver builder's expected columns.

      Pre-commit gate on the creator script.
    </step>
    <step>
      Phase 2 — Run creator script empirically:
        python data/orion/manual_api/create_performance_dim_query.py
      Expected outcome: HTTP 200/201 from Orion; new "Performance Dim" saved query created (or
      existing one updated) with populated additionalOptions.

      Verify post-create:
        python -c "
        import boto3, json, requests, uuid
        s3 = boto3.client('s3', region_name='us-east-1')
        meta = json.loads(s3.get_object(Bucket='opal-data-inf', Key='orion/jwt/current.json')['Body'].read())
        H = {'Authorization': f'Session {meta[\"jwt\"]}', 'App':'OrionConnect',
             'AppPath':'/reports/dataqueries/querybuilder',
             'BrowserSessionId':str(uuid.uuid4()),
             'Origin':'https://api.cloud.orionadvisor.com',
             'Referer':'https://api.cloud.orionadvisor.com/orionconnectapp/',
             'Accept':'application/json, text/plain, */*'}
        qr = requests.get('https://api.cloud.orionadvisor.com/api/v1/Reporting/Envision/ExcelReports', headers=H, timeout=30).json()
        perf = next(q for q in qr if q.get('name') == 'Performance Dim')
        v = requests.get(f'https://api.cloud.orionadvisor.com/api/v1/Reporting/Envision/ExcelReports/Verbose/{perf[\"id\"]}', headers=H, params={'expand':'all'}, timeout=30).json()
        print(f'requiredOptions count: {len(v.get(\"requiredOptions\", []))}')
        print(f'additionalOptions count: {len(v.get(\"additionalOptions\", []))}')
        print(f'schema columns: {len(v.get(\"schema\", {}).get(\"columns\", []))}')
        "
      MUST show: additionalOptions count &gt; 0 (was 0 pre-fix). schema columns count unchanged from pre-fix.
    </step>
    <step>
      Phase 3 — Empirical pull-script test (confirms BOTH bugs resolved):
        python data/orion/manual_api/pull_inflection_performance_dim.py --upload-bronze --snapshot-date 2024-06-15 --window 1y
      Expected outcome: HTTP 201 from Generate (NOT 400 SKIP); poll completes; performance.csv
      lands with non-zero rows; S3 path s3://opal-data-inf/bronze/orion-api/2024-06-15/performance_dim.csv
      exists with size &gt; 1KB.

      Verify:
        aws s3 ls s3://opal-data-inf/bronze/orion-api/2024-06-15/
      Should show: performance_dim.csv (real data, not _SKIP marker)

      Clean up old SKIP marker:
        aws s3 rm s3://opal-data-inf/bronze/orion-api/2024-06-15/performance_dim_SKIP.json
    </step>
    <step>
      Phase 4 — Pre-onboarding date sanity test (preserve graceful 400 SKIP behavior for legitimately pre-onboarding dates):
        python data/orion/manual_api/pull_inflection_performance_dim.py --upload-bronze --snapshot-date 2020-03-11 --window 1y
      Expected outcome: 400 SKIP (Inflection wasn't on Orion in 2020-03 — this is correct behavior).
      The skip-400 guard pattern in post_generate() should still fire and write _SKIP.json marker.
    </step>
    <step>
      Phase 5 — Mid-history sanity test:
        python data/orion/manual_api/pull_inflection_performance_dim.py --upload-bronze --snapshot-date 2023-04-12 --window 1y
      Expected: real data (Inflection has been on Orion through 2023). If 400 SKIP, root cause
      may be more nuanced than additionalOptions — RAVC immediately with full error response.
    </step>
    <step>
      Phase 6 — Commit + push:
        .tools/safe-commit.sh \
          --author "0.4.0_DS_ClientPlatform~A &lt;0.4.0_DS_ClientPlatform~A@opal.agent&gt;" \
          -m "fix(ADVI_INFETL.PERFDIM-CREATOR): Performance Dim saved-query additionalOptions clone + pull script ORION_PULL_DATE fix; unblocks performance bronze (was always 400 SKIP)" \
          -- data/orion/manual_api/pull_inflection_performance_dim.py \
             data/orion/manual_api/create_performance_dim_query.py
      git push origin CLOUD.
    </step>
    <step>
      Phase 7 — S3 deploy (per CLAUDE.md rule 13):
        aws s3 cp data/orion/manual_api/pull_inflection_performance_dim.py \
          s3://opal-data-inf/code/manual_api/pull_inflection_performance_dim.py
      Verify via comp-pipescript or analogous tool that deployed copy matches canonical.
      (Performance pull is currently EC2-orchestrator-bound per DAILY-AUDIT classification — no
      Lambda copy to sync until LAMBDA-DIMS Phase B P3 ships. AE 0.7 owns Lambda-side resync
      when that lands.)
    </step>
    <step>
      Phase 8 — RAVC to COO:
        - Commit hash + S3 ETag of pull script + creator script
        - Phase 2 verbose-endpoint snapshot: requiredOptions count + additionalOptions count + schema columns count (pre-fix vs post-fix)
        - Phase 3 empirical: performance_dim.csv size + row count + first 3 rows headers
        - Phase 4 pre-onboarding empirical: confirmed 400 SKIP preserved
        - Phase 5 mid-history empirical: real data confirmed
        - SKIP-marker cleanup confirmation
        - Any deviations (e.g., requiredOptions schema needed adjustment, query renamed instead of replaced, etc.)

      Once RAVC lands, COO will dispatch performance backward+cutoff backfill (separate runner
      script .runtmp/backward_cutoff_backfill.py — already written tonight; runs cleanly with
      fixed pull script).
    </step>
  </scope>

  <compiler_mandate>
    <tool>.tools/ds-commit-gate.sh on both pull script + creator script — all three checks PASS</tool>
    <tool>Empirical verbose-endpoint check showing additionalOptions populated post-fix</tool>
    <tool>Empirical pull on 2024-06-15 showing real performance_dim.csv lands (not _SKIP marker)</tool>
    <tool>Empirical pull on 2020-03-11 showing 400 SKIP preserved (pre-onboarding behavior intact)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">pull_inflection_performance_dim.py: 4-hunk diff committed (import os + _pull_date helper + build_generate_body line replacement + main() env sync). py_compile + ds-precommit-check + ruff PASS.</criterion>
    <criterion id="AC2">create_performance_dim_query.py: new file authored, mirrors UAD-CREATOR architecture. py_compile + ds-precommit-check + ruff PASS.</criterion>
    <criterion id="AC3">Creator script run produces a Performance Dim saved query with populated additionalOptions (verified via verbose endpoint count &gt; 0; was 0 pre-fix).</criterion>
    <criterion id="AC4">Saved query schema (column list) preserved from pre-fix — silver builder's expected columns unchanged.</criterion>
    <criterion id="AC5">Empirical 2024-06-15 pull lands real performance_dim.csv (size &gt; 1KB, row count &gt; 0). Old _SKIP marker cleaned up.</criterion>
    <criterion id="AC6">Empirical 2020-03-11 pull still produces 400 SKIP (pre-onboarding graceful behavior preserved).</criterion>
    <criterion id="AC7">Empirical 2023-04-12 pull lands real data (mid-history sanity).</criterion>
    <criterion id="AC8">Commit pushed to CLOUD; S3 deploy of pull script complete; RAVC to COO with full evidence.</criterion>
    <criterion id="AC9">No regressions to billing/tax pull scripts (their _pull_date pattern unchanged; this TO touches performance only).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — independent investigation/fix. Pull-script edits already on disk; creator-script authoring is the work.</upstream>
    <downstream>
      (1) Performance backfill (backward+cutoff via .runtmp/backward_cutoff_backfill.py) becomes possible once this TO ships.
      (2) Silver builder for performance (build_performance in convert_orion_api_to_silver.py) starts producing real data once bronze populates.
      (3) INF_D_00c + INF_D_02 + INF_D_04 portal scripts will gain real performance fields (currently null fallbacks) once silver populates.
      (4) LAMBDA-DIMS Phase B P3 inf-perf-daily Lambda (AE 0.7 lane) gates on this fix — performance Lambdafication blocked until pull script + saved query both correct.
    </downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~21:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HIGH-priority TO. Andrew direct: "we will address it later tonight." Continue SHAPE-VERIFY work first if you're mid-stream there; pivot to PERFDIM-CREATOR once SHAPE-VERIFY checkpoint reached. Bronze cascade tonight (~22:55Z billing) doesn't gate on this — INFNNA cascade is transactions+accounts_v2 only. Performance fix is parallel infrastructure work. RAVC at Phase 8 with all empirical evidence.</message>
  </go_signal>
</task_order>
