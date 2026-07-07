# Task Order: NFRA_CMTQUE TO-4 -- CloudWatch alarms -- the one UNbuilt CMTQUE leg (the alarms half of durable-queue+alarms)

```xml
<task_order>
  <metadata>
    <id>2.0.0_SA_COO-2026-07-07-nfra-cmtque-to-4</id>
    <issued_by>2.0.0_SA_COO</issued_by>
    <issued_to>0.7.0_AE_CloudOps~B</issued_to>
    <date>2026-07-07</date>
    <status>ready</status>
    <dispatch_state>WRITTEN-NOT-DISPATCHED (wind-down 2026-07-07; Andrew directed decomposition materialized before device reboot; dispatch on restart per the allocation-map in the session handoff /log)</dispatch_state>
    <gate_note>COO-RESOLVABLE now, no window needed. Owner 0.7.0~B (CloudOps, owns the box).</gate_note>
  </metadata>

  <objective>Replace the cw_metric local-file STUB (commit-worker.sh:86-90) with real aws cloudwatch put-metric-data + Terraform (Rule 1) the worker-liveness alarm + DLQ-depth alarm + queue-depth/latency gauges, each on a VERIFIED SNS subscription (the schwab PendingConfirmation lesson). CMTQUE is ~80% built; this is the unbuilt piece.</objective>

  <requirements>
    <requirement id="1">worker killed -> delivering alarm FIRES (exercised, not config-read)</requirement>
    <requirement id="2">a DLQ'd request -> delivering alarm fires</requirement>
    <requirement id="3">comp-iam clean on the new CloudWatch/SNS grant</requirement>
    <requirement id="4">assert a REAL SNS subscriber (not silently-expiring email)</requirement>
  </requirements>
</task_order>
```
