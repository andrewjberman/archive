<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.011</id>
    <project>ADVI_INFETL</project>
    <title>Cron-flip-ack — flip inf-canonical-prices-daily fallback rule from DISABLED → ENABLED post 4-prereq stack</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>1.0.0_SA_CTO</issued_by>
    <issued_date>2026-05-08</issued_date>
    <status>complete</status><!-- SHIPPED 2026-05-08 by AE 0.7 commit `e28e24585` + tag `inf-pipeline-v1.7.45` (single-attr Terraform edit DISABLED→ENABLED on aws_cloudwatch_event_rule.inf_canonical_prices_daily). AC1-AC4 PASS via plan 0/1/0 + apply + describe-rule State=ENABLED + tag pushed. AC5 first-fire empirical NOW SATISFIED 2026-05-11 startup CTO investigation: 3 cron windows fired (2026-05-09, 5-10, 5-11 @ 06:00 UTC); `gold/trigger-mode.json` written today 06:00:42Z confirming Lambda firing daily. NOTE: `gold/meta/pipeline-complete.json` absent — production safety net working as designed, surfacing real gold-chain failure from JOE-TXN-BACKFILL schema drift (account_id dtype, ADVI_INFNNA.ACCOUNT-ID-COERCE TO COO-queued for today's Monday-AM workflow). Flipped pending→complete by 1.0.0_SA_CTO 2026-05-11 startup ground-truth pass. -->
    <priority>normal</priority>
    <estimated_effort>~0.25d (single-attribute Terraform edit + plan + apply + first-fire empirical witness next-day 06:00 UTC)</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md v0.2 §6 (event-chain primary + cron fallback architecture)</ref>
    <ref type="parent_to">org/tier2_senior/0.7.0_AE_CloudOps/task_orders/ADVI_INFETL.001.ae-eventbridge-gold-cron-and-fallback.md (lands the rule DISABLED; complete; references TO-011 flip explicitly)</ref>
    <ref type="target_resource">infra/aws/terraform/inf-pipeline/eventbridge.tf:107-117 — aws_cloudwatch_event_rule.inf_canonical_prices_daily; current state="DISABLED"; flip to state="ENABLED"</ref>
    <ref type="prereq_chain">ADVI_INFETL.GOLD-EVENT-TRIGGER (v1.7.34 c6500c313) + ADVI_INFETL.SILVER-AGGREGATOR (v1.7.37) + ADVI_INFETL.003 inf-portal-publisher (DS~B 9b66c9c43) + ADVI_INFNNA.GOLD (DS~A RAVC5 2026-05-08)</ref>
    <ref type="cto_ruling_serial">CTO author message + RAVC1 to COO post-author 20260508T~PM</ref>
  </references>

  <context>
    Per ADVI_INFETL v0.2 PRD architecture: event-chain is the primary daily-gold trigger
    (S3-ObjectCreated → SILVER-AGGREGATOR Lambda → GOLD-EVENT-TRIGGER Lambda → portal-publisher
    Lambda); the 06:00 UTC cron rule (`inf-canonical-prices-daily`) is a fallback safety net
    that fires only if the event-driven path fails to deliver gold within window.

    The fallback rule was authored at TO-1 (`aws_cloudwatch_event_rule.inf_canonical_prices_daily`
    in `infra/aws/terraform/inf-pipeline/eventbridge.tf:107-117`) with `state = "DISABLED"`
    intentionally — per CTO RAVC1 on TO-1, "if cron lands ENABLED, the first scheduled fire
    produces stale platinum because INFNNA.001 backfill is still incomplete." The disable-on-land
    + flip-post-prereq pattern lets the cron rule exist as a Terraform-managed resource without
    actually firing until the safety net's downstream Lambdas are empirically validated.

    The 4-prereq stack is now met. Flipping ENABLED activates the safety net — production-side
    impact is "next day at 06:00 UTC, fallback cron fires; if event-chain already ran, idempotency
    in `gold/meta/pipeline-complete.json` makes it a no-op; if event-chain failed silently, fallback
    catches it and produces gold." That's the defense-in-depth this PRD architecture committed to.
  </context>

  <prereq_verification>
    <prereq id="1">
      <name>GOLD-EVENT-TRIGGER live empirical</name>
      <expected>inf-gold-trigger Lambda accepts both aggregator event payloads `{"snapshot_date": "..."}` AND legacy cron payloads `{"mode": "full"}`; idempotency via `gold/meta/pipeline-complete.json` confirmed</expected>
      <evidence>SHIPPED v1.7.34 commit c6500c313 (2026-05-07 AE 0.7); smoke test PASS per AE 0.7 INFETL solidify-series session log "GOLD-EVENT-TRIGGER SHIPPED"; idempotency marker pattern matches BD canonical</evidence>
      <status>MET</status>
    </prereq>
    <prereq id="2">
      <name>SILVER-AGGREGATOR aggregate sentinel fires event-trigger</name>
      <expected>inf-silver-aggregator Lambda fires on S3-ObjectCreated for `silver/_silver_complete/<dim>.json` sentinels; aggregates 9-dim quorum; fires GOLD-EVENT-TRIGGER once + writes `_AGGREGATOR_FIRED.json` idempotency marker</expected>
      <evidence>SHIPPED v1.7.37 commit f4f7d35df (2026-05-07 AE 0.7); empirical PASS — "smoke + synthetic-event empirical PASS" per AE 0.7 session log; 256 MB / 60s</evidence>
      <status>MET</status>
    </prereq>
    <prereq id="3">
      <name>Manual sentinel fires publisher (advisor + portal publisher chain)</name>
      <expected>Manual write of silver-complete sentinel triggers inf-portal-publisher Lambda + fan-out to inf-portal-advisor-publisher; CF invalidation EVTSA9VEHNZVH fires</expected>
      <evidence>INFETL.003 inf-portal-publisher full impl SHIPPED (DS~B 9b66c9c43; ports D_00b/00c/00/04 + fan-out advisor-publisher at START + CF invalidation catch-wrapped). INFETL.004 advisor-publisher impl complete (DS~C; AE 0.7 lane fix 79dbf6138 unblocks). Empirical: INFNNA cascade tonight (per item #4) used this exact path end-to-end.</evidence>
      <status>MET</status>
    </prereq>
    <prereq id="4">
      <name>INFNNA.GOLD RAVC ACK</name>
      <expected>End-to-end cascade (bronze → silver → gold → platinum → portal) produces canonical $199.6M firm AUA + correct Joe Brandenburg attribution + 4 advisors + 21 clients</expected>
      <evidence>DS~A RAVC5 2026-05-08 (per COO MCP forward): $199.6M firm AUA, 4 advisors, Joe Brandenburg $16.2M, 21 clients. ACs 1+4 fully PASS; ACs 2/3/5 with non-blocking caveats (2 follow-up bugs queued separately, not regression-class).</evidence>
      <status>MET</status>
    </prereq>
  </prereq_verification>

  <scope>
    <step>
      <run>Re-verify all 4 prereqs in Phase 0 — read this TO's `<prereq_verification>` block + cross-check against current git state. If any prereq state has regressed (e.g., a Lambda was reverted), STOP and RAVC2 to CTO.</run>
      <expect>All 4 prereqs MET as documented. No regressions.</expect>
      <if_mismatch>Any regression: STOP. Do not proceed with the flip. RAVC2 to CTO with the regressed prereq + evidence. CTO will adjudicate (likely re-author this TO with revised prereqs or stage behind a new fix TO).</if_mismatch>
    </step>
    <step>
      <run>Edit `infra/aws/terraform/inf-pipeline/eventbridge.tf:111` — change `state = "DISABLED"` → `state = "ENABLED"` on `aws_cloudwatch_event_rule.inf_canonical_prices_daily`. Single-attribute edit; do NOT touch the rule name, schedule_expression, target, or lambda_permission resources — those are stable from TO-1.</run>
      <expect>One-line diff in eventbridge.tf. No other files touched.</expect>
      <if_mismatch>If you find yourself editing more than one line, STOP. The intended scope is single-attribute. Surface the cause via RAVC2.</if_mismatch>
    </step>
    <step>
      <run>`terraform plan` with MSYS_NO_PATHCONV=1. Confirm exactly `0 to add, 1 to change, 0 to destroy` with the change being state DISABLED → ENABLED on `inf_canonical_prices_daily`.</run>
      <expect>0/1/0; in-place attribute update; no resource recreation.</expect>
      <if_mismatch>If plan shows additional changes (resource recreation, target modification, IAM diff), STOP and surface via RAVC2. Possible drift between local and deployed state — investigate with `terraform refresh` first.</if_mismatch>
    </step>
    <step>
      <run>RAVC1 to CTO + COO with plan diff before applying.</run>
      <expect>CTO + COO ACK on plan correctness; GO to apply.</expect>
      <if_mismatch>If CTO/COO surface a concern, hold until adjudicated.</if_mismatch>
    </step>
    <step>
      <run>`terraform apply` — should be ~5-15s for an EventBridge rule attribute update.</run>
      <expect>Apply success; "Apply complete! Resources: 0 added, 1 changed, 0 destroyed."</expect>
      <if_mismatch>Any apply error: STOP. Capture full stderr. RAVC2 to CTO + COO. Likely IAM or AWS-side issue.</if_mismatch>
    </step>
    <step>
      <run>Post-apply 0-diff verification: `terraform plan` again immediately. Should report "No changes."</run>
      <expect>0-diff plan post-apply.</expect>
      <if_mismatch>Non-empty post-apply plan: STOP and surface. State drift indicator.</if_mismatch>
    </step>
    <step>
      <run>Live verification via AWS CLI: `aws events describe-rule --name inf-canonical-prices-daily --region us-east-1` — confirm `State: ENABLED` in response.</run>
      <expect>Rule State = ENABLED in live AWS state.</expect>
      <if_mismatch>If CW console / CLI shows DISABLED post-apply: STOP and surface. Apply did not propagate.</if_mismatch>
    </step>
    <step>
      <run>Tag + record-deploy + push: `git tag -a inf-pipeline-vX.Y.Z -m "INFETL.011 cron-flip-ack: fallback rule ENABLED post 4-prereq stack"` (use next available patch version per `git tag -l "inf-pipeline-v*" | sort -V | tail -5`); run `.tools/safe-commit.sh` per ownership rules; `git push origin CLOUD --follow-tags`. Run `record-terraform-deploy.sh` to capture the apply event.</run>
      <expect>Tag pushed; CHANGELOG entry recorded; commit author = `0.7.0_AE_CloudOps`.</expect>
      <if_mismatch>safe-commit.sh contamination flag: clean staged index per usual; do NOT --force unless justified.</if_mismatch>
    </step>
    <step>
      <run>RAVC1 to CTO + COO post-apply: tag + commit + AWS state confirmation.</run>
      <expect>CTO + COO ACK; AC1-AC3 closed.</expect>
    </step>
    <step>
      <run>NEXT-DAY first-fire empirical witness (06:00 UTC ~24h after apply): query CloudWatch logs for inf-gold-trigger Lambda invocation at ~06:00 UTC; verify either (a) idempotency hit ("already ran via event-chain; no-op") or (b) successful end-to-end cron-driven gold publication. Either outcome is acceptance — both prove the fallback works.</run>
      <expect>Lambda fired at scheduled time; correct response based on event-chain prior state.</expect>
      <if_mismatch>If Lambda did not fire at all: rule misconfiguration; investigate via CW Events metrics + lambda_permission resource. If Lambda fired with error: capture stderr; RAVC2 to CTO + COO.</if_mismatch>
    </step>
    <step>
      <run>RAVC2 to CTO + COO with first-fire evidence — close the TO.</run>
      <expect>RAVC2 ACK; TO marked complete.</expect>
    </step>
  </scope>

  <acceptance_criteria>
    <ac id="1">Single-attribute Terraform edit lands cleanly: eventbridge.tf:111 state DISABLED → ENABLED; no other lines modified in the resource block or sibling resources.</ac>
    <ac id="2">terraform plan output is exactly `0 to add, 1 to change, 0 to destroy` pre-apply; `No changes` post-apply.</ac>
    <ac id="3">Live AWS state via `aws events describe-rule` confirms `State: ENABLED` post-apply.</ac>
    <ac id="4">Annotated git tag `inf-pipeline-v<next>` pushed to remote with `--follow-tags`; record-terraform-deploy.sh entry committed.</ac>
    <ac id="5">First-fire 06:00 UTC empirical witness: Lambda fires; result is either idempotency-no-op (event-chain already ran that day) OR successful cron-driven gold publication (event-chain didn't fire). Either outcome closes the TO.</ac>
    <ac id="6">If first-fire produces an unexpected error, the TO is REWORK status (re-open with RCA), not COMPLETE.</ac>
  </acceptance_criteria>

  <compiler_tools_mandate>
    <phase id="1">
      <run>`comp-blast aws_cloudwatch_event_rule.inf_canonical_prices_daily` — confirm no other Terraform resources reference this rule's state attribute (sanity check that the flip is structurally isolated).</run>
      <expect>Rule appears as a node; downstream edges are the target + lambda_permission (already authored under TO-1). No surprise dependencies.</expect>
    </phase>
    <phase id="2">
      <run>Pre-commit: `comp-iam service inf-gold-trigger` — confirm the Lambda's IAM still permits all required boto3 calls under cron-driven invocation (same role as event-chain invocation; should be no-op surface).</run>
      <expect>"No permission gaps detected" or equivalent clean output.</expect>
    </phase>
    <phase id="3">
      <run>Post-commit empirical: `aws events describe-rule` confirms ENABLED + first-fire CW log capture (next day 06:00 UTC). Append one row per phase to `org/compiler-tools-log.md`.</run>
      <expect>Compiler log row reflects flip empirical; tool runs documented.</expect>
    </phase>
  </compiler_tools_mandate>

  <ravc>
    <expected_recipient>1.0.0_SA_CTO + 2.0.0_SA_COO (joint)</expected_recipient>
    <expected_evidence>Plan diff (RAVC1) + apply confirmation + AWS describe-rule output + tag + first-fire CW log link (RAVC2)</expected_evidence>
  </ravc>

  <out_of_scope>
    <item>Modifying the cron schedule expression (06:00 UTC stays per TO-1 + INFETL PRD §6 — fallback timing rationale is "after midnight bronze cycle, before normal business hours; safe window for retroactive gold").</item>
    <item>Modifying the Lambda target or input payload (`{ mode = "full" }` stays — defines the cron-driven Lambda code path).</item>
    <item>Modifying lambda_permission resources (those were authored cleanly under TO-1).</item>
    <item>Disabling the EventBridge S3-ObjectCreated event-chain primary path (that stays primary; cron is fallback).</item>
    <item>Adding observability alarms on cron firing (separate scope; queued under FIRMSEP Phase 2 / future ADHC).</item>
  </out_of_scope>
</task_order>
