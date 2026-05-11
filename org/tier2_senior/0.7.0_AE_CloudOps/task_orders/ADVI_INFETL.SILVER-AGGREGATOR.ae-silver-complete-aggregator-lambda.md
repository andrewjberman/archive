<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.SILVER-AGGREGATOR</id>
    <project>ADVI_INFETL</project>
    <title>inf-silver-aggregator Lambda — detects N/N silver-complete sentinels per date and fires gold trigger</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>SHIPPED inf-pipeline-v1.7.37. COO confirmed 2026-05-11.</completed_note>
    <priority>high</priority>
    <estimated_effort>~0.75d</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_prd">docs/architecture/ADVI_INFETL.md</ref>
    <ref type="andrew_directive">2026-05-07 — gold runner EC2 should be event-based, triggered at receipt of all daily silver data</ref>
    <ref type="upstream_TO">INFETL.LAMBDA-DIMS — produces per-dim silver-complete sentinels at silver/_silver_complete/{date}/{dim}.json</ref>
    <ref type="downstream_TO">INFETL.GOLD-EVENT-TRIGGER — modifies inf-gold-trigger to accept event-based invoke</ref>
    <ref type="bd_pattern">BD pipeline does not have an exact analog; this is a new pattern. Closest reference: AWS Step Functions Map state for parallel completion detection. We choose Lambda for simplicity.</ref>
  </references>

  <context>
    With per-dim daily Lambdas writing silver-complete sentinels, the aggregator must
    detect when all dims for a given snapshot_date have completed and fire the gold
    trigger. Two design options:

    Option A — Lambda triggered on S3 ObjectCreated for silver/_silver_complete/{date}/*.json:
      Each sentinel write fires the aggregator. Aggregator counts existing sentinels
      for that date prefix; if count == N (canonical dim count, e.g., 9), invokes
      inf-gold-trigger with {"snapshot_date": "YYYY-MM-DD"} payload.
      Pros: simple, low latency, minimal infra
      Cons: each sentinel-write fires Lambda; ~9 invocations per day for noop-counting

    Option B — Step Function Map state:
      Map iterates each dim Lambda in parallel; on all complete, fire gold trigger.
      Pros: structured, explicit
      Cons: more complex; requires changing per-dim Lambdas to fit Step Function model

    Recommendation: Option A. Simpler, fits existing event-driven architecture, and
    9 noop-counting invocations/day is trivial cost.
  </context>

  <scope>
    <step>
      Define canonical dim list constant (9 dims: tax, perf, billing, transactions,
      accounts_v2, unified_account_dim, representatives, assets_v2, positions_daily).
      Stored in Lambda env var INF_DIM_LIST (or in code).
    </step>
    <step>
      Build inf-silver-aggregator Lambda:
        - Trigger: S3 ObjectCreated on silver/_silver_complete/ prefix
        - Logic:
          1. Parse event for date_dim_key
          2. Extract date from key path
          3. List silver/_silver_complete/{date}/ keys
          4. If count == len(DIM_LIST) AND all sentinels report status=ok → invoke inf-gold-trigger
          5. Else → no-op (return)
        - Memory: 256 MB
        - Timeout: 60s (just S3 list + invoke)
    </step>
    <step>
      Add Terraform:
        - aws_lambda_function inf_silver_aggregator with IAM (s3 list + lambda invoke)
        - aws_s3_bucket_notification update on opal-data-inf — add lambda_function block on silver/_silver_complete/ prefix → inf-silver-aggregator
        - aws_lambda_permission for s3 invoke
    </step>
    <step>
      Coordinate with INFETL.GOLD-EVENT-TRIGGER TO so aggregator's invoke target is the
      event-mode-modified inf-gold-trigger (not the legacy cron-mode).
    </step>
    <step>
      Tag bump inf-pipeline-v1.X.Y. record-terraform-deploy.sh.
    </step>
    <step>
      Manual empirical:
        - Pre-state: ensure no recent silver-complete sentinels exist
        - Trigger 9 Lambda invocations manually (or via cron)
        - Verify aggregator fires each time but only fires gold trigger ONCE when 9th sentinel lands
        - Verify gold trigger received {"snapshot_date": "..."} payload
    </step>
    <step>
      RAVC: aggregator deployed + empirical chain complete + gold trigger fired exactly once for the test date.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-iam service inf-silver-aggregator</tool>
    <tool>comp-routes trace inf-silver-aggregator</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Lambda deployed + S3 trigger wired.</criterion>
    <criterion id="AC2">Idempotent: receiving the same sentinel twice does not double-fire gold trigger (use S3 conditional or lock marker).</criterion>
    <criterion id="AC3">Empirical: 9 silver-complete sentinels for a date fire gold trigger exactly once.</criterion>
    <criterion id="AC4">Aggregator memory + timeout adequately sized (no timeouts under normal operation).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>INFETL.LAMBDA-DIMS — needs at least 1-2 dim Lambdas writing sentinels for empirical test.</upstream>
    <downstream>INFETL.GOLD-EVENT-TRIGGER — gold trigger must accept event-mode invoke before aggregator is wired live.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Pre-authorized. Ships in parallel with INFETL.LAMBDA-DIMS; full empirical wait gates on at least one Lambda dim and the GOLD-EVENT-TRIGGER landing.</message>
  </go_signal>
</task_order>
