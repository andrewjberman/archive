<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_INFETL.005</id>
    <project>ADVI_INFETL</project>
    <title>S3 ObjectCreated rule on gold/meta/pipeline-complete.json → inf-portal-publisher Lambda invoke (Terraform)</title>
    <issued_to>0.7.0_AE_CloudOps</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <completed_date>2026-05-11</completed_date>
    <completed_note>SHIPPED 2026-05-07 commit 7e9d30e7d (bundled with INFETL.001). COO confirmed 2026-05-11.</completed_note>
    <priority>normal</priority>
    <estimated_effort>~0.25d</estimated_effort>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_INFETL.md §3 (5-tier model, Tier 5a S3-event publisher trigger), §4.2 (publisher invocation chain), §6 Phase 1 TO-5</ref>
    <ref type="bd_pattern">infra/aws/terraform/bd-pipeline/s3-notifications.tf — aws_s3_bucket_notification.opal_data_bd lambda_function block on gold/pipeline-complete.json → bd-portal-publisher (canonical reference)</ref>
    <ref type="target_file">infra/aws/terraform/inf-pipeline/s3-notifications.tf</ref>
    <ref type="critical_constraint">Existing aws_s3_bucket_notification.opal_data_inf has eventbridge=true for the bronze sentinel chain (_BRONZE_COMPLETE.json → inf-silver-chain). The lambda_function {} block MUST be added without breaking the existing eventbridge=true config. AWS allows both attributes on a single bucket-notification resource.</ref>
    <ref type="depends_on">TO-2 (sentinel write live in dispatch.sh) + TO-3 (inf-portal-publisher Lambda functional) — both must ship before TO-5 can be empirically validated, though TO-5 Terraform can apply pre-empirical (resources exist, fire when sentinel exists).</ref>
  </references>

  <context>
    INFETL §3 architecture wires the publisher chain via S3 ObjectCreated event:
      gold/meta/pipeline-complete.json (written by orion-gold-dispatch.sh per TO-2)
        → S3 ObjectCreated event
        → inf-portal-publisher Lambda (implemented per TO-3)
        → reads gold/, writes platinum/firm/*.json
        → fans out to inf-portal-advisor-publisher (TO-4) + inf-capture-output-versions (TO-6)

    This TO lands the wire — the aws_s3_bucket_notification.opal_data_inf gets a
    lambda_function {} block keyed on gold/meta/pipeline-complete.json key + ObjectCreated
    events + filter_prefix="gold/meta/" + filter_suffix=".json". Plus a lambda_permission
    resource granting s3.amazonaws.com permission to invoke inf-portal-publisher.

    Critical preservation: existing eventbridge=true config on the bucket notification
    must not be removed. AWS bucket-notification resources support both eventbridge AND
    lambda_function blocks simultaneously — no architectural conflict.
  </context>

  <scope>
    <step>
      Read infra/aws/terraform/inf-pipeline/s3-notifications.tf — confirm existing
      aws_s3_bucket_notification.opal_data_inf has eventbridge=true (per CTO PRD §2).
      Confirm there is NO existing lambda_function {} block (this TO adds the first one).
    </step>
    <step>
      Read infra/aws/terraform/bd-pipeline/s3-notifications.tf — confirm BD canonical
      pattern for lambda_function block + filter_prefix + filter_suffix + events list.
    </step>
    <step>
      Modify aws_s3_bucket_notification.opal_data_inf to add:

      lambda_function {
        lambda_function_arn = aws_lambda_function.inf_portal_publisher.arn
        events              = ["s3:ObjectCreated:*"]
        filter_prefix       = "gold/meta/"
        filter_suffix       = "pipeline-complete.json"
      }

      Preserve existing eventbridge=true. Do NOT remove or alter the bronze-sentinel
      EventBridge wire.

      Add lambda_permission:

      resource "aws_lambda_permission" "allow_s3_invoke_inf_portal_publisher" {
        statement_id  = "AllowExecutionFromS3InfPortalPublisher"
        action        = "lambda:InvokeFunction"
        function_name = aws_lambda_function.inf_portal_publisher.function_name
        principal     = "s3.amazonaws.com"
        source_arn    = "arn:aws:s3:::opal-data-inf"
      }
    </step>
    <step>
      Pre-apply: terraform plan in infra/aws/terraform/inf-pipeline/. Expected diff:
      modify aws_s3_bucket_notification.opal_data_inf (add lambda_function block) +
      1 new resource (lambda_permission). Existing eventbridge=true preserved.
      No drift on existing resources.
    </step>
    <step>terraform apply (verify 0-diff post).</step>
    <step>
      Manual empirical (post TO-2 + TO-3 ship):
      a. Manually write a sentinel: aws s3 cp /dev/null s3://opal-data-inf/gold/meta/pipeline-complete.json
         with sample JSON body
      b. Confirm CloudWatch log /aws/lambda/inf-portal-publisher shows invocation within ~5 seconds
      c. Confirm publisher Lambda completes without IAM error (TO-3 IAM mandate gates this)
      d. Confirm fresh platinum/firm/*.json files written
    </step>
    <step>
      Daily-cron empirical (post TO-1 flip ENABLED via TO-011):
      e. First scheduled gold chain produces sentinel → publisher fires → fresh platinum
      Documented in TO-011 cron-flip-ack acceptance criteria.
    </step>
    <step>
      Tag bump: inf-pipeline-v1.7.X per latest tag discovery.
    </step>
    <step>
      record-terraform-deploy.sh updates CHANGELOG.json + commits + pushes via safe-commit.sh.
    </step>
    <step>
      RAVC to COO: terraform apply 0-diff confirmation + manual sentinel-write empirical
      result (publisher invocation CW log evidence) + tag bump number.
    </step>
  </scope>

  <compiler_mandate>
    <tool>comp-routes trace inf-portal-publisher — confirms full path: S3 sentinel → bucket-notification → Lambda → IAM → gold reads → platinum writes</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">Terraform applies clean — existing eventbridge=true on opal-data-inf bucket notification preserved (NOT removed).</criterion>
    <criterion id="AC2">Manual sentinel write triggers inf-portal-publisher Lambda invocation within ~5s (CloudWatch log evidence).</criterion>
    <criterion id="AC3">Daily-cron sentinel writes (post TO-1+TO-2 ship + TO-011 cron flip) trigger publisher (verified in TO-011 acceptance).</criterion>
    <criterion id="AC4">First end-to-end empirical run (cron → chain → sentinel → publisher → platinum) produces fresh platinum/firm/*.json files (verified in TO-011 acceptance).</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>
      TO-2 (sentinel write present in dispatch.sh) — required for empirical validation, not for terraform apply.
      TO-3 (inf-portal-publisher Lambda functional, NOT stub) — required for empirical validation.
      Both can ship in parallel with TO-5 Terraform; AC2-AC4 wait on those.
    </upstream>
    <downstream>
      TO-011 (cron-flip-ack) — TO-5 wire must be present for cron-driven publisher chain to function post flip.
    </downstream>
  </gates_dependencies>

  <risks_failure_modes>
    <risk>
      Removal of existing eventbridge=true would break bronze-silver chain (S3 → inf-silver-chain).
      AC1 explicitly verifies preservation. AE must NOT use a block-form notification config
      that overwrites the existing settings — either modify in-place or use the multi-config
      AWS notification API correctly.
    </risk>
    <risk>
      Filter prefix/suffix mismatch: if the dispatch.sh sentinel writes to a different key
      pattern than gold/meta/pipeline-complete.json, the rule will not fire. Cross-check
      with TO-2 actual sentinel-write key pre-empirical.
    </risk>
    <risk>
      Lambda execution timeout / memory: inf-portal-publisher may need higher memory_size
      or timeout than default. Out of scope here (TO-3 sets Lambda config); flag if AC2
      shows resource exhaustion.
    </risk>
  </risks_failure_modes>

  <go_signal>
    <issued_at>pending Andrew confirmation of OQ1+OQ8+INFNNA-scope</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>HOLD. TO authored pre-Andrew GO per CTO RAVC2 authorization. Can ship Terraform pre-empirical (resources exist before TO-2/TO-3 land); AC2-AC4 verified post TO-3 ship.</message>
  </go_signal>
</task_order>
