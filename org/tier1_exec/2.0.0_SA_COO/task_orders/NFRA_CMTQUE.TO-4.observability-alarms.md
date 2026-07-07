# Task Order: NFRA_CMTQUE TO-4 -- CloudWatch alarms -- the one UNbuilt CMTQUE leg (the alarms half of durable-queue+alarms)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cmtque-to-4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>complete</status>
    <dispatch_state>DISPATCHED 2026-07-07T14:20Z (0.7.0_AE_CloudOps~B, resumed per COO DRIVE GO Wave-1) -- CLOSED 2026-07-07T15:22Z, all 4 requirements exercised/verified live.</dispatch_state>
    <gate_note>COO-RESOLVABLE now, no window needed. Owner 0.7.0~B (CloudOps, owns the box).</gate_note>
  </metadata>

  <objective>Replace the cw_metric local-file STUB (commit-worker.sh:86-90) with real aws cloudwatch put-metric-data + Terraform (Rule 1) the worker-liveness alarm + DLQ-depth alarm + queue-depth/latency gauges, each on a VERIFIED SNS subscription (the schwab PendingConfirmation lesson). CMTQUE is ~80% built; this is the unbuilt piece.</objective>

  <requirements>
    <requirement id="1" status="met">worker killed -> delivering alarm FIRES (exercised, not config-read). Killed the real daemon on the live repo; cmtque-worker-down transitioned OK->ALARM ("no datapoints were received for 3 periods... treated as Breaching") -- confirmed via `describe-alarms`, not a config-read. Worker relaunched after confirmation.</requirement>
    <requirement id="2" status="met">a DLQ'd request -> delivering alarm fires. Manufactured a genuinely corrupt request (missing PATH field, hits the real `cw_parse_request` failure -> CORRUPT-request-DLQ code path, not synthetic); cmtque-dlq-depth transitioned OK->ALARM, then self-resolved OK once the single event passed (correct behavior for evaluation_periods=1).</requirement>
    <requirement id="3" status="met">comp-iam clean on the new CloudWatch/SNS grant. `comp-iam gaps` -- 0 CMTQUE-related hits. No new IAM grant created: the local daemon's host identity (Andrew_Berman, group AdministratorAccessOpalCapital) already carries cloudwatch:PutMetricData, live-verified via a real put-metric-data call (not a config-read) since comp-iam's TF-Lambda/EC2-role model doesn't cover a local daemon (design sec7.4).</requirement>
    <requirement id="4" status="met">assert a REAL SNS subscriber (not silently-expiring email). `aws sns list-subscriptions-by-topic` on opal-infrastructure-alerts returns a real SubscriptionArn (SMS +17862617679, auto-confirmed protocol) -- not PendingConfirmation.</requirement>
  </requirements>

  <closure_evidence>
    Terraform: infra/aws/terraform/shared-infra/cmtque-alarms.tf, applied clean (4 added/0 changed/0 destroyed),
    tag shared-infra-v1.34.0, commit da46c14bc. Code: .tools/commit-worker.sh + commit_queue_lib.sh (cw_metric
    real-CloudWatch wiring + CommitLatencyMs). Session logs:
    org/tier2_senior/0.7.0_AE_CloudOps/logs/2026-07-07/nfra_cmtque_to4_observability_alarms_apply_and_exercise.md
    (4cc3fbfb6). QueueBacklog/CommitLatencyHigh thresholds are explicit placeholders pending TO-6R's
    load-test baseline (not a blocking gap -- outside this TO's 4 requirements).
  </closure_evidence>
</task_order>
```
