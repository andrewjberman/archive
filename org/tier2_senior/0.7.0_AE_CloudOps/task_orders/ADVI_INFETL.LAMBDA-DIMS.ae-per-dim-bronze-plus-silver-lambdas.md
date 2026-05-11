<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.LAMBDA-DIMS</id>
    <project>ADVI_INFETL</project>
    <title>Build per-dim daily Lambdas (bronze pull + silver convert in one invocation)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>SHIPPED Phase A+B — inf-pipeline-v1.7.43 through v1.7.47 (today). COO confirmed 2026-05-11.</completed_note>
    <priority>high</priority>
    <estimated_effort>~3-5d cumulative across 8 Lambdas</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_prd">docs/architecture/ADVI_INFETL.md</ref>
    <ref type="andrew_directive">2026-05-07 — "lambdas should be doing both daily incremental ingestion and silver conversion. then our gold runner ec2 needs to be event-based to trigger at the receipt of all daily silver data"</ref>
    <ref type="upstream_audit">INFETL.DAILY-AUDIT matrix (gates priority + dim list)</ref>
    <ref type="reference_lambda">inf-api-txn Lambda v1.7.30 (commit fd4105bec) — T-1 default cron, bronze + silver pattern. Canonical reference for new Lambdas.</ref>
    <ref type="paired_TOs">INFETL.SILVER-AGGREGATOR + INFETL.GOLD-EVENT-TRIGGER (downstream chain)</ref>
  </references>

  <context>
    Each Inflection dim gets a dedicated Lambda that:
      1. Pulls bronze from Orion API for the snapshot_date (event input or T-1 default)
      2. Converts to silver parquet
      3. Writes per-dim sentinel `silver/_silver_complete/{date}/{dim}.json` indicating ok
    
    The aggregator (INFETL.SILVER-AGGREGATOR) detects N/N sentinels for the date, then
    fires the gold trigger (event-driven, not cron).

    For per-client iter dims (assets_v2, positions_daily), use asyncio internal parallelism
    to fit Lambda 15-min cap. Concurrency target: 50-100 concurrent client requests per
    Lambda invocation. If still exceeding 15 min, fall back to chunked invocation
    (Step Function Map state distributing client batches across N Lambdas).
  </context>

  <scope>
    <step>
      Per-dim list (8 Lambdas; UAD blocked on INFNNA.UAD-CREATOR fix):
        - inf-tax-daily
        - inf-perf-daily
        - inf-billing-daily
        - inf-assets-v2-daily (asyncio internal)
        - inf-positions-daily (asyncio internal)
        - inf-accounts-v2-daily
        - inf-representatives-daily
        - inf-unified-account-dim-daily (after UAD-CREATOR fix)
        (inf-api-txn-daily already exists — v1.7.30)
    </step>
    <step>
      Per Lambda implementation pattern:
        - Event input: {"snapshot_date": "YYYY-MM-DD"} (or T-1 default if absent)
        - Stage 1: invoke pull script logic (or refactor into reusable lib import)
        - Stage 2: invoke silver builder logic for that dim + snapshot_date
        - Stage 3: aws s3 put silver/_silver_complete/{date}/{dim}.json with status + row counts + duration
        - Memory: 2048-4096 MB for compute-heavy dims, 1024 MB for light
        - Timeout: 900s default; assets_v2/positions_daily may need 900s + asyncio
    </step>
    <step>
      Per-Lambda Terraform module (mirror inf-api-txn pattern):
        - aws_lambda_function with layer = pandas-pyarrow-layer
        - aws_cloudwatch_event_rule cron expression (per dim — most daily 13:00 UTC, monthly for billing on EOM)
        - aws_lambda_permission for EventBridge invoke
        - IAM role with S3 read + write + Secrets Manager (JWT)
        - Source map entry per CLAUDE.md rule 4
    </step>
    <step>
      Build incrementally: ship 1 Lambda per day with comp-iam + comp-pipescript MATCH
      verify. Order priority per INFETL.DAILY-AUDIT matrix.
    </step>
    <step>
      For each Lambda shipped:
        - Tag bump inf-pipeline-v1.X.Y
        - record-terraform-deploy.sh
        - Manual empirical: invoke with synthetic event, verify silver landed + sentinel written
        - RAVC per Lambda
    </step>
    <step>
      Final RAVC: all 8 Lambdas live + per-dim cron firing + silver sentinels accumulating.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-iam service inf-{dim}-daily — required for each Lambda</tool>
    <tool>comp-pipescript io inf-{dim}-daily — required for each Lambda</tool>
    <tool>comp-routes trace inf-{dim}-daily — full path verification</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">8 Lambdas (or 9 incl UAD post-creator-fix) deployed and on EventBridge daily cron.</criterion>
    <criterion id="AC2">Each Lambda writes silver/_silver_complete/{date}/{dim}.json sentinel on success.</criterion>
    <criterion id="AC3">For per-client iter dims: asyncio + concurrency cap; verified to complete under 14 min via empirical run.</criterion>
    <criterion id="AC4">Per-Lambda comp-iam, comp-pipescript io, comp-routes evidence captured in RAVC.</criterion>
    <criterion id="AC5">No 429s on Orion side from concurrent Lambdas (rate budget explicitly accounted for in design).</criterion>
    <criterion id="AC6">EC2 inf-bronze-runner can be retired post-migration (or kept only for backfills).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>INFETL.DAILY-AUDIT matrix; INFNNA.UAD-CREATOR for UAD specifically.</upstream>
    <downstream>INFETL.SILVER-AGGREGATOR consumes the silver-complete sentinels.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Largest TO in solidify series. ~3-5d cumulative. Ship Lambdas one-per-day with full empirical per Lambda; do not batch.</message>
  </go_signal>
</task_order>
