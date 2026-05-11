<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.GOLD-EVENT-TRIGGER</id>
    <project>ADVI_INFETL</project>
    <title>Modify inf-gold-trigger Lambda — accept event-based invocation; cron becomes fallback (revises ADVI_INFETL.001)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>active</status>
    <priority>high</priority>
    <estimated_effort>~0.5d Lambda code + Terraform</estimated_effort>
  </metadata>

  <references>
    <ref type="parent_prd">docs/architecture/ADVI_INFETL.md</ref>
    <ref type="andrew_directive">2026-05-07 — gold runner EC2 should be event-based, triggered at receipt of all daily silver data</ref>
    <ref type="upstream_TO">INFETL.SILVER-AGGREGATOR — invokes inf-gold-trigger with snapshot_date payload when all silvers complete</ref>
    <ref type="revises_TO">ADVI_INFETL.001 (EventBridge cron + nightly fallback Terraform). Cron remains, but role changes from primary to fallback only.</ref>
    <ref type="target_lambda">infra/aws/lambda/inf-gold-trigger/lambda_function.py</ref>
    <ref type="target_terraform">infra/aws/terraform/inf-pipeline/eventbridge.tf + lambdas.tf</ref>
  </references>

  <context>
    Andrew's architecture: gold runner EC2 dispatched event-based (silver-complete →
    aggregator → gold trigger), with EventBridge cron acting only as a fallback safety
    net (not the primary trigger).

    inf-gold-trigger Lambda must:
      1. Accept event input from inf-silver-aggregator: {"snapshot_date": "YYYY-MM-DD"}
      2. Continue to accept legacy cron event payload: {"mode": "full"} or {"mode": "full", "fallback": true}
      3. Idempotent: if gold chain already ran for snapshot_date today, skip (unless --force)

    EventBridge cron rules from ADVI_INFETL.001 land DISABLED. Once event-driven path
    is empirically validated (per INFETL.SILVER-AGGREGATOR), cron is enabled at lower
    frequency as fallback (e.g., 06:00 UTC daily — fires only if event chain failed
    to deliver gold completion within expected window).
  </context>

  <scope>
    <step>
      Read current inf-gold-trigger Lambda code. Confirm event-payload handling and SSM
      dispatch patterns.
    </step>
    <step>
      Modify Lambda to:
        - Detect event source: aggregator (has snapshot_date), cron primary (has mode=full), cron fallback (has fallback=true)
        - For aggregator events: dispatch SSM with --date {snapshot_date} --mode incremental
        - For cron events: dispatch SSM with --mode full (legacy behavior)
        - Add idempotency check: read gold/meta/pipeline-complete.json; if exists for today and chain_label matches, log "already complete" + return without dispatch
        - Pass freshness gate as before (ADHC_COMPIL.013 silver-prep gate)
    </step>
    <step>
      Lambda permission update: ensure aws_lambda_permission allows aggregator invoke principal.
    </step>
    <step>
      Terraform changes (revising ADVI_INFETL.001):
        - aws_cloudwatch_event_rule.inf_canonical_prices_daily: keep state="DISABLED" until event-path verified, then change schedule to "cron(0 6 * * ? *)" and state="ENABLED" as FALLBACK at 06:00 UTC
        - aws_cloudwatch_event_rule.inf_gold_nightly_fallback: REMOVE or merge into the 06:00 UTC fallback (one fallback is enough)
        - Update tags + descriptions to clarify fallback role
    </step>
    <step>
      Tag bump inf-pipeline-v1.X.Y. record-terraform-deploy.sh.
    </step>
    <step>
      Manual empirical:
        - Test 1: synthesize aggregator event {"snapshot_date":"2026-05-07"} via aws lambda invoke. Verify SSM dispatched with --date arg.
        - Test 2: synthesize cron event {"mode":"full"}. Verify SSM dispatched in legacy mode.
        - Test 3: synthesize aggregator event for a date where pipeline-complete.json exists. Verify idempotent skip.
    </step>
    <step>
      RAVC: code change diff + 3 empirical test results + Terraform 0-diff post-apply.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-pipescript deployed inf-gold-trigger — MATCH</tool>
    <tool>comp-iam service inf-gold-trigger — confirm ssm:SendCommand still permitted</tool>
    <tool>comp-routes trace inf-gold-trigger</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Lambda accepts both aggregator event-payload and legacy cron payload.</criterion>
    <criterion id="AC2">Idempotency: re-firing the same snapshot_date does not re-run gold chain.</criterion>
    <criterion id="AC3">Cron rule(s) reconfigured to fallback role (06:00 UTC) — not primary.</criterion>
    <criterion id="AC4">3 empirical tests pass.</criterion>
    <criterion id="AC5">SILVER-AGGREGATOR can wire to this Lambda without further changes.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — can ship in parallel with SILVER-AGGREGATOR.</upstream>
    <downstream>INFETL.SILVER-AGGREGATOR final wiring waits on this TO's empirical pass.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~18:00Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO. Pre-authorized. Revises ADVI_INFETL.001 — appendin a "REVISION 2026-05-07" section to that TO file is fine; or COO will close-loop revision tracking.</message>
  </go_signal>
</task_order>
