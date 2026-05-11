<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.001</id>
    <project>ADVI_INFETL</project>
    <title>EventBridge daily gold cron + nightly fallback rules + lambda_permission resources (lands DISABLED; flipped via TO-011)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>SHIPPED 2026-05-07 commit 7e9d30e7d (inf-pipeline fallback gold cron + S3 notification). COO confirmed 2026-05-11.</completed_note>
    <priority>normal</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 4 daily trigger), §4.1 (EventBridge component spec), §6 Phase 1 TO-1</ref>
    <ref type="bd_pattern">infra/aws/terraform/bd-pipeline/eventbridge.tf — aws_cloudwatch_event_rule.bd_canonical_prices_daily + bd_gold_nightly_fallback (canonical reference; mirror structure)</ref>
    <ref type="target_file">infra/aws/terraform/inf-pipeline/eventbridge.tf (extend existing 3 rules: jwt-fetch, bronze-runner, export-schedule)</ref>
    <ref type="lambda_permission_pattern">aws_lambda_permission.allow_eventbridge_* (one per rule, sourcearn = rule arn, action = lambda:InvokeFunction, principal = events.amazonaws.com)</ref>
    <ref type="cron_flip_coordination">CTO RAVC1 + RAVC2 — these rules MUST land state="DISABLED". TO-011 (ADVI_INFETL.011-cron-flip-ack, authored by CTO post INFNNA.001 backfill RAVC ACCEPT) flips state="ENABLED" via single-attribute edit + 2-rule terraform plan + apply.</ref>
  </references>

  <context>
    INFETL §3 architecture mandates that the inf-pipeline gold chain runs daily on a
    schedule, mirroring BD's pattern. Currently inf-gold-trigger Lambda has NO
    EventBridge cron and NO S3 trigger — full gold chain runs ONLY when manually
    SSM-dispatched. This TO lands the two missing cron rules + lambda_permission
    resources, with state="DISABLED" so the rules exist as Terraform-managed resources
    BEFORE the cron-flip-ack TO (ADVI_INFETL.011) flips them to ENABLED post-backfill.

    Why DISABLED initially: per CTO RAVC1 — "if cron lands ENABLED, the first scheduled
    fire produces stale platinum because INFNNA.001 backfill is still incomplete (partial
    silver + canonical_nna). Flip ENABLED only AFTER backfill RAVC ACK so the first
    scheduled run is a clean smoke test."

    Why two rules: BD canonical pattern uses 04:00 UTC daily as primary + 23:00 UTC
    Mon-Sat as fallback. Fallback handles cases where 04:00 UTC fire missed (e.g.,
    EC2 was busy with manual QA dispatch and inf-gold-trigger pending-marker logic
    skipped the run).

    Cron-timing literal (OQ1): default 04:00 UTC overnight per BD parity. If Andrew
    rules 13:30 UTC (same-day post-bronze), AE 0.7 changes the cron literal BEFORE
    commit. Non-blocking; specifically called out by CTO RAVC2.
  </context>

  <scope>
    <step>
      Read infra/aws/terraform/inf-pipeline/eventbridge.tf — confirm existing 3 rules
      (jwt-fetch, bronze-runner, export-schedule) and their structure. Read
      infra/aws/terraform/bd-pipeline/eventbridge.tf — confirm BD canonical pattern
      (bd_canonical_prices_daily + bd_gold_nightly_fallback + 2 lambda_permission resources).
    </step>
    <step>
      Add to infra/aws/terraform/inf-pipeline/eventbridge.tf:

      resource "aws_cloudwatch_event_rule" "inf_canonical_prices_daily" {
        name                = "inf-canonical-prices-daily"
        description         = "Daily 04:00 UTC trigger for inf-gold-trigger Lambda (mode=full)"
        schedule_expression = "cron(0 4 * * ? *)"
        state               = "DISABLED"  # FLIPPED ENABLED via ADVI_INFETL.011 post INFNNA backfill
        tags                = local.common_tags
      }

      resource "aws_cloudwatch_event_target" "inf_canonical_prices_daily_target" {
        rule  = aws_cloudwatch_event_rule.inf_canonical_prices_daily.name
        arn   = aws_lambda_function.inf_gold_trigger.arn
        input = jsonencode({ "mode": "full" })
      }

      resource "aws_lambda_permission" "allow_eventbridge_inf_canonical_prices_daily" {
        statement_id  = "AllowExecutionFromEventBridgeInfCanonicalPricesDaily"
        action        = "lambda:InvokeFunction"
        function_name = aws_lambda_function.inf_gold_trigger.function_name
        principal     = "events.amazonaws.com"
        source_arn    = aws_cloudwatch_event_rule.inf_canonical_prices_daily.arn
      }

      resource "aws_cloudwatch_event_rule" "inf_gold_nightly_fallback" {
        name                = "inf-gold-nightly-fallback"
        description         = "Nightly 23:00 UTC Mon-Sat fallback trigger for inf-gold-trigger Lambda"
        schedule_expression = "cron(0 23 ? * MON-SAT *)"
        state               = "DISABLED"  # FLIPPED ENABLED via ADVI_INFETL.011 post INFNNA backfill
        tags                = local.common_tags
      }

      resource "aws_cloudwatch_event_target" "inf_gold_nightly_fallback_target" {
        rule  = aws_cloudwatch_event_rule.inf_gold_nightly_fallback.name
        arn   = aws_lambda_function.inf_gold_trigger.arn
        input = jsonencode({ "mode": "full", "fallback": true })
      }

      resource "aws_lambda_permission" "allow_eventbridge_inf_gold_nightly_fallback" {
        statement_id  = "AllowExecutionFromEventBridgeInfGoldNightlyFallback"
        action        = "lambda:InvokeFunction"
        function_name = aws_lambda_function.inf_gold_trigger.function_name
        principal     = "events.amazonaws.com"
        source_arn    = aws_cloudwatch_event_rule.inf_gold_nightly_fallback.arn
      }

      (Adjust attribute names to match existing inf-pipeline conventions if they differ.)
    </step>
    <step>
      Verify pending-marker logic in inf-gold-trigger Lambda (infra/aws/lambda/inf-gold-trigger/
      lambda_function.py or equivalent) handles the EC2-busy race. Pattern reference:
      bd-gold-trigger Lambda — when EC2 is busy with a manual SSM dispatch, the trigger
      Lambda detects via SSM ListCommands or instance state, sets a pending marker in S3,
      and the busy dispatch's wrapper checks the marker and re-dispatches at end. If
      inf-gold-trigger does NOT have this logic, AE adds a TO addendum or a new TO
      (does not block this TO; flag to COO).
    </step>
    <step>
      Pre-apply: terraform plan in infra/aws/terraform/inf-pipeline/. Expected diff:
      6 new resources (2 rules + 2 targets + 2 lambda_permissions). No drift on
      existing 3 rules.
    </step>
    <step>terraform apply (verify 0-diff post).</step>
    <step>
      AWS Console verification: both new rules present + state="DISABLED" + targets
      pointing to inf-gold-trigger ARN.
    </step>
    <step>
      Tag bump: git tag -l "inf-pipeline-v*" | sort -V | tail -5 to find latest;
      next: inf-pipeline-v1.7.X (X = next patch). git tag -a + git push --follow-tags.
    </step>
    <step>
      record-terraform-deploy.sh (per CLAUDE.md rule 14a — runs safe-commit.sh internally)
      to update CHANGELOG.json + commit + push.
    </step>
    <step>
      RAVC to COO: Terraform apply 0-diff confirmation + AWS Console screenshots/text
      proof of both rules state=DISABLED + tag bump number + post-apply terraform plan
      empty diff confirmation.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-iam service inf-gold-trigger — confirms IAM permissions sufficient for EC2 StartInstance + SSM SendCommand (no IAM gap added/required by this TO; sanity)</tool>
    <tool>comp-pipescript deployed inf-gold-trigger — parity vs BD analog (no script drift)</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">2 EventBridge rules + 2 targets + 2 lambda_permissions land via Terraform; terraform plan post-apply shows 0 diff.</criterion>
    <criterion id="AC2">Both rules visible in AWS Console with state="DISABLED".</criterion>
    <criterion id="AC3">Tag bump inf-pipeline-v1.7.X created + pushed (git tag --list confirms).</criterion>
    <criterion id="AC4">Pending-marker logic in inf-gold-trigger Lambda verified parity with bd-gold-trigger; if gap, flagged to COO with separate scope estimate (does NOT block AC1-AC3).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>None — TO-1 ships independently. First in Phase 1 sequence.</upstream>
    <downstream>
      TO-5 (S3 ObjectCreated rule) ships in same Terraform module; can land same apply or follow-on apply.
      TO-011 (cron-flip-ack) flips both rules state=DISABLED → state=ENABLED via 2-attribute Terraform edit, gated on (a) INFNNA.001 backfill RAVC ACCEPT, (b) TO-2 sentinel write live, (c) TO-3+TO-4+TO-5 publisher chain shipped + manual sentinel produces fresh platinum.
    </downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      OQ1 ruling differs from default 04:00 UTC: AE 0.7 edits the cron(0 4 * * ? *)
      literal pre-commit. Single-line change. Non-blocking.
    </risk>
    <risk>
      Pending-marker logic gap in inf-gold-trigger Lambda: AC4 surfaces this as a
      follow-on TO; do NOT block AC1-AC3 on it. Without pending-marker, the cron
      could collide with manual SSM dispatch — but rules are DISABLED initially,
      so empirical risk is zero until TO-011 flip.
    </risk>
    <risk>
      inf-gold-trigger Lambda function_name in Terraform may differ from the inferred
      aws_lambda_function.inf_gold_trigger reference name. AE uses actual reference
      from existing inf-pipeline Terraform module.
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. Cron literal default is 04:00 UTC (OQ1 default per BD parity); AE 0.7 may adjust to 13:30 UTC pre-commit if Andrew rules differently. State="DISABLED" is non-negotiable — TO-011 flip post backfill.</message>
  </go_signal>

  <revision_2026_05_07>
    Andrew direct 2026-05-07 (post INFNNA.001 root cause discovery): "lambdas should be doing
    both daily incremental ingestion and silver conversion. then our gold runner ec2 needs
    to be event-based to trigger at the receipt of all daily silver data."

    REVISED ROLE: This TO's EventBridge cron rules become FALLBACK only, not primary.

    Primary trigger path is now event-driven via:
      - INFETL.LAMBDA-DIMS (per-dim Lambdas write silver-complete sentinels)
      - INFETL.SILVER-AGGREGATOR (counts sentinels, fires gold trigger when N/N)
      - INFETL.GOLD-EVENT-TRIGGER (modifies inf-gold-trigger to accept event payload)

    Implementation impact on this TO:
      - inf_canonical_prices_daily: fallback rule. Schedule changes from 04:00 UTC to 06:00 UTC
        (gives event-path 6 hours to deliver gold; if event-driven dispatch fires before 06:00,
        idempotency check in inf-gold-trigger skips the cron-fire). State remains DISABLED
        until event-path empirically validated.
      - inf_gold_nightly_fallback: REMOVE (one fallback rule is enough; merging into the
        06:00 UTC cron above).
      - State flip via TO-011 cron-flip-ack: now flips ONLY the 06:00 UTC fallback rule
        (single rule, one state flip).

    AE 0.7: when implementing, follow this revised role rather than the original PRD
    primary-cron framing. Cross-reference INFETL.GOLD-EVENT-TRIGGER for full pattern.

    REVISION ISSUED: 2026-05-07T~18:00Z by 2.0.0_SA_COO
  </revision_2026_05_07>
</task_order>
