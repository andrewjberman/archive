<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFREL.010</id>
    <project>ADVI_INFREL</project>
    <title>Orion endpoint lookback audit + 2020 historical backfill + daily dim cadence confirm</title>
    <issued_to>0.6.1_AE_PartnerETL</issued_to>
    <issued_to_secondary>0.7.0_AE_CloudOps</issued_to_secondary>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-06</issued_date>
    <status>phase0-complete-phase1-pending-coo-go</status><!-- Phase 0 audit complete 20260507T~18:30Z (AE 0.6.1). RAVC3 sent to COO. Billing Wave C 2020-2024 dates + 83/83 silver CLOSED per COO RAVC7. Phase 0 findings: billing+tax date-range-capable via ORION_PULL_DATE env; performance needs --snapshot-date orchestrator fix; unified_account_dim/accounts_v2/assets snapshot-only (no backfill viable). expected_fail removed from assets (confirmed). Phase 1 GO pending COO + Andrew approval (large-scale S3 writes). -->
    <priority>high</priority>
    <estimated_effort>Phase 0: ~0.5d audit; Phase 1: multi-day runner job (6+ years data; parallelizable by dim); Phase 2: ~0.25d cadence confirm</estimated_effort>
  </metadata>

  <references>
    <ref type="trigger">INFREL.002 Fix4 backfill attempt 20260506T~1426Z (AE 0.7 RAVC3): transactions 500 on historical date; billing/tax wrote to today's partition; accounts_v2 --upload-bronze usage error; overall=failure. Andrew-directed follow-on.</ref>
    <ref type="hypothesis_transactions">transactions 500 on --date 2026-05-04 = likely missing @StartDate/@EndDate POST body params in orchestrator dispatch, not a fundamental Custom Reports capability gap. pull_inflection_transactions_v2.py:182 already has post_generate(jwt, start_date, end_date) — the orchestrator invocation path may not be passing the date through correctly.</ref>
    <ref type="hypothesis_billing_tax">billing/tax use Envision report endpoint which almost certainly supports date-range parameterization. Their "wrote to 2026-05-06 partition not 2026-05-04" behavior = orchestrator --date flag does not propagate the date to individual dim script partition-write paths. Fix is orchestrator-side, not script-side.</ref>
    <ref type="hypothesis_accounts_v2">accounts_v2 (portfolio snapshot) is likely snapshot-only by nature — point-in-time holdings state, not a date-range pull. Historical backfill not applicable for this dim.</ref>
    <ref type="daily_cadence_concern">expected_fail=true on assets in today's bronze/orion-api/2026-05-06/_BRONZE_COMPLETE.json requires investigation before declaring daily cadence clean. If assets is expected_fail-flagged routinely, the dim is silently skipping daily.</ref>
    <ref type="backfill_scope">2020-01-01 to present. Probably multi-day runner job for 6+ years of data (~2,300 daily partitions per dim). Parallelizable by dim. Runner: inf-bronze-runner (i-083ad9ae297f88e9f).</ref>
    <ref type="orchestrator">infra/aws/ec2/inf-bronze-runner/orchestrator.py — owns DimSpec extra_args + --date flag dispatch logic</ref>
  </references>

  <context>
    INFREL.002 Fix4 attempted to backfill 2026-05-04 bronze by passing --date to orchestrator.py.
    Results revealed three class of issues:

    (1) Date-param propagation gap: orchestrator.py accepts --date but individual dim pull scripts
    may not receive or use it for their S3 partition write paths. billing/tax "succeeded" but wrote
    to today's date, not the target date. This is an orchestrator-side bug in how it passes the
    date through to dim scripts.

    (2) Endpoint capability unknown: for transactions, the 500 may be a missing param issue
    rather than a fundamental historical data gap. The pull script already has date range support
    (start_date/end_date). Other endpoints (billing/tax Envision reports) likely also support
    historical date ranges. accounts_v2 (snapshot) likely cannot do historical.

    (3) Daily cadence silent failures: expected_fail=true on assets and potentially other dims
    may mask routine silent failures that never surface to alerting.

    Phase 0 (audit) MUST precede Phase 1 (writing backfill code). Do not write any backfill
    logic until per-dim endpoint capability is empirically confirmed.
  </context>

  <phase id="0" when="Phase 0 — lookback audit (REQUIRED before Phase 1)">

    <step id="0.1">
      <objective>Per-dim endpoint date-range capability matrix.</objective>
      <run>For each dim in orchestrator.py DimSpecs, determine empirically:
        (a) Does the Orion/Envision endpoint accept a historical date parameter?
        (b) Does the pull script already have date-range argparse args?
        (c) Does the orchestrator pass --date through to the dim script?

      Test each dim by attempting a single historical date pull (e.g., 2026-04-01) and
      observing: success with correct-date data, 500/4xx error, or date silently ignored
      (data written to today's partition).
      </run>
      <dims_to_audit>
        - unified_account_dim: suspect snapshot-only (account-level attributes as of today)
        - accounts_v2: suspect snapshot-only (portfolio snapshot)
        - billing: suspect date-range capable (Envision report)
        - tax: suspect date-range capable (Envision report; ExcelReports/Verbose endpoint)
        - performance: not yet authored (INFREL.001b scope); audit after 001b ships
        - transactions: likely date-range capable once @StartDate/@EndDate params passed correctly
        - assets: investigate expected_fail=true first; determine if dim is snapshot or historical
        - geo: Track 2, not yet authored; skip
      </dims_to_audit>
      <deliverable>
        Audit matrix table: dim | endpoint_type | date_range_capable (Y/N/unknown) |
        historical_param_mechanism | snapshot_only_reason (if N) | orchestrator_passes_date (Y/N/bug)
      </deliverable>
    </step>

    <step id="0.2">
      <objective>Investigate expected_fail=true on assets in today's daily run.</objective>
      <run>Check orchestrator.py DimSpec for assets dim: why is expected_fail=true set?
      Is this a permanent flag (assets endpoint always unreliable) or a transient flag set during
      a migration period? If assets is routinely expected_fail, the daily partition is never being
      written — that is a silent data gap, not an expected operational state.
      Cross-check: does bronze/orion-api/ have assets partitions for recent dates?
      </run>
      <expect>Root cause of expected_fail=true on assets documented; either (a) remove flag and fix
      underlying issue, or (b) confirm assets is intentionally excluded with documented reason.</expect>
    </step>

    <step id="0.3">
      <objective>Diagnose orchestrator --date propagation bug.</objective>
      <run>Read orchestrator.py to understand how --date propagates to individual dim script
      invocations. Determine: does the orchestrator pass the target date to each script's argparse
      args? Does it control the S3 partition write path (bronze/orion-api/{date}/) from the
      orchestrator level, or does each script write its own path independently?
      The billing/tax "success but wrong partition" behavior suggests the script wrote to today's
      date instead of the specified --date. Find the code path.
      </run>
      <expect>Root cause of partition write path mismatch documented. Fix design proposed (e.g.,
      orchestrator passes --date to each dim script, dim scripts use it for their S3 key prefix).</expect>
    </step>

    <step id="0.4">
      <objective>RAVC3 to COO with Phase 0 audit matrix + fix designs.</objective>
      <run>Compile: per-dim capability matrix + expected_fail root cause + --date propagation fix
      design. Surface any dims that are fundamentally snapshot-only (no backfill possible).
      COO gates Phase 1 GO on this RAVC3.</run>
    </step>

  </phase>

  <phase id="1" when="Phase 1 — historical backfill (gates on Phase 0 RAVC3 + COO GO)">

    <step id="1.1">
      <objective>Fix orchestrator --date propagation for dims confirmed date-range capable.</objective>
      <run>Implement the fix identified in Phase 0.3: ensure --date correctly propagates to dim
      script invocations AND to S3 partition write paths. All date-capable dims must write to
      bronze/orion-api/{specified_date}/ not bronze/orion-api/{today}/.
      Pre-commit gate per CLAUDE.md Rule 14.</run>
    </step>

    <step id="1.2">
      <objective>Design backfill job for 2020-01-01 to present.</objective>
      <run>AE 0.7 input needed on:
        (a) S3 write path design: backfill writes to bronze/orion-api/{date}/ — confirm no
            collision with production daily writes (backfill should be idempotent; re-running for
            a date that already has data is safe if scripts are idempotent)
        (b) Runner parallelization strategy: dim-by-dim sequential vs concurrent
        (c) Estimated wall time at nominal rate: ~2,300 dates × N dims × avg_dim_duration
        (d) inf-bronze-runner capacity: can it run a multi-day job without shutdown/interruption?
            Likely needs --no-auto-shutdown or equivalent for a long-running backfill job.

      Propose a backfill dispatch plan to COO before starting execution.
      </run>
    </step>

    <step id="1.3">
      <objective>Execute backfill for confirmed date-range-capable dims.</objective>
      <run>Per approved dispatch plan: iterate date range 2020-01-01 to present for each capable
      dim. Use orchestrator.py --mode backfill --backfill-from 2020-01-01 --backfill-to {today}
      or equivalent (per Phase 0 fix). Monitor: check _BRONZE_COMPLETE.json sentinels per date
      as they land. Surface any systematic failures.
      AE 0.7 monitoring runner infrastructure during execution.
      </run>
      <expect>bronze/orion-api/{date}/ partitions populated for all capable dims from 2020-01-01
      to present. Sentinel _BRONZE_COMPLETE.json per date confirms completion.</expect>
    </step>

    <step id="1.4">
      <objective>Silver propagation for backfilled bronze (if applicable).</objective>
      <run>After bronze backfill lands, silver chain must also backfill for dims that have silver
      consumers. Determine: which backfilled dims have downstream silver consumers? Run silver
      chain backfill for those dims (or trigger silver Lambda per date partition).
      Note: performance dim, transactions dim — silver builders may not exist yet for all dims
      (INFREL.001b + INFINGE.005b silver builder). Stage those dims' silver backfill after their
      silver builders ship.</run>
    </step>

  </phase>

  <phase id="2" when="Phase 2 — daily cadence confirm (parallel to Phase 1)">

    <step id="2.1">
      <objective>Verify every dim in orchestrator.py DimSpecs hits the daily cron and produces
      a bronze partition.</objective>
      <run>For each dim: check S3 for 5 consecutive recent daily partitions. Any dim missing ≥1
      partition in the last 5 days is a cadence failure. Expected_fail dims (found in Phase 0.2)
      must be resolved before declaring cadence clean.
      Cross-ref with Fix C alarm (Opal/InflectionSilver/DimConversionFailure) for silver-side
      gaps that indicate bronze input missing.</run>
      <expect>Per-dim cadence table: dim | last_5_partitions | status (clean/gap/expected_fail-TBD)</expect>
    </step>

    <step id="2.2">
      <objective>Add CW metric for orchestrator expected_fail dims (if any remain flagged after
      Phase 0.2 resolution).</objective>
      <run>If any dim has a legitimate expected_fail case (e.g., Orion endpoint truly unavailable
      on weekends for specific report types), add a CW metric for it rather than silently
      swallowing the failure. Emit `Opal/InflectionBronze/DimSkipped` with dim_name dimension.
      Alarm on unexpected skip patterns.</run>
    </step>

    <step id="2.3">
      <objective>RAVC5 to COO: cadence table + any new alarms authored.</objective>
    </step>

  </phase>

  <acceptance_criteria>
    <criterion id="AC1">Phase 0: per-dim lookback audit matrix complete — endpoint_type, date_range_capable, historical_param_mechanism, snapshot_only_reason, orchestrator_passes_date.</criterion>
    <criterion id="AC2">Phase 0: expected_fail=true on assets root cause documented; either flag removed + underlying fix, or intentional exclusion documented with reason.</criterion>
    <criterion id="AC3">Phase 0: orchestrator --date propagation bug root cause documented; fix design proposed.</criterion>
    <criterion id="AC4">Phase 1: orchestrator --date fix shipped; confirmed-capable dims write to bronze/orion-api/{specified_date}/ not bronze/orion-api/{today}/.</criterion>
    <criterion id="AC5">Phase 1: backfill dispatch plan proposed + COO approved before execution begins. Plan includes wall-time estimate, parallelization strategy, runner infrastructure requirements.</criterion>
    <criterion id="AC6">Phase 1: bronze/orion-api/{date}/ partitions populated for all date-range-capable dims from 2020-01-01 to present. Sentinel counts match expected date range.</criterion>
    <criterion id="AC7">Phase 2: per-dim cadence table — all dims clean (no silent skips) or all skips have CW metric + documented reason.</criterion>
    <criterion id="AC8">AE 0.7: runner infra + S3 write path design approved before Phase 1 execution. Runner kept live for duration of backfill job.</criterion>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="0" when="before any orchestrator.py edit">comp-blast orchestrator — confirm blast radius of --date propagation fix before implementing</phase>
    <phase id="1" when="before committing orchestrator fix">comp-iam service inf-bronze-runner + .tools/ds-commit-gate.sh (for any pull script edits) + safe-commit.sh</phase>
    <phase id="2" when="after Phase 1 ship">comp-pipescript consumers silver/api_dims/{dim}/ per newly-backfilled dim — confirm silver chain coverage</phase>
  </compiler_tools_mandate>

  <cross_domain_coordination>
    <item>AE 0.7 SECONDARY on Phase 1 infrastructure design (runner keep-alive during multi-day job, S3 write path idempotency, parallelization). AE 0.6.1 does NOT start Phase 1 execution without AE 0.7 infrastructure review.</item>
    <item>Phase 1 backfill execution is a long-running runner job — coordinate with AE 0.7 on inf-bronze-runner EC2 lifecycle (no auto-shutdown; dedicated window; monitoring). Andrew must approve any large-scale S3 write operations before execution.</item>
    <item>Silver backfill (Phase 1.4) gates on INFREL.001b + INFINGE.005b silver builder ship for performance and transactions dims. Backfill those dims' silver after builders ship.</item>
    <item>Non-blocking on INFREL.001 empirical window, INFREL.002 Phase 2 empirical, INFREL.001b authorship. Can proceed in parallel.</item>
  </cross_domain_coordination>

  <do_not>
    <rule>Do NOT write any backfill code or run any backfill job before Phase 0 audit matrix is complete and COO-approved. Phase 0 is the gate.</rule>
    <rule>Do NOT run large-scale S3 write operations (multi-year backfill) without Andrew approval on the dispatch plan. This writes to production bronze paths.</rule>
    <rule>Do NOT modify existing daily partition data. Backfill writes to previously-empty date partitions only. Idempotency: if a partition already exists for a date, do not overwrite without explicit authorization.</rule>
    <rule>Do NOT declare daily cadence clean until expected_fail=true on assets is resolved (Phase 0.2). A routinely-expected-fail dim is a silent gap, not an expected state.</rule>
  </do_not>

  <go_signal>
    <issued_at>20260506T~1430Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>Andrew-directed. Phase 0 GO immediate. Phase 1 GO gates on Phase 0 RAVC3 + COO + Andrew approval of dispatch plan (large-scale S3 writes require explicit Andrew authorization before execution). AE 0.7 secondary for Phase 1 infrastructure design.</message>
  </go_signal>

</task_order>
