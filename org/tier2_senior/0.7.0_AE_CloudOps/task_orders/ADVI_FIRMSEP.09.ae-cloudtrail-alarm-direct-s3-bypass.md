<?xml version="1.0" encoding="UTF-8"?>
<task_order>
  <metadata>
    <id>ADVI_FIRMSEP.09</id>
    <project>ADVI_FIRMSEP</project>
    <title>Phase 2 — CloudTrail alarm on direct S3 access to opal-data-{bd,inf,cot} bypassing CloudFront</title>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_date>2026-05-07</issued_date>
    <status>complete</status>
    <priority>medium</priority>
    <estimated_effort>~0.5d</estimated_effort>
    <completed_date>2026-05-11</completed_date>
    <completed_commit>63358ee24 (TF rule) + cloudwatch-alarms.tf CT-enabled comment update (this session)</completed_commit>
    <completed_by>0.7.0_AE_CloudOps</completed_by>
    <completion_note>EventBridge rule FIRMSEP-s3-direct-access-bypass deployed + ENABLED. CT S3 data events enabled 2026-05-11 per COO GO (ReadOnly selector on opal-data-bd + opal-data-inf). Empirical bypass test (aws s3api get-object from non-CF context): GetObject submitted ~19:39Z. AC4 PASS CONFIRMED: TriggeredRules=21, Invocations=21 (0 failed) across 19:40-19:45Z windows. SNS delivery to opal-infrastructure-alerts: 100%. All ACs DONE.</completion_note>
  </metadata>

  <references>
    <ref type="prd">docs/architecture/ADVI_FIRMSEP.md §4.7 + §6 Phase 2.09 + §7.OQ6</ref>
    <ref type="targets">opal-data-bd, opal-data-inf, opal-data-cot (+ cot once Cottonwood ships)</ref>
    <ref type="sns_topic">opal-infrastructure-alerts</ref>
    <ref type="oq_default">OQ6 default: alarm on EVERY non-CF source IP; allowlist via CW alarm suppression rule for known-good source IP CIDRs (e.g., Opal staff outbound IPs for diagnostic access).</ref>
  </references>

  <context>
    All firm-bucket reads SHOULD flow through CloudFront → OAI → S3. Direct S3 GetObject
    requests outside CloudFront are signals of:
      - Operational diagnostic access (CTO/AE during debugging)
      - IAM role misconfiguration allowing app-layer to bypass
      - Compromised credentials accessing buckets directly
      - Data exfiltration attempt

    Today: NO alarm. CloudTrail logs the events but no detection.

    Fix: CloudTrail event selector + EventBridge rule (or CW Logs metric filter on CT log
    group) → CW alarm on s3:GetObject events on opal-data-{bd,inf,cot}/* with source IP
    NOT in CloudFront edge ranges.

    OQ6 resolved per CTO default: alarm on every non-CF source; allowlist via SNS subscription
    filter or CW alarm composite-rule for known-good Opal staff CIDRs. Initial scope: alarm
    on all; add allowlist incrementally as ops noise surfaces.

    NOTE: CloudFront edge IP ranges are vast and change. Easiest matcher: `userAgent` field
    (CloudFront sets `Amazon CloudFront`) OR `vpcEndpointId` (if VPC endpoint is used) OR
    `sourceIPAddress != "AWS Internal"` AND not in published CF IP ranges.
    Decision: filter on `userAgent` field — if NOT matching CloudFront UA → alarm. Simpler
    than maintaining a CF IP CIDR allowlist.
  </context>

  <scope>
    <step>
      Verify CloudTrail data event logging is enabled for the firm buckets:
        aws cloudtrail get-event-selectors --trail-name <trail-name>
      If S3 data events NOT logged: enable for opal-data-bd, opal-data-inf (write to a
      data-events trail; this can be expensive — verify Andrew acknowledges $ before enabling
      if not already on). If already on: proceed.
    </step>
    <step>
      Decide implementation approach:
        OPTION 1 — CW Logs metric filter on CloudTrail log group:
          - CT logs events to a CW Log group; pattern-match s3:GetObject + bucket + non-CF UA.
          - Promote to CW metric → CW alarm.
        OPTION 2 — EventBridge rule on CT events:
          - EventBridge rule with pattern matching s3:GetObject + bucket-arn list + non-CF UA.
          - Target: Lambda OR SNS (or both).
        OPTION 3 — CT Insights with Athena query + scheduled Lambda emitting CW metric.
          - Most flexible; highest setup cost.
      CTO recommendation: Option 2 (EventBridge) — cleanest separation, easiest to maintain.
      If EventBridge rule complexity for non-CF UA matching is constraining, fall back to
      Option 1 with regex on userAgent field.
    </step>
    <step>
      EventBridge rule (Option 2) Terraform:
        resource "aws_cloudwatch_event_rule" "firmsep_s3_bypass" {
          name = "FIRMSEP-s3-direct-access-bypass"
          description = "FIRMSEP.09: alarm on s3:GetObject to firm buckets bypassing CloudFront"
          event_pattern = jsonencode({
            source = ["aws.s3"]
            "detail-type" = ["AWS API Call via CloudTrail"]
            detail = {
              eventName = ["GetObject"]
              requestParameters = {
                bucketName = ["opal-data-bd", "opal-data-inf", "opal-data-cot"]
              }
              userAgent = [{ "anything-but" = ["Amazon CloudFront"] }]
            }
          })
        }
        resource "aws_cloudwatch_event_target" "firmsep_s3_bypass_sns" {
          rule = aws_cloudwatch_event_rule.firmsep_s3_bypass.name
          target_id = "sns"
          arn = aws_sns_topic.opal_infrastructure_alerts.arn
        }
    </step>
    <step>
      Optional: companion CW Log group + metric for trend visibility (count of bypass events
      over time). Promote to CW alarm (e.g., > 0 events in any 5-minute period → ALARM).
    </step>
    <step>
      Allowlist scaffold (do NOT populate yet; add incrementally as ops noise surfaces):
        - Document allowlist mechanism: SNS subscription filter on payload field, OR
          composite CW alarm with secondary metric for allowlisted CIDRs.
        - Initial state: empty allowlist; ALL non-CF accesses page.
    </step>
    <step>
      terraform plan / apply. ZERO modifications to existing resources expected. Plan diff
      should be ADD-only.
    </step>
    <step>
      Empirical: from a non-CF context (e.g., aws s3 cp s3://opal-data-bd/test.json - on
      laptop), verify alarm fires + SNS notification arrives. Capture eventId + alarm
      transition timestamp.
    </step>
    <step>
      Tag bump shared-infra-vX.Y.Z (or wherever CT alarms live). record-terraform-deploy.
    </step>
    <step>
      RAVC to COO: alarm definition + empirical-trigger evidence + SNS delivery confirmation
      + allowlist scaffold doc.
    </step>
  </scope>

  <compiler_mandate>
    <tool>aws cloudtrail get-event-selectors — confirm S3 data events on relevant buckets logged</tool>
    <tool>aws events list-rules — confirm rule registered post-apply</tool>
    <tool>empirical bypass test (aws s3 cp from laptop) — alarm + SNS</tool>
  </compiler_mandate>

  <acceptance_criteria>
    <criterion id="AC1">CloudTrail S3 data events logged for opal-data-{bd,inf} (cot pre-creation).</criterion>
    <criterion id="AC2">EventBridge rule (or CW Logs metric filter) registered for non-CF s3:GetObject pattern.</criterion>
    <criterion id="AC3">SNS-to-opal-infrastructure-alerts wired.</criterion>
    <criterion id="AC4">Empirical: laptop aws s3 cp on bucket → alarm fires + SNS notification within 1-5 min.</criterion>
    <criterion id="AC5">Allowlist scaffold + mechanism documented; ZERO entries on initial deploy (alarm on all bypass).</criterion>
    <criterion id="AC6">Tag bump + record-terraform-deploy.</criterion>
    <criterion id="AC7">FIRMSEP.10 will add opal-data-cot to the bucket-name list at Cottonwood ship time.</criterion>
  </acceptance_criteria>

  <gates_dependencies>
    <upstream>Phase 1 ships first.</upstream>
    <downstream>FIRMSEP.10 updates the rule's bucket list to include opal-data-cot.</downstream>
  </gates_dependencies>

  <go_signal>
    <issued_at>20260507T~19:55Z</issued_at>
    <issued_by>2.0.0_SA_COO</issued_by>
    <message>GO post Phase 1. OQ6 default: alarm-on-all + allowlist scaffold (empty initial). Option 2 (EventBridge) preferred. Verify CT data events on first; if disabled, surface to COO before enabling ($ implication). RAVC with empirical bypass-trigger.</message>
  </go_signal>
</task_order>
